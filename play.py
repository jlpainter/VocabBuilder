import words as Words

count = int(raw_input("How many words? "))
c = Words.Chooser(count, "database.csv")
c.playGame()
