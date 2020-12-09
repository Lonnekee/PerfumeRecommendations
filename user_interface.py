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
            master.switch_frame(NewPage)

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
            tk.Label(self, text="%s" % q.question,wraplengt=600, font=('Helvetica', 12)).pack(side="top", fill="x", pady=5)

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

            elif q.type == qt.DROPDOWN:  # a dropdown list is needed, where multiple items can be selected
                perfumes = q.get_perfumes()  # list of strings, describing perfume name and brand
                self.given_answer = tk.StringVar()
                self.given_answer.set(perfumes[0])
                dropdown_menu = tk.OptionMenu(self, self.given_answer, *perfumes)
                dropdown_menu.pack()

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
            value = [1, 2]  # TODO! give list of indices of (multiple) selected answers
        elif self.question.type == qt.CHOICE_DISPLAY:
            print("Display UI: no choice needed")
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
        tk.Label(self, text="Your recommended scent is %s" % ((master.outcome).get()),
                 font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Go back to start page", command=lambda: master.switch_frame(StartPage)).pack(
            side="bottom")


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
