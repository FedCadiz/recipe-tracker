from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from tkinter import filedialog
import csv

root = Tk() #create window
root.geometry("1080x720") #set window size
root.resizable(False,False)
root.title("Fridge Tracker") #name window

icon = PhotoImage(file="Chungay.png") #turn png to photo image
root.iconphoto(True, icon) #set photo to window icon


# =====================Fridge====================== #

def addFridge():
    def submit():
        if addFridgeEntry.get() == "":
            pass
        else:
            with open("fridge.csv", "a", newline="") as fridgeCSV:
                csv_writer = csv.writer(fridgeCSV)
                csv_writer.writerow([addFridgeEntry.get()])
                addFridgeEntry.delete(0,END)

            fridgeItemsListBox.delete(0,END)

            with open("fridge.csv", "r") as fridgeCSV:
                csv_reader = csv.reader(fridgeCSV)

                for line in fridgeCSV:  
                    fridgeItemsListBox.insert(0,line)




    addFridgeWindow = Toplevel()

    addFridgeLabel = Label(addFridgeWindow, text="Add Fridge Item",font=("Helvetica",10))
    addFridgeLabel.pack(padx=10,pady=5)

    addFridgeEntry = Entry(addFridgeWindow,font=("Helvetica",10))
    addFridgeEntry.pack(padx=10)

    addFridgeButton = Button(addFridgeWindow, text="SUBMIT",command=submit,font=("Helvetica",10,"bold"))
    addFridgeButton.pack(pady=5)


def deleteFridge():
    try:
        if messagebox.askokcancel(title="Delete Item",message="Delete Item?"):
            fridgeItems = list()
            with open("fridge.csv", "r") as fridgeCSV:
                csv_reader = csv.reader(fridgeCSV)
                for row in csv_reader:
                    fridgeItems.append(row)

            selected = [(fridgeItemsListBox.get(fridgeItemsListBox.curselection()))]
            selected = [x[:-1] for x in selected]

            fridgeItems.remove(selected)

            with open("fridge.csv", "w", newline="") as fridgeCSV:
                csv_writer = csv.writer(fridgeCSV)
                csv_writer.writerows(fridgeItems)

            fridgeItemsListBox.delete(0,END)

            with open("fridge.csv", "r") as fridgeCSV:
                csv_reader = csv.reader(fridgeCSV)

                for line in fridgeCSV:  
                    fridgeItemsListBox.insert(0, line)
        else:
            pass
    except TclError:
        messagebox.showerror(title="Delete Item",message="Please select a fridge item")


fridgeFrame = Frame(root,bd=5,relief=RAISED)
fridgeFrame.pack(side=LEFT,anchor="n",fill=Y)

fridgeTitle = Label(fridgeFrame,text="FRIDGE",font=("Helvetica",25,"bold"))
fridgeTitle.pack()

fridgeScroll = Scrollbar(fridgeFrame, orient=VERTICAL)

fridgeItemsListBox = Listbox(fridgeFrame,font=("Helvetica",15),height=26, yscrollcommand=fridgeScroll.set)

with open("fridge.csv", "r") as fridgeCSV:
    csv_reader = csv.reader(fridgeCSV)

    for line in fridgeCSV:  
        fridgeItemsListBox.insert(END,line)

fridgeScroll.config(command=fridgeItemsListBox.yview)
fridgeScroll.pack(side=RIGHT,fill=Y)
fridgeItemsListBox.pack()

fridgeAddButton = Button(fridgeFrame, text="Add Item",command=addFridge)
fridgeAddButton.pack(side=LEFT, padx=10,pady=5)

fridgeDeleteButton = Button(fridgeFrame, text="Delete Item", command=deleteFridge)
fridgeDeleteButton.pack(side=RIGHT, padx=10,pady=5)

# ====================Recipes======================= #

