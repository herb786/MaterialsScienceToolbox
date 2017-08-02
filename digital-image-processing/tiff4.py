container = ['fer']
filename=container[0]+"_ply.tif"
info =dict(ap_min = 2.78, ap_max = 2.78, qp_min = 2.6, qp_max = 2.6)
info =json.dumps(info)
description=info
output = open(filename,'wb')
# Write the header
head = chr(0x49)+chr(0x49)+chr(0x2a)+chr(0x00)
thefile=head # Little endian & TIFF identifier
dim0 = mx.shape[0]
dim1 = mx.shape[1]
offset = dim0*dim1*2 + 8
a1=(offset & 0xff000000)/2**32
a2=(offset & 0x00ff0000)/2**16
a3=(offset & 0x0000ff00)/2**8
a4=(offset & 0x000000ff)
aa=chr(a4)+chr(a3)+chr(a2)+chr(a1)
thefile=thefile+aa


# Write the binary data
for row in range (0,dim0):
    for col in range (0,dim1):
        value = mx[row,col]
        a3=(value & 0x0000ff00)/256
        a4=(value & 0x000000ff)
        aa=chr(a4)+chr(a3)
        thefile=thefile+aa


# Number of directory entries:16
aa=chr(0x10)+chr(0x00)
thefile=thefile+aa

# Width tag
tag=chr(0x00)+chr(0x01)
typs=chr(0x03)+chr(0x00)
count=chr(0x01)+chr(0x00)+chr(0x00)+chr(0x00)
a1 = (dim1 & 0xff00)/256
a2 = (dim1 & 0x00ff)
val = chr(a2)+chr(a1)+chr(0x00)+chr(0x00)
aa = tag+typs+count+val
thefile=thefile+aa

# Length tag
tag=chr(0x01)+chr(0x01)
typs=chr(0x03)+chr(0x00)
count=chr(0x01)+chr(0x00)+chr(0x00)+chr(0x00)
a1 = (dim0 & 0xff00)/256
a2 = (dim0 & 0x00ff)
vall = chr(a2)+chr(a1)+chr(0x00)+chr(0x00)
aa=tag+typs+count+vall
thefile=thefile+aa

# Bits per sample: 16bits
tag=chr(0x02)+chr(0x01)
typs=chr(0x03)+chr(0x00)
count=chr(0x01)+chr(0x00)+chr(0x00)+chr(0x00)
val=chr(0x10)+chr(0x00)+chr(0x00)+chr(0x00)
aa=tag+typs+count+val
thefile=thefile+aa

# Compresion: 1
tag=chr(0x03)+chr(0x01)
typs=chr(0x03)+chr(0x00)
count=chr(0x01)+chr(0x00)+chr(0x00)+chr(0x00)
val=chr(0x01)+chr(0x00)+chr(0x00)+chr(0x00)
aa=tag+typs+count+val
thefile=thefile+aa

# Photometry: Grayscale
tag=chr(0x06)+chr(0x01)
typs=chr(0x03)+chr(0x00)
count=chr(0x01)+chr(0x00)+chr(0x00)+chr(0x00)
val=chr(0x01)+chr(0x00)+chr(0x00)+chr(0x00)
aa=tag+typs+count+val
thefile=thefile+aa

# Fill Order: 1
tag=chr(0x01)+chr(0x0a)
typs=chr(0x03)+chr(0x00)
count=chr(0x01)+chr(0x00)+chr(0x00)+chr(0x00)
val=chr(0x01)+chr(0x00)+chr(0x00)+chr(0x00)
aa=tag+typs+count+val
thefile=thefile+aa

# Document name: 1
tag=chr(0x0d)+chr(0x01)
typs=chr(0x02)+chr(0x00)
count=chr((len(filename)))+chr(0x00)+chr(0x00)+chr(0x00)
offset = dim0*dim1*2 + 8 + 2 +12*16
a1=(offset & 0xff000000)/2**32
a2=(offset & 0x00ff0000)/2**16
a3=(offset & 0x0000ff00)/2**8
a4=(offset & 0x000000ff)
val=chr(a4)+chr(a3)+chr(a2)+chr(a1)
aa=tag+typs+count+val
thefile=thefile+aa

