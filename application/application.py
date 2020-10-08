# importing stuff
import tkinter
from tkinter import StringVar, filedialog
from tkinter import simpledialog
from tkinter.constants import END
from tkinter import messagebox

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
    os.system('python -m pip install psycopg2')
import psycopg2

import uuid

import datetime

from PIL import Image, ImageDraw, ImageFont, ImageEnhance
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
    draw.text((0, (watermark.size[1] - n_height)), text, font=n_font)
    alpha = watermark.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(0.25)
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
window = tkinter.Tk()
window.title("Heebphotography.ch")
window.wm_iconbitmap("favicon.ico")
# connect to database
password = simpledialog.askstring(
    title="Database Password", prompt="Password:")
conn = psycopg2.connect(host="heebphotography.ch", port="5500",
                        database="heebphotography", user="postgres", password=password) # so eifach chasch du sack nöd uf mini db zuägriffä :)
# layout
# select image
selected_images = tkinter.StringVar()

label_select_image = tkinter.Label(window, text="Select Image:", fg="red")
path_to_image = tkinter.Label(window, textvariable=selected_images, fg="green")


def save_image_path():
    selected_images.set(filedialog.askopenfilename(
        title="Select the image", filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*"))))
    button_select_image.config(fg="black")
    label_select_image.config(fg="black")
    window.update()


button_select_image = tkinter.Button(
    window, text="Select Image", command=save_image_path, fg="red")
# path to gallery
gallery_path = tkinter.StringVar()

label_gallery_path = tkinter.Label(
    window, text="Select the path to the gallery folder:", fg="red")
path_to_gallery = tkinter.Label(window, textvariable=gallery_path, fg="green")


def select_gallery_path():
    global gallery_path
    gallery_path.set(filedialog.askdirectory())
    label_gallery_path.config(fg="black")
    button_gallery_path.config(fg="black")
    window.update()


button_gallery_path = tkinter.Button(
    window, text="Select Path", command=select_gallery_path, fg="red")
# category selection
label_category = tkinter.Label(window, text="Select a category...:", fg="red")

category_selection = tkinter.Listbox(window, fg="red", exportselection=0)


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
    window, text="...or add a new one:", fg="red")
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
    window, fg="red", textvariable=custom_category)
# type selection
label_type = tkinter.Label(window, text="Select a type...:", fg="red")

type_selection = tkinter.Listbox(window, fg="red", exportselection=0)


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
    window, text="...or add a new one:", fg="red")
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
entry_custom_type = tkinter.Entry(window, fg="red", textvariable=custom_type)
# german category selection
de_label_category = tkinter.Label(
    window, text="Select a german category...:", fg="red")

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
while de_category != None and de_category[0] != None:
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
de_label_type = tkinter.Label(
    window, text="Select a german type...:", fg="red")

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
while de_type != None and de_type[0] != None:
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
de_entry_custom_type = tkinter.Entry(
    window, fg="red", textvariable=de_custom_type)
# add comment
comment = StringVar()
comment.set("")
label_comment = tkinter.Label(window, text="Add an additional comment:")

entry_comment = tkinter.Entry(window, textvariable=comment)
# submit button


def submit():
    if bool(selected_images.get()) and bool(gallery_path.get()) and (bool(category_selection.curselection()) or bool(custom_category.get())) and (bool(type_selection.curselection() or bool(custom_type.get()))) and ((bool(de_category_selection.curselection()) or bool(de_custom_category.get())) and (bool(de_type_selection.curselection() or bool(de_custom_type.get())))):
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

        sql_query = """
        INSERT INTO images (name, category, type, comment, upload_date, width, height, size, thumbnail_size, thumbnail_width, thumbnail_height, de_category, de_type)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cur = conn.cursor()
        cur.execute(sql_query, (db_name, db_category, db_type, db_comment, db_upload_date, db_width,
                                db_height, db_size, db_thumbnail_size, db_thumbnail_width, db_thumbnail_height, db_de_category, db_de_type))
        conn.commit()
        messagebox.showinfo(
            "Success!", "Image uploaded successfully. Please don't forget to also update GitHub!")

    else:
        messagebox.showerror("Idiot Sanwdich",
                             "Not everything is filled out!")


submit_button = tkinter.Button(window, text="Submit", command=submit)
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
category_selection.grid(row=5, column=0)

label_custom_category.grid(row=6, column=0)
entry_custom_category.grid(row=7, column=0)
# select german category
de_label_category.grid(row=4, column=1)
de_category_selection.grid(row=5, column=1)

de_label_custom_category.grid(row=6, column=1)
de_entry_custom_category.grid(row=7, column=1)
# select type
label_type.grid(row=8, column=0)
type_selection.grid(row=9, column=0)

label_custom_type.grid(row=10, column=0)
entry_custom_type.grid(row=11, column=0)
# select german type
de_label_type.grid(row=8, column=1)
de_type_selection.grid(row=9, column=1)

de_label_custom_type.grid(row=10, column=1)
de_entry_custom_type.grid(row=11, column=1)
# add comment
label_comment.grid(row=12, column=0, columnspan=2)
entry_comment.grid(row=13, column=0, columnspan=2)
# submit button
submit_button.grid(row=14, column=0, columnspan=2)
# window
window.mainloop()
