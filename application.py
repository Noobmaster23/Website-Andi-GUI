# importing stuff
import tkinter
from tkinter import Label, StringVar, filedialog
from tkinter import simpledialog
from tkinter.constants import END
from tkinter import messagebox
from tkinter import ttk
from io import BytesIO

import os

from tkinter.tix import ROW

try:
    import PIL
except ImportError:
    print("Trying to Install required module: Pillow\n")
    os.system('python -m pip install Pillow')
import PIL

try:
    import psycopg2
except ImportError:
    print("Trying to Install required module: psycopg2\n")
    os.system('python -m pip install psycopg2-binary')
import psycopg2

try:
    import requests
except ImportError:
    print("Trying to Install requiroped module: requests\n")
    os.system('python -m pip install requests')
import psycopg2

import uuid

import datetime

from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageTk
# image editing


def make_copyright_image(image_path, gallery_path, img_name):
    result = {"width": 0, "height": 0, "size": 0,
              "new_img_path": ""}
    img = Image.open(image_path)
    result["width"] = img.size[0]
    result["height"] = img.size[1]
    result["size"] = os.path.getsize(image_path)
    img.convert("RGB")
    watermark = Image.new("RGBA", img.size, (0, 0, 0, 0))
    size = 2
    font = 'Raleway-Light.ttf'
    n_font = ImageFont.truetype(font, size)
    text = "© Andreas Heeb" + str(datetime.datetime.now().year)
    n_width, n_height = n_font.getsize(text)
    while (n_width+n_height < watermark.size[0]/2):
        size += 2
        n_font = ImageFont.truetype(font, size)
        n_width, n_height = n_font.getsize(text)
    draw = ImageDraw.Draw(watermark, 'RGBA')
    draw.text((watermark.size[0] - n_width,
               (watermark.size[1] - n_height)), text, font=n_font)
    alpha = watermark.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(0.5)
    watermark.putalpha(alpha)
    watermark = Image.composite(watermark, img, watermark)
    watermark.save(gallery_path + img_name + ".jpg", optimize=True, quality=95)
    result["new_img_path"] = gallery_path + img_name + ".jpg"
    return result


def make_thumbnail_image(gallery_path, img_name):
    img = Image.open(gallery_path + img_name + ".jpg")
    img = img.resize((int(img.size[0]/5), int(img.size[1]/5)), Image.ANTIALIAS)
    size = img.size
    img.save(gallery_path + "thumbnail/" + img_name +
             ".jpg", optimize=True, quality=50)
    return [os.path.getsize(gallery_path + "thumbnail/" + img_name + ".jpg"), size[0], size[1]]


# tkinter background stuff
root = tkinter.Tk()
root.title("Heebphotography.ch")
root.wm_iconbitmap("favicon.ico")
# frames
db_upload = tkinter.Frame(root)
db_update = tkinter.Frame(root)
db_delete = tkinter.Frame(root)
# connect to database
password = simpledialog.askstring(
    title="Database Password", prompt="Password:")
conn = psycopg2.connect(host="heebphotography.ch", port="5500",
                        database="heebphotography", user="postgres", password=password)  # so eifach chasch du sack nöd uf mini db zuägriffä :)
# layout
# select image
selected_images = tkinter.StringVar()

label_select_image = tkinter.Label(db_upload, text="Select Image:", fg="red")
path_to_image = tkinter.Label(
    db_upload, textvariable=selected_images, fg="green")


