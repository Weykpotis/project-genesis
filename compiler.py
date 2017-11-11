#Alpha Compiler v1.2 by Harrison Chudleigh, with some help from Evan La Fontaine
#Max 75 pairs of brackets (including square ones). If you're using this many,
#please rewrite your code. For reference, 75 is this many: (((((((((((((((((((((
#((((((((((((((((((((((((((((((((((((((((((((((((((((((.
#Max 80 args to a function. If you rally need to provide thousands of arguments
#use an array.
#Declarations first (may add rearranger later)
#Violating any max limit is currently considered UNDEFINED BEHAVIOUR. DO NOT!
#Added in 1.2: Binary shift.
#Added in 1.1: Optimizations.
stack=0
lnames={}
lnamescache=[]
lcounter=0
gnames={}
gcounter=0
code=[]
nlabels={}
loopstack=[]
funcs={'~':[0, 0, 'SKIPMAIN']}
funcsc=['~']
b32=2**32
lblcnt=-1
labelnum=0
labelpos={}
gotopos={}
optimize=0
statements=[]
def getutflen(string):
  return len(bytes(string, 'utf-8'))
def genlbl():
  global lblcnt
  lblcnt=lblcnt+1
  return hexj(lblcnt, 8)
def hexj(number, just):
  return hexn(number).rjust(just, '0')
def hexn(number):
  if type(number)==type(''):
    number=int(number)
  return hex(number)[2:].replace('a', 'A').replace('b', 'B').replace('c', 'C').replace('d', 'D').replace('e', 'E').replace('f', 'F')
def numload(number, reg):
  if number==0:
    out("XOR"+3*(" r"+hexj(reg, 2)))
    return
  out("NUM r"+hexj(reg, 2)+" t01 i"+hexj(int((number%(b32*b32))//b32), 8))
  out("NUM r"+hexj(reg, 2)+" t00 i"+hexj(int(number%b32), 8))
def out(string):
  global code
  global labelnum
  global gotopos
  global labelpos
  if string.startswith('LBL '):
    labelpos[string[5:13]]=len(code)-labelnum
    labelnum=labelnum+1
  if string.startswith('GTO '):
    gotopos[len(code)]=[string[13:21], labelnum]
  code.append(string)
def getvar(name, reg):
  if name.startswith('&'):
    if name[1:] not in lnames:
      if funcsc[0]=='~':
        numload(gnames[name[1:]], reg)
      else:
        numload(gnames[name[2:]], reg)
    else:
      numload(80+lnames[name[1:]], reg)
      out("ADD r"+hexj(reg, 2)+" rF7 r"+hexj(reg, 2))
  else:
    if name not in lnames:
      if optimize>1:
        if funcsc[0]=='~' and gnames[name]<(2**24):
          out("LDA r"+hexj(reg, 2)+" m"+hexj(gnames[name], 6))
          return
        elif gnames[name[1:]]<(2**24):
          out("LDA r"+hexj(reg, 2)+" m"+hexj(gnames[name[1:]], 6))
          return
      if funcsc[0]=='~':
        numload(gnames[name], 252)
      else:
        numload(gnames[name[1:]], 252)
    else:
      numload(80+lnames[name], 252)
      out("ADD rFC rF7 rFC")
    out("LDR r"+hexj(reg, 2)+" rmFC")
def setvar(name, reg):
  if name not in lnames:
    if optimize>1:
      if funcsc[0]=='~' and gnames[name]<(2**24):
        out("STA r"+hexj(reg, 2)+" m"+hexj(gnames[name], 6))
        return
      elif gnames[name[1:]]<(2**24):
        out("STA r"+hexj(reg, 2)+" m"+hexj(gnames[name[1:]], 6))
        return
    if funcsc[0]=='~':
      numload(gnames[name], 252)
    else:
      numload(gnames[name[1:]], 252)
  else:
    numload(80+lnames[name], 252)
    out("ADD rFC rF7 rFC")
  out("STM r"+hexj(reg, 2)+" rmFC")
def label_stat(explist):
  if explist not in nlabels:
    nlabels[explist]=genlbl()
  out('LBL n'+nlabels[explist])
def def_func(name, params):
  global loopstack
  global lnamescache
  global lnames
  funcsc.append(name)
  funcs[name]=[len(code)-labelnum, len(params), genlbl()]
  out('GTO r00 r00 n'+funcs[name][2]+' t00')
  lnamescache.append(lnames)
  lnames={}
  for i in range(len(params)):
    lnames[params[i]]=i
  loopstack.append(['def', funcs[name][2]])
def call_func(name, params):
  numload(80+funcs[name][1], 241)
  numload(params, 242)
  numload(funcs[name][0], 243)
  out('EQU rFF rF0')
  out('GTO r00 r00 nFFFFFFFB t00')
def call_return(name, explist):
  evalexp(explist)
  numload(80+funcs[name][1], 242)
  out('GTO r00 r00 nFFFFFFFA t00')
def syslib():
  out('GTO r00 r00 nFFFFFFFF t00')
  #internals.endsys
  out('LBL nFFFFFFFE')
  out('ACC rF0')
  out('ACC rF0')
  out('BRR r00 r00 rdF0 t00')
  #sys.dalloc - rF1 is the start pointer.
  out('LBL rFFFFFFFD')
  out('XOR rF5 rF5 rF5')
  out('NEG rF1 rF3')
  out('ACC rF3')
  out('NEG rF3 rF3')
  out('LDR rF2 rmF3')
  out('NEG rF2 rF4')
  out('NEG rF3 rF3')
  out('ACC rF3')
  out('NEG rF3 rF3')
  out('STA rF1 m000000')
  out('XOR rF1 rF1 rF1')
  out('LDR rF6 rmF3')
  out('JMP rF6 rF1 i00000007 t03')
  out('LDR rF6 rmF3')
  out('ADD rF4 rF4 rF6')
  out('NEG rF4 rF4')
  out('ADI rF4 rF4 i00000002')
  out('NEG rF4 rF4')
  out('ACC rF5')
  out('LDA rF1 m000000')
  out('ADD rF1 rF2 rF3')
  out('ACC rF3')
  out('STA rF1 m000000')
  out('XOR rF1 rF1 rF1')
  out('LDR rF6 rmF3')
  out('JMP rF6 rF1 i00000007 t03')
  out('LDR rF6 rmF3')
  out('ADD rF4 rF4 rF6')
  out('NEG rF4 rF4')
  out('ADI rF4 rF4 i00000002')
  out('NEG rF4 rF4')
  out('ADI rF5 rF5 i00000002')
  out('LDA rF1 m000000')
  out('ADD rF1 rF2 rF3')
  out('XOR rF6 rF6 rF6')
  out('ACC rF6')
  out('JMP rF4 rF6 i00000009 t04')
  out('NEG rF5 rF5')
  out('ADI rF5 rF5 i00000002')
  out('NEG rF5 rF5')
  out('ACC rF3')
  out('LDR rF6 rmF3')
  out('ADD rF3 rF3 rF6')
  out('STM rF4 rmF3')
  out('JMP r00 r00 i00000002 t00')
  out('STM rF4 rmF3')
  out('NEG rF1 rF3')
  out('ADI rF3 rF3 i00000002')
  out('NEG rF3 rF3')
  out('XOR rF6 rF6 rF6')
  out('ACC rF6')
  out('JMP rF4 rF6 i00000005 t01')
  out('LDR rF6 rmF3')
  out('ADD rF3 rF3 rF6')
  out('STM rF4 rmF3')
  out('JMP r00 r00 i00000003 t00')
  out('ACC rF3')
  out('STM rF4 rmF3')
  out('GTO r00 r00 nFFFFFFFE t00')
  #sys.malloc - rF1 is the size of the block, rF2 is the returned pointer.
  out('LBL rFFFFFFFC')
  out('NUM rF2 t01 i00000000')
  out('NUM rF2 t00 i000001FE')
  out('XOR rF3 rF3 rF3')
  out('ADD rF3 rF1 rF4')
  out('XOR rF5 rF5 rF5')
  out('JMP rF4 rF5 i0000000B t04')
  out('JMP rF3 rF5 i00000004 t04')
  out('ADD rF2 rF3 rF2')
  out('ADI rF2 rF2 i00000002')
  out('JMP r00 r00 i00000005 t00')
  out('ADI rF2 rF2 i00000002')
  out('NEG rF2 rF2')
  out('ADD rF2 rF3 rF2')
  out('NEG rF2 rF2')
  out('LDR rF3 rmF2')
  out('JMP r00 r00 i0000000C t10')
  out('EQU rF2 rF4')
  out('ACC rF2')
  out('STM rF1 rmF4')
  out('ADD rF1 rF2 rF4')
  out('ACC rF4')
  out('STM rF1 rmF4')
  out('ACC rF4')
  out('ADD rF1 rF3 rF5')
  out('ADI rF5 rF5 i00000002')
  out('NEG rF5 rF5')
  out('STM rF5 rmF4')
  out('ADI rF2 rF4 i00000001')
  out('NEG rF4 rF4')
  out('ADD rF4 rF3 rF4')
  out('STM rF5 rmF4')
  out('STM rF1 rmF2')
  out('GTO r00 r00 nFFFFFFFE t00')
  #internal.callfunc
  out('LBL nFFFFFFFB')
  out('EQU rF0 rF6')
  out('STM rF7 rF8')
  out('ACC rF8')
  out('STA rF2 m000002')
  out('STA rF3 m000003')
  out('STA rF6 m0001FF')
  out('EQU rFF rF0')
  out('BRN r00 r00 d0000000C t00')
  out('EQU rF6 rF0')
  out('EQU rF2 rF7')
  out('EQU rF7 rFC')
  numload(96, 250)
  numload(80, 254)
  out('XOR rFD rFD rFD')
  out('JMP rFD rFE d00000007 t05')
  out('LDR rFB rmFA')
  out('STM rFB rmFC')
  out('ACC rFA')
  out('ACC rFC')
  out('ACC rFD')
  out('JMP r00 r00 d00000006 t10')
  out('LDA rFE m000002')
  out('XOR rFD rFD rFD')
  out('JMP rFD rFE d00000007 t05')
  out('LDR rFB rmFA')
  out('STM rFB rmFC')
  out('ACC rFA')
  out('ACC rFC')
  out('ACC rFD')
  out('JMP r00 r00 d00000006 t10')
  out('LDA rF3 m000003')
  out('BRR r00 r00 rdF3 t00')
  #internal.return
  out('LBL nFFFFFFFA')
  out('EQU rF7 rF1')
  out('EQU rFF rF0')
  out('BRN r00 r00 d00000004 t00')
  numload(78, 242)
  out('EQU rF6 rF0')
  out('XOR rF6 rF6 rF6')
  out('ADD rF2 rF7 rF3')
  out('LDR rFD rmF3')
  out('NEG rF2 rF2')
  out('ACC rF2')
  out('NEG rF2 rF2')
  out('JMP rF6 rF2 d00000009 t05')
  out('ADD rF2 rF7 rF3')
  out('ADI rF2 rF4 i00000010')
  out('LDR rFC rmF3')
  out('STM rFC rmF4')
  out('NEG rF2 rF2')
  out('ACC rF2')
  out('NEG rF2 rF2')
  out('JMP r00 r00 d00000008 t10')
  out('NEG rF8 rF8')
  out('ACC rF8')
  out('NEG rF8 rF8')
  out('LDR rF7 rmF8')
  out('LDA rF0 m0001FF')
  out('GTO r00 r00 nFFFFFFFE t00')
def extlib():
  #pict.rect
  out('LBL nFFFFFFF9')
  out('EQU rF1 rF6')
  out('NUM rF3 t01 iFFFFFFFF')
  out('NUM rF3 t00 iFFFFFFF9')
  out('XOR rF4 rF4 rF4')
  out('JMP rF3 rF4 d00000005 t05')
  out('BSI rF6 i00000008 t01')
  out('ADD rF1 rF6 rF6')
  out('ACC rF3')
  out('JMP r00 r00 d00000004 t10')
  out('EQU rF6 rF1')
  out('NUM rF3 t01 iFFFFFFFF')
  out('NUM rF3 t00 iFFFFFFFF')
  out('DVI rF2 i00010000 rF4 rF6')
  out('EQU rF2 rF5')
  out('BSI rF5 i00000013 t00')
  out('DVI rF5 i00002000 rF4 rF5')
  out('MLT rF5 rF6 rF4')
  out('ACC rF3')
  out('JMP rF3 rF4 d00000017 t05')
  out('EQU rF2 rF6')
  out('BSI rF6 i00000033 t00')
  out('EQU rF2 rF5')
  out('BSI rF5 i00000013 t00')
  out('DVI rF5 i00002000 rF4 rF5')
  out('DIV rF3 rF5 rF4 rF5')
  out('ADD rF5 rF6 rF6')
  out('EQU rF2 rF5')
  out('BSI rF5 i00000020 t00')
  out('DVI rF5 i00010000 rF4 rF5')
  out('STA rF6 m000000')
  out('EQU rF2 rF6')
  out('BSI rF6 i00000013 t00')
  out('DVI rF6 i00002000 rF4 rF6')
  out('DIV rF3 rF6 rF6 rF4')
  out('ADD rF6 rF5 rF5')
  out('LDA rF6 m000000')
  out('MLI rF5 rF5 i00000028')
  out('ADD rF5 rF6 rF5')
  out('ADI rF5 rF5 i00000400')
  out('STM rF1 rmF5')
  out('JMP r00 r00 d0000001C t10')
  out('GTO r00 r00 nFFFFFFFE t00')
  #pict.image
  out('LBL nFFFFFFF8')
  out('NUM rF3 t01 iFFFFFFFF')
  out('NUM rF3 t00 iFFFFFFFF')
  out('DVI rF2 i00010000 rF4 rF6')
  out('EQU rF2 rF5')
  out('BSI rF5 i00000013 t00')
  out('DVI rF5 i00002000 rF4 rF5')
  out('MLT rF5 rF6 rF4')
  out('ACC rF3')
  out('JMP rF3 rF4 d00000019 t05')
  out('EQU rF2 rF6')
  out('BSI rF6 i00000033 t00')
  out('EQU rF2 rF5')
  out('BSI rF5 i00000013 t00')
  out('DVI rF5 i00002000 rF4 rF5')
  out('DIV rF3 rF5 rF4 rF5')
  out('ADD rF5 rF6 rF6')
  out('EQU rF2 rF5')
  out('BSI rF5 i00000020 t00')
  out('DVI rF5 i00010000 rF4 rF5')
  out('STA rF6 m000000')
  out('EQU rF2 rF6')
  out('BSI rF6 i00000013 t00')
  out('DVI rF6 i00002000 rF4 rF6')
  out('DIV rF3 rF6 rF6 rF4')
  out('ADD rF6 rF5 rF5')
  out('LDA rF6 m000000')
  out('MLI rF5 rF5 i00000028')
  out('ADD rF5 rF6 rF5')
  out('ADI rF5 rF5 i00000400')
  out('ADD rF1 rF3 rF4')
  out('LDR rF5 rmF4')
  out('STM rF5 rmF6')
  out('JMP r00 r00 d0000001E t10')
  out('GTO r00 r00 nFFFFFFFE t00')
  #pict.update
  out('LBL nFFFFFFF7')
  out('XOR rF3 rF3 rF3')
  out('NUM rF4 t01 i00000000')
  out('NUM rF4 t00 i00012C00')
  out('JMP rF3 rF4 i0000000E t05')
  out('DVI rF3 i00000008 rF5 rF4')
  out('ADI rF5 rF5 i00000400')
  out('LDS rF6 rF5 rF4')
  out('BSI rF6 i00000010 t01')
  out('DVI rF3 i00000140 rF4 rF5')
  out('ADD rF6 rF5 rF6')
  out('BSI rF6 i00000010 t01')
  out('ADD rF6 rF4 rF6')
  out('BSI rF6 i00000018 t01')
  out('STA rF6 m000000')
  out('SNA p03 m000000')
  out('ACC rF3')
  out('JMP t00 t00 i0000000F t10')
  out('NUM rF6 t01 i62656E65')
  out('NUM rF6 t00 i662E6974')
  out('STA rF6 m000000')
  out('SNA p04 m000000')
  out('GTO r00 r00 nFFFFFFFE t00')
  #pict.event
  out('LBL nFFFFFFF6')
  out('NUM rF6 t01 i6576656E')
  out('NUM rF6 t01 i74676574')
  out('STA rF6 m000000')
  out('SNA p06 m000000')
  out('RCA p05 m000000')
  out('LDA rF1 m000000')
  out('GTO r00 r00 nFFFFFFFE t00')
def init():
  #jump to here to start
  out('LBL nFFFFFFFF')
  numload(256, 248)
  numload(-96766, 240)
  out('STA rF0 m000200')
  out('STA rF0 m017BFF')
################################################################################
def textToTokens(text):
  string=None
  comment=False
  tlist=list(text.replace('\n}\nELSE {\n', '\nELSE\n'))
  ret=['']
  for i in tlist:
    if comment==False:
      if i[0]=='#':
        comment=True
        continue
      if i in ' \t' and string==None:
        if ret[-1]!='':
          ret.append('')
      elif i=='"' and string==None:
        ret.append('"')
        string='"'
      elif i=="'" and string==None:
        ret.append("'")
        string="'"
      elif i=='"' and string=='"':
        ret.append('')
        string=None
      elif i=="'" and string=="'":
        ret.append('')
        string=None
      elif i in "[]{}()+-^*/$%=<>!\n," and string==None:
        if i=='=' and ret[-1]=='' and len(ret)>1:
          if ret[-2] in ['<', '>', '!', '=']:
            ret[-2]=ret[-2]+i
          else:
            ret[-1]=i
            ret.append('')
        elif i=='<' and ret[-1]=='' and len(ret)>1:
          if ret[-2]=='<':
            ret[-2]=ret[-2]+i
          else:
            ret[-1]=i
            ret.append('')
        elif i=='>' and ret[-1]=='' and len(ret)>1:
          if ret[-2]=='>':
            ret[-2]=ret[-2]+i
          else:
            ret[-1]=i
            ret.append('')
        elif i=='-' and (len(ret)==0 or ret[-1] in '[]{}()+-^*/$%=<>!\n,' or ret[-1] in ['<=', '>=', '==']):
          if ret[-1]!='':
            ret.append('~')
          else:
            ret[-1]='~'
          ret.append('')
        else:
          if ret[-1]!='':
            ret.append(i)
          else:
            ret[-1]=i
          ret.append('')
      else:
        ret[-1]=ret[-1]+i
    else:
      if i=='\n':
        comment=False
  return ret
def tokensToRecursive(block, index):
  global optimize
  #do syntax checks here?
  lins=[[]]
  assgn=False
  nexop=[0, '']
  while index<len(block):
    if nexop[0]==1:
      lins[-1].append(nexop[1])
      nexop=[0, '']
    if nexop[0]==0 and nexop[1]!='':
      nexop[0]=1
    tmp=block[index]
    if tmp=='':
      index=index+1
    elif tmp =='(':
      tmp2=tokensToRecursive(block, index+1)
      if index>0:
        if block[index-1] in ['\n', '(', '[', '~', '*', '^', '%', '/', '+', '-', '=', 'RET', 'IF', 'WHILE', 'GOTO', 'FOR']:
          tmpx=[['(']]
        else:
          if index>1:
            if block[index-2]=='FOR':
              tmpx=[['(']]
            else:
              tmpx=[[block[index-1], '(']]
          else:
            tmpx=[[block[index-1], '(']]
      else:
        tmpx=[[tmp]]
      for i in tmp2[0][0]:
        tmpx[0].append(i)
      for i in tmp2[0][1:]:
        tmpx.append(i)
      if index>0:
        if block[index-1] in ['\n', '(', '[', '~', '*', '^', '%', '/', '+', '-', '=', 'RET', 'IF', 'WHILE', 'GOTO', 'FOR']:
          tmp3=lins[-1]+tmpx
        else:
          if index>1:
            if block[index-2]=='FOR':
              tmp3=lins[-1]+tmpx
            else:
              tmp3=lins[-1][:-1]+tmpx
          else:
            tmp3=lins[-1][:-1]+tmpx
      else:
        tmp3=lins[-1]+tmpx
      del lins[-1]
      lins.append(tmp3)
      index=tmp2[1]
    elif tmp =='[':
      tmp2=tokensToRecursive(block, index+1)
      tmpx=[[tmp2[0][0][0], tmp]+tmp2[0][0][1:]]
      for i in tmp2[0][1:]:
        tmpx.append(i)
      tmp3=lins[-1]+tmpx
      del lins[-1]
      lins.append(tmp3)
      index=tmp2[1]
    elif tmp in '])':
      lins[-1].append(tmp)
      if assgn==True:
        lins[-1].append('=')
      return [lins, index+1]
    elif tmp in '\n':
      if assgn==True:
        lins[-1].append('=')
        assgn=False
      if lins[-1]!=[]:
        lins.append([])
      index=index+1
      nexop=[0, '']
    elif tmp=='=':
      assgn=True
      index=index+1
    elif tmp in "/*^+-%~" or tmp in ["<<", ">>"]:
      if index<len(block)-1 and optimize>0:
        if block[index+1].isdigit():
          if tmp in '/*' and int(block[index+1]) in [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608, 16777216, 33554432, 67108864, 134217728, 268435456, 536870912, 1073741824, 2147483648, 4294967296, 8589934592, 17179869184, 34359738368, 68719476736, 137438953472, 274877906944, 549755813888, 1099511627776, 2199023255552, 4398046511104, 8796093022208, 17592186044416, 35184372088832, 70368744177664, 140737488355328, 281474976710656, 562949953421312, 1125899906842624, 2251799813685248, 4503599627370496, 9007199254740992, 18014398509481984, 36028797018963968, 72057594037927936, 144115188075855872, 288230376151711744, 576460752303423488, 1152921504606846976, 2305843009213693952, 4611686018427387904, 9223372036854775808]:
            nexop=[0, ['_BSIOP', tmp, block[index+1]]]
            index=index+2
          elif tmp in ['<<', '>>']:
            nexop=[0, ['_BSIOP', tmp, block[index+1]]]
            index=index+2
          elif int(block[index+1])<(2**32) and tmp not in '~^':
            nexop=[0, ['_DIROP', tmp, block[index+1]]]
            index=index+2
          else:
            nexop=[0, tmp]
            index=index+1
        else:
          nexop=[0, tmp]
          index=index+1
      else:
        nexop=[0, tmp]
        index=index+1
    else:
      lins[-1].append(tmp)
      index=index+1
  if nexop[1]!='':
    lins[-1].append(nexop[-1])
  if assgn==True:
    lins[-1].append('=')
  return [lins, index]
################################################################################
def recursiveToCode(lines):
  for i in lines:
    pass
def outputCode():
  pass
def asm_embed(explist):
  string=''
  for i in explist:
    string=string+i+' '
  out(string[:-1])
def while_loop(explist):
  global stack
  newlist=[[], '', []]
  labl1=genlbl()
  labl2=genlbl()
  elem=0
  for i in explist:
    if elem==0:
      if i in ['==', '!=', '<', '>', '<=', '>=']:
        newlist[1]=i
        elem=1
      else:
        newlist[0].append(i)
    else:
      newlist[2].append(i)
  out('LBL n'+labl1)
  evalexp(newlist[0])
  evalexp(newlist[2])
  out('GTO rFD rFE n'+labl2+' t0'+{'==':'1', '!=':'0', '<':'5', '>':'4', '<=':'3', '>=':'2'}[newlist[1]])
  loopstack.append(['while', labl1, labl2])
  stack=stack-2
def for_loop(explist):
  global stack
  labl1=genlbl()
  labl2=genlbl()
  numload(b32*b32-1, 251)
  setvar(explist[0], 251)
  out('LBL n'+labl1)
  evalexp(explist[1:])
  getvar(explist[0], 251)
  out('ACC rFB')
  out('GTO rFB rFE n'+labl2+' t05')
  setvar(explist[0], 251)
  loopstack.append(['for', labl1, labl2])
  stack=stack-1
def if_loop(explist):
  newlist=[[], '', []]
  labl1=genlbl()
  labl2=genlbl()
  elem=0
  for i in explist:
    if elem==0:
      if i in ['==', '!=', '<', '>', '<=', '>=']:
        newlist[1]=i
        elem=1
      else:
        newlist[0].append(i)
    else:
      newlist[2].append(i)
  evalexp(newlist[0])
  evalexp(newlist[2])
  out('GTO rFD rFE n'+labl1+' t0'+{'==':'1', '!=':'0', '<':'5', '>':'4', '<=':'3', '>=':'2'}[newlist[1]])
  loopstack.append(['if', labl1, labl2])
def else_loop(explist):
  loopstack[-1][0]='else'
  out('GTO r00 r00 n'+loopstack[-1][2]+' t00')
  out('LBL n'+loopstack[-1][1])
def goto_loop(explist):
  newlist=[[], '', []]
  elem=0
  for i in explist[1:]:
    if elem==0:
      if i in ['==', '!=', '<', '>', '<=', '>=']:
        newlist[1]=i
        elem=1
      else:
        newlist[0].append(i)
    else:
      newlist[2].append(i)
  evalexp(newlist[0])
  evalexp(newlist[2])
  if explist[0] not in nlabels:
    nlabels[explist[0]]=genlbl()
  out('GTO rFD rFE n'+nlabels[explist[0]]+' t0'+{'==':'1', '!=':'0', '<':'5', '>':'4', '<=':'3', '>=':'2'}[newlist[1]])
def end_loop():
  global loopstack
  global lnamescache
  global funcsc
  if loopstack[-1][0]=='if':
    out('GTO r00 r00 n'+loopstack[-1][2]+' t00')
    out('LBL n'+loopstack[-1][1])
    out('LBL n'+loopstack[-1][2])
  if loopstack[-1][0]=='else':
    out('LBL n'+loopstack[-1][2])
  if loopstack[-1][0] in ['while', 'for']:
    out('GTO r00 r00 n'+loopstack[-1][1]+' t00')
    out('LBL n'+loopstack[-1][2])
  if loopstack[-1][0]=='def':
    out('LBL n'+loopstack[-1][1])
    lnames=lnamescache[-1]
    del lnamescache[-1]
    del funcsc[-1]
  del loopstack[-1]
def evalexp(explist):
  global stack
  if type(explist)!=type([]):
    explist=[explist]
  if explist==[]:
    return
  if explist[-1]=='=':
    j=len(explist)-1
    for i in range(1, len(explist)-1):
      if type(explist[i])==type([]):
        if explist[i][1]=='[':
          continue
        j=i
        break
      j=i
      break
    if j>1:
      evalexp(explist[j:-1])
      for i in range(j-1):
        evalexp(explist[i])
      evalexp(explist[j-1][0])
      evalexp(explist[j-1][2:])
      popstack('+')
      out('STM rFD rmFE')
    else:
      evalexp(explist[1:-1])
      setvar(explist[0], 254)
    stack=0
    return
  for j in range(len(explist)):
    i=explist[j]
    if type(i)==type([]):
      if i[0] in '{(':
        evalexp(i[1:])
      elif i[1]=='[':
        evalexp(i)
      elif i[0]=='_BSIOP':
        length=len(bin(int(i[2])))-3
        if i[1]=='*':
          out('BSI rFE i'+hexj(length, 8)+' t01')
        elif i[1]=='/':
          out('BSI rFE i'+hexj(length, 8)+' t00')
        elif i[1]=='<<':
          out('BSI rFE i'+hexj(int(i[2]), 8)+' t01')
        elif i[1]=='>>':
          out('BSI rFE i'+hexj(int(i[2]), 8)+' t00')
      elif i[0]=='_DIROP':
        if i[1]=='+':
          out('ADI rFE rFE i'+hexj(i[2], 8))
        if i[1]=='-':
          out('NEG rFE')
          out('ADI rFE rFE i'+hexj(i[2], 8))
          out('NEG rFE')
        if i[1]=='*':
          out('MLI rFE rFE i'+hexj(i[2], 8))
        if i[1]=='/':
          out('DVI rFE i'+hexj(i[2], 8)+' rFE rFC')
        if i[1]=='%':
          out('DVI rFE i'+hexj(i[2], 8)+' rFC rFE')
      else:
        clist=[[]]
        for k in i[2:-1]:
          if k==',':
            clist.append([])
          else:
            clist[-1].append(k)
        if i[0]=='sys.malloc':
          evalexp(clist[0])
          out('EQU rFE rF1')
          out('EQU rFF rF0')
          out('GTO r00 r00 nFFFFFFFC t00')
          out('EQU rF2 rFE')
        elif i[0]=='sys.dalloc':
          evalexp(clist[0])
          out('EQU rFE rF1')
          out('EQU rFF rF0')
          out('GTO r00 r00 nFFFFFFFD t00')
          popstack('')
        elif i[0]=='pict.rect':
          evalexp(clist[0])
          out('EQU rFE rF1')
          popstack('')
          evalexp(clist[1])
          out('EQU rFE rF2')
          popstack('')
          out('BSI rF2 i00000010 t01')
          evalexp(clist[2])
          out('ADD rFE rF2 rF2')
          popstack('')
          out('BSI rF2 i00000010 t01')
          evalexp(clist[3])
          out('ADD rFE rF2 rF2')
          popstack('')
          out('BSI rF2 i00000010 t01')
          evalexp(clist[4])
          out('ADD rFE rF2 rF2')
          popstack('')
          out('EQU rFF rF0')
          out('GTO r00 r00 nFFFFFFF9 t00')
        elif i[0]=='pict.image':
          evalexp(clist[0])
          out('EQU rFE rF1')
          popstack('')
          evalexp(clist[1])
          out('EQU rFE rF2')
          popstack('')
          out('BSI rF2 i00000010 t01')
          evalexp(clist[2])
          out('ADD rFE rF2 rF2')
          popstack('')
          out('BSI rF2 i00000010 t01')
          evalexp(clist[3])
          out('ADD rFE rF2 rF2')
          popstack('')
          out('BSI rF2 i00000010 t01')
          evalexp(clist[4])
          out('ADD rFE rF2 rF2')
          popstack('')
          out('EQU rFF rF0')
          out('GTO r00 r00 nFFFFFFF8 t00')
        elif i[0]=='pict.update':
          out('EQU rFF rF0')
          out('GTO r00 r00 nFFFFFFF7 t00')
        elif i[0]=='pict.event':
          pushstack('')
          out('EQU rFF rF0')
          out('GTO r00 r00 nFFFFFFF6 t00')
          out('EQU rF1 rFE')
        elif i[0]=='io.read':
          evalexp(clist[0])
          out('XOR rFC rFC rFC')
          out('LDM rdFE rmFC')
          out('LDR rFE rmFC')
        else:
          if stack>1:
            out('STA rFD m'+hexj(96+stack-2, 6))
          if stack>0:
            out('STA rFE m'+hexj(96+stack-1, 6))
          numload(96, 250)
          numload(16, 251)
          if stack>2:
            numload(stack-2, 254)
          else:
            out('XOR rFE rFE rFE')
          out('XOR rFD rFD rFD')
          out('JMP rFD rFE d00000007 t05')
          out('LDR rFC rmFB')
          out('STM rFC rmFA')
          out('ACC rFA')
          out('ACC rFB')
          out('ACC rFD')
          out('JMP r00 r00 d00000006 t10')
          pstack=stack
          stack=0
          if clist!=[[]]:
            for k in clist:
              evalexp(k)
          if stack>1:
            out('STA rFD m'+hexj(176+stack-2, 6))
          if stack>0:
            out('STA rFE m'+hexj(176+stack-1, 6))
          numload(176, 250)
          numload(16, 251)
          if stack>2:
            numload(stack-2, 254)
          else:
            out('XOR rFE rFE rFE')
          out('XOR rFD rFD rFD')
          out('JMP rFD rFE d00000007 t05')
          out('LDR rFC rmFB')
          out('STM rFC rmFA')
          out('ACC rFA')
          out('ACC rFB')
          out('ACC rFD')
          out('JMP r00 r00 d00000006 t10')
          call_func(i[0], stack)
          stack=pstack+1
    elif i in "/*^+-%[~" or i in ["<<", ">>"]:
      popstack(i)
    elif i in ')]':
      return
    elif i=='}':
      end_loop()
      return
    elif i!='{':
      pushstack(i)
def pushstack(var):
  global stack
  if stack>1:
    out("STA rFD m"+hexj(16+stack-2, 6))
  if stack>0:
    out('EQU rFE rFD')
  stack=stack+1
  if var.isalpha():
    getvar(var, 254)
  elif var.isdigit():
    numload(int(var), 254)
  else:
    if getutflen(var[1:])<9:
      numload(int.from_bytes(bytes(var[1:], 'utf-8').ljust(8, b'\x00'), 'big'), 254)
    else:
      print("LONG STRINGS NOT YET IMPLEMENTED.")
def popstack(op):
  global stack
  if op=='+':
    out('ADD rFD rFE rFE')
  elif op=='-':
    out('NEG rFE rFE')
    out('ADD rFD rFE rFE')
  elif op=='*':
    out('MLT rFD rFE rFE')
  elif op=='/':
    out('DIV rFD rFE rFE rFD')
  elif op=='^':
    out('XOR rFD rFE rFE')
  elif op=='%':
    out('DIV rFD rFE rFD rFE')
  elif op=='[':
    out('ADD rFD rFE rFD')
    out('LDR rFE rFD')
  elif op=='<<':
    out('BNS rFD rFE t01')
    out('EQU rFD rFE')
  elif op=='>>':
    out('BNS rFD rFE t01')
    out('EQU rFD rFE')
  elif op=='~':
    out('NEG rFE rFE')
  elif op=='':
    out('EQU rFD rFE')
  if stack>2:
    out("LDA rFD m"+hexj(16+stack-3, 6))
    #out("XOR rFC rFC rFC")
    #out("STA rFC m"+hexj(16+stack-3, 6))
  stack=stack-1
def parse_line(i):
  j=i[0]
  if j=='IF':
    if_loop(i[1:])
  elif j=='ELSE':
    else_loop(i[1:])
  elif j=='WHILE':
    while_loop(i[1:])
  elif j=='GOTO':
    goto_loop(i[1:])
  elif j=='FOR':
    for_loop(i[1:])
  elif j=='LABEL':
    label_stat(i[1])
  elif j=='DEF':
    def_func(i[1][0], i[1][2:-1:2])
  elif j=='RET':
    call_return(funcsc[-1], i[1:])
  elif j=='INT':
    if funcsc[-1]=='~':
      gnames[i[1]]=513+funcs[funcsc[-1]][1]
    else:
      lnames[i[1]]=funcs[funcsc[-1]][1]
    funcs[funcsc[-1]][1]+=1
  elif j=='ARRAY':
    if funcsc[-1]=='~':
      gnames[i[1]]=513+funcs['~'][1]
      numload(gnames[i[1]]+1, 251)
      setvar(i[1], 251)
    else:
      lnames[i[1]]=funcs[funcsc[-1]][1]
      numload(lnames[i[1]]+1, 251)
      out('ADD rFB rF7 rFB')
      setvar(i[1], 251)
    funcs[funcsc[-1]][1]+=1+int(i[2])
  elif j=='ASM':
    asm_embed(i[1:])
  elif j=='}':
    end_loop()
  elif j!='IMPORT':
    evalexp(i)
def parse_block(tokens):
  global statements
  for h in range(len(tokens)):
    i=tokens[h]
    j=i[0]
    if not i:
      continue
    if j=='INT':
      gnames[i[1]]=513+funcs[funcsc[-1]][1]
      funcs[funcsc[-1]][1]+=1
    elif j=='ARRAY':
      gnames[i[1]]=513+funcs['~'][1]
      numload(gnames[i[1]]+1, 251)
      setvar(i[1], 251)
      funcs[funcsc[-1]][1]+=1+int(i[2])
    else:
      statements+=tokens[h:]
      return
def parse_rem(text):
  tokens=tokensToRecursive(textToTokens(text), 0)[0]
  for i in tokens:
    if i[0]=='IMPORT':
      parse_block(tokensToRecursive(textToTokens(open('/Applications/AssemblyOS/alp/'+i[1]+'.alp').read()), 0)[0])
  parse_block(tokens)
  numload(funcs['~'][1], 241)
  out('EQU rFF rF0')
  out('GTO r00 r00 nFFFFFFFC t00')
  out('EQU rF2 rF7')
  for i in statements:
    parse_line(i)
if __name__=="__main__":
  optimize=int(input('OPTIMIZATION LEVEL~'))
  syslib()
  extlib()
  init()
  parse_rem(open(input('FILE NAME~')+'.alp').read())
  for j in gotopos:
    i=gotopos[j]
    x=code[j]
    if abs(j-i[1]-labelpos[i[0]])<2**32:
      code[j]='JMP'+x[3:13]+hexj(abs(j-i[1]-labelpos[i[0]]), 8)
    else:
      print('AAARGH!')
      #probably doesn't work yet.
      code[j]='JMR'+x[3:12]+'rdFA'
      ucode=code[j:]
      code=code[:j]
      numload(abs(j-i[1]-labelpos[i[0]]), 250)
      code=code+ucode
    if j-i[1]-labelpos[i[0]]<0:
      code[j]+=x[21:25]
    else:
      code[j]+=' t1'+x[24]
  code=[i for i in code if i[0:4]!='LBL ']
  file=open(input('OFILE NAME~')+'.asa', mode='w')
  for i in code:
    file.write(i+'\n')
  file.close()
