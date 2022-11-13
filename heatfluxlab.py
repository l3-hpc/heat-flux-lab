#Alias Pandas as pd, for manipulating tables and timeseries
import pandas as pd
#Alias MatPlotLib at plt, for making plots/graphs/figures
import matplotlib.pyplot as plt
#Alias Numpy as'np', for the arrays
import numpy as np

# write function to calculate change in temperature that receives the inputs Qt, z, and days
def readfile (fname):
    data = pd.read_csv(fname, sep=',', engine='python') 
    return data
    
def checkdata (data):
    return data.head()

def renamecols(df,names):
    df.columns=names
    
#Create timestamp
def maketimestamp(df,timevars):
        return pd.to_datetime(df[timevars])
    
#Check what time period is covered in the dataset.
def checktimerange(Time):
    return (Time.max() - Time.min())

#Calculate change in temperature given time, heat flux, depth, specific heat capacity, and density
def tempchange (Time, Q, z, c, rho):
    timerange = Time.max() - Time.min()
    tsec = timerange.total_seconds()
    Qave = Q.mean()
    strz = str(z)
    stround = str(round((Qave*tsec)/(c*rho*z),2))
    message = "The expected change in temperature for the given heat flux for a water column depth of " + strz + "m is "  + stround + " degrees C"
    return print(message)

#Plot a single variable
def single_plot (xvar, yvar, title, xlabel, ylabel, color):
    #Daily ticks in month-date format for year 2017
    from matplotlib.dates import DayLocator
    from matplotlib.dates import DateFormatter
    date_form = DateFormatter("%m-%d")
    dloc = DayLocator()

    #Make a timeseries plot
    fig1, (ax1) = plt.subplots(1, figsize=(20,3)) #form two rows and one column (2,1) of subplots
    fig1.suptitle(title, fontsize=18, y=1.05)

    #First plot, solar radiation
    ax1.plot(xvar, yvar, color) #main plot
    ax1.axes.get_xaxis().set_ticks([]) #remove dates
    ax1.set_xlim([xvar.min(), xvar.max()]) #x-limits
    ax1.set_ylim([yvar.min(),yvar.max()])   #y-limits
    ax1.legend([ylabel],framealpha=1, fontsize=12)
    ax1.set_ylabel(ylabel,fontsize=14)
    ax1.xaxis.set_major_locator(dloc)
    ax1.grid(color='lightgrey', linestyle='--', linewidth=0.5) #gridlines
    ax1.yaxis.labelpad = 15
    plt.xticks(rotation = 45) 
    ax1.xaxis.labelpad = 20
    
    ax1.xaxis.set_major_formatter(date_form)
    
    plt.show()
    
#Plot all variables in a dataframe
def multi_plot (xvar, yvar,xlabel,ylabel):
#, title, xlabel, ylabel, colors):
    #Make a timeseries plot
    fig1, (ax1) = plt.subplots(1, figsize=(20, 3)) #form two rows and one column (2,1) of subplots
    #Choose which colors will be used automatically for plots
    #First plot, solar radiation
    ax1.plot(xvar, yvar) #main plot
    ax1.set_xlim([Time.min(), Time.max()]) #x-limits
    ax1.set_xlabel(xlabel, fontsize=14)
    ax1.set_ylabel(ylabel, fontsize=14)
    plt.show()
    
