# Project: Berlin Bike Traffic Dashboard

![Berlin Bike Traffic Dashboard GIF](images/bike_dashboard.gif)

### Live Website
https://berlin-bike-traffic.herokuapp.com/

### Background

The city of Berlin makes some of their bicycle data publicly accessible.  
Data for bicycle counters exists starting from 2012, with most data points starting from 2017. 
This dashboard includes the latest data from 2017 through 2019. 

### Goal

Build a dashboard on bike traffic in Berlin with pandas, folium and dash.

### Data Wrangling

Transformation steps for raw data are implemented in data_wrangling.py.

### Sources

Original data found [here](https://www.berlin.de/sen/uvk/verkehr/verkehrsplanung/radverkehr/weitere-radinfrastruktur/zaehlstellen-und-fahrradbarometer/)  
Image by [unDraw](https://www.undraw.co)

### Influenced by

https://github.com/GesaJo/Capital-Bike-Dashboard  
https://lab.technologiestiftung-berlin.de/projects/bikerides/de/  

### To Do

* Use data from all years
* put helper functions in packages
* Add longer explanatory text in README
* Add notebook with prediction, analyze development during Covid-19, when 2020 data goes public
* Improve loading time (prepare csv file completely beforehand)
* Improve design (dropdowns, highlight station name)
* Add tests
* Add CI with github actions
* Publish dashboard