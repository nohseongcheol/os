#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from eżegwixxa_kmand import pprojetta_għerq,kmand

def serje():
    destinazzjoni_VALUE_pożizzjoni=pprojetta_għerq/'build/verification/swing';destinazzjoni_VALUE_pożizzjoni.mkdir(parents=True,exist_ok=True)
    klassi_mogħdija=pprojetta_għerq/'build/verification/new-java';klassi_mogħdija.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(pprojetta_għerq/'dist/jkoros-native-korean.jar'),'-d',str(klassi_mogħdija),str(pprojetta_għerq/'시험/자바/스윙시험.java'),str(pprojetta_għerq/'시험/자바/한글창시험.java')])
    validazzjoni_rapport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((pprojetta_għerq/'build/kernel8.img').read_bytes()).hexdigest()};LOG_RECORD=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        data_pożizzjoni=subprocess.Popen(kmand()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        selettur_a916db4e=selectors.DefaultSelector();selettur_a916db4e.register(data_pożizzjoni.stdout,selectors.EVENT_READ)
        def handle_avveniment(초단위=.1):
            for 누름값,_ in selettur_a916db4e.select(초단위):
                SECOND_VALUE=누름값.fileobj.read(65536)
                if SECOND_VALUE:LOG_RECORD.extend(SECOND_VALUE)
            assert b'PANIC:' not in LOG_RECORD and b'HALTED' not in LOG_RECORD,LOG_RECORD[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            ttermina_OFFSET=time.monotonic()+초단위
            while 확인표시 not in LOG_RECORD[현재위치:]:
                if time.monotonic()>ttermina_OFFSET or data_pożizzjoni.poll() is not None:raise AssertionError(LOG_RECORD[현재위치:].decode('utf-8','replace'))
                handle_avveniment()
            return bytes(LOG_RECORD[현재위치:])
        def bagħat(SECOND_VALUE,확인표시=b'jkoros-native> '):
            현재위치=len(LOG_RECORD);data_pożizzjoni.stdin.write(SECOND_VALUE);data_pożizzjoni.stdin.flush();return 기다리기(확인표시,현재위치)
        def shell(string_data):return bagħat((string_data+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def shortcut_VALUE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def klikkja_buttuna(koordinat_x,세로좌표):return bytes([30,1,1,koordinat_x&255,koordinat_x>>8,세로좌표&255,세로좌표>>8,30,1,0,koordinat_x&255,koordinat_x>>8,세로좌표&255,세로좌표>>8])
        def kmand_MODE():
            data_pożizzjoni.stdin.write(b'\x1b');data_pożizzjoni.stdin.flush();ttermina_OFFSET=time.monotonic()+.2
            while time.monotonic()<ttermina_OFFSET:handle_avveniment(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            shell('terminal');handle_avveniment(.3)
            data=(pprojetta_għerq/'build/verification/new-java/스윙시험.class').read_bytes()
            bagħat('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(data),64):bagħat(data[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            bagħat(b'.\n')
            bagħat('java 스윙시험\n'.encode(),b'SWING READY')
            ttermina_OFFSET=time.monotonic()+3
            while time.monotonic()<ttermina_OFFSET:handle_avveniment(.1)
            # JFrame centered at (120,100), content at y=130.
            bagħat(klikkja_buttuna(200,210),b'',)  # focus JTextField
            data_pożizzjoni.stdin.write('누리'.encode());data_pożizzjoni.stdin.flush()
            ttermina_OFFSET=time.monotonic()+.3
            while time.monotonic()<ttermina_OFFSET:handle_avveniment(.05)
            miżura=bagħat(klikkja_buttuna(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(LOG_RECORD)-len(miżura))
            bagħat(shortcut_VALUE(1),b'TERMINAL FOCUS 2')
            miżura=shell('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in miżura
            bagħat(klikkja_buttuna(180,12),b'TERMINAL FOCUS 1')
            ttermina_OFFSET=time.monotonic()+.3
            while time.monotonic()<ttermina_OFFSET:handle_avveniment(.05)
            with socket.socket(socket.AF_UNIX) as kodiċi_tal_karattru:
                kodiċi_tal_karattru.settimeout(10);kodiċi_tal_karattru.connect(str(모의제어접속))
                with kodiċi_tal_karattru.makefile('rwb') as fajl_entrata:
                    json.loads(fajl_entrata.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(destinazzjoni_VALUE_pożizzjoni/'native-swing.png'),'format':'png'}}):
                        fajl_entrata.write((json.dumps(요청값)+'\n').encode());fajl_entrata.flush()
                        while True:
                            반환값=json.loads(fajl_entrata.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            bagħat(klikkja_buttuna(505,115))
            shell('echo SWING_CLOSED_OK')
            data=(klassi_mogħdija/'한글창시험.class').read_bytes()
            bagħat('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(data),64):bagħat(data[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            bagħat(b'.\n')
            bagħat('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            bagħat(klikkja_buttuna(200,255),'KOREAN SWING CLICK isem'.encode())
            bagħat(klikkja_buttuna(505,115))
            shell('echo KOREAN_SWING_CLOSED_OK')
            validazzjoni_rapport.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','Malti tieqa/buttuna/동작알림/avveniment_kju directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if data_pożizzjoni.poll() is None:data_pożizzjoni.terminate()
            try:data_pożizzjoni.wait(timeout=5)
            except subprocess.TimeoutExpired:data_pożizzjoni.kill();data_pożizzjoni.wait()
            selettur_a916db4e.close();data_pożizzjoni.stdin.close();data_pożizzjoni.stdout.close();(destinazzjoni_VALUE_pożizzjoni/'serial.log').write_bytes(LOG_RECORD);(destinazzjoni_VALUE_pożizzjoni/'report.json').write_text(json.dumps(validazzjoni_rapport,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':serje()
