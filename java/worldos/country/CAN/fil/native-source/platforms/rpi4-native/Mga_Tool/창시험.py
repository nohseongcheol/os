#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Mag_execute_utos import Project_root,utos

def run():
    patutunguhan_VALUE_posisyon=Project_root/'build/verification/windows';patutunguhan_VALUE_posisyon.mkdir(parents=True,exist_ok=True)
    pagpapatibay_ulat={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_root/'build/kernel8.img').read_bytes()).hexdigest()};LOG_hanay=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        data_posisyon=subprocess.Popen(utos()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        tagapili_a916db4e=selectors.DefaultSelector();tagapili_a916db4e.register(data_posisyon.stdout,selectors.EVENT_READ)
        def hawakán_kaganapan(초단위=.1):
            for 누름값,_ in tagapili_a916db4e.select(초단위):
                SECOND_VALUE=누름값.fileobj.read(65536)
                if SECOND_VALUE:LOG_hanay.extend(SECOND_VALUE)
            assert b'PANIC:' not in LOG_hanay and b'HALTED' not in LOG_hanay,LOG_hanay[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            tapusin_OFFSET=time.monotonic()+초단위
            while 확인표시 not in LOG_hanay[현재위치:]:
                if time.monotonic()>tapusin_OFFSET or data_posisyon.poll() is not None:raise AssertionError(LOG_hanay[현재위치:].decode('utf-8','replace'))
                hawakán_kaganapan()
            return bytes(LOG_hanay[현재위치:])
        def i_email(SECOND_VALUE,확인표시=b'jkoros-native> '):
            현재위치=len(LOG_hanay);data_posisyon.stdin.write(SECOND_VALUE);data_posisyon.stdin.flush();return 기다리기(확인표시,현재위치)
        def shell(string_data):return i_email((string_data+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def shortcut_VALUE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def magklik_button(x_coordinate,Y_button_coordinate):return bytes([30,1,1,x_coordinate&255,x_coordinate>>8,Y_button_coordinate&255,Y_button_coordinate>>8,30,1,0,x_coordinate&255,x_coordinate>>8,Y_button_coordinate&255,Y_button_coordinate>>8])
        def utos_MODE():
            data_posisyon.stdin.write(b'\x1b');data_posisyon.stdin.flush();tapusin_OFFSET=time.monotonic()+.2
            while time.monotonic()<tapusin_OFFSET:hawakán_kaganapan(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            shell('terminal');hawakán_kaganapan(.3)
            shell('mkdir first; cd first; export NAME=one')
            i_email('vi 첫째.py\n'.encode(),b'NORMAL')
            i_email('i값 = 21\nprint(VALUE * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            tapusin_OFFSET=time.monotonic()+3
            while time.monotonic()<tapusin_OFFSET:hawakán_kaganapan(.1)
            i_email(shortcut_VALUE(1),b'TERMINAL FOCUS 2');hawakán_kaganapan(.2)
            assert b'/\r\n' in shell('pwd')
            shell('export NAME=two')
            i_email('vi 둘째.txt\n'.encode(),b'NORMAL')
            i_email('i두 번째 window\n'.encode(),b'INSERT')
            i_email(magklik_button(180,12),b'TERMINAL FOCUS 1');hawakán_kaganapan(.2)
            utos_MODE();i_email(b':wq\r')
            assert b'one:/first' in shell('echo "$NAME:$PWD"')
            assert 'VALUE = 21\r\nprint(VALUE * 2)'.encode() in shell('cat 첫째.py')
            sukat=shell('python 첫째.py');assert b'42\r\n' in sukat,sukat
            # Close the first shell with its actual title-bar X; second editor resumes.
            i_email(magklik_button(560,63),b'TERMINAL FOCUS 2');hawakán_kaganapan(.2)
            utos_MODE();i_email(b':wq\r')
            assert b'two:/' in shell('echo "$NAME:$PWD"')
            assert '두 번째 window'.encode() in shell('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            i_email('vi 둘째.txt\n'.encode(),b'NORMAL');i_email(b'xu',b'NORMAL')
            i_email(b'iX',b'INSERT');utos_MODE();i_email(b':q\r',b'Unsaved')
            i_email(b':q!\r');assert '두 번째 window'.encode() in shell('cat 둘째.txt')
            i_email(shortcut_VALUE(1),b'TERMINAL FOCUS 1');hawakán_kaganapan(.2)
            i_email(shortcut_VALUE(1),b'TERMINAL FOCUS 3');hawakán_kaganapan(.2)
            i_email(shortcut_VALUE(1),b'TERMINAL FOCUS 4');hawakán_kaganapan(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            data_posisyon.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));data_posisyon.stdin.flush()
            shell('echo DRAGGED_OK')
            i_email('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            i_email('i저장하지 않은 data'.encode(),b'INSERT')
            i_email(magklik_button(578,97),b'TERMINAL FOCUS 3');hawakán_kaganapan(.2)
            assert '버릴문서.txt'.encode() not in shell('ls')
            i_email(shortcut_VALUE(1),b'TERMINAL FOCUS 4');hawakán_kaganapan(.2)
            shell('echo REUSED_WINDOW_OK')
            완료량=LOG_hanay.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            tapusin_OFFSET=time.monotonic()+.3
            while time.monotonic()<tapusin_OFFSET:hawakán_kaganapan(.05)
            with socket.socket(socket.AF_UNIX) as character_code:
                character_code.settimeout(10);character_code.connect(str(모의제어접속))
                with character_code.makefile('rwb') as file_pagpasok:
                    json.loads(file_pagpasok.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(patutunguhan_VALUE_posisyon/'four-terminals.png'),'format':'png'}}):
                        file_pagpasok.write((json.dumps(요청값)+'\n').encode());file_pagpasok.flush()
                        while True:
                            반환값=json.loads(file_pagpasok.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(patutunguhan_VALUE_posisyon/'four-terminals.png')).convert('RGB')
            for pares_ng_coordinate,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(pares_ng_coordinate)==색상,(pares_ng_coordinate,화소들.getpixel(pares_ng_coordinate))
            shell('echo FOUR_WINDOWS_OK')
            pagpapatibay_ulat.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if data_posisyon.poll() is None:data_posisyon.terminate()
            try:data_posisyon.wait(timeout=5)
            except subprocess.TimeoutExpired:data_posisyon.kill();data_posisyon.wait()
            tagapili_a916db4e.close();data_posisyon.stdin.close();data_posisyon.stdout.close();(patutunguhan_VALUE_posisyon/'serial.log').write_bytes(LOG_hanay);(patutunguhan_VALUE_posisyon/'report.json').write_text(json.dumps(pagpapatibay_ulat,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':run()
