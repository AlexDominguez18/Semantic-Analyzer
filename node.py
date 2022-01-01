class Node:
    _ambit = ''
    _table = []
    _errors = []
    def __init__(self, lexeme=None, ambit=None, data_type=None, next=None):
        self.lexeme = lexeme
        self.ambit = ambit if ambit else ""
        self.data_type = data_type
        self.next = next

    def __repr__(self):
        return f"{type(self).__name__}: {self.lexeme}"

    @property
    def ambit(self):
        return Node._ambit

    @ambit.setter
    def ambit(self, ambit: str):
        Node._ambit = ambit

    @property
    def table(self):
        return Node._table

    @table.setter
    def table(self, table: list):
        Node._table = table

    @property
    def errors(self):
        return Node._errors

    @errors.setter
    def errors(self, errors: list):
        Node._errors = errors

    def validate_semantic(self):
        pass

    def var_exists(self, type, id, ambit):
        for item in self._table:
            if item["id"] == id and item["ambit"] == ambit:
                return True
        return False

    def func_exists(self, type, id, ambit, strParams):
        for item in self._table:
            if item["type"] == type and item["id"] == id and item["ambit"] == ambit \
                    and item["params"] == strParams:
                return True
        return False