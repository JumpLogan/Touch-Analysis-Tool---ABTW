#!/usr/bin/python
          # -*- coding: latin-1 -*-
#!/usr/bin/env python
"""
Use this program to convert CSV touch data into a graphic which indicates what events were recognized at which location.
Generates connecting lines between consecutive events
"""
from sys import argv
from os import path
import collections
import csv
import matplotlib
import pylab as pl
import numpy as np
from numpy import arange, pi, cos, sin, pi
from numpy.random import rand
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.pyplot import figure, show
from matplotlib.backends.backend_pdf import PdfPages

# create empty list
#CSVEvents
CSVEvents =  np.asarray([[0,0,0,'#ffffff','0.0','',0,  0,0,0,'#ffffff','0.0','',0,  0,0,0,'#ffffff','0.0','',0,  0,0,0,'#ffffff','0.0','',0,  0,0,0,'#ffffff','0.0','',0,  0,0,0,'#ffffff','0.0','',0,  0,0,0,'#ffffff','0.0','',0,  0,0,0,'#ffffff','0.0','',0,  0,0,0,'#ffffff','0.0','',0,  0,0,0,'#ffffff','0.0','',0]])
EmptyEvent = np.asarray([[0,0,0,'#ffffff','0.0','',0,  0,0,0,'#ffffff','0.0','',0,  0,0,0,'#ffffff','0.0','',0,  0,0,0,'#ffffff','0.0','',0,  0,0,0,'#ffffff','0.0','',0,  0,0,0,'#ffffff','0.0','',0,  0,0,0,'#ffffff','0.0','',0,  0,0,0,'#ffffff','0.0','',0,  0,0,0,'#ffffff','0.0','',0,  0,0,0,'#ffffff','0.0','',0]])
IntValsX = []
IntValsY = []
EventTypeCnt = np.asarray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 ]) # counters for 1st finger hover/hover(release)/press/move/release, 2nd finger hover/hover(release)/press/move/release,

Frequency_X = np.zeros(1024) # create array of counters for each axis - will help identifying stacked events in ghosting analysis
Frequency_Y = np.zeros(1024)
Frequency_HX = np.zeros(1024) # same for hovering
Frequency_HY = np.zeros(1024)
Frequency_c = np.zeros(1024) # just an array to hold the corresponding coordinate. Will be filled with 0,1,2,3,4,5...
for cnt in range(0, 1023): 
    Frequency_c[cnt] = cnt
FMinX = 1023 # prepare border indicators for plotting
FMaxX = 0
FMinY = 1023
FMaxY = 0
FMinHX = 1023 # same for hovering
FMaxHX = 0
FMinHY = 1023
FMaxHY = 0
# check if parameter is correct
#CSV_filename = "testdata.csv"
if (len(argv) == 1):
    print ("No filename given, using testdata.csv as default")
    CSV_filename = "testdata.csv"
else: 
    if not (path.isfile(argv[1])):
        print ("Filename/path: Not found.[" + argv[1] + "]  Using default data")
    else:
        CSV_filename = argv[1]
    # end if
#end if

