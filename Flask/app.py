# import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, cast, Integer
from flask import Flask, render_template, redirect, jsonify, request
import pandas as pd
import os

# pyspark imports 
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel

# Set Environment Variables
import os
os.environ["JAVA_HOME"] = "C:\Program Files\Java\jdk1.8.0_271"
os.environ["HADOOP_HOME"] = "C:\Installations\Hadoop"
os.environ["SPARK_HOME"] = "D:\spark-2.4.5-bin-hadoop2.7\spark-2.4.5-bin-hadoop2.7"

# Start a Spark session
spark =  SparkSession.builder \
    .master("local[*]") \
    .getOrCreate()  

app = Flask(__name__)

# database setup
# Configure settings for RDS
# rds_connection_string = "postgres:postgres@mypostgresaws2020.c002u923zftw.us-east-2.rds.amazonaws.com:5432/FinalProjectGroup3"
# engine = create_engine(f'postgresql://{rds_connection_string}')

# # reflect an existing database into a new model
# Base = automap_base()
# # reflect the tables
# Base.prepare(engine, reflect=True)
# # print(Base.classes.keys())
# # Save reference to the table
# Testfinal = Base.classes.testfinal
# Trainfinal = Base.classes.trainfinal

# Create route for index.html
@app.route("/", methods=["GET", "POST"])
def index():
    output= None
    results= None
    if request.method == "POST":
        input_data = request.values.get("input")
        loaded_model = PipelineModel.load("models/lr_regression_eval")
        testreview = spark.createDataFrame([(f"{str(input_data)}", 0)], ["review", "rating"])
        transformed_model = loaded_model.transform(testreview)
        output = str(int(transformed_model.select("prediction").collect()[0]["prediction"]))
        if (output == "0"):
            results = "This is a positive review"
        else:
            results = "This is a negative review"

    # Return template and data
    return render_template("index.html", output= results)

@app.route("/data")
def datapage():

    return render_template("data.html")

@app.route("/chart")
def chartpage():

    return render_template("chart.html")

@app.route("/profile")
def profilepage():

    return render_template("profile.html")

if __name__ == "__main__":
    app.run(debug=True)

# @app.route("/testfinal")
# def testfinal():

#     session = Session(engine)
#     results = []
#     result = session.execute(Testfinal.__table__.select())
#     for row in result:
#         results.append(dict(row))
#     session.close()

#     return jsonify(results)


# @app.route("/trainfinal")
# def trainfinal():

#     session = Session(engine)
#     results = []
#     result = session.execute(Trainfinal.__table__.select())
#     for row in result:
#         results.append(dict(row))
#     session.close()

#     return jsonify(results)
