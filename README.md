# Data sourcing

In the `raw` folder, raw contributions and expenditures data is taken from: http://tracer.sos.colorado.gov/PublicSite/DataDownload.aspx

They are made by joining the 2017 data with the 2018 data.

There were some encoding issues, so we created a "clean" version of the most commonly used file in the `processed` folder.

The results of all the processing - for downstream applications - is put into the `results` folder.

Analyses are in `analysis`, though may not run since I moved files around.
