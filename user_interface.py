try:
    import Tkinter as tk
except:
    import tkinter as tk


class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry('750x500')
        self.title('Perfume Knowledge System')
        self._frame = None
        self.switch_frame(StartPage)
        self.first_name = tk.StringVar()
        self.outcome = tk.StringVar()

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self,
                 text="Welcome to the perfume knowledge system! After you have answered the questions, the system will determine the ideal scented product for your personal use.",
                 wraplength=750, font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Click here to start", command=lambda: master.switch_frame(PageOne)).pack()


class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="What is your name?", wraplength=750, font=('Helvetica', 18, "bold")).pack(side="top",
                                                                                                       fill="x", pady=5)
        tk.Label(self, text="Name")
        name_string = tk.StringVar()
        name_entry = tk.Entry(self, textvariable=name_string)
        name_entry.pack()

        def get_input():
            first_name = name_string.get()
            (master.first_name).set(first_name)
            master.switch_frame(PageTwo)

        tk.Button(self, text="Next", command=get_input).pack()


class PageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Welcome %s" % ((master.first_name).get()), font=('Helvetica', 18, "bold")).pack(side="top",
                                                                                                             fill="x",
                                                                                                             pady=5)
        tk.Label(self, text="Do you like the smell of roses?", font=('Helvetica', 12)).pack(side="top", fill="x",
                                                                                            pady=5)

        def yesButton():
            (master.outcome).set("Eau de Rose")
            master.switch_frame(EndPage)

        def noButton():
            (master.outcome).set("Not Rose")
            master.switch_frame(EndPage)

        v = tk.IntVar()
        tk.Radiobutton(self, text="Yes", variable=v, value=1, indicatoron=0, command=yesButton).pack()
        tk.Radiobutton(self, text="No", variable=v, value=2, indicatoron=0, command=noButton).pack()


class EndPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Your recommended scent is %s" % ((master.outcome).get()),
                 font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Go back to start page", command=lambda: master.switch_frame(StartPage)).pack(
            side="bottom")


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
