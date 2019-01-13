#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 17:06:04 2018

@author: admin
"""
import re

class Utils():
    COMMA_DELIMITER=re.compile(''',!@#$%^&*()''')    


from pyspark import SparkContext,SparkConf

sc=SparkContext("local[3]","world count")
sc.setLogLevel("ERROR")

lines=sc.textFile("/home/admin/Desktop/python-spark-tutorial-master/in/word_count.text")

words=lines.flatMap(lambda line: line.split(" "))

wordCounts=words.countByValue()
for word,count in wordCounts.items():
    print("{} : {}".format(word,count))
    
#####################################################################

conf=SparkConf().setAppName("airports").setMaster("local[2]")

sc=SparkContext(conf=conf)  #The main entry point for Spark functionality
    #SparkContext representes the connection to a spark cluster 
    #and can be used to create RDD's accumulator and broadcast 
    #variables on that cluster

airport=sc.textFile("**************") #load file as string RDD
airportInUSA=airport.filter(lambda line: Utils.COMMA_DELIMITER.split(line)[3]=="\"United States\"")
