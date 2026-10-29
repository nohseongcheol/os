#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Rith_ordú import teilgean_fréamh,Ordú

def Rith_2():
    sprioc_VALUE_suíomh=teilgean_fréamh/'build/verification/windows';sprioc_VALUE_suíomh.mkdir(parents=True,exist_ok=True)
    bailíochtú_tuairisc={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((teilgean_fréamh/'build/kernel8.img').read_bytes()).hexdigest()};LOG_ró=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        sonraí_suíomh=subprocess.Popen(Ordú()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        roghnóir_a916db4e=selectors.DefaultSelector();roghnóir_a916db4e.register(sonraí_suíomh.stdout,selectors.EVENT_READ)
        def hanla_ócáid(초단위=.1):
            for 누름값,_ in roghnóir_a916db4e.select(초단위):
                SECOND_VALUE=누름값.fileobj.read(65536)
                if SECOND_VALUE:LOG_ró.extend(SECOND_VALUE)
            assert b'PANIC:' not in LOG_ró and b'HALTED' not in LOG_ró,LOG_ró[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            cuir_deireadh_le_OFFSET=time.monotonic()+초단위
            while 확인표시 not in LOG_ró[현재위치:]:
                if time.monotonic()>cuir_deireadh_le_OFFSET or sonraí_suíomh.poll() is not None:raise AssertionError(LOG_ró[현재위치:].decode('utf-8','replace'))
                hanla_ócáid()
            return bytes(LOG_ró[현재위치:])
        def seol(SECOND_VALUE,확인표시=b'jkoros-native> '):
            현재위치=len(LOG_ró);sonraí_suíomh.stdin.write(SECOND_VALUE);sonraí_suíomh.stdin.flush();return 기다리기(확인표시,현재위치)
        def blaosc(teaghrán_sonraí):return seol((teaghrán_sonraí+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def aicearra_VALUE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def cliceáil_cnaipe(x_chomhordanáid,세로좌표):return bytes([30,1,1,x_chomhordanáid&255,x_chomhordanáid>>8,세로좌표&255,세로좌표>>8,30,1,0,x_chomhordanáid&255,x_chomhordanáid>>8,세로좌표&255,세로좌표>>8])
        def ordú_mód():
            sonraí_suíomh.stdin.write(b'\x1b');sonraí_suíomh.stdin.flush();cuir_deireadh_le_OFFSET=time.monotonic()+.2
            while time.monotonic()<cuir_deireadh_le_OFFSET:hanla_ócáid(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            blaosc('terminal');hanla_ócáid(.3)
            blaosc('mkdir first; cd first; export NAME=one')
            seol('vi 첫째.py\n'.encode(),b'NORMAL')
            seol('i값 = 21\nprint(VALUE * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            cuir_deireadh_le_OFFSET=time.monotonic()+3
            while time.monotonic()<cuir_deireadh_le_OFFSET:hanla_ócáid(.1)
            seol(aicearra_VALUE(1),b'TERMINAL FOCUS 2');hanla_ócáid(.2)
            assert b'/\r\n' in blaosc('pwd')
            blaosc('export NAME=two')
            seol('vi 둘째.txt\n'.encode(),b'NORMAL')
            seol('i두 번째 fuinneog\n'.encode(),b'INSERT')
            seol(cliceáil_cnaipe(180,12),b'TERMINAL FOCUS 1');hanla_ócáid(.2)
            ordú_mód();seol(b':wq\r')
            assert b'one:/first' in blaosc('echo "$NAME:$PWD"')
            assert 'VALUE = 21\r\nprint(VALUE * 2)'.encode() in blaosc('cat 첫째.py')
            tomhas=blaosc('python 첫째.py');assert b'42\r\n' in tomhas,tomhas
            # Close the first shell with its actual title-bar X; second editor resumes.
            seol(cliceáil_cnaipe(560,63),b'TERMINAL FOCUS 2');hanla_ócáid(.2)
            ordú_mód();seol(b':wq\r')
            assert b'two:/' in blaosc('echo "$NAME:$PWD"')
            assert '두 번째 fuinneog'.encode() in blaosc('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            seol('vi 둘째.txt\n'.encode(),b'NORMAL');seol(b'xu',b'NORMAL')
            seol(b'iX',b'INSERT');ordú_mód();seol(b':q\r',b'Unsaved')
            seol(b':q!\r');assert '두 번째 fuinneog'.encode() in blaosc('cat 둘째.txt')
            seol(aicearra_VALUE(1),b'TERMINAL FOCUS 1');hanla_ócáid(.2)
            seol(aicearra_VALUE(1),b'TERMINAL FOCUS 3');hanla_ócáid(.2)
            seol(aicearra_VALUE(1),b'TERMINAL FOCUS 4');hanla_ócáid(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            sonraí_suíomh.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));sonraí_suíomh.stdin.flush()
            blaosc('echo DRAGGED_OK')
            seol('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            seol('i저장하지 않은 sonraí'.encode(),b'INSERT')
            seol(cliceáil_cnaipe(578,97),b'TERMINAL FOCUS 3');hanla_ócáid(.2)
            assert '버릴문서.txt'.encode() not in blaosc('ls')
            seol(aicearra_VALUE(1),b'TERMINAL FOCUS 4');hanla_ócáid(.2)
            blaosc('echo REUSED_WINDOW_OK')
            완료량=LOG_ró.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            cuir_deireadh_le_OFFSET=time.monotonic()+.3
            while time.monotonic()<cuir_deireadh_le_OFFSET:hanla_ócáid(.05)
            with socket.socket(socket.AF_UNIX) as pointe_cóid:
                pointe_cóid.settimeout(10);pointe_cóid.connect(str(모의제어접속))
                with pointe_cóid.makefile('rwb') as comhad_iontráil:
                    json.loads(comhad_iontráil.readline())
                    for iarratas_HTTP_VALUE in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(sprioc_VALUE_suíomh/'four-terminals.png'),'format':'png'}}):
                        comhad_iontráil.write((json.dumps(iarratas_HTTP_VALUE)+'\n').encode());comhad_iontráil.flush()
                        while True:
                            반환값=json.loads(comhad_iontráil.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(sprioc_VALUE_suíomh/'four-terminals.png')).convert('RGB')
            for péire_comhordanáidí,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(péire_comhordanáidí)==색상,(péire_comhordanáidí,화소들.getpixel(péire_comhordanáidí))
            blaosc('echo FOUR_WINDOWS_OK')
            bailíochtú_tuairisc.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if sonraí_suíomh.poll() is None:sonraí_suíomh.terminate()
            try:sonraí_suíomh.wait(timeout=5)
            except subprocess.TimeoutExpired:sonraí_suíomh.kill();sonraí_suíomh.wait()
            roghnóir_a916db4e.close();sonraí_suíomh.stdin.close();sonraí_suíomh.stdout.close();(sprioc_VALUE_suíomh/'serial.log').write_bytes(LOG_ró);(sprioc_VALUE_suíomh/'report.json').write_text(json.dumps(bailíochtú_tuairisc,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Rith_2()
