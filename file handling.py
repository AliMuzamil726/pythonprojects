#simple file handling by txt file read and write data

#open the file
with open("a12.txt","r") as note:#'with' statement
#Now read the file
 content=note.read() #read,readline,readlines
 print(content)
#content=file.readline() #read,readline,readlines
##print(content)
#content=file.readlines() #read,readline,readlines
#print(content)
#file.close()  #close the file best practice and also with statement


#write data in file
#file=open("a12.txt","w")
#content=file.write("This write mode ")# When we use right mode it will destroy all previous data and add new

#file=open("a12.txt","a")
#content=file.write("\nHello,i am ali muzamil")# in append mode new data will add at new line
