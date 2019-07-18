import json

class Prompter:
    def __init__(self, name):
        self.name = name
    
    def filePrompter(self):
        filename = input('Welcome, ' + self.name + '! Please enter the name of a valid file you\'d like to analyze: ')
        mystuff = Spotifier(filename)
        
        while True:
            if mystuff.getData() != 'Not a valid file.':
                break
            else:
                filename = input('Invalid file. Please enter the name of a valid file you\'d like to analyze: ')
                mystuff = Spotifier(filename)
        print('Accessed ' + filename + ' successfully.')
        return mystuff
    
    def tools(self, data:'Spotifier'):
        while True:
            command = input('What would you like to do?\n> Enter "A" for an artist breakdown.\n> Enter "S" to view a song breakdown.\n> Enter "F" to search.\n> Enter "Q" to quit./n')
            if command.upper() == 'Q':
                print('Thanks for using Spotifier, ' + self.name + '!')
                break
            elif command.upper() == 'A':
                print('Getting artist breakdown...')
                data.artistBreakdown()
            elif command.upper() == 'S':
                print('Getting song breakdown...')
            elif command.upper() == 'F':
                data.search()
        
class Spotifier:
    def __init__(self, filename):
        self.fileName = filename
        
    def isSubstring(self, sub, phrase): 
        subLength = len(sub)
        phraseLength = len(phrase) # N
        
        for x in range(phraseLength - subLength + 1):
            if phrase[x:x+subLength] == sub:
                return True
        
        return False

    def getData(self):
        try:
            file = open(self.fileName, 'r')
            data = json.load(file)
            file.close()
            return data
        except OSError:
            return 'Not a valid file.'
    
    def getArtistList(self):
        data = self.getData()
        artists = set()
        for obj in data:
            artists.add(obj['artistName'])
        return artists
    
    def getSongList(self):
        data = self.getData()
        songs = set()
        for obj in data:
            songs.add(str(obj['artistName'] + " - " + obj['trackName']))
        return songs
    
    def favoriteSongs(self):
        data = self.getData()
        tally = {}
        for obj in data:
            tally[obj['trackName'] + ' by ' + obj['artistName']] = 0
            
        for obj in data:
            tally[obj['trackName'] + ' by ' + obj['artistName']] += obj['msPlayed']
        return tally
    
    def favoriteArtists(self):
        data = self.getData()
        tally = {}
        for obj in data:
            tally[obj['artistName']] = 0
        
        for obj in data:
            tally[obj['artistName']] += obj['msPlayed']
                
        return tally
    
    def search(self):
        songs = self.getSongList()
        artists = self.getArtistList()
        all = {}
        
        for x in artists:
            all[x] = 'Artist'
        for x in songs:
            all[x] = 'Song'
        for x in all:
            x = x.upper()
        
        while True:
            query = input('What would you like to search for? ')
            q = query.upper()
            results = {}
            found = False
            
            for elem in all:
                srch = self.isSubstring(q, elem.upper())
                if srch:
                    results[elem] = all[elem]
                    found = True
        
            if found:
                if len(results) == 1:
                    print('Found 1 result for ' + q)
                else:
                    print('Found ' + str(len(results)) + ' results for ' + q)
                
                count = 1
                for key in results:
                    print('%3d. %s: %s'%(count, results[key], key))
                    #print(str(count) + '. ' + results[key] + ': ' + key)
                    count += 1
                
                inp = input('Conduct another search? Y/N ')
                if inp.upper() == 'N':
                    break
                
            else:
                inp = input('No results found. Enter Y to search again, N to quit. ')
                if inp.upper() == 'N':
                    break
    
    def convert(self, ms, type):
        sec = ms // 1000
        mins = sec // 60
        seconds = sec - (mins * 60)
        hours = mins / 60
        minutes = mins - (hours * 60)
        days = hours / 24
        if type == 'sec':
            return seconds
        elif type == 'mins':
            return minutes
        elif type == 'hours':
            return hours
        elif type == 'days':
            return days
        
    def getTimes(self):
        data = self.getData()
        first = data[0]
        last = data[-1]
        return first['endTime'] + ' to ' + last['endTime']
    
    def artistBreakdown(self):
        artists = self.getArtistList()
        favArtists = self.favoriteArtists()
        sortedFavArtists = sorted(favArtists.items(), key=lambda item: item[1], reverse = True)
        print('> Here is your artist breakdown, based on your streaming history from ' + self.getTimes() + '.')
        print('> You have ' + str(len(artists)) + ' artists in your library.')
        print('> Your favorite artists are:\n')
        count = 1
        totalTime = 0
        for key in sortedFavArtists:
            print('\t%d. %s, with %.2f hours of listening time.' % (count, key[0], self.convert(key[1], 'hours')))
            totalTime += self.convert(key[1], 'hours')
            count += 1
            if count > 5:
                print('')
                break
        print('> You listened to your favorite artists for a combined %.2f hours.' % totalTime)
        
        totalTime = 0
        for key in sortedFavArtists:
            totalTime += self.convert(key[1], 'hours')
        if totalTime > 24:
            print('> You listened to a combined %.2f days of content on Spotify during this period!' % (totalTime / 24))
        else:
            print('> You listened to a combined %.2f hours of content on Spotify during this period!' % totalTime)
            
    def songBreakdown(self):
        songs = self.favoriteSongs()
        favSongs = sorted(songs.items(), key=lambda item: item[1], reverse = True)
        print('> Here is your song breakdown, based on your streaming history from ' + self.getTimes() + '.')
        print('>Your favorite songs were:\n')
        count = 1
        for x in favSongs:
            minutes = self.convert(x[1],'hours')
            print('\t %d. %s, %.2f hours of listening time' % (count, x[0], minutes))
            count +=1
            if count > 5:
                break