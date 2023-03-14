import os
import csv
import sys

from surprise import Dataset
from surprise import Reader
import secrets

class ExtractData:

    purposeID_to_name = {}
    name_to_purposeID = {}
    ratingsPath = '../PurposeRecommender/training-data/mapping_dataset.csv'
    purposePath = '../PurposeRecommender/training-data/purpose-Table 1.csv'
    
    def loadData(self):

        # Look for files relative to the directory we are running from
        os.chdir(os.path.dirname(sys.argv[0]))

        dataset = 0
        self.purposeID_to_name = {}
        self.name_to_purposeID = {}

        reader = Reader(line_format='user item rating', sep=',', skip_lines=1)

        dataset = Dataset.load_from_file(self.ratingsPath, reader=reader)

        with open(self.purposePath, newline='', encoding='ISO-8859-1') as csvfile:
                purposeReader = csv.reader(csvfile)
                next(purposeReader)  #Skip header line
                for row in purposeReader:
                    purposeID = row[0]
                    purposeName = row[1]
                    self.purposeID_to_name[purposeID] = purposeName
                    self.name_to_purposeID[purposeName] = purposeID

        return dataset
    
    def getpurposeName(self, purposeID):
        if purposeID in self.purposeID_to_name:
            return self.purposeID_to_name[purposeID]
        else:
            return ""
        
    def getpurposeID(self, purposeName):
        if purposeName in self.name_to_purposeID:
            return self.name_to_purposeID[purposeName]
        else:
            return 0

