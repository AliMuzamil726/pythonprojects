#import means we import a module that is prebuild in python 
#such as import math means math modules that contains math functions

import math
"""print(math.sqrt(18))
print(math.pi)
print(math.sin(30))
print(math.sin(90))
print(math.sin(0))
print(math.sin(180))
print(math.sin(360))
print(math.sin(270))"""
"""print(math.log(10))"""

#print(math.exp2(5))
while True:
    x=int(input("Enter any number = "))
    print(f"The Factorial of {x} is ",math.factorial(x))

    z=input(("Do you want to continue the progam! (Y/N) = ")).lower()
    if z=="n".lower():
        print("Exiting the program!")
        break