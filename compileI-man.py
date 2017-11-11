def linewrite(mode, string):
  global asm
  global chars
  st=''
  if mode==0:
    st=st+'COM '
    for i in string:
      if i in chars:
        st=st+i
    st=st.ljust(20, '0')
  if mode==1:
    st=st+'DAT '
    for i in string:
      if i in chars:
        st=st+i
    st=st.ljust(20, '0')
  st=st+'\n'
  asm.write(st)
name=input('NAME~')
asa=open(name+'.asa')
asm=open(name+'.asm', mode='w')
chars=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
funcs={'LDR':'00', 'STM':'01', 'LDA':'02', 'STA':'03', 'LDM':'04', 'STD':'05', 'LDB':'06', 'STB':'07',
       'RCV':'08', 'SND':'09', 'RCA':'0A', 'SNA':'0B', 'ACC':'0C', 'EQU':'0D', 'BRN':'0E', 'TRM':'0F',
       'BNS':'10', 'XOR':'11', 'ADD':'12', 'NEG':'13', 'MLT':'14', 'JMP':'15', 'GTO':'16', 'LBL':'17',
       'DIV':'18', 'NUM':'19', 'BRR':'1A', 'ADI':'1B', 'MLI':'1C', 'DVI':'1D', 'DVJ':'1E', 'JMR':'1F',
       'BSI':'20', 'STC':'21', 'LDC':'22', 'STS':'23', 'LDS':'24'}
for i in asa:
  if i[0:3]=='DAT':
    linewrite(1, i[4:20])
  if i[0:3] in funcs:
    linewrite(0, funcs[i[0:3]]+i[4:])
asa.close()
asm.close()
