#!/usr/bin/env python3
"""πραγματικός_δεδομένα RFB 클라이언트로 QEMU 창의 한글/Κλειδί_τιμή/클립보드/마우스와 화면 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from υπολογιστής_Προβολή import 정확한값
from εκτελώ_εντολή import έργο_ρίζα


def Εκτέλεση_2():
    출력결과=έργο_ρίζα/'build/verification/desktop'; 출력결과.mkdir(parents=True,exist_ok=True)
    Διεργασία=subprocess.Popen(['python3',str(έργο_ρίζα/'Εργαλεία/υπολογιστής_Προβολή.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비살피미=selectors.DefaultSelector(); 준비살피미.register(Διεργασία.stdout,selectors.EVENT_READ)
    μεταγραφή=bytearray(); επικύρωση_έκθεση={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((έργο_ρίζα/'build/kernel8.img').read_bytes()).hexdigest()}
    def 까지(δείκτης_8b722c5f,Εκτέλεση_2=0):
        προθεσμία_ώρα=time.monotonic()+45
        while δείκτης_8b722c5f not in μεταγραφή[Εκτέλεση_2:]:
            if time.monotonic()>προθεσμία_ώρα or Διεργασία.poll() is not None: raise AssertionError(μεταγραφή[Εκτέλεση_2:].decode('utf-8','replace'))
            for 누름값,_ in 준비살피미.select(.1):
                δεδομένα=누름값.fileobj.read(4096)
                if δεδομένα: μεταγραφή.extend(δεδομένα)
        return bytes(μεταγραφή[Εκτέλεση_2:])
    try:
        까지(b'TERMINAL READY')
        αριθμός_θύρας=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',μεταγραφή).group(1))
        with socket.create_connection(('127.0.0.1',αριθμός_θύρας),timeout=10) as πελάτης:
            assert 정확한값(πελάτης,12)==b'RFB 003.008\n'; πελάτης.sendall(b'RFB 003.008\n')
            assert 1 in 정확한값(πελάτης,정확한값(πελάτης,1)[0]); πελάτης.sendall(b'\x01'); assert 정확한값(πελάτης,4)==b'\0'*4
            πελάτης.sendall(b'\x01'); 초기값=정확한값(πελάτης,24); assert struct.unpack('>HH',초기값[:4])==(640,480); 정확한값(πελάτης,struct.unpack('>I',초기값[20:])[0])
            πελάτης.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            πελάτης.sendall(struct.pack('>BBHi',2,0,1,0))
            def 누름값(σύμβολο_τιμή,누르는중=True): πελάτης.sendall(struct.pack('>BBHI',4,int(누르는중),0,σύμβολο_τιμή))
            def 글자입력(Κείμενο):
                for δεδομένα_χαρακτήρων in Κείμενο:
                    σύμβολο=0xff0d if δεδομένα_χαρακτήρων=='\n' else ord(δεδομένα_χαρακτήρων) if ord(δεδομένα_χαρακτήρων)<256 else 0x01000000|ord(δεδομένα_χαρακτήρων)
                    누름값(σύμβολο); 누름값(σύμβολο,False)
            def 글쇠누르기(σύμβολο_τιμή): 누름값(σύμβολο_τιμή); 누름값(σύμβολο_τιμή,False)
            # Start with English keys only, as delivered without a host IME.
            Υπέρθεση_τιμή=len(μεταγραφή); 글자입력('echo '); 글쇠누르기(0xffc6)
            글자입력('dkssudgktpdy gksrmf'); 글쇠누르기(0xffc6); 글자입력('\n')
            까지('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),Υπέρθεση_τιμή)
            Υπέρθεση_τιμή=len(μεταγραφή); 글자입력('echo ')
            누름값(0xffe1); 글쇠누르기(32); 누름값(0xffe1,False)
            글자입력('dlfr'); 글쇠누르기(0xff08); 글쇠누르기(0xff08); 글자입력('fr')
            글쇠누르기(0xff31); 글자입력(' EN\n')
            까지('\r\n읽 EN\r\njkoros-native> '.encode(),Υπέρθεση_τιμή)
            Υπέρθεση_τιμή=len(μεταγραφή); 글자입력('echo '); 글쇠누르기(0xff31)
            글자입력('rhk rkqtk RkRnd'); 글쇠누르기(0xff31); 글자입력('\n')
            까지('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),Υπέρθεση_τιμή)
            # The same composition edits UTF-8 text in the native vi editor.
            Υπέρθεση_τιμή=len(μεταγραφή); 글자입력('vi 한글입력.txt\n'); 까지(b'NORMAL',Υπέρθεση_τιμή)
            글자입력('i'); 글쇠누르기(0xffc6); 글자입력('gksrmf dlfr'); 글쇠누르기(0xffc6)
            글쇠누르기(0xff1b); 글자입력(':wq\n'); 까지(b'jkoros-native> ',Υπέρθεση_τιμή)
            Υπέρθεση_τιμή=len(μεταγραφή); 글자입력('cat 한글입력.txt\n')
            까지('한글 읽'.encode(),Υπέρθεση_τιμή); 까지(b'jkoros-native> ',Υπέρθεση_τιμή)
            Υπέρθεση_τιμή=len(μεταγραφή); 글자입력('help ko\n')
            까지('한/μηδέν_τελεστέος Κλειδί_τιμή, Shift+Space 또는 F9'.encode(),Υπέρθεση_τιμή); 까지(b'jkoros-native> ',Υπέρθεση_τιμή)
            Υπέρθεση_τιμή=len(μεταγραφή); 글자입력('clear\necho "VNC 한글 είσοδος_τιμή 😀"\n'); 까지('VNC 한글 είσοδος_τιμή 😀\r\n'.encode(),Υπέρθεση_τιμή)
            Υπέρθεση_τιμή=len(μεταγραφή); 누름값(0xffe3); 누름값(ord('u')); 누름값(ord('u'),False); 누름값(0xffe3,False); 글자입력('echo CONTROL_OK\n'); 까지(b'\r\nCONTROL_OK\r\n',Υπέρθεση_τιμή)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            πρόχειρο_τιμή='echo "επικολλώ_τιμή 완료"\n'.encode(); Υπέρθεση_τιμή=len(μεταγραφή)
            πελάτης.sendall(struct.pack('>B3xI',6,len(πρόχειρο_τιμή))+πρόχειρο_τιμή)
            for Συμβάν,_ in 준비살피미.select(.15):
                μπλοκ_δεδομένων=Συμβάν.fileobj.read(4096)
                if μπλοκ_δεδομένων: μεταγραφή.extend(μπλοκ_δεδομένων)
            assert 'επικολλώ_τιμή 완료'.encode() not in μεταγραφή[Υπέρθεση_τιμή:]
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('v')); 누름값(ord('v'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            까지('\r\n붙여넣기 완료\r\njkoros-native> '.encode(),Υπέρθεση_τιμή)
            πελάτης.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            빛삼원색=bytearray(640*480*3); 본항목들=False
            while not 본항목들:
                γνωστοποίηση_μήνυμα=정확한값(πελάτης,1)[0]
                if γνωστοποίηση_μήνυμα==2: continue
                if γνωστοποίηση_μήνυμα==3:
                    Μέγεθος=struct.unpack('>I',정확한값(πελάτης,7)[3:])[0]; 정확한값(πελάτης,Μέγεθος); continue
                assert γνωστοποίηση_μήνυμα==0,γνωστοποίηση_μήνυμα
                사각형들=struct.unpack('>H',정확한값(πελάτης,3)[1:])[0]
                for _ in range(사각형들):
                    συντεταγμένη_x,κουμπί_Y_συντονισμός,너비값,ζητήθηκε_ύψος_τιμή,σύνολο_χαρακτήρων=struct.unpack('>HHHHi',정확한값(πελάτης,12)); assert σύνολο_χαρακτήρων==0,σύνολο_χαρακτήρων
                    화소들=정확한값(πελάτης,너비값*ζητήθηκε_ύψος_τιμή*4)
                    for 안쪽순번 in range(ζητήθηκε_ύψος_τιμή):
                        for 순번 in range(너비값):
                            원본주소=(안쪽순번*너비값+순번)*4; προορισμός_διεύθυνση=((κουμπί_Y_συντονισμός+안쪽순번)*640+συντεταγμένη_x+순번)*3
                            빛삼원색[προορισμός_διεύθυνση:προορισμός_διεύθυνση+3]=bytes((화소들[원본주소+2],화소들[원본주소+1],화소들[원본주소]))
                    본항목들=True
            assert 빛삼원색[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (출력결과/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+빛삼원색)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(출력결과/'vnc-terminal.png'))
            Υπέρθεση_τιμή=len(μεταγραφή)
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('t')); 누름값(ord('t'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            까지(b'TERMINAL FOCUS 2',Υπέρθεση_τιμή)
            Υπέρθεση_τιμή=len(μεταγραφή); 글자입력('echo SECOND_VNC_WINDOW\n'); 까지(b'\r\nSECOND_VNC_WINDOW\r\n',Υπέρθεση_τιμή)
            Υπέρθεση_τιμή=len(μεταγραφή); πελάτης.sendall(struct.pack('>BBHH',5,1,576,81)); πελάτης.sendall(struct.pack('>BBHH',5,0,576,81)); 까지(b'TERMINAL FOCUS 1',Υπέρθεση_τιμή)
            Υπέρθεση_τιμή=len(μεταγραφή); 글자입력('python -c \'print("x"*9000)\'\n'); 까지(b'\r\njkoros-native> ',Υπέρθεση_τιμή)
            assert len(μεταγραφή)-Υπέρθεση_τιμή>8192,'exercise output longer than bridge status buffer'
            Υπέρθεση_τιμή=len(μεταγραφή); πελάτης.sendall(struct.pack('>BBHH',5,1,560,63)); πελάτης.sendall(struct.pack('>BBHH',5,0,560,63)); 까지(b'TERMINAL FOCUS 1',Υπέρθεση_τιμή)
            Υπέρθεση_τιμή=len(μεταγραφή); πελάτης.sendall(struct.pack('>BBHH',5,1,80,16)); πελάτης.sendall(struct.pack('>BBHH',5,0,80,16)); 까지(b'TERMINAL FOCUS 1',Υπέρθεση_τιμή)
            Υπέρθεση_τιμή=len(μεταγραφή); 글자입력('echo REOPENED_VNC_WINDOW\n'); 까지(b'\r\nREOPENED_VNC_WINDOW\r\n',Υπέρθεση_τιμή)
            Υπέρθεση_τιμή=len(μεταγραφή); 글자입력('gui\n'); 까지(b'GUI READY:',Υπέρθεση_τιμή)
            Υπέρθεση_τιμή=len(μεταγραφή); πελάτης.sendall(struct.pack('>BBHH',5,1,80,332)); πελάτης.sendall(struct.pack('>BBHH',5,0,80,332)); 까지(b'TERMINAL READY',Υπέρθεση_τιμή)
            επικύρωση_έκθεση.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if Διεργασία.poll() is None:
            Διεργασία.terminate()
            try: Διεργασία.wait(timeout=8)
            except subprocess.TimeoutExpired: Διεργασία.kill(); Διεργασία.wait()
        준비살피미.close(); Διεργασία.stdout.close()
        (출력결과/'serial.log').write_bytes(μεταγραφή)
        (출력결과/'report.json').write_text(json.dumps(επικύρωση_έκθεση,indent=2)+'\n')


if __name__=='__main__': Εκτέλεση_2()
