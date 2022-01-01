class SemanticElement():

    def __init__(self, id='', type='', ambit='', strParams=''):
        self.id = id
        self.type = type
        self.ambit = ambit
        self.strParams = strParams
    
    def get_id(self):
        return self.id
    
    def get_type(self):
        return self.type
    
    def get_ambit(self):
        return self.ambit
    
    def get_strParams(self):
        return self.strParams