#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, מקש_ערך 입력은 עצמי ליבה_ערך UART로 전달한다. localhost 전용, 단일 פקד_ערך 클라이언트.
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
from לבצע_פקודה import פקודה
from local_input import create


def 정확한값(소켓, גודל):
    נתונים = bytearray()
    while len(נתונים) < גודל:
        조각 = 소켓.recv(גודל - len(נתונים))
        if not 조각: raise EOFError()
        נתונים.extend(조각)
    return bytes(נתונים)


class מקלדת:
    def __init__(자신, שלח, 입력방식알림=None):
        자신.바이트전송 = שלח; 자신.מקש_צירוף = set(); 자신.לוח_ערך = b''
        자신.한글조합기 = create(שלח, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.מתג_מקש = set()
        자신.יוניקוד_קלט = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def שלח(자신, נתונים):
        자신.한글조합기.조합확정()
        자신.바이트전송(נתונים)

    def מתג_מצב(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, מקש_סימן):
        if מקש_סימן in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.מקש_צירוף.add(מקש_סימן)
            else: 자신.מקש_צירוף.discard(מקש_סימן)
            return
        if not 누르는중:
            자신.מתג_מקש.discard(מקש_סימן)
            return
        מקש_CTRL = bool(자신.מקש_צירוף & {0xffe3, 0xffe4})
        מקש_SHIFT = bool(자신.מקש_צירוף & {0xffe1, 0xffe2})
        if מקש_CTRL and מקש_SHIFT and מקש_סימן in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.יוניקוד_קלט = ''; return
        if 자신.יוניקוד_קלט is not None:
            if מקש_סימן in (32,0xff0d):
                try:
                    ערך=int(자신.יוניקוד_קלט,16)
                    if 32<=ערך<=0x10ffff and not 0xd800<=ערך<=0xdfff: 자신.שלח(chr(ערך).encode('utf-8'))
                except ValueError: pass
                자신.יוניקוד_קלט=None
            elif מקש_סימן==0xff1b: 자신.יוניקוד_קלט=None
            elif מקש_סימן==0xff08: 자신.יוניקוד_קלט=자신.יוניקוד_קלט[:-1]
            elif מקש_סימן<128 and chr(מקש_סימן) in '0123456789abcdefABCDEF' and len(자신.יוניקוד_קלט)<6: 자신.יוניקוד_קלט+=chr(מקש_סימן)
            return
        if מקש_סימן in (0xff31,0xffc6) or מקש_סימן==32 and מקש_SHIFT and not מקש_CTRL:
            if מקש_סימן not in 자신.מתג_מקש: 자신.מתג_מצב()
            자신.מתג_מקש.add(מקש_סימן)
            return
        if מקש_סימן==0xff08 and 자신.한글여부 and not מקש_CTRL and 자신.한글조합기.앞글자지우기(): return
        if מקש_CTRL and מקש_SHIFT and מקש_סימן in (ord('t'),ord('T')):
            자신.שלח(bytes([30,2,1,0,0,0,0])); return
        if מקש_סימן==0xffc3: 자신.שלח(bytes([30,2,2,0,0,0,0])); return
        if מקש_סימן==0xffc9: 자신.שלח(bytes([30,2,3,0,0,0,0])); return
        if מקש_CTRL and מקש_SHIFT and מקש_סימן in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.שלח(자신.לוח_ערך); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if מקש_סימן in 특수글쇠: 자신.שלח(특수글쇠[מקש_סימן]); return
        תו_קידוד = מקש_סימן & 0xffffff if מקש_סימן & 0xff000000 == 0x01000000 else מקש_סימן
        if תו_קידוד > 0x10ffff or 0xd800 <= תו_קידוד <= 0xdfff or מקש_סימן >= 0xff00 and מקש_סימן < 0x1000000: return
        if מקש_CTRL and 0x40 <= תו_קידוד <= 0x7f: 자신.שלח(bytes([תו_קידוד & 31])); return
        if תו_קידוד < 32: return
        if 자신.한글여부 and 자신.מקש_צירוף & {0xffea,0xfe03,0xff7e} and not מקש_CTRL and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.הזנה_מקש(chr(תו_קידוד), altgr=True): return
        앞부분 = b'\x1b' if 자신.מקש_צירוף & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not מקש_CTRL and not 앞부분 and 32<=תו_קידוד<127:
            נתוני_תווים=chr(תו_קידוד).upper() if מקש_SHIFT else chr(תו_קידוד)
            if 자신.한글조합기.הזנה_מקש(נתוני_תווים): return
        자신.שלח(앞부분 + chr(תו_קידוד).encode('utf-8'))


class לקשר_מחשב_שולחני:
    def __init__(자신, תהליך):
        자신.תהליך=תהליך; 자신.נעל_ערך=threading.Lock(); 자신.준비완료=False; 자신.מסוף=False; 자신.시작화면=False; 자신.מערכות_מידע_נסגר=False

    def שלח(자신, נתונים):
        if not נתונים or 자신.מערכות_מידע_נסגר: return
        with 자신.נעל_ערך:
            try: 자신.תהליך.stdin.write(נתונים); 자신.תהליך.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                נתונים=자신.תהליך.stdout.read(4096)
                if not נתונים: break
                sys.stdout.buffer.write(נתונים); sys.stdout.buffer.flush()
                끝부분=(끝부분+נתונים)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); מערכות_מידע_נסגר=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,מערכות_מידע_נסגר,그림화면,종료됨)>=0:
                    자신.מסוף=열림>max(מערכות_מידע_נסגר,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,מערכות_מידע_נסגר,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.שלח(b'terminal\n')
        finally: 자신.מערכות_מידע_נסגר=True

    def לקוח(자신, לקוח, נתיב):
        שרת_ערך=socket.socket(socket.AF_UNIX); שרת_ערך.settimeout(10); לקוח.settimeout(10)
        מקלדת_ערך=מקלדת(자신.שלח,lambda 한글여부:자신.שלח(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            שרת_ערך.connect(str(נתיב))
            # מצב_התחלתי 협상은 순서대로 끝낸다. 이후 פלטטקסט 가닥만 클라이언트에 쓴다.
            לקוח.sendall(정확한값(שרת_ערך,12))
            מספר_גירסה=정확한값(לקוח,12)
            if מספר_גירסה not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            שרת_ערך.sendall(מספר_גירסה)
            개수=정확한값(שרת_ערך,1);לקוח.sendall(개수+정확한값(שרת_ערך,개수[0]))
            אבטחה=정확한값(לקוח,1)
            if אבטחה!=b'\x01': raise ValueError('unexpected security type')
            שרת_ערך.sendall(אבטחה)
            if מספר_גירסה==b'RFB 003.008\n':לקוח.sendall(정확한값(שרת_ערך,4))
            שרת_ערך.sendall(정확한값(לקוח,1))
            초기값=정확한값(שרת_ערך,24)
            לקוח.sendall(초기값+정확한값(שרת_ערך,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            לקוח.settimeout(None);שרת_ערך.settimeout(None)
            def פלט():
                try:
                    while True:
                        אזור_ערך=정확한값(שרת_ערך,1)[0]
                        if אזור_ערך==0:
                            ראש_ערך=정확한값(שרת_ערך,3);항목수=struct.unpack('>H',ראש_ערך[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 מרוחק_ערך 포인터의 중복을 피한다.
                            מוסתר_ערך=포인터지원
                            if מוסתר_ערך:לקוח.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            לקוח.sendall(bytes([אזור_ערך])+ראש_ערך)
                            for _ in range(항목수):
                                מלבן=정확한값(שרת_ערך,12);가로,אנכי_עמדה,폭,גובה_ערך,קידוד_ערך=struct.unpack('>HHHHi',מלבן)
                                if קידוד_ערך!=0:raise ValueError('unexpected framebuffer encoding: '+str(קידוד_ערך))
                                לקוח.sendall(מלבן)
                                남음=폭*גובה_ערך*화소바이트
                                while 남음:
                                    נתונים=정확한값(שרת_ערך,min(남음,65536));לקוח.sendall(נתונים);남음-=len(נתונים)
                        elif אזור_ערך==1:
                            ראש_ערך=정확한값(שרת_ערך,5);개수=struct.unpack('>H',ראש_ערך[3:])[0]
                            לקוח.sendall(bytes([אזור_ערך])+ראש_ערך+정확한값(שרת_ערך,개수*6))
                        elif אזור_ערך==2:לקוח.sendall(bytes([אזור_ערך]))
                        elif אזור_ערך==3:
                            ראש_ערך=정확한값(שרת_ערך,7);개수=struct.unpack('>I',ראש_ערך[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            לקוח.sendall(bytes([אזור_ערך])+ראש_ערך+정확한값(שרת_ערך,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(אזור_ערך))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:לקוח.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            משימתרקע=threading.Thread(target=פלט,daemon=True);משימתרקע.start()
            while not 자신.מערכות_מידע_נסגר:
                אזור_ערך=정확한값(לקוח,1)[0]
                if אזור_ערך==4:
                    גוף_הטקסט=정확한값(לקוח,7); מקלדת_ערך.누름값(גוף_הטקסט[0]!=0,struct.unpack('>I',גוף_הטקסט[3:])[0]); continue
                if אזור_ערך==255:
                    גוף_הטקסט=정확한값(לקוח,11)
                    if גוף_הטקסט[0]!=0: raise ValueError('unsupported QEMU input extension')
                    מקלדת_ערך.누름값(struct.unpack('>H',גוף_הטקסט[1:3])[0]!=0,struct.unpack('>I',גוף_הטקסט[3:7])[0]); continue
                if אזור_ערך==5:
                    גוף_הטקסט=정확한값(לקוח,5); 단추들,קואורדינטת_x,세로좌표=struct.unpack('>BHH',גוף_הטקסט)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: מקלדת_ערך.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=קואורדינטת_x<576 and 112<=세로좌표<372:
                        חפושׂ_מדד=(세로좌표-112)//52
                        if (세로좌표-112)%52<40 and חפושׂ_מדד<5: 자신.שלח(bytes([ord('1')+חפושׂ_מדד]))
                    else: 자신.שלח(bytes([30,1,단추들,קואורדינטת_x&255,קואורדינטת_x>>8,세로좌표&255,세로좌표>>8]))
                    continue
                if אזור_ערך==6:
                    גוף_הטקסט=정확한값(לקוח,7); 길이=struct.unpack('>i',גוף_הטקסט[3:])[0]
                    if abs(길이)>65536: raise ValueError('clipboard too large')
                    טקסט=정확한값(לקוח,abs(길이))
                    if 길이>=0:
                        try: מקלדת_ערך.לוח_ערך=טקסט.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: מקלדת_ערך.לוח_ערך=טקסט.decode('latin-1').encode('utf-8')
                        מקלדת_ערך.לוח_ערך=מקלדת_ערך.לוח_ערך[:65536].decode('utf-8','ignore').encode('utf-8')
                    שרת_ערך.sendall(bytes([אזור_ערך])+גוף_הטקסט+טקסט); continue
                if אזור_ערך==0:
                    גוף_הטקסט=정확한값(לקוח,19)
                    if גוף_הטקסט[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=גוף_הטקסט[3]//8
                elif אזור_ערך==2:
                    גוף_הטקסט=정확한값(לקוח,3); 항목수=struct.unpack('>H',גוף_הטקסט[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(לקוח,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 ערך_ברירת_מחדל Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    גוף_הטקסט=struct.pack('>BHi',0,1,0)
                elif אזור_ערך in (3,150): גוף_הטקסט=정확한값(לקוח,9)
                elif אזור_ערך==248:
                    גוף_הטקסט=정확한값(לקוח,8)
                    if גוף_הטקסט[7]>64: raise ValueError('fence too large')
                    גוף_הטקסט+=정확한값(לקוח,גוף_הטקסט[7])
                elif אזור_ערך==250: גוף_הטקסט=정확한값(לקוח,3)
                elif אזור_ערך==251:
                    גוף_הטקסט=정확한값(לקוח,7)
                    if גוף_הטקסט[5]>16: raise ValueError('too many screens')
                    גוף_הטקסט+=정확한값(לקוח,גוף_הטקסט[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(אזור_ערך))
                שרת_ערך.sendall(bytes([אזור_ערך])+גוף_הטקסט)
        except (OSError,EOFError,ValueError) as שגיאה:
            if str(שגיאה): print('VNC client:',שגיאה,file=sys.stderr,flush=True)
        finally:
            for 소켓 in (לקוח,שרת_ערך):
                try: 소켓.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                소켓.close()


def להפעיל_מחשב_שולחני(מספר_יציאה=5902, רשת=False, העברת_קבצים_מספר_יציאה=2121, 전달규칙들=(), רזולוציה_ערך=(640, 480), אורח_למען=None, ארח_למען='127.0.0.1'):
    with ExitStack() as משאבים, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        גשר_ערך_d01f7493 = None
        if רשת:
            from גשר_3de4fe3a import גשר_3de4fe3a
            גשר_ערך_d01f7493 = משאבים.enter_context(גשר_3de4fe3a(העברת_קבצים_מספר_יציאה, 전달규칙들, אורח_למען=אורח_למען, ארח_למען=ארח_למען))
        נתיב=Path(작업경로)/'display.sock'
        with socket.socket() as לקבל_הסב:
            לקבל_הסב.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            לקבל_הסב.bind(('127.0.0.1',מספר_יציאה)); לקבל_הסב.listen(1); לקבל_הסב.settimeout(.2)
            원격화면접속번호=לקבל_הסב.getsockname()[1]
            if גשר_ערך_d01f7493 and (원격화면접속번호==העברת_קבצים_מספר_יציאה or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and ארח==원격화면접속번호 for 통신규약,ארח,_ in גשר_ערך_d01f7493.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            תהליך=subprocess.Popen(פקודה(רזולוציה_ערך)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(נתיב)]+(גשר_ערך_d01f7493.전달인수() if גשר_ערך_d01f7493 else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            גשר=לקשר_מחשב_שולחני(תהליך); קורא=threading.Thread(target=גשר.직렬입출력,daemon=True); קורא.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(לקבל_הסב.getsockname()[1]),flush=True)
            if גשר_ערך_d01f7493: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(ארח_למען,העברת_קבצים_מספר_יציאה),flush=True)
            def סיום_7f587623(신호번호,실행틀): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,סיום_7f587623)
            עיבוד_משימה=None; 가로채기됨=False
            try:
                while תהליך.poll() is None:
                    try: לקוח,_=לקבל_הסב.accept()
                    except socket.timeout: continue
                    if עיבוד_משימה is not None and עיבוד_משימה.is_alive(): לקוח.close(); continue
                    if not נתיב.exists(): לקוח.close(); continue
                    עיבוד_משימה=threading.Thread(target=גשר.לקוח,args=(לקוח,נתיב),daemon=True); עיבוד_משימה.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                גשר.מערכות_מידע_נסגר=True
                if גשר_ערך_d01f7493: גשר_ערך_d01f7493.השהה_אירוע.set()
                if תהליך.poll() is None:
                    תהליך.terminate()
                    try: תהליך.wait(timeout=5)
                    except subprocess.TimeoutExpired: תהליך.kill(); תהליך.wait()
                קורא.join(timeout=2); תהליך.stdin.close(); תהליך.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if גשר_ערך_d01f7493 and גשר_ערך_d01f7493.שגיאה: raise RuntimeError('network bridge: '+גשר_ערך_d01f7493.שגיאה)
            return 0 if 가로채기됨 else תהליך.returncode


if __name__=='__main__':
    from לבצע_פקודה import 해상도읽기
    מנתח=argparse.ArgumentParser(description=__doc__); מנתח.add_argument('--port',type=int,default=5902)
    מנתח.add_argument('--resolution',type=해상도읽기,default=(640,480))
    מנתח.add_argument('--network',action='store_true'); מנתח.add_argument('--ftp-port',type=int,default=2121)
    מנתח.add_argument('--forward',action='append',default=[])
    ארגומנט_מערך=מנתח.parse_args()
    if ארגומנט_מערך.forward and not ארגומנט_מערך.network: מנתח.error('--forward requires --network')
    raise SystemExit(להפעיל_מחשב_שולחני(ארגומנט_מערך.port,רשת=ארגומנט_מערך.network,העברת_קבצים_מספר_יציאה=ארגומנט_מערך.ftp_port,전달규칙들=ארגומנט_מערך.forward,רזולוציה_ערך=ארגומנט_מערך.resolution))
