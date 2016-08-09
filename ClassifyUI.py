import tkinter
from tkinter import filedialog

from ClassifyGuest import ClassifyGuest

class app_tk(tkinter.Tk):
    def __init__(self,parent):
        tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()



        button_select_d = tkinter.Button(self,text="Select Daily Files",
                                command=self.askOpenFiles)
        button_select_d.grid(column=0,row=0)

        var = tkinter.StringVar()
        label = tkinter.Label(self, textvariable = var)
        var.set("Number of results: ")
        label.grid(column = 0, row=1)

        var_spin_default = tkinter.StringVar()

        w = tkinter.Spinbox(self,from_=1, to = 1000, 
                            textvariable=var_spin_default)
        var_spin_default.set("50")
        w.grid(column = 1, row = 1)
        self.num_of_results = w

        button_select_run = tkinter.Button(self,text="Run",
                                command=self.run)
        button_select_run.grid(column=0,row=2)




        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False)
        self.update()
        #self.geometry(self.geometry())       


        
    #open multiple files
    def askOpenFiles(self):
        filenames = filedialog.askopenfilenames()
        self.list_daily = list(filenames)


    def run(self):
        if len(self.list_daily) == 0:
            print("You haven't select daily files!")
            return None
        cg = ClassifyGuest(self.list_daily,int(self.num_of_results.get()))
        cg.train()
        cg.predict()



if __name__ == "__main__":
    app = app_tk(None)
    app.title('ClassifyGuest')
    app.geometry("300x200")
    app.mainloop()