def addRecipes():
    def selectImage():
        global filePath
        filePath = filedialog.askopenfilename()
        addRecipesPicture.config(text="Image Chosen")

    def submit():
        recipesFieldNames = ["name","image","ingredients","instructions"]
        with open("recipes.csv", "a",newline="") as recipesCSV:
            csv_writer = csv.DictWriter(recipesCSV, recipesFieldNames)
            csv_writer.writerow({"name":addRecipesName.get(),"image":filePath,"ingredients":addRecipesIngredients.get("1.0","end-1c"),"instructions":addRecipesInstructions.get("1.0","end-1c")})
        recipesListFrame.destroy()
        showRecipes()
        

    addRecipesWindow = Toplevel(padx=20,pady=20)

    Label(addRecipesWindow,text="Recipe Name",font=("Helvetica 12")).grid(row=0,column=0,padx=(0,10))

    addRecipesName = Entry(addRecipesWindow,width=30)
    addRecipesName.grid(row=0,column=1)

    addRecipesPicture = Button(addRecipesWindow,text="Select Image", command=selectImage)
    addRecipesPicture.grid(row=0,column=2,padx=(30,0))

    Label(addRecipesWindow,text="Ingredients",font=("Helvetica 13")).grid(row=1,column=0,padx=(0,25))

    addRecipesIngredients = Text(addRecipesWindow,width=38,height=3)
    addRecipesIngredients.grid(row=1,column=1,columnspan=2,pady=(15,0))

    Label(addRecipesWindow,text="Instructions",font="Helvetica 13").grid(row=2,column=1,pady=(15,0))

    addRecipesInstructions = Text(addRecipesWindow,width=53)
    addRecipesInstructions.grid(row=3,columnspan=3,pady=(0,10))

    addRecipesSubmit = Button(addRecipesWindow, text="SUBMIT",command=submit,padx=5,font="bold")
    addRecipesSubmit.grid(row=4,column=1)


    

def deleteRecipes():
    pass

def searchRecipes():
    pass

def showRecipes():
    global recipesListFrame
    recipesListFrame = Frame(root,bd=5, relief=RAISED)
    recipesListFrame.pack(fill=BOTH)
    with open("recipes.csv", "r") as recipesCSV:
        csv_reader = csv.DictReader(recipesCSV)
    
        for line in csv_reader:
            recipesItemFrame = Frame(recipesListFrame)
            recipesItemFrame.pack(fill=X)

            recipeImage = Image.open(line["image"])
            recipeImage = recipeImage.resize((125,125),Image.Resampling.LANCZOS)
            recipeImage = ImageTk.PhotoImage(recipeImage)


            Label(recipesItemFrame,image=recipeImage).grid(row=0,column=0)
            Button(recipesItemFrame,text=line["name"],command=Toplevel,font=("Helvetica",15,"underline"),bd=0,).grid(row=0,column=1)
            Checkbutton(recipesItemFrame, onvalue=4).place(relx = 1,rely = .5,anchor=E)


recipesFrame = Frame(root,bd=5,relief=RAISED)
recipesFrame.pack(anchor="n",fill=X)

recipesTitle = Label(recipesFrame, text="RECIPES", font=("Helvetica", 25, "bold"))
recipesTitle.pack()

recipesSearchEntry = Entry(recipesFrame,width=25)
recipesSearchEntry.pack(side=LEFT, padx=5)

recipesSearchButton = Button(recipesFrame,text="Search",command=searchRecipes)
recipesSearchButton.pack(side=LEFT)

recipesCheckButton = Checkbutton(recipesFrame, text="Show Available Recipes Only")
recipesCheckButton.pack(side=LEFT,padx=20)

recipesAddButton = Button(recipesFrame, text="Add Recipe", command=addRecipes)
recipesAddButton.pack(padx=5, pady=5, side=RIGHT)

recipesDeleteButton = Button(recipesFrame,text="Delete Recipe", command=deleteRecipes)
recipesDeleteButton.pack(padx=5, pady=5,side=RIGHT)



showRecipes()



root.mainloop()