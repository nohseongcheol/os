#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, သော့တန်ဖိုး 입력은 ကိုယ်ပိုင် အူတိုင်တန်ဖိုး UART로 전달한다. localhost 전용, 단일 ထိန်းချုပ်တန်ဖိုး 클라이언트.
RFB 3.8: https://www.rfc-editor.org/rfc/rfc6143.html
"""
import argparse
from contextlib import ExitStack
from pathlib import Path
import signal
import socket
import struct
import subprocess
import sys
import tempfile
import threading
import time
from စက်မောင်း import အမိန့်
from local_input import create


def 정확한값(ကွန်ရက်ပေါက်တန်ဖိုး, အရွယ်):
    ဒေတာ = bytearray()
    while len(ဒေတာ) < အရွယ်:
        အစိတ်အပိုင်း = ကွန်ရက်ပေါက်တန်ဖိုး.recv(အရွယ် - len(ဒေတာ))
        if not အစိတ်အပိုင်း: raise EOFError()
        ဒေတာ.extend(အစိတ်အပိုင်း)
    return bytes(ဒေတာ)


class လက်ကွက်:
    def __init__(자신, ပို့, 입력방식알림=None):
        자신.လွှဲပြောင်းဘိုက်များ = ပို့; 자신.보조글쇠 = set(); 자신.붙임판 = b''
        자신.한글조합기 = create(ပို့, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.အလှည့်ပြောင်းသော့ = set()
        자신.Unicodeအဝင် = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def ပို့(자신, ဒေတာ):
        자신.한글조합기.조합확정()
        자신.လွှဲပြောင်းဘိုက်များ(ဒေတာ)

    def အလှည့်ပြောင်းနည်းစနစ်(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, သော့သင်္ကေတ):
        if သော့သင်္ကေတ in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.보조글쇠.add(သော့သင်္ကေတ)
            else: 자신.보조글쇠.discard(သော့သင်္ကေတ)
            return
        if not 누르는중:
            자신.အလှည့်ပြောင်းသော့.discard(သော့သင်္ကေတ)
            return
        ထိန်းချုပ်သော့ = bool(자신.보조글쇠 & {0xffe3, 0xffe4})
        ရွှေ့ပြောင်းသော့ = bool(자신.보조글쇠 & {0xffe1, 0xffe2})
        if ထိန်းချုပ်သော့ and ရွှေ့ပြောင်းသော့ and သော့သင်္ကေတ in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.Unicodeအဝင် = ''; return
        if 자신.Unicodeအဝင် is not None:
            if သော့သင်္ကေတ in (32,0xff0d):
                try:
                    တန်ဖိုး=int(자신.Unicodeအဝင်,16)
                    if 32<=တန်ဖိုး<=0x10ffff and not 0xd800<=တန်ဖိုး<=0xdfff: 자신.ပို့(chr(တန်ဖိုး).encode('utf-8'))
                except ValueError: pass
                자신.Unicodeအဝင်=None
            elif သော့သင်္ကေတ==0xff1b: 자신.Unicodeအဝင်=None
            elif သော့သင်္ကေတ==0xff08: 자신.Unicodeအဝင်=자신.Unicodeအဝင်[:-1]
            elif သော့သင်္ကေတ<128 and chr(သော့သင်္ကေတ) in '0123456789abcdefABCDEF' and len(자신.Unicodeအဝင်)<6: 자신.Unicodeအဝင်+=chr(သော့သင်္ကေတ)
            return
        if သော့သင်္ကေတ in (0xff31,0xffc6) or သော့သင်္ကေတ==32 and ရွှေ့ပြောင်းသော့ and not ထိန်းချုပ်သော့:
            if သော့သင်္ကေတ not in 자신.အလှည့်ပြောင်းသော့: 자신.အလှည့်ပြောင်းနည်းစနစ်()
            자신.အလှည့်ပြောင်းသော့.add(သော့သင်္ကေတ)
            return
        if သော့သင်္ကေတ==0xff08 and 자신.한글여부 and not ထိန်းချုပ်သော့ and 자신.한글조합기.앞글자지우기(): return
        if ထိန်းချုပ်သော့ and ရွှေ့ပြောင်းသော့ and သော့သင်္ကေတ in (ord('t'),ord('T')):
            자신.ပို့(bytes([30,2,1,0,0,0,0])); return
        if သော့သင်္ကေတ==0xffc3: 자신.ပို့(bytes([30,2,2,0,0,0,0])); return
        if သော့သင်္ကေတ==0xffc9: 자신.ပို့(bytes([30,2,3,0,0,0,0])); return
        if ထိန်းချုပ်သော့ and ရွှေ့ပြောင်းသော့ and သော့သင်္ကေတ in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.ပို့(자신.붙임판); return
        အထူးသော့ = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if သော့သင်္ကေတ in အထူးသော့: 자신.ပို့(အထူးသော့[သော့သင်္ကေတ]); return
        အက္ခရာကုဒ်သွင်းစနစ် = သော့သင်္ကေတ & 0xffffff if သော့သင်္ကေတ & 0xff000000 == 0x01000000 else သော့သင်္ကေတ
        if အက္ခရာကုဒ်သွင်းစနစ် > 0x10ffff or 0xd800 <= အက္ခရာကုဒ်သွင်းစနစ် <= 0xdfff or သော့သင်္ကေတ >= 0xff00 and သော့သင်္ကေတ < 0x1000000: return
        if ထိန်းချုပ်သော့ and 0x40 <= အက္ခရာကုဒ်သွင်းစနစ် <= 0x7f: 자신.ပို့(bytes([အက္ခရာကုဒ်သွင်းစနစ် & 31])); return
        if အက္ခရာကုဒ်သွင်းစနစ် < 32: return
        if 자신.한글여부 and 자신.보조글쇠 & {0xffea,0xfe03,0xff7e} and not ထိန်းချုပ်သော့ and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.글쇠넣기(chr(အက္ခရာကုဒ်သွင်းစနစ်), altgr=True): return
        앞부분 = b'\x1b' if 자신.보조글쇠 & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not ထိန်းချုပ်သော့ and not 앞부분 and 32<=အက္ခရာကုဒ်သွင်းစနစ်<127:
            အက္ခရာဒေတာ=chr(အက္ခရာကုဒ်သွင်းစနစ်).upper() if ရွှေ့ပြောင်းသော့ else chr(အက္ခရာကုဒ်သွင်းစနစ်)
            if 자신.한글조합기.글쇠넣기(အက္ခရာဒေတာ): return
        자신.ပို့(앞부분 + chr(အက္ခရာကုဒ်သွင်းစနစ်).encode('utf-8'))


class အလုပ်မျက်နှာပြင်ဆက်:
    def __init__(자신, 실행과정):
        자신.실행과정=실행과정; 자신.သော့ခတ်တန်ဖိုး=threading.Lock(); 자신.준비완료=False; 자신.အဆုံးသုံးမျက်နှာပြင်=False; 자신.အစဦးမျက်နှာပြင်=False; 자신.ပိတ်ပြီးသလား=False

    def ပို့(자신, ဒေတာ):
        if not ဒေတာ or 자신.ပိတ်ပြီးသလား: return
        with 자신.သော့ခတ်တန်ဖိုး:
            try: 자신.실행과정.stdin.write(ဒေတာ); 자신.실행과정.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def အစဉ်ဆက်အဝင်အထွက်(자신):
        끝부분=b''
        try:
            while True:
                ဒေတာ=자신.실행과정.stdout.read(4096)
                if not ဒေတာ: break
                sys.stdout.buffer.write(ဒေတာ); sys.stdout.buffer.flush()
                끝부분=(끝부분+ဒေတာ)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); ပိတ်ပြီးသလား=끝부분.rfind(b'TERMINAL CLOSED'); ပုံရေးဆွဲမှုမျက်နှာပြင်=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,ပိတ်ပြီးသလား,ပုံရေးဆွဲမှုမျက်နှာပြင်,종료됨)>=0:
                    자신.အဆုံးသုံးမျက်နှာပြင်=열림>max(ပိတ်ပြီးသလား,ပုံရေးဆွဲမှုမျက်နှာပြင်,종료됨)
                    자신.အစဦးမျက်နှာပြင်=ပုံရေးဆွဲမှုမျက်နှာပြင်>max(열림,ပိတ်ပြီးသလား,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.ပို့(b'terminal\n')
        finally: 자신.ပိတ်ပြီးသလား=True

    def လက်ခံစက်(자신, လက်ခံစက်, လမ်း):
        ဝန်ဆောင်စက်တန်ဖိုး=socket.socket(socket.AF_UNIX); ဝန်ဆောင်စက်တန်ဖိုး.settimeout(10); လက်ခံစက်.settimeout(10)
        လက်ကွက်အချက်=လက်ကွက်(자신.ပို့,lambda 한글여부:자신.ပို့(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            ဝန်ဆောင်စက်တန်ဖိုး.connect(str(လမ်း))
            # အစဦးအခြေအနေ 협상은 순서대로 끝낸다. 이후 အထွက် 가닥만 클라이언트에 쓴다.
            လက်ခံစက်.sendall(정확한값(ဝန်ဆောင်စက်တန်ဖိုး,12))
            ထုတ်ဝေမှုကိန်း=정확한값(လက်ခံစက်,12)
            if ထုတ်ဝေမှုကိန်း not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            ဝန်ဆောင်စက်တန်ဖိုး.sendall(ထုတ်ဝေမှုကိန်း)
            အရေအတွက်=정확한값(ဝန်ဆောင်စက်တန်ဖိုး,1);လက်ခံစက်.sendall(အရေအတွက်+정확한값(ဝန်ဆောင်စက်တန်ဖိုး,အရေအတွက်[0]))
            ကာကွယ်ရေးမူဝါဒ=정확한값(လက်ခံစက်,1)
            if ကာကွယ်ရေးမူဝါဒ!=b'\x01': raise ValueError('unexpected security type')
            ဝန်ဆောင်စက်တန်ဖိုး.sendall(ကာကွယ်ရေးမူဝါဒ)
            if ထုတ်ဝေမှုကိန်း==b'RFB 003.008\n':လက်ခံစက်.sendall(정확한값(ဝန်ဆောင်စက်တန်ဖိုး,4))
            ဝန်ဆောင်စက်တန်ဖိုး.sendall(정확한값(လက်ခံစက်,1))
            အစဦးတန်ဖိုး=정확한값(ဝန်ဆောင်စက်တန်ဖိုး,24)
            လက်ခံစက်.sendall(အစဦးတန်ဖိုး+정확한값(ဝန်ဆောင်စက်တန်ဖိုး,struct.unpack('>I',အစဦးတန်ဖိုး[20:])[0]))
            ပုံမှတ်ဘိုက်များ=အစဦးတန်ဖိုး[4]//8;포인터지원=False
            လက်ခံစက်.settimeout(None);ဝန်ဆောင်စက်တန်ဖိုး.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        분류=정확한값(ဝန်ဆောင်စက်တန်ဖိုး,1)[0]
                        if 분류==0:
                            ဦးခေါင်းတန်ဖိုး=정확한값(ဝန်ဆောင်စက်တန်ဖိုး,3);အချက်အရေအတွက်=struct.unpack('>H',ဦးခေါင်းတန်ဖိုး[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 အဝေးတန်ဖိုး 포인터의 중복을 피한다.
                            숨김=포인터지원
                            if 숨김:လက်ခံစက်.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            လက်ခံစက်.sendall(bytes([분류])+ဦးခေါင်းတန်ဖိုး)
                            for _ in range(အချက်အရေအတွက်):
                                စတုဂံ=정확한값(ဝန်ဆောင်စက်တန်ဖိုး,12);အလျားတည်နေရာ,ဒေါင်လိုက်တည်နေရာ,အကျယ်အဝန်း,အမြင့်တန်ဖိုး,ကုဒ်သွင်းစနစ်တန်ဖိုး=struct.unpack('>HHHHi',စတုဂံ)
                                if ကုဒ်သွင်းစနစ်တန်ဖိုး!=0:raise ValueError('unexpected framebuffer encoding: '+str(ကုဒ်သွင်းစနစ်တန်ဖိုး))
                                လက်ခံစက်.sendall(စတုဂံ)
                                လက်ကျန်ဒေတာ=အကျယ်အဝန်း*အမြင့်တန်ဖိုး*ပုံမှတ်ဘိုက်များ
                                while လက်ကျန်ဒေတာ:
                                    ဒေတာ=정확한값(ဝန်ဆောင်စက်တန်ဖိုး,min(လက်ကျန်ဒေတာ,65536));လက်ခံစက်.sendall(ဒေတာ);လက်ကျန်ဒေတာ-=len(ဒေတာ)
                        elif 분류==1:
                            ဦးခေါင်းတန်ဖိုး=정확한값(ဝန်ဆောင်စက်တန်ဖိုး,5);အရေအတွက်=struct.unpack('>H',ဦးခေါင်းတန်ဖိုး[3:])[0]
                            လက်ခံစက်.sendall(bytes([분류])+ဦးခေါင်းတန်ဖိုး+정확한값(ဝန်ဆောင်စက်တန်ဖိုး,အရေအတွက်*6))
                        elif 분류==2:လက်ခံစက်.sendall(bytes([분류]))
                        elif 분류==3:
                            ဦးခေါင်းတန်ဖိုး=정확한값(ဝန်ဆောင်စက်တန်ဖိုး,7);အရေအတွက်=struct.unpack('>I',ဦးခေါင်းတန်ဖိုး[3:])[0]
                            if အရေအတွက်>1048576:raise ValueError('server clipboard too large')
                            လက်ခံစက်.sendall(bytes([분류])+ဦးခေါင်းတန်ဖိုး+정확한값(ဝန်ဆောင်စက်တန်ဖိုး,အရေအတွက်))
                        else:raise ValueError('unexpected RFB server message: '+str(분류))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:လက်ခံစက်.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            အလုပ်သမား=threading.Thread(target=출력결과,daemon=True);အလုပ်သမား.start()
            while not 자신.ပိတ်ပြီးသလား:
                분류=정확한값(လက်ခံစက်,1)[0]
                if 분류==4:
                    ကိုယ်ထည်စာသား=정확한값(လက်ခံစက်,7); လက်ကွက်အချက်.누름값(ကိုယ်ထည်စာသား[0]!=0,struct.unpack('>I',ကိုယ်ထည်စာသား[3:])[0]); continue
                if 분류==255:
                    ကိုယ်ထည်စာသား=정확한값(လက်ခံစက်,11)
                    if ကိုယ်ထည်စာသား[0]!=0: raise ValueError('unsupported QEMU input extension')
                    လက်ကွက်အချက်.누름값(struct.unpack('>H',ကိုယ်ထည်စာသား[1:3])[0]!=0,struct.unpack('>I',ကိုယ်ထည်စာသား[3:7])[0]); continue
                if 분류==5:
                    ကိုယ်ထည်စာသား=정확한값(လက်ခံစက်,5); 단추들,xတည်နေရာအမှတ်,yတည်နေရာအမှတ်=struct.unpack('>BHH',ကိုယ်ထည်စာသား)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: လက်ကွက်အချက်.한글조합기.조합확정()
                    if 눌림&1 and 자신.အစဦးမျက်နှာပြင် and 64<=xတည်နေရာအမှတ်<576 and 112<=yတည်နေရာအမှတ်<372:
                        ရှာကြည့်အညွှန်းကိန်း=(yတည်နေရာအမှတ်-112)//52
                        if (yတည်နေရာအမှတ်-112)%52<40 and ရှာကြည့်အညွှန်းကိန်း<5: 자신.ပို့(bytes([ord('1')+ရှာကြည့်အညွှန်းကိန်း]))
                    else: 자신.ပို့(bytes([30,1,단추들,xတည်နေရာအမှတ်&255,xတည်နေရာအမှတ်>>8,yတည်နေရာအမှတ်&255,yတည်နေရာအမှတ်>>8]))
                    continue
                if 분류==6:
                    ကိုယ်ထည်စာသား=정확한값(လက်ခံစက်,7); အလျား=struct.unpack('>i',ကိုယ်ထည်စာသား[3:])[0]
                    if abs(အလျား)>65536: raise ValueError('clipboard too large')
                    စာသား=정확한값(လက်ခံစက်,abs(အလျား))
                    if အလျား>=0:
                        try: လက်ကွက်အချက်.붙임판=စာသား.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: လက်ကွက်အချက်.붙임판=စာသား.decode('latin-1').encode('utf-8')
                        လက်ကွက်အချက်.붙임판=လက်ကွက်အချက်.붙임판[:65536].decode('utf-8','ignore').encode('utf-8')
                    ဝန်ဆောင်စက်တန်ဖိုး.sendall(bytes([분류])+ကိုယ်ထည်စာသား+စာသား); continue
                if 분류==0:
                    ကိုယ်ထည်စာသား=정확한값(လက်ခံစက်,19)
                    if ကိုယ်ထည်စာသား[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    ပုံမှတ်ဘိုက်များ=ကိုယ်ထည်စာသား[3]//8
                elif 분류==2:
                    ကိုယ်ထည်စာသား=정확한값(လက်ခံစက်,3); အချက်အရေအတွက်=struct.unpack('>H',ကိုယ်ထည်စာသား[1:])[0]
                    if အချက်အရေအတွက်>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(အချက်အရေအတွက်)+'i',정확한값(လက်ခံစက်,အချက်အရေအတွက်*4))
                    포인터지원=-239 in 부호들
                    # 로컬 မျက်နှာပြင် 중계는 မူလသတ်မှတ်တန်ဖိုး Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    ကိုယ်ထည်စာသား=struct.pack('>BHi',0,1,0)
                elif 분류 in (3,150): ကိုယ်ထည်စာသား=정확한값(လက်ခံစက်,9)
                elif 분류==248:
                    ကိုယ်ထည်စာသား=정확한값(လက်ခံစက်,8)
                    if ကိုယ်ထည်စာသား[7]>64: raise ValueError('fence too large')
                    ကိုယ်ထည်စာသား+=정확한값(လက်ခံစက်,ကိုယ်ထည်စာသား[7])
                elif 분류==250: ကိုယ်ထည်စာသား=정확한값(လက်ခံစက်,3)
                elif 분류==251:
                    ကိုယ်ထည်စာသား=정확한값(လက်ခံစက်,7)
                    if ကိုယ်ထည်စာသား[5]>16: raise ValueError('too many screens')
                    ကိုယ်ထည်စာသား+=정확한값(လက်ခံစက်,ကိုယ်ထည်စာသား[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(분류))
                ဝန်ဆောင်စက်တန်ဖိုး.sendall(bytes([분류])+ကိုယ်ထည်စာသား)
        except (OSError,EOFError,ValueError) as အမှား:
            if str(အမှား): print('VNC client:',အမှား,file=sys.stderr,flush=True)
        finally:
            for ကွန်ရက်ပေါက်တန်ဖိုး in (လက်ခံစက်,ဝန်ဆောင်စက်တန်ဖိုး):
                try: ကွန်ရက်ပေါက်တန်ဖိုး.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                ကွန်ရက်ပေါက်တန်ဖိုး.close()


def အလုပ်မျက်နှာပြင်စက်မောင်း(ဆက်သွယ်ပေါက်ကိန်း=5902, ကွန်ရက်သုံးမှု=False, ဖိုင်လွှဲပြောင်းဆက်သွယ်ပေါက်ကိန်း=2121, 전달규칙들=(), ကြည်လင်ပြတ်သားမှုတန်ဖိုး=(640, 480), ဧည့်သည်လိပ်စာ=None, အိမ်ရှင်လိပ်စာ='127.0.0.1'):
    with ExitStack() as 자원관리, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as လုပ်ဆောင်လမ်း:
        ကွန်ရက်တံတားအချက် = None
        if ကွန်ရက်သုံးမှု:
            from ကွန်ရက်တံတား import ကွန်ရက်တံတား
            ကွန်ရက်တံတားအချက် = 자원관리.enter_context(ကွန်ရက်တံတား(ဖိုင်လွှဲပြောင်းဆက်သွယ်ပေါက်ကိန်း, 전달규칙들, ဧည့်သည်လိပ်စာ=ဧည့်သည်လိပ်စာ, အိမ်ရှင်လိပ်စာ=အိမ်ရှင်လိပ်စာ))
        လမ်း=Path(လုပ်ဆောင်လမ်း)/'display.sock'
        with socket.socket() as ဆက်သွယ်ပေါက်လက်ခံရယူ:
            ဆက်သွယ်ပေါက်လက်ခံရယူ.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            ဆက်သွယ်ပေါက်လက်ခံရယူ.bind(('127.0.0.1',ဆက်သွယ်ပေါက်ကိန်း)); ဆက်သွယ်ပေါက်လက်ခံရယူ.listen(1); ဆက်သွယ်ပေါက်လက်ခံရယူ.settimeout(.2)
            원격화면접속번호=ဆက်သွယ်ပေါက်လက်ခံရယူ.getsockname()[1]
            if ကွန်ရက်တံတားအချက် and (원격화면접속번호==ဖိုင်လွှဲပြောင်းဆက်သွယ်ပေါက်ကိန်း or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and အိမ်ရှင်==원격화면접속번호 for 통신규약,အိမ်ရှင်,_ in ကွန်ရက်တံတားအချက်.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            실행과정=subprocess.Popen(အမိန့်(ကြည်လင်ပြတ်သားမှုတန်ဖိုး)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(လမ်း)]+(ကွန်ရက်တံတားအချက်.전달인수() if ကွန်ရက်တံတားအချက် else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            တံတား=အလုပ်မျက်နှာပြင်ဆက်(실행과정); ဖတ်သူ=threading.Thread(target=တံတား.အစဉ်ဆက်အဝင်အထွက်,daemon=True); ဖတ်သူ.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(ဆက်သွယ်ပေါက်လက်ခံရယူ.getsockname()[1]),flush=True)
            if ကွန်ရက်တံတားအချက်: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(အိမ်ရှင်လိပ်စာ,ဖိုင်လွှဲပြောင်းဆက်သွယ်ပေါက်ကိန်း),flush=True)
            def အဆုံးသတ်(အချက်ပြကိန်း,လုပ်ဆောင်မှုဘောင်): raise KeyboardInterrupt()
            ယခင်=signal.signal(signal.SIGTERM,အဆုံးသတ်)
            လုပ်ငန်းစဉ်ဆောင်ရွက်မှုအလုပ်=None; 가로채기됨=False
            try:
                while 실행과정.poll() is None:
                    try: လက်ခံစက်,_=ဆက်သွယ်ပေါက်လက်ခံရယူ.accept()
                    except socket.timeout: continue
                    if လုပ်ငန်းစဉ်ဆောင်ရွက်မှုအလုပ် is not None and လုပ်ငန်းစဉ်ဆောင်ရွက်မှုအလုပ်.is_alive(): လက်ခံစက်.close(); continue
                    if not လမ်း.exists(): လက်ခံစက်.close(); continue
                    လုပ်ငန်းစဉ်ဆောင်ရွက်မှုအလုပ်=threading.Thread(target=တံတား.လက်ခံစက်,args=(လက်ခံစက်,လမ်း),daemon=True); လုပ်ငန်းစဉ်ဆောင်ရွက်မှုအလုပ်.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                တံတား.ပိတ်ပြီးသလား=True
                if ကွန်ရက်တံတားအချက်: ကွန်ရက်တံတားအချက်.ခဏရပ်ဖြစ်ရပ်.set()
                if 실행과정.poll() is None:
                    실행과정.terminate()
                    try: 실행과정.wait(timeout=5)
                    except subprocess.TimeoutExpired: 실행과정.kill(); 실행과정.wait()
                ဖတ်သူ.join(timeout=2); 실행과정.stdin.close(); 실행과정.stdout.close(); signal.signal(signal.SIGTERM,ယခင်)
            if ကွန်ရက်တံတားအချက် and ကွန်ရက်တံတားအချက်.အမှား: raise RuntimeError('network bridge: '+ကွန်ရက်တံတားအချက်.အမှား)
            return 0 if 가로채기됨 else 실행과정.returncode


if __name__=='__main__':
    from စက်မောင်း import ကြည်လင်ပြတ်သားမှုဖတ်
    인수해석기=argparse.ArgumentParser(description=__doc__); 인수해석기.add_argument('--port',type=int,default=5902)
    인수해석기.add_argument('--resolution',type=ကြည်လင်ပြတ်သားမှုဖတ်,default=(640,480))
    인수해석기.add_argument('--network',action='store_true'); 인수해석기.add_argument('--ftp-port',type=int,default=2121)
    인수해석기.add_argument('--forward',action='append',default=[])
    ပေးအချက်အခင်းအကျင်း=인수해석기.parse_args()
    if ပေးအချက်အခင်းအကျင်း.forward and not ပေးအချက်အခင်းအကျင်း.network: 인수해석기.error('--forward requires --network')
    raise SystemExit(အလုပ်မျက်နှာပြင်စက်မောင်း(ပေးအချက်အခင်းအကျင်း.port,ကွန်ရက်သုံးမှု=ပေးအချက်အခင်းအကျင်း.network,ဖိုင်လွှဲပြောင်းဆက်သွယ်ပေါက်ကိန်း=ပေးအချက်အခင်းအကျင်း.ftp_port,전달규칙들=ပေးအချက်အခင်းအကျင်း.forward,ကြည်လင်ပြတ်သားမှုတန်ဖိုး=ပေးအချက်အခင်းအကျင်း.resolution))
