def to_hsl_checker(tup):
    r=float(tup[0])/255
    g=float(tup[1])/255
    b=float(tup[2])/255
    mi=min(r,g,b)
    ma=max(r,g,b)
    L=(ma+mi)/2
    if ma==mi:
        S=0
    elif L<=0.5:
        S=(ma-mi)/(ma+mi)
    elif L>0.5:
        S=(ma-mi)/(2.00-ma-mi)

    if ma==mi:
        H=0
    elif r==ma:
        H=(g-b)/(ma-mi)
    elif g==ma:
        H=2+(b-r)/(ma-mi)
    elif b==ma:
        H=4+(r-g)/(ma-mi)
    H*=60
    if H<0:
        H+=360

    if H<20 or H>=239:
        return True
    return False

def check(co):
    R=float(co[0])
    G=float(co[1])
    B=float(co[2])
    if R+B+G==0:
        r,b,g=0,0,0
    else:
        r=R/(R+B+G)
        b=B/(R+B+G)
        g=G/(R+B+G)
    f1=-1.376*r**2+1.0743*r+0.2
    f2=-0.776*r**2+0.5601*r+0.18
    w=(r-0.33)**2+(g-0.33)**2
    if f1>g and f2<g and w>0.0004:
        return True
    return False


import struct

a=str(raw_input())

bmp_img = open(a, 'rb')
new_bmp = open('new.bmp','wb')
all_data = bytearray(bmp_img.read())
bmp_img.seek(54, 0)


new_bmp.write(all_data[0:55])
size = struct.unpack('<II', all_data[18:26])

for i in range(size[0]*size[1]):
     color_data=bmp_img.read(1)
     color0=int(color_data.encode('hex'), 16)
     color_data=bmp_img.read(1)
     color1=int(color_data.encode('hex'), 16)
     color_data=bmp_img.read(1)
     color2=int(color_data.encode('hex'), 16)
     color=color0,color1,color2
     if check(color) or not to_hsl_checker(color):
       new_bmp.write(b'\xff\xff\xff')
     else:
       new_bmp.write(b'\x00\x00\x00')

new_bmp.write(all_data[55+size[0]*size[1]:])
new_bmp.close()
bmp_img.close()
