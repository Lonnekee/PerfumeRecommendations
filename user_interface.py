try:
    import Tkinter as tk
    import Tkinter.messagebox
except:
    import tkinter as tk
    import tkinter.messagebox
import io
import urllib.request
from PIL import Image, ImageTk
import os
from pathlib import Path
import pandas as pd
from functools import partial
import webbrowser
from pyglet import font

import engine.InferenceEngine as ie
from engine.question.QuestionType import QuestionType as qt

PATH = Path(__file__).parent
if not (PATH / "data/").resolve().exists():
    # The executable is running, not the source files.
    PATH = PATH.parent.parent

# Add fonts
fonts_path = (PATH / "fonts").resolve()
for f in fonts_path.glob("**/*.ttf"):
    font.add_file((fonts_path / f).resolve())


# Create the application's frame
class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry('900x600')
        self.title('Perfume Knowledge System')
        self.engine = ie.InferenceEngine()
        self._frame = None
        self.switch_frame(StartPage)
        self.first_name = tk.StringVar()
        self.outcome = tk.StringVar()
        self.widgets = []
        self.chosen_products = []
        # self.relevant_index = 0

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        # self.geometry = "750x700"
        master.title('Perfume Knowledge System')
        master['bg'] = '#FBF8EE'
        self['bg'] = '#FBF8EE'

        def switch_and_clear():
            start_button.destroy()
            master.switch_frame(NewPage)

        start_label = tk.Label(self,
                               text="Welcome to the Perfume Knowledge System!\n\n\n",
                               wraplength=700, font=('Alegreya Sans Regular', 18), fg='#8A5C3C', bg='#FBF8EE')
        start_label2 = tk.Label(self,
                               text="\n\n\nPerfume can be your most personal accessory, but how to find amongst the enormous offer of perfumes your ideal scented product? We have bundled the expertise of perfumers and scent experts to be able to determine your ideal fragrance. Discover now!",
                               wraplength=700, font=('Alegreya Sans Regular', 14), fg='#8A5C3C', bg='#FBF8EE')
        start_label.pack()

        im_path = (PATH / "data/Logo-PL-liggend.png").resolve()

        self.img = Image.open(im_path)
        img_width, img_height = self.img.size
        img_width = int(img_width / 4)
        img_height = int(img_height / 4)
        self.img = self.img.resize((img_width, img_height), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.img)
        canvas = tk.Canvas(self, height=img_height, width=img_width, bg='#FBF8EE')
        canvas.pack()

        canvas.create_image(img_width / 2 + 1, img_height / 2, image=self.img, anchor=tk.CENTER)

        start_label2.pack()
        start_button = tk.Button(text="Click here to start", font=('Alegreya Sans', '12', 'italic'), fg='#8A5C3C',
                                 bg="#FBF8EE", activebackground="#5a371e", activeforeground="#FBF8EE", width=750,
                                 command=switch_and_clear)
        start_button.pack(side=tk.BOTTOM, pady=50)


