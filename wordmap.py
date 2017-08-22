import numpy as np
import scipy as sp
import csv

def readFile(filename):
	with open(filename) as f:
		blurbs = f.readlines()
		blurbs = [x.strip() for x in blurbs] 
	f.close()
	return blurbs

def replacePunctuation(line):
	line = line.replace(',', ' ')
	line = line.replace('.', ' ')
	line = line.replace('-', ' ')
	line = line.replace('?', ' ')
	line = line.replace('!', ' ')
	line = line.replace(':', ' ')
	line = line.replace(';', ' ')
	line = line.replace('...', ' ')
	line = line.replace('\'', ' ')
	line = line.replace('\"', ' ')
	line = line.replace('(', ' ')
	line = line.replace(')', ' ')		
	line = line.replace('|', ' ')
	line = line.replace('/', ' ')
	line = line.replace('*', ' ')
	line = line.replace('[', ' ')
	line = line.replace(']', ' ')
	line = line.replace('{', ' ')
	line = line.replace('}', ' ')
	line = line.replace('\\', ' ')
	return line

def buildWordMap(text):
	wordmap = {}
	minWordLen = 4
	for line in text:
		line = str.lower(line)
		line = replacePunctuation(line)
		for word in line.split():
			if len(word) < minWordLen:
				continue
			elif word in wordmap:
				value = wordmap[word]
				wordmap[word] = value + 1
			else:
				wordmap[word] = 1
	return wordmap

def writeCsvFromDict(filename, dict):
	with open(filename, 'wb') as csv_file:
	    writer = csv.writer(csv_file)
	    for key, value in dict.items():
	       writer.writerow([key, value])

def NLP(descriptions, titles, numProjects, blurbMap, titleMap):
	matrix = np.zeros((numProjects, 6))
	for i in range(numProjects):
		title = str.lower(replacePunctuation(titles[i]))
		description = str.lower(replacePunctuation(descriptions[i]))
		title_word_ct = 0
		title_word_match = 0
		title_score = 0
		for word in title.split():
			title_word_ct = title_word_ct + 1
			if word in titleMap:
				title_word_match = title_word_match + 1
				title_score = title_score + titleMap[word]
		blurb_word_ct = 0
		blurb_word_match = 0
		blurb_score = 0
		for word in description.split():
			blurb_word_ct = blurb_word_ct + 1
			if word in blurbMap:
				blurb_word_match = blurb_word_match + 1
				blurb_score = blurb_score + blurbMap[word]
		matrix[i][0] = title_word_ct
		matrix[i][1] = title_word_match
		matrix[i][2] = title_score
		matrix[i][3] = blurb_word_ct
		matrix[i][4] = blurb_word_match
		matrix[i][5] = blurb_score
	return matrix

def readFileIntoList(filename):
	with open(filename) as f:
		lines = f.readlines()
	f.close()
	return lines

NUM_CAMPAIGNS = 2280
topBlurbs = readFile('mostBackedBlurbs.txt')
mostBackedWordmap = buildWordMap(topBlurbs)
writeCsvFromDict('wordmap.csv', mostBackedWordmap)
topTitles = readFile('mostBackedTitles.txt')
mostBackedTitleMap = buildWordMap(topTitles)
writeCsvFromDict('mostBackedTitleMap.csv', mostBackedTitleMap)
descriptions = readFileIntoList('descriptions.csv')
titles = readFileIntoList('titles.csv')
nlp_data = NLP(descriptions, titles, NUM_CAMPAIGNS, mostBackedWordmap, mostBackedTitleMap)
np.savetxt('nlp.csv', nlp_data, delimiter = ",")


