# german category selection
de_label_category = tkinter.Label(window, text="Select a german category...:", fg="red")

de_category_selection = tkinter.Listbox(window, fg="red", exportselection=0)


def de_category_listbox_changed(*args):
    if de_custom_category.get() != "":
        de_entry_custom_category.config(fg="green")
        de_label_custom_category.config(fg="green")
        de_category_selection.config(fg="red")
        de_label_category.config(fg="red")
    elif not de_category_selection.curselection():
        de_entry_custom_category.config(fg="red")
        de_label_custom_category.config(fg="red")
        de_category_selection.config(fg="red")
        de_label_category.config(fg="red")
    else:
        de_entry_custom_category.config(fg="red")
        de_label_custom_category.config(fg="red")
        de_category_selection.config(fg="green")
        de_label_category.config(fg="green")


de_category_selection.bind('<<ListboxSelect>>', de_category_listbox_changed)
# gets data from sql database
de_all_categories = []
cur = conn.cursor()
sql_query = """
SELECT de_category FROM images
GROUP BY de_category;
"""
cur.execute(sql_query)
de_category = cur.fetchone()
while de_category != None:
    de_category = "".join(de_category)
    de_all_categories.append(de_category)
    # adds the category to the selectionlist
    de_category_selection.insert(END, de_category)
    de_category = cur.fetchone()
# lets user add own option
de_label_custom_category = tkinter.Label(
    window, text="...or add a new one:", fg="red")
de_custom_category = StringVar()
de_custom_category.set("")


def de_changed_custom_category(*args):
    if de_custom_category.get() != "":
        de_entry_custom_category.config(fg="green")
        de_label_custom_category.config(fg="green")
        de_category_selection.config(fg="red")
        de_label_category.config(fg="red")
    elif not de_category_selection.curselection():
        de_entry_custom_category.config(fg="red")
        de_label_custom_category.config(fg="red")
        de_category_selection.config(fg="red")
        de_label_category.config(fg="red")
    else:
        de_entry_custom_category.config(fg="red")
        de_label_custom_category.config(fg="red")
        de_category_selection.config(fg="green")
        de_label_category.config(fg="green")


de_custom_category.trace_add("write", de_changed_custom_category)
de_entry_custom_category = tkinter.Entry(
    window, fg="red", textvariable=de_custom_category)
# german type selection
de_label_type = tkinter.Label(window, text="Select a german type...:", fg="red")

de_type_selection = tkinter.Listbox(window, fg="red", exportselection=0)


def de_type_listbox_changed(*args):
    if de_custom_type.get() != "":
        de_entry_custom_type.config(fg="green")
        de_label_custom_type.config(fg="green")
        de_type_selection.config(fg="red")
        de_label_type.config(fg="red")
    elif not de_type_selection.curselection():
        de_entry_custom_type.config(fg="red")
        de_label_custom_type.config(fg="red")
        de_type_selection.config(fg="red")
        de_label_type.config(fg="red")
    else:
        de_entry_custom_type.config(fg="red")
        de_label_custom_type.config(fg="red")
        de_type_selection.config(fg="green")
        de_label_type.config(fg="green")


de_type_selection.bind('<<ListboxSelect>>', de_type_listbox_changed)
# gets data from sql database
de_all_types = []
cur = conn.cursor()
sql_query = """
SELECT de_type FROM images
GROUP BY de_type;
"""
cur.execute(sql_query)
de_type = cur.fetchone()
while de_type != None:
    de_type = "".join(de_type)
    de_all_types.append(de_type)
    # adds the category to the selectionlist
    de_type_selection.insert(END, de_type)
    de_type = cur.fetchone()
# lets user add own option
de_label_custom_type = tkinter.Label(
    window, text="...or add a new one:", fg="red")
de_custom_type = StringVar()
de_custom_type.set("")


def de_changed_custom_type(*args):
    if de_custom_type.get() != "":
        de_entry_custom_type.config(fg="green")
        de_label_custom_type.config(fg="green")
        de_type_selection.config(fg="red")
        de_label_type.config(fg="red")
    elif not de_type_selection.curselection():
        de_entry_custom_type.config(fg="red")
        de_label_custom_type.config(fg="red")
        de_type_selection.config(fg="red")
        de_label_type.config(fg="red")
    else:
        de_entry_custom_type.config(fg="red")
        de_label_custom_type.config(fg="red")
        de_type_selection.config(fg="green")
        de_label_type.config(fg="green")


de_custom_type.trace_add("write", de_changed_custom_type)
de_entry_custom_type = tkinter.Entry(window, fg="red", textvariable=de_custom_type)
