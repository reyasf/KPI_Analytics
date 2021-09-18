# KPI_Analytics

Pyhton script allows to read .csv file from a URL and parse it. Allows filters on the parsed values.

### Pandas Dataframes

The script uses Pandas Dataframe to store the calculated KPI's. This allows us to filter values faster comparing to an array approach.
The different filter fields used in the script are
* Date (can use from and to date for range of dates, or only from date to filter from that particular date)
* Week (week of the month, "Friday" is considered as start of the week)
```
calendar.setfirstweekday(calendar.FRIDAY)
```
* Platform (KPI's related to App or Web can be filtered)

## Improvement Ideas

* The script is developed using OOP and can be enhanced with more generic approach of calculating KPI's (ex: parser class for different file types, KPI's can be defined as properties of class, and corresponding calculations can be incorporated as methods, filter class to accept any filter fields among the KPI's properties and filter algorithm can be incorporated as methods)
* The filtering mechanism can be developed as an API, where the KPI's can be stored in a Database, File or Cache and can be filtered from the storage
* The validation of filter fields and values can be more generic, when we follow point 1.
* The application can also be developed as Dashboard, using HTML frontend with ajax request to the API as in point 2
