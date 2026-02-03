tasks=[]
while True:
    print("1.Add task ")
    print("2.Remove task ")
    print("3.View task ")
    print("4.Exit  ")
    user=input(("Enter b\w (1___4) = "))
    if user=="1":
        task=input(("Enter Your task name: "))
        tasks.append(task)
        print("\nTask add successfully!")
    elif user=="2":
        if not tasks:
            print("No task available")
        else:
            num=int(input(("Enter task you want to remove:")))
            if 1<=num <=len(tasks):
                removed=tasks.pop(num-1)
                print(f"Removed Successfully!{removed}")
            else:
                print("Invalid task!")
    elif user=="3":
        if not tasks:
            print("No tasks are available")
        else:
            print("\n Yours tasks are:") 
            for i, task in enumerate(tasks,start=1):
                print(f"{i}.{task}")  
    elif user=="4":
        print("Exiting form lists tasks manager!")
        break
    else:
        print("Invalid choose.Try again!")








 