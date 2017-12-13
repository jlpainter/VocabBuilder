import os
import sys
import csv
import random

## ###############################################
## Keep track of a user's score throughout the game play
## ###############################################
class Score:

    def __init__(self, count):

        self.questionCount = count
        self.correct       = 0
        self.wrong         = 0

    ## ############################################################
    def addCorrect(self):
        self.correct = self.correct + 1
        return

    ## ############################################################
    def addWrong(self):
        self.wrong = self.wrong + 1
        return

    ## ############################################################
    def getAverage(self):
        c = self.correct
        n = self.questionCount
        print str(c) + " out of " + str(n) + " correct\n"
        if n == 0:
            print "Divide by zero!"
            return 0
        else:
            avg = float(c)/float(n)
            return (avg*100)

## ###############################################
## Main control of game is handled by the Chooser
## ###############################################
class Chooser:

    def __init__(self, count, database):
        self.questions = count
        self.words     = {}
        self.chosen    = {}
        self.wrong     = []

        # create a score object
        self.score     = Score(count)

        # load the dictionary
        self.loadDictionary(database)

    ## ############################################################
    def loadDictionary(self, database):
        reader = csv.reader( open(database), delimiter = "|" )
        for fields in reader:
            word        = fields[0]
            definition  = fields[1]
            self.words[word] = definition
        return

    ## ############################################################
    def getNewWord(self):
        # make a random choice
        pick  = random.choice(self.words.keys())

        # test if chosen previously
        if self.chosen.has_key(pick):
            return self.getNewWord()
        else:
            self.chosen[pick] = True
            return pick

    ## ############################################################
    def askQuestion(self):
        ## random module stuff
        ## http://docs.python.org/lib/module-random.html
        ## randomly pick a word match or def match type question
        pick = random.choice([0, 1])
        if pick == 0:
            self.askWord()
        else:
            self.askDefinition()
        return

    ## ############################################################
    def askWord(self):

        ## begin by creating a new list of shuffled words
        wordList = []
        for word in self.words:
            wordList.append(word)

        # create random pick list
        pick  = random.sample(wordList, 5) 

        # pick a unique word and answer for this question
        word     = ""
        word     = self.getNewWord()
        answer   = self.words[word]

        # make sure our word is in the pick list
        if word in pick:
            pass
        else:
            r = random.choice( pick )
            idx = pick.index(r)
            pick[idx] = word

        # create alternate answers
        words = []
        for i in range(0,5):
            randomWord = random.choice( pick )
            pick.remove(randomWord)
            words.append(randomWord)

        print " =================================== \n"
        print " Definition >> " + answer
        print "  1. " + words[0]
        print "  2. " + words[1]
        print "  3. " + words[2]
        print "  4. " + words[3]
        print "  5. " + words[4]
        testAns = self.getAnswer()
        testAns = int(testAns - 1)
        if word == words[testAns]:
            print "Correct!\n"
            self.score.addCorrect()
        else:
            print "You chose: " + words[testAns] + " which means: " + self.words[words[testAns]]
            print "Incorrect >> ANSWER: " + word + "\n"
            self.wrong.append(word)
            self.score.addWrong()
        return

    ## ############################################################
    ##  Get the player's answer and test if it is a valid option
    ## ############################################################
    def getAnswer(self):
        answer = ""
        answer = raw_input("?")
        if answer in ([ "1", "2", "3", "4", "5", "q", "Q" ]):
            if answer == "q" or answer == "Q":
                print "Good bye!"
                sys.exit()
            else:
                answer = int(answer)
                return answer
        else:
            print "Invalid input! Try again"
            return self.getAnswer()

    ## ############################################################
    def askDefinition(self):
        ## begin by creating a new list of shuffled words
        wordList = []
        for word in self.words:
            wordList.append(word)

        # create random pick list
        pick  = random.sample(wordList, 5) 

        # pick word and answer
        word     = ""
        word     = self.getNewWord()
        answer   = self.words[word]

        # make sure our word is in the pick list
        wrongWords  = []
        if word in pick:
            pass
        else:
            r = random.choice( pick )
            idx = pick.index(r)
            pick[idx] = word

        # create alternate answers
        definitions = []
        for i in range(0,5):
            randomDef = random.choice( pick )
            pick.remove(randomDef)
            definitions.append( self.words[randomDef] )

            ## keep a list of the words to alert player to real definition
            wrongWords.append(randomDef)

        # shuffle alternate answers
        print " =================================== \n"
        print " Word >> " + word
        print "  1. " + definitions[0]
        print "  2. " + definitions[1]
        print "  3. " + definitions[2]
        print "  4. " + definitions[3]
        print "  5. " + definitions[4]
        testAns = self.getAnswer()
        testAns = int(testAns - 1)

        pickedWord = wrongWords[testAns]
        if answer == definitions[testAns]:
            print "Correct!\n"
            self.score.addCorrect()
        else:
            print "You chose: " + pickedWord + " :: " + definitions[testAns] + "\n"
            print "Incorrect >> ANSWER: " + answer + "\n"
            self.wrong.append(word)
            self.score.addWrong()
        return

    ## ############################################################
    def playGame(self):
        for q in range(0,self.questions):
            number = q + 1
            print "Question " + str(number)
            self.askQuestion()
        avg = self.score.getAverage()
        print " >> Final Score << "
        print "    " + str(avg) + "\n"
        print " >> Words to study << "
        for word in self.wrong:
            print " Word: " + word 
            print " Definition: " + self.words[word] + "\n"
