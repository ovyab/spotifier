from spotifySorter import *

def main():
    name = input('Welcome to Spotifier! What\'s your name? ')
    prompt = Prompter(name)
    file = prompt.filePrompter()
    prompt.tools(file)
    
test = Spotifier('s.json')
test.songBreakdown()

# StreamingHistory.json