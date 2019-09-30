from stack_array import Stack
import math

# You do not need to change this class
class PostfixFormatException(Exception):
    pass

def postfix_eval(input_str):
    """Evaluates a postfix expression"""

    """Input argument:  a string containing a postfix expression where tokens 
    are space separated.  Tokens are either operators + - * / ^ or numbers
    Returns the result of the expression evaluation. 
    Raises an PostfixFormatException if the input is not well-formed"""
    stack = Stack(30)
    inputted = input_str.split()
    val_count = 0
    oper_count = 0
    for val in inputted:
        if val.isdigit():
            val = int(val)
            stack.push(val)
            val_count += 1
        elif '.' in val:
            dot_counter = 0
            dig_counter = 0
            neg_counter = 0
            for char in val:
                if char == '.':
                    dot_counter += 1
                if char.isdigit():
                    dig_counter += 1
                if char == '-':
                    neg_counter += 1
            if dot_counter == 1 and (dig_counter + 1) == len(val) and neg_counter == 0:
                val = float(val)
                stack.push(val)
                val_count += 1
            elif dot_counter == 1 and (dig_counter + 2) == len(val) and neg_counter == 1:
                val = float(val)
                stack.push(val)
                val_count += 1
            else:
                raise PostfixFormatException('Invalid token')
        elif '-' in val:
            neg_counter = 0
            dig_counter = 0
            for char in val:
                if char == '-':
                    neg_counter+=1
                if char.isdigit():
                    dig_counter += 1
            if neg_counter == 1 and dig_counter + 1 == len(val) and len(val) > 1:
                val = int(val)
                stack.push(val)
                val_count += 1
            elif neg_counter == 1 and len(val) == 1:
                if stack.num_items >= 2:
                    num1 = stack.pop()
                    num2 = stack.pop()
                    stack.push(num2-num1)
                    oper_count += 1
                elif stack.num_items < 2:
                    raise PostfixFormatException('Insufficient operands')
            else:
                raise PostfixFormatException('Invalid token')

        elif val == '+':
            if stack.num_items >= 2:
                num1 = stack.pop()
                num2 = stack.pop()
                stack.push(num2 + num1)
                oper_count += 1
            elif stack.num_items < 2:
                raise PostfixFormatException('Insufficient operands')
        
        elif val == '*':
            if stack.num_items >= 2:
                num1 = stack.pop()
                num2 = stack.pop()
                stack.push(num2*num1)
                oper_count += 1
            elif stack.num_items < 2:
                raise PostfixFormatException('Insufficient operands')
        elif val == '**':
            if stack.num_items >= 2:
                num1 = stack.pop()
                num2 = stack.pop()
                stack.push(num2**num1)
                oper_count += 1
            elif stack.num_items < 2:
                raise PostfixFormatException('Insufficient operands')
        elif val == '/':
            if stack.num_items >= 2:
                num1 = stack.pop()
                num2 = stack.pop()
                if num1 == 0:
                    raise ValueError
                else:
                    stack.push(num2/num1)
                    oper_count += 1
            elif stack.num_items <2:
                raise PostfixFormatException('Insufficient operands')
        elif val == '<<':
            if stack.num_items >= 2:
                num1 = stack.pop()
                num2 = stack.pop()
                if isinstance(num1,int) and isinstance(num2,int):
                    stack.push(num2<<num1)
                    oper_count += 1
                else:
                    raise PostfixFormatException('Illegal bit shift operand')
        elif val == '>>':
            if stack.num_items >= 2:
                num1 = stack.pop()
                num2 = stack.pop()
                if isinstance(num1,int) and isinstance(num2,int):
                    stack.push(num2>>num1)
                    oper_count += 1
                else:
                    raise PostfixFormatException('Illegal bit shift operand')
        else:
            raise PostfixFormatException('Invalid token')

    if oper_count < (val_count - 1):
        raise PostfixFormatException('Too many operands')
    return stack.pop()


def infix_to_postfix(input_str):
    """Converts an infix expression to an equivalent postfix expression"""

    """Input argument:  a string containing an infix expression where tokens are 
    space separated.  Tokens are either operators + - * / ^ parentheses ( ) or numbers
    Returns a String containing a postfix expression """
    prec = {}
    prec['<<'] = 5
    prec['>>'] = 5
    prec['**'] = 4
    prec['*'] = 3
    prec['/'] = 3
    prec['+'] = 2
    prec['-'] = 2
    prec['('] = 1
    stack = Stack(30)
    PFN = []
    inputter = input_str.split()
    for val in inputter:
        if val.isdigit() == True:
            PFN.append(val)
        elif '.' in val:
            PFN.append(val)
        elif '-' in val and len(val) > 1:
            PFN.append(val)
        elif val == '(':
            stack.push(val)
        elif val == ')':
            while stack.peek() != '(':
                PFN.append(stack.pop())
            stack.pop()
        else:
            if val != '**':
                while (stack.is_empty() == False) and (prec[stack.peek()] >= prec[val]):
                    PFN.append(stack.pop())
            elif val == '**':
                while (stack.is_empty() == False) and (prec[stack.peek()] > prec[val]):
                    PFN.append(stack.pop())
            stack.push(val)
    while stack.is_empty() == False:
        PFN.append(stack.pop())
    x = ' '
    PFN = x.join(PFN)
    return PFN

def prefix_to_postfix(input_str):
    """Converts a prefix expression to an equivalent postfix expression"""
    """Input argument: a string containing a prefix expression where tokens are 
    space separated.  Tokens are either operators + - * / ^ parentheses ( ) or numbers
    Returns a String containing a postfix expression(tokens are space separated)"""
    inputted = input_str.split()
    inputted = inputted[::-1]
    stack = Stack(30)
    PFN = ''
    for val in inputted:
        if val.isdigit():
            stack.push(val)
        elif '.' in val:
            stack.push(val)
        elif '-' in val and len(val) > 1:
            stack.push(val)
        elif val == '+' or val == '-' or val == '*' or val == '/' or val == '<<' or val == '>>' or val == '**':
            op1 = stack.pop()
            op2 = stack.pop()
            PFN = op1 + ' ' + op2 + ' ' + val
            stack.push(PFN)
    return stack.pop()
