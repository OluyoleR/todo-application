import typer
import time
import mysql.connector
app = typer.Typer()
db = mysql.connector.connect(
    host      = 'localhost',
    user      = 'root',
    password  = 'password',
    database  = 'events_project'
)

mycursor = db.cursor()
class Task:
    def __init__(self,name,date,status):
        self.name = name
        self.status = status
        self.complete = False
        self.date = date

@app.command(short_help = "This command displays a list of all the tasks which are active and waiting to be completed.")
def display_active_tasks():
    query = ("SELECT * FROM Tasks WHERE status = 'active';")
    mycursor.execute(query)
    active_task_list = mycursor.fetchall()

    print("List of current and active tasks:\n")
    for task in active_task_list:
        print(f"{task}\n")

@app.command()
def add_task_P():
        print("Without giving a task name,description, or due date you have entered prompt mode where you are prompted to enter these values individually - this mode helps you pause and think over the actual values you want for the task")
        print("Alternatively you can add a task in just one line of text straight from the command line by entering todo.py add-one-task '[task name]' '[task description]'  '[task date as YYYY-MM-DD]'}\n")
        use_line = input("Enter Y to proceed in prompt mode or N to try  to exit and try again from the command line ")
        if use_line == "N":
            return
        
        print("In prompt mode you always have a chance start over if you have made changes you did not want to keep and even after you have they may still be reverted so you can just focus on learning the app and entering your chosen task information,exit and start over ? (Y/N)")
        print("In order the steps are 1. Enter a task name however long you would like\n2.A description of your choice(try to make it unique)\n3.a date in format of YYYY-MM-DD")
        print("For the date you must make absolutely sure that you do not use anything other than hyphens to separate the numbers and that you have no spaces before and after the date you enter")
        while True:
            name = input("Enter the new task name ")
            description = input("Enter the description for the new task here: ")
            due_date = input("Enter the task due date Ex: 2020-11-11: ")
            confirmation  = input(F"Are you sure that you would like to add the following task: Name:{name}\nDescription:{description}\nDue:{due_date}\n (Y to proceed or N to start over X to exit without changes)")
            if confirmation == "X":
                print("No changes were made and no more prompts will be asked unless you add-one-task again")
                return
            if confirmation == "N":
                pass
            if confirmation == "Y":
                query = F"INSERT INTO `Tasks`(`Name`,`Description`,`Status` ,`Complete` ,`DueDate`)VALUES('{name}','{description}','active',0,'{str(due_date)}'); "
                mycursor.execute(query)
                db.commit()
                break
        
        print("This is the full task list with the task that you just added included\n")
        display_active_tasks()
        keep =  input(F"Enter Y to keep this new task list which includes ({name,description,due_date}) or N to discard the change :  (Y/N)")
        if keep == "Y":
            print("changes have been saved ")
            display_active_tasks()
            return
        if keep == "N":
            query = F"SELECT TaskId from Tasks where Description = '{description}' AND DueDate = '{due_date}'"
            mycursor.execute(query)
            id = mycursor.fetchall()[0][0]
            delete_query = f"DELETE FROM Tasks where TaskId = {id};"
            mycursor.execute(delete_query)
            db.commit()
            print("REVERTED TASK LIST")
            display_active_tasks()
            return
        

@app.command(help= "this command either takes 3 inputs which are '[task name]' '[task description]'  '[task date as YYYY-MM-DD]' or no input which puts you into prompt mode where name,task, and description are obtained individually")
def add_task_CL(name:str  ,description:str, due_date:str): 
    try:
        confirm = input(F"\nTask to Be added:\n\nName:{name}\nDescription:{description}\nDue:{due_date}\nAre you certain this is the task you would like to add ? (Y to proceed/N to start over) ") 
        if confirm == "Y":
            query = F"INSERT INTO `Tasks`(`Name`,`Description`,`Status` ,`Complete` ,`DueDate`)VALUES('{name}','{description}','active',0,'{str(due_date)}'); "
            print(query)
            mycursor.execute(query)

            db.commit()
        if confirm =="N":
            print("\nNo new tasks were added ")
            print("Try again by entering todo.py add-one-task '[name of the task]' '[description of the task]' [due date(YYYY-MM-DD)] \n ALTERNATIVELY you can enter todo.py add-task-p to try entering your information as a prompt")
        if confirm =="Y":
            print("New task has been added\nYou can always view the list of tasks and delete them using the following todo.py delete-task to start the process for deleting it")
    except: 
        raise typer.BadParameter("missing a parameter")
    display_active_tasks()