# Description: 1
tag=chr(0x0e)+chr(0x01)
typs=chr(0x02)+chr(0x00)
count=chr((len(description)))+chr(0x00)+chr(0x00)+chr(0x00)
offset = dim0*dim1*2 + 8 + 2 +12*16 + len(filename)
a1=(offset & 0xff000000)/2**32
a2=(offset & 0x00ff0000)/2**16
a3=(offset & 0x0000ff00)/2**8
a4=(offset & 0x000000ff)
val=chr(a4)+chr(a3)+chr(a2)+chr(a1)
aa=tag+typs+count+val
thefile=thefile+aa

# Strip Offset: after header
tag=chr(0x11)+chr(0x01)
typs=chr(0x04)+chr(0x00)
count=chr(0x01)+chr(0x00)+chr(0x00)+chr(0x00)
val=chr(0x08)+chr(0x00)+chr(0x00)+chr(0x00)
aa=tag+typs+count+val
thefile=thefile+aa

# Orientation
tag=chr(0x12)+chr(0x01)
typs=chr(0x03)+chr(0x00)
count=chr(0x01)+chr(0x00)+chr(0x00)+chr(0x00)
val=chr(0x01)+chr(0x00)+chr(0x00)+chr(0x00)
aa=tag+typs+count+val
thefile=thefile+aa

# Sample per pixel
tag=chr(0x15)+chr(0x01)
typs=chr(0x03)+chr(0x00)
count=chr(0x01)+chr(0x00)+chr(0x00)+chr(0x00)
val=chr(0x01)+chr(0x00)+chr(0x00)+chr(0x00)
aa=tag+typs+count+val
thefile=thefile+aa

# Rows per strip
tag=chr(0x16)+chr(0x01)
typs=chr(0x03)+chr(0x00)
count=chr(0x01)+chr(0x00)+chr(0x00)+chr(0x00)
aa=tag+typs+count+vall
thefile=thefile+aa

# Strip byte count: 16 bits (2 bytes)
tag=chr(0x17)+chr(0x01)
typs=chr(0x04)+chr(0x00)
count=chr(0x01)+chr(0x00)+chr(0x00)+chr(0x00)
byts = dim0*dim1*2
a1=(byts & 0xff000000)/2**32
a2=(byts & 0x00ff0000)/2**16
a3=(byts & 0x0000ff00)/2**8
a4=(byts & 0x000000ff)
val=chr(a4)+chr(a3)+chr(a2)+chr(a1)
aa=tag+typs+count+val
thefile=thefile+aa

# X Resolution
tag=chr(0x1a)+chr(0x01)
typs=chr(0x05)+chr(0x00)
count=chr(0x01)+chr(0x00)+chr(0x00)+chr(0x00)
offset = dim0*dim1*2 + 8 + 2 +12*16 + len(filename)+len(description)
a1=(offset & 0xff000000)/2**32
a2=(offset & 0x00ff0000)/2**16
a3=(offset & 0x0000ff00)/2**8
a4=(offset & 0x000000ff)
val=chr(a4)+chr(a3)+chr(a2)+chr(a1)
aa=tag+typs+count+val
thefile=thefile+aa

# Y Resolution
tag=chr(0x1b)+chr(0x01)
typs=chr(0x05)+chr(0x00)
count=chr(0x01)+chr(0x00)+chr(0x00)+chr(0x00)
offset = dim0*dim1*2 + 8 + 2 +12*16 + len(filename)+len(description)+8
a1=(offset & 0xff000000)/2**32
a2=(offset & 0x00ff0000)/2**16
a3=(offset & 0x0000ff00)/2**8
a4=(offset & 0x000000ff)
val=chr(a4)+chr(a3)+chr(a2)+chr(a1)
aa=tag+typs+count+val
thefile=thefile+aa

# Planar Configuration
tag=chr(0x1c)+chr(0x01)
typs=chr(0x03)+chr(0x00)
count=chr(0x01)+chr(0x00)+chr(0x00)+chr(0x00)
val=chr(0x01)+chr(0x00)+chr(0x00)+chr(0x00)
aa=tag+typs+count+val
thefile=thefile+aa

# Name + Description
thefile=thefile+filename+description

#Xres and Yres
a4=chr(0x00)+chr(0x00)+chr(0x00)+chr(0x64)
a3=chr(0x00)+chr(0x00)+chr(0x00)+chr(0x01)
a2=chr(0x00)+chr(0x00)+chr(0x00)+chr(0x64)
a1=chr(0x00)+chr(0x00)+chr(0x00)+chr(0x01)
aa=a4+a3+a2+a1
thefile=thefile+aa


output.write(bytes(thefile))
output.close()