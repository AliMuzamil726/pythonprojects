
while True:

    num1=float(input("Enter 1st Number = "))
    num2=float(input("Enter 2nd Number = "))
    oper=(input("Enter operator (*,+,-,/) = " ))
    if oper=="*":
        prod=num1*num2
        print(f"The product is {prod} ")
    elif oper=="+":
        add=num1+num2
        print(f"The addition is {add}")
    elif oper=="-":
        sub=num1-num2
        print(f"The substraction is {sub}")
    elif oper=="/":
        div=num1/num2
        print(f"The division is {div}")
    else:
        print("Invalid operator") 

    again=input("Do you want to close it: Yes or No = ").lower()
    if again!="n":
        print("Calculator closed")
        break