from node import *
from semantic_element import *

class DefVar(Node):
    def __init__(self, stack):
        super().__init__()
        stack.pop()
        stack.pop()
        stack.pop()
        self.var_list = stack.pop()
        self.id = Id(stack)
        stack.pop()
        self.type = stack.pop()

    def __repr__(self):
        return f"{type(self).__name__}: {self.type} {self.id} {self.var_list}"

    def validate_semantic(self):
        data_type = self.type.lexeme
        id = self.id.lexeme
        ambit = self.ambit if self.ambit != "" else ""
        if not self.var_exists(data_type, id, ambit):
            self.table.append({
                "id": id,
                "type": data_type,
                "ambit": ambit,
                "params": ''
            })
        else:
            self.errors.append("La variable " + id + " ya existe en el ambito" + ambit)
        aux = self.var_list
        while hasattr(aux, 'id'):
            if not self.var_exists(data_type, aux.id.lexeme, ambit):
                self.table.append({
                    "id": aux.id.lexeme,
                    "type": data_type,
                    "ambit": ambit,
                    "params": ''
                })
            else:
                self.errors.append("La variable " + id + " ya existe en el ambito" + ambit)
            aux = aux.var_list
        if self.next:
            self.next.data_type = self.data_type
            self.next.validate_semantic()


class DefFunc(Node):
    def __init__(self, stack):
        super().__init__()
        stack.pop()
        self.bloq_func = stack.pop()
        stack.pop()
        stack.pop()
        stack.pop()
        self.parameters = stack.pop()
        stack.pop()
        stack.pop()
        self.id = Id(stack)
        stack.pop()
        self.type = stack.pop()
        self.node_return = None

    def __repr__(self):
        return f"{type(self).__name__}: {self.type} {self.id}({self.parameters})"

    def validate_semantic(self):
        ambit = self.id.lexeme
        strParams = ""
        aux = self.parameters
        while hasattr(aux, 'id'):
            data_type = aux.type.lexeme
            if not self.var_exists(data_type, aux.id.lexeme, ambit):
                self.table.append({
                    "id": aux.id.lexeme,
                    "type": data_type,
                    "ambit": ambit,
                    "params": ''
                })
                strParams += aux.type.lexeme
            else:
                self.errors.append("La variable " + aux.id.lexeme + " ya existe en el ambito" + ambit)
            aux = aux.param_list
        data_type = self.type.lexeme
        if not self.func_exists(data_type, self.id.lexeme, '', strParams):
            self.table.append({
                "id": self.id.lexeme,
                "type": data_type,
                "ambit": '',
                "params": strParams
            })
        self.ambit = self.id.lexeme
        self.bloq_func.data_type = data_type
        self.bloq_func.validate_semantic()
        self.ambit = ""
        if self.next:
            self.next.validate_semantic()


class Parameters(Node):
    def __init__(self, stack: list):
        super().__init__()
        stack.pop()
        self.param_list = stack.pop()
        self.id = Id(stack)
        stack.pop()
        self.type = stack.pop()

    def __repr__(self):
        return f"{type(self).__name__}: {self.type} {self.id} {self.param_list}"


class VarList(Node):
    def __init__(self, stack: list):
        super().__init__()
        stack.pop()
        self.var_list = stack.pop()
        self.id = Id(stack)
        stack.pop()
        stack.pop()

    def __repr__(self):
        has_contents = self.id.lexeme is not None
        return ', ' + self.id.lexeme if has_contents else ''


class ParamList(Node):
    def __init__(self, stack: list):
        super().__init__()
        stack.pop()
        self.param_list = stack.pop()
        self.id = Id(stack)
        stack.pop()
        self.type = stack.pop()
        stack.pop()
        stack.pop()

    def __repr__(self):
        has_contents = self.id.lexeme is not None
        return ', ' + self.type.lexeme + self.id.lexeme if has_contents else ''


class Assigment(Node):
    def __init__(self, stack: list):
        super().__init__()
        stack.pop()
        stack.pop()
        stack.pop()
        self.expression = stack.pop()
        stack.pop()
        self.operator = stack.pop()
        self.id = Id(stack)

    def __repr__(self):
        return f"{type(self).__name__}: {self.id.lexeme} {self.operator.lexeme} {self.expression}"

    def validate_semantic(self):
        self.id.validate_semantic()
        if not self.id.data_type:
            self.errors.append("La variable a la que se intenta asignar \'" + self.id.lexeme +"\' no existe")
        self.expression.validate_semantic()
        if self.id.data_type != self.expression.data_type:
            self.errors.append("La expresion " + str(self.expression) + " y  la variable \'" + self.id.lexeme + "\' no coinciden en el tipo de dato ")
        if self.next:
            self.next.data_type = self.data_type
            self.next.validate_semantic()