#Plot solar radiation, heat flux loss terms, and sea surface temperature
def plotfluxtemp (Time, df, where, when):
    
    #Define Title String
    titlestring = "Data was gathered near " + where + " during " + when +"."
    
    #Define SST and Qin
    sst = df['sst']
    Qin = df['Qin']
    #Define data frame called heatloss containing the last three columns of the data file.
    vars = ['Qb','Qh','Qe']
    heatloss = df[vars]

    #Daily ticks in month-date format for year 2019
    from matplotlib.dates import DayLocator
    from matplotlib.dates import DateFormatter
    date_form = DateFormatter("%m-%d")
    dloc = DayLocator()

    #Choose which colors will be used automatically for plots
    from cycler import cycler
    plt.rc('axes', prop_cycle=(cycler('color', ['black', 'blue', 'grey'])))

    #Make a timeseries plot with heat gain and heat loss terms
    fig1, (ax1, ax2, ax3) = plt.subplots(3,1, figsize=(18, 8)) #form two rows and one column (2,1) of subplots
    fig1.suptitle('\n Magnitude of Heat Flux Terms (W/m$^2$) and Sea Surface Temperature ($^{\circ}$C)', fontsize=18)

    #First plot, solar radiation
    ax1.plot(Time, Qin,'darkred') #main plot
    ax1.axes.get_xaxis().set_ticks([]) #remove dates
    ax1.set_xlim([Time.min(), Time.max()]) #x-limits
    ax1.set_ylim([Qin.min(),Qin.max()+50])   #y-limits
    ax1.legend(['Q$_{in}$  Solar Radiation'],framealpha=1, fontsize=12)
    ax1.set_xticklabels('')
    ax1.minorticks_off()
    ax1.set_ylabel('Heat Gain',fontsize=14)
    ax1.xaxis.set_major_locator(dloc)
    ax1.grid(color='lightgrey', linestyle='--', linewidth=0.5) #gridlines
    ax1.yaxis.labelpad = 15

    #Plot all of the heat loss terms
    ax2.plot(Time, heatloss) #main plot
    ax2.grid(color='lightgrey', linestyle='--', linewidth=0.5)#gridlines
    ax2.set_xlim([Time.min(), Time.max()]) #x-limits
    ax2.set_ylim([heatloss['Qe'].min(),heatloss['Qe'].max()+50]) #y-limits
    ax2.xaxis.set_major_locator(dloc)
    ax2.axes.get_xaxis().set_ticks([]) #remove dates
    plt.xlabel(titlestring, fontsize=16)
    ax2.xaxis.labelpad = 20
    ax2.legend(['Q$_b$  Back Radiation','Q$_h$  Sensible Heat Flux','Q$_e$  Latent Heat Flux'],framealpha=1, fontsize=12)
    ax2.set_xticklabels('')
    ax2.minorticks_off()
    ax2.set_ylabel('Heat Loss', fontsize=14)
    ax2.axes.get_xaxis().set_ticks([]) #remove dates
    ax2.xaxis.set_major_locator(dloc)

    ax2.yaxis.labelpad = 15
    plt.subplots_adjust(hspace=0.01)

    #Third plot, Temperature
    ax3.plot(Time, sst,'darkblue') #main plot
    ax3.axes.get_xaxis().set_ticks([]) #remove dates
    ax3.set_xlim([Time.min(), Time.max()]) #x-limits
    ax3.set_ylim([sst.min()-.25,sst.max()+.25])   #y-limits
    ax3.legend(['SST  Sea Surface Temperature'],framealpha=1, fontsize=12)
    ax3.set_xticklabels('')
    ax3.minorticks_off()
    ax3.set_ylabel('Temperature',fontsize=14)
    ax3.xaxis.set_major_locator(dloc)
    ax3.grid(color='lightgrey', linestyle='--', linewidth=0.5) #gridlines
    ax3.yaxis.labelpad = 20
    ax3.xaxis.set_major_formatter(date_form)
    plt.xticks(rotation = 45) 
    ax3.xaxis.labelpad = 20

    plt.show()
    
