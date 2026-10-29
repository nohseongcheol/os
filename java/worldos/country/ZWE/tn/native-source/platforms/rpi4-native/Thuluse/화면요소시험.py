#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from diragatsa_Taelo import 기준,Taelo

def dirisa():
    목적위치=기준/'build/verification/swing';목적위치.mkdir(parents=True,exist_ok=True)
    mofuta_tsela=기준/'build/verification/new-java';mofuta_tsela.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'dist/jkoros-native-korean.jar'),'-d',str(mofuta_tsela),str(기준/'시험/자바/스윙시험.java'),str(기준/'시험/자바/한글창시험.java')])
    netefatso_pego={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()};rekota_mola=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        자료위치=subprocess.Popen(Taelo()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        setlhophi_a916db4e=selectors.DefaultSelector();setlhophi_a916db4e.register(자료위치.stdout,selectors.EVENT_READ)
        def mokgwakamogelo_tiragalo(초단위=.1):
            for 누름값,_ in setlhophi_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:rekota_mola.extend(둘째값)
            assert b'PANIC:' not in rekota_mola and b'HALTED' not in rekota_mola,rekota_mola[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            kgaola_Baya_ka_Tekatekanyo=time.monotonic()+초단위
            while 확인표시 not in rekota_mola[현재위치:]:
                if time.monotonic()>kgaola_Baya_ka_Tekatekanyo or 자료위치.poll() is not None:raise AssertionError(rekota_mola[현재위치:].decode('utf-8','replace'))
                mokgwakamogelo_tiragalo()
            return bytes(rekota_mola[현재위치:])
        def romela(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(rekota_mola);자료위치.stdin.write(둘째값);자료위치.stdin.flush();return 기다리기(확인표시,현재위치)
        def setlhalosataelo(dikwalwa_tshedimosetso):return romela((dikwalwa_tshedimosetso+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def tlhabanyetso_Boleng(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def tobetsa_konopo(kgokagano_ya_x,세로좌표):return bytes([30,1,1,kgokagano_ya_x&255,kgokagano_ya_x>>8,세로좌표&255,세로좌표>>8,30,1,0,kgokagano_ya_x&255,kgokagano_ya_x>>8,세로좌표&255,세로좌표>>8])
        def Taelo_mokgwa():
            자료위치.stdin.write(b'\x1b');자료위치.stdin.flush();kgaola_Baya_ka_Tekatekanyo=time.monotonic()+.2
            while time.monotonic()<kgaola_Baya_ka_Tekatekanyo:mokgwakamogelo_tiragalo(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            setlhalosataelo('terminal');mokgwakamogelo_tiragalo(.3)
            tshedimosetso=(기준/'build/verification/new-java/스윙시험.class').read_bytes()
            romela('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(tshedimosetso),64):romela(tshedimosetso[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            romela(b'.\n')
            romela('java 스윙시험\n'.encode(),b'SWING READY')
            kgaola_Baya_ka_Tekatekanyo=time.monotonic()+3
            while time.monotonic()<kgaola_Baya_ka_Tekatekanyo:mokgwakamogelo_tiragalo(.1)
            # JFrame centered at (120,100), content at y=130.
            romela(tobetsa_konopo(200,210),b'',)  # focus JTextField
            자료위치.stdin.write('누리'.encode());자료위치.stdin.flush()
            kgaola_Baya_ka_Tekatekanyo=time.monotonic()+.3
            while time.monotonic()<kgaola_Baya_ka_Tekatekanyo:mokgwakamogelo_tiragalo(.05)
            결과=romela(tobetsa_konopo(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(rekota_mola)-len(결과))
            romela(tlhabanyetso_Boleng(1),b'TERMINAL FOCUS 2')
            결과=setlhalosataelo('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in 결과
            romela(tobetsa_konopo(180,12),b'TERMINAL FOCUS 1')
            kgaola_Baya_ka_Tekatekanyo=time.monotonic()+.3
            while time.monotonic()<kgaola_Baya_ka_Tekatekanyo:mokgwakamogelo_tiragalo(.05)
            with socket.socket(socket.AF_UNIX) as khoutuletshwao:
                khoutuletshwao.settimeout(10);khoutuletshwao.connect(str(모의제어접속))
                with khoutuletshwao.makefile('rwb') as faele_tsenyo:
                    json.loads(faele_tsenyo.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(목적위치/'native-swing.png'),'format':'png'}}):
                        faele_tsenyo.write((json.dumps(요청값)+'\n').encode());faele_tsenyo.flush()
                        while True:
                            반환값=json.loads(faele_tsenyo.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            romela(tobetsa_konopo(505,115))
            setlhalosataelo('echo SWING_CLOSED_OK')
            tshedimosetso=(mofuta_tsela/'한글창시험.class').read_bytes()
            romela('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(tshedimosetso),64):romela(tshedimosetso[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            romela(b'.\n')
            romela('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            romela(tobetsa_konopo(200,255),'KOREAN SWING CLICK leina'.encode())
            romela(tobetsa_konopo(505,115))
            setlhalosataelo('echo KOREAN_SWING_CLOSED_OK')
            netefatso_pego.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','한국어 fensetere/konopo/동작알림/tiragalo_diletakgatiso directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if 자료위치.poll() is None:자료위치.terminate()
            try:자료위치.wait(timeout=5)
            except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            setlhophi_a916db4e.close();자료위치.stdin.close();자료위치.stdout.close();(목적위치/'serial.log').write_bytes(rekota_mola);(목적위치/'report.json').write_text(json.dumps(netefatso_pego,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':dirisa()
