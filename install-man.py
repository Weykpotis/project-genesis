import time
class version():
  def __init__(self):
    self.major=1
    self.minor=0
    self.micro=0
    self.type='p'
    self.build=0
    self.total='AssemblyOS Installer 1.0.0p'
def alta(bytstr, point):
  global file
  file.seek(point)
  alt(bytstr)
def alt(bytstr):
  global file
  bytlst=[]
  for i in range(8):
    bytlst.append(16*int(bytstr[2*i], base=16)+int(bytstr[2*i+1], base=16))
  file.write(bytes(bytlst))
def altex(read, point):
  for i in read:
    if i[0:3]=='COM':
      if i[4:6] in ['00', '01', '02', '03', '04', '05', '06', '07',
                    '08', '09', '0A', '0B', '0C', '0D', '0E', '0F',
                    '10', '11', '12', '13', '14', '15', '16', '18',
                    '19', '1A', '1B', '1C', '1D', '1E', '1F', '20',
                    '21', '22', '23', '24']:
        alta(i[4:20], point)
        point=point+8
      if i[4:6]=='17':
        alta(i[4:20], point)
        point=point+8
    elif i[0:3]=='DAT':
      alta(i[4:20], point)
      point=point+8
formatd=input('FORMAT?')
a=time.time()
if formatd:
  file=open('/Applications/AssemblyOS/dt.aod', 'wb')
  for i in range(int(formatd)*128):
    if i%8192==0:
      print(str(i//128)+' KB wiped.')
    alt('0000000000000000')
  print('Disk formatted.')
  file.seek(0)
  file.close()
file=open('/Applications/AssemblyOS/dt.aod', 'rb+')
######
trl=open('/Applications/AssemblyOS/asm/window.asm', mode='r')
altex(trl, 0)
print('trl')
######
file.close()
print('INSTALLATION COMPLETE in '+str(time.time()-a)+' seconds.')
