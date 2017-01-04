import unicodedata
import quopri
import os

EMOJIDB = "database/emojis.txt"

class MojiCoder:
    def __init__(self):
        self._mojiDict = {}
        self._asciiDict = {}
        emojifile = open(os.path.normpath(EMOJIDB), 'r')
        emojifile.seek(0)
        contents = emojifile.readlines()
        emojifile.close()
        for line in contents:
            (key, val) = line.split('=>')
            self._mojiDict[int(key)] = val
            self._asciiDict[val] = int(key)
            # print(line)

    def _AddEmoji(self, emoji, value='value not specified'):
        if value == 'value not specified':
            value = unicodedata.name(emoji)
        key = ord(emoji)
        self._mojiDict[key] = value

        #Not the same emojifile as above
        emojifile = open(EMOJIDB, 'a')
        emojifile.write('\n' + str(key) + '=>' + value)
        emojifile.close()
        print (self._mojiDict)

    def Demoji(self, content): # content is the string containing emojis
        workingString = content #self._ConvertFromQuotedPrintable(content)
        # print("Content in coder", type(content))
        returnList = []
        contentParts = list(workingString)
        for part in contentParts:
            codePoint = ord(part)
            if codePoint not in self._mojiDict:
                self._AddEmoji(part)
            returnList.append(self._mojiDict[codePoint].strip("\n"))
        return "".join(returnList).strip()

    # returns single emoji based on passing the value in.  You will have to build text around
    # this returned emoji data *fingers crossed*
    def Enoji(self, content): # content is the new emoji that we wish to get
        workingString = content
        returnList = []
        '''
        take content, find it in the values of the dictionary and then
        get the key.  turn the key from a number into a string and put in returnList
        '''

        return "".join(returnList).strip()
        pass





def main():
    # test = MojiCoder()
    # test.AddEmoji('💩')
    print("testing")

if __name__ == "__main__":
    main()
