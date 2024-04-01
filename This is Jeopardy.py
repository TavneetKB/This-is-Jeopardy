#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 00:12:07 2024

@author: tavneetbahia
"""

import pandas as pd
pd.set_option('display.max_colwidth', -1)

import random

########################################################################################
#Loading data set

jeopardy = pd.read_csv("*My directory*/jeopardy.csv")

########################################################################################
#Checking data set

#print(jeopardy.head(10))

#print(jeopardy.describe(include="all"))

########################################################################################
#Remove leading space in column names
#print(jeopardy.columns.values.tolist())

jeopardy.rename(columns=lambda x: x.strip(), inplace=True)
#print(jeopardy.columns.values.tolist())
#print(jeopardy[["Question","Answer"]])
#print(jeopardy["Show Number"])

########################################################################################
#Function that filters the dataset for questions that contains all of the words in a list of words

def Words_in_Question(df, wordlist):
    
#First attempt however does not check if all of the list is in a single cell, only checks if each element is in a cell

  """word =[]
  for x in df.Question:
    for i in wordlist:
      if i.lower() in x.lower().split(" "):
        word.append(x)
  word
  return df[df["Question"].isin(word)]"""

#Second attempt using all to correct, Attribute error kept showing so used try-except to remove as code is working
  word =[]
  try:
      for y in df.Question:
          if all(i.lower() in y.lower() for i in wordlist):
              word.append(y)
      word
      return df[df["Question"].isin(word)]
  except AttributeError:
      print("")

king_england = Words_in_Question(jeopardy, ["King", "England"])
#print(king_england)


########################################################################################
#Convert Values into floats from strings

#print(jeopardy["Value"])

jeopardy.Value = jeopardy.Value.apply(lambda x: x.strip("$"))

jeopardy.Value = jeopardy.Value.apply(lambda x: x.replace("no value","0"))

jeopardy.Value = jeopardy.Value.apply(lambda x: x.replace(",",""))

#print(jeopardy["Value"])

#print(jeopardy["Value"].dtype)

jeopardy['New Value'] = pd.to_numeric(jeopardy['Value'], errors='coerce')
#print(jeopardy["New Value"].dtype)

#print("The average value each question has is ${}".format(jeopardy["New Value"].mean()))

king = Words_in_Question(jeopardy, ["King"])
#print("The average values of a question containing King is ${}".format(king["New Value"].mean()))

########################################################################################
#Function that counts the unique answers to all the questions in dataset

def count_unique_answer(questionlist):
  dictans = {}
  for i in questionlist["Answer"]:
    dictans[i] = questionlist["Answer"].value_counts()[i]
  return dictans
      

#print(count_unique_answer(king))

########################################################################################
#Create a function which filters the questions by date
#print(jeopardy["Air Date"])
jeopardy["Air Date"] = pd.to_datetime(jeopardy["Air Date"])
#print(jeopardy["Air Date"])

def question_date(df, year, wordlist):
#This filters by year
    datelist =[]
    for x in df["Air Date"]:
        if year == x.year:
          datelist.append(x)
    datelist
    date_df = df[df["Air Date"].isin(datelist)]
#This filters by word
#Old method:
    """word =[]
    for x in date_df.Question:
      for i in wordlist:
        if i.lower() in x.lower().split(" "):
          word.append(x)
    word
    date_df[date_df["Question"].isin(word)]"""
    
#New method
    word =[]
    try:
        for y in date_df.Question:
            if all(i.lower() in y.lower() for i in wordlist):
                word.append(y)
        word
        date_df[date_df["Question"].isin(word)]
    except AttributeError:
        print("")
#This counts how many times word appears in question
    return "The amount of time {} appears is {} in the year {}.".format(wordlist,len(date_df),year)

#print(question_date(jeopardy, 2004,"Computer"))
#print(question_date(jeopardy, 1990,"Computer"))

########################################################################################
#Check if there is a connection between round and categories
#This method is taking too long to load: Due to the amount of for loops, also gave the wrong answer due to using value_counts

"""def round_category(df):
#Lists Rounds
  rounds = []
  for i in df["Round"]:
    if i not in rounds:
      rounds.append(i)
    else:
      rounds
  rounds

#Creates a new df for each type of round
  roundlist1 =[]
  roundlist2 =[]
  roundlist3 =[]
  roundlist4 = []

  for x in df["Round"]:
      if rounds[0] == x:
        roundlist1.append(x)
  roundlist1
  round_df1 = df[df["Round"].isin(roundlist1)]

  for x in df["Round"]:
      if rounds[1] == x:
        roundlist2.append(x)
  roundlist2
  round_df2 = df[df["Round"].isin(roundlist2)]

  for x in df["Round"]:
      if rounds[2] == x:
        roundlist3.append(x)
  roundlist3
  round_df3 = df[df["Round"].isin(roundlist3)]
  
  for x in df["Round"]:
      if rounds[3] == x:
        roundlist4.append(x)
  roundlist4
  round_df4 = df[df["Round"].isin(roundlist4)]
  
  #return round_df1, round_df2, round_df3, round_df4

#Finds the category that shows up the most in each round type

  dictround1 = {}
  for i in round_df1["Category"]:
    dictround1[i] = round_df1["Category"].value_counts()[i]
  dictround1

  dictround2 = {}
  for i in round_df2["Category"]:
    dictround2[i] = round_df2["Category"].value_counts()[i]
  dictround2

  dictround3 = {}
  for i in round_df3["Category"]:
    dictround3[i] = round_df3["Category"].value_counts()[i]
  dictround3
  
  dictround4 = {}
  for i in round_df4["Category"]:
    dictround4[i] = round_df4["Category"].value_counts()[i]
  dictround4
  

  return "For {} the most likely category to appear is {}.".format(rounds[0],max(dictround1)), "For {} the most likely category to appear is {}.".format(rounds[1],max(dictround2)), "For {} the most likely category to appear is {}.".format(rounds[2],max(dictround3),"For {} the most likely category to appear is {}.".format(rounds[3],max(dictround4))

print(round_category(jeopardy))"""

#Second method
def round_category(df):
    
    mode_elements = df.groupby('Round')['Category'].apply(lambda x: x.mode())
    return "Most frequent elements in Category for each element in Round: \n{}".format(mode_elements)

print(round_category(jeopardy))

########################################################################################
#Build quizzing system

def quiz(df):
#Generates random number to obtain question
  questionnum = random.randint(0,len(df["Question"]))
  question = " "
#Assign a number to each question

  df["Number"] = range(len(df))

#Obtain question
  #questionnumber = df.loc[(df['Number'] == questionnum)]['Question']
  question = df.iloc[questionnum]["Question"]
  #print(df[["Number", "Question"]].head())

#For the corresponding answer
  #answernumber = df.loc[(df['Number'] == questionnum), 'Answer']
  answer = df.iloc[questionnum]["Answer"]
# Take in the answer
  ans = input("The question is: {}. What is your answer?".format(question))
    
  for x in answer:
      for i in ans:
          if i.lower() in x.lower().split(" "):
              return "That is correct! The correct answer is: {}".format(answer)
          else:
              return "That is incorrect... The correct answer is: {}".format(answer)
     

#print(quiz(jeopardy))


