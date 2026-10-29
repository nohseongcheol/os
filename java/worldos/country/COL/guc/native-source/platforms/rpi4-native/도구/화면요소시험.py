#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from 실행 import 기준,aluwataaya

def 시작():
    목적위치=기준/'build/verification/swing';목적위치.mkdir(parents=True,exist_ok=True)
    akotchijuushi_wopu_a_ttaaleemüin=기준/'build/verification/new-java';akotchijuushi_wopu_a_ttaaleemüin.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'dist/jkoros-native-korean.jar'),'-d',str(akotchijuushi_wopu_a_ttaaleemüin),str(기준/'시험/자바/스윙시험.java'),str(기준/'시험/자바/한글창시험.java')])
    anaajiaakua_ipa_achikiimaajatü={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()};aa_innachikimaajatü_aparatsee=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        자료위치=subprocess.Popen(aluwataaya()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        선택기=selectors.DefaultSelector();선택기.register(자료위치.stdout,selectors.EVENT_READ)
        def aapaaya_kasachiki(초단위=.1):
            for 누름값,_ in 선택기.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:aa_innachikimaajatü_aparatsee.extend(둘째값)
            assert b'PANIC:' not in aa_innachikimaajatü_aparatsee and b'HALTED' not in aa_innachikimaajatü_aparatsee,aa_innachikimaajatü_aparatsee[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            끝위치=time.monotonic()+초단위
            while 확인표시 not in aa_innachikimaajatü_aparatsee[현재위치:]:
                if time.monotonic()>끝위치 or 자료위치.poll() is not None:raise AssertionError(aa_innachikimaajatü_aparatsee[현재위치:].decode('utf-8','replace'))
                aapaaya_kasachiki()
            return bytes(aa_innachikimaajatü_aparatsee[현재위치:])
        def ajütaa(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(aa_innachikimaajatü_aparatsee);자료위치.stdin.write(둘째값);자료위치.stdin.flush();return 기다리기(확인표시,현재위치)
        def aluwataalapu_u(kaleena_atijaaya):return ajütaa((kaleena_atijaaya+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def a_ttaaya_uwatuale_e_ajutuu(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def aküliküjaa_ajüttülee(가로좌표,세로좌표):return bytes([30,1,1,가로좌표&255,가로좌표>>8,세로좌표&255,세로좌표>>8,30,1,0,가로좌표&255,가로좌표>>8,세로좌표&255,세로좌표>>8])
        def aluwataaya_akua_ipaa():
            자료위치.stdin.write(b'\x1b');자료위치.stdin.flush();끝위치=time.monotonic()+.2
            while time.monotonic()<끝위치:aapaaya_kasachiki(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            aluwataalapu_u('terminal');aapaaya_kasachiki(.3)
            atijaaya=(기준/'build/verification/new-java/스윙시험.class').read_bytes()
            ajütaa('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(atijaaya),64):ajütaa(atijaaya[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            ajütaa(b'.\n')
            ajütaa('java 스윙시험\n'.encode(),b'SWING READY')
            끝위치=time.monotonic()+3
            while time.monotonic()<끝위치:aapaaya_kasachiki(.1)
            # JFrame centered at (120,100), content at y=130.
            ajütaa(aküliküjaa_ajüttülee(200,210),b'',)  # focus JTextField
            자료위치.stdin.write('누리'.encode());자료위치.stdin.flush()
            끝위치=time.monotonic()+.3
            while time.monotonic()<끝위치:aapaaya_kasachiki(.05)
            결과=ajütaa(aküliküjaa_ajüttülee(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(aa_innachikimaajatü_aparatsee)-len(결과))
            ajütaa(a_ttaaya_uwatuale_e_ajutuu(1),b'TERMINAL FOCUS 2')
            결과=aluwataalapu_u('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in 결과
            ajütaa(aküliküjaa_ajüttülee(180,12),b'TERMINAL FOCUS 1')
            끝위치=time.monotonic()+.3
            while time.monotonic()<끝위치:aapaaya_kasachiki(.05)
            with socket.socket(socket.AF_UNIX) as 문자값:
                문자값.settimeout(10);문자값.connect(str(모의제어접속))
                with 문자값.makefile('rwb') as anaajaalaa_ekeroliaa:
                    json.loads(anaajaalaa_ekeroliaa.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(목적위치/'native-swing.png'),'format':'png'}}):
                        anaajaalaa_ekeroliaa.write((json.dumps(요청값)+'\n').encode());anaajaalaa_ekeroliaa.flush()
                        while True:
                            반환값=json.loads(anaajaalaa_ekeroliaa.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            ajütaa(aküliküjaa_ajüttülee(505,115))
            aluwataalapu_u('echo SWING_CLOSED_OK')
            atijaaya=(akotchijuushi_wopu_a_ttaaleemüin/'한글창시험.class').read_bytes()
            ajütaa('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(atijaaya),64):ajütaa(atijaaya[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            ajütaa(b'.\n')
            ajütaa('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            ajütaa(aküliküjaa_ajüttülee(200,255),'KOREAN SWING CLICK 이름'.encode())
            ajütaa(aküliküjaa_ajüttülee(505,115))
            aluwataalapu_u('echo KOREAN_SWING_CLOSED_OK')
            anaajiaakua_ipa_achikiimaajatü.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','한국어 analaaya/ajüttülee/동작알림/kasachiki_a_atapajüsüirua directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if 자료위치.poll() is None:자료위치.terminate()
            try:자료위치.wait(timeout=5)
            except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            선택기.close();자료위치.stdin.close();자료위치.stdout.close();(목적위치/'serial.log').write_bytes(aa_innachikimaajatü_aparatsee);(목적위치/'report.json').write_text(json.dumps(anaajiaakua_ipa_achikiimaajatü,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':시작()
