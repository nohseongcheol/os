#!/usr/bin/env python3
"""വാസ്തവമായ_ഡാറ്റാ RFB 클라이언트로 QEMU 창의 한글/കീ_മൂല്യം/클립보드/마우스와 화면 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from ഡെസ്ക്ടോപ്പ്_കാഴ്ച import 정확한값
from നടപ്പാക്കുക_കമാന്_ഡ് import പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം


def നടപ്പിലാക്കുക():
    출력결과=പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'build/verification/desktop'; 출력결과.mkdir(parents=True,exist_ok=True)
    പ്രക്രിയ=subprocess.Popen(['python3',str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'ഉപകരണങ്ങൾ/ഡെസ്ക്ടോപ്പ്_കാഴ്ച.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비살피미=selectors.DefaultSelector(); 준비살피미.register(പ്രക്രിയ.stdout,selectors.EVENT_READ)
    대화기록=bytearray(); నిర్ధారణ_నివేదిక={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'build/kernel8.img').read_bytes()).hexdigest()}
    def 까지(확인표시,നടപ്പിലാക്കുക=0):
        마감시각=time.monotonic()+45
        while 확인표시 not in 대화기록[നടപ്പിലാക്കുക:]:
            if time.monotonic()>마감시각 or പ്രക്രിയ.poll() is not None: raise AssertionError(대화기록[നടപ്പിലാക്കുക:].decode('utf-8','replace'))
            for 누름값,_ in 준비살피미.select(.1):
                ഡാറ്റാ=누름값.fileobj.read(4096)
                if ഡാറ്റാ: 대화기록.extend(ഡാറ്റാ)
        return bytes(대화기록[നടപ്പിലാക്കുക:])
    try:
        까지(b'TERMINAL READY')
        പോര്_ട്ട്_നമ്പര്=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        with socket.create_connection(('127.0.0.1',പോര്_ട്ട്_നമ്പര്),timeout=10) as ക്ലയന്_റ്:
            assert 정확한값(ക്ലയന്_റ്,12)==b'RFB 003.008\n'; ക്ലയന്_റ്.sendall(b'RFB 003.008\n')
            assert 1 in 정확한값(ക്ലയന്_റ്,정확한값(ക്ലയന്_റ്,1)[0]); ക്ലയന്_റ്.sendall(b'\x01'); assert 정확한값(ക്ലയന്_റ്,4)==b'\0'*4
            ക്ലയന്_റ്.sendall(b'\x01'); 초기값=정확한값(ക്ലയന്_റ്,24); assert struct.unpack('>HH',초기값[:4])==(640,480); 정확한값(ക്ലയന്_റ്,struct.unpack('>I',초기값[20:])[0])
            ക്ലയന്_റ്.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            ക്ലയന്_റ്.sendall(struct.pack('>BBHi',2,0,1,0))
            def 누름값(nbsp_ചിഹ്നം_മൂല്യം,누르는중=True): ക്ലയന്_റ്.sendall(struct.pack('>BBHI',4,int(누르는중),0,nbsp_ചിഹ്നം_മൂല്യം))
            def 글자입력(പദാവലി):
                for പ്രതീക_ഡാറ്റ in പദാവലി:
                    nbsp_ചിഹ്നം=0xff0d if പ്രതീക_ഡാറ്റ=='\n' else ord(പ്രതീക_ഡാറ്റ) if ord(പ്രതീക_ഡാറ്റ)<256 else 0x01000000|ord(പ്രതീക_ഡാറ്റ)
                    누름값(nbsp_ചിഹ്നം); 누름값(nbsp_ചിഹ്നം,False)
            def 글쇠누르기(nbsp_ചിഹ്നം_മൂല്യം): 누름값(nbsp_ചിഹ്നം_മൂല്യം); 누름값(nbsp_ചിഹ്നം_മൂല്യം,False)
            # Start with English keys only, as delivered without a host IME.
            ഓഫ്_സെറ്റ്_മൂല്യം=len(대화기록); 글자입력('echo '); 글쇠누르기(0xffc6)
            글자입력('dkssudgktpdy gksrmf'); 글쇠누르기(0xffc6); 글자입력('\n')
            까지('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),ഓഫ്_സെറ്റ്_മൂല്യം)
            ഓഫ്_സെറ്റ്_മൂല്യം=len(대화기록); 글자입력('echo ')
            누름값(0xffe1); 글쇠누르기(32); 누름값(0xffe1,False)
            글자입력('dlfr'); 글쇠누르기(0xff08); 글쇠누르기(0xff08); 글자입력('fr')
            글쇠누르기(0xff31); 글자입력(' EN\n')
            까지('\r\n읽 EN\r\njkoros-native> '.encode(),ഓഫ്_സെറ്റ്_മൂല്യം)
            ഓഫ്_സെറ്റ്_മൂല്യം=len(대화기록); 글자입력('echo '); 글쇠누르기(0xff31)
            글자입력('rhk rkqtk RkRnd'); 글쇠누르기(0xff31); 글자입력('\n')
            까지('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),ഓഫ്_സെറ്റ്_മൂല്യം)
            # The same composition edits UTF-8 text in the native vi editor.
            ഓഫ്_സെറ്റ്_മൂല്യം=len(대화기록); 글자입력('vi 한글입력.txt\n'); 까지(b'NORMAL',ഓഫ്_സെറ്റ്_മൂല്യം)
            글자입력('i'); 글쇠누르기(0xffc6); 글자입력('gksrmf dlfr'); 글쇠누르기(0xffc6)
            글쇠누르기(0xff1b); 글자입력(':wq\n'); 까지(b'jkoros-native> ',ഓഫ്_സെറ്റ്_മൂല്യം)
            ഓഫ്_സെറ്റ്_മൂല്യം=len(대화기록); 글자입력('cat 한글입력.txt\n')
            까지('한글 읽'.encode(),ഓഫ്_സെറ്റ്_മൂല്യം); 까지(b'jkoros-native> ',ഓഫ്_സെറ്റ്_മൂല്യം)
            ഓഫ്_സെറ്റ്_മൂല്യം=len(대화기록); 글자입력('help ko\n')
            까지('한/영 കീ_മൂല്യം, Shift+Space 또는 F9'.encode(),ഓഫ്_സെറ്റ്_മൂല്യം); 까지(b'jkoros-native> ',ഓഫ്_സെറ്റ്_മൂല്യം)
            ഓഫ്_സെറ്റ്_മൂല്യം=len(대화기록); 글자입력('clear\necho "VNC 한글 입력 😀"\n'); 까지('VNC 한글 입력 😀\r\n'.encode(),ഓഫ്_സെറ്റ്_മൂല്യം)
            ഓഫ്_സെറ്റ്_മൂല്യം=len(대화기록); 누름값(0xffe3); 누름값(ord('u')); 누름값(ord('u'),False); 누름값(0xffe3,False); 글자입력('echo CONTROL_OK\n'); 까지(b'\r\nCONTROL_OK\r\n',ഓഫ്_സെറ്റ്_മൂല്യം)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            പകര്_പ്പിടം_മൂല്യം='echo "ഒട്ടിക്കുക_മൂല്യം 완료"\n'.encode(); ഓഫ്_സെറ്റ്_മൂല്യം=len(대화기록)
            ക്ലയന്_റ്.sendall(struct.pack('>B3xI',6,len(പകര്_പ്പിടം_മൂല്യം))+പകര്_പ്പിടം_മൂല്യം)
            for ഇവന്റ്,_ in 준비살피미.select(.15):
                ഡാറ്റാ_തടയുക=ഇവന്റ്.fileobj.read(4096)
                if ഡാറ്റാ_തടയുക: 대화기록.extend(ഡാറ്റാ_തടയുക)
            assert 'ഒട്ടിക്കുക_മൂല്യം 완료'.encode() not in 대화기록[ഓഫ്_സെറ്റ്_മൂല്യം:]
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('v')); 누름값(ord('v'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            까지('\r\n붙여넣기 완료\r\njkoros-native> '.encode(),ഓഫ്_സെറ്റ്_മൂല്യം)
            ക്ലയന്_റ്.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            빛삼원색=bytearray(640*480*3); 본항목들=False
            while not 본항목들:
                알림문=정확한값(ക്ലയന്_റ്,1)[0]
                if 알림문==2: continue
                if 알림문==3:
                    വലിപ്പം=struct.unpack('>I',정확한값(ക്ലയന്_റ്,7)[3:])[0]; 정확한값(ക്ലയന്_റ്,വലിപ്പം); continue
                assert 알림문==0,알림문
                사각형들=struct.unpack('>H',정확한값(ക്ലയന്_റ്,3)[1:])[0]
                for _ in range(사각형들):
                    x_ഏകോപനം,Y_ബട്ടൺ_ഏകോപനം,너비값,높이값,പ്രതീക_ഗണം=struct.unpack('>HHHHi',정확한값(ക്ലയന്_റ്,12)); assert പ്രതീക_ഗണം==0,പ്രതീക_ഗണം
                    화소들=정확한값(ക്ലയന്_റ്,너비값*높이값*4)
                    for 안쪽순번 in range(높이값):
                        for 순번 in range(너비값):
                            원본주소=(안쪽순번*너비값+순번)*4; ഉദ്ദിഷ്ടസ്ഥാനം_ഇമെയിൽ=((Y_ബട്ടൺ_ഏകോപനം+안쪽순번)*640+x_ഏകോപനം+순번)*3
                            빛삼원색[ഉദ്ദിഷ്ടസ്ഥാനം_ഇമെയിൽ:ഉദ്ദിഷ്ടസ്ഥാനം_ഇമെയിൽ+3]=bytes((화소들[원본주소+2],화소들[원본주소+1],화소들[원본주소]))
                    본항목들=True
            assert 빛삼원색[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (출력결과/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+빛삼원색)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(출력결과/'vnc-terminal.png'))
            ഓഫ്_സെറ്റ്_മൂല്യം=len(대화기록)
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('t')); 누름값(ord('t'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            까지(b'TERMINAL FOCUS 2',ഓഫ്_സെറ്റ്_മൂല്യം)
            ഓഫ്_സെറ്റ്_മൂല്യം=len(대화기록); 글자입력('echo SECOND_VNC_WINDOW\n'); 까지(b'\r\nSECOND_VNC_WINDOW\r\n',ഓഫ്_സെറ്റ്_മൂല്യം)
            ഓഫ്_സെറ്റ്_മൂല്യം=len(대화기록); ക്ലയന്_റ്.sendall(struct.pack('>BBHH',5,1,576,81)); ക്ലയന്_റ്.sendall(struct.pack('>BBHH',5,0,576,81)); 까지(b'TERMINAL FOCUS 1',ഓഫ്_സെറ്റ്_മൂല്യം)
            ഓഫ്_സെറ്റ്_മൂല്യം=len(대화기록); 글자입력('python -c \'print("x"*9000)\'\n'); 까지(b'\r\njkoros-native> ',ഓഫ്_സെറ്റ്_മൂല്യം)
            assert len(대화기록)-ഓഫ്_സെറ്റ്_മൂല്യം>8192,'exercise output longer than bridge status buffer'
            ഓഫ്_സെറ്റ്_മൂല്യം=len(대화기록); ക്ലയന്_റ്.sendall(struct.pack('>BBHH',5,1,560,63)); ക്ലയന്_റ്.sendall(struct.pack('>BBHH',5,0,560,63)); 까지(b'TERMINAL FOCUS 1',ഓഫ്_സെറ്റ്_മൂല്യം)
            ഓഫ്_സെറ്റ്_മൂല്യം=len(대화기록); ക്ലയന്_റ്.sendall(struct.pack('>BBHH',5,1,80,16)); ക്ലയന്_റ്.sendall(struct.pack('>BBHH',5,0,80,16)); 까지(b'TERMINAL FOCUS 1',ഓഫ്_സെറ്റ്_മൂല്യം)
            ഓഫ്_സെറ്റ്_മൂല്യം=len(대화기록); 글자입력('echo REOPENED_VNC_WINDOW\n'); 까지(b'\r\nREOPENED_VNC_WINDOW\r\n',ഓഫ്_സെറ്റ്_മൂല്യം)
            ഓഫ്_സെറ്റ്_മൂല്യം=len(대화기록); 글자입력('gui\n'); 까지(b'GUI READY:',ഓഫ്_സെറ്റ്_മൂല്യം)
            ഓഫ്_സെറ്റ്_മൂല്യം=len(대화기록); ക്ലയന്_റ്.sendall(struct.pack('>BBHH',5,1,80,332)); ക്ലയന്_റ്.sendall(struct.pack('>BBHH',5,0,80,332)); 까지(b'TERMINAL READY',ഓഫ്_സെറ്റ്_മൂല്യം)
            నిర్ధారణ_నివేదిక.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if പ്രക്രിയ.poll() is None:
            പ്രക്രിയ.terminate()
            try: പ്രക്രിയ.wait(timeout=8)
            except subprocess.TimeoutExpired: പ്രക്രിയ.kill(); പ്രക്രിയ.wait()
        준비살피미.close(); പ്രക്രിയ.stdout.close()
        (출력결과/'serial.log').write_bytes(대화기록)
        (출력결과/'report.json').write_text(json.dumps(నిర్ధారణ_నివేదిక,indent=2)+'\n')


if __name__=='__main__': നടപ്പിലാക്കുക()
