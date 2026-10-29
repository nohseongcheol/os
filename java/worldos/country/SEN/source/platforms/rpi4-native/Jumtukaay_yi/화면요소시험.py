#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from def_ndigel import 기준,ndigel

def daw():
    목적위치=기준/'build/verification/swing';목적위치.mkdir(parents=True,exist_ok=True)
    maas_Yoonu_jëmale=기준/'build/verification/new-java';maas_Yoonu_jëmale.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'dist/jkoros-native-korean.jar'),'-d',str(maas_Yoonu_jëmale),str(기준/'시험/자바/스윙시험.java'),str(기준/'시험/자바/한글창시험.java')])
    wéral_tënk={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()};làq_Dënk=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        자료위치=subprocess.Popen(ndigel()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        tànnkat_a916db4e=selectors.DefaultSelector();tànnkat_a916db4e.register(자료위치.stdout,selectors.EVENT_READ)
        def yombal_xewxew(초단위=.1):
            for 누름값,_ in tànnkat_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:làq_Dënk.extend(둘째값)
            assert b'PANIC:' not in làq_Dënk and b'HALTED' not in làq_Dënk,làq_Dënk[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            jeexal_Randal=time.monotonic()+초단위
            while 확인표시 not in làq_Dënk[현재위치:]:
                if time.monotonic()>jeexal_Randal or 자료위치.poll() is not None:raise AssertionError(làq_Dënk[현재위치:].decode('utf-8','replace'))
                yombal_xewxew()
            return bytes(làq_Dënk[현재위치:])
        def Yónnee(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(làq_Dënk);자료위치.stdin.write(둘째값);자료위치.stdin.flush();return 기다리기(확인표시,현재위치)
        def Wëreef(araf_yu_bennoo_mbir):return Yónnee((araf_yu_bennoo_mbir+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def Teggi_xëyma(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def bës_butoñ(rëddu_iks_yi,세로좌표):return bytes([30,1,1,rëddu_iks_yi&255,rëddu_iks_yi>>8,세로좌표&255,세로좌표>>8,30,1,0,rëddu_iks_yi&255,rëddu_iks_yi>>8,세로좌표&255,세로좌표>>8])
        def ndigel_anam():
            자료위치.stdin.write(b'\x1b');자료위치.stdin.flush();jeexal_Randal=time.monotonic()+.2
            while time.monotonic()<jeexal_Randal:yombal_xewxew(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            Wëreef('terminal');yombal_xewxew(.3)
            mbir=(기준/'build/verification/new-java/스윙시험.class').read_bytes()
            Yónnee('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(mbir),64):Yónnee(mbir[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            Yónnee(b'.\n')
            Yónnee('java 스윙시험\n'.encode(),b'SWING READY')
            jeexal_Randal=time.monotonic()+3
            while time.monotonic()<jeexal_Randal:yombal_xewxew(.1)
            # JFrame centered at (120,100), content at y=130.
            Yónnee(bës_butoñ(200,210),b'',)  # focus JTextField
            자료위치.stdin.write('누리'.encode());자료위치.stdin.flush()
            jeexal_Randal=time.monotonic()+.3
            while time.monotonic()<jeexal_Randal:yombal_xewxew(.05)
            결과=Yónnee(bës_butoñ(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(làq_Dënk)-len(결과))
            Yónnee(Teggi_xëyma(1),b'TERMINAL FOCUS 2')
            결과=Wëreef('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in 결과
            Yónnee(bës_butoñ(180,12),b'TERMINAL FOCUS 1')
            jeexal_Randal=time.monotonic()+.3
            while time.monotonic()<jeexal_Randal:yombal_xewxew(.05)
            with socket.socket(socket.AF_UNIX) as kotu_araf:
                kotu_araf.settimeout(10);kotu_araf.connect(str(모의제어접속))
                with kotu_araf.makefile('rwb') as bara_denc_dugal_xabaar:
                    json.loads(bara_denc_dugal_xabaar.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(목적위치/'native-swing.png'),'format':'png'}}):
                        bara_denc_dugal_xabaar.write((json.dumps(요청값)+'\n').encode());bara_denc_dugal_xabaar.flush()
                        while True:
                            반환값=json.loads(bara_denc_dugal_xabaar.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            Yónnee(bës_butoñ(505,115))
            Wëreef('echo SWING_CLOSED_OK')
            mbir=(maas_Yoonu_jëmale/'한글창시험.class').read_bytes()
            Yónnee('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(mbir),64):Yónnee(mbir[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            Yónnee(b'.\n')
            Yónnee('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            Yónnee(bës_butoñ(200,255),'KOREAN SWING CLICK tur_253d1510'.encode())
            Yónnee(bës_butoñ(505,115))
            Wëreef('echo KOREAN_SWING_CLOSED_OK')
            wéral_tënk.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','한국어 palanteer/butoñ/동작알림/xewxew_Topplante_xaarandi directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if 자료위치.poll() is None:자료위치.terminate()
            try:자료위치.wait(timeout=5)
            except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            tànnkat_a916db4e.close();자료위치.stdin.close();자료위치.stdout.close();(목적위치/'serial.log').write_bytes(làq_Dënk);(목적위치/'report.json').write_text(json.dumps(wéral_tënk,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':daw()
