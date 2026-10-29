#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from kawe_tono import whakaatu_pūtake,tono

def whakahaere():
    ūnga_uara_tūranga=whakaatu_pūtake/'build/verification/swing';ūnga_uara_tūranga.mkdir(parents=True,exist_ok=True)
    tauaha_ara=whakaatu_pūtake/'build/verification/new-java';tauaha_ara.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(whakaatu_pūtake/'dist/jkoros-native-korean.jar'),'-d',str(tauaha_ara),str(whakaatu_pūtake/'시험/자바/스윙시험.java'),str(whakaatu_pūtake/'시험/자바/한글창시험.java')])
    whakamana_pūrongo={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((whakaatu_pūtake/'build/kernel8.img').read_bytes()).hexdigest()};LOG_RECORD=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        raraunga_tūranga=subprocess.Popen(tono()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        pūtīpako_a916db4e=selectors.DefaultSelector();pūtīpako_a916db4e.register(raraunga_tūranga.stdout,selectors.EVENT_READ)
        def raweke_hui(초단위=.1):
            for 누름값,_ in pūtīpako_a916db4e.select(초단위):
                SECOND_uara=누름값.fileobj.read(65536)
                if SECOND_uara:LOG_RECORD.extend(SECOND_uara)
            assert b'PANIC:' not in LOG_RECORD and b'HALTED' not in LOG_RECORD,LOG_RECORD[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            mutu_OFFSET=time.monotonic()+초단위
            while 확인표시 not in LOG_RECORD[현재위치:]:
                if time.monotonic()>mutu_OFFSET or raraunga_tūranga.poll() is not None:raise AssertionError(LOG_RECORD[현재위치:].decode('utf-8','replace'))
                raweke_hui()
            return bytes(LOG_RECORD[현재위치:])
        def tuku(SECOND_uara,확인표시=b'jkoros-native> '):
            현재위치=len(LOG_RECORD);raraunga_tūranga.stdin.write(SECOND_uara);raraunga_tūranga.stdin.flush();return 기다리기(확인표시,현재위치)
        def anga(aho_raraunga):return tuku((aho_raraunga+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def pokatata_uara(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def pāwhiri_pātene(taunga_x,세로좌표):return bytes([30,1,1,taunga_x&255,taunga_x>>8,세로좌표&255,세로좌표>>8,30,1,0,taunga_x&255,taunga_x>>8,세로좌표&255,세로좌표>>8])
        def tono_MODE():
            raraunga_tūranga.stdin.write(b'\x1b');raraunga_tūranga.stdin.flush();mutu_OFFSET=time.monotonic()+.2
            while time.monotonic()<mutu_OFFSET:raweke_hui(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            anga('terminal');raweke_hui(.3)
            raraunga=(whakaatu_pūtake/'build/verification/new-java/스윙시험.class').read_bytes()
            tuku('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(raraunga),64):tuku(raraunga[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            tuku(b'.\n')
            tuku('java 스윙시험\n'.encode(),b'SWING READY')
            mutu_OFFSET=time.monotonic()+3
            while time.monotonic()<mutu_OFFSET:raweke_hui(.1)
            # JFrame centered at (120,100), content at y=130.
            tuku(pāwhiri_pātene(200,210),b'',)  # focus JTextField
            raraunga_tūranga.stdin.write('누리'.encode());raraunga_tūranga.stdin.flush()
            mutu_OFFSET=time.monotonic()+.3
            while time.monotonic()<mutu_OFFSET:raweke_hui(.05)
            mēhua=tuku(pāwhiri_pātene(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(LOG_RECORD)-len(mēhua))
            tuku(pokatata_uara(1),b'TERMINAL FOCUS 2')
            mēhua=anga('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in mēhua
            tuku(pāwhiri_pātene(180,12),b'TERMINAL FOCUS 1')
            mutu_OFFSET=time.monotonic()+.3
            while time.monotonic()<mutu_OFFSET:raweke_hui(.05)
            with socket.socket(socket.AF_UNIX) as waehere_pūāhua:
                waehere_pūāhua.settimeout(10);waehere_pūāhua.connect(str(모의제어접속))
                with waehere_pūāhua.makefile('rwb') as kōnae_tāurunga:
                    json.loads(kōnae_tāurunga.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(ūnga_uara_tūranga/'native-swing.png'),'format':'png'}}):
                        kōnae_tāurunga.write((json.dumps(요청값)+'\n').encode());kōnae_tāurunga.flush()
                        while True:
                            반환값=json.loads(kōnae_tāurunga.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            tuku(pāwhiri_pātene(505,115))
            anga('echo SWING_CLOSED_OK')
            raraunga=(tauaha_ara/'한글창시험.class').read_bytes()
            tuku('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(raraunga),64):tuku(raraunga[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            tuku(b'.\n')
            tuku('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            tuku(pāwhiri_pātene(200,255),'KOREAN SWING CLICK Ingoa'.encode())
            tuku(pāwhiri_pātene(505,115))
            anga('echo KOREAN_SWING_CLOSED_OK')
            whakamana_pūrongo.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','Reo_Māori matapihi/pātene/동작알림/hui_tūtira directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if raraunga_tūranga.poll() is None:raraunga_tūranga.terminate()
            try:raraunga_tūranga.wait(timeout=5)
            except subprocess.TimeoutExpired:raraunga_tūranga.kill();raraunga_tūranga.wait()
            pūtīpako_a916db4e.close();raraunga_tūranga.stdin.close();raraunga_tūranga.stdout.close();(ūnga_uara_tūranga/'serial.log').write_bytes(LOG_RECORD);(ūnga_uara_tūranga/'report.json').write_text(json.dumps(whakamana_pūrongo,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':whakahaere()
