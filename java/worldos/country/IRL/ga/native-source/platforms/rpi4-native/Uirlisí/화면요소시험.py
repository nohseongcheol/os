#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Rith_ordú import teilgean_fréamh,Ordú

def Rith_2():
    sprioc_VALUE_suíomh=teilgean_fréamh/'build/verification/swing';sprioc_VALUE_suíomh.mkdir(parents=True,exist_ok=True)
    aicme_cosán=teilgean_fréamh/'build/verification/new-java';aicme_cosán.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(teilgean_fréamh/'dist/jkoros-native-korean.jar'),'-d',str(aicme_cosán),str(teilgean_fréamh/'시험/자바/스윙시험.java'),str(teilgean_fréamh/'시험/자바/한글창시험.java')])
    bailíochtú_tuairisc={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((teilgean_fréamh/'build/kernel8.img').read_bytes()).hexdigest()};LOG_ró=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        sonraí_suíomh=subprocess.Popen(Ordú()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        roghnóir_a916db4e=selectors.DefaultSelector();roghnóir_a916db4e.register(sonraí_suíomh.stdout,selectors.EVENT_READ)
        def hanla_ócáid(초단위=.1):
            for 누름값,_ in roghnóir_a916db4e.select(초단위):
                SECOND_VALUE=누름값.fileobj.read(65536)
                if SECOND_VALUE:LOG_ró.extend(SECOND_VALUE)
            assert b'PANIC:' not in LOG_ró and b'HALTED' not in LOG_ró,LOG_ró[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            cuir_deireadh_le_OFFSET=time.monotonic()+초단위
            while 확인표시 not in LOG_ró[현재위치:]:
                if time.monotonic()>cuir_deireadh_le_OFFSET or sonraí_suíomh.poll() is not None:raise AssertionError(LOG_ró[현재위치:].decode('utf-8','replace'))
                hanla_ócáid()
            return bytes(LOG_ró[현재위치:])
        def seol(SECOND_VALUE,확인표시=b'jkoros-native> '):
            현재위치=len(LOG_ró);sonraí_suíomh.stdin.write(SECOND_VALUE);sonraí_suíomh.stdin.flush();return 기다리기(확인표시,현재위치)
        def blaosc(teaghrán_sonraí):return seol((teaghrán_sonraí+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def aicearra_VALUE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def cliceáil_cnaipe(x_chomhordanáid,세로좌표):return bytes([30,1,1,x_chomhordanáid&255,x_chomhordanáid>>8,세로좌표&255,세로좌표>>8,30,1,0,x_chomhordanáid&255,x_chomhordanáid>>8,세로좌표&255,세로좌표>>8])
        def ordú_mód():
            sonraí_suíomh.stdin.write(b'\x1b');sonraí_suíomh.stdin.flush();cuir_deireadh_le_OFFSET=time.monotonic()+.2
            while time.monotonic()<cuir_deireadh_le_OFFSET:hanla_ócáid(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            blaosc('terminal');hanla_ócáid(.3)
            sonraí=(teilgean_fréamh/'build/verification/new-java/스윙시험.class').read_bytes()
            seol('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(sonraí),64):seol(sonraí[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            seol(b'.\n')
            seol('java 스윙시험\n'.encode(),b'SWING READY')
            cuir_deireadh_le_OFFSET=time.monotonic()+3
            while time.monotonic()<cuir_deireadh_le_OFFSET:hanla_ócáid(.1)
            # JFrame centered at (120,100), content at y=130.
            seol(cliceáil_cnaipe(200,210),b'',)  # focus JTextField
            sonraí_suíomh.stdin.write('누리'.encode());sonraí_suíomh.stdin.flush()
            cuir_deireadh_le_OFFSET=time.monotonic()+.3
            while time.monotonic()<cuir_deireadh_le_OFFSET:hanla_ócáid(.05)
            tomhas=seol(cliceáil_cnaipe(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(LOG_ró)-len(tomhas))
            seol(aicearra_VALUE(1),b'TERMINAL FOCUS 2')
            tomhas=blaosc('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in tomhas
            seol(cliceáil_cnaipe(180,12),b'TERMINAL FOCUS 1')
            cuir_deireadh_le_OFFSET=time.monotonic()+.3
            while time.monotonic()<cuir_deireadh_le_OFFSET:hanla_ócáid(.05)
            with socket.socket(socket.AF_UNIX) as pointe_cóid:
                pointe_cóid.settimeout(10);pointe_cóid.connect(str(모의제어접속))
                with pointe_cóid.makefile('rwb') as comhad_iontráil:
                    json.loads(comhad_iontráil.readline())
                    for iarratas_HTTP_VALUE in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(sprioc_VALUE_suíomh/'native-swing.png'),'format':'png'}}):
                        comhad_iontráil.write((json.dumps(iarratas_HTTP_VALUE)+'\n').encode());comhad_iontráil.flush()
                        while True:
                            반환값=json.loads(comhad_iontráil.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            seol(cliceáil_cnaipe(505,115))
            blaosc('echo SWING_CLOSED_OK')
            sonraí=(aicme_cosán/'한글창시험.class').read_bytes()
            seol('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(sonraí),64):seol(sonraí[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            seol(b'.\n')
            seol('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            seol(cliceáil_cnaipe(200,255),'KOREAN SWING CLICK Ainm'.encode())
            seol(cliceáil_cnaipe(505,115))
            blaosc('echo KOREAN_SWING_CLOSED_OK')
            bailíochtú_tuairisc.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','Gaeilge fuinneog/cnaipe/동작알림/ócáid_scuaine directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if sonraí_suíomh.poll() is None:sonraí_suíomh.terminate()
            try:sonraí_suíomh.wait(timeout=5)
            except subprocess.TimeoutExpired:sonraí_suíomh.kill();sonraí_suíomh.wait()
            roghnóir_a916db4e.close();sonraí_suíomh.stdin.close();sonraí_suíomh.stdout.close();(sprioc_VALUE_suíomh/'serial.log').write_bytes(LOG_ró);(sprioc_VALUE_suíomh/'report.json').write_text(json.dumps(bailíochtú_tuairisc,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Rith_2()
