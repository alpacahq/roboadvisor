FROM python:3.6

WORKDIR /home/robo-advisor
ADD . /home/robo-advisor

RUN apt-get update && apt-get install -y \
	libatlas-base-dev \
	python-dev \
	gfortran \
	pkg-config \
	vim \
	libfreetype6-dev

RUN pip install pandas==0.18.1 \
				urllib3==1.21.1 \
				pymarketstore \
				zipline \
				ConfigParser \
				matplotlib \
				alpaca-trade-api

RUN zipline ingest -b quantopian-quandl
RUN mv setup/dotzipline.tgz /root/.zipline/
RUN rm /root/.zipline/extension.py
RUN tar -xvzf /root/.zipline/dotzipline.tgz -C /root/.zipline/
RUN mkdir /root/.zipline/data/alpaca/2018-06-11T20\;08\;42.452595/minute_equities.bcolz
RUN cp `find /root/.zipline/ -name "metadata.json"` /root/.zipline/data/alpaca/2018-06-11T20\;08\;42.452595/minute_equities.bcolz/
RUN cp $(find /root/.zipline/data/quantopian-quandl -name "adjustments.sqlite") /root/.zipline/data/alpaca/2018-06-11T20\;08\;42.452595/