@app.command()
def complete_one_task():
    print("complete-one-task is an existing feature whcih has the benefits of being simple to use when a task needs to be marked as complete\n")
    print("This is useful if you want to mark exactly one task as completed but a detriment when you have many tasks you need update at once")
    print("If you are interested in trying a feature that allows many tasks to be completed quickly try todo.py complete-many")
    print("complete many lets you manage many tasks which is useful but this also allows you to make more errors in your task list")
    leave = input("Exit to try complete-many? (Y/N to continue with complete-one)")
    if leave == "Y":
        return
    display_active_tasks()
    task_num = input("Enter the number of the task you would like marked as completed: ")
    query = f"UPDATE Tasks set Complete = 1 where TaskId = {task_num}"
    confirmation = input(F'Are you sure that you would like to mark this task as completed : {task_num} Y/N: ')
    if confirmation == "Y":
        mycursor.execute(query)
        db.commit()
        print("Task has been marked complete")  
    else:
        print("no changes were made to your tasks")
    display_active_tasks()

@app.command()
def complete_many(): 
    
    print("complete-one is a new feature similar to complete-one except it continues taking input for numbers of tasks that you want to mark as completed")
    print("The upside of this is that you can update your completed tasks faster while the downside is that you have the potential to make large sweeping changes you might not always want to keep so be careful\n\n")
    print("Here you trade the simplicity and slow nature of many complete-ones for the speed and potential issues of complete-many")

    choice =input("If you would like to just complete one task instead enter C\nfor a detailed explanation of complete-many before proceeding enter D\nand if you would just like to jump in enter J\n")
    if choice == "C":
        complete_one_task()
    if choice == "J":
        pass
    if choice == "D":
        print("compelte many is a mode where you can sort of handpick tasks you want marked for completion and then agree to keep those changes all at once\n")
        print("For this to be done you will get a list of all tasks and you can decide which you want marked\n")
        print("Then you enter the numbers corresponding to those tasks repeatedly and the list of your choices will be shown to help you visually keep track\n ")
        print("inputs will be accepted until you exit or confirm choices\n ")
        print("For example entering in [1] then entering [2] and [X] would cause no changes and end complete-many-mode X negates your prior choices \n")
        print("Entering [6] then [7] then [2] would cause 6,7,2 to appear in the tasks marked for completion then entering C would confirm your choices and give you one last view of how they look before you commit them in the next step\n ")
        print("basic controls : X-no save exit,C-confirm,display-tasks-see all tasks regardless of completion,CL-clear choices marked\n")
        proceed = input("Do you want to proceed and try this ? (Y/N)")
        if proceed == "N":
            print("You can retry this feature anytime and get more info using todo.py complete-many --help on the command line")
            return
    display_active_tasks()
    distraction_counter = 0
    tasks = set()
    while True:
        print(F"These tasks among the above are set to marked as complete: {tasks}")
        finished_task = input("Enter the number of the task which you have completed, X to exit without saving , C to confirm choices  or display-active-tasks to view both tasks that are set to be completed and those that are not ")
        if finished_task.isnumeric():
            distraction_counter +=1
        print(F"Tasks that will set to complete when you confirm(C): {tasks}")
        if finished_task == "X":
            print("No changes will be made")
            return
        if finished_task == "display-active-tasks":
            display_active_tasks()
            print(F"These tasks among the above are set to marked as complete: {tasks}")
        if finished_task == "C":
            print(F"Choices : {tasks}")
            break
        if distraction_counter >=4 :
            distraction_counter = 0 
            print("It might tempting to complete many tasks at once, but make sure you have actually completed them")
            curr = []
            for task_num in tasks:
                query = f"SELECT * FROM Tasks where TaskId = {task_num}"
                mycursor.execute(query)
                curr.append(mycursor.fetchone())
            print(F"Are you sure you completed these tasks \n {curr} \n")
            cont = input("Enter N to start the list over or Y to continue adding: ")
            if cont == "N":
                tasks = set()
        if finished_task.isnumeric():
            tasks.add(finished_task)

    for task_num in tasks:
        query = f"UPDATE Tasks set Complete = 1 where TaskId = {task_num}"
        mycursor.execute(query)

    db.commit()
    display_active_tasks()

@app.command()
def merge(task1:int,task2:int):
    print("tasks merged\n new task name: test task name 1 AND test task name 2 : due: 2020-11-11")

if __name__ == "__main__":
    app()
