#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from zbatoj_komandë import Project_rrënjë,Komanda

def Ekzekuto():
    vendmbërritje_VALUE_pozicioni=Project_rrënjë/'build/verification/swing';vendmbërritje_VALUE_pozicioni.mkdir(parents=True,exist_ok=True)
    klasë_shteg=Project_rrënjë/'build/verification/new-java';klasë_shteg.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(Project_rrënjë/'dist/jkoros-native-korean.jar'),'-d',str(klasë_shteg),str(Project_rrënjë/'시험/자바/스윙시험.java'),str(Project_rrënjë/'시험/자바/한글창시험.java')])
    miratim_raport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_rrënjë/'build/kernel8.img').read_bytes()).hexdigest()};LOG_RECORD=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        të_dhëna_pozicioni=subprocess.Popen(Komanda()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        përzgjedhësi_a916db4e=selectors.DefaultSelector();përzgjedhësi_a916db4e.register(të_dhëna_pozicioni.stdout,selectors.EVENT_READ)
        def dorezë_ngjarje(초단위=.1):
            for 누름값,_ in përzgjedhësi_a916db4e.select(초단위):
                SECOND_VALUE=누름값.fileobj.read(65536)
                if SECOND_VALUE:LOG_RECORD.extend(SECOND_VALUE)
            assert b'PANIC:' not in LOG_RECORD and b'HALTED' not in LOG_RECORD,LOG_RECORD[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            mbaroj_OFFSET=time.monotonic()+초단위
            while 확인표시 not in LOG_RECORD[현재위치:]:
                if time.monotonic()>mbaroj_OFFSET or të_dhëna_pozicioni.poll() is not None:raise AssertionError(LOG_RECORD[현재위치:].decode('utf-8','replace'))
                dorezë_ngjarje()
            return bytes(LOG_RECORD[현재위치:])
        def dërgoj(SECOND_VALUE,확인표시=b'jkoros-native> '):
            현재위치=len(LOG_RECORD);të_dhëna_pozicioni.stdin.write(SECOND_VALUE);të_dhëna_pozicioni.stdin.flush();return 기다리기(확인표시,현재위치)
        def pasues(varg_të_dhëna):return dërgoj((varg_të_dhëna+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def shkurtore_VALUE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def klik_buton(koordinata_x,Y_koordinatë):return bytes([30,1,1,koordinata_x&255,koordinata_x>>8,Y_koordinatë&255,Y_koordinatë>>8,30,1,0,koordinata_x&255,koordinata_x>>8,Y_koordinatë&255,Y_koordinatë>>8])
        def komandë_MODE():
            të_dhëna_pozicioni.stdin.write(b'\x1b');të_dhëna_pozicioni.stdin.flush();mbaroj_OFFSET=time.monotonic()+.2
            while time.monotonic()<mbaroj_OFFSET:dorezë_ngjarje(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            pasues('terminal');dorezë_ngjarje(.3)
            të_dhëna=(Project_rrënjë/'build/verification/new-java/스윙시험.class').read_bytes()
            dërgoj('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(të_dhëna),64):dërgoj(të_dhëna[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            dërgoj(b'.\n')
            dërgoj('java 스윙시험\n'.encode(),b'SWING READY')
            mbaroj_OFFSET=time.monotonic()+3
            while time.monotonic()<mbaroj_OFFSET:dorezë_ngjarje(.1)
            # JFrame centered at (120,100), content at y=130.
            dërgoj(klik_buton(200,210),b'',)  # focus JTextField
            të_dhëna_pozicioni.stdin.write('누리'.encode());të_dhëna_pozicioni.stdin.flush()
            mbaroj_OFFSET=time.monotonic()+.3
            while time.monotonic()<mbaroj_OFFSET:dorezë_ngjarje(.05)
            llogaritje=dërgoj(klik_buton(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(LOG_RECORD)-len(llogaritje))
            dërgoj(shkurtore_VALUE(1),b'TERMINAL FOCUS 2')
            llogaritje=pasues('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in llogaritje
            dërgoj(klik_buton(180,12),b'TERMINAL FOCUS 1')
            mbaroj_OFFSET=time.monotonic()+.3
            while time.monotonic()<mbaroj_OFFSET:dorezë_ngjarje(.05)
            with socket.socket(socket.AF_UNIX) as kodi_i_karakterit:
                kodi_i_karakterit.settimeout(10);kodi_i_karakterit.connect(str(모의제어접속))
                with kodi_i_karakterit.makefile('rwb') as skedar_futje:
                    json.loads(skedar_futje.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(vendmbërritje_VALUE_pozicioni/'native-swing.png'),'format':'png'}}):
                        skedar_futje.write((json.dumps(요청값)+'\n').encode());skedar_futje.flush()
                        while True:
                            반환값=json.loads(skedar_futje.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            dërgoj(klik_buton(505,115))
            pasues('echo SWING_CLOSED_OK')
            të_dhëna=(klasë_shteg/'한글창시험.class').read_bytes()
            dërgoj('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(të_dhëna),64):dërgoj(të_dhëna[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            dërgoj(b'.\n')
            dërgoj('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            dërgoj(klik_buton(200,255),'KOREAN SWING CLICK Emër'.encode())
            dërgoj(klik_buton(505,115))
            pasues('echo KOREAN_SWING_CLOSED_OK')
            miratim_raport.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','한국어 Dritare/Buton/동작알림/ngjarje_radhë directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if të_dhëna_pozicioni.poll() is None:të_dhëna_pozicioni.terminate()
            try:të_dhëna_pozicioni.wait(timeout=5)
            except subprocess.TimeoutExpired:të_dhëna_pozicioni.kill();të_dhëna_pozicioni.wait()
            përzgjedhësi_a916db4e.close();të_dhëna_pozicioni.stdin.close();të_dhëna_pozicioni.stdout.close();(vendmbërritje_VALUE_pozicioni/'serial.log').write_bytes(LOG_RECORD);(vendmbërritje_VALUE_pozicioni/'report.json').write_text(json.dumps(miratim_raport,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Ekzekuto()
