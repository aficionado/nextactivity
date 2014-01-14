Next Activity
=============

Predicting Sean's next activity using [Sean J. Taylor](https://github.com/seanjtaylor) ([@seanjtaylor](https://twitter.com/seanjtaylor))'s Basis watch data.

## Getting the data

1. Fork, clone, or just [download](https://github.com/seanjtaylor/basis/blob/master/data/clean/states_10011230.csv) latest data from [Sean's repo](https://github.com/seanjtaylor/basis)

**Note**: Isn't clear to me whether dates have been applied TZ conversion in the clean data or not. But that would be an easy fix.

## Analyzing the data
1. Install bigmler:

        pip install bigmler

2. Set up your BIGML_USERNAME and BIGML_API_KEY

3. Run the script.

 		./next_activity.py --source basis/data/clean/states_10011230.csv  --balance --share

	    [2014-01-14 12:05:39] Creating source...
	    [2014-01-14 12:05:43] Creating dataset...
	    [2014-01-14 12:05:46] Transforming dataset...
	    [2014-01-14 12:05:48] Splitting dataset...
	    [2014-01-14 12:05:53] Creating a model using the training dataset...
	    [2014-01-14 12:05:55] Evaluating model against the test dataset...
	    [2014-01-14 12:05:59] Creating model for the full dataset...
	    [2014-01-14 12:06:02] Sharing resources...
	    [2014-01-14 12:06:04] https://bigml.com/shared/dataset/pNCDHYn75BLRTtB9GF3ULZiJPcb
	    [2014-01-14 12:06:04] https://bigml.com/shared/model/mZpNgH26YHG7NLLI82ujAyW5pdJ
	    [2014-01-14 12:06:04] https://bigml.com/shared/evaluation/zcwx4rk003IZxXQtUX52zPu8Sy9

## Visualizing the data

* [dataset](https://bigml.com/shared/dataset/pNCDHYn75BLRTtB9GF3ULZiJPcb)

<img src="https://raw.github.com/aficionado/nextactivity/master/images/dataset.png" alt="Dataset">

* [model](https://bigml.com/shared/model/mZpNgH26YHG7NLLI82ujAyW5pdJ)

<img src="https://raw.github.com/aficionado/nextactivity/master/images/sunburst.png" alt="Sunburst">

* [evaluation](https://bigml.com/shared/evaluation/zcwx4rk003IZxXQtUX52zPu8Sy9)

<img src="https://raw.github.com/aficionado/nextactivity/master/images/confusion_matrix.png" alt="Evaluation">


