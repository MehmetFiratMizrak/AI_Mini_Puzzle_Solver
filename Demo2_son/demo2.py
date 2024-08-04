# -*- coding: utf-8 -*-
"""
@authors:
*************FIVEBROS******************
Mehmet Fırat Mızrak
Alperen Balcı

*************FIVEBROS******************
"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
import re
from datetime import datetime
from datetime import date
import os
import time
import nltk
from tkinter import Tk, Canvas, Frame, BOTH
import numpy as np
import random
from numba import jit, cuda
import numpy as np
from timeit import default_timer as timer  
#from gensim.parsing.preprocessing import remove_stopwords
import copy

delay_time = 1

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

chromeDriver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=options)

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
        if number_of_elements== 1:#Black cells have only 1 element 
            answers.append(["",""])#append null when black cell
        elif number_of_elements== 3:
            letter = revealed_box.get_property("parentNode").get_property("childNodes")[1].get_property("textContent")#first node gives letter when without number
            answers.append([letter[0],""])#letters taken as letter[0] since text content has 2 same letter
        else:
            number = revealed_box.get_property("parentNode").get_property("childNodes")[1].get_property("textContent")#first node gives number when with number
            letter = revealed_box.get_property("parentNode").get_property("childNodes")[2].get_property("textContent")#second node gives letter when with number
            answers.append([letter[0], number])#letters taken as letter[0] since text content has 2 same letter
    return answers

def _createGui(across_clues,down_clues,answers):#Constructing Gui
    BOX_SIZE = 100
    LETTERS_PADDING = 50
    root = Tk()
    canvas = Canvas(root, width=1890, height=1200)
    box_num = 0
    crosword_puzzle_size = 5 #5*5 puzzle
    for y in range(crosword_puzzle_size):
        for x in range(crosword_puzzle_size):
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
    box_num = 0
    slide_num = 1100
    answers[10][0] = 'C'
    answers[14][0] = 'I'
    for y in range(crosword_puzzle_size):
        for x in range(crosword_puzzle_size):
            if answers[box_num][0] == "":
                canvas.create_rectangle(slide_num+BOX_SIZE * (x + 1), BOX_SIZE * (y + 1), slide_num+BOX_SIZE + (BOX_SIZE * (x + 1)), BOX_SIZE + (BOX_SIZE * (y + 1)),fill="black")
            elif answers[box_num][1] != "":
                canvas.create_rectangle(slide_num+BOX_SIZE * (x + 1), BOX_SIZE * (y + 1), slide_num+BOX_SIZE + (BOX_SIZE * (x + 1)), BOX_SIZE + (BOX_SIZE * (y + 1)),fill="white")
                canvas.create_text((slide_num+BOX_SIZE * (x + 1)) +LETTERS_PADDING, (BOX_SIZE * (y + 1)) + LETTERS_PADDING, fill="blue",font="Arial 45 bold",text=answers[box_num][0])
                canvas.create_text((slide_num+BOX_SIZE * (x + 1)) + 10, (BOX_SIZE * (y + 1)) + 15, fill="black",font="Arial 16 ",text=answers[box_num][1])
            else:
                canvas.create_rectangle(slide_num+BOX_SIZE * (x + 1), BOX_SIZE * (y + 1), slide_num+BOX_SIZE + (BOX_SIZE * (x + 1)), BOX_SIZE + (BOX_SIZE * (y + 1)),fill="white")
                canvas.create_text((slide_num+BOX_SIZE * (x + 1)) + LETTERS_PADDING, (BOX_SIZE * (y + 1)) + LETTERS_PADDING, fill="blue",font="Arial 45 bold", text=answers[box_num][0])
            box_num += 1


    #Creating group nickname and date:
    canvas.create_text( (BOX_SIZE * 5) + 50, (BOX_SIZE * 6) + 20, fill="black", font="Calibri 14 italic", text="FIVEBROS")
    canvas.create_text( (BOX_SIZE * 5) + 50, (BOX_SIZE * 6) + 40, fill="black", font="Arial 10", text="clock: " + str(current_time))
    canvas.create_text( (BOX_SIZE * 5) + 50, (BOX_SIZE * 6) + 60, fill="black", font="Arial 10", text="date: " + str(today))

    #Creating clues:
    for i in range(down_clues.__len__()):
        canvas.create_text(640, 300 + (i*25), fill="black", font="Arial 10", text=down_clues[i][1] + "  " + down_clues[i][2], anchor = "w")#Anchor ="w" used for left side of all text are in line
    for i in range(across_clues.__len__()):
        canvas.create_text(640, 120 + (i*25), fill="black", font="Arial 10", text=across_clues[i][1] + "  " + across_clues[i][2], anchor = "w")

    canvas.create_text( 830, 260, fill="black", font="Arial 18 bold", text="DOWN",anchor = "w")
    canvas.create_text( 830, 80, fill="black", font="Arial 18 bold", text="ACROSS", anchor = "w")

    canvas.create_text( 230, 80, fill="black", font="Arial 16 bold", text="REAL SOLUTIONS", anchor = "w")
    canvas.create_text( 1300, 80, fill="black", font="Arial 16 bold", text="SOLVED BY OUR TEAM", anchor = "w")

    canvas.pack(fill=BOTH, expand=1)
    root.mainloop()

#*******************************************************************************************************************************

def _getAnswerLength(answers):#Getting Answers Length
    acrossAnswersLenght = list()
    downAnswersLenght = list() 
    for index, answer in enumerate(answers):
        if answer[1] != "":
            acr_temp = 1
            dow_temp = 1
            for i in range(5-(index)%5):   
                if index + i < 25:  
                    if answers[index+i][0] == "" :
                        acrossAnswersLenght.append([answer[1], acr_temp-1])
                        break
                    elif (index+i + 1) % 5 == 0 :
                        acrossAnswersLenght.append([answer[1], acr_temp])
                        break
                    else:
                        acr_temp = acr_temp + 1 
                else:
                    break   
            for i in range(5-index//5):
                if index+5*i < 25:  
                    if  answers[index+5*i][0] == "": 
                        downAnswersLenght.append([answer[1],dow_temp-1])
                        break
                    elif index+5*i > 19: 
                        downAnswersLenght.append([answer[1],dow_temp])
                        break
                    else:
                        dow_temp = dow_temp + 1  
                else:
                    break   
    
    return acrossAnswersLenght, downAnswersLenght

def _FilterNumberOfLetter(possible_answers,desired_length):#Getting Answers Length
    filtered_possible_answers = list()
    for single_answer in possible_answers:
        if len(single_answer) == desired_length:
            if single_answer not in filtered_possible_answers:
                filtered_possible_answers.append(single_answer)
    return filtered_possible_answers

def _cutClue(clue):#for deleting unnecessary chars in clue
    new_string = clue.replace("'", "")
    new_string = clue.replace('"', "")
    return new_string

def _cutUnnecessaryChars(possible_answers):#for deleting unnecessary chars in possible_answers
    cutted_list = list()
    for single_ans in possible_answers:
        s1="".join(c for c in single_ans if c.isalnum())
        s2=re.sub("[0-9]","",s1)
        cutted_list.append(s2)
    return cutted_list

def getPossibleAnswers(across_clues,down_clues,acrossAnswersLenght,downAnswersLenght):#Getting Answers Length

    possible_all_across_answers = list()
    possible_all_down_answers = list()
    ttt = 1
    for clue in across_clues:
        clue_to_give = clue[2]
        clue_to_give = _cutClue(clue_to_give)#for deleting unnecessary chars
        print("across clue: ",clue_to_give)
        possible_a_answers1 = _getFromWikipediaPage(clue_to_give) #viki source
        possible_a_answers4 = _getFromEncyclopediaPage(clue_to_give)   #enc source
        possible_a_answers2 = _getFromMeriamWesterPage(clue_to_give)  #m-w source
        possible_a_answers3 = _getFromWordNetPage(clue_to_give)  #wordnet source
        merged_all_source = possible_a_answers1 + list(set(possible_a_answers2)-set(possible_a_answers1))+list(set(possible_a_answers3)-set(possible_a_answers2)-set(possible_a_answers1))
        merged_all_source = merged_all_source + list(set(possible_a_answers4)-set(merged_all_source))
        merged_all_source = _cutUnnecessaryChars(merged_all_source)#for deleting unnecessary chars
        filtered_list = _FilterNumberOfLetter(merged_all_source,acrossAnswersLenght[(int(clue[1])-1)][1])
        print("filtered_list")
        filtered_list = [x.upper() for x in filtered_list]#make all strings to uppercase
        filtered_list = [i for j, i in enumerate(filtered_list) if i not in filtered_list[:j]]
        possible_all_across_answers.append(filtered_list)
        print(filtered_list)
        print("number of words: ", len(filtered_list))
        ttt = ttt + 1

    ttt = 1
    for clue in down_clues:
        clue_to_give = clue[2]
        clue_to_give = _cutClue(clue_to_give)#for deleting unnecessary chars
        print("down clue: ", clue_to_give)
        possible_d_answers1 = _getFromWikipediaPage(clue_to_give)   #viki source
        possible_d_answers4 = _getFromEncyclopediaPage(clue_to_give)   #enc source
        possible_d_answers2 = _getFromMeriamWesterPage(clue_to_give)  #m-w source
        possible_d_answers3 =  _getFromWordNetPage(clue_to_give) #wordnet source
        merged_all_source = possible_d_answers1 + list(set(possible_d_answers2)-set(possible_d_answers1))+list(set(possible_d_answers3)-set(possible_d_answers2)-set(possible_d_answers1))
        merged_all_source = merged_all_source + list(set(possible_d_answers4)-set(merged_all_source))
        merged_all_source = _cutUnnecessaryChars(merged_all_source)#for deleting unnecessary chars
        filtered_list = _FilterNumberOfLetter(merged_all_source,downAnswersLenght[(int(clue[1]))-1][1])
        print("filtered_list :")
        filtered_list = [x.upper() for x in filtered_list]#make all strings to uppercase
        filtered_list = [i for j, i in enumerate(filtered_list) if i not in filtered_list[:j]]
        possible_all_down_answers.append(filtered_list)
        print(filtered_list)
        print("number of words: ",len(filtered_list))
        ttt = ttt + 1
    return possible_all_across_answers,possible_all_down_answers

def Convert(string):
    li = list(string.split(" "))
    return li

def _getFromWikipediaPage(aList):

    chromeDriver.get('https://en.wikipedia.org/wiki/Main_Page')
    search_box = chromeDriver.find_element_by_name("search")
    search_box.send_keys(aList)
    search_box.submit()
    try:
        #_dab("/html/body/div[3]/div[3]/div[4]/div[4]/p[2]/a[5]", delay_time)  # 250 results per page
        element = chromeDriver.find_element_by_xpath("/html/body/div[3]/div[3]/div[4]/div[4]/ul")
        List = Convert(element.text)
    except:
        element = chromeDriver.find_element_by_xpath("/html/body/div[3]/div[3]")
        List = Convert(element.text)
    newList = list()
    List = _cutUnnecessaryChars(List)
    x = len(List)
    for singleList in List:
        if len(singleList) > 2 and len(singleList) < 8:
            newList.append(singleList)
    time.sleep(0.05) 
    return newList

def _getFromWordNetPage(aList):
    filtered_sentence = remove_stopwords(aList)
    print(filtered_sentence)
    newListeSplitted = filtered_sentence.split()  # Listeyi fonksiyona yollayınca kelimeleri tek tek ayırıp yeni liste haline gelmiş durumu.

    if len(newListeSplitted) < 3:
        newList = list()
        for single in newListeSplitted:
            chromeDriver.get('http://wordnetweb.princeton.edu/perl/webwn')
            search_box = chromeDriver.find_element_by_name("s")
            search_box.send_keys(single)
            search_box.submit()
            try:
                element = chromeDriver.find_element_by_xpath("/html/body/div[2]")
                List = Convert(element.text)
            except:
                print("error")
            try:
                List = _cutUnnecessaryChars(List)
                for singleList in List:
                    if len(singleList) > 2 and len(singleList) < 8:
                        newList.append(singleList)
            except:
                newList = []
    else:
        newList = []
    time.sleep(0.05) 
    return newList

def _getFromEncyclopediaPage(aList):

    chromeDriver.get('https://www.encyclopedia.com/')
    search_box = chromeDriver.find_element_by_xpath("/ html / body / div[2] / div / div / div[1] / div[2] / div[3] / form / div[1] / input")
    search_box.send_keys(aList)
    search_box.submit()

    try:
        element = chromeDriver.find_element_by_xpath("/html/body/div[2]/div/main/div/div[3]/div[1]/div[2]/article/div/div/div/div/div/div/div[5]/div[2]/div/div/div[1]")
        List = Convert(element.text)
    except:
        print("error")

    newList = list()
    List = _cutUnnecessaryChars(List)
    for singleList in List:
        if len(singleList) > 2 and len(singleList) < 8:
            newList.append(singleList)
    time.sleep(0.05) 
    return newList

def _getFromMeriamWesterPage(aList):
    filtered_sentence = remove_stopwords(aList)
    newListeSplitted = filtered_sentence.split()  # Listeyi fonksiyona yollayınca kelimeleri tek tek ayırıp yeni liste haline gelmiş durumu.

    if len(newListeSplitted) < 3:
        newList = list()
        for single in newListeSplitted:
            chromeDriver.get('https://www.merriam-webster.com/')
            search_box = chromeDriver.find_element_by_name("s")
            search_box.send_keys(single)
            search_box.submit()
            try:
                element = chromeDriver.find_element_by_xpath("/html/body/div[1]/div/div[5]/div[1]/div[1]")
                List = Convert(element.text)
            except:
                print("error")
                List = []
            List = _cutUnnecessaryChars(List)
            for singleList in List:
                if len(singleList) > 2 and len(singleList) < 8:
                    newList.append(singleList)
    else:
        newList = []
    time.sleep(0.05)
    from_terurus = _getFromMeriamWesterTauserusPage(newListeSplitted)
    newList = newList + from_terurus
    return newList
def _getFromMeriamWesterTauserusPage(newListeSplitted):
    if len(newListeSplitted) < 2:
        newList = list()
        for single in newListeSplitted:
            chromeDriver.get('https://www.merriam-webster.com/')
            _dab("/html/body/div[1]/div/div[3]/div/form/div[2]/div[2]", delay_time)
            search_box = chromeDriver.find_element_by_name("s")
            search_box.send_keys(single)
            search_box.submit()
            try:
                element = chromeDriver.find_element_by_xpath("/html/body/div[1]/div/div[5]/div[1]/div[1]")
                List = Convert(element.text)
            except:
                print("error")
                List = []
            List = _cutUnnecessaryChars(List)
            for singleList in List:
                if len(singleList) > 2 and len(singleList) < 8:
                    newList.append(singleList)
    else:
        newList = []
    time.sleep(0.05) 
    return newList


class WebDriver:
    def __init__(self):
        self.chromeDriver = webdriver.Chrome(ChromeDriverManager().install())

    def dab(self, path, delayTime):#This function used for click to defined path with specified delay
        self.chromeDriver.find_element_by_xpath(path).click()
        time.sleep(delayTime)  

    def goToMiniPuzzlePage(self, website):#Using paths, go desired page
        self.chromeDriver.get(website)
        localPuzzle = (website.split('.')[-1] == "html")
        if not localPuzzle:
            delayTime = 1
            try:
                self.dab("/html/body/div[1]/div/div/div[4]/div/main/div[2]/div/div[2]/div[3]/div/article/div[2]/button/div",delayTime)#path cont. without create account
            except:
                self.dab("/html/body/div[1]/div/div/div[4]/div/main/div[2]/div/div[2]/div[3]/div/article/button",delayTime)#path ok
            time.sleep(delayTime)
            self.dab("/html/body/div[1]/div/div/div[4]/div/main/div[2]/div/div/ul/div[2]/li[2]/button",delayTime)#path reveal
            self.dab("/html/body/div[1]/div/div/div[4]/div/main/div[2]/div/div/ul/div[2]/li[2]/ul/li[3]/a",delayTime)#path puzzle
            self.dab("/html/body/div[1]/div/div[2]/div[2]/article/div[2]/button[2]/div",delayTime)#path reveal
            self.dab("/html/body/div[1]/div/div[2]/div[2]/span",delayTime)#path escape

    def getDriver(self):
        return self.chromeDriver

class Square:
    def __init__(self, squareNum, content): # 'squareNum = 0' indicates white square without number, 'squareNum = -1' indicates black square
        self.squareNum = squareNum
        self.setContent(content)

    def setContent(self, content):
        self.content = content

class Puzzle:
    def __init__(self, chromeDriver):
        self.chromeDriver = chromeDriver
        self.setPuzzleFormat()

    def setPuzzleFormat(self):
        self.squares = []
        for i in range(25):
            revealedSquare = self.chromeDriver.find_element_by_id("cell-id-{i}".format(i=i))
            numOfElements = revealedSquare.get_property("parentNode").get_property("childElementCount")
            if numOfElements == 1:
                self.squares.append(Square(-1,''))
            elif numOfElements == 3:
                self.squares.append(Square(0,' '))
            elif numOfElements == 4:
                number = int(revealedSquare.get_property("parentNode").get_property("childNodes")[1].get_property("textContent"))
                self.squares.append(Square(number,' '))
        self.remainingCoordinates = self.findCoordinatesOfInitials()
        self.numOfItems = 0
                      
    def findCoordinatesOfInitials(self):
        numbers = self.chromeDriver.find_elements_by_class_name("Clue-label--2IdMY") # numbers taken by using common class name
        clues = self.chromeDriver.find_elements_by_class_name("Clue-text--3lZl7")#clues taken by using common class name
        squareNums = []
        lengthsOfClues = []
        for number, clue in zip(numbers, clues):
            squareNums.append(int(number.get_property("textContent")))
            lengthsOfClues.append(len(clue.get_property("textContent").split()))
        coordinatesOfInitials = []
        clueIndex = 0
        for squareNum, lengthOfClue in zip(squareNums, lengthsOfClues):
            for coordinate in range(len(self.squares)):
                square = self.squares[coordinate]
                if square.squareNum > 0 and square.squareNum == squareNum:
                    if clueIndex >= 0 and clueIndex <= 4:
                        coordinatesOfInitials.append(["across", (clueIndex % 5) + 1, coordinate, lengthOfClue])
                    elif clueIndex >= 5 and clueIndex <= 9:
                        coordinatesOfInitials.append(["down", (clueIndex % 5) + 1, coordinate, lengthOfClue])
                    clueIndex += 1
                    break
        return self.sortCoordinatesOfInitials(coordinatesOfInitials)
    
    def sortCoordinatesOfInitials(self, coordinatesOfInitials):
        tempLists = coordinatesOfInitials
        coordinatesOfInitials = []
        minClueLength = 0
        indexOfMinClueLength = 0
        while len(tempLists) > 0:
            for i in range(len(tempLists)):
                tempList = tempLists[i]
                if i == 0:
                    minClueLength = tempList[3]
                    indexOfMinClueLength = i
                elif tempList[3] < minClueLength:
                    minClueLength = tempList[3]
                    indexOfMinClueLength = i
            coordinateInfo = tempLists.pop(indexOfMinClueLength)
            coordinatesOfInitials.append(coordinateInfo)
        return coordinatesOfInitials
    
    def isItemCompatible(self, item, itemIndex, coordinatesOfInitials):
        previousItem = self.getItem(itemIndex, coordinatesOfInitials)
        if len(item) == len(previousItem) and item != previousItem:
            for i in range(len(item)):
                if previousItem[i] != ' ' and previousItem[i] != item[i]:
                    return False
            return True
        return False
    @jit
    def setItem(self, item, itemIndex, coordinatesOfInitials):
        currentItem = item.upper()
        if self.isItemCompatible(currentItem, itemIndex, coordinatesOfInitials):
            squareIndex = coordinatesOfInitials[itemIndex][2]
            for contentIndex in range(len(currentItem)):
                self.getSquare(squareIndex).setContent(currentItem[contentIndex])
                if coordinatesOfInitials[itemIndex][0] == "across":
                    squareIndex += 1
                elif coordinatesOfInitials[itemIndex][0] == "down":
                    squareIndex += 5
            self.findRemainingCoordinates(coordinatesOfInitials)
            return True
        return False
    @jit
    def getItem(self, itemIndex, coordinatesOfInitials):
        squareIndex = coordinatesOfInitials[itemIndex][2]
        item = []
        if coordinatesOfInitials[itemIndex][0] == "across":
            acrossBoundary = 1
            while squareIndex < len(self.squares) and self.getSquare(squareIndex).squareNum >= 0 and acrossBoundary > 0:
                item.append(self.getSquare(squareIndex).content)
                squareIndex += 1
                acrossBoundary = squareIndex % 5
        elif coordinatesOfInitials[itemIndex][0] == "down":
            while squareIndex < len(self.squares) and self.getSquare(squareIndex).squareNum >= 0:
                item.append(self.getSquare(squareIndex).content)
                squareIndex += 5
        return item

    def findRemainingCoordinates(self, coordinatesOfInitials):
        self.remainingCoordinates = []
        for itemIndex in range(len(coordinatesOfInitials)):
            currentItem = self.getItem(itemIndex, coordinatesOfInitials)
            for content in currentItem:
                if content == ' ':
                    self.remainingCoordinates.append(coordinatesOfInitials[itemIndex])
                    break
        self.numOfItems = 10 - len(self.remainingCoordinates)

    def printPuzzle(self):
        p = copy.deepcopy(self.squares)
        for i in range(len(p)):
            p[i] = [p[i].squareNum, p[i].content]
        print('+------------+------------+------------+------------+------------+')
        print('|  %s  |  %s  |  %s  |  %s  |  %s  |' % (p[0], p[1], p[2], p[3], p[4]))
        print('+------------+------------+------------+------------+------------+')
        print('|  %s  |  %s  |  %s  |  %s  |  %s  |' % (p[5], p[6], p[7], p[8], p[9]))
        print('+------------+------------+------------+------------+------------+')
        print('|  %s  |  %s  |  %s  |  %s  |  %s  |' % (p[10], p[11], p[12], p[13], p[14]))
        print('+------------+------------+------------+------------+------------+')
        print('|  %s  |  %s  |  %s  |  %s  |  %s  |' % (p[15], p[16], p[17], p[18], p[19]))
        print('+------------+------------+------------+------------+------------+')
        print('|  %s  |  %s  |  %s  |  %s  |  %s  |' % (p[20], p[21], p[22], p[23], p[24]))
        print('+------------+------------+------------+------------+------------+')

    def getSquare(self, squareIndex):
        return self.squares[squareIndex]
    
    def getRemainingCoordinates(self):
        return self.remainingCoordinates
    
    def getNumOfItems(self):
        return self.numOfItems

class PuzzleSolver:
    def __init__(self, chromeDriver, listsOfItems):
        self.chromeDriver = chromeDriver
        self.getAnswerKey()
        self.listsOfItems = listsOfItems
        self.solutionPath = None

    def getAnswerKey(self):
        self.answerKeyPuzzle = Puzzle(self.chromeDriver)
        self.coordinatesOfInitials = copy.deepcopy(self.answerKeyPuzzle.getRemainingCoordinates())
        for i in range(len(self.answerKeyPuzzle.squares)):
            revealedSquare = self.chromeDriver.find_element_by_id("cell-id-{i}".format(i=i))
            numOfElements = revealedSquare.get_property("parentNode").get_property("childElementCount")
            square = self.answerKeyPuzzle.getSquare(i)
            content = ''
            if square.squareNum == 0:
                content = revealedSquare.get_property("parentNode").get_property("childNodes")[1].get_property("textContent")[0]
            elif square.squareNum > 0:
                content = revealedSquare.get_property("parentNode").get_property("childNodes")[2].get_property("textContent")[0]
            square.setContent(content)
        self.answerKeyPuzzle.findRemainingCoordinates(self.coordinatesOfInitials)
    
    def getCopyPuzzle(self, puzzle):
        copyPuzzle = Puzzle(puzzle.chromeDriver)
        copyPuzzle.squares = copy.deepcopy(puzzle.squares)
        copyPuzzle.remainingCoordinates = copy.deepcopy(puzzle.remainingCoordinates)
        copyPuzzle.numOfItems = puzzle.numOfItems
        return copyPuzzle
    
    def getCopyPath(self, path):
        copyPath = []
        for puzzleState in path:
            copyPath.append(self.getCopyPuzzle(puzzleState))
        return copyPath
    @jit
    def getChildStates(self, puzzle):
        childStates = []
        remainingCoordinates = puzzle.getRemainingCoordinates()
        for itemIndex in range(len(remainingCoordinates)):
            currentCoordinate = remainingCoordinates[itemIndex]
            if currentCoordinate[0] == "across":
                listIndex = currentCoordinate[1] - 1
            elif currentCoordinate[0] == "down":
                listIndex = currentCoordinate[1] + 4
            listOfItems = self.listsOfItems[listIndex]
            print(listOfItems)
            #k=1
            for item in listOfItems:
                temp = self.getCopyPuzzle(puzzle)
                itemFits = temp.setItem(item, itemIndex, copy.deepcopy(remainingCoordinates))
                isCompatible = self.isStateCompatible(temp)
                print([item, currentCoordinate[0] + str(currentCoordinate[1]), itemFits, isCompatible])
                if itemFits and isCompatible:
                    childStates.insert(0, temp)
                    #print(k)
                    #print("info")
                    #print(temp.getRemainingCoordinates())
                    #print(temp.getNumOfItems())
                    #k+=1
                    # temp.printPuzzle()
                    temp.printPuzzle()        
        return childStates
    @jit
    def isStateCompatible(self, puzzle):
        listIndex = 0
        for itemIndex in range(len(self.coordinatesOfInitials)):
            currentItem = puzzle.getItem(itemIndex, self.coordinatesOfInitials)
            #currentItem = currentItem.translate({ord(c): None for c in currentItem.whitespace})
            currentCoordinate = self.coordinatesOfInitials[itemIndex]
            if currentCoordinate[0] == "across":
                listIndex = currentCoordinate[1] - 1
            elif currentCoordinate[0] == "down":
                listIndex = currentCoordinate[1] + 4
            listOfItems = self.listsOfItems[listIndex]
            if not self.doesItemExist(currentItem, listOfItems):
                return False
        return True
    @jit
    def doesItemExist(self, currentItem, listOfItems):
        doesExist = False
        for itemInList in listOfItems:
            doesExist = False
            for i in range(len(currentItem)):
                if currentItem[i] != ' ' and itemInList[i] != currentItem[i]:
                    break
                elif i == len(currentItem) - 1:
                    doesExist = True
                    break
            #print("doesItemExist")
            #print([currentItem, itemInList, doesExist])
            if doesExist:
                break
        return doesExist
    @jit
    def depthFirstSearch(self):
        initialState = Puzzle(self.chromeDriver)
        queue = []
        queue.append([initialState])
        self.solutionPath = None
        nearMisses = []
        while True:
            if len(queue) == 0:
                print("Search could not be completed since there is no path left in the queue!")
                break
            else:
                path = queue.pop(0)
                currentState = path[-1]
                children = self.getChildStates(currentState)
                if len(children) == 0:
                    if currentState.getNumOfItems() >= 5:
                        print("This is our goal: " + str(currentState.getNumOfItems()) + " items >= 5 items" )
                        self.solutionPath = path
                        break
                    elif currentState.getNumOfItems() > 3:
                        nearMisses.append(path)
                else:
                    for child in children:
                        newPath = self.getCopyPath(path)
                        newPath.append(child)
                        queue.insert(0, newPath)
        if self.solutionPath == None and len(nearMisses) > 0:
            print("This is our estimate goal: " + str(currentState.getNumOfItems()) + " items < 5 items" )
            nearMisses = self.sortNearMisses(nearMisses)
            self.solutionPath = nearMisses[0]

    def sortNearMisses(self, nearMisses):
        partialSolutions = nearMisses
        nearMisses = []
        maxNumOfItems = 0
        indexOfMaxNumOfItems = 0
        while len(partialSolutions) > 0:
            for i in range(len(partialSolutions)):
                tempPath = partialSolutions[i]
                lastState = tempPath[-1]
                if i == 0:
                    maxNumOfItems = lastState.getNumOfItems()
                    indexOfMaxNumOfItems = i
                elif lastState.getNumOfItems() > maxNumOfItems:
                    maxNumOfItems = lastState.getNumOfItems()
                    indexOfMaxNumOfItems = i
            partialSolution = partialSolutions.pop(indexOfMaxNumOfItems)
            nearMisses.append(partialSolution)
        return nearMisses

##Calling functions here
#chromeDriver.get('file:///C:/Users/Alperen/Downloads/20210426.html')
_goMiniPuzzlePage()
across_clues,down_clues = _getClues()
answers = _getAnswers()
acrossAnswersLenght,downAnswersLenght = _getAnswerLength(answers)#It gives output like[['1', 4], ['2', 3], ['3', 2], ['4', 1], ['5', 5], ['6', 1], ['7', 5], ['8', 5], ['9', 4]], means first string numbered clue answer can have specified number of letters.
possible_all_across_answers,possible_all_down_answers = getPossibleAnswers(across_clues,down_clues,acrossAnswersLenght,downAnswersLenght)

chromeDriver.quit()

website = "https://www.nytimes.com/crosswords/game/mini"
driverClass = WebDriver()
driverClass.goToMiniPuzzlePage(website)
chromeDriver = driverClass.getDriver()

puzzleSolver = PuzzleSolver(chromeDriver, items)
puzzleSolver.depthFirstSearch()
print("Solution:")
for puzzleState in puzzleSolver.solutionPath:
    print(puzzleState.getNumOfItems())
    puzzleState.printPuzzle()

_createGui(across_clues,down_clues,answers)

# print("answers :")
# print(answers)
# print("across_clues :") 
# print(across_clues)
# print("down_clues :")
# print(down_clues)
# print("acrossAnswersLenght :")
# print(acrossAnswersLenght)
# print("downAnswersLenght :")
# print(downAnswersLenght)

####################################################################################################################

# def _findListSpecifiedChars(List_given, char, index):#index 0 to 4
#     if char != None:
#         check = char
#         print("The original list : " + str(List_given))
#         res = [idx for idx in test_list if idx[index].lower() == check.lower()]
#         print("The list of matching first letter : " + str(res))
#         return res
#     else:
#         return List_given

# def _solvePuzzle(across_possibles,down_possibles,across_clues,down_clues,answers):
#     black_or_not = list()
#     for i in answers:
#         if i[0] == "":
#             black_or_not.append(True)
#         else:
#             black_or_not.append(False)
#     across_nums = list()
#     for i in across_clues:
#         across_nums.append(i[1])
#     down_nums = list()
#     for i in down_clues:
#         down_nums.append(i[1])
#     puzzle = [None]*25
#     across_possible_for_1 = across_possibles[i]
#     print(random.choice(across_possible_for_1))
#     return []
    
    














