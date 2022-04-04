# Importing required modules
from tkinter import *
from PIL import Image,ImageTk
from pdf2image import convert_from_path
import pandas as pd
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
canvas.old_node_id = None
 
#self.canvas.find_all() finds all the objects

# Ending of mainloop
class Node:
    def __init__(self, x, y, id, tag):
        self.x = x
        self.y = y
        self.id = id
        self.tag = tag
    
class Edge:
    def __init__(self, x1,y1,x2,y2,id,nodeid1,nodeid2):
        self.x1 = x1
        self.y1 = y1
        self.id = id
        self.x2 = x2
        self.y2 = y2
        self.nodeid1 = nodeid1
        self.nodeid2 = nodeid2


nodes = []
edges = []
def draw_line(event):
  x,y = event.x, event.y
  completed = False
  for node in nodes:
    if canvas.old_coords and abs(x - node.x)^2 + abs(y - node.y)^2 < 8^2:
        x1, y1 = canvas.old_coords
        tempid = canvas.create_line(node.x,node.y,x1,y1,width=5, fill='blue')
        edges.append(Edge(node.x,node.y,x1,y1,tempid,node.id ,canvas.old_node_id))
        canvas.tag_raise(node.id)
        canvas.tag_raise(canvas.old_node_id)
        canvas.old_coords = None
        canvas.old_node_id = None
        completed = True
    if abs(x - node.x)^2 + abs(y - node.y)^2 < 8^2 and not completed:
      canvas.old_coords = node.x,node.y
      canvas.old_node_id = node.id
  

def draw_circle(event):
  r = 8
  x,y = event.x, event.y
  tempid = canvas.create_oval(x-r, y-r, x+r, y+r, fill="red")
  nodes.append(Node(x,y,tempid,'class'))

mode = 1
mode_str = ''
def mode_switch(event):
  if mode == 1: 
    #node mode
    mode_str = 'node mode'
    mode =2
  elif mode == 2:
    #connect mode
    mode_str = 'connect mode'
    mode =2

def print_all_nodes_and_edges(event):
    for a in nodes:
        print(f'x: {a.x}, y:{a.y}, id:{a.id}')
    for a in edges:
        print(f'x1: {a.x1}, y1:{a.y1}, x2: {a.x2}, y2:{a.y2}, EdgeId:{a.id}, NodeId1:{a.nodeid1}, NodeId2:{a.nodeid2}')

def draw_exit(event):
  r = 8
  x,y = event.x, event.y
  tempid = canvas.create_oval(x-r, y-r, x+r, y+r, fill="green")
  nodes.append(Node(x,y,tempid,'exit'))


def write_to_csv(event):
    #asdf
    data = [[0,0]]
    los = pd.DataFrame(data, columns=['In_Node', 'Visibile' ])
    for node in nodes:
        for edge in edges:
            if node.id == edge.nodeid1:
                df2 = {'In_Node':node.id, 'Visibile':edge.nodeid2}
                los = los.append(df2, ignore_index = True)
            elif node.id == edge.nodeid2:
                df2 = {'In_Node':node.id, 'Visibile':edge.nodeid1}
                los = los.append(df2, ignore_index = True)
    los.drop_duplicates()
    los.to_csv('./csvs/new_los.csv', index=False)
    data = [[0,0,0]]
    distance = pd.DataFrame(data, columns=['In_Node', 'Visibile', 'Distance (in pixels)'])
    for node in nodes:
        for edge in edges:
            if node.id == edge.nodeid1:
                df2 = {'In_Node':node.id, 'Visibile':edge.nodeid2, 'Distance (in pixels)':(abs(edge.x1 - edge.x2)^2 + abs(edge.y1 - edge.y2)^2)}
                distance = distance.append(df2, ignore_index = True)
            elif node.id == edge.nodeid2:
                df2 = {'In_Node':node.id, 'Visibile':edge.nodeid1, 'Distance (in pixels)':(abs(edge.x1 - edge.x2)^2 + abs(edge.y1 - edge.y2)^2)}
                distance = distance.append(df2, ignore_index = True)
    distance.drop_duplicates()
    distance.to_csv('./csvs/new_distances.csv', index=False)

# Write CSV
root.bind('<Enter>', write_to_csv)
root.bind('<Enter>', write_to_csv)

# Printing nodes and edges
root.bind('p', print_all_nodes_and_edges)
root.bind('p', print_all_nodes_and_edges)
# Switching modes
root.bind('a', mode_switch)
root.bind('a', mode_switch)
# Drawing lines
root.bind('<Button-3>', draw_line)
root.bind('<Button-3>', draw_line)
# Drawing Dots
root.bind('<ButtonPress-1>', draw_circle)
root.bind('<ButtonPress-1>', draw_circle)
# Drawing Exits
root.bind('<ButtonPress-2>', draw_exit)
root.bind('<ButtonPress-2>', draw_exit)

root.mainloop()