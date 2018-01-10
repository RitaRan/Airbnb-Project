# Airbnb-Project
This is a repository for a group project for COMPSCI 316 'Introduction to Database' at Duke. The goal of this project is to
build a database-driven website from the ground up. Our group chose to build a website having similar features as Airbnb but we also added additional features that Airbnb does not provide. The features we added are:

- Adding a section for house hosts to give them price recommendation
- Adding two new filter options, based on nearby crime rate and based on nearby entertainment, for house renters. These two filter options are accomplished by combining Airbnb data with local crime rate data and Yelp data

# Team Members:
- Ran Zhou

- Zhaoxi Zhang

- Yanlin Yu

- Jialei Guo

- Jiahui Wang 

- Yiyi Ye


# URL we used to download the raw data
(1) Airbnb hosts' data in Toronto (http://insideairbnb.com/get-the-data.html)

(2) Crime rate data in Toronto (http://data.torontopolice.on.ca/datasets/mci-2016/data?geometry=-80.368%2C43.378%2C-76.412%2C44.073)

(3) Yelp data in Toronto (https://www.yelp.com/dataset/documentation/sql)

We did some data preprocessing to create new features and new data tables to be easily loaded into our database. The new tables are in csv format in Data folder.

# How to run the website
1. To load the database into your machine, you should also download the house_new.csv, crime rate.csv, airdb.sql under ‘Data’ folder in source_code.zip. ‘cd’ to the directory where you save all these three files.

2. Change the paths to the .csv files in the airdb.sql file to the actual path in your computer where you save the house_new.csv and crimerate.csv to help load the data into your database.

   Create the database by running:
   
   dropdb airdb; createdb airdb; psql airdb -af airdb.sql
   
4. We implement the sql using postgresSQL

5. After loading the database into your machine, to open the webpage, ‘cd’ to the folder ‘flask-airdb_final_web’ and make sure the python script ‘app.py’ is in the folder. Run the following in the terminal to open the website:

   python app.py
   
Open a browser and type “http://0.0.0.0:5010/” in the address bar. Play with the website and have fun!
