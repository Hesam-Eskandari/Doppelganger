from cv2 import imshow, circle, putText, FONT_HERSHEY_SIMPLEX, waitKey, destroyAllWindows, line
from cv2 import VideoWriter, imread, resize, destroyWindow, namedWindow, setMouseCallback, EVENT_FLAG_LBUTTON
from numpy import shape, array, ones
from random import sample
from numpy import sum as np_sum

def rectangle(ground,x_c,y_c,length,width,thick,fill,color):
    # use this command:
    # line(ground,(x1,y1),(x2,y2),color,thickness)
    points = [[x_c-length/2,y_c-width/2],[x_c+length/2,y_c-width/2],
              [x_c+length/2,y_c+width/2],[x_c-length/2,y_c+width/2]]
    for ind in [-1,0,1,2]:
        line(ground,(points[ind][0],points[ind][1]),(points[ind+1][0],points[ind+1][1]),color,thick)
    
    if min(length,width)<=2 or fill == False:
        return ground
    else:
        return rectangle(ground,x_c,y_c, length-4, width-4,thick,fill, color)

def left_click(event,x,y,flags,param):
    if event == EVENT_FLAG_LBUTTON and work_g[y,x,1] == 0:
        distance=[]
        for item in coords:
            distance.append((item[0]-x)**2+(item[1]-y)**2)
        distance = array(distance)
        global target
        target = coords[distance == min(distance)][0]

def load_picture(length,width):
    image=[]
    for i in range(8):
        img = imread(str(i+1)+'a.jpg')
        img = resize(img,(length,width))
        image.append(img)
        image.append(img)
    return image

target = []
dim_y = 600
dim_x = int(dim_y*1.618+0.5)
out = VideoWriter('Doppelganger.mp4',4, 30, (dim_x,dim_y))
namedWindow('Doppelganger')
setMouseCallback('Doppelganger', left_click)
width = int(dim_y/6)
length = int(width*1.618+0.5)//2*2
ground = ones((dim_y,dim_x,3))*255
ground = ground.astype('uint8')
background= ground.copy()
color = [255,0,0]
image = load_picture(length,width)
image = sample(image,16)
global coords
coords = []
item = 0
for row in range(4):
    for column in range(4):
        rectangle(ground,dim_x/2+(row-2)*(length+5)+length/2,dim_y/2+(column-2)*(width+5)+width/2,length,width,2,1,color)
        background[dim_y/2+(column-2)*(width+5):dim_y/2+(column-2)*(width+5)+width,
                   dim_x/2+(row-2)*(length+5):dim_x/2+(row-2)*(length+5)+length]=image[item]
        coords.append([dim_x/2+(row-2)*(length+5)+length/2,dim_y/2+(column-2)*(width+5)+width/2])
        item+=1
coords = array(coords) 
global work_g
work_g = ground.copy()
counter = 0;im=[];tar=[]
timer = 0
while timer<50:
    imshow('Doppelganger',background)
    key = waitKey(1) & 0xFF
    out.write(background)
    timer+=1
vw_counter = 0
while True:
    vw_counter+=1
    if target!=[]:
        tar.append(target)
        work_g[target[1]-width/2:target[1]+width/2,
               target[0]-length/2:target[0]+length/2] = background[target[1]-width/2:target[1]+width/2,
                target[0]-length/2:target[0]+length/2]
        im.append(background[target[1]-width/2:target[1]+width/2,
               target[0]-length/2:target[0]+length/2])
        counter+=1
        imshow('Doppelganger',work_g)
        key = waitKey(1) & 0xFF
        out.write(work_g)
        if key == 27:
            break
        if counter==2:
            timer=0
            while timer<100:
                timer+=1
                if timer%6==0:
                    out.write(work_g)
                waitKey(3)
            #print im[0]
            #print im[1]
            #print np_sum(1-(im[0]==im[1]))
            if np_sum(1-(im[0]==im[1]))!=0:
                work_g[target[1]-width/2:target[1]+width/2,
                       target[0]-length/2:target[0]+length/2] = ground[target[1]-width/2:target[1]+width/2,
                       target[0]-length/2:target[0]+length/2]
                work_g[tar[0][1]-width/2:tar[0][1]+width/2,
                       tar[0][0]-length/2:tar[0][0]+length/2] = ground[tar[0][1]-width/2:tar[0][1]+width/2,
                       tar[0][0]-length/2:tar[0][0]+length/2]
            counter = 0
            tar=[]
            im=[]        
        target = []
    imshow('Doppelganger',work_g)
    #imshow('bg',background)
    key = waitKey(1) & 0xFF
    if key == 27:
        break
    if vw_counter%8==0:
        out.write(work_g)
out.release()
destroyAllWindows()
