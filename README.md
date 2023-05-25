# Cleaning Case
This file consist three cases of data cleaning of each folders:
* Earnings data
* Livestream analytics data
* Product analytics data

 ### Earnings data
Problems found in the raw earnings data:
* General data types
* Time data type unmatch
* Unwanted columns

Expected output of the clean data: 
* Replacing data types 
* Parsing time format
* Renaming columns
* Dropping unused columns.

### Livestream analytics data
Problems found in the raw earnings data:
* Inconsistent data types
* Null data
* Currency problems
* Separated number Problems
* Time data type unmatch

Expected output of clean data:
* No null values
* Using regex to filter and fix the currency data
* Uniform integer and float data
* Convert & parse time data to specific time (hours, minute, second)

### Product analytics data
Problems found in the raw product data:
* Shifted and inconsistency rows
* Currency problems
* Inconsistent data types
* Mixed rows data

Expected output of clean data:
* Consistent rows and cells data
* Matched data types each columns
* Renamed column
* Fix the currency and separated number problems