first = 1
eCnt = 0
#GraphElem = collections.namedtuple('GraphElem','x,y,dx,dy,color,alpha,symb,evtp,size,scrap')
GraphElem = collections.namedtuple('GraphElem','x1,y1,z1,c1,a1,s1,si1,x2,y2,z2,c2,a2,s2,si2,x3,y3,z3,c3,a3,s3,si3,x4,y4,z4,c4,a4,s4,si4,x5,y5,z5,c5,a5,s5,si5,x6,y6,z6,c6,a6,s6,si6,x7,y7,z7,c7,a7,s7,si7,x8,y8,z8,c8,a8,s8,si8,x9,y9,z9,c9,a9,s9,si9,x10,y10,z10,c10,a10,s10,si10,scrap')
for elem in map(GraphElem._make, csv.reader(open(CSV_filename, newline=''))):
    CSVEvents[eCnt,0] = int(elem.x1)
    IntValsX    = np.append(IntValsX,int(elem.x1))
    CSVEvents[eCnt,1] = int(elem.y1)
    IntValsY    = np.append(IntValsY,int(elem.y1))
    CSVEvents[eCnt,2] = int(elem.z1)
    CSVEvents[eCnt,3] = elem.c1
    CSVEvents[eCnt,4] = elem.a1
    CSVEvents[eCnt,5] = elem.s1
    CSVEvents[eCnt,6] = elem.si1
    CSVEvents[eCnt,7] = int(elem.x2)
    CSVEvents[eCnt,8] = int(elem.y2)
    CSVEvents[eCnt,9] = int(elem.z2)
    CSVEvents[eCnt,10] = elem.c2
    CSVEvents[eCnt,11] = elem.a2
    CSVEvents[eCnt,12] = elem.s2
    CSVEvents[eCnt,13] = elem.si2
    CSVEvents[eCnt,14] = int(elem.x3)
    CSVEvents[eCnt,15] = int(elem.y3)
    CSVEvents[eCnt,16] = int(elem.z3)
    CSVEvents[eCnt,17] = elem.c3
    CSVEvents[eCnt,18] = elem.a3
    CSVEvents[eCnt,19] = elem.s3
    CSVEvents[eCnt,20] = elem.si3
    CSVEvents[eCnt,21] = int(elem.x4)
    CSVEvents[eCnt,22] = int(elem.y4)
    CSVEvents[eCnt,23] = int(elem.z4)
    CSVEvents[eCnt,24] = elem.c4
    CSVEvents[eCnt,25] = elem.a4
    CSVEvents[eCnt,26] = elem.s4
    CSVEvents[eCnt,27] = elem.si4
    CSVEvents[eCnt,28] = int(elem.x5)
    CSVEvents[eCnt,29] = int(elem.y5)
    CSVEvents[eCnt,30] = int(elem.z5)
    CSVEvents[eCnt,31] = elem.c5
    CSVEvents[eCnt,32] = elem.a5
    CSVEvents[eCnt,33] = elem.s5
    CSVEvents[eCnt,34] = elem.si5
    CSVEvents[eCnt,35] = int(elem.x6)
    CSVEvents[eCnt,36] = int(elem.y6)
    CSVEvents[eCnt,37] = int(elem.z6)
    CSVEvents[eCnt,38] = elem.c6
    CSVEvents[eCnt,39] = elem.a6
    CSVEvents[eCnt,40] = elem.s6
    CSVEvents[eCnt,41] = elem.si6
    CSVEvents[eCnt,42] = int(elem.x7)
    CSVEvents[eCnt,43] = int(elem.y7)
    CSVEvents[eCnt,44] = int(elem.z7)
    CSVEvents[eCnt,45] = elem.c7
    CSVEvents[eCnt,46] = elem.a7
    CSVEvents[eCnt,47] = elem.s7
    CSVEvents[eCnt,48] = elem.si7
    CSVEvents[eCnt,49] = int(elem.x8)
    CSVEvents[eCnt,50] = int(elem.y8)
    CSVEvents[eCnt,51] = int(elem.z8)
    CSVEvents[eCnt,52] = elem.c8
    CSVEvents[eCnt,53] = elem.a8
    CSVEvents[eCnt,54] = elem.s8
    CSVEvents[eCnt,55] = elem.si8
    CSVEvents[eCnt,56] = int(elem.x9)
    CSVEvents[eCnt,57] = int(elem.y9)
    CSVEvents[eCnt,58] = int(elem.z9)
    CSVEvents[eCnt,59] = elem.c9
    CSVEvents[eCnt,60] = elem.a9
    CSVEvents[eCnt,61] = elem.s9
    CSVEvents[eCnt,62] = elem.si9
    CSVEvents[eCnt,63] = int(elem.x10)
    CSVEvents[eCnt,64] = int(elem.y10)
    CSVEvents[eCnt,65] = int(elem.z10)
    CSVEvents[eCnt,66] = elem.c10
    CSVEvents[eCnt,67] = elem.a10
    CSVEvents[eCnt,68] = elem.s10
    CSVEvents[eCnt,69] = elem.si10
    CSVEvents = np.append(CSVEvents,EmptyEvent,axis = 0)
    #print(CSVEvents)
    #print(eCnt)
    for fid in range(0, 9):
        xloc = 7*fid+0
        yloc = 7*fid+1
        zloc = 7*fid+2
        if (int(CSVEvents[eCnt,zloc])>252):
            EventTypeCnt[int(CSVEvents[eCnt,zloc])-251+fid*5] += 1 # add press / move / release
            Frequency_X[int(CSVEvents[eCnt,xloc])] += 1
            Frequency_Y[int(CSVEvents[eCnt,yloc])] += 1
            if (int(CSVEvents[eCnt,7*fid+0])<FMinX):
                FMinX = int(CSVEvents[eCnt,xloc])
            if (int(CSVEvents[eCnt,7*fid+0])>FMaxX):
                FMaxX = int(CSVEvents[eCnt,xloc])
            if (int(CSVEvents[eCnt,7*fid+1])<FMinY):
                FMinY = int(CSVEvents[eCnt,yloc])
            if (int(CSVEvents[eCnt,7*fid+1])>FMaxY):
                FMaxY = int(CSVEvents[eCnt,yloc])
        elif ((int(CSVEvents[eCnt,zloc])>99) and (int(CSVEvents[eCnt,zloc])<200)):
            EventTypeCnt[fid*5] += 1 # add hover
            Frequency_HX[int(CSVEvents[eCnt,xloc])] += 1
            Frequency_HY[int(CSVEvents[eCnt,yloc])] += 1
            if (int(CSVEvents[eCnt,7*fid+0])<FMinHX):
                FMinHX = int(CSVEvents[eCnt,xloc])
            if (int(CSVEvents[eCnt,7*fid+0])>FMaxHX):
                FMaxHX = int(CSVEvents[eCnt,xloc])
            if (int(CSVEvents[eCnt,7*fid+1])<FMinHY):
                FMinHY = int(CSVEvents[eCnt,yloc])
            if (int(CSVEvents[eCnt,7*fid+1])>FMaxHY):
                FMaxHY = int(CSVEvents[eCnt,yloc])
        elif (int(CSVEvents[eCnt,zloc])==200):
            EventTypeCnt[1+fid*5] += 1 # add hover(release)
            Frequency_HX[int(CSVEvents[eCnt,xloc])] += 1
            Frequency_HY[int(CSVEvents[eCnt,yloc])] += 1
            if (int(CSVEvents[eCnt,7*fid+0])<FMinHX):
                FMinHX = int(CSVEvents[eCnt,xloc])
            if (int(CSVEvents[eCnt,7*fid+0])>FMaxHX):
                FMaxHX = int(CSVEvents[eCnt,xloc])
            if (int(CSVEvents[eCnt,7*fid+1])<FMinHY):
                FMinHY = int(CSVEvents[eCnt,yloc])
            if (int(CSVEvents[eCnt,7*fid+1])>FMaxHY):
                FMaxHY = int(CSVEvents[eCnt,yloc])
    # end if

    eCnt = eCnt + 1

print (EventTypeCnt)
# used only for connecting lines
Events_x = CSVEvents[:eCnt-1,0]
#print (Events_x)
Events_y = CSVEvents[:eCnt-1,1]
#print (Events_y)
MaxX = np.amax(IntValsX)
#print (MaxX)
MinX = np.amin(IntValsX)
#print (MinX)
MaxY = np.amax(IntValsY)
#print (MaxY)
MinY = np.amin(IntValsY)
#print (MinY)
#Events_dx = CSVEvents[:,2]
#Events_dy = CSVEvents[:,3]
#Events_col = CSVEvents[0:9,4]
#Events_sym = CSVEvents[0:9,6]
#print (Events_dx)
#print (Events_dy)
#print (Events_col)
#print (Events_sym)

#prepare grid for contour plot

#delta = 4
x_range = np.arange(0,100, 1)
y_range = np.arange(0,100, 1)
##Z       = np.meshgrid(x_range,y_range)
#
#hlpr = np.zeros((np.size(x_range),np.size(y_range)))
#
##precheck for data errors
NumOfPts = len(CSVEvents)
#pt_errors = np.zeros(NumOfPts)
#loc_tria = np.zeros((3,3))
#pt_cnt   = 2
pt_error = 0
#
##prepare map
z = np.zeros((np.size(x_range),np.size(y_range)))

# start painting:
#print("start painting")
fig = plt.figure()

# ***************************************************
# ***************************************************
ToutL = np.asarray([[0, 0 ],
				    [0, 999 ],  
				    [599, 0 ],  
				    [599, 999 ]])

#pt_error = 0
if (pt_error == 0):
    im = plt.imshow(z, interpolation='bilinear', origin='lower',
                #cmap=cm.spectral, extent=(xyz[0,0],xyz[1,0],xyz[0,1],xyz[1,1]),
                #cmap=cm.spectral, extent=(ToutL[0,1],ToutL[1,1],ToutL[2,0],ToutL[3,0]),
                #cmap=cm.spectral, extent=(ToutL[0,1],ToutL[3,1],ToutL[3,0],ToutL[0,0]),
                cmap=cm.spectral, extent=(MinX,MaxX+150,MaxY+50,MinY),
                #cmap=cm.spectral, extent=(0,1279,639,0),
                alpha=0.0) # alpha = 0.0 => invisible background
#end if
    
# ***************************************************
ax = fig.add_subplot(111)
ax.grid()

# define contour levels
levels = np.arange(-0.00, 2.00, 0.1)
# paint contours
# ***************************************************
pt_error = 1
if (pt_error == 0):
    CS = plt.contour(z,levels, colors=('#661111','#116611'),
                 origin='lower',
                 linewidths=1,
                 extent=(xyz[0,0],xyz[1,0],xyz[0,1],xyz[1,1]))
#end if
# ***************************************************
# add labels to contours
# ***************************************************
if (pt_error == 0):
    plt.clabel(CS, levels[1::1],  # label every second level
           inline=1,
           fmt='%1.2f',
           fontsize=10)
#end if
# ***************************************************
# make a colorbar for the contour lines
# ***************************************************
#CB = plt.colorbar(CS, shrink=0.8, extend='both')

# ***************************************************
# make a colorbar for the background map
# ***************************************************
#CBI = plt.colorbar(im, orientation='horizontal', shrink=0.8)
pt_error = 0
#if (pt_error == 0):
#    CBI = plt.colorbar(im)
#end if
# ***************************************************
# plot mesh of triangles
# ***************************************************
#tri = plt.triplot(x,y,triangles)

# ***************************************************
# Punkte kennzeichnen
# ***************************************************
# unit area ellipse
rx, ry = 3., 3.
area = rx * ry * 3.1415
theta = np.arange(0, 2*3.1415+0.01, 0.1)
s = 300
#c = 'white'
#sc = plt.scatter(x,y,s,c='white')

#ax.plot(x,y, '-o', ms=20, lw=0, alpha=1.0, mfc='white')
#LegOriX = 600
#LegOriY = 20

