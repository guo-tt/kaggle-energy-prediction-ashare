# energy-prediction-ashare

## Data Source

### Kaggle data
* Weather :
- we make sure that every date-time between `2016-01-01 00:00:00` and `2018-12-31 23:00:00` is present in the data, we reindex to make sure it's the case.
- we get external data for weather (darksky, Irish weather) and appended it to the weather provided by Kaggle
- we then fill NAs by interpolation if number of NA in a row less or equal to 4.
- there are still some NA at the end, we can decide to use the external data to fill the NA if needed for linear model.
- Add irradiance and radiance at the end. 

* Building data : 
- fill NA for year_built with average value
- fill NA for floor count by using a linear model using square_feet and primary use
- add log square feet variable

* Train data
- Add holidays
- Add days with day saving time
- Add cosine features 


### Intermediate data

* radiance.csv
'site_id','local_time','utc_time','altitude','azimuth','radiation'
* city_info.csv
'site_id','location','state','lat_long','low_elevation','high_elevation','timezone','utc','country'
* public_holiday.csv
'date','holiday','type'
In 'type' column, ['US','UK','IR'] demonstrate country holiday, ['texas','florida','california','utah','newyork','arizona','utah'] demonstrate state holiday.