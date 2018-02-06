from PIL import Image, ExifTags

#This part is copied from stackoverflow.com in order to keep safe from unexpexted rotations
#Start of the copied part

def get_rotation_code(img):
    """
    Returns rotation code which say how much photo is rotated.
    Returns None if photo does not have exif tag information.
    Raises Exception if cannot get Orientation number from python
    image library.
    """
    if not hasattr(img, '_getexif') or img._getexif() is None:
        return None

    for code, name in ExifTags.TAGS.iteritems():
        if name == 'Orientation':
            orientation_code = code
            break
    else:
        raise Exception('Cannot get orientation code from library.')

    return img._getexif().get(orientation_code, None)


class IncorrectRotationCode(Exception):
    pass


def rotate_image(img, rotation_code):
    """
    Returns rotated image file.

    img: PIL.Image file.
    rotation_code: is rotation code retrieved from get_rotation_code.
    """
    if rotation_code == 1:
        return img
    if rotation_code == 3:
        img = img.transpose(Image.ROTATE_180)
    elif rotation_code == 6:
        img = img.transpose(Image.ROTATE_270)
    elif rotation_code == 8:
        img = img.transpose(Image.ROTATE_90)
    else:
        raise IncorrectRotationCode('{} is unrecognized '
                                    'rotation code.'
                                    .format(rotation_code))
    return img

#End of the copied part

def check(co):
    R=co[0]
    G=co[1]
    B=co[2]
    if R+B+G==0:
        r,b,g=0,0,0
    else:
        r=float(R)/(R+B+G)
        b=float(B)/(R+B+G)
        g=float(G)/(R+B+G)
    f1=-1.376*(r**2)+1.0743*r+0.2
    f2=-0.776*(r**2)+0.5601*r+0.18
    w=(r-0.33)**2+(g-0.33)**2
    if f1>g and f2<g and w>0.0004:
        return True
    return False
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


a=str(raw_input())
new=Image.open(a)
pix=new.load()
h,w=new.size

for i in range(h):
    for j in range (w):
        if check(pix[i,j]) or not to_hsl_checker(pix[i,j]):
            pix[i,j]=255,255,255
        else:
            pix[i,j]=0,0,0
rotation_code = get_rotation_code(new)


if rotation_code is not None:
    new = rotate_image(new, rotation_code)
    new.save('new'+a[-4:])
else:
    new.save('new'+a[-4:])