hover0,   = plt.plot([0,1],[0,0],'ko',ls=(0,(2,3,2,3,5,3,8,3)),ms=3, lw=1, alpha=0.8,mfc='#ffffff',mec='#003399')
hovrel0,  = plt.plot([0,1],[0,0],'ko',ls=(0,(2,3,2,3,5,3,8,3)),ms=7, lw=1, alpha=0.8,mfc='#ffffff',mec='#aa3300')
press0,   = plt.plot([0,1],[0,0],'ko',ls=(0,(2,3,2,3,5,3,8,3)),ms=6, lw=1, alpha=0.8,mfc='None'   ,mec='#009900', mew=3) # unsichtbar zeichnen: alpha=0.0
move0,    = plt.plot([0,1],[0,0],'ko',ls=(0,(2,3,2,3,5,3,8,3)),ms=4, lw=1, alpha=0.6,mfc='#003399',mec='#003399')
release0, = plt.plot([0,1],[0,0],'ko',ls=(0,(2,3,2,3,5,3,8,3)),ms=6, lw=1, alpha=0.8,mfc='#aa3300',mec='#cc1100')
hover1,   = plt.plot([0,1],[0,0],'ko',ls=(0,(2,3,2,3,5,3,8,3)),ms=4, lw=1, alpha=0.8,mfc='#009970',mec='#009970')
hovrel1,  = plt.plot([0,1],[0,0],'ko',ls=(0,(2,3,2,3,5,3,8,3)),ms=7, lw=1, alpha=0.8,mfc='#ffffff',mec='#aa3300')
press1,   = plt.plot([0,1],[0,0],'ko',ls=(0,(2,3,2,3,5,3,8,3)),ms=6, lw=1, alpha=0.8,mfc='None'   ,mec='#009900', mew=3)
move1,    = plt.plot([0,1],[0,0],'kd',ls=(0,(2,3,2,3,5,3,8,3)),ms=4, lw=1, alpha=0.6,mfc='#003399',mec='#003399')
release1, = plt.plot([0,1],[0,0],'ko',ls=(0,(2,3,2,3,5,3,8,3)),ms=6, lw=1, alpha=0.8,mfc='#aa3300',mec='#cc1100')
#Mflick,   = plt.plot([0,1],[0,0],'ko',ls=(0,(2,3,2,3,5,3,8,3)),ms=5, lw=1, alpha=1.0,mfc='#0099cc')
#Mpress2,  = plt.plot([0,1],[0,0],'kD',ls=(0,(2,3,2,3,5,3,8,3)),ms=7, lw=1, alpha=1.0,mfc='#00ee00')
#Mdrag2,   = plt.plot([0,1],[0,0],'kD',ls=(0,(2,3,2,3,5,3,8,3)),ms=5, lw=1, alpha=1.0,mfc='#000088')
#Mflick2,  = plt.plot([0,1],[0,0],'kD',ls=(0,(2,3,2,3,5,3,8,3)),ms=5, lw=1, alpha=1.0,mfc='#0099cc')
#Mzoom,    = plt.plot([0,1],[0,0],'kD',ls=(0,(2,3,2,3,5,3,8,3)),ms=5, lw=1, alpha=1.0,mfc='#ff00ff')
#Mrotate,  = plt.plot([0,1],[0,0],'kD',ls=(0,(2,3,2,3,5,3,8,3)),ms=5, lw=1, alpha=1.0,mfc='#bb9900')
#Mraw2,    = plt.plot([0,1],[0,0],'kD',ls=(0,(2,3,2,3,5,3,8,3)),ms=5, lw=1, alpha=1.0,mfc='#000000')
#Mraw2p,   = plt.plot([0,1],[0,0],'k*',ls=(0,(2,3,2,3,5,3,8,3)),ms=6, lw=1, alpha=1.0,mfc='#000000')
#LegHandle = plt.legend([Mpress,Mclick,Mrelease,Mdrag,Mflick,Mpress2,Mdrag2,Mflick2,Mzoom,Mrotate,Mraw2,Mraw2p],
#LegHandle = plt.legend([hover0,hovrel0,press0,move0,release0,hover1,hovrel1,press1,move1,release1],
LegHandle = plt.legend([hover0,hovrel0,press0,move0,release0,press1,move1,release1],
                      ["hover0 ("+str(EventTypeCnt[0])+  ")",
                       "hoveRel0 ("+str(EventTypeCnt[1])+  ")",
                       "press0 ("+str(EventTypeCnt[2])+  ")",
                       "move0 (" +str(EventTypeCnt[3])+  ")",
					   "release0 ("+str(EventTypeCnt[4])+")",
                       #"hover1 ("+str(EventTypeCnt[5])+  ")",
                       #"hoveRel1 ("+str(EventTypeCnt[6])+  ")",
                       "press1 ("+str(EventTypeCnt[7])+  ")",
                       "move1 (" +str(EventTypeCnt[8])+  ")",
                       "release1 ("+str(EventTypeCnt[9])+")"#,
					   #"flick ("+str(EventTypeCnt[5])+")",
                       #"press2 ("+str(EventTypeCnt[8])+")",
                       #"drag2 ("+str(EventTypeCnt[9])+")",
                       #"flick2 ("+str(EventTypeCnt[10])+")",
                       #"zoom ("+str(EventTypeCnt[11])+")",
                       #"rotate ("+str(EventTypeCnt[6])+")",
                       #"raw2 ("+str(EventTypeCnt[7])+")",
                       #"raw2+ ("+str(EventTypeCnt[13])+")"
                       ],
                       fontsize=10)
