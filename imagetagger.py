import mariadb


class ImageTagger:
	def __init__(self):
		self.conn = mariadb.connect(user="ehbot", password="Tpeys9NRs9RqXIexaJhu", database="ehbot", host="localhost")
		self.cursor = self.conn.cursor()
		self.path = "/sftp/nas/upload/eh/pics/"

	def close(self):
		self.cursor.close()
		self.conn.close()

	def strToTags(self, string, tagsplit=",", combosplit="+"):
		if string == "":
			return [[]]

		tags = string.split(tagsplit)
		taggroups = []

		for tag in tags:
			taggroups.append(tag.split(combosplit))

		return taggroups

	def registerImage(self, path, name, tags, description=None, setId=None, setNo=None):
		try:
			self.cursor.execute("INSERT INTO imagetags (path, name, description, tags, setId, setNo) VALUES (?,?,?,?,?,?)", (path, name, description, tags, setId, setNo))
			return {"status":0}
		except mariadb.IntegrityError as e:
			return {"status": 1, "error": e}

	def getImageOptions(self, tags):
		self.cursor.execute("SELECT id, tags FROM imagetags")
		files = self.cursor.fetchall()
			
		options = []
			
		for tag in tags:
			for i in files:
				if all(elem in i[1].split(",") for elem in tag):
					options.append(i[0])
		
		self.cursor.execute("SELECT id, path, setId FROM imagetags WHERE id in ({0})".format(str(options)[1:-1]))
		options = self.cursor.fetchall()

		return options
	
	def getSet(self, setId):
		self.cursor.execute("SELECT id, path, setId, setNo FROM imagetags WHERE setId = ?", (setId,))
		return self.cursor.fetchall()
	

it = ImageTagger()

images = it.getImageOptions(it.strToTags("")) 

print(it.getSet(1))

it.close()


