from engine.question.Question import Question

try:
    import Tkinter as tk
except:
    import tkinter as tk
import io
import urllib.request
from PIL import Image, ImageTk
import os

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
        master['bg'] = '#FBF8EE'
        self['bg'] = '#FBF8EE'
        tk.Label(self,
                 text="Welcome to the perfume knowledge system! After you have answered the questions, the system will determine the ideal scented product for your personal use.",
                 wraplength=750, font=('Alegreya sans', 18), fg='#8A5C3C',bg='#FBF8EE').pack(side="top", fill="x", pady=5)
        start_button = tk.Button(self, text="CLICK HERE TO START", font=('Alegreya sans', '12', 'italic'), width=100, fg="#FBF8EE", bg='#8A5C3C',command=lambda: master.switch_frame(NewPage))
        #start_button.place(x=325, y=250)
        start_button.pack(side=tk.BOTTOM, pady=100)


class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self['bg'] = '#FBF8EE'
        tk.Label(self, text="What is your name?", wraplength=750, font=('Alegreya sans', 18),fg='#8A5C3C',bg='#FBF8EE').pack(side="top",
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

        #tk.Button(self, text="NEXT", font=('Alegreya sans', '12', 'italic'),fg="#FBF8EE", bg='#8A5C3C', command=get_input).pack(side=tk.BOTTOM, fill="x", pady=50)

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
            self['bg'] = '#FBF8EE'

            q = master.engine.get_next_question()
            self.question = q

            # Display the question that this frame is about
            tk.Label(self, text="%s" % q.question, wraplengt=600, font=('Alegreya sans', 12),fg='#8A5C3C',bg='#FBF8EE').pack(side="top", fill="x",
                                                                                               pady=5)

            # Add the appropriate buttons or fields for the answers
            if q.type == qt.SINGLE:  # radio buttons needed
                self.given_answer = tk.IntVar()
                for i, answer in enumerate(q.answers):
                    radios = tk.Radiobutton(self, text=answer, fg="#FBF8EE", bg='#8A5C3C', variable=self.given_answer, value=i)
                    radios.pack()

            elif q.type == qt.MULTIPLE:  # selectable boxes or images needed (?)
                self.given_answer = len(q.answers) * [0]
                for i in range(len(q.answers)):
                    self.given_answer[i] = tk.IntVar()
                    c = tk.Checkbutton(self, text=q.answers[i], fg="#FBF8EE", bg='#8A5C3C', variable=self.given_answer[i])
                    c.pack()

            elif q.type == qt.DISPLAY:
                print("Display, no buttons needed.")

            elif q.type == qt.DROPDOWN:  # a list is needed, where multiple items can be selected
                # perfumes = q.get_perfumes()  list of strings, describing perfume name and brand
                print(q.labels)
                if ("takePerfume" in q.labels):
                    self.droplist = q.get_perfumes()  # lists of strings, describing perfume name and brand and their tags
                elif ("takeFamily" in q.labels):
                    self.droplist = q.get_families()  # lists of strings, describing olfactory families and their tags
                elif ("takeIngredient" in q.labels):
                    self.droplist = q.get_ingredients()  # lists of strings, describing ingredients and their tags
                else:
                    self.droplist = None
                    print("Appropriate dropdown not found.")

                # add scrollbar to listbox
                scrollbar = tk.Scrollbar(self)
                scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

                self.lbox = tk.Listbox(self, selectmode=tk.MULTIPLE, width=75, height=10)
                self.lbox.insert("end", *self.droplist)
                self.lbox.config(yscrollcommand = scrollbar.set)
                scrollbar.config(command = self.lbox.yview)

                self.lbox.pack()
                self.given_answer = tk.StringVar()
                self.given_answer.set(self.droplist[0])


                self.search_var = tk.StringVar()
                self.search_bar = tk.Entry(self, textvariable=self.search_var)
                self.search_bar.pack()

                self.value = []
                self.product_index = []

                def search_keyword():
                    selection=self.lbox.curselection()
                    self.add_selected(selection)
                    search_term = self.search_var.get()
                    self.lbox.delete(0, tk.END)
                    for item in self.droplist:
                        if search_term.lower() in item.lower():
                            self.lbox.insert(0, item)

                def clear_list():
                    selection=self.lbox.curselection()
                    self.add_selected(selection)
                    self.lbox.delete(0, tk.END)
                    self.search_bar.delete(0, tk.END)
                    self.lbox.insert("end", *self.droplist)

                self.add_selected(self.lbox.curselection())
                search = tk.Button(self, text="Search", width=10, fg="#FBF8EE", bg='#8A5C3C', command=search_keyword)
                clear = tk.Button(self, text="Clear", width=10,fg="#FBF8EE", bg='#8A5C3C', command=clear_list)
                search.pack()
                clear.pack()

            elif q.type == qt.BUDGET:
                minPrice, maxPrice = master.engine.get_price_range()
                self.given_answer = tk.DoubleVar()
                scale_entry = tk.Scale(self, variable=self.given_answer, label='Maximum budget in euros:', from_=minPrice, to=maxPrice, tickinterval=(maxPrice-minPrice), orient=tk.HORIZONTAL,length=200)
                scale_entry.set(int((maxPrice-minPrice)/2+minPrice))
                scale_entry.pack()
            elif q.type == qt.NAME:
                self.given_answer = tk.StringVar()
                name_entry = tk.Entry(self, textvariable=self.given_answer)
                name_entry.pack()

            # Create submit button that can send the answer to the inference engine
            submit = tk.Button(self, text="NEXT QUESTION", font=('Alegrya sans', '12', 'italic'),width=600,fg="#FBF8EE", bg='#8A5C3C', command=self._send_result)
            submit.place(x=325, y=250)
            submit.pack(side=tk.BOTTOM, fill="x", pady=50)

    # Continuously add current selection of dropdown in list
    def add_selected(self, selection):
        if len(selection)>0:
            for item in range(len(selection)):
                self.value.append(self.lbox.get(selection[item]))
        for product in self.value:
            if product in self.droplist:
                self.product_index.append(self.droplist.index(product))
        print("selection:"'%s' % self.value)
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
    images = []

    def save_results(self, recommendations):
        desktop = os.path.expanduser("~/Desktop/")
        f = open(desktop + "Perfume_Recommendations.txt","w") 
        
        for index in range(len(recommendations.index)):
            row = recommendations.iloc[index]
            f.write("Recommendation #" + str(index+1) + "\n")
            f.write(row['Title'] + " by " + row['Vendor'] + "\n")
            f.write(row['Type'] + "\n\n")
        
        f.close()


    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self['bg']="#FBF8EE"
        tk.Label(self, text="Hi %s, here are your scent recommendations" % master.first_name.get(),
                 font=('Alegreya sans', 18, "bold"),fg='#8A5C3C',bg='#FBF8EE')\
            .grid(row=0, columnspan=3, pady=5)

        recommendations = master.engine.get_recommendations()  # Pandas dataframe

        start_row = 1
        no_items = 5
        no_columns = 3
        im_width = 100

        for index in range(len(recommendations.index)):
            row = recommendations.iloc[index]
            column = index % no_columns

            # Image
            url = row['Image']
            raw_data = urllib.request.urlopen(url).read()
            im = Image.open(io.BytesIO(raw_data))

            width, height = im.size
            factor = width / im_width
            im = im.resize((round(height / factor), round(im_width)))

            image = ImageTk.PhotoImage(im)
            tk.Label(self, image=image).grid(row=start_row + 0, column=column)
            self.images.append(image)  # Append to list of images to keep the reference. Otherwise, it might not show.

            # Vendor
            tk.Label(self, fg='#8A5C3C', bg='#FBF8EE', text=row['Vendor']).grid(row=start_row + 1, column=column)

            # Name of perfume
            tk.Label(self, fg='#8A5C3C', bg='#FBF8EE', text=row['Title']).grid(row=start_row + 2, column=column)

            # Type of perfume (eau de parfum, eau de toilette, etc.)
            tk.Label(self, fg='#8A5C3C', bg='#FBF8EE', text=row['Type']).grid(row=start_row + 3, column=column)

            # Price
            price = "€" + str(row['Price'])
            tk.Label(self, fg='#8A5C3C', bg='#FBF8EE', text=price).grid(row=start_row + 4, column=column)

            if column == no_columns - 1 or index == len(recommendations)-1:
                start_row += no_items

        tk.Button(self, text="Save the results to my Desktop", fg="#FBF8EE", bg='#8A5C3C', command=self.save_results(recommendations))\
            .grid(row=start_row, columnspan=3)

        tk.Button(self, text="Go back to start page", fg="#FBF8EE", bg='#8A5C3C', command=self._reset)\
            .grid(row=start_row+2, columnspan=3)


    def _reset(self):
        self.master.first_name.set('')
        self.master.engine.reset()
        self.master.switch_frame(StartPage)


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