class NewPage(tk.Frame):
    given_answer = None
    question = None

    def __init__(self, master):
        super(NewPage, self).__init__()
        self.master = master
        self.buttons = []
        self.widgets = []
        self.count = 0
        self.value = []
        self.product_index = []

        # Recursive call: make new page for each question until you reach the last
        if master.engine.has_reached_goal():
            master.switch_frame(EndPage)
        else:
            # Initialise frame
            tk.Frame.__init__(self, master)
            # self.geometry = "900x500"
            self['bg'] = '#FBF8EE'

            if master.engine.get_question_direction() == 1:
                q = master.engine.get_next_question()
            else:
                q = master.engine.get_previous_question()
                self.master.engine.set_current_question(q)

            self.question = q

            # Display the question that this frame is about
            label = tk.Label(text="%s" % q.question, wraplength=600, font=('Alegreya Sans', 12), fg='#8A5C3C',
                             bg='#FBF8EE')
            label.pack(side=tk.TOP)
            self.widgets.append(label)

            # Add the appropriate buttons or fields for the answers
            if q.type == qt.SINGLE:  # radio buttons needed
                self.given_answer = tk.IntVar()
                if not q.id == 2:
                    for i, answer in enumerate(q.answers):
                        radios = tk.Radiobutton(self, text=answer, activebackground="#FBF8EE", background="#FBF8EE",
                                                activeforeground="black",
                                                foreground="black", selectcolor="#8A5C3C", width=50, indicatoron=0,
                                                offrelief=tk.FLAT, bd=3, pady=8, variable=self.given_answer, value=i)
                        radios.pack()
                else:
                    for i, answer in enumerate(q.answers):
                        radios = tk.Radiobutton(text=answer, activebackground="#FBF8EE", background="#FBF8EE",
                                                activeforeground="black",
                                                foreground="black", selectcolor="#8A5C3C", width=50, indicatoron=0,
                                                offrelief=tk.FLAT, bd=3, pady=8, variable=self.given_answer, value=i)
                        radios.pack()
                        self.widgets.append(radios)

            elif q.type == qt.MULTIPLE:  # selectable boxes or images needed (?)
                self.given_answer = len(q.answers) * [0]
                for i in range(len(q.answers)):
                    self.given_answer[i] = tk.IntVar()
                    c = tk.Checkbutton(self, text=q.answers[i], bg="#FBF8EE", fg='#5a371e', activebackground="#5a371e",
                                       activeforeground="#FBF8EE", selectcolor="#FBF8EE", width=50, indicatoron=1,
                                       pady=8, bd=3, variable=self.given_answer[i])
                    c.pack()

            elif q.type == qt.DISPLAY:
                print("Display, no buttons needed.")

            elif q.type == qt.DROPDOWN:  # a list is needed, where multiple items can be selected
                self.droplist = q.get_list()

                self.lbox = tk.Listbox(self, selectmode=tk.MULTIPLE, width=65, height=24, selectbackground="#8A5C3C",
                                       selectforeground="#FBF8EE")

                self.sorted_droplist = sorted(self.droplist)

                if self.master.chosen_products != []:
                    # Remove options the user can dislike, if they have previously indicated they like these options.
                    for item in self.master.chosen_products:
                        if item in self.droplist:
                            self.droplist.remove(item)
                    self.lbox.insert("end", *self.sorted_droplist)
                    self.master.chosen_products = []
                else:
                    self.lbox.insert("end", *self.sorted_droplist)

                if len(self.droplist) > 24:
                    # add scrollbar to listbox if needed
                    scrollbar = tk.Scrollbar(self)
                    scrollbar.grid(row=0, column=1, sticky=tk.NS)
                    self.lbox.config(yscrollcommand=scrollbar.set)
                    scrollbar.config(command=self.lbox.yview)

                self.lbox.grid(row=0, column=0)
                self.given_answer = tk.StringVar()
                self.given_answer.set(self.droplist[0])

                self.search_var = tk.StringVar()
                self.search_bar = tk.Entry(textvariable=self.search_var)
                self.search_bar.place(x=270, rely=0.835, relwidth=0.2, height=31)
                self.widgets.append(self.search_bar)

                def search_keyword():
                    selection = self.lbox.curselection()
                    self.add_selected(selection)
                    search_term = self.search_var.get()
                    self.lbox.delete(0, tk.END)
                    for item in self.droplist:
                        if search_term.lower() in item.lower():
                            self.lbox.insert(0, item)

                def clear_list():
                    selection = self.lbox.curselection()
                    self.add_selected(selection)
                    self.lbox.delete(0, tk.END)
                    self.search_bar.delete(0, tk.END)
                    self.lbox.insert("end", *self.droplist)

                self.add_selected(self.lbox.curselection())
                search = tk.Button(text="Search", width=10, fg='#8A5C3C', bg="#FBF8EE", activebackground="#5a371e",
                                   activeforeground="#FBF8EE", command=search_keyword)
                clear = tk.Button(text="Clear", width=10, fg='#8A5C3C', bg="#FBF8EE", activebackground="#5a371e",
                                  activeforeground="#FBF8EE", command=clear_list)
                search.place(x=450, rely=0.835, relwidth=0.1, height=31)
                clear.place(x=540, rely=0.835, relwidth=0.1, height=31)
                self.buttons.append(search)
                self.buttons.append(clear)

            elif q.type == qt.BUDGET:
                minPrice, maxPrice = master.engine.get_price_range()
                self.given_answer = tk.DoubleVar()
                scale_entry = tk.Scale(self, variable=self.given_answer, label='Maximum budget in euros:',
                                       from_=minPrice, to=maxPrice, tickinterval=(maxPrice - minPrice),
                                       orient=tk.HORIZONTAL, length=200, fg='#8A5C3C', bg="#FBF8EE",
                                       activebackground="#FBF8EE", troughcolor="#5a371e")
                scale_entry.set(int((maxPrice - minPrice) / 2 + minPrice))
                scale_entry.pack()

            elif q.type == qt.NAME:
                self.given_answer = tk.StringVar()
                name_entry = tk.Entry(master, textvariable=self.given_answer)
                name_entry.pack()
                self.widgets.append(name_entry)

            # Create button that can stop the program prematurely
            stop_text = "Show my recommendations"
            stop = tk.Button(text=stop_text, font=('Alegrya sans', '12', 'italic'), fg='#8A5C3C', bg="#FBF8EE",
                             activebackground="#5a371e", activeforeground="#FBF8EE",
                             command=self._premature_recommendations)
            stop.pack(side=tk.BOTTOM)  # , anchor=tk.NE)

            # Create submit button that can send the answer to the inference engine
            next_text = ["Next", "\u1405"]
            submit = tk.Button(text=next_text, font=('Alegrya sans', '12', 'italic'), fg='#8A5C3C', bg="#FBF8EE",
                               activebackground="#5a371e", activeforeground="#FBF8EE", width=15, command=self._send_result)
            submit.pack(side=tk.RIGHT)

            # Create button that goes to previous page and reverts answers given, only appears after the first answered question
            if len(self.master.engine.get_traversed_path()) > 0:
                previous_text = ["\u140A", "Previous"]
                previous = tk.Button(text=previous_text, font=('Alegrya sans', '12', 'italic'), fg='#8A5C3C',
                                     bg="#FBF8EE", activebackground="#5a371e", activeforeground="#FBF8EE", width=15,
                                     command=self._revert_answers)
                previous.pack(side=tk.LEFT)
                self.buttons.append(previous)

            self.buttons.append(submit)
            self.buttons.append(stop)

    # show recommendations before the end of the program
    def _premature_recommendations(self):
        ans = tk.messagebox.askquestion('Stop recommending',
                                        'You have not answered all the questions yet. Are you sure you want to see your recommendations already?')

        if ans == 'yes':
            # show current best recommendations
            self.master.switch_frame(EndPage)
            for button in self.buttons:
                button.destroy()
                self.buttons = []
            for widget in self.widgets:
                widget.destroy()
                self.widgets = []
        else:
            print("Continuing with questions")

    # Changes the frame to the previous question and reverts answers
    def _revert_answers(self):
        self.master.engine.set_question_direction(0)

        for button in self.buttons:
            button.destroy()
            self.buttons = []

        for widget in self.widgets:
            widget.destroy()
            self.widgets = []

        # undo the voting
        traversed = self.master.engine.get_traversed_path()
        print(traversed)
        if traversed:
            prev_id = traversed[-1]
            print(prev_id)
            self.master.engine.reverseAnswer(prev_id)

        self.master.switch_frame(NewPage)

    # Continuously add current selection of dropdown in list
    def add_selected(self, selection):
        if len(selection) > 0:
            for item in range(len(selection)):
                self.value.append(self.lbox.get(selection[item]))
        for product in self.value:
            if product in self.droplist:
                self.product_index.append(self.droplist.index(product))
        print("selection:"'%s' % self.value)
        self.master.chosen_products = self.value
        self.given_answer = list(set(self.product_index))
        print("indexes:", self.given_answer)

    # Sends result to inference engine and switches frame
    def _send_result(self):
        value = None

        if self.question.type == qt.SINGLE:
            value = int(self.given_answer.get())

        elif self.question.type == qt.MULTIPLE:
            value = [int(a.get()) for a in self.given_answer]

        elif self.question.type == qt.DROPDOWN:
            self.add_selected(self.lbox.curselection())
            value = [a for a in self.given_answer]

        elif self.question.type == qt.DISPLAY:
            print("Display UI: no choice needed")

        elif self.question.type == qt.BUDGET:
            value = float(self.given_answer.get())

        elif self.question.type == qt.NAME:
            first_name = self.given_answer.get()
            if first_name != '':
                self.master.first_name.set(first_name)
                self.master.title('Perfume Recommendations for %s' % first_name)

        else:
            print("Question type's answer can not be processed yet.")

        self.master.engine.set_answer(value)
        if self.master.engine.has_reached_goal():
            self.master.switch_frame(EndPage)
        else:
            self.master.engine.set_question_direction(1)
            self.master.switch_frame(NewPage)
        for button in self.buttons:
            button.destroy()
            self.buttons = []
        for widget in self.widgets:
            widget.destroy()
            self.widgets = []


class EndPage(tk.Frame):
    images = []

    def save_results(self, recommendations):
        desktop = os.path.expanduser("~/Desktop/")
        f = open(desktop + "Perfume_Recommendations.txt", "w")

        for index in range(len(recommendations.index)):
            row = recommendations.iloc[index]
            f.write("Recommendation #" + str(index + 1) + "\n")
            f.write(row['Title'] + " by " + row['Vendor'] + "\n")
            f.write(row['Type'] + "\n\n")
            f.write("Relevant questions:" + row['rel_q'] + "\n")

        f.close()

    def __init__(self, master):
        super(EndPage, self).__init__()
        tk.Frame.__init__(self, master)
        self.master.relevant_questions = []
        self.master.relevant_answers = []
        self.master.relevant_index = 0
        # self.master.image_buttons = []
        self.master.button_identities = []
        self.master.extra_information = []
        self.master.vendors = []
        self.master.titles = []
        self.master.types = []
        self.master.prices = []
        self.master.handles = []
        self['bg'] = "#FBF8EE"
        tk.Label(self, text="Hi %s, here are your scent recommendations" % self.master.first_name.get(),
                 font=('Alegreya Sans', 18, "bold"), fg='#8A5C3C', bg='#FBF8EE') \
            .grid(row=0, columnspan=3, pady=5)

        recommendations = master.engine.get_recommendations()  # Pandas dataframe

        pd.pandas.set_option('display.max_columns', None)
        pd.pandas.set_option('display.max_rows', None)
        pd.set_option('display.max_colwidth', None)
        print(recommendations.facts)
        print(recommendations.rel_q)

        all = master.engine.get_all()
        # print(all)

        start_row = 1
        no_items = 5
        no_columns = 3
        im_width = 100
        wraplength = 200

        # print("len:",len(recommendations.index))
        for index in range(len(recommendations.index)):
            # print(index)
            row = recommendations.iloc[index]
            column = index % no_columns

            print("Facts:", index, row['rel_q'])
            self.master.relevant_questions.append(row['rel_q'])
            self.master.relevant_answers.append(row['facts'])

            # self.master.relevant_index.append(index)

            def switch_to_end(button_id):
                # print("index:", self.master.relevant_index)
                self.master.relevant_index = index
                bname = list(str(self.master.button_identities[button_id]))
                bname = bname[len(bname) - 1]
                if bname == "n":
                    self.master.relevant_index = 0
                else:
                    self.master.relevant_index = int(bname) - 1
                print("bname:", bname)
                self.master.switch_frame(ProductPage)

            # Image
            url = row['Image']
            raw_data = urllib.request.urlopen(url).read()
            im = Image.open(io.BytesIO(raw_data))

            width, height = im.size
            factor = width / im_width
            im = im.resize((round(height / factor), round(im_width)))

            image = ImageTk.PhotoImage(im)

            # Create an image button that takes you to the product page
            image_button = tk.Button(self, image=image,command=partial(switch_to_end, index))
            self.master.button_identities.append(image_button)
            image_button.grid(row=start_row + 0, column=column, pady=10)
            image_button_ttp = CreateToolTip(image_button, text="Click to see why this product was recommended...")

            # self.image_buttons.append(image_button)
            self.images.append(image)  # Append to list of images to keep the reference. Otherwise, it might not show.

            # Vendor
            vendor = tk.Label(self,
                              fg='#323232',
                              bg='#FBF8EE',
                              text=row['Vendor'].upper(),
                              font=("Courier", 12),
                              wraplength=wraplength)\
                .grid(row=start_row + 1, column=column)
            self.master.vendors.append(row['Vendor'])

            # Name of perfume
            title = tk.Label(self,
                             fg='#323232',
                             bg='#FBF8EE',
                             text=row['Title'],
                             font=("Marcellus", 14),
                             wraplength=wraplength) \
                .grid(row=start_row + 2, column=column)
            self.master.titles.append(row['Title'])

            # Type of perfume (eau de parfum, eau de toilette, etc.)
            perfume_type = tk.Label(self, fg='#8A5C3C', bg='#FBF8EE', text=row['Type'].upper(),
                                    font=("Courier", 12)).grid(row=start_row + 3, column=column)
            self.master.types.append(row['Type'])

            # Price
            price = "From €{:.2f}".format(row['Price'])
            price = tk.Label(self, fg='#8A5C3C', bg='#FBF8EE', text=price, font=("Courier", 12)) \
                .grid(row=start_row + 4, column=column)
            self.master.prices.append(price)

            # Save tags for display in product page
            self.master.extra_information.append(row['Tag'])

            # Save handle for url in product page
            self.master.handles.append(row['Handle'])

            if column == no_columns - 1 or index == len(recommendations) - 1:
                self.master.grid_rowconfigure(start_row + no_items, minsize=100)
                start_row += no_items + 1

        tk.Button(self, text="Modify price range", fg='#8A5C3C', bg="#FBF8EE",activebackground="#5a371e", activeforeground="#FBF8EE",
                  command=self._modify_price) \
            .grid(row=start_row, columnspan=3)

        tk.Button(self, text="Save the results to my Desktop", fg='#8A5C3C', bg="#FBF8EE", activebackground="#5a371e",
                  activeforeground="#FBF8EE",
                  command=self.save_results(recommendations)) \
            .grid(row=start_row + 1, columnspan=3)

        tk.Button(self, text="Go back to start page", fg='#8A5C3C', bg="#FBF8EE", activebackground="#5a371e",
                  activeforeground="#FBF8EE", command=self._reset) \
            .grid(row=start_row + 2, columnspan=3)

        # for x in range(len(self.master.relevant_questions)):
        #    print("questions:",self.master.relevant_questions[x])
        # print("buttons:", self.master.button_identities)

    def _reset(self):
        self.master.first_name.set('')
        self.master.engine.reset()
        self.master.switch_frame(StartPage)

    def _modify_price(self):
        #undo the voting
        traversed = self.master.engine.get_traversed_path()
        #self.master.engine.add_budget_to_path()
        print("traversed path:", traversed)

        if traversed.count(35) > 0:
            print("CONTAINS BUDGET QUESTION")
            prev_id = traversed[-1]
            print("prev_id:",prev_id)
            self.master.engine.get_latest_path_value()
            self.master.engine.reverseAnswer(prev_id)
        else:
            print("add")
            self.master.engine.add_budget_to_path()
        #print("print facts:",self.master.facts)

        # Go back to the previous page
        #self.master.engine.get_latest_path_value()
        self.master.engine.set_question_direction(0)
        self.master.switch_frame(NewPage)


# Frame class containing a single recommended product with description/motivation for it
class ProductPage(tk.Frame):

    def __init__(self, master):
        super(ProductPage, self).__init__()
        def switch_back_to_recs():
            back_to_recs_button.destroy()
            PL_button.destroy()
            self.master.switch_frame(EndPage)

        tk.Frame.__init__(self, master)
        self['bg'] = "#FBF8EE"

        # Remove duplicate motivation lines
        display_text = self.master.relevant_questions[self.master.relevant_index]
        display_text = set(display_text.split("\n"))
        display_text.discard('')
        display_text = sorted(list(display_text))
        display_text = '\n'.join(display_text)
        print("split:", display_text)

        # Display the motivation for recommending this product
        tk.Label(self,
                 fg='#8A5C3C',
                 bg='#FBF8EE',
                 font=('Alegreya Sans', 18, "bold"),
                 wraplength=800,
                 pady=10,
                 text="This scent is recommended to you because of the following questions:").pack()
        # tk.Label(self, fg='#8A5C3C', bg='#FBF8EE',text=self.master.relevant_questions[self.master.relevant_index], wraplength=600).pack()
        tk.Label(self, fg='#8A5C3C', bg='#FBF8EE', text=display_text, wraplength=600).pack()

        # TODO: Display a more detailed description of the product
        tk.Label(self, fg='#8A5C3C', bg='#FBF8EE', font=('Alegreya Sans', 14, "bold"), wraplength=800,
                 text="More information about this product:").pack()
        tk.Label(self, fg='#8A5C3C', bg='#FBF8EE', text=self.master.vendors[self.master.relevant_index],
                 wraplength=600).pack()
        tk.Label(self, fg='#8A5C3C', bg='#FBF8EE', text=self.master.titles[self.master.relevant_index],
                 wraplength=600).pack()
        tk.Label(self, fg='#8A5C3C', bg='#FBF8EE', text=self.master.types[self.master.relevant_index],
                 wraplength=600).pack()
        tk.Label(self, fg='#8A5C3C', bg='#FBF8EE', text=self.master.prices[self.master.relevant_index],
                 wraplength=600).pack()
        tk.Label(self, fg='#8A5C3C', bg='#FBF8EE', text=self.master.extra_information[self.master.relevant_index],
                 wraplength=600).pack()

        # Create button that takes the user back to the overview of recommended products
        back_to_recs_button = tk.Button(text="Back to overview", fg='#8A5C3C', bg="#FBF8EE", activebackground="#5a371e",
                                        activeforeground="#FBF8EE",
                                        command=switch_back_to_recs)
        back_to_recs_button.pack(side=tk.BOTTOM, pady=50)

        # Create button that takes the user to the product page on the PL website
        PL_link = "https://www.perfumelounge.nl/products/" + str(self.master.handles[self.master.relevant_index])

        def callback(url):
            webbrowser.open_new(url)

        PL_button = tk.Button(text="Read more on the Perfume Lounge website", fg='#8A5C3C', bg="#FBF8EE",
                              activebackground="#5a371e", activeforeground="#FBF8EE",
                              command=lambda: callback(PL_link))
        PL_button.pack(side=tk.BOTTOM)


# This class creates a tooltip: a box of text that appears when hovering over a widget. 
class CreateToolTip(object):
    def __init__(self, widget, text='widget info'):
        self.waittime = 200  # miliseconds
        self.wraplength = 180  # pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 100
        y += self.widget.winfo_rooty() + 50
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                         background="#ffffff", relief='solid', borderwidth=1,
                         wraplength=self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()


def run():
    app = SampleApp()
    app.mainloop()
