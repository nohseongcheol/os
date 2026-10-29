#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from exekutatu_komando import Project_erro,Komandoa

def Exekutatu_2():
    helburu_balio_kargu=Project_erro/'build/verification/swing';helburu_balio_kargu.mkdir(parents=True,exist_ok=True)
    Gela_bide_izen=Project_erro/'build/verification/new-java';Gela_bide_izen.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(Project_erro/'dist/jkoros-native-korean.jar'),'-d',str(Gela_bide_izen),str(Project_erro/'시험/자바/스윙시험.java'),str(Project_erro/'시험/자바/한글창시험.java')])
    balidazio_txosten={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_erro/'build/kernel8.img').read_bytes()).hexdigest()};LOG_marka=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        datuak_kargu=subprocess.Popen(Komandoa()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        선택기=selectors.DefaultSelector();선택기.register(datuak_kargu.stdout,selectors.EVENT_READ)
        def helduleku_gertaera(초단위=.1):
            for 누름값,_ in 선택기.select(초단위):
                SEGUNDOA_balio=누름값.fileobj.read(65536)
                if SEGUNDOA_balio:LOG_marka.extend(SEGUNDOA_balio)
            assert b'PANIC:' not in LOG_marka and b'HALTED' not in LOG_marka,LOG_marka[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            amaitu_Geruzak=time.monotonic()+초단위
            while 확인표시 not in LOG_marka[현재위치:]:
                if time.monotonic()>amaitu_Geruzak or datuak_kargu.poll() is not None:raise AssertionError(LOG_marka[현재위치:].decode('utf-8','replace'))
                helduleku_gertaera()
            return bytes(LOG_marka[현재위치:])
        def bidali(SEGUNDOA_balio,확인표시=b'jkoros-native> '):
            현재위치=len(LOG_marka);datuak_kargu.stdin.write(SEGUNDOA_balio);datuak_kargu.stdin.flush();return 기다리기(확인표시,현재위치)
        def shell(kate_datuak):return bidali((kate_datuak+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def lasterbide_balio(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def klik_botoi(X_koordenatu,Y_koordenatu):return bytes([30,1,1,X_koordenatu&255,X_koordenatu>>8,Y_koordenatu&255,Y_koordenatu>>8,30,1,0,X_koordenatu&255,X_koordenatu>>8,Y_koordenatu&255,Y_koordenatu>>8])
        def komando_MODA():
            datuak_kargu.stdin.write(b'\x1b');datuak_kargu.stdin.flush();amaitu_Geruzak=time.monotonic()+.2
            while time.monotonic()<amaitu_Geruzak:helduleku_gertaera(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            shell('terminal');helduleku_gertaera(.3)
            datuak=(Project_erro/'build/verification/new-java/스윙시험.class').read_bytes()
            bidali('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(datuak),64):bidali(datuak[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            bidali(b'.\n')
            bidali('java 스윙시험\n'.encode(),b'SWING READY')
            amaitu_Geruzak=time.monotonic()+3
            while time.monotonic()<amaitu_Geruzak:helduleku_gertaera(.1)
            # JFrame centered at (120,100), content at y=130.
            bidali(klik_botoi(200,210),b'',)  # focus JTextField
            datuak_kargu.stdin.write('누리'.encode());datuak_kargu.stdin.flush()
            amaitu_Geruzak=time.monotonic()+.3
            while time.monotonic()<amaitu_Geruzak:helduleku_gertaera(.05)
            EMAITZA=bidali(klik_botoi(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(LOG_marka)-len(EMAITZA))
            bidali(lasterbide_balio(1),b'TERMINAL FOCUS 2')
            EMAITZA=shell('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in EMAITZA
            bidali(klik_botoi(180,12),b'TERMINAL FOCUS 1')
            amaitu_Geruzak=time.monotonic()+.3
            while time.monotonic()<amaitu_Geruzak:helduleku_gertaera(.05)
            with socket.socket(socket.AF_UNIX) as karaktere_kode:
                karaktere_kode.settimeout(10);karaktere_kode.connect(str(모의제어접속))
                with karaktere_kode.makefile('rwb') as fitxategi_sarrera:
                    json.loads(fitxategi_sarrera.readline())
                    for eskaera_balio in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(helburu_balio_kargu/'native-swing.png'),'format':'png'}}):
                        fitxategi_sarrera.write((json.dumps(eskaera_balio)+'\n').encode());fitxategi_sarrera.flush()
                        while True:
                            반환값=json.loads(fitxategi_sarrera.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            bidali(klik_botoi(505,115))
            shell('echo SWING_CLOSED_OK')
            datuak=(Gela_bide_izen/'한글창시험.class').read_bytes()
            bidali('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(datuak),64):bidali(datuak[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            bidali(b'.\n')
            bidali('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            bidali(klik_botoi(200,255),'KOREAN SWING CLICK Izena'.encode())
            bidali(klik_botoi(505,115))
            shell('echo KOREAN_SWING_CLOSED_OK')
            balidazio_txosten.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','Euskara Leihoa/botoia/동작알림/gertaera_ilara directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if datuak_kargu.poll() is None:datuak_kargu.terminate()
            try:datuak_kargu.wait(timeout=5)
            except subprocess.TimeoutExpired:datuak_kargu.kill();datuak_kargu.wait()
            선택기.close();datuak_kargu.stdin.close();datuak_kargu.stdout.close();(helburu_balio_kargu/'serial.log').write_bytes(LOG_marka);(helburu_balio_kargu/'report.json').write_text(json.dumps(balidazio_txosten,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Exekutatu_2()
