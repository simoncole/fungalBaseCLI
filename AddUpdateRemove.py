class AddUpdateRemove:
    def __init__(self, db):
        self.db = db
        self.cursor = db.cursor()

    def addSpecies(self):
        #add new species to the tax tables
        newSpecies = input('''
            Enter the Binomial nomenclature of the new organism you would like to add:
            ''')
        if self.checkExists(newSpecies) == True:
            print('Species already exists in the database. Please try again.')
            self.addSpecies()
        
        paramDict = {
            'binomial': newSpecies,
            'genus': newSpecies.split(' ')[0]
        }
        
        self.cursor.execute('''
            INSERT INTO Species(species, genus)
            VALUES(%(binomial)s, %(genus)s);
        ''', paramDict)
        self.db.commit()

        traitsChoice = input("Would you like to add traits for this new species? (y/n)")
        if traitsChoice == 'y':
            self.addFungalTraits(newSpecies)
    
    def addFungalTraits(self, newSpecies):
        #add the new specie's fungal traits
        self.cursor.execute('''
            DESCRIBE fungalTraits;
        ''')
        traitsList = self.cursor.fetchall()
        traitsList = [trait[0] for trait in traitsList]
        traitsDict = {}
        for trait in traitsList:
            if trait == 'species':
                traitsDict[trait] = newSpecies
            else: 
                newTrait = input("Enter the " + trait + " for " + newSpecies + " (press enter to skip): ")
                traitsDict[trait] = newTrait
        insertString = '''
            INSERT INTO fungalTraits(
                '''
        for trait in traitsList:
            insertString += trait + ', '
        insertString = insertString[:-2] + ') VALUES('
        for trait in traitsList:
            insertString += '%(' + trait + ')s, '
        insertString = insertString[:-2] + ');'
        self.cursor.execute(insertString, traitsDict)
        self.db.commit()

    def update(self):
        #ability to change the taxonomy and fungal traits of an existing species
        species = input('''
            Enter the binomial nomenclature of the species you would like to update.
            ''')
        if self.checkExists(species) == False:
            print('Invalid species. Please try again.')
            self.update()
        updateChoice = input('''
            1. Update taxonomy
            2. Update fungal traits
            ''')
        if updateChoice == '1':
            self.updateTaxonomy(species)
        elif updateChoice == '2':
            self.updateFungalTraits(species)
        else:
            print('Invalid input. Please enter a number between 1 and 2.')
            self.update()
        
    
    def updateTaxonomy(self, species):
        #update the binomial nomeclature of an existing species
        self.cursor.execute('''
            SELECT * FROM Species WHERE species = %(binomial)s
            ''', {'binomial': species})
        columns = self.cursor.description
        result = [{columns[index][0]:column for index, column in enumerate(value)} for value in self.cursor.fetchall()]
        resultKeys = result[0].keys()
        speciesDict = {}
        for key in resultKeys:
            if(result[0][key] != ''): speciesDict[key] = result[0][key]

        newSpecies = input('''
            Enter the new binomial nomenclature for this species:
        ''')
        updateDict = {
            'newSpecies': newSpecies,
            'newGenus': newSpecies.split(' ')[0],
            'species': species
        }
        updateString = '''
            UPDATE Species SET species = %(newSpecies)s, genus = %(newGenus)s
            WHERE species = %(species)s;
        '''
        self.cursor.execute(updateString, updateDict)
        self.db.commit()
        updateChoice = input('''
            Would you like to update the fungal traits for this species? (y/n)
            ''')
        if updateChoice == 'y':
            self.updateFungalTraits(newSpecies)
        else:
            return
    
    def updateFungalTraits(self, species):
        #update the fungal traits of an existing species
        self.cursor.execute('''
            SELECT * FROM fungalTraits WHERE species = %(binomial)s
            ''', {'binomial': species})
        columns = self.cursor.description
        result = [{columns[index][0]:column for index, column in enumerate(value)} for value in self.cursor.fetchall()]
        resultKeys = result[0].keys()
        traitsDict = {}
        for key in resultKeys:
            if(result[0][key] != ''): traitsDict[key] = result[0][key]
        print(traitsDict)
        traitsChoice = input('''
            Enter the name of the trait you would like to update (type n to quit):
            ''')
        if traitsChoice == 'n':
            return
        else:
            newTrait = input('''
                Enter the new value for this trait:
                ''')
            updateDict = {
                'newTrait': newTrait,
                'species': species,
                'trait': traitsChoice
            }
            updateString = '''
                UPDATE fungalTraits SET ''' + traitsChoice + ''' = %(newTrait)s
                WHERE species = %(species)s;
            '''
            self.cursor.execute(updateString, updateDict)
            self.db.commit()
            self.updateFungalTraits(species)
    def remove(self):
        species = input('''
            Enter the binomial nomenclature of the species you would like to remove. 
            This will remove the taxonomy for this species as well as its fungal traits: 
            ''')
        removeDict = {
            'species': species
        }
        removeString = '''
            DELETE FROM Species WHERE species = %(species)s;
            '''
        self.cursor.execute(removeString, removeDict)
        affectedRows = self.cursor.rowcount
        if affectedRows != 0:
            self.db.commit()
            print('''
                Species removed.
                ''')
            return
        else:
            print('''
                Species not found.
                ''')
            return

    def checkExists(self, species):
        checkSpecies = {
            'binomial': species
        }
        self.cursor.execute('''
            SELECT * FROM Species WHERE species = %(binomial)s
            ''', checkSpecies)
        if self.cursor.rowcount == -1:
            return False
        else:
            return True