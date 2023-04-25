class AddUpdateRemove:
    def __init__(self, db):
        self.db = db
        self.cursor = db.cursor()

    def addSpecies(self):
        #add new species to the tax tables
        newSpecies = input('''
            Enter the Binomial nomenclature of the new organism you would like to add:
            ''')
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
    # def update(self, path):

    # def remove(self, path):
