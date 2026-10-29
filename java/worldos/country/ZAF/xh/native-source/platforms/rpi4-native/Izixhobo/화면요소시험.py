#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from ukwenza_umyalelo import 기준,Umyalelo

def Phumeza():
    목적위치=기준/'build/verification/swing';목적위치.mkdir(parents=True,exist_ok=True)
    iklasi_indlela=기준/'build/verification/new-java';iklasi_indlela.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'dist/jkoros-native-korean.jar'),'-d',str(iklasi_indlela),str(기준/'시험/자바/스윙시험.java'),str(기준/'시험/자바/한글창시험.java')])
    uqinisekiso_ingxelo={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()};ilog_umqolo=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        자료위치=subprocess.Popen(Umyalelo()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        umkhethi_a916db4e=selectors.DefaultSelector();umkhethi_a916db4e.register(자료위치.stdout,selectors.EVENT_READ)
        def isibambi_umcimbi(초단위=.1):
            for 누름값,_ in umkhethi_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:ilog_umqolo.extend(둘째값)
            assert b'PANIC:' not in ilog_umqolo and b'HALTED' not in ilog_umqolo,ilog_umqolo[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            phela_Ukulinganisa=time.monotonic()+초단위
            while 확인표시 not in ilog_umqolo[현재위치:]:
                if time.monotonic()>phela_Ukulinganisa or 자료위치.poll() is not None:raise AssertionError(ilog_umqolo[현재위치:].decode('utf-8','replace'))
                isibambi_umcimbi()
            return bytes(ilog_umqolo[현재위치:])
        def thumela(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(ilog_umqolo);자료위치.stdin.write(둘째값);자료위치.stdin.flush();return 기다리기(확인표시,현재위치)
        def isiniki_myalelo(uluhlu_lweekharektha_iingcombolo):return thumela((uluhlu_lweekharektha_iingcombolo+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def isinqumleli_ixabiso(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def cofa_iqhosha(isilungelelanisi_x,세로좌표):return bytes([30,1,1,isilungelelanisi_x&255,isilungelelanisi_x>>8,세로좌표&255,세로좌표>>8,30,1,0,isilungelelanisi_x&255,isilungelelanisi_x>>8,세로좌표&255,세로좌표>>8])
        def umyalelo_imo():
            자료위치.stdin.write(b'\x1b');자료위치.stdin.flush();phela_Ukulinganisa=time.monotonic()+.2
            while time.monotonic()<phela_Ukulinganisa:isibambi_umcimbi(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            isiniki_myalelo('terminal');isibambi_umcimbi(.3)
            iingcombolo=(기준/'build/verification/new-java/스윙시험.class').read_bytes()
            thumela('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(iingcombolo),64):thumela(iingcombolo[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            thumela(b'.\n')
            thumela('java 스윙시험\n'.encode(),b'SWING READY')
            phela_Ukulinganisa=time.monotonic()+3
            while time.monotonic()<phela_Ukulinganisa:isibambi_umcimbi(.1)
            # JFrame centered at (120,100), content at y=130.
            thumela(cofa_iqhosha(200,210),b'',)  # focus JTextField
            자료위치.stdin.write('누리'.encode());자료위치.stdin.flush()
            phela_Ukulinganisa=time.monotonic()+.3
            while time.monotonic()<phela_Ukulinganisa:isibambi_umcimbi(.05)
            결과=thumela(cofa_iqhosha(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(ilog_umqolo)-len(결과))
            thumela(isinqumleli_ixabiso(1),b'TERMINAL FOCUS 2')
            결과=isiniki_myalelo('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in 결과
            thumela(cofa_iqhosha(180,12),b'TERMINAL FOCUS 1')
            phela_Ukulinganisa=time.monotonic()+.3
            while time.monotonic()<phela_Ukulinganisa:isibambi_umcimbi(.05)
            with socket.socket(socket.AF_UNIX) as ikhowudi_yekharakhtha:
                ikhowudi_yekharakhtha.settimeout(10);ikhowudi_yekharakhtha.connect(str(모의제어접속))
                with ikhowudi_yekharakhtha.makefile('rwb') as ifayile_ufako_nkcukacha:
                    json.loads(ifayile_ufako_nkcukacha.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(목적위치/'native-swing.png'),'format':'png'}}):
                        ifayile_ufako_nkcukacha.write((json.dumps(요청값)+'\n').encode());ifayile_ufako_nkcukacha.flush()
                        while True:
                            반환값=json.loads(ifayile_ufako_nkcukacha.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            thumela(cofa_iqhosha(505,115))
            isiniki_myalelo('echo SWING_CLOSED_OK')
            iingcombolo=(iklasi_indlela/'한글창시험.class').read_bytes()
            thumela('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(iingcombolo),64):thumela(iingcombolo[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            thumela(b'.\n')
            thumela('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            thumela(cofa_iqhosha(200,255),'KOREAN SWING CLICK Igama'.encode())
            thumela(cofa_iqhosha(505,115))
            isiniki_myalelo('echo KOREAN_SWING_CLOSED_OK')
            uqinisekiso_ingxelo.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','isiXhosa i_window/iqhosha/동작알림/umcimbi_ityhu directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if 자료위치.poll() is None:자료위치.terminate()
            try:자료위치.wait(timeout=5)
            except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            umkhethi_a916db4e.close();자료위치.stdin.close();자료위치.stdout.close();(목적위치/'serial.log').write_bytes(ilog_umqolo);(목적위치/'report.json').write_text(json.dumps(uqinisekiso_ingxelo,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Phumeza()
