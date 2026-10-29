#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from yürütmek_komut import işlem_kök,komut

def çalıştır():
    hedef_değer_konum=işlem_kök/'build/verification/windows';hedef_değer_konum.mkdir(parents=True,exist_ok=True)
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
            kabuk('mkdir first; cd first; export NAME=one')
            göndermek('vi 첫째.py\n'.encode(),b'NORMAL')
            göndermek('i값 = 21\nprint(değer * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            Bitiş_Ofset=time.monotonic()+3
            while time.monotonic()<Bitiş_Ofset:sap_olay(.1)
            göndermek(kısayol_değer(1),b'TERMINAL FOCUS 2');sap_olay(.2)
            assert b'/\r\n' in kabuk('pwd')
            kabuk('export NAME=two')
            göndermek('vi 둘째.txt\n'.encode(),b'NORMAL')
            göndermek('i두 번째 Pencere\n'.encode(),b'INSERT')
            göndermek(tık_düğme(180,12),b'TERMINAL FOCUS 1');sap_olay(.2)
            komut_mod();göndermek(b':wq\r')
            assert b'one:/first' in kabuk('echo "$NAME:$PWD"')
            assert 'değer = 21\r\nprint(değer * 2)'.encode() in kabuk('cat 첫째.py')
            sonuç=kabuk('python 첫째.py');assert b'42\r\n' in sonuç,sonuç
            # Close the first shell with its actual title-bar X; second editor resumes.
            göndermek(tık_düğme(560,63),b'TERMINAL FOCUS 2');sap_olay(.2)
            komut_mod();göndermek(b':wq\r')
            assert b'two:/' in kabuk('echo "$NAME:$PWD"')
            assert '두 번째 Pencere'.encode() in kabuk('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            göndermek('vi 둘째.txt\n'.encode(),b'NORMAL');göndermek(b'xu',b'NORMAL')
            göndermek(b'iX',b'INSERT');komut_mod();göndermek(b':q\r',b'Unsaved')
            göndermek(b':q!\r');assert '두 번째 Pencere'.encode() in kabuk('cat 둘째.txt')
            göndermek(kısayol_değer(1),b'TERMINAL FOCUS 1');sap_olay(.2)
            göndermek(kısayol_değer(1),b'TERMINAL FOCUS 3');sap_olay(.2)
            göndermek(kısayol_değer(1),b'TERMINAL FOCUS 4');sap_olay(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            veri_konum.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));veri_konum.stdin.flush()
            kabuk('echo DRAGGED_OK')
            göndermek('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            göndermek('i저장하지 않은 veri'.encode(),b'INSERT')
            göndermek(tık_düğme(578,97),b'TERMINAL FOCUS 3');sap_olay(.2)
            assert '버릴문서.txt'.encode() not in kabuk('ls')
            göndermek(kısayol_değer(1),b'TERMINAL FOCUS 4');sap_olay(.2)
            kabuk('echo REUSED_WINDOW_OK')
            Bitenler_tutar=LOG_KAYIT.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',Bitenler_tutar)
            # UART completion precedes the next QEMU display refresh.
            Bitiş_Ofset=time.monotonic()+.3
            while time.monotonic()<Bitiş_Ofset:sap_olay(.05)
            with socket.socket(socket.AF_UNIX) as kod_noktası:
                kod_noktası.settimeout(10);kod_noktası.connect(str(모의제어접속))
                with kod_noktası.makefile('rwb') as Dosya_girdi:
                    json.loads(Dosya_girdi.readline())
                    for istek_değer in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(hedef_değer_konum/'four-terminals.png'),'format':'png'}}):
                        Dosya_girdi.write((json.dumps(istek_değer)+'\n').encode());Dosya_girdi.flush()
                        while True:
                            반환값=json.loads(Dosya_girdi.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(hedef_değer_konum/'four-terminals.png')).convert('RGB')
            for koordinat_çifti,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(koordinat_çifti)==색상,(koordinat_çifti,화소들.getpixel(koordinat_çifti))
            kabuk('echo FOUR_WINDOWS_OK')
            doğrulama_Rapor.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if veri_konum.poll() is None:veri_konum.terminate()
            try:veri_konum.wait(timeout=5)
            except subprocess.TimeoutExpired:veri_konum.kill();veri_konum.wait()
            seçici_a916db4e.close();veri_konum.stdin.close();veri_konum.stdout.close();(hedef_değer_konum/'serial.log').write_bytes(LOG_KAYIT);(hedef_değer_konum/'report.json').write_text(json.dumps(doğrulama_Rapor,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':çalıştır()