#Plot solar radiation, heat flux loss terms, and sea surface temperature
def plotsummary (Time, df):
        
    #Define SST and Qin
    sst = df['sst']
    Qin = df['Qin']
    #Define data frame called heatloss containing the last three columns of the data file.
    vars = ['Qb','Qh','Qe']
    heatloss = df[vars]

    #Ticks in month-date format
    from matplotlib.dates import DayLocator
    from matplotlib.dates import DateFormatter
    date_form = DateFormatter("%m-%d")
    dloc = DayLocator(interval=3)

    #Choose which colors will be used automatically for plots
    from cycler import cycler
    plt.rc('axes', prop_cycle=(cycler('color', ['black', 'royalblue', 'grey'])))

    #Make a timeseries plot with heat gain and heat loss terms
    #, figsize=(18, 8)
    fig1, axes = plt.subplots(3,2,figsize=(30, 15)) #form three rows and two columns (3,2) of subplots
 
    ax1=axes[0,0]
    #First plot, solar radiation
    ax1.plot(Time, Qin,'darkred') #main plot
    ax1.axes.get_xaxis().set_ticks([]) #remove dates
    ax1.set_xlim([Time.min(), Time.max()]) #x-limits
    ax1.set_ylim([Qin.min(),Qin.max()+50])   #y-limits
    ax1.legend(['Q$_{in}$  Solar Radiation'],framealpha=1, fontsize=14)
    ax1.set_xticklabels('')
    ax1.minorticks_off()
    #ax1.set_ylabel('Heat Gain',fontsize=14)
    ax1.xaxis.set_major_locator(dloc)
    ax1.grid(color='lightgrey', linestyle='--', linewidth=0.5) #gridlines
    

    ax2=axes[1,0]
    #Plot all of the heat loss terms
    ax2.plot(Time, heatloss) #main plot
    ax2.grid(color='lightgrey', linestyle='--', linewidth=0.5)#gridlines
    ax2.set_xlim([Time.min(), Time.max()]) #x-limits
    ax2.set_ylim([heatloss['Qe'].min(),heatloss['Qe'].max()+50]) #y-limits
    ax2.xaxis.set_major_locator(dloc)
    ax2.axes.get_xaxis().set_ticks([]) #remove dates
    ax2.legend(['Q$_b$  Back Radiation','Q$_h$  Sensible Heat Flux','Q$_e$  Latent Heat Flux'],framealpha=1, fontsize=14)
    ax2.set_xticklabels('')
    ax2.minorticks_off()
    #ax2.set_ylabel('Heat Loss', fontsize=14)
    ax2.axes.get_xaxis().set_ticks([]) #remove dates
    ax2.xaxis.set_major_locator(dloc)
    plt.subplots_adjust(hspace=0.01,wspace=0)

    ax3=axes[2,0]
    #Third plot, Temperature
    ax3.plot(Time, sst,'darkgreen') #main plot
    ax3.axes.get_xaxis().set_ticks([]) #remove dates
    ax3.set_xlim([Time.min(), Time.max()]) #x-limits
    ax3.set_ylim([sst.min()-.25,sst.max()+.25])   #y-limits
    ax3.legend(['Sea Surface Temperature (SST)'],framealpha=1, fontsize=14)
    ax3.set_xticklabels('',rotation=45)
    ax3.minorticks_off()
    #ax3.set_ylabel('Sea Surface Temperature',fontsize=14)
    ax3.xaxis.set_major_locator(dloc)
    ax3.grid(color='lightgrey', linestyle='--', linewidth=0.5) #gridlines
    ax3.xaxis.set_major_formatter(date_form)
    plt.xticks(rotation = 45) 
    ax3.tick_params(axis='x',labelrotation=45)
    
    
    ax4=axes[0,1]
    #Fourth plot, Wind Speed
    ax4.plot(Time, df['Vm'],'saddlebrown') #main plot
    ax4.axes.get_xaxis().set_ticks([]) #remove dates
    ax4.set_xlim([Time.min(), Time.max()]) #x-limits
    ax4.set_ylim([df['Vm'].min(),df['Vm'].max()])   #y-limits
    ax4.legend(['Wind Speed'],framealpha=1, fontsize=14)
    ax4.set_xticklabels('')
    ax4.minorticks_off()
    #ax4.set_ylabel('Wind Speed',fontsize=14)
    ax4.xaxis.set_major_locator(dloc)
    ax4.grid(color='lightgrey', linestyle='--', linewidth=0.5) #gridlines
    ax4.yaxis.set_label_position("right")
    ax4.yaxis.tick_right()

    ax5=axes[1,1]
    #Fifth plot, Relative Humidity
    ax5.plot(Time, df['RH'],'darkblue') #main plot
    ax5.grid(color='lightgrey', linestyle='--', linewidth=0.5)#gridlines
    ax5.set_xlim([Time.min(), Time.max()]) #x-limits
    ax5.set_ylim(df['RH'].min(),df['RH'].max()) #y-limits
    ax5.xaxis.set_major_locator(dloc)
    ax5.axes.get_xaxis().set_ticks([]) #remove dates
    ax5.legend(['Relative Humidity'],framealpha=1, fontsize=14)
    ax5.set_xticklabels('')
    ax5.minorticks_off()
    #ax5.set_ylabel('Relative Humidity', fontsize=14)
    ax5.axes.get_xaxis().set_ticks([]) #remove dates
    ax5.xaxis.set_major_locator(dloc)
    plt.subplots_adjust(hspace=0.01)
    ax5.yaxis.set_label_position("right")
    ax5.yaxis.tick_right()

    ax6=axes[2,1]
    #Sixth plot, Difference in Air and Water temperature
    diffairtemp = df['Vm']-df['sst']
    ax6.plot(Time, diffairtemp,'indigo') #main plot
    ax6.axes.get_xaxis().set_ticks([]) #remove dates
    ax6.set_xlim([Time.min(), Time.max()]) #x-limits
    ax6.set_ylim([diffairtemp.min(),diffairtemp.max()])   #y-limits
    ax6.legend(['Air-Sea Temperature Difference'],framealpha=1, fontsize=14)
    ax6.set_xticklabels('')
    ax6.minorticks_off()
    #ax6.set_ylabel('Air-Water Temperature$',fontsize=14)
    ax6.xaxis.set_major_locator(dloc)
    ax6.grid(color='lightgrey', linestyle='--', linewidth=0.5) #gridlines
    ax6.xaxis.set_major_formatter(date_form)
    plt.xticks(rotation = 45) 
    ax6.yaxis.set_label_position("right")
    ax6.yaxis.tick_right()
       
    plt.show()
