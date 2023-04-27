class Browse:
    def __init__(self, db):
        self.db = db
        self.cursor = db.cursor()
        self.promptBrowse()

    #prompts the user for browsing options
    def promptBrowse(self):
        species = input('''
            Enter the binomial nomenclature of the species you would like to browse (x to exit).
            ''')
        if species == 'x':
            return
        if self.checkExists(species) == False:
            print('Invalid species. Please try again.')
            self.promptBrowse()
            return
        infoChoice = input('''
        1. Get fungal traits
        2. Get genomic information
        3. Get transporter gene information
        ''')
        if infoChoice == '1':
            fungalTraits = self.getFungalTraits(species)
            self.printData(fungalTraits)
        elif infoChoice == '2':
            genomicInfo = self.getGenomicInfo(species)
            self.printData(genomicInfo)
        elif infoChoice == '3':
            transporterInfo = self.getTransporterInfo(species)
            self.printTransporterInfo(transporterInfo)
        else:
            print('Invalid input. Please enter a number between 1 and 3.')
            self.promptBrowse()

    #gets the fungal traits of a species
    def getFungalTraits(self, species):
        print(species)
        paramDict = {
            'binomial': species
        }
        self.cursor.execute('''
            SELECT * FROM fungalTraits WHERE Species = %(binomial)s
            ''', paramDict)
        columns = self.cursor.description
        result = [{columns[index][0]:column for index, column in enumerate(value)} for value in self.cursor.fetchall()]
        resultKeys = result[0].keys()
        fungalTraits = {}
        for key in resultKeys:
            if(result[0][key] != ''): fungalTraits[key] = result[0][key]
        return fungalTraits
    
    #gets the genomic information of a species
    def getGenomicInfo(self, species):
        paramDict = {
            'binomial': species
        }
        self.cursor.execute('''
            SELECT * FROM genomesInfo WHERE species = %(binomial)s
            ''', paramDict)
        columns = self.cursor.description
        result = [{columns[index][0]:column for index, column in enumerate(value)} for value in self.cursor.fetchall()]
        genomicInfo = {}
        for key in result[0]:
            if(result[0][key] != ''): genomicInfo[key] = result[0][key]
        return genomicInfo

    #gets the transporter genes and their qunatities of a species
    def getTransporterInfo(self, species):
        paramDict = {
            'binomial': species
        }
        self.cursor.execute('''
        SELECT t.transporterID, COUNT(*) AS transporterQuantity
        FROM genomesInfo gi JOIN transporters t 
        ON gi.genomeID = t.genomeID
        WHERE gi.species = %(binomial)s
        GROUP BY t.transporterID
        ORDER BY transporterQuantity DESC;
            ''', paramDict)
        columns = self.cursor.description
        transporterInfo = self.cursor.fetchall()
        return transporterInfo
    
    #prints the data in a readable format
    def printData(self, data):
        for key in data:
            print(key + ': ' + data[key])
        self.promptBrowse()

    #prints the transporter info in a readable format
    def printTransporterInfo(self, data):
        choice = input("""
        How many transporters would you like to see (type all or the number)? 
        """)
        if choice == 'all':
            for row in data:
                print('Transporter ID: ' + str(row[0]) + ', Quantity: ' + str(row[1]))
        else:
            for i in range(0, int(choice)):
                print('Transporter ID: ' + str(data[i][0]) + ', Quantity: ' + str(data[i][1]))
        self.promptBrowse()
    
    #checks if a species exists in the database
    def checkExists(self, species):
        checkSpecies = {
            'binomial': species
        }
        self.cursor.execute('''
            SELECT * FROM Species WHERE species = %(binomial)s;
            ''', checkSpecies)
        self.cursor.fetchall()
        if self.cursor.rowcount == -1:
            return False
        else:
            return True