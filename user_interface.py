from engine.question.Question import Question

try:
    import Tkinter as tk
except:
    import tkinter as tk

import engine.InferenceEngine as ie
from engine.question.QuestionType import QuestionType as qt


class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry('750x500')
        self.title('Perfume Knowledge System')
        # self.title = tk.StringVar()
        self.engine = ie.InferenceEngine()
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
        master.title('Perfume Knowledge System')
        tk.Label(self,
                 text="Welcome to the perfume knowledge system! After you have answered the questions, the system will determine the ideal scented product for your personal use.",
                 wraplength=750, font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Click here to start", command=lambda: master.switch_frame(NewPage)).pack()


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
            if first_name != '':
                (master.first_name).set(first_name)
                master.title('Perfume Recommendations for %s' % first_name)
            self.master.switch_frame(NewPage)

        tk.Button(self, text="Next", command=get_input).pack()


class NewPage(tk.Frame):
    given_answer = None
    question = None

    def __init__(self, master):
        self.master = master

        # Recursive call: make new page for each question until you reach the last
        if master.engine.has_reached_goal():
            master.switch_frame(EndPage)
        else:
            # Initialise frame
            tk.Frame.__init__(self, master)

            q = master.engine.get_next_question()
            self.question = q

            # Display the question that this frame is about
            tk.Label(self, text="%s" % q.question, wraplengt=600, font=('Helvetica', 12)).pack(side="top", fill="x",
                                                                                               pady=5)

            # Add the appropriate buttons or fields for the answers
            if q.type == qt.CHOICE_SINGLE_SELECT:  # radio buttons needed
                self.given_answer = tk.IntVar()
                for i, answer in enumerate(q.answers):
                    radios = tk.Radiobutton(self, text=answer, variable=self.given_answer, value=i)
                    radios.pack()

            elif q.type == qt.CHOICE_MULTIPLE_SELECT:  # selectable boxes or images needed (?)
                self.given_answer = len(q.answers) * [0]
                for i in range(len(q.answers)):
                    self.given_answer[i] = tk.IntVar()
                    c = tk.Checkbutton(self, text=q.answers[i], variable=self.given_answer[i])
                    c.pack()

            elif q.type == qt.CHOICE_DISPLAY:
                print("Display, no buttons needed.")

            elif q.type == qt.DROPDOWN:  # a list is needed, where multiple items can be selected
                # perfumes = q.get_perfumes()  list of strings, describing perfume name and brand
                print(q.labels)
                if ("takePerfume" in q.labels):
                    droplist, tags = q.get_perfumes()  # lists of strings, describing perfume name and brand and their tags
                elif ("takeFamily" in q.labels):
                    droplist, tags = q.get_families()  # lists of strings, describing olfactory families and their tags
                elif ("takeIngredient" in q.labels):
                    droplist, tags = q.get_ingredients()  # lists of strings, describing ingredients and their tags
                else:
                    droplist, tags = None, None
                    print("Appropriate dropdown not found.")

                # add scrollbar to listbox
                scrollbar = tk.Scrollbar(self)
                scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

                self.lbox = tk.Listbox(self, selectmode=tk.MULTIPLE, width=75, height=10)
<<<<<<< HEAD
                self.lbox.config(yscrollcommand = scrollbar.set)
                scrollbar.config(command = self.lbox.yview)

=======
                self.lbox.config(yscrollcommand=scrollbar.set)
                scrollbar.config(command=self.lbox.yview)
>>>>>>> 69afa07a56b8048f9d3c97b7ce8cfa99f40f49e0
                self.lbox.pack()
                self.given_answer = tk.StringVar()
                self.given_answer.set(droplist[0])

                # TODO: (autocomplete) search bar
                self.search_var = tk.StringVar()
<<<<<<< HEAD
                self.search_bar = tk.Entry(self, textvariable=self.search_var)
                self.search_bar.pack()

=======
                search_bar = tk.Entry(self, textvariable=self.search_var)
                search_bar.pack()

                # self.extrabox = tk.Listbox(self, selectmode=tk.MULTIPLE, width=35, height=10)
>>>>>>> 69afa07a56b8048f9d3c97b7ce8cfa99f40f49e0
                def search_keyword():
                    search_term = self.search_var.get()
                    for item in droplist:
                        if search_term.lower() in item.lower():
                            self.lbox.insert(0, item)

                def clear_list():
                    self.lbox.delete(0, tk.END)
                    self.search_bar.delete(0, tk.END)
                    self.lbox.pack()

                search = tk.Button(self, text="Search", width=10, command=search_keyword)
                clear = tk.Button(self, text="Clear", width=10, command=clear_list)
                search.pack()
                clear.pack()
                self.lbox.delete(0, tk.END)
                # for item in droplist:
                #    if search_term.lower() in item.lower():
                #        self.lbox.insert(tk.END, item)

            elif q.type == qt.NUMBER:
                self.given_answer = tk.DoubleVar()
                number_entry = tk.Entry(self, textvariable=self.given_answer)
                number_entry.pack()
            elif q.type == qt.STRING:
                self.given_answer = tk.StringVar()
                name_entry = tk.Entry(self, textvariable=self.given_answer)
                name_entry.pack()

            # Create submit button that can send the answer to the inference engine
            submit = tk.Button(self, text="Next question", width=10, command=self._send_result)
            submit.pack()

    # Sends result to inference engine and switches frame
    def _send_result(self):
        value = None
        if self.question.type == qt.CHOICE_SINGLE_SELECT:
            value = int(self.given_answer.get())
        elif self.question.type == qt.CHOICE_MULTIPLE_SELECT:
            value = [int(a.get()) for a in self.given_answer]
        elif self.question.type == qt.DROPDOWN:
            value = [int(index) for index in list(self.lbox.curselection())]
        elif self.question.type == qt.CHOICE_DISPLAY:
            print("Display UI: no choice needed")
        elif self.question.type == qt.NUMBER:
            value = float(self.given_answer.get())
        elif self.question.type == qt.STRING:
            first_name = self.given_answer.get()
            if first_name != '':
                (self.master.first_name).set(first_name)
                self.master.title('Perfume Recommendations for %s' % first_name)
        else:
            print("Question type's answer can not be processed yet.")

        self.master.engine.set_answer(value)
        if self.master.engine.has_reached_goal():
            self.master.switch_frame(EndPage)
        else:
            self.master.switch_frame(NewPage)


class EndPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Hi %s, here are your scent recommendations" % master.first_name.get(),
                 font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Go back to start page", command=self._reset).pack(side="bottom")

        recommendations = master.engine.get_recommendations()  # Pandas dataframe

        for index in range(len(recommendations.index)):
            text = "'" + recommendations['Title'].iloc[index] + "' by " + recommendations['Vendor'].iloc[index]
            tk.Label(self, text=text).pack()

    def _reset(self):
        self.master.first_name.set('')
        self.master.engine.reset()
        self.master.switch_frame(StartPage)


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
