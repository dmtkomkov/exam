from _base_db import _base_DB

class DB(_base_DB):
	def __init__(self, dbpath, rate):
		_base_DB.__init__(self, dbpath)
		self.rate = rate

	# === # Word operations # === #

	def addWord(self, fname, eng, rus):
		self.createWord(fname, eng, rus)

	def removeWord(self, fname, eng):
		self.removeWordExamples(fname, eng)
		self.deleteWord(fname, eng)

	def changeWord(self, fname, eng, rus1, rus2):
		self.updateWord(fname, eng, rus2)

	def getWords(self, eng = None, rus = None, fname = None, output = 7, updated_before = None):
		return self.getWordEntries(eng, rus, fname, output, updated_before)

	def findWords(self, eng):
		return self.getWordsLike(eng)

	def getSortedWords(self, max_passed):
		return self.getWordsByStats(max_passed, self.rate)

	def getSortedPhrases(self):
		return self.getPrases()

	# === # Stats operations # === #

	def getMaxPassed(self):
		return self.getMaxCounter("passed")

	def getRawDataByDate(self, date):
		return self.getHistoryByStats(date, self.rate)

	def getDatesMinMax(self):
		return self.getMinDate(), self.getMaxDate()

	def changeCounter(self, eng, counter):
		self.updateCounter(eng, counter)

	def getMinMaxDates(self):
		return self.getMinDate(), self.getMaxDate()

	def getCountByDate(self, date_str):
		return self.getHistoryCountByDate(date_str)

	# === # Lingvo operations # === #

	def getLingvoCounters(self, eng):
		return self.getWordStats(eng)

	def setLingvoCounters(self, eng, tr_num, ex_num, ph_num):
		self.setWordStats(eng, tr_num, ex_num, ph_num)

	def addExamples(self, eng, examples):
		self.createExamples(eng, examples)

	def getExamples(self, eng):
		return self.getExamplePairs(eng)

	def getWordsByExample(self, eng):
		return self.getWordPairs(eng)

	def updateExamples(self, eng, examples):
		db_examples = self.getExamplePairs(eng)
		if db_examples:
			examples_to_create = list()
			db_eng_examples = zip(*db_examples)[0]
			for ex_eng, ex_rus in examples:
				if ex_eng in db_eng_examples:
					continue
				examples_to_create.append((ex_eng, ex_rus))
			if examples_to_create:
				self.addExamples(eng, examples_to_create)
		else:
			self.addExamples(eng, examples)

	def getWordRank(self, eng):
		tr, ex, ph, date = self.getLingvoCounters(eng)
		if date is None:
			return None
		return tr + ex + ph

	def removeWordExamples(self, fname, eng):
		self.deleteWordExamples(fname, eng)
