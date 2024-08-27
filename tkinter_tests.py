from tkinter import *
from tkinter import ttk
import tkintermapview

import pandas as pd
import altair as alt
from altair import Chart
import vl_convert as vlc
from PIL import Image, ImageTk
from pathlib import Path

from geocoder import ip
g = ip('me')

"""
'''
root = Tk()
root.title('Testing Tkinter Sections')
frame = ttk.Frame(root, padding='12 12 12 12')
frame.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

user_entry = ttk.Entry(frame, width=21)
user_entry.grid(column=0, row=0, sticky=E)
'''
'''
ttk.Label(frame, text='Account Found, Currently Loading...', padding='0 0 0 10' ).grid(column=0, row=0, sticky=W)
progress_bar = ttk.Progressbar(frame, maximum=70)
progress_bar.grid(column=0, row=2, columnspan=2, sticky=(W, E))

print(12*24)
root.after(1000)
for i in range(10):
    progress_bar.step(1)
frame.update_idletasks()
print(3*2)
root.after(1000)
for i in range(50):
    progress_bar.step(1)
frame.update_idletasks()
print(5 + 5)
frame.update_idletasks()
root.after(1000)
progress_bar.step(1)
frame.update_idletasks()
'''
from tkinter import *
from tkinter import ttk

class ShowData:
    def __init__(self, root, all_activities=''):
        
        root.title('Garmin Activities Data')

        # make notebook
        notebook = ttk.Notebook(root)
        notebook.grid(column=0, row=0, sticky=(N, W, E, S))
            # frames of notebook
        self.run_frame = ttk.Frame(notebook, padding='12 12 12 12')
        self.run_frame.grid(column=0, row=0, sticky=(N, W, E, S))
        notebook.add(self.run_frame, text='Running')

        self.bike_frame = ttk.Frame(notebook, padding='12 12 12 12')
        self.bike_frame.grid(column=0, row=0, sticky=(N, W, E, S))
        notebook.add(self.bike_frame, text='Biking')

        self.swim_frame = ttk.Frame(notebook, padding='12 12 12 12')
        self.swim_frame.grid(column=0, row=0, sticky=(N, W, E, S))
        notebook.add(self.swim_frame, text='Swimming')

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        notebook.columnconfigure(0, weight=1)
        notebook.rowconfigure(0, weight=1)
        # use this to see if frame works, need to add widget for window to actually show up
        user_entry = ttk.Entry(self.run_frame, width=21)
        user_entry.grid(column=0, row=0, sticky=E)

        # create all pandas dataframes to use
        #self.running_df, self.biking_df, self.swimming_df = self.create_dfs(all_activities)
    
    def create_dfs(activites):
        pass
root=Tk()
ttk.Label(root, text="Sorry, you've tried to sign in too many times, and so too many requests have been made to Garmin.  Take a break, and try again later!", foreground='red', wraplength=300).grid(column=0, row=0, sticky=(N, E, S, W))
root.mainloop()
'''
ShowData(root)
root.mainloop()
'''

root = Tk()

root.title('Garmin Activities Data')

# make notebook
notebook = ttk.Notebook(root)
notebook.grid(column=0, row=0, sticky=(N, W, E, S))
    # frames of notebook
run_frame = ttk.Frame(notebook, padding='12 12 12 12')
run_frame.grid(column=0, row=0, sticky=(N, W, E, S))
notebook.add(run_frame, text='Running')

bike_frame = ttk.Frame(notebook, padding='12 12 12 12')
bike_frame.grid(column=0, row=0, sticky=(N, W, E, S))
notebook.add(bike_frame, text='Biking')

swim_frame = ttk.Frame(notebook, padding='12 12 12 12')
swim_frame.grid(column=0, row=0, sticky=(N, W, E, S))
notebook.add(swim_frame, text='Swimming')

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
notebook.columnconfigure(0, weight=1)
notebook.rowconfigure(0, weight=1)

root.mainloop()
"""
'''
from tkinter import Tk
from tkinterweb import HtmlFrame  # Import HtmlFrame from tkinterweb

import altair as alt
import pandas as pd
import numpy as np

# Initialize Tkinter root window
root = Tk()
root.title('Altair Chart in Tkinter')

# Create the HTML frame
html_frame = HtmlFrame(root)
html_frame.grid(column=0, row=0, sticky=(N, S, E, W))

# Ensure proper resizing behavior
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Generate random data
data = pd.DataFrame({
    'x': np.random.randint(0, 100, 20),
    'y': np.random.randint(0, 100, 20)
})

# Create the Altair chart
chart = alt.Chart(data).mark_circle(size=100).encode(
    x='x',
    y='y',
    color=alt.value('orange'),
).properties(
    title='Randomly Generated Data'
)

# Convert the Altair chart to HTML
chart_html = chart.to_html()

# Debug: Print t

# Load the HTML into the HtmlFrame
html_frame.enable_images(enabled=True)
html_frame.load_html(chart_html)
html_frame.add_html(chart_html)

# Run the Tkinter main loop
root.mainloop()
'''
'''
# create tkinter window
root_tk = Tk()
root_tk.geometry(f"{800}x{600}")
root_tk.title("map_view_example.py")

# create map widget
map_widget = tkintermapview.TkinterMapView(root_tk, width=800, height=600, corner_radius=0)
map_widget.place(relx=0.5, rely=0.5, anchor=CENTER)
map_widget.set_position(g.lat, g.lng)
map_widget.set_zoom(7)
map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
map_widget.set_marker(g.lat, g.lng, marker_color_circle='red', marker_color_outside='red')
root_tk.mainloop()
'''
'''
root = Tk()

sign_in_frame = ttk.Frame(root, padding='12 12 12 12')
sign_in_frame.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

data = {
    'x': [1, 2, 3, 4, 5],
    'y': [10, 20, 30, 40, 50]
}
df = pd.DataFrame(data)

# Create an Altair chart
chart = alt.Chart(df).mark_line().encode(
    x='x',
    y='y'
)

chart = Chart(df.iloc[0:5]).mark_area().encode(
            x=alt.X('x', title='Last Week'),
            y='y',
            color=alt.value('#fc6b03'),
            opacity=alt.value(0.4)
        ) + \
        Chart(df.iloc[0:5]).mark_line().encode(
            x=alt.X('x'),
            y='y',
            color=alt.value('#fc6b03')
        ) + \
        Chart(df.iloc[0:5]).mark_circle().encode(
            x=alt.X('x'),
            y='y',
            color=alt.value('#fc5e03'),
            size=alt.value(50))

photos = dict()
month_png_data = vlc.vegalite_to_png(chart.to_json(), scale=2) # vl_version="5.17.0"
with open("chart.png", "wb") as f:
    f.write(month_png_data)
    # load the image
month_image = Image.open("chart"+"."+"png")
photos['month'] = ImageTk.PhotoImage(month_image)

week_label = Label(root, image=photos['month'])
week_label.grid(column=0, row=0, sticky=(N, W, E, S))

root.mainloop()
'''