#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from yürütmek_komut import işlem_kök,komut

def çalıştır():
    hedef_değer_konum=işlem_kök/'build/verification/swing';hedef_değer_konum.mkdir(parents=True,exist_ok=True)
    Sınıf_yol=işlem_kök/'build/verification/new-java';Sınıf_yol.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(işlem_kök/'dist/jkoros-native-korean.jar'),'-d',str(Sınıf_yol),str(işlem_kök/'sınamalar/자바/Swing_test.java'),str(işlem_kök/'sınamalar/자바/한글창시험.java')])
    doğrulama_Rapor={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((işlem_kök/'build/kernel8.img').read_bytes()).hexdigest()};LOG_KAYIT=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        veri_konum=subprocess.Popen(komut()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        seçici_a916db4e=selectors.DefaultSelector();seçici_a916db4e.register(veri_konum.stdout,selectors.EVENT_READ)
        def sap_olay(초단위=.1):
            for 누름값,_ in seçici_a916db4e.select(초단위):
                SANİYE_değer=누름값.fileobj.read(65536)
                if SANİYE_değer:LOG_KAYIT.extend(SANİYE_değer)
            assert b'PANIC:' not in LOG_KAYIT and b'HALTED' not in LOG_KAYIT,LOG_KAYIT[-2048:]
        def 기다리기(işaret,geçerli_konum,초단위=50):
            Bitiş_Ofset=time.monotonic()+초단위
            while işaret not in LOG_KAYIT[geçerli_konum:]:
                if time.monotonic()>Bitiş_Ofset or veri_konum.poll() is not None:raise AssertionError(LOG_KAYIT[geçerli_konum:].decode('utf-8','replace'))
                sap_olay()
            return bytes(LOG_KAYIT[geçerli_konum:])
        def göndermek(SANİYE_değer,işaret=b'jkoros-native> '):
            geçerli_konum=len(LOG_KAYIT);veri_konum.stdin.write(SANİYE_değer);veri_konum.stdin.flush();return 기다리기(işaret,geçerli_konum)
        def kabuk(dize_veri):return göndermek((dize_veri+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def kısayol_değer(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def tık_düğme(x_koordinatı,Y_koordinat):return bytes([30,1,1,x_koordinatı&255,x_koordinatı>>8,Y_koordinat&255,Y_koordinat>>8,30,1,0,x_koordinatı&255,x_koordinatı>>8,Y_koordinat&255,Y_koordinat>>8])
        def komut_mod():
            veri_konum.stdin.write(b'\x1b');veri_konum.stdin.flush();Bitiş_Ofset=time.monotonic()+.2
            while time.monotonic()<Bitiş_Ofset:sap_olay(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            kabuk('terminal');sap_olay(.3)
            veri=(işlem_kök/'build/verification/new-java/Swing_test.class').read_bytes()
            göndermek('load Swing_test.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(veri),64):göndermek(veri[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            göndermek(b'.\n')
            göndermek('java Swing_test\n'.encode(),b'SWING READY')
            Bitiş_Ofset=time.monotonic()+3
            while time.monotonic()<Bitiş_Ofset:sap_olay(.1)
            # JFrame centered at (120,100), content at y=130.
            göndermek(tık_düğme(200,210),b'',)  # focus JTextField
            veri_konum.stdin.write('누리'.encode());veri_konum.stdin.flush()
            Bitiş_Ofset=time.monotonic()+.3
            while time.monotonic()<Bitiş_Ofset:sap_olay(.05)
            sonuç=göndermek(tık_düğme(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(LOG_KAYIT)-len(sonuç))
            göndermek(kısayol_değer(1),b'TERMINAL FOCUS 2')
            sonuç=kabuk('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in sonuç
            göndermek(tık_düğme(180,12),b'TERMINAL FOCUS 1')
            Bitiş_Ofset=time.monotonic()+.3
            while time.monotonic()<Bitiş_Ofset:sap_olay(.05)
            with socket.socket(socket.AF_UNIX) as kod_noktası:
                kod_noktası.settimeout(10);kod_noktası.connect(str(모의제어접속))
                with kod_noktası.makefile('rwb') as Dosya_girdi:
                    json.loads(Dosya_girdi.readline())
                    for istek_değer in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(hedef_değer_konum/'native-swing.png'),'format':'png'}}):
                        Dosya_girdi.write((json.dumps(istek_değer)+'\n').encode());Dosya_girdi.flush()
                        while True:
                            반환값=json.loads(Dosya_girdi.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            göndermek(tık_düğme(505,115))
            kabuk('echo SWING_CLOSED_OK')
            veri=(Sınıf_yol/'한글창시험.class').read_bytes()
            göndermek('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(veri),64):göndermek(veri[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            göndermek(b'.\n')
            göndermek('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            göndermek(tık_düğme(200,255),'KOREAN SWING CLICK İsim'.encode())
            göndermek(tık_düğme(505,115))
            kabuk('echo KOREAN_SWING_CLOSED_OK')
            doğrulama_Rapor.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','Türkçe Pencere/düğme/Eylem_uyarı/olay_sıra directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if veri_konum.poll() is None:veri_konum.terminate()
            try:veri_konum.wait(timeout=5)
            except subprocess.TimeoutExpired:veri_konum.kill();veri_konum.wait()
            seçici_a916db4e.close();veri_konum.stdin.close();veri_konum.stdout.close();(hedef_değer_konum/'serial.log').write_bytes(LOG_KAYIT);(hedef_değer_konum/'report.json').write_text(json.dumps(doğrulama_Rapor,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':çalıştır()
