#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from keyra_skipun import verk_rót,Skipun

def Keyra_2():
    endastaður_VALUE_staða=verk_rót/'build/verification/swing';endastaður_VALUE_staða.mkdir(parents=True,exist_ok=True)
    klasi_slóð=verk_rót/'build/verification/new-java';klasi_slóð.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(verk_rót/'dist/jkoros-native-korean.jar'),'-d',str(klasi_slóð),str(verk_rót/'시험/자바/스윙시험.java'),str(verk_rót/'시험/자바/한글창시험.java')])
    prófun_skrá={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((verk_rót/'build/kernel8.img').read_bytes()).hexdigest()};LOG_lína=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        gögn_staða=subprocess.Popen(Skipun()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        val_a916db4e=selectors.DefaultSelector();val_a916db4e.register(gögn_staða.stdout,selectors.EVENT_READ)
        def hald_atvik(초단위=.1):
            for 누름값,_ in val_a916db4e.select(초단위):
                SECOND_VALUE=누름값.fileobj.read(65536)
                if SECOND_VALUE:LOG_lína.extend(SECOND_VALUE)
            assert b'PANIC:' not in LOG_lína and b'HALTED' not in LOG_lína,LOG_lína[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            ljúka_OFFSET=time.monotonic()+초단위
            while 확인표시 not in LOG_lína[현재위치:]:
                if time.monotonic()>ljúka_OFFSET or gögn_staða.poll() is not None:raise AssertionError(LOG_lína[현재위치:].decode('utf-8','replace'))
                hald_atvik()
            return bytes(LOG_lína[현재위치:])
        def senda(SECOND_VALUE,확인표시=b'jkoros-native> '):
            현재위치=len(LOG_lína);gögn_staða.stdin.write(SECOND_VALUE);gögn_staða.stdin.flush();return 기다리기(확인표시,현재위치)
        def skel(strengur_gögn):return senda((strengur_gögn+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def flýtileið_VALUE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def smella_hnappur(x_hnit,Y_hnit):return bytes([30,1,1,x_hnit&255,x_hnit>>8,Y_hnit&255,Y_hnit>>8,30,1,0,x_hnit&255,x_hnit>>8,Y_hnit&255,Y_hnit>>8])
        def skipun_MODE():
            gögn_staða.stdin.write(b'\x1b');gögn_staða.stdin.flush();ljúka_OFFSET=time.monotonic()+.2
            while time.monotonic()<ljúka_OFFSET:hald_atvik(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            skel('terminal');hald_atvik(.3)
            gögn=(verk_rót/'build/verification/new-java/스윙시험.class').read_bytes()
            senda('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(gögn),64):senda(gögn[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            senda(b'.\n')
            senda('java 스윙시험\n'.encode(),b'SWING READY')
            ljúka_OFFSET=time.monotonic()+3
            while time.monotonic()<ljúka_OFFSET:hald_atvik(.1)
            # JFrame centered at (120,100), content at y=130.
            senda(smella_hnappur(200,210),b'',)  # focus JTextField
            gögn_staða.stdin.write('누리'.encode());gögn_staða.stdin.flush()
            ljúka_OFFSET=time.monotonic()+.3
            while time.monotonic()<ljúka_OFFSET:hald_atvik(.05)
            NIÐURSTAÐA=senda(smella_hnappur(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(LOG_lína)-len(NIÐURSTAÐA))
            senda(flýtileið_VALUE(1),b'TERMINAL FOCUS 2')
            NIÐURSTAÐA=skel('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in NIÐURSTAÐA
            senda(smella_hnappur(180,12),b'TERMINAL FOCUS 1')
            ljúka_OFFSET=time.monotonic()+.3
            while time.monotonic()<ljúka_OFFSET:hald_atvik(.05)
            with socket.socket(socket.AF_UNIX) as stafkóði:
                stafkóði.settimeout(10);stafkóði.connect(str(모의제어접속))
                with stafkóði.makefile('rwb') as skrá_færsla_3d0c1245:
                    json.loads(skrá_færsla_3d0c1245.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(endastaður_VALUE_staða/'native-swing.png'),'format':'png'}}):
                        skrá_færsla_3d0c1245.write((json.dumps(요청값)+'\n').encode());skrá_færsla_3d0c1245.flush()
                        while True:
                            반환값=json.loads(skrá_færsla_3d0c1245.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            senda(smella_hnappur(505,115))
            skel('echo SWING_CLOSED_OK')
            gögn=(klasi_slóð/'한글창시험.class').read_bytes()
            senda('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(gögn),64):senda(gögn[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            senda(b'.\n')
            senda('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            senda(smella_hnappur(200,255),'KOREAN SWING CLICK Heiti'.encode())
            senda(smella_hnappur(505,115))
            skel('echo KOREAN_SWING_CLOSED_OK')
            prófun_skrá.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','Íslenska Gluggi/hnappur/동작알림/atvik_biðröð directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if gögn_staða.poll() is None:gögn_staða.terminate()
            try:gögn_staða.wait(timeout=5)
            except subprocess.TimeoutExpired:gögn_staða.kill();gögn_staða.wait()
            val_a916db4e.close();gögn_staða.stdin.close();gögn_staða.stdout.close();(endastaður_VALUE_staða/'serial.log').write_bytes(LOG_lína);(endastaður_VALUE_staða/'report.json').write_text(json.dumps(prófun_skrá,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Keyra_2()
