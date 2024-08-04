# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 21:36:13 2021

@author: Firat Mizrak
"""

from selenium import webdriver
from webdriver.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
import re
from datetime import datetime
from datetime import date
import os
import time
from tkinter import Tk, Canvas, Frame, BOTH

delay_time = 1
chromeDriver = webdriver.Chrome(ChromeDriverManager().install())
#driver = webdriver.Chrome()

#Taking current date
current_date = datetime.now()
current_time = current_date.strftime("%H:%M:%S")
print("Current Time:", current_time)
today = date.today()
print("Today's date:", today)

def _dab(path, delay_time):#This function used for click to defined path with specified delay
    chromeDriver.find_element_by_xpath(path).click()
    time.sleep(delay_time)  

def _goMiniPuzzlePage():#Using paths, go desired page
    chromeDriver.get('https://www.nytimes.com/crosswords/game/mini')
    try:
        _dab("/html/body/div[1]/div/div/div[4]/div/main/div[2]/div/div[2]/div[3]/div/article/div[2]/button/div",delay_time)#path cont. without create account
    except:
        _dab("/html/body/div[1]/div/div/div[4]/div/main/div[2]/div/div[2]/div[3]/div/article/button",delay_time)#path ok
    time.sleep(delay_time)
    _dab("/html/body/div[1]/div/div/div[4]/div/main/div[2]/div/div/ul/div[2]/li[2]/button",delay_time)#path reveal
    _dab("/html/body/div[1]/div/div/div[4]/div/main/div[2]/div/div/ul/div[2]/li[2]/ul/li[3]/a",delay_time)#path puzzle
    _dab("/html/body/div[1]/div/div[2]/div[2]/article/div[2]/button[2]/div",delay_time)#path reveal
    _dab("/html/body/div[1]/div/div[2]/div[2]/span",delay_time)#path escape

def _getClues():#Here clues and corresponding numbers taken
    numbers = chromeDriver.find_elements_by_class_name("Clue-label--2IdMY")#numbers taken by using common class name
    clues = chromeDriver.find_elements_by_class_name("Clue-text--3lZl7")#clues taken by using common class name
    across_clues = []
    down_clues = []
    i = 1
    for number, clue in zip(numbers, clues):#zip used to take values iteratively
        no = number.get_property("textContent")#
        content = clue.get_property("textContent")
        if i < 6:
            acr = ["ACROSS",no,content]
            print(acr)
            across_clues.append(acr)
        else:
            dow = ["DOWN",no,content]
            print(dow)
            down_clues.append(dow)
        i+=1
    return across_clues,down_clues

def _getAnswers():#Getting correspoınding answers letter by letter with their numbers
    answers = []
    for i in range(25):
        revealed_box = chromeDriver.find_element_by_id("cell-id-{i}".format(i=i))
        number_of_elements = revealed_box.get_property("parentNode").get_property("childElementCount")
        if number_of_elements == 1:#Black cells have only 1 element 
            answers.append(["",""])#append null when black cell
        elif number_of_elements == 3:
            letter = revealed_box.get_property("parentNode").get_property("childNodes")[1].get_property("textContent")#first node gives letter when with number
            answers.append([letter[0],""])#letters taken as letter[0] since text content has 2 same letter
        elif number_of_elements == 4:
            number = revealed_box.get_property("parentNode").get_property("childNodes")[1].get_property("textContent")#first node gives number when with number
            letter = revealed_box.get_property("parentNode").get_property("childNodes")[2].get_property("textContent")#second node gives letter when with number
            answers.append([letter[0], number])#letters taken as letter[0] since text content has 2 same letter
    return answers

def createGui(across_clues,down_clues,answers):#Constructing Gui
    BOX_SIZE = 100
    LETTERS_PADDING = 50
    root = Tk()
    canvas = Canvas(root, width=1550, height=1200)
    box_num = 0
    for y in range(5):
        for x in range(5):
            if answers[box_num][0] == "":
                canvas.create_rectangle(BOX_SIZE * (x + 1), BOX_SIZE * (y + 1), BOX_SIZE + (BOX_SIZE * (x + 1)), BOX_SIZE + (BOX_SIZE * (y + 1)),fill="black")
            elif answers[box_num][1] != "":
                canvas.create_rectangle(BOX_SIZE * (x + 1), BOX_SIZE * (y + 1), BOX_SIZE + (BOX_SIZE * (x + 1)), BOX_SIZE + (BOX_SIZE * (y + 1)),fill="white")
                canvas.create_text((BOX_SIZE * (x + 1)) +LETTERS_PADDING, (BOX_SIZE * (y + 1)) + LETTERS_PADDING, fill="blue",font="Arial 45 bold",text=answers[box_num][0])
                canvas.create_text((BOX_SIZE * (x + 1)) + 10, (BOX_SIZE * (y + 1)) + 15, fill="black",font="Arial 16 ",text=answers[box_num][1])
            else:
                canvas.create_rectangle(BOX_SIZE * (x + 1), BOX_SIZE * (y + 1), BOX_SIZE + (BOX_SIZE * (x + 1)), BOX_SIZE + (BOX_SIZE * (y + 1)),fill="white")
                canvas.create_text((BOX_SIZE * (x + 1)) + LETTERS_PADDING, (BOX_SIZE * (y + 1)) + LETTERS_PADDING, fill="blue",font="Arial 45 bold", text=answers[box_num][0])
            box_num += 1

    #Creating group nickname and date:
    canvas.create_text( (BOX_SIZE * 5) + 50, (BOX_SIZE * 6) + 20, fill="black", font="Calibri 14 italic", text="FIVEBROS")
    canvas.create_text( (BOX_SIZE * 5) + 50, (BOX_SIZE * 6) + 40, fill="black", font="Arial 10", text="time: " + str(current_time))
    canvas.create_text( (BOX_SIZE * 5) + 50, (BOX_SIZE * 6) + 60, fill="black", font="Arial 10", text="date: " + str(today))

    #Creating clues:
    for i in range(down_clues.__len__()):
        canvas.create_text(1040, 120 + (i*20), fill="black", font="Arial 9", text=down_clues[i][1] + "  " + down_clues[i][2], anchor = "w")#Anchor ="w" used for left side of all text are in line
    for i in range(across_clues.__len__()):
        canvas.create_text(640, 120 + (i*20), fill="black", font="Arial 9", text=across_clues[i][1] + "  " + across_clues[i][2], anchor = "w")

    canvas.create_text( 1040, 80, fill="black", font="Arial 18 bold", text="DOWN",anchor = "w")
    canvas.create_text( 640, 80, fill="black", font="Arial 18 bold", text="ACROSS", anchor = "w")

    canvas.pack(fill=BOTH, expand=1)
    root.mainloop()


_goMiniPuzzlePage()
across_clues,down_clues = _getClues()
answers = _getAnswers()
createGui(across_clues,down_clues,answers)

