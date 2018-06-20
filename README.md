# roboadvisor

# Introduction
Robo advisors are automated advising services that require little to no user interaction. They specialize in maintaining portfolios based on the investors chosen risk level. The first robo-advisor was launched at the start of the financial crisis in 2008.

The logic for a robo-advisor takes place in 3 stages:
  - Allocation - Given a risk level, portions of capital are allocated to different positions.
  - Distance - Over a regular time interval, the adviser scans to see if there’s a significant change in the portfolio balance
  - Rebalancing - Buys and Sells stock 

# Source Material
At this point, the robo-advisor does not use mean-variance optimization to allocate. The risk-based weight allocation is taken from this [Vanguard Portfolios](https://advisors.vanguard.com/iwe/pdf/FASINVMP.pdf). Each series its individual universe. 

# Contents
The src files in the repo contain a robo advisor in three distinct stages.

 - buy-and-hold.py: Allocates weights based on risk, and orders appropriate number of shares
 - distance.py: Allocates based on risk. Continually checks the distance
 - robo-advisor.py: A fully functioning robo-advisor with all 3 stages as well as all 6 Vanguard universes implemented. 


# Running Locally
If you're interested in running the code locally. There are dependencies to install, and steps to take.
1. Install Zipline. 
2. Ingest the bundle that contains ticker data for backtesting

You can find OS-specific installation instructions for zipline [here](http://www.zipline.io/install.html). I'm going to second their recommendation to run zipline in either a virtual environment. 

This robo-advisor makes use of a custom bundle alpaca, which comes with the repository. To make use of alpaca data, 

# Running with Docker
If you're interested in running backtesting in a docker container, this repository is configured to do so. Running the following commands will create and launch a docker images that has all necessary dependencies installed, as well as the alpaca bundle ingested.
