# roboadvisor

## Introduction
Robo advisors are automated advising services that require little to no user interaction. They specialize in maintaining portfolios based on the investors chosen risk level. The first robo-advisor was launched at the start of the financial crisis in 2008.

The logic for a robo-advisor takes place in 3 stages:
  - Allocation - Given a risk level, portions of capital are allocated to different positions.
  - Distance - Over a regular time interval, the adviser scans to see if there’s a significant change in the portfolio balance
  - Rebalancing - Buys and Sells stock 

## Source Material
At this point, the robo-advisor does not use mean-variance optimization to allocate. The risk-based weight allocation is taken from this [Vanguard Portfolios](https://advisors.vanguard.com/iwe/pdf/FASINVMP.pdf). Each series its individual universe. 

## Contents
The src files in the repo contain a robo advisor in three distinct stages.

 - buy-and-hold.py: Allocates weights based on risk, and orders appropriate number of shares
 - distance.py: Allocates based on risk. Continually checks the distance
 - robo-advisor.py: A fully functioning robo-advisor with all 3 stages as well as all 6 Vanguard universes implemented. 


## Running Locally
If you're interested in running the code locally, there are dependencies to install, and steps to take.
1. Install Zipline. 
2. Install the alpaca-trade-api. It's necessary for bundle use. 
3. Ingest the bundle that contains ticker data for backtesting

You can find OS-specific installation instructions for zipline [here](http://www.zipline.io/install.html). I'm going to second their recommendation to run zipline in either a virtual environment. You can find installation instructions for the alpaca-trade-api [here](https://github.com/alpacahq/alpaca-trade-api-python). 

To ingest the bundle. Run the following command after cloning the repository:
```
$./setup/setup.sh
```


## Running with Docker
If you're interested in running backtesting in a docker container, this repository is configured to do so. Running the following commands will create and launch a docker images that has all necessary dependencies installed, as well as the alpaca bundle ingested.

```
$git clone https://github.com/alpacahq/roboadvisor.git
$cd roboadvisor.git
$docker build -t alpaca/roboadvisor .
$docker run -it alpaca/roboadvisor bash
```

If executed properly, you'll see the following in your terminal:

```
$docker run -it alpaca/roboadvisor bash
$root@b2cefad654cf:/home/robo-advisor#
```

You can then run the algorithm you want using the command:

```
$zipline run -f <filename> -b alpaca --start 2018-01-01 --end 2018-06-01
```

If you're interested in running your own algorithm using the data the Alpaca bundle provides (ETFs among others), simply add the file containing your algorithm to the folder, and rebuild the docker image using the `docker build` command. If you use the same name (`alpaca/roboadvisor`), the previous image will be overwritten. 
