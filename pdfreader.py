# Importing required modules
from tkinter import *
from PIL import Image,ImageTk
from pdf2image import convert_from_path
# Creating Tk container
root = Tk()
root.geometry("1600x900")
# Creating the frame for PDF Viewer
pdf_frame = Frame(root).pack(fill=BOTH,expand=0)
# Adding Scrollbar to the PDF frame
scrol_y = Scrollbar(pdf_frame,orient=VERTICAL)
# Adding text widget for inserting images
#pdf = Text(pdf_frame,yscrollcommand=scrol_y.set,bg="grey")
# Setting the scrollbar to the right side
scrol_y.pack(side=RIGHT,fill=Y)
# Here the PDF is converted to list of images
pages = convert_from_path('Center_Point_1stFloor.pdf',size=(1600,900))
# Empty list for storing images
photos = []
# Storing the converted images into list
for i in range(len(pages)):
  photos.append(ImageTk.PhotoImage(pages[i]))

canvas = Canvas(root,width = 1600, height = 900, bd=0)
image_id = canvas.create_image(800,450, image = photos[0])
canvas.pack()
canvas.old_coords = None

def draw_line(event):
  x,y = event.x, event.y
  if canvas.old_coords:
      x1, y1 = canvas.old_coords
      canvas.create_line(x,y,x1,y1,width=5, fill='blue')
  canvas.old_coords = x,y

def draw_circle(event):
  r = 8
  x,y = event.x, event.y
  canvas.create_oval(x-r, y-r, x+r, y+r, fill="red")


# Ending of mainloop
# Drawing lines
root.bind('<Button-3>', draw_line)
root.bind('<Button-3>', draw_line)
# Drawing Dots
root.bind('<ButtonPress-1>', draw_circle)
root.bind('<ButtonPress-1>', draw_circle)
root.mainloop()