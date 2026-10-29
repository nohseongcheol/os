#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, Κλειδί_τιμή 입력은 ίδιο πυρήνας_τιμή UART로 전달한다. localhost 전용, 단일 έλεγχος_τιμή 클라이언트.
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
from εκτελώ_εντολή import Εντολή
from local_input import create


def 정확한값(υποδοχή_τιμή, Μέγεθος):
    δεδομένα = bytearray()
    while len(δεδομένα) < Μέγεθος:
        조각 = υποδοχή_τιμή.recv(Μέγεθος - len(δεδομένα))
        if not 조각: raise EOFError()
        δεδομένα.extend(조각)
    return bytes(δεδομένα)


class πληκτρολόγιο:
    def __init__(자신, στέλνω, 입력방식알림=None):
        자신.바이트전송 = στέλνω; 자신.πλήκτρο_τροποποίησης = set(); 자신.πρόχειρο_τιμή = b''
        자신.한글조합기 = create(στέλνω, Path(__file__).resolve().parents[1]); 자신.한글여부 = False; 자신.αλλάζω_Κλειδί = set()
        자신.유니코드입력 = None
        자신.입력방식알림 = 입력방식알림
        if 입력방식알림: 입력방식알림(False)

    def στέλνω(자신, δεδομένα):
        자신.한글조합기.조합확정()
        자신.바이트전송(δεδομένα)

    def αλλάζω_λειτουργία(자신):
        자신.한글조합기.조합확정(); 자신.한글여부 = not 자신.한글여부
        if 자신.입력방식알림: 자신.입력방식알림(자신.한글여부)

    def 누름값(자신, 누르는중, Κλειδί_σύμβολο):
        if Κλειδί_σύμβολο in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if 누르는중: 자신.πλήκτρο_τροποποίησης.add(Κλειδί_σύμβολο)
            else: 자신.πλήκτρο_τροποποίησης.discard(Κλειδί_σύμβολο)
            return
        if not 누르는중:
            자신.αλλάζω_Κλειδί.discard(Κλειδί_σύμβολο)
            return
        πλήκτρο_Ctrl = bool(자신.πλήκτρο_τροποποίησης & {0xffe3, 0xffe4})
        πλήκτρο_SHIFT = bool(자신.πλήκτρο_τροποποίησης & {0xffe1, 0xffe2})
        if πλήκτρο_Ctrl and πλήκτρο_SHIFT and Κλειδί_σύμβολο in (ord('u'),ord('U')):
            자신.한글조합기.조합확정(); 자신.유니코드입력 = ''; return
        if 자신.유니코드입력 is not None:
            if Κλειδί_σύμβολο in (32,0xff0d):
                try:
                    τιμή=int(자신.유니코드입력,16)
                    if 32<=τιμή<=0x10ffff and not 0xd800<=τιμή<=0xdfff: 자신.στέλνω(chr(τιμή).encode('utf-8'))
                except ValueError: pass
                자신.유니코드입력=None
            elif Κλειδί_σύμβολο==0xff1b: 자신.유니코드입력=None
            elif Κλειδί_σύμβολο==0xff08: 자신.유니코드입력=자신.유니코드입력[:-1]
            elif Κλειδί_σύμβολο<128 and chr(Κλειδί_σύμβολο) in '0123456789abcdefABCDEF' and len(자신.유니코드입력)<6: 자신.유니코드입력+=chr(Κλειδί_σύμβολο)
            return
        if Κλειδί_σύμβολο in (0xff31,0xffc6) or Κλειδί_σύμβολο==32 and πλήκτρο_SHIFT and not πλήκτρο_Ctrl:
            if Κλειδί_σύμβολο not in 자신.αλλάζω_Κλειδί: 자신.αλλάζω_λειτουργία()
            자신.αλλάζω_Κλειδί.add(Κλειδί_σύμβολο)
            return
        if Κλειδί_σύμβολο==0xff08 and 자신.한글여부 and not πλήκτρο_Ctrl and 자신.한글조합기.앞글자지우기(): return
        if πλήκτρο_Ctrl and πλήκτρο_SHIFT and Κλειδί_σύμβολο in (ord('t'),ord('T')):
            자신.στέλνω(bytes([30,2,1,0,0,0,0])); return
        if Κλειδί_σύμβολο==0xffc3: 자신.στέλνω(bytes([30,2,2,0,0,0,0])); return
        if Κλειδί_σύμβολο==0xffc9: 자신.στέλνω(bytes([30,2,3,0,0,0,0])); return
        if πλήκτρο_Ctrl and πλήκτρο_SHIFT and Κλειδί_σύμβολο in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            자신.στέλνω(자신.πρόχειρο_τιμή); return
        특수글쇠 = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if Κλειδί_σύμβολο in 특수글쇠: 자신.στέλνω(특수글쇠[Κλειδί_σύμβολο]); return
        κωδικοποίηση_χαρακτήρα = Κλειδί_σύμβολο & 0xffffff if Κλειδί_σύμβολο & 0xff000000 == 0x01000000 else Κλειδί_σύμβολο
        if κωδικοποίηση_χαρακτήρα > 0x10ffff or 0xd800 <= κωδικοποίηση_χαρακτήρα <= 0xdfff or Κλειδί_σύμβολο >= 0xff00 and Κλειδί_σύμβολο < 0x1000000: return
        if πλήκτρο_Ctrl and 0x40 <= κωδικοποίηση_χαρακτήρα <= 0x7f: 자신.στέλνω(bytes([κωδικοποίηση_χαρακτήρα & 31])); return
        if κωδικοποίηση_χαρακτήρα < 32: return
        if 자신.한글여부 and 자신.πλήκτρο_τροποποίησης & {0xffea,0xfe03,0xff7e} and not πλήκτρο_Ctrl and hasattr(자신.한글조합기, 'profile'):
            if 자신.한글조합기.τροφοδοσία_Κλειδί(chr(κωδικοποίηση_χαρακτήρα), altgr=True): return
        앞부분 = b'\x1b' if 자신.πλήκτρο_τροποποίησης & {0xffe9, 0xffea} else b''
        if 자신.한글여부 and not πλήκτρο_Ctrl and not 앞부분 and 32<=κωδικοποίηση_χαρακτήρα<127:
            δεδομένα_χαρακτήρων=chr(κωδικοποίηση_χαρακτήρα).upper() if πλήκτρο_SHIFT else chr(κωδικοποίηση_χαρακτήρα)
            if 자신.한글조합기.τροφοδοσία_Κλειδί(δεδομένα_χαρακτήρων): return
        자신.στέλνω(앞부분 + chr(κωδικοποίηση_χαρακτήρα).encode('utf-8'))


class συνδέω_υπολογιστής:
    def __init__(자신, Διεργασία):
        자신.Διεργασία=Διεργασία; 자신.κλείδωμα_τιμή=threading.Lock(); 자신.준비완료=False; 자신.Τερματικό=False; 자신.시작화면=False; 자신.πληροφοριακά_συστήματα_κλειστή=False

    def στέλνω(자신, δεδομένα):
        if not δεδομένα or 자신.πληροφοριακά_συστήματα_κλειστή: return
        with 자신.κλείδωμα_τιμή:
            try: 자신.Διεργασία.stdin.write(δεδομένα); 자신.Διεργασία.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def 직렬입출력(자신):
        끝부분=b''
        try:
            while True:
                δεδομένα=자신.Διεργασία.stdout.read(4096)
                if not δεδομένα: break
                sys.stdout.buffer.write(δεδομένα); sys.stdout.buffer.flush()
                끝부분=(끝부분+δεδομένα)[-8192:]
                열림=끝부분.rfind(b'TERMINAL READY'); πληροφοριακά_συστήματα_κλειστή=끝부분.rfind(b'TERMINAL CLOSED'); 그림화면=끝부분.rfind(b'GUI READY:'); 종료됨=끝부분.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(열림,πληροφοριακά_συστήματα_κλειστή,그림화면,종료됨)>=0:
                    자신.Τερματικό=열림>max(πληροφοριακά_συστήματα_κλειστή,그림화면,종료됨)
                    자신.시작화면=그림화면>max(열림,πληροφοριακά_συστήματα_κλειστή,종료됨)
                if not 자신.준비완료 and b'jkoros-native> ' in 끝부분:
                    자신.준비완료=True; 자신.στέλνω(b'terminal\n')
        finally: 자신.πληροφοριακά_συστήματα_κλειστή=True

    def πελάτης(자신, πελάτης, ΔΙΑΔΡΟΜΗ):
        διακομιστής_τιμή=socket.socket(socket.AF_UNIX); διακομιστής_τιμή.settimeout(10); πελάτης.settimeout(10)
        πληκτρολόγιο_καταχώρηση=πληκτρολόγιο(자신.στέλνω,lambda 한글여부:자신.στέλνω(bytes([30,3,int(한글여부),0,0,0,0])))
        이전단추=0
        try:
            διακομιστής_τιμή.connect(str(ΔΙΑΔΡΟΜΗ))
            # αρχική_κατάσταση 협상은 순서대로 끝낸다. 이후 Έξοδος 가닥만 클라이언트에 쓴다.
            πελάτης.sendall(정확한값(διακομιστής_τιμή,12))
            αριθμός_έκδοσης=정확한값(πελάτης,12)
            if αριθμός_έκδοσης not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            διακομιστής_τιμή.sendall(αριθμός_έκδοσης)
            개수=정확한값(διακομιστής_τιμή,1);πελάτης.sendall(개수+정확한값(διακομιστής_τιμή,개수[0]))
            Ασφάλεια=정확한값(πελάτης,1)
            if Ασφάλεια!=b'\x01': raise ValueError('unexpected security type')
            διακομιστής_τιμή.sendall(Ασφάλεια)
            if αριθμός_έκδοσης==b'RFB 003.008\n':πελάτης.sendall(정확한값(διακομιστής_τιμή,4))
            διακομιστής_τιμή.sendall(정확한값(πελάτης,1))
            초기값=정확한값(διακομιστής_τιμή,24)
            πελάτης.sendall(초기값+정확한값(διακομιστής_τιμή,struct.unpack('>I',초기값[20:])[0]))
            화소바이트=초기값[4]//8;포인터지원=False
            πελάτης.settimeout(None);διακομιστής_τιμή.settimeout(None)
            def 출력결과():
                try:
                    while True:
                        περιοχή_τιμή=정확한값(διακομιστής_τιμή,1)[0]
                        if περιοχή_τιμή==0:
                            머리=정확한값(διακομιστής_τιμή,3);항목수=struct.unpack('>H',머리[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 απομακρυσμένος_τιμή 포인터의 중복을 피한다.
                            Κρυφή_τιμή=포인터지원
                            if Κρυφή_τιμή:πελάτης.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            πελάτης.sendall(bytes([περιοχή_τιμή])+머리)
                            for _ in range(항목수):
                                ορθογώνιο=정확한값(διακομιστής_τιμή,12);가로,τομέας_θέση,폭,ύψος_τιμή,κωδικοποίηση_τιμή=struct.unpack('>HHHHi',ορθογώνιο)
                                if κωδικοποίηση_τιμή!=0:raise ValueError('unexpected framebuffer encoding: '+str(κωδικοποίηση_τιμή))
                                πελάτης.sendall(ορθογώνιο)
                                남음=폭*ύψος_τιμή*화소바이트
                                while 남음:
                                    δεδομένα=정확한값(διακομιστής_τιμή,min(남음,65536));πελάτης.sendall(δεδομένα);남음-=len(δεδομένα)
                        elif περιοχή_τιμή==1:
                            머리=정확한값(διακομιστής_τιμή,5);개수=struct.unpack('>H',머리[3:])[0]
                            πελάτης.sendall(bytes([περιοχή_τιμή])+머리+정확한값(διακομιστής_τιμή,개수*6))
                        elif περιοχή_τιμή==2:πελάτης.sendall(bytes([περιοχή_τιμή]))
                        elif περιοχή_τιμή==3:
                            머리=정확한값(διακομιστής_τιμή,7);개수=struct.unpack('>I',머리[3:])[0]
                            if 개수>1048576:raise ValueError('server clipboard too large')
                            πελάτης.sendall(bytes([περιοχή_τιμή])+머리+정확한값(διακομιστής_τιμή,개수))
                        else:raise ValueError('unexpected RFB server message: '+str(περιοχή_τιμή))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:πελάτης.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            작업가닥=threading.Thread(target=출력결과,daemon=True);작업가닥.start()
            while not 자신.πληροφοριακά_συστήματα_κλειστή:
                περιοχή_τιμή=정확한값(πελάτης,1)[0]
                if περιοχή_τιμή==4:
                    σώμα_κειμένου=정확한값(πελάτης,7); πληκτρολόγιο_καταχώρηση.누름값(σώμα_κειμένου[0]!=0,struct.unpack('>I',σώμα_κειμένου[3:])[0]); continue
                if περιοχή_τιμή==255:
                    σώμα_κειμένου=정확한값(πελάτης,11)
                    if σώμα_κειμένου[0]!=0: raise ValueError('unsupported QEMU input extension')
                    πληκτρολόγιο_καταχώρηση.누름값(struct.unpack('>H',σώμα_κειμένου[1:3])[0]!=0,struct.unpack('>I',σώμα_κειμένου[3:7])[0]); continue
                if περιοχή_τιμή==5:
                    σώμα_κειμένου=정확한값(πελάτης,5); 단추들,συντεταγμένη_x,κουμπί_Y_συντονισμός=struct.unpack('>BHH',σώμα_κειμένου)
                    눌림=단추들&~이전단추; 이전단추=단추들
                    if 눌림: πληκτρολόγιο_καταχώρηση.한글조합기.조합확정()
                    if 눌림&1 and 자신.시작화면 and 64<=συντεταγμένη_x<576 and 112<=κουμπί_Y_συντονισμός<372:
                        Αναζήτηση_Ευρετήριο=(κουμπί_Y_συντονισμός-112)//52
                        if (κουμπί_Y_συντονισμός-112)%52<40 and Αναζήτηση_Ευρετήριο<5: 자신.στέλνω(bytes([ord('1')+Αναζήτηση_Ευρετήριο]))
                    else: 자신.στέλνω(bytes([30,1,단추들,συντεταγμένη_x&255,συντεταγμένη_x>>8,κουμπί_Y_συντονισμός&255,κουμπί_Y_συντονισμός>>8]))
                    continue
                if περιοχή_τιμή==6:
                    σώμα_κειμένου=정확한값(πελάτης,7); διάρκεια_τιμή=struct.unpack('>i',σώμα_κειμένου[3:])[0]
                    if abs(διάρκεια_τιμή)>65536: raise ValueError('clipboard too large')
                    Κείμενο=정확한값(πελάτης,abs(διάρκεια_τιμή))
                    if διάρκεια_τιμή>=0:
                        try: πληκτρολόγιο_καταχώρηση.πρόχειρο_τιμή=Κείμενο.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: πληκτρολόγιο_καταχώρηση.πρόχειρο_τιμή=Κείμενο.decode('latin-1').encode('utf-8')
                        πληκτρολόγιο_καταχώρηση.πρόχειρο_τιμή=πληκτρολόγιο_καταχώρηση.πρόχειρο_τιμή[:65536].decode('utf-8','ignore').encode('utf-8')
                    διακομιστής_τιμή.sendall(bytes([περιοχή_τιμή])+σώμα_κειμένου+Κείμενο); continue
                if περιοχή_τιμή==0:
                    σώμα_κειμένου=정확한값(πελάτης,19)
                    if σώμα_κειμένου[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    화소바이트=σώμα_κειμένου[3]//8
                elif περιοχή_τιμή==2:
                    σώμα_κειμένου=정확한값(πελάτης,3); 항목수=struct.unpack('>H',σώμα_κειμένου[1:])[0]
                    if 항목수>512: raise ValueError('too many encodings')
                    부호들=struct.unpack('>'+str(항목수)+'i',정확한값(πελάτης,항목수*4))
                    포인터지원=-239 in 부호들
                    # 로컬 화면 중계는 προεπιλεγμένη_τιμή Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    σώμα_κειμένου=struct.pack('>BHi',0,1,0)
                elif περιοχή_τιμή in (3,150): σώμα_κειμένου=정확한값(πελάτης,9)
                elif περιοχή_τιμή==248:
                    σώμα_κειμένου=정확한값(πελάτης,8)
                    if σώμα_κειμένου[7]>64: raise ValueError('fence too large')
                    σώμα_κειμένου+=정확한값(πελάτης,σώμα_κειμένου[7])
                elif περιοχή_τιμή==250: σώμα_κειμένου=정확한값(πελάτης,3)
                elif περιοχή_τιμή==251:
                    σώμα_κειμένου=정확한값(πελάτης,7)
                    if σώμα_κειμένου[5]>16: raise ValueError('too many screens')
                    σώμα_κειμένου+=정확한값(πελάτης,σώμα_κειμένου[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(περιοχή_τιμή))
                διακομιστής_τιμή.sendall(bytes([περιοχή_τιμή])+σώμα_κειμένου)
        except (OSError,EOFError,ValueError) as ΣΦΑΛΜΑ:
            if str(ΣΦΑΛΜΑ): print('VNC client:',ΣΦΑΛΜΑ,file=sys.stderr,flush=True)
        finally:
            for υποδοχή_τιμή in (πελάτης,διακομιστής_τιμή):
                try: υποδοχή_τιμή.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                υποδοχή_τιμή.close()


def εκτελώ_υπολογιστής(αριθμός_θύρας=5902, δίκτυο=False, μεταφορά_αρχείων_αριθμός_θύρας=2121, 전달규칙들=(), ανάλυση_τιμή=(640, 480), Επισκέπτης_διεύθυνση=None, φιλοξενώ_διεύθυνση='127.0.0.1'):
    with ExitStack() as Πόροι, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as 작업경로:
        γέφυρα_καταχώρηση = None
        if δίκτυο:
            from γέφυρα_3de4fe3a import γέφυρα_3de4fe3a
            γέφυρα_καταχώρηση = Πόροι.enter_context(γέφυρα_3de4fe3a(μεταφορά_αρχείων_αριθμός_θύρας, 전달규칙들, Επισκέπτης_διεύθυνση=Επισκέπτης_διεύθυνση, φιλοξενώ_διεύθυνση=φιλοξενώ_διεύθυνση))
        ΔΙΑΔΡΟΜΗ=Path(작업경로)/'display.sock'
        with socket.socket() as λαμβάνω_θύρα:
            λαμβάνω_θύρα.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            λαμβάνω_θύρα.bind(('127.0.0.1',αριθμός_θύρας)); λαμβάνω_θύρα.listen(1); λαμβάνω_θύρα.settimeout(.2)
            원격화면접속번호=λαμβάνω_θύρα.getsockname()[1]
            if γέφυρα_καταχώρηση and (원격화면접속번호==μεταφορά_αρχείων_αριθμός_θύρας or 50000<=원격화면접속번호<=50007 or any(통신규약=='tcp' and φιλοξενώ==원격화면접속번호 for 통신규약,φιλοξενώ,_ in γέφυρα_καταχώρηση.전달규칙들)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            Διεργασία=subprocess.Popen(Εντολή(ανάλυση_τιμή)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(ΔΙΑΔΡΟΜΗ)]+(γέφυρα_καταχώρηση.전달인수() if γέφυρα_καταχώρηση else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            γέφυρα=συνδέω_υπολογιστής(Διεργασία); Αναγνώστης=threading.Thread(target=γέφυρα.직렬입출력,daemon=True); Αναγνώστης.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(λαμβάνω_θύρα.getsockname()[1]),flush=True)
            if γέφυρα_καταχώρηση: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(φιλοξενώ_διεύθυνση,μεταφορά_αρχείων_αριθμός_θύρας),flush=True)
            def τερματίζω(신호번호,εκτέλεση_κάδρο): raise KeyboardInterrupt()
            이전항목=signal.signal(signal.SIGTERM,τερματίζω)
            επεξεργασία_εργασία=None; 가로채기됨=False
            try:
                while Διεργασία.poll() is None:
                    try: πελάτης,_=λαμβάνω_θύρα.accept()
                    except socket.timeout: continue
                    if επεξεργασία_εργασία is not None and επεξεργασία_εργασία.is_alive(): πελάτης.close(); continue
                    if not ΔΙΑΔΡΟΜΗ.exists(): πελάτης.close(); continue
                    επεξεργασία_εργασία=threading.Thread(target=γέφυρα.πελάτης,args=(πελάτης,ΔΙΑΔΡΟΜΗ),daemon=True); επεξεργασία_εργασία.start()
            except KeyboardInterrupt: 가로채기됨=True
            finally:
                γέφυρα.πληροφοριακά_συστήματα_κλειστή=True
                if γέφυρα_καταχώρηση: γέφυρα_καταχώρηση.Παύση_συμβάν.set()
                if Διεργασία.poll() is None:
                    Διεργασία.terminate()
                    try: Διεργασία.wait(timeout=5)
                    except subprocess.TimeoutExpired: Διεργασία.kill(); Διεργασία.wait()
                Αναγνώστης.join(timeout=2); Διεργασία.stdin.close(); Διεργασία.stdout.close(); signal.signal(signal.SIGTERM,이전항목)
            if γέφυρα_καταχώρηση and γέφυρα_καταχώρηση.ΣΦΑΛΜΑ: raise RuntimeError('network bridge: '+γέφυρα_καταχώρηση.ΣΦΑΛΜΑ)
            return 0 if 가로채기됨 else Διεργασία.returncode


if __name__=='__main__':
    from εκτελώ_εντολή import 해상도읽기
    ανάλυση=argparse.ArgumentParser(description=__doc__); ανάλυση.add_argument('--port',type=int,default=5902)
    ανάλυση.add_argument('--resolution',type=해상도읽기,default=(640,480))
    ανάλυση.add_argument('--network',action='store_true'); ανάλυση.add_argument('--ftp-port',type=int,default=2121)
    ανάλυση.add_argument('--forward',action='append',default=[])
    όρισμα_πίνακας=ανάλυση.parse_args()
    if όρισμα_πίνακας.forward and not όρισμα_πίνακας.network: ανάλυση.error('--forward requires --network')
    raise SystemExit(εκτελώ_υπολογιστής(όρισμα_πίνακας.port,δίκτυο=όρισμα_πίνακας.network,μεταφορά_αρχείων_αριθμός_θύρας=όρισμα_πίνακας.ftp_port,전달규칙들=όρισμα_πίνακας.forward,ανάλυση_τιμή=όρισμα_πίνακας.resolution))
