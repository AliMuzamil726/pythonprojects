#define functions here  
#Here are some example functions
#parameters can be added as needed and return statements can be used to return values
#parameters are variables that are passed into functions
#parameters means what operations the function will perform on the values given to it
#return statements are used to return values from functions after performing operations on the parameters



"""def square(x):
	return x * x
def addition(x,y):
    return x+y
def modulus(x,y):
    return x%y
def exponent(x):
    return x**6
    
print(square(6))
print(addition(12,8))
print(modulus(69,2))
print(exponent(4))
def subtraction(x,y):
    return x-y
print(subtraction(10,5))
def multiplication(x,y):
    return x*y
print(multiplication(4,5))
def division(x,y):
    return x/y
print(division(20,4))
def floor_division(x,y):
    return x//y
print(floor_division(22,7))
def cube(x):
    return x**3
print(cube(3))
"""
"""while True:

    def calculator():
        
     x=float(input("Enter first number  = "))
     y=float(input("Enter second number = "))
     op=input("Enter operator (+,-,*,/) = ")
    
     if op=="+":
        sum=x+y
        print(f"The {x} {op}{y} = {sum}")
        return x+y
     elif op=="-":
        sub=x-y
        print(f"The {x} {op} {y} = {sub}")
        return x-y
     elif op=="*":
        pro=x*y
        print(f"The {x} {op} {y} = {pro}")
        return x*y
        
     elif op=="/":
        divide=x/y
        print(f"The {x} {op} {y} = {divide}")
        return x/y
     else:
        print('Invalid')
    

    calculator()
    cont=input("Do you want to continue? (yes/no): ")
    if cont.lower() != 'y':

     break
        """
#parameters and augmentation example

#this is parameter name and parameter name is being passed into the function greet
"""def greet(name):
    print(name)
    return name

#now we are calling the function greet and passing the argument "Ali" and others names to the parameter name
#means we passing the argument "Ali" to the parameter name
greet("Ali")
greet("Bob")
greet("Charlie")
greet("David")
greet("Eve")
greet("Frank")"""


#local and global variable example
#Global means variable that is defined outside a function and can be accessed anywhere in the code
#local means variable that is defined inside a function and can only be accessed within that function

x = "global x"  # This is a global variable

def my_function():

    y = "local y"  # This is a local variable

    print(y)  # Accessing the local variable

    print(x)  # Accessing the global variable
    
my_function()

