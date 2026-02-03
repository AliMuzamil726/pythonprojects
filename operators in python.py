

#operators in python
a=10
b=20
#arithmetic operators
print("The sum is:",a+b)            
print("The difference is:",b-a)
print("The product is:",a*b)
print("The division is:",b/a)
print("The modulus is:",b%a)
print("The exponent is:",a**2)
print("The floor division is:",b//a)
#comparison operators
print(a==b)   #equal to
print(a!=b)   #not equal to
print(a>b)    #greater than
print(a<b)    #less than
print(a>=b)   #greater than or equal to
print(a<=b)   #less than or equal to
#logical operators
print(a<15 and b>15)   #and operator
print(a<15 or b<15)    #or operator
print(not(a<15))        #not operator
#assignment operators
c=a
c+=5
print("The value of c after +=5 is:",c)
c-=3
print("The value of c after -=3 is:",c)
c*=2
print("The value of c after *=2 is:",c)
c/=4
print("The value of c after /=4 is:",c)
c%=3
print("The value of c after %=3 is:",c)
c**=2
print("The value of c after **=2 is:",c)
c//=2
print("The value of c after //=2 is:",c)
#bitwise operators
x=5    #binary: 0101
y=3    #binary: 0011
print("The bitwise AND is:",x&y)   #binary: 0001
print("The bitwise OR is:",x|y)    #binary: 0111
print("The bitwise XOR is:",x^y)   #binary: 0110
print("The bitwise NOT of x is:",~x) #binary: 1010
print("The left shift of x by 1 is:",x<<1) #binary: 1010
print("The right shift of x by 1 is:",x>>1) #binary: 0010
