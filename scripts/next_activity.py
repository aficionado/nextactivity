#!/usr/bin/env python
# -*- coding: utf-8 -*-

##############################################################################
# Copyright (c) 2014 BigML, Inc
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
##############################################################################
"""Playing with Sean Taylor's activity data.

"""

import sys
import argparse

from bigml.api import BigML
from bigml.fields import Fields
from bigmler.utils import log_message, dated


def log(message):
    """Dates and logs messsage.

    """
    log_message(dated(message.rstrip('\n') + '\n'),  console=1)


def train_test_split(api, dataset, rate=0.8, seed='seed'):
    """Generates disjoint training and test sets.

    """
    training_set = api.create_dataset(dataset, {
        'sample_rate': rate,
        'seed': seed})
    test_set = api.create_dataset(dataset, {
        'sample_rate': rate,
        'seed': seed,
        'out_of_bag': True})

    if api.ok(training_set) and api.ok(test_set):
        return training_set, test_set


def share_dataset(api, dataset):
    """Creates a secret link to share `dataset`.

    """
    dataset = api.update_dataset(dataset, {"shared": True})
    if api.ok(dataset):
        return ("https://bigml.com/shared/dataset/%s" %
                dataset['object']['shared_hash'])


def share_model(api, model):
    """Creates a secret link to share `model`.

    """
    model = api.update_model(model, {"shared": True})
    if api.ok(model):
        return ("https://bigml.com/shared/model/%s" %
                model['object']['shared_hash'])


def share_evaluation(api, evaluation):
    """Creates a secret link to share `evaluation`.

    """
    evaluation = api.update_evaluation(evaluation, {"shared": True})
    if api.ok(evaluation):
        return ("https://bigml.com/shared/evaluation/%s" %
                evaluation['object']['shared_hash'])


def previous_activity():
    """Flatline s-expression for the value of the previous activity.

    """
    return ["f", "activity", -1]


def previous_duration():
    """Flatline s-expression of the duration of previous activity in minutes.

    """
    return ["integer", ["/", ["-", ["f", "end", -1], ["f", "start", -1]], 60]]


def start_day():
    """Day of the week using start date.

    """
    return ["epoch-weekday", ["*", 1000, ["f", "start"]]]


def end_day():
    """Hour of start date.

    """
    return  ["epoch-hour", ["*", 1000, ["f", "start"]]]


def new_fields():
    """New field params.
    """
    return [
        {"name": "previous activity", "field": previous_activity()},
        {"name": "previous duration", "field": previous_duration()},
        {"name": "start.weekday", "field": start_day()},
        {"name": "start.hour", "field": end_day()}]


def excluded_fields():
    """Lists first column of dataset and timestamps.

    """
    return ["field1", "start", "end"]


def main(args=sys.argv[1:]):
    """Parses command-line parameters and calls the actual main function.

    """
    parser = argparse.ArgumentParser(
        description="Dataset analysis",
        epilog="BigML, Inc")

    # source with activity data
    parser.add_argument('--source',
                        action='store',
                        dest='source',
                        default=None,
                        help="Full path to file")

    # create private links or not
    parser.add_argument('--share',
                        action='store_true',
                        default=False,
                        help="Share created resources or not")

    # weight models or not
    parser.add_argument('--balance',
                        action='store_true',
                        default=False,
                        help="Weight model or not")

    args = parser.parse_args(args)

    if not args.source:
        sys.exit("You need to provide a valid path to a source")

    api = BigML()

    name = "Sean's activity"

    log("Creating source...")
    source_args = {'name': name}
    source = api.create_source(args.source, source_args)
    if not api.ok(source):
        sys.exit("Source isn't ready...")

    log("Creating dataset...")
    dataset = api.create_dataset(source)
    if not api.ok(dataset):
        sys.exit("Dataset isn't ready...")

    log("Transforming dataset...")
    # Extends dataset with new field for previous activity, previous duration,
    # start day, and start hour. Removes first column, start, and end fields.
    new_dataset_args = {
        'name': name,
        'new_fields': new_fields(),
        'all_but': excluded_fields()}
    new_dataset = api.create_dataset(dataset, new_dataset_args)
    if not api.ok(new_dataset):
        sys.exit("Dataset isn't ready...")

    # Set objective field to activity
    fields = Fields(new_dataset['object']['fields'])
    objective_id = fields.field_id('activity')
    new_dataset_args = {
        'objective_field': {'id': objective_id}}
    new_dataset = api.update_dataset(new_dataset, new_dataset_args)

    # Create training and test set for evaluation
    log("Splitting dataset...")
    training, test = train_test_split(api, new_dataset)

    log("Creating a model using the training dataset...")
    model_args = {
        'objective_field': objective_id,
        'balance_objective': args.balance,
        'name': training['object']['name']}
    model = api.create_model(training, model_args)
    if not api.ok(model):
        sys.exit("Model isn't ready...")

    # Creating an evaluation
    log("Evaluating model against the test dataset...")
    eval_args = {
        'name': name + ' - 80% vs 20%'}
    evaluation = api.create_evaluation(model, test, eval_args)
    if not api.ok(evaluation):
        sys.exit("Evaluation isn't ready...")

    log("Creating model for the full dataset...")
    model = api.create_model(new_dataset, model_args)
    if not api.ok(model):
        sys.exit("Model isn't ready...")

    # Create private links
    if args.share:
        log("Sharing resources...")
        dataset_private_link = share_dataset(api, new_dataset)
        model_private_link = share_model(api, model)
        evaluation_private_link = share_evaluation(api, evaluation)
        log(dataset_private_link)
        log(model_private_link)
        log(evaluation_private_link)

if __name__ == "__main__":
    main()
