import urllib2
import pprint, json
import time

def numToStr(num):
	if num < 10:
		return "0" + str(num)
	else:
		return str(num)

class FXPriceGenerator(object):
	oldest_year = 2000
	current_year = int(time.strftime("%Y"))

 	url = "http://api.fixer.io/"
	data = []

 	def __init__(self, base, symbol):
 		super(FXPriceGenerator, self).__init__()
		self.base = base
		self.symbol = symbol
		current_year = int(time.strftime("%Y"))

	def setBase(self, base):
		self.base = base
		self.data = []

	def setSymbols(self, symbol):
		self.symbol = symbol
		self.data = []

	def getBaseSetting(self):
		return "base=" + self.base

	def getSymbolSetting(self):
		return "symbols=" +  self.symbol

	def generateDataUrl(self, year, month, day):
		data_url = self.url + str(year) + "-" + numToStr(month) + "-" + numToStr(day) + "?" + \
				   self.getBaseSetting() + "&" + self.getSymbolSetting()
		return data_url

	def validateDate(self, from_year, to_year, from_month, to_month, from_day, to_day):
		# haven't impletmented the case that same year but different months or days.
		# for example,
		# XXX from 2012 to 2012, from December to Feburary
		# OOO from 2012 to 2013, from December to Feburary
		if not(from_year <= to_year and self.current_year >= to_year and self.oldest_year <= from_year):
			return False
		if not(1 <= from_month <= 12 and 1 <= to_month <= 12):
			return False
		if not(1 <= from_day <= 31 and 1 <= to_day <= 31):
			return False
		return True

	def deriveData(self, from_year, to_year=-1, from_month=1, to_month=1, from_day=1, to_day=1):
		self.data = []
		if to_year == -1:
			to_year = from_year
		if self.validateDate(from_year, to_year, from_month, to_month, from_day, to_day):
			while from_year < to_year or from_month < to_month or from_day < to_day:
 				# if from_year == to_year:
 				# 	if from_month  == to_month:
 				# 		if from_day > to_day:
 				# 			break
 				parametored_url = self.generateDataUrl(from_year, from_month, from_day)

				print from_year, from_month, from_day
				try:
					textData = urllib2.urlopen(parametored_url).read()
				except urllib2.HTTPError:
					pass
				else:
					json_data = json.loads(textData)
					if json_data not in self.data:
						self.data.append(json_data)
				if from_day < 31:
					from_day += 1
				elif from_month < 12:
					from_month += 1
					from_day = 1
				else:
					from_year += 1
					from_month = 1
					from_day = 1
			return self.data
		else:
			print "The date is not valid."

	def saveDataToFile(self, file_name=-1):
		if file_name == -1:
			file_name = self.base + "vs" + self.symbol + self.data[0]["date"] + \
						"to" + self.data[-1]["date"]
			#USDvsJPY2015-01-01to2016-01-01.txt
		with open(file_name + '.txt', 'w') as outfile:
		    json.dump(self.data, outfile)
	

# generator = FXPriceGenerator("USD","JPY")
# generator.deriveData(2010, to_year=2016)
# generator.saveDataToFile()


def calculateDayProbability(file_name):
	occurence = [0 for x in range(31)]
	up_count = [0 for x in range(31)]
	diff_total = [0 for x in range(31)]
	with open(file_name) as data_file:    
	    data = json.load(data_file)
	# pprint.pprint(data)
	for i in range(len(data)):
		if 0 < i:
			day = int(data[i]["date"][-2:])
			occurence[day-1] += 1
			diff_total[day-1] += (data[i]["rates"]["JPY"] - data[i-1]["rates"]["JPY"])
			isUp = data[i]["rates"]["JPY"] > data[i-1]["rates"]["JPY"]
			if isUp:
				up_count[day-1] += 1
	probs= []
	for i in range(len(occurence)):
		probs.append({"day": i+1,
			    "occurence": occurence[i],
				"up count": up_count[i],
				"probability": 100.0*float(up_count[i])/float(occurence[i]),
				"diffrence total": diff_total[i]})
	sortedProbs = sorted([x["probability"] for x in probs])
	
	for i in range(len(sortedProbs)):
		for dailyProb in probs:
			if sortedProbs[i] == dailyProb["probability"]:
				print "[Day" + numToStr(dailyProb["day"]) + "] Occurence: " + numToStr(dailyProb["occurence"]) +\
					  "  up count: " + numToStr(dailyProb["up count"]) + "  probability: " + \
					  "%.2f" % dailyProb["probability"] + "%  diffrence total: " + str(dailyProb["diffrence total"])
				probs.remove(dailyProb)

calculateDayProbability("USDvsJPY2009-12-31to2015-12-31.txt")
