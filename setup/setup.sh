#!/bin/bash

zipline ingest -b quantopian-quandl
mv dotzipline.tgz ~/.zipline/
tar -xvzf ~/.zipline/dotzipline.tgz -C ~/.zipline/
mkdir ~/.zipline/data/alpaca/2018-06-11T20\;08\;42.452595/minute_equities.bcolz
cp `find ~/.zipline/ -name "metadata.json"` ~/.zipline/data/alpaca/2018-06-11T20\;08\;42.452595/minute_equities.bcolz/
cp `find ~/.zipline/data/quantopian-quandl -name "adjustments.sqlite"` ~/.zipline/data/alpaca/2018-06-11T20\;08\;42.452595/
