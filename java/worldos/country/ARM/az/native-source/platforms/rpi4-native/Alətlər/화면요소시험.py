#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from icra_etmək_əmr import Project_kök,Əmr

def İcra_Et():
    təyinat_VALUE_yerinə_qoymaq=Project_kök/'build/verification/swing';təyinat_VALUE_yerinə_qoymaq.mkdir(parents=True,exist_ok=True)
    Sinif_yol=Project_kök/'build/verification/new-java';Sinif_yol.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(Project_kök/'dist/jkoros-native-korean.jar'),'-d',str(Sinif_yol),str(Project_kök/'시험/자바/스윙시험.java'),str(Project_kök/'시험/자바/한글창시험.java')])
    yoxlama_hesabat={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_kök/'build/kernel8.img').read_bytes()).hexdigest()};LOG_yaz=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        verilənlər_yerinə_qoymaq=subprocess.Popen(Əmr()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        seçici_a916db4e=selectors.DefaultSelector();seçici_a916db4e.register(verilənlər_yerinə_qoymaq.stdout,selectors.EVENT_READ)
        def tutacaq_hadisə(초단위=.1):
            for 누름값,_ in seçici_a916db4e.select(초단위):
                SECOND_VALUE=누름값.fileobj.read(65536)
                if SECOND_VALUE:LOG_yaz.extend(SECOND_VALUE)
            assert b'PANIC:' not in LOG_yaz and b'HALTED' not in LOG_yaz,LOG_yaz[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            bitirmək_OFFSET=time.monotonic()+초단위
            while 확인표시 not in LOG_yaz[현재위치:]:
                if time.monotonic()>bitirmək_OFFSET or verilənlər_yerinə_qoymaq.poll() is not None:raise AssertionError(LOG_yaz[현재위치:].decode('utf-8','replace'))
                tutacaq_hadisə()
            return bytes(LOG_yaz[현재위치:])
        def göndərmək(SECOND_VALUE,확인표시=b'jkoros-native> '):
            현재위치=len(LOG_yaz);verilənlər_yerinə_qoymaq.stdin.write(SECOND_VALUE);verilənlər_yerinə_qoymaq.stdin.flush();return 기다리기(확인표시,현재위치)
        def örtük(sətir_verilənlər):return göndərmək((sətir_verilənlər+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def qısayol_VALUE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def klikləmə_düymə(x_koordinatı,Y_koordinat):return bytes([30,1,1,x_koordinatı&255,x_koordinatı>>8,Y_koordinat&255,Y_koordinat>>8,30,1,0,x_koordinatı&255,x_koordinatı>>8,Y_koordinat&255,Y_koordinat>>8])
        def əmr_MODE():
            verilənlər_yerinə_qoymaq.stdin.write(b'\x1b');verilənlər_yerinə_qoymaq.stdin.flush();bitirmək_OFFSET=time.monotonic()+.2
            while time.monotonic()<bitirmək_OFFSET:tutacaq_hadisə(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            örtük('terminal');tutacaq_hadisə(.3)
            verilənlər=(Project_kök/'build/verification/new-java/스윙시험.class').read_bytes()
            göndərmək('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(verilənlər),64):göndərmək(verilənlər[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            göndərmək(b'.\n')
            göndərmək('java 스윙시험\n'.encode(),b'SWING READY')
            bitirmək_OFFSET=time.monotonic()+3
            while time.monotonic()<bitirmək_OFFSET:tutacaq_hadisə(.1)
            # JFrame centered at (120,100), content at y=130.
            göndərmək(klikləmə_düymə(200,210),b'',)  # focus JTextField
            verilənlər_yerinə_qoymaq.stdin.write('누리'.encode());verilənlər_yerinə_qoymaq.stdin.flush()
            bitirmək_OFFSET=time.monotonic()+.3
            while time.monotonic()<bitirmək_OFFSET:tutacaq_hadisə(.05)
            ölçü=göndərmək(klikləmə_düymə(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(LOG_yaz)-len(ölçü))
            göndərmək(qısayol_VALUE(1),b'TERMINAL FOCUS 2')
            ölçü=örtük('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in ölçü
            göndərmək(klikləmə_düymə(180,12),b'TERMINAL FOCUS 1')
            bitirmək_OFFSET=time.monotonic()+.3
            while time.monotonic()<bitirmək_OFFSET:tutacaq_hadisə(.05)
            with socket.socket(socket.AF_UNIX) as simvol_kodu:
                simvol_kodu.settimeout(10);simvol_kodu.connect(str(모의제어접속))
                with simvol_kodu.makefile('rwb') as fayl_daxiletmə:
                    json.loads(fayl_daxiletmə.readline())
                    for HTTP_sorğusu_VALUE in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(təyinat_VALUE_yerinə_qoymaq/'native-swing.png'),'format':'png'}}):
                        fayl_daxiletmə.write((json.dumps(HTTP_sorğusu_VALUE)+'\n').encode());fayl_daxiletmə.flush()
                        while True:
                            반환값=json.loads(fayl_daxiletmə.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            göndərmək(klikləmə_düymə(505,115))
            örtük('echo SWING_CLOSED_OK')
            verilənlər=(Sinif_yol/'한글창시험.class').read_bytes()
            göndərmək('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(verilənlər),64):göndərmək(verilənlər[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            göndərmək(b'.\n')
            göndərmək('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            göndərmək(klikləmə_düymə(200,255),'KOREAN SWING CLICK Ad'.encode())
            göndərmək(klikləmə_düymə(505,115))
            örtük('echo KOREAN_SWING_CLOSED_OK')
            yoxlama_hesabat.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','한국어 pəncərə/düymə/동작알림/hadisə_növbə directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if verilənlər_yerinə_qoymaq.poll() is None:verilənlər_yerinə_qoymaq.terminate()
            try:verilənlər_yerinə_qoymaq.wait(timeout=5)
            except subprocess.TimeoutExpired:verilənlər_yerinə_qoymaq.kill();verilənlər_yerinə_qoymaq.wait()
            seçici_a916db4e.close();verilənlər_yerinə_qoymaq.stdin.close();verilənlər_yerinə_qoymaq.stdout.close();(təyinat_VALUE_yerinə_qoymaq/'serial.log').write_bytes(LOG_yaz);(təyinat_VALUE_yerinə_qoymaq/'report.json').write_text(json.dumps(yoxlama_hesabat,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':İcra_Et()
