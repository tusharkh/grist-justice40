# Grist Justice40 Analysis

In this repo, I attempt to recreate the analysis from the Grist article [*The White House excluded race from its environmental justice tool. We put it back in.*](https://grist.org/equity/climate-and-economic-justice-screening-tool-race/) by 
[Naveena Sadasivam](https://grist.org/author/naveena-sadasivam/) & [Clayton Aldern](https://grist.org/author/clayton-aldern/). Just getting some practice playing with census data and putting together nice visualizations.

There seem to be some minor discrepancies with the Grist analysis. One potential source of error is that is seems as though the ACS 2019 data and the CEJST data on population don't match, but I thought they should (because [CEJST says it uses ACS 2015-2019](https://screeningtool.geoplatform.gov/en/methodology#3/33.47/-97.5)). Another potential source of error is the way Grist bins the data. I wasn't sure how exactly its binned. Overall, the differences seem relatively minor though. The figure I produced matches theirs quite closely. Here's my figure below, which you can compare to the original one [here](https://grist.org/wp-content/uploads/2022/02/cejst-acs-percent-race-data.png?w=1200).

![chart](https://github.com/tusharkh/grist-justice40/blob/main/figures/demographic-distribution.jpg)