#print("done legend plotting")

pt_error = 1
Seq_start = 0
Seq_end = 0
if (pt_error != 0): #mark wrong points
    pt_cnt = 0
	#connecting lines; linestyle: 1,1,4,1,8,1 means: [- ---- -------- ]
    #MyPl = ax.plot(Events_x,Events_y,ls=(0,(2,3,2,3,5,3,8,3)),color='k', ms=5, lw=1, alpha=0.35, mfc='#000000') # plot connecting lines
    #for c in MyPl.collections:
    #    c.set_dashes([(0,(2.0, 2.0))])
    #Line2D.set_dashes([0,(2.0, 2.0)])
    #Line2D.set_dashes(0,(2.0, 2.0))
    
    # plot display boundaries
    ax.plot([0,779]  ,[0,0]    , '-o',color='#0000ff', ms=1, lw=1, alpha=1.0, mfc='#0000ff',mec='#0000ff')
    ax.plot([779,779],[0,349]  , '-o',color='#0000ff', ms=1, lw=1, alpha=1.0, mfc='#0000ff',mec='#0000ff')
    ax.plot([0,779]  ,[349,349], '-o',color='#0000ff', ms=1, lw=1, alpha=1.0, mfc='#0000ff',mec='#0000ff')
    ax.plot([0,0]    ,[0,349]  , '-o',color='#0000ff', ms=1, lw=1, alpha=1.0, mfc='#0000ff',mec='#0000ff')

    # plot number of events for each X value and for each Y value
    ax.plot(Frequency_c[FMinX:FMaxX],Frequency_X[FMinX:FMaxX], '-o',color='#00ffff', ms=1, lw=1, alpha=0.3, mfc='#00ffff',mec='#00ffff')
    ax.plot(Frequency_Y[FMinY:FMaxY],Frequency_c[FMinY:FMaxY], '-o',color='#00ffff', ms=1, lw=1, alpha=0.3, mfc='#00ffff',mec='#00ffff')
    ax.plot(Frequency_c[FMinHX:FMaxHX],Frequency_HX[FMinHX:FMaxHX], '-o',color='#ffaa00', ms=1, lw=1, alpha=0.3, mfc='#ffaa00',mec='#ffaa00')
    ax.plot(Frequency_HY[FMinHY:FMaxHY],Frequency_c[FMinHY:FMaxHY], '-o',color='#ffaa00', ms=1, lw=1, alpha=0.3, mfc='#ffaa00',mec='#ffaa00')
    
    fid = 0
    hover_active = False
    while (fid < 10):
        pt_cnt = 0
        while (pt_cnt < NumOfPts-1):
            #while (pt_cnt < 300):
                #plot each element individually to allow individual settings for size, colour, symbol etc.
                #print(pt_cnt)
                #print(CSVEvents[pt_cnt][:])
                #if (pt_errors[pt_cnt] == 1):
                #ax.plot(TouchEvents[pt_cnt][0],TouchEvents[pt_cnt][1], TouchEvents[pt_cnt][3], ms=TouchEvents[pt_cnt][4], lw=0, alpha=1.0, mfc=TouchEvents[pt_cnt][2])
        		# plot(x,y,symbol,size,linewidth,alpha,color)
                if ((CSVEvents[pt_cnt][7*fid+0] > '0') or (CSVEvents[pt_cnt][7*fid+1] > '0')): # plot only existing points
                    if ((int(CSVEvents[pt_cnt][7*fid+2]) > 99) and (int(CSVEvents[pt_cnt][7*fid+2]) < 200)): # hovering event, plot white center
                        ax.plot(CSVEvents[pt_cnt][7*fid+0],CSVEvents[pt_cnt][7*fid+1], CSVEvents[pt_cnt][7*fid+5], ms=(int(CSVEvents[pt_cnt][7*fid+2])-100)/5, lw=1, alpha=1.0-(float(CSVEvents[pt_cnt][7*fid+2])-100)/90, mfc='#ffffff',mec=CSVEvents[pt_cnt][7*fid+3]) # recognized point
                    elif ((int(CSVEvents[pt_cnt][7*fid+2]) == 200)): # hovering event, plot white center
                        ax.plot(CSVEvents[pt_cnt][7*fid+0],CSVEvents[pt_cnt][7*fid+1], CSVEvents[pt_cnt][7*fid+5], ms=(int(CSVEvents[pt_cnt][7*fid+2])-100)/5, lw=1, alpha=0.6, mfc='None',mec=CSVEvents[pt_cnt][7*fid+3]) # recognized point
                    elif ((int(CSVEvents[pt_cnt][7*fid+2]) == 253)): # press event
                    #   ax.plot(CSVEvents[pt_cnt][7*fid+0],CSVEvents[pt_cnt][7*fid+1], CSVEvents[pt_cnt][7*fid+5], ms=(int(CSVEvents[pt_cnt][7*fid+2])-100)/5, lw=1, alpha=0.6, mfc='None',mec=CSVEvents[pt_cnt][7*fid+3]) # recognized point
                        ax.plot(CSVEvents[pt_cnt][7*fid+0],CSVEvents[pt_cnt][7*fid+1], CSVEvents[pt_cnt][7*fid+5], ms=8, mew=3, alpha=float(CSVEvents[pt_cnt][7*fid+4]),mfc='None',mec=CSVEvents[pt_cnt][7*fid+3])
                    elif ((int(CSVEvents[pt_cnt][7*fid+2]) == 255)): # release event
                        #ax.plot(CSVEvents[pt_cnt][7*fid+0],CSVEvents[pt_cnt][7*fid+1], CSVEvents[pt_cnt][7*fid+5], ms=7, lw=20, alpha=float(CSVEvents[pt_cnt][7*fid+4]),mfc=CSVEvents[pt_cnt][7*fid+3],mec='None')
                        ax.plot(CSVEvents[pt_cnt][7*fid+0],CSVEvents[pt_cnt][7*fid+1], CSVEvents[pt_cnt][7*fid+5], ms=7, lw=20, alpha=float(CSVEvents[pt_cnt][7*fid+4]),mfc=CSVEvents[pt_cnt][7*fid+3],mec='None')
                    else: # all other events
                        ax.plot(CSVEvents[pt_cnt][7*fid+0],CSVEvents[pt_cnt][7*fid+1], CSVEvents[pt_cnt][7*fid+5], ms=CSVEvents[pt_cnt][7*fid+6], lw=1, alpha=float(CSVEvents[pt_cnt][7*fid+4]), mfc=CSVEvents[pt_cnt][7*fid+3],mec=CSVEvents[pt_cnt][7*fid+3])
                #end if
                if (CSVEvents[pt_cnt][7*fid+2] == '200'): # hover release
                    Seq_end = pt_cnt
                    hover_active = False
                    print('release')
                    #if (Seq_start > 0):
                    Seq_Xvals = CSVEvents[Seq_start:Seq_end+1,7*fid+0] # input sequence completed. Go from start to end
                    Seq_Yvals = CSVEvents[Seq_start:Seq_end+1,7*fid+1]
                    MyPl = ax.plot(Seq_Xvals,Seq_Yvals,ls=(0,(2,3,2,3,5,3,8,3)),color='g', ms=5, lw=1, alpha=0.45, mfc='#000000') # plot connecting lines grey
                    print('finger zeichnet',Seq_start,Seq_end)
                    #print(Seq_Xvals,Seq_Yvals)
                if (CSVEvents[pt_cnt][7*fid+2] == '255'): # release
                    Seq_end = pt_cnt
                    print('release')
                    #if (Seq_start > 0):
                    Seq_Xvals = CSVEvents[Seq_start:Seq_end+1,7*fid+0] # input sequence completed. Go from start to end
                    Seq_Yvals = CSVEvents[Seq_start:Seq_end+1,7*fid+1]
                    MyPl = ax.plot(Seq_Xvals,Seq_Yvals,ls=(0,(2,3,2,3,5,3,8,3)),color='k', ms=5, lw=1, alpha=0.45, mfc='#000000') # plot connecting lines grey
                    print('finger zeichnet',Seq_start,Seq_end)
                    #print(Seq_Xvals,Seq_Yvals)
                if ((int(CSVEvents[pt_cnt][7*fid+2]) > 99) and (int(CSVEvents[pt_cnt][7*fid+2]) < 200)) : # enter hover  
                    if (hover_active == False):
                        Seq_start = pt_cnt
                        hover_active = True
                    print('press',Seq_end,Seq_start)
                    if (Seq_end > 0):
                        Seq_Xvals = CSVEvents[Seq_end:Seq_start+1,7*fid+0] # input sequence completed. Go from previous end to new start
                        Seq_Yvals = CSVEvents[Seq_end:Seq_start+1,7*fid+1]
                        MyPl = ax.plot(Seq_Xvals,Seq_Yvals,ls=(0,(2,3,2,3,5,3,8,3)),color='y', ms=5, lw=1, alpha=0.25, mfc='#000000') # plot connecting lines yellow
                        print('finger fliegt',Seq_end,Seq_start)
                        #print(Seq_Xvals,Seq_Yvals)
                if (CSVEvents[pt_cnt][7*fid+2] == '253'): # press  
                    Seq_start = pt_cnt
                    print('press',Seq_end,Seq_start)
                    if (Seq_end > 0):
                        Seq_Xvals = CSVEvents[Seq_end:Seq_start+1,7*fid+0] # input sequence completed. Go from previous end to new start
                        Seq_Yvals = CSVEvents[Seq_end:Seq_start+1,7*fid+1]
                        MyPl = ax.plot(Seq_Xvals,Seq_Yvals,ls=(0,(2,3,2,3,5,3,8,3)),color='y', ms=5, lw=1, alpha=0.25, mfc='#000000') # plot connecting lines yellow
                        print('finger fliegt',Seq_end,Seq_start)
                        #print(Seq_Xvals,Seq_Yvals)
                pt_cnt = pt_cnt + 1
        fid = fid + 1
#ax = pl.subplot(2,1,1)
#print("done plotting points")

pt_error = 1
if (pt_error == 0): #mark wrong points
    plt.title('Alg_Interpol3D')
else:
    #plt.title('Touchevents')
    head,tail = path.split(CSV_filename) # get filename without path
    plt.title(tail)
#end if
plt.flag()
#print("done plt.flag()")

# This makes the original colorbar look a bit out of place,
# so let's improve its position.
l,b,w,h = plt.gca().get_position().bounds
#ll,bb,ww,hh = CB.ax.get_position().bounds
#CB.ax.set_position([ll, b+0.1*h, ww, h*0.8])

pp = PdfPages(tail+'.pdf')
pp.savefig() #save PDF
pp.close()   #all done - close file.

plt.show()
print (":-)")
