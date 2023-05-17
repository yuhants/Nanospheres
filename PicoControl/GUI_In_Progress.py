# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 09:53:45 2023

@author: Microspheres
"""

import tkinter as tk
from tkinter import ttk
from Taking_Data_Picoscope_FCN import take_data 
from Charge_From_TT2_FCN import get_charge


#def run_scope():
    
    #return(take_data(int(buff_size.get()), int(num_buffs.get()), int(sample_int.get())))

#def channel_compare():
    
    #return(get_charge(int(num.get()),int(buff_size.get()), int(num_buffs.get()), int(sample_int.get())))

top = tk.Tk()
top.title('Lab GUI') #Title for the GUI

#creating input variables for the functions that correspond to the two functions (td = take data and tt2 = get charge)
buff_size_td = tk.StringVar()  
num_buffs_td = tk.StringVar()
sample_int_td = tk.StringVar()

num_tt2 = tk.StringVar()
buff_size_tt2 = tk.StringVar()
num_buffs_tt2 = tk.StringVar()
sample_int_tt2 = tk.StringVar()

#creating labels for the entry boxes (_td denotes take data input and _gc indicates get charge input)

bs_label_td = tk.ttk.Label(top, width=12, text='buffer size')
nb_label_td = tk.ttk.Label(top, width=12, text='number of buffers')
si_label_td = tk.ttk.Label(top, width=12, text='sample interval ')
n_label_gc = tk.ttk.Label(top, width=12, text='number of iterations')
bs_label_gc = tk.ttk.Label(top, width=12, text='buffer size')
nb_label_gc = tk.ttk.Label(top, width=12, text='number of buffers')
si_label_gc = tk.ttk.Label(top, width=12, text='sample interval')

#creating entry boxes for the function variables

buff_size_td_entry = ttk.Entry(width=7, textvariable=buff_size_td)
num_buffs_td_entry = ttk.Entry(width=7, textvariable=num_buffs_td)
sample_int_td_entry = ttk.Entry(width=7, textvariable=sample_int_td)

num_tt2_entry = ttk.Entry(width=7, textvariable=num_tt2)
buff_size_tt2_entry = ttk.Entry(width=7, textvariable=buff_size_tt2)
num_buffs_tt2_entry = ttk.Entry(width=7, textvariable=num_buffs_tt2)
sample_int_tt2_entry = ttk.Entry(width=7, textvariable=sample_int_tt2)

#This resets the values of the variables so the GUID doesn't reuse a previous entry
buff_size_td.set("")
num_buffs_td.set("")
sample_int_td.set("")

num_tt2.set("")
buff_size_tt2.set("")
num_buffs_tt2.set("")
sample_int_tt2.set("")

#setting the grid layout for the GUI. Labels are in the row above the entry boxes. 
#Both rows and columns start with index 0

bs_label_td.grid(row=0, column =0, padx=5, pady=5, sticky='ew')
nb_label_td.grid(row=0, column =1, padx=5,pady=5, sticky='ew')
si_label_td.grid(row=0, column =2, padx=5,pady=5, sticky='ew')

bs_label_gc.grid(row=3, column =0, padx=5, pady=5, sticky='ew')
nb_label_gc.grid(row=3, column =1, padx=5,pady=5, sticky='ew')
si_label_gc.grid(row=3, column =2, padx=5,pady=5, sticky='ew')
n_label_gc.grid(row=3, column =3, padx=5,pady=5, sticky='ew')

buff_size_td_entry.grid(row=1, column=0, padx=5, pady=5, sticky='ew')
num_buffs_td_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
sample_int_td_entry.grid(row=1, column=2, padx=5, pady=5, sticky='ew')

num_tt2_entry.grid(row=4, column=3, padx=5, pady=5, sticky='ew')
buff_size_tt2_entry.grid(row=4, column=0, padx=5, pady=5, sticky='ew')
num_buffs_tt2_entry.grid(row=4, column=1, padx=5, pady=5, sticky='ew')
sample_int_tt2_entry.grid(row=4, column=2, padx=5, pady=5, sticky='ew')

#making the function buttons. The inputs are converted to integers inside these commands

takedata = tk.Button(top, width=7, text = 'take data', command =lambda: take_data(int(buff_size_td.get()), int(num_buffs_td.get()), int(sample_int_td.get())))
takedata.grid(row=2, column=0,padx=5,pady=5, sticky='ew')
charge_tt2 = tk.Button(top, width=7, text = 'get charge', command =lambda: get_charge(int(num_tt2.get()),int(buff_size_tt2.get()), int(num_buffs_tt2.get()), int(sample_int_tt2.get())))
charge_tt2.grid(row=5, column=0,padx=5, pady=5, sticky='ew')

#resetting values again
buff_size_td.set("")
num_buffs_td.set("")
sample_int_td.set("")

num_tt2.set("")
buff_size_tt2.set("")
num_buffs_tt2.set("")
sample_int_tt2.set("")

#configuring grid column size

top.grid_columnconfigure(0, weight=1)
top.grid_columnconfigure(1, weight=1)
top.grid_columnconfigure(2, weight=1)
top.grid_columnconfigure(3, weight=1)

#closing out the GUI

top.mainloop()

