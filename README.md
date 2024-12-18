# PSI_2022

How to run CrossTalk_Plotter.py, 
1) Make sure that positions and channelPositions are set to the specific detector you're working with.
2) In the dictionary function, (should be first function), make sure that you have in the dictionary a list of all voltage values in the given series of Runs you are working with, e.g., if you have runs with voltages 100V, 150V, and 210V make sure you have a dictionary for each of those voltages, e.g., 
'100V':[],
'150V':[],
'210V':[]
3) Similarly, in the voltage_averages function, copy the previous dictionary you just made into the dictionary labeled as voltageIndexValues.
4) In the same function find the pmaxValues named variable which is a list, in this list designate the specific variables you are looking for, e.g., pmax## or riseTime##, where ## is some channel number.
5) Change the nunmber of entries after the voltage_averages function, I recommend starting at around 500-1000 to make sure everything works right first, since larger numbers take a long time to run.
6) In the plot_regular function make changes to the x-axis, y-axis, title, and file name to fit the specific varaiables your plotting. You can also change the coloring schema and the markers here if you wish.
7) Making sure that the entries are set to a relativly low value (500-1000), run the file in the terminal with Python3 CrossTalk_Plotter.py, after which you should see a .png generated, check the .png and make sure it looks like what you expected.
8) If the .png is correct, then go back into the .py file and change the entries to 100000, (100,000 is typically the number of entries in a Run) and run the .py file in the terminal again. WARNING running the file with entires set to around 100,000 will take a few minutes to maybe an hour. Make sure everything is perfect beforing fully running it.



How to run MultiWaveFormPlotter.py,
1) Insert name of specific run you are interested in in line 7, 
2) Make sure the senor channle is correct in line 9,
3) Set the trip_nebh values to the specific channles you are interested in plotting,
3) always make sure the number of colors matches the number of channels OPTIONAL Make changes to the color if you wish,
4) Change the entry value on line 20 to the specific entry you are interested in,
5) Run the MultiWaveFormPlotter.py file




