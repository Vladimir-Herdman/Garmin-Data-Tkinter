from tkinter import *
from tkinter import ttk

import pandas as pd

import altair as alt
from altair import Chart

import vl_convert as vlc
from PIL import Image, ImageTk
from pathlib import Path
from io import BytesIO

import folium
from folium.plugins import HeatMap
import tkintermapview
from geocoder import ip


class ShowData:
    def __init__(self, root, all_activities, today):

        self.today = today
        self.location = ip("me")

        self.photos = dict()
        self.photo_paths = list()
        
        self.root = root
        self.root.title('Garmin Activities Data')
        self.root.option_add('*tearOff', FALSE)

        # create menu bar
        menubar = Menu(self.root)
        self.root['menu'] = menubar
            # add menu
        menu_themes = Menu(menubar)
        menubar.add_cascade(menu=menu_themes, label='Theme')
            # add item to theme
        check = BooleanVar()
        menu_themes.add_checkbutton(label='Dark Mode', variable=check, onvalue=1, offvalue=0, command=self.dark_mode_func)


        # make canvas so scroll wheel can be added
        canvas_back = Canvas(self.root, bg='#3a3b3c')
        canvas_back.grid(column=0, row=0, sticky=(N, W, E, S))
            # scroll wheel
        scroll_bar_canvas = ttk.Scrollbar(self.root, orient=VERTICAL, command=canvas_back.yview)
        scroll_bar_canvas.grid(column=1, row=0, sticky=(N, S))
        canvas_back['yscrollcommand'] = scroll_bar_canvas.set
            # scrollable frame inside canvas for all other widgets to be placed inside of
        scrollable_frame = ttk.Frame(canvas_back)
        scrollable_frame.columnconfigure(0, weight=1)
        scrollable_frame.rowconfigure(0, weight=1)
        canvas_back.create_window((0, 0), window=scrollable_frame, anchor="nw")
        scrollable_frame.bind("<Configure>", lambda e: canvas_back.configure(scrollregion=canvas_back.bbox("all")))

        # make notebook
        notebook = ttk.Notebook(scrollable_frame)
        notebook.grid(column=0, row=0, sticky=(N, W, E, S))
            # frames of notebook
                # run
        self.run_frame = ttk.Frame(notebook, padding='12 12 12 12')
        #self.run_frame.grid(column=0, row=0, sticky=(N, W, E, S))
        notebook.add(self.run_frame, text='Running')

                # bike
        self.bike_frame = ttk.Frame(notebook, padding='12 12 12 12')
        #self.bike_frame.grid(column=0, row=0, sticky=(N, W, E, S))
        notebook.add(self.bike_frame, text='Biking')

                # swim
        self.swim_frame = ttk.Frame(notebook, padding='12 12 12 12')
        #self.swim_frame.grid(column=0, row=0, sticky=(N, W, E, S))
        notebook.add(self.swim_frame, text='Swimming')

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        canvas_back.columnconfigure(0, weight=1)
        canvas_back.rowconfigure(0, weight=1)
        notebook.columnconfigure(0, weight=1)
        notebook.rowconfigure(0, weight=1)

        # data variables (do these dataframes actually have data we need to show?)
        self.run_data = BooleanVar(value=True)
        self.bike_data = BooleanVar(value=True)
        self.swim_data = BooleanVar(value=True)

        # create all pandas dataframes to use
        self.run_df, self.bike_df, self.swim_df = self.create_all_dfs(all_activities)

        # add graphs frames to run, bike, and swim frames if data in them
        if self.run_data:
            self.data_over_time(self.run_frame, self.run_df, 'run')
            self.create_activity_map(self.run_frame, self.run_df)
            self.create_activity_heatmap(self.run_frame, self.run_df)
            if self.run_df.shape[0] > 3:
                self.place_data_records(self.run_frame, self.run_df)
        else:
            self.no_data(self.run_frame, 'run')

        if self.bike_data:
            self.data_over_time(self.bike_frame, self.bike_df, 'bike')
            self.create_activity_map(self.bike_frame, self.bike_df)
            self.create_activity_heatmap(self.bike_frame, self.bike_df)
            if self.bike_df.shape[0] > 3:
                self.place_data_records(self.bike_frame, self.bike_df)
        else:
            self.no_data(self.bike_frame, 'bike')

        if self.swim_data:
            self.data_over_time(self.swim_frame, self.swim_df, 'swim')
            self.create_activity_map(self.swim_frame, self.swim_df)
            self.create_activity_heatmap(self.swim_frame, self.swim_df)
            if self.swim_df.shape[0] > 3:
                self.place_data_records(self.swim_frame, self.swim_df)
        else:
            self.no_data(self.swim_frame, 'swim')

        # run program on window close
        self.root.protocol("WM_DELETE_WINDOW", self.window_close_func)

        # size correction
        self.root.geometry("1200x800")

    def place_data_records(self, frame, df):
        """
        Places the records of the time last week, 
        month, year time frames
        """
        last_week = 6
        last_month = 29
        last_year = 364

        font_basic = ("Courier", 15)

        week_frame = Frame(frame, bg="#ccb1b1")
        week_frame.grid(column=1, row=0, sticky=(N, E, S, W), padx=24, pady=24)
        week_df = df.iloc[0:last_week]
        total = week_df["miles"].sum()
        maximum = week_df["miles"].max()
        avg = round(week_df["miles"].mean(), 3)
        double_days = week_df[week_df["times"] > 1]["times"].count()
        full_text = f"\nTotal Miles:  {total} {"miles" if total != 1 else "mile"}\n\nDouble Days:  {double_days}\n\nHighest In one Day:  {maximum}\n\nAverage Every Day:  {avg}"
        week_label = Label(week_frame, bg="#ccb1b1", font=font_basic, text=full_text)
        week_label.grid(column=0, row=0, sticky=(W, E), padx=12, pady=12)

        month_frame = Frame(frame, bg="#ccb1b1")
        month_frame.grid(column=1, row=2, sticky=(N, E, S, W), padx=24, pady=24)
        month_df = df.iloc[0:last_month]
        total = month_df["miles"].sum()
        maximum = month_df["miles"].max()
        avg = round(month_df["miles"].mean(), 3)
        double_days = month_df[month_df["times"] > 1]["times"].count()
        full_text = f"\nTotal Miles:  {total} {"miles" if total != 1 else "mile"}\n\nDouble Days:  {double_days}\n\nHighest In one Day:  {maximum}\n\nAverage Every Day:  {avg}"
        month_label = Label(month_frame, bg="#ccb1b1", font=font_basic, text=full_text)
        month_label.grid(column=0, row=0, sticky=(W, E), padx=12, pady=12)

        year_frame = Frame(frame, bg="#ccb1b1")
        year_frame.grid(column=1, row=4, sticky=(N, E, S, W), padx=24, pady=24)
        year_df = df.iloc[0:last_year]
        total = year_df["miles"].sum()
        maximum = year_df["miles"].max()
        avg = round(year_df["miles"].mean(), 3)
        double_days = year_df[year_df["times"] > 1]["times"].count()
        full_text = f"\nTotal Miles:  {total} {"miles" if total != 1 else "mile"}\n\nDouble Days:  {double_days}\n\nHighest In one Day:  {maximum}\n\nAverage Every Day:  {avg}"
        year_label = Label(year_frame, bg="#ccb1b1", font=font_basic, text=full_text)
        year_label.grid(column=0, row=0, sticky=(W, E), padx=12, pady=12)
    
    def create_all_dfs(self, activities):
        # set up lists for data being taken
        dates = list()
        avgHR = list()
        miles = list()
        location = list()
        activity_type = list()
        times_activity_done = list()

        # get data and put into lists
        for activity in activities:
            if any(x in activity['activityType']['typeKey'] for x in ('run', 'cycling', 'swim')):
                dates.append(activity['startTimeGMT'].split()[0])
                try:
                    avgHR.append(activity['averageHR'])
                except KeyError:
                    avgHR.append(145.0)
                miles.append(round(activity['distance'] / 1600, 3))
                activity_type.append(activity['activityType']['typeKey'])
                times_activity_done.append(1)
                try:
                    location.append([activity['startLatitude'], activity['startLongitude']])
                except KeyError:
                    location.append([0, 0])

        # make the dates an actual date data-type and set as index
        all_df = pd.DataFrame({'date': dates, 'activity': activity_type, 'times': times_activity_done, 'miles': miles, 'avgHR': avgHR, 'loc': location})
        all_df['date'] = pd.to_datetime(all_df['date'])
        all_df.set_index('date', inplace=True)

        # rename activities
        all_df['activity'] = all_df['activity'].apply(lambda activity: 'running' if 'run' in activity else ('biking' if 'cycling' in activity else ('swim' if 'swim' in activity else 'other')))

        # seperate into seperate df's
        run_df = all_df[all_df['activity'] == 'running']
        bike_df = all_df[all_df['activity'] == 'biking']
        swim_df = all_df[all_df['activity'] == 'swim']
            # check if actual data in that dataframe
        if run_df.shape[0] == 0:
            self.run_data = False
            self.run_df = None
        if bike_df.shape[0] == 0:
            self.nike_data = False
            self.bike_df = None
        if swim_df.shape[0] == 0:
            self.swim_data = False
            self.swim_df = None

        # clean up each dataframe, if data actually in that dataframe
            # running
        clean_dates_series = pd.date_range('2003-08-14', self.today)
        if self.run_data:
            run_df = run_df.groupby(run_df.index).agg({'times': 'sum', 'miles': 'sum', 'avgHR': 'mean', 'loc': 'first'})
            run_df['avgHR'] = run_df['avgHR'].round(3)
            run_df = run_df.reset_index()
                # clean up missing values
            run_df = run_df.sort_values(by='date', ascending=True)
            run_df.index = pd.DatetimeIndex(run_df['date'])
            run_df = run_df.reindex(clean_dates_series, fill_value=0)
            run_df = run_df.reset_index()
            run_df.rename(columns={'date': 'remove', 'index': 'date'}, inplace=True)
            run_df = run_df.drop('remove', axis=1)
            run_df.sort_values(by='date', ascending=False, inplace=True)
            # biking
        if self.bike_data:
            bike_df = bike_df.groupby(bike_df.index).agg({'times': 'sum', 'miles': 'sum', 'avgHR': 'mean', 'loc': 'first'})
            bike_df['avgHR'] = bike_df['avgHR'].round(3)
            bike_df = bike_df.reset_index()
                # clean up missing values
            bike_df = bike_df.sort_values(by='date', ascending=True)
            bike_df.index = pd.DatetimeIndex(bike_df['date'])
            bike_df = bike_df.reindex(clean_dates_series, fill_value=0)
            bike_df = bike_df.reset_index()
            bike_df.rename(columns={'date': 'remove', 'index': 'date'}, inplace=True)
            bike_df = bike_df.drop('remove', axis=1)
            bike_df.sort_values(by='date', ascending=False, inplace=True)
            # swimming
        if self.swim_data:
            swim_df = swim_df.groupby(swim_df.index).agg({'times': 'sum', 'miles': 'sum', 'avgHR': 'mean', 'loc': 'first'})
            swim_df['avgHR'] = swim_df['avgHR'].round(3)
            swim_df = swim_df.reset_index()
                # clean up missing values
            swim_df = swim_df.sort_values(by='date', ascending=True)
            swim_df.index = pd.DatetimeIndex(swim_df['date'])
            swim_df = swim_df.reindex(clean_dates_series, fill_value=0)
            swim_df = swim_df.reset_index()
            swim_df.rename(columns={'date': 'remove', 'index': 'date'}, inplace=True)
            swim_df = swim_df.drop('remove', axis=1)
            swim_df.sort_values(by='date', ascending=False, inplace=True)

        # return created dataframes
        return run_df, bike_df, swim_df
    
    def data_over_time(self, frame, df, specializer):
        """
        Will generate the charts of the last year, 
        month, and year, then add it to frame
        """
        # variables for remembering dates
        last_week = 6
        last_month = 29
        last_year = 364

        # color based on activity
        colors = {
            "run": "#fc6b03",
            "bike": "#eb6157",
            "swim": "#4da3d1"
        }

        # last week
            # make the chart
        week_chart = Chart(df.iloc[0:last_week]).mark_area().encode(
            x=alt.X('date', title='Last Week'),
            y='miles',
            color=alt.value(colors[specializer]),
            opacity=alt.value(0.4)
        ) + \
        Chart(df.iloc[0:last_week]).mark_line().encode(
            x=alt.X('date'),
            y='miles',
            color=alt.value(colors[specializer])
        ) + \
        Chart(df.iloc[0:last_week]).mark_circle().encode(
            x=alt.X('date'),
            y='miles',
            color=alt.value(colors[specializer]),
            size=alt.value(50))
            # save chart as a PNG image
        week_png_data = vlc.vegalite_to_png(week_chart.to_json(), scale=2) # vl_version="5.17.0"
        with open("chart0_"+specializer+".png", "wb") as f:
            f.write(week_png_data)
            # load the image
        week_image = Image.open("chart0_"+specializer+".png")
        week_image = week_image.resize((570, 450), Image.Resampling.LANCZOS)
        self.photo_paths.append("chart0_"+specializer+".png")
        self.photos['week'+specializer] = ImageTk.PhotoImage(week_image)
            # display inage in frame
        week_label = Label(frame, image=self.photos['week'+specializer])
        week_label.photo = self.photos['week'+specializer]  # This line here is the single error that kept me up at night.  I do not understand it, but it makes the graphs show up in the frame
        week_label.grid(column=0, row=0, sticky=(N, W, E, S))

        # last month
            # make the chart
        month_chart = Chart(df.iloc[0:last_month]).mark_area().encode(
            x=alt.X('date', title='Last Month'),
            y='miles',
            color=alt.value(colors[specializer]),
            opacity=alt.value(0.4)
        ) + \
        Chart(df.iloc[0:last_month]).mark_line().encode(
            x=alt.X('date'),
            y='miles',
            color=alt.value(colors[specializer])
        ) + \
        Chart(df.iloc[0:last_month]).mark_circle().encode(
            x=alt.X('date'),
            y='miles',
            color=alt.value(colors[specializer]),
            size=alt.value(50))
            # save chart as a PNG image
        month_png_data = vlc.vegalite_to_png(month_chart.to_json(), scale=2) # vl_version="5.17.0"
        with open("chart1_"+specializer+".png", "wb") as f:
            f.write(month_png_data)
            # load the image
        month_image = Image.open("chart1_"+specializer+".png")
        month_image = month_image.resize((570, 450), Image.Resampling.LANCZOS)
        self.photo_paths.append("chart1_"+specializer+".png")
        self.photos['month'+specializer] = ImageTk.PhotoImage(month_image)
            # display inage in frame
        month_label = Label(frame, image=self.photos['month'+specializer])
        month_label.photo = self.photos['month'+specializer]
        month_label.grid(column=0, row=2, sticky=(N, W, E, S))

        # last year
            # make the chart
        year_chart = Chart(df.iloc[0:last_year]).mark_area().encode(
            x=alt.X('date', title='Last Year'),
            y='miles',
            color=alt.value(colors[specializer]),
            opacity=alt.value(0.4)
        ) + \
        Chart(df.iloc[0:last_year]).mark_line().encode(
            x=alt.X('date'),
            y='miles',
            color=alt.value(colors[specializer]))
            # save chart as a PNG image
        year_png_data = vlc.vegalite_to_png(year_chart.to_json(), scale=2) # vl_version="5.17.0"
        with open("chart2_"+specializer+".png", "wb") as f:
            f.write(year_png_data)
            # load the image
        year_image = Image.open("chart2_"+specializer+".png")
        year_image = year_image.resize((570, 450), Image.Resampling.LANCZOS)
        self.photo_paths.append("chart2_"+specializer+".png")
        self.photos['year'+specializer] = ImageTk.PhotoImage(year_image)
            # display inage in frame
        year_label = Label(frame, image=self.photos['year'+specializer])
        year_label.photo = self.photos['year'+specializer]
        year_label.grid(column=0, row=4, sticky=(N, W, E, S))

        frame.update_idletasks()

    def no_data(self, frame, activity):
        """
        No data in the dataframe, so simply write 
        out no such data found over all time, and
        put into tkinter frame for that activity

        Parameters:
        activity (str): a string representation of the activity that had no data found, so it can be specified in the error message
        """
        ttk.Label(frame, text=f"There was no {activity} data found in your garmin accounts records. Are you sure you've ever even done this? Huh? Have you?", foreground='red', wraplength=300).grid(column=0, row=0, sticky=(N, E, S, W))

    def create_activity_map(self, frame, df):
        """
        Will generate the map off all the location data,
        creating points for every activity started
        """
        # get location (lat, lng)

        # make map widget
        map_widget = tkintermapview.TkinterMapView(frame, width=600, height=450, corner_radius=0)
        map_widget.grid(column=0, row=6, sticky=(N, W, E, S))
        map_widget.set_position(self.location.lat, self.location.lng)
        map_widget.set_zoom(6)
        map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

        # clean_df to get rid of zeros
        clean_df = df[df['loc'].apply(lambda x: x != 0 and x != [0, 0])]
        
        # add markers for activity
        for loc in clean_df['loc']:
            map_widget.set_marker(loc[0], loc[1], marker_color_circle='red', marker_color_outside='red')

        frame.update_idletasks()

    def create_activity_heatmap(self, frame, df):
        """
        Creates a folium heat map PNG of your 
        activities and where you do them most 
        based around where you currently are
        """
        coordinates_list = df[df['loc'].apply(lambda x: x != 0 and x != [0, 0])]['loc'].to_list()

        map = folium.Map(location=(self.location.lat, self.location.lng), zoom_start=6, tiles="cartodb positron")
        heatmap = HeatMap(coordinates_list, radius=15, blur=10, min_opacity=0.4)
        map.add_child(heatmap)

        # save folium map as a PNG
        img_data = map._to_png(1)
        img = Image.open(BytesIO(img_data))
        img = img.resize((800, 550), Image.Resampling.LANCZOS)
        self.photos['folium_map'] = ImageTk.PhotoImage(img)

        # add map to frame
        folium_label = Label(frame, image=self.photos['folium_map'])
        folium_label.photo = self.photos['folium_map']
        folium_label.grid(column=0, row=7, sticky=(N, W, E, S))

    def dark_mode_func(self):
        pass
    
    def window_close_func(self):
        """
        Get rid of the PNG's no longer needed
        on window close
        """
        try:
            for png in self.photo_paths:
                    Path(png).unlink()
            self.root.destroy()
        except Exception as e:
            print(e)