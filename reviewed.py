#txt file handling
#read mode
file=open("a12.txt","r")#that is simple syntax for opening a file
note=file.read()#used to read data in file
print(note)#print require result
#write mode
book=open("a13.txt","w")
sheet=book.write("it is a write mode \n hello muzamil")
book.close()
#append mode in write a file
book=open("a13.txt","a")
sheet=book.write("\nthis is a append mode for ali")
book.close()