def save_image_path():
    selected_images.set(filedialog.askopenfilename(
        title="Select the image", filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*"))))
    button_select_image.config(fg="black")
    label_select_image.config(fg="black")
    db_upload.update()


button_select_image = tkinter.Button(
    db_upload, text="Select Image", command=save_image_path, fg="red")
# path to gallery
gallery_path = tkinter.StringVar()

label_gallery_path = tkinter.Label(
    db_upload, text="Select the path to the gallery folder:", fg="red")
path_to_gallery = tkinter.Label(
    db_upload, textvariable=gallery_path, fg="green")


def select_gallery_path():
    global gallery_path
    gallery_path.set(filedialog.askdirectory())
    label_gallery_path.config(fg="black")
    button_gallery_path.config(fg="black")
    db_upload.update()


button_gallery_path = tkinter.Button(
    db_upload, text="Select Path", command=select_gallery_path, fg="red")
# category selection
label_category = tkinter.Label(
    db_upload, text="Select a category...:", fg="red")

category_selection = tkinter.Listbox(db_upload, fg="red", exportselection=0)


def category_listbox_changed(*args):
    if custom_category.get() != "":
        entry_custom_category.config(fg="green")
        label_custom_category.config(fg="green")
        category_selection.config(fg="red")
        label_category.config(fg="red")
    elif not category_selection.curselection():
        entry_custom_category.config(fg="red")
        label_custom_category.config(fg="red")
        category_selection.config(fg="red")
        label_category.config(fg="red")
    else:
        entry_custom_category.config(fg="red")
        label_custom_category.config(fg="red")
        category_selection.config(fg="green")
        label_category.config(fg="green")


category_selection.bind('<<ListboxSelect>>', category_listbox_changed)
# gets data from sql database
all_categories = []
cur = conn.cursor()
sql_query = """
SELECT category FROM images
WHERE category IS NOT NULL
GROUP BY category;
"""
cur.execute(sql_query)
category = cur.fetchone()
while category != None and category[0] != None:
    category = "".join(category)
    all_categories.append(category)
    # adds the category to the selectionlist
    category_selection.insert(END, category)
    category = cur.fetchone()
# lets user add own option
label_custom_category = tkinter.Label(
    db_upload, text="...or add a new one:", fg="red")
custom_category = StringVar()
custom_category.set("")


def changed_custom_category(*args):
    if custom_category.get() != "":
        entry_custom_category.config(fg="green")
        label_custom_category.config(fg="green")
        category_selection.config(fg="red")
        label_category.config(fg="red")
    elif not category_selection.curselection():
        entry_custom_category.config(fg="red")
        label_custom_category.config(fg="red")
        category_selection.config(fg="red")
        label_category.config(fg="red")
    else:
        entry_custom_category.config(fg="red")
        label_custom_category.config(fg="red")
        category_selection.config(fg="green")
        label_category.config(fg="green")


custom_category.trace_add("write", changed_custom_category)
entry_custom_category = tkinter.Entry(
    db_upload, fg="red", textvariable=custom_category)
# type selection
label_type = tkinter.Label(db_upload, text="Select a type...:", fg="red")

type_selection = tkinter.Listbox(db_upload, fg="red", exportselection=0)


def type_listbox_changed(*args):
    if custom_type.get() != "":
        entry_custom_type.config(fg="green")
        label_custom_type.config(fg="green")
        type_selection.config(fg="red")
        label_type.config(fg="red")
    elif not type_selection.curselection():
        entry_custom_type.config(fg="red")
        label_custom_type.config(fg="red")
        type_selection.config(fg="red")
        label_type.config(fg="red")
    else:
        entry_custom_type.config(fg="red")
        label_custom_type.config(fg="red")
        type_selection.config(fg="green")
        label_type.config(fg="green")


type_selection.bind('<<ListboxSelect>>', type_listbox_changed)
# gets data from sql database
all_types = []
cur = conn.cursor()
sql_query = """
SELECT type FROM images
WHERE type IS NOT NULL
GROUP BY type;
"""
cur.execute(sql_query)
type_ = cur.fetchone()
while type_ != None and type_[0] != None:
    type_ = "".join(type_)
    all_types.append(type_)
    # adds the category to the selectionlist
    type_selection.insert(END, type_)
    type_ = cur.fetchone()
# lets user add own option
label_custom_type = tkinter.Label(
    db_upload, text="...or add a new one:", fg="red")
custom_type = StringVar()
custom_type.set("")


def changed_custom_type(*args):
    if custom_type.get() != "":
        entry_custom_type.config(fg="green")
        label_custom_type.config(fg="green")
        type_selection.config(fg="red")
        label_type.config(fg="red")
    elif not type_selection.curselection():
        entry_custom_type.config(fg="red")
        label_custom_type.config(fg="red")
        type_selection.config(fg="red")
        label_type.config(fg="red")
    else:
        entry_custom_type.config(fg="red")
        label_custom_type.config(fg="red")
        type_selection.config(fg="green")
        label_type.config(fg="green")


custom_type.trace_add("write", changed_custom_type)
entry_custom_type = tkinter.Entry(
    db_upload, fg="red", textvariable=custom_type)
# german category selection
de_label_category = tkinter.Label(
    db_upload, text="Select a german category...:", fg="red")

de_category_selection = tkinter.Listbox(db_upload, fg="red", exportselection=0)


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
WHERE de_category IS NOT NULL
GROUP BY de_category;
"""
cur.execute(sql_query)
de_category = cur.fetchone()
while de_category != None and de_category[0] != None:
    de_category = "".join(de_category)
    de_all_categories.append(de_category)
    # adds the category to the selectionlist
    de_category_selection.insert(END, de_category)
    de_category = cur.fetchone()
# lets user add own option
de_label_custom_category = tkinter.Label(
    db_upload, text="...or add a new one:", fg="red")
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
    db_upload, fg="red", textvariable=de_custom_category)
# german type selection
de_label_type = tkinter.Label(
    db_upload, text="Select a german type...:", fg="red")

de_type_selection = tkinter.Listbox(db_upload, fg="red", exportselection=0)


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
WHERE de_type IS NOT NULL
GROUP BY de_type;
"""
cur.execute(sql_query)
de_type = cur.fetchone()
while de_type != None and de_type[0] != None:
    de_type = "".join(de_type)
    de_all_types.append(de_type)
    # adds the category to the selectionlist
    de_type_selection.insert(END, de_type)
    de_type = cur.fetchone()
# lets user add own option
de_label_custom_type = tkinter.Label(
    db_upload, text="...or add a new one:", fg="red")
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
de_entry_custom_type = tkinter.Entry(
    db_upload, fg="red", textvariable=de_custom_type)
# latin name selection
latin_name_label = tkinter.Label(
    db_upload, text="Select a latin name...:", fg="red")

latin_name_selection = tkinter.Listbox(db_upload, fg="red", exportselection=0)


def latin_listbox_changed(*args):
    if latin_custom_name.get() != "":
        custom_latin_name_entry.config(fg="green")
        custom_latin_name_label.config(fg="green")
        latin_name_selection.config(fg="red")
        latin_name_label.config(fg="red")
    elif not latin_name_selection.curselection():
        custom_latin_name_entry.config(fg="red")
        custom_latin_name_label.config(fg="red")
        latin_name_selection.config(fg="red")
        latin_name_label.config(fg="red")
    else:
        custom_latin_name_entry.config(fg="red")
        custom_latin_name_label.config(fg="red")
        latin_name_selection.config(fg="green")
        latin_name_label.config(fg="green")


latin_name_selection.bind('<<ListboxSelect>>', latin_listbox_changed)
# gets data from sql database
all_latin_names = []
cur = conn.cursor()
sql_query = """
SELECT latin_name FROM images
WHERE latin_name IS NOT NULL
GROUP BY latin_name;
"""
cur.execute(sql_query)
latin_name = cur.fetchone()
while latin_name != None and latin_name[0] != None:
    latin_name = "".join(latin_name)
    all_latin_names.append(latin_name)
    # adds the category to the selectionlist
    latin_name_selection.insert(END, latin_name)
    latin_name = cur.fetchone()
# lets user add own option
custom_latin_name_label = tkinter.Label(
    db_upload, text="...or add a new one:", fg="red")
latin_custom_name = StringVar()
latin_custom_name.set("")


def changed_custom_latin_name(*args):
    if de_custom_type.get() != "":
        custom_latin_name_entry.config(fg="green")
        custom_latin_name_label.config(fg="green")
        latin_name_selection.config(fg="red")
        latin_name_label.config(fg="red")
    elif not latin_name_selection.curselection():
        custom_latin_name_entry.config(fg="red")
        custom_latin_name_label.config(fg="red")
        latin_name_selection.config(fg="red")
        latin_name_label.config(fg="red")
    else:
        custom_latin_name_entry.config(fg="red")
        custom_latin_name_label.config(fg="red")
        latin_name_selection.config(fg="green")
        latin_name_label.config(fg="green")


latin_custom_name.trace_add("write", changed_custom_latin_name)
custom_latin_name_entry = tkinter.Entry(
    db_upload, fg="red", textvariable=latin_custom_name)
# add comment
comment = StringVar()
comment.set("")
label_comment = tkinter.Label(db_upload, text="Add an additional comment:")

entry_comment = tkinter.Entry(db_upload, textvariable=comment)
# submit button


def submit():
    if bool(selected_images.get()) and bool(gallery_path.get()) and (bool(category_selection.curselection()) or bool(custom_category.get())) and (bool(type_selection.curselection() or bool(custom_type.get()))) and ((bool(de_category_selection.curselection()) or bool(de_custom_category.get())) and (bool(de_type_selection.curselection() or bool(de_custom_type.get()))) and (bool(latin_name_selection.curselection() or bool(latin_custom_name.get())))):
        # uploads the full_img to the database
        db_name = uuid.uuid1()
        db_category = custom_category.get() if bool(custom_category.get(
        )) else category_selection.get(category_selection.curselection())
        db_de_category = de_custom_category.get() if bool(de_custom_category.get(
        )) else de_category_selection.get(de_category_selection.curselection())
        db_type = custom_type.get() if bool(
            custom_type.get()) else type_selection.get(type_selection.curselection())
        db_de_type = de_custom_type.get() if bool(
            de_custom_type.get()) else de_type_selection.get(de_type_selection.curselection())
        db_comment = entry_comment.get() if bool(entry_comment.get()) else "NULL"
        db_upload_date = datetime.datetime.now()
        img_editing_result = make_copyright_image(
            selected_images.get(), gallery_path.get() + "/", str(db_name))
        db_name = str(db_name)
        db_category = str(db_category).replace(" ", "_")
        db_type = str(db_type).replace(" ", "_")
        db_comment = str(db_comment)
        db_upload_date = str(db_upload_date)
        db_width = str(img_editing_result["width"])
        db_height = str(img_editing_result["height"])
        db_size = str(img_editing_result["size"])
        thumbnail_result = make_thumbnail_image(
            gallery_path.get() + "/", db_name)
        db_thumbnail_size = str(thumbnail_result[0])
        db_thumbnail_width = str(thumbnail_result[1])
        db_thumbnail_height = str(thumbnail_result[2])
        db_de_category = str(db_de_category).replace(" ", "_")
        db_de_type = str(db_de_type).replace(" ", "_")
        # latin name
        db_latin_name = latin_custom_name.get() if bool(latin_custom_name.get(
        )) else latin_name_selection.get(latin_name_selection.curselection())
        db_latin_name = str(db_latin_name).replace(
            " ", "_")  # so no errors in db

        sql_query = """
        INSERT INTO images (name, category, type, comment, upload_date, width, height, size, thumbnail_size, thumbnail_width, thumbnail_height, de_category, de_type, latin_name, last_changed)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cur = conn.cursor()
        cur.execute(sql_query, (db_name, db_category, db_type, db_comment, db_upload_date, db_width,
                                db_height, db_size, db_thumbnail_size, db_thumbnail_width, db_thumbnail_height, db_de_category, db_de_type, db_latin_name, db_upload_date))
        conn.commit()
        messagebox.showinfo(
            "Success!", "Image uploaded successfully. Please don't forget to also update GitHub!")

    else:
        messagebox.showerror("Idiot Sanwdich",
                             "Not everything is filled out!")


submit_button = tkinter.Button(db_upload, text="Upload", command=submit)
# update things in the database
# make variables
update_name_selection_value = tkinter.StringVar()
update_de_category_selection_value = tkinter.StringVar()
update_de_type_selection_value = tkinter.StringVar()
update_category_selection_value = tkinter.StringVar()
update_type_selection_value = tkinter.StringVar()
update_latin_name_selection_value = tkinter.StringVar()
# gets all image names
cur = conn.cursor()
sql_query = """
SELECT name FROM images
WHERE name IS NOT NULL
GROUP BY name;
"""
cur.execute(sql_query)
name = cur.fetchone()
all_names = []
while name != None and name[0] != None:
    name = "".join(name)
    all_names.append(name)
    name = cur.fetchone()
# make the label for combox
update_name_label = tkinter.Label(db_update, text="Select an image to update:")
# makes combox
update_name_selection = ttk.Combobox(
    db_update, textvariable=update_name_selection_value, values=all_names, width=40)
# inserts the values if the combox value changes


def update_name_selection_value_changed(*args):
    # changes the other values to the values in the database
    cur = conn.cursor()
    sql_query = """
    SELECT de_category FROM images
    WHERE name = '{0}'
    GROUP BY de_category;
    """.format(update_name_selection_value.get())
    cur.execute(sql_query)
    temp_sql_value = "".join(cur.fetchone())
    update_de_category_selection_value.set(temp_sql_value)

    cur = conn.cursor()
    sql_query = """
    SELECT de_type FROM images
    WHERE name = '{0}'
    GROUP BY de_type;
    """.format(update_name_selection_value.get())
    cur.execute(sql_query)
    temp_sql_value = "".join(cur.fetchone())
    update_de_type_selection_value.set(temp_sql_value)

    cur = conn.cursor()
    sql_query = """
    SELECT category FROM images
    WHERE name = '{0}'
    GROUP BY category;
    """.format(update_name_selection_value.get())
    cur.execute(sql_query)
    temp_sql_value = "".join(cur.fetchone())
    update_category_selection_value.set(temp_sql_value)

    cur = conn.cursor()
    sql_query = """
    SELECT type FROM images
    WHERE name = '{0}'
    GROUP BY type;
    """.format(update_name_selection_value.get())
    cur.execute(sql_query)
    temp_sql_value = "".join(cur.fetchone())
    update_type_selection_value.set(temp_sql_value)

    cur = conn.cursor()
    sql_query = """
    SELECT latin_name FROM images
    WHERE name = '{0}'
    GROUP BY latin_name;
    """.format(update_name_selection_value.get())
    cur.execute(sql_query)
    temp_sql_value = "".join(cur.fetchone())
    update_latin_name_selection_value.set(temp_sql_value)


update_name_selection_value.trace_add(
    "write", update_name_selection_value_changed)
# changeable de category
update_de_category_label = tkinter.Label(
    db_update, text="Select a german category or make a new one:")
# combox
# gets all de categories
cur = conn.cursor()
sql_query = """
SELECT de_category FROM images
WHERE de_category IS NOT NULL
GROUP BY de_category
ORDER BY de_category;
"""
cur.execute(sql_query)
de_category = cur.fetchone()
all_de_categories = []
while de_category != None and de_category[0] != None:
    de_category = "".join(de_category)
    all_de_categories.append(de_category)
    de_category = cur.fetchone()
update_de_category_selection = ttk.Combobox(
    db_update, textvariable=update_de_category_selection_value, values=all_de_categories)
# changeable de type
update_de_type_label = tkinter.Label(
    db_update, text="Select a german type or make a new one:")
# combox
# gets all de categories
cur = conn.cursor()
sql_query = """
SELECT de_type FROM images
WHERE de_type IS NOT NULL
GROUP BY de_type
ORDER BY de_type;
"""
cur.execute(sql_query)
de_type = cur.fetchone()
all_de_types = []
while de_type != None and de_type[0] != None:
    de_type = "".join(de_type)
    all_de_types.append(de_type)
    de_type = cur.fetchone()
update_de_type_selection = ttk.Combobox(
    db_update, textvariable=update_de_type_selection_value, values=all_de_types)
# changeable category
update_category_label = tkinter.Label(
    db_update, text="Select a category or make a new one:")
# combox
# gets all de categories
cur = conn.cursor()
sql_query = """
SELECT category FROM images
WHERE category IS NOT NULL
GROUP BY category
ORDER BY category;
"""
cur.execute(sql_query)
category = cur.fetchone()
all_categories = []
while category != None and category[0] != None:
    category = "".join(category)
    all_categories.append(category)
    category = cur.fetchone()
update_category_selection = ttk.Combobox(
    db_update, textvariable=update_category_selection_value, values=all_categories)
# changeable type
update_type_label = tkinter.Label(
    db_update, text="Select a type or make a new one:")
# combox
# gets all de categories
cur = conn.cursor()
sql_query = """
SELECT type FROM images
WHERE type IS NOT NULL
GROUP BY type
ORDER BY type;
"""
cur.execute(sql_query)
type_ = cur.fetchone()
all_types = []
while type_ != None and type_[0] != None:
    type_ = "".join(type_)
    all_types.append(type_)
    type_ = cur.fetchone()
update_type_selection = ttk.Combobox(
    db_update, textvariable=update_type_selection_value, values=all_types)
# changeable latin name
update_latin_name_label = tkinter.Label(
    db_update, text="Select a latin name or make a new one:")
# combox
# gets all de categories
cur = conn.cursor()
sql_query = """
SELECT latin_name FROM images
WHERE latin_name IS NOT NULL
GROUP BY latin_name
ORDER BY latin_name;
"""
cur.execute(sql_query)
latin_name = cur.fetchone()
all_latin_names = []
while latin_name != None and latin_name[0] != None:
    latin_name = "".join(latin_name)
    all_latin_names.append(latin_name)
    latin_name = cur.fetchone()
update_latin_name_selection = ttk.Combobox(
    db_update, textvariable=update_latin_name_selection_value, values=all_latin_names)
# update database (button + function)


def update_db():
    db_update_name = update_name_selection_value.get()
    db_update_name = db_update_name.replace(" ", "_")

    db_update_de_category = update_de_category_selection_value.get()
    db_update_de_category = db_update_de_category.replace(" ", "_")

    db_update_de_type = update_de_type_selection_value.get()
    db_update_de_type = db_update_de_type.replace(" ", "_")

    db_update_category = update_category_selection_value.get()
    db_update_category = db_update_category.replace(" ", "_")

    db_update_type = update_type_selection_value.get()
    db_update_type = db_update_type.replace(" ", "_")

    db_update_latin_name = update_latin_name_selection_value.get()
    db_update_latin_name = db_update_latin_name.replace(" ", "_")

    db_update_last_changed = datetime.datetime.now()
    db_update_last_changed = str(db_update_last_changed)

    cur = conn.cursor()

    sql_query = "UPDATE images SET category = '{0}', type = '{1}', de_category = '{2}', de_type = '{3}', latin_name = '{4}', last_changed = '{5}' WHERE name = '{6}';".format(
        db_update_category, db_update_type, db_update_de_category, db_update_de_type, db_update_latin_name, db_update_last_changed, db_update_name)
    cur.execute(sql_query)
    conn.commit()
    cur.close()

    messagebox.showinfo(
        "Success!", "Image update successfull.")


update_button = tkinter.Button(db_update, text="Update", command=update_db)
# add all thing to the update frame
update_name_label.grid(row=0, column=0)
update_name_selection.grid(row=1, column=0)

update_de_category_label.grid(row=2, column=0)
update_de_category_selection.grid(row=3, column=0)

update_de_type_label.grid(row=4, column=0)
update_de_type_selection.grid(row=5, column=0)

update_category_label.grid(row=6, column=0)
update_category_selection.grid(row=7, column=0)

update_type_label.grid(row=8, column=0)
update_type_selection.grid(row=9, column=0)

update_latin_name_label.grid(row=10, column=0)
update_latin_name_selection.grid(row=11, column=0)

update_button.grid(row=12, column=0)
# delete page
# variables
db_delete_name_selection_value = tkinter.StringVar()
# select name
cur = conn.cursor()
sql_query = "SELECT DISTINCT name FROM images;"
cur.execute(sql_query)
name = cur.fetchone()
all_names = []
while name != None and name[0] != None:
    name = "".join(name)
    all_names.append(name)
    name = cur.fetchone()

db_delete_name_label = tkinter.Label(
    db_delete, text="Select an image to delete:")
db_delete_name_selection = ttk.Combobox(
    db_delete, textvariable=db_delete_name_selection_value, values=all_names, width=40)
# on combobox value change, load the image
# image
db_delete_image = tkinter.Label(db_delete)


def db_delete_name_selection_value_change(*args):
    global render
    url = "https://heebphotography.ch/public/images/gallery/thumbnail/" + \
        db_delete_name_selection_value.get() + ".jpg"
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    # img.show()
    render = ImageTk.PhotoImage(img)

    db_delete_image.config(image=render)


db_delete_name_selection_value.trace_add(
    'write', db_delete_name_selection_value_change)
# delete button
def delete_image(*args):
    if messagebox.askokcancel("DELETING IMAGE!", "Do you really want to delete this image? This can't be undone!"):
        cur = conn.cursor()
        sql_query = "DELETE FROM images WHERE name = '{0}';".format(db_delete_name_selection_value.get())
        cur.execute(sql_query)
        conn.commit()
        cur.close()

db_delete_button = tkinter.Button(db_delete, text="DELETE", command=delete_image)
# insert everything
db_delete_name_label.grid(row=0, column=0)
db_delete_name_selection.grid(row=1, column=0)
db_delete_image.grid(row=3, column=0)
db_delete_button.grid(row=4, column=0)
# switch to upload function, switches to the upload selection when selection in menubar


def switch_to_upload():
    # deletes ALL Frames
    db_delete.pack_forget()
    db_update.pack_forget()
    db_upload.pack_forget()

    # makes only the upload frame
    db_upload.pack()
# switch to upload function, switches to the upload selection when selection in menubar


def switch_to_delete():
    # deletes ALL Frames
    db_delete.pack_forget()
    db_update.pack_forget()
    db_upload.pack_forget()

    # makes only the delete frame
    db_delete.pack()
 # switch to upload function, switches to the upload selection when selection in menubar


def switch_to_update():
    # deletes ALL Frames
    db_delete.pack_forget()
    db_update.pack_forget()
    db_upload.pack_forget()

    # makes only the update frame
    db_update.pack()


# Menubar
menubar = tkinter.Menu(root)
# Adds upload selection to menubar
menubar.add_command(label="Upload", command=switch_to_upload)
# Adds update selection to menubar
menubar.add_command(label="Update", command=switch_to_update)
# Adds delete selection to menubar
menubar.add_command(label="Delete", command=switch_to_delete)
# makes the window
# select image
label_select_image.grid(row=0, column=0)
button_select_image.grid(row=0, column=1)
path_to_image.grid(row=1, column=0, columnspan=2)
# select gallery path
label_gallery_path.grid(row=2, column=0)
button_gallery_path.grid(row=2, column=1)
path_to_gallery.grid(row=3, column=0, columnspan=2)
# select category
label_category.grid(row=4, column=0)
selection_height = 4
category_selection.configure(height=selection_height)
category_selection.grid(row=5, column=0)

label_custom_category.grid(row=6, column=0)
entry_custom_category.grid(row=7, column=0)
# select german category
de_label_category.grid(row=4, column=1)
de_category_selection.configure(height=selection_height)
de_category_selection.grid(row=5, column=1)

de_label_custom_category.grid(row=6, column=1)
de_entry_custom_category.grid(row=7, column=1)
# select type
label_type.grid(row=8, column=0)
type_selection.configure(height=selection_height)
type_selection.grid(row=9, column=0)

label_custom_type.grid(row=10, column=0)
entry_custom_type.grid(row=11, column=0)
# select german type
de_label_type.grid(row=8, column=1)
de_type_selection.configure(height=selection_height)
de_type_selection.grid(row=9, column=1)

de_label_custom_type.grid(row=10, column=1)
de_entry_custom_type.grid(row=11, column=1)
# select latin name
latin_name_label.grid(row=12, column=0, columnspan=2)
latin_name_selection.configure(height=selection_height)
latin_name_selection.grid(row=13, column=0, columnspan=2)

custom_latin_name_label.grid(row=14, column=0, columnspan=2)
custom_latin_name_entry.grid(row=15, column=0, columnspan=2)
# add comment
label_comment.grid(row=16, column=0, columnspan=2)
entry_comment.grid(row=17, column=0, columnspan=2)
# submit button
submit_button.grid(row=18, column=0, columnspan=2)
# db_upload frame
db_upload.pack()
# window
root.config(menu=menubar)
root.mainloop()