class If(Node):
    def __init__(self, stack: list):
        super().__init__()
        stack.pop()
        self.other = stack.pop()
        stack.pop()
        self.bloq_sentence = stack.pop()
        stack.pop()
        stack.pop()
        stack.pop()
        self.expression = stack.pop()
        stack.pop()
        stack.pop()
        stack.pop()
        self.if_token = stack.pop()

    def __repr__(self):
        return f"{type(self).__name__} ({self.expression})"

    def validate_semantic(self):
        self.bloq_sentence.data_type = self.data_type
        self.bloq_sentence.validate_semantic()
        self.other.data_type = self.data_type
        self.other.validate_semantic()
        if self.next:
            self.next.data_type = self.data_type
            self.next.validate_semantic()


class While(Node):
    def __init__(self, stack: list):
        super().__init__()
        stack.pop()
        self.bloq = stack.pop()
        stack.pop()
        stack.pop()
        stack.pop()
        self.expression = stack.pop()
        stack.pop()
        stack.pop()
        stack.pop()
        self.while_token = stack.pop()

    def __repr__(self):
        return f"{type(self).__name__} ({self.expression})"

    def validate_semantic(self):
        self.bloq.data_type = self.data_type
        self.bloq.validate_semantic()
        if self.next:
            self.next.data_type = self.data_type
            self.next.validate_semantic()


class Return(Node):
    def __init__(self, stack: list):
        super().__init__()
        stack.pop()
        stack.pop()
        stack.pop()
        self.expression = stack.pop()
        stack.pop()
        stack.pop()

    def __repr__(self):
        return f"{type(self).__name__} {self.expression}"

    def validate_semantic(self):
        self.expression.validate_semantic()
        if self.expression.data_type:
            if self.data_type != self.expression.data_type:
                self.errors.append("El tipo de dato a regresar no coincide con el de la funcion " \
                    + self.ambit + ", " + self.expression.data_type + " y " +  self.data_type)
        else:
            self.errors.append("Se desconoce el tipo de dato del valor a retornar")


class Id(Node):
    def __init__(self, stack: list):
        super().__init__()
        stack.pop()
        self.lexeme = stack.pop().lexeme

    def __repr__(self):
        return f"{type(self).__name__}: {self.lexeme}"

    def __str__(self):
        return self.lexeme

    def validate_semantic(self):
        for item in self._table:
            if item["id"] == self.lexeme and item["ambit"] == self.ambit:
                self.data_type = item["type"]


class Constant(Node):
    def __init__(self, stack: list):
        super().__init__()
        stack.pop()
        self.lexeme = stack.pop().lexeme

    def __repr__(self):
        return f"{type(self).__name__}: {self.lexeme}"

    def __str__(self):
        return self.lexeme

    def validate_semantic(self):
        if "." in self.lexeme:
            self.data_type = "float"
        else:
            self.data_type = "int"

class FunCall(Node):
    def __init__(self, stack: list):
        super().__init__()
        stack.pop()
        stack.pop()
        stack.pop()
        self.params = stack.pop()
        stack.pop()
        stack.pop()
        self.id = Id(stack)

    def __repr__(self):
        return f"{type(self).__name__}: {self.id}({self.params})"

    def validate_semantic(self):
        strParams = ""
        id = self.id.lexeme
        aux = self.params
        while aux.lexeme != None:
            aux.validate_semantic()
            data_type = aux.data_type
            if data_type:
                strParams += data_type
            else:
                self.errors.append("Se desconoce el tipo de dato del argumento '" + str(aux) + \
                    "' en la llamada a funcion de " + id)
            aux = aux.next
        type_return = self.data_type
        flag = False
        for item in self.table:
            if item["id"] == id and item["params"] == strParams:
                self.data_type = item["type"]
                flag = True
        if self.id.lexeme == "print":
            self.id.validate_semantic()
        else:
            if not flag:
                self.data_type = None
            if not self.data_type:
                self.errors.append("Se desconoce la llamada a funcion de " + id)
        if self.next:
            self.next.data_type = type_return
            self.next.validate_semantic()


class Operation(Node):
    def __init__(self, stack: list):
        super().__init__()
        stack.pop()
        self.right = stack.pop()
        stack.pop()
        self.operator = stack.pop()
        stack.pop()
        self.left = stack.pop()

    def __repr__(self):
        return f"{type(self).__name__}: {self.left} {self.operator.lexeme} {self.right}"

    def __str__(self):
        return f"{self.left} {self.operator.lexeme} {self.right}"

    def validate_semantic(self):
        self.right.validate_semantic()
        self.left.validate_semantic()
        error = None
        if not self.left.data_type:
            self.errors.append("Se desconoce el tipo de dato de la parte izquierda")
            error = True
        if not self.right.data_type:
            self.errors.append("Se desconoce el tipo de dato de la parte derecha")
            error = True
        if self.left.data_type and self.right.data_type and self.left.data_type != self.right.data_type:
            self.errors.append("Los tipos de dato de ambos lados de la operacion no coinciden")
            error = True
        if not error:
            self.data_type = self.left.data_type
