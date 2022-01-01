import os
from rules import *
from stack import Stack

RIGHT = 1
LEFT = 0

class SyntacticAnalyzer():

    def __init__(self):
        self.table = []
        self.rules = []
        self.get_table()
        self.get_rules()
    
    def get_table(self):
        path_file = os.path.join(os.path.dirname(__file__), 'rules/GR2slrTable.txt')
        f = open(path_file, 'r')
        for line in f.readlines():
            self.table.append( [ int (x) for x in line.split('\t') ] )
        f.close()

    def get_rules(self):
        path_file = os.path.join(os.path.dirname(__file__), 'rules/GR2slrRulesId.txt')
        f = open(path_file, 'r')
        for line in f.readlines():
            self.rules.append( [ int (x) for x in line.split('\t') ] )
        f.close()

    def is_accepted(self, code):
        #Creating the stack
        stack = Stack()
        #Initial push
        stack.push(0)
        #Analyzing
        i = 0
        while i < len(code):
            rule = stack.top()
            column = code[i]['number']
            action = self.table[rule][column]
            # Displacement case
            if action > 0:
                stack.push(Node(lexeme=code[i]['lexeme']))
                stack.push(action)
                i += 1
            # Reduction case
            elif action < 0:
                if action == -1:
                    stack.pop()
                    return True, stack.pop()
                rule = abs(action + 1)
                column = self.rules[rule][LEFT]
                pops_left = self.rules[rule][RIGHT] * 2
                if rule == 0 or rule == 3 or rule == 4 or rule == 16 or rule == 17\
                        or rule == 32 or rule == 36 or rule == 37:
                    stack.pop()
                    node = stack.pop()
                elif rule == 2 or rule == 15 or rule == 19 or rule == 29:
                    stack.pop()
                    aux = stack.pop()
                    stack.pop()
                    node = stack.pop()
                    node.next = aux
                elif rule == 5:
                    node = DefVar(stack)
                elif rule == 7:
                    node = VarList(stack)
                elif rule == 8:
                    node = DefFunc(stack)
                elif rule == 10:
                    node = Parameters(stack)
                elif rule == 12:
                    node = ParamList(stack)
                elif rule == 13 or rule == 27 or rule == 38:
                    stack.pop()
                    stack.pop()
                    stack.pop()
                    node = stack.pop()
                    stack.pop()
                    stack.pop()
                elif rule == 20:
                    node = Assigment(stack)
                elif rule == 21:
                    node = If(stack)
                elif rule == 22:
                    node = While(stack)
                elif rule == 23:
                    node = Return(stack)
                elif rule == 24:
                    stack.pop()
                    stack.pop()
                    stack.pop()
                    node = stack.pop()
                elif rule == 26:
                    stack.pop()
                    node = stack.pop()
                    stack.pop()
                    stack.pop()
                elif rule == 31:
                    stack.pop()
                    aux = stack.pop()
                    stack.pop()
                    node = stack.pop()
                    node.next = aux
                    stack.pop()
                    stack.pop()
                elif rule == 33:
                    node = Id(stack)
                elif rule == 34:
                    node = Constant(stack)
                elif rule == 35:
                    node = FunCall(stack)
                elif 39 <= rule <= 42:
                    node = Operation(stack)
                else:
                    node = Node()
                    while pops_left:
                        stack.pop()
                        pops_left -= 1
                row = stack.top()
                stack.push(node)
                stack.push(self.table[row][column])
            # Empty cell
            else:
                return False, None
