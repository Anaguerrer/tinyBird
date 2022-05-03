# tinyBird

In order to generate random data for a demo, we must first think about the goal, that is, the use case.

To solve this exercise, I've decided to show some important metrics in the delivery business in order to present good statistics to their clients:

1. Time it takes (on average) for the company to deliver a package since the user makes the order.
2. Number of missing packages per month.
3. Number of returned packages by the consumer.


From here, the event generation code is built:

For this I've chosen Python as the programming language and Pandas (NumPy) as the library to generate and process the data I need.
The reason is that Python is the language par excellence in data engineering (besides R) and I have already used Pandas before to generate test dataframes.

I wasn't sure in the beginning if pandas could generate 10M events quickly and efficiently, but after a local test I saw that there was no problem.

I would choose Bigquery to store the data. I know, from other projects, that bigquery perfectly supports the size we are handling here and that you can also create views, queries and connect with Google Cloud Datastore to make the dashboard in an easy and intuitive way.

Maybe for this client in particular I would not choose BigQuery as the main database, I think Firebase would be more appropriate for all its additional features and functionalities; which can also connect to bigQuery if we wanted to treat some specific data in a relational way and thus do the descriptive analysis that we mentioned in the test.

In this case I have not added the connection to Biguery, but it could be done in 3 ways (I have not investigated which of them is more efficient):
 * Upload Dataframe using pandas.DataFrame.to_gbq() function
 * Saving Dataframe as CSV and then upload it as a file to BigQuery using the Python API
 * Saving Dataframe as CSV and then upload the file to Google Cloud Storage using this procedure and then reading it from BigQuery

I would like to describe a little bit the argument followed for this events generation and explain some of the code:

Taking into account the chosen use case, I define the columns and structure of the final table that I need to get this information:

tracking_order, shipped, waiting, waiting_date, delivered, delivered_date, returned, returned_date, missing, missing_date

Since I want to know both how many packets are lost and how many are returned, by intuition I decide that the distribution of the weights will be:

* 3% of missing packages
* 8% of waiting packages
* 11% of returned packages

Everybody could change the weights in an easy way (defining the parameters in main.py); so if in the demo the client tells us that they are far from reality, it would be enough to modify them and re-execute the process (which, being connected to bigquery and this to Datastudio, would update de dashboard inmidiatly).

Firstable, we generate (sequentially) an identification code for each order (which would be the primary key).
Next, since we need the shipping dates, as well as the change status dates, we generate an array of random dates included in a certain range and assign them to the order codes ----> this will be the shipping dates.

Next, we assing the status to the orders based on the defined weights, so that 1=true and 0=false; for example:

* If delivered=1, the package has been delivered.

Then we need to assign random dates to status changes, and for this we take as reference the shipping date previously assigned to each record and we add a random number of days.

A foot chart has been added at the end to verify the final dataframe.

As for how I would solve the use case once I have the data in Bigquery, as I said, I would connect this datasource with Data Studio and show the mentioned metrics there (surely with pie charts).

Please note that the process could take a few minutes (maybe 3-4) for 15M rows.



