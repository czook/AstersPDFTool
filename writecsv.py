from pdfreader import *
from node import *
import pandas as pd

def write_to_csv(event):
    #asdf
    los = pd.DataFrame({'In_Node':0, 'Visibile':0})

    for node in nodes:
        for edge in edges:
            if node.id == edge.nodeid1:
                df2 = {'In_Node':node.id, 'Visibile':edge.nodeid2}
                los = los.append(df2, ignore_index = True)
            elif node.id == edge.nodeid2:
                df2 = {'In_Node':node.id, 'Visibile':edge.nodeid1}
                los = los.append(df2, ignore_index = True)
    los.to_csv('./csvs/new_los.csv')


