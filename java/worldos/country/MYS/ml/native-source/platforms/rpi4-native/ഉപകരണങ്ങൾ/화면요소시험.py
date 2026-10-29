#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from നടപ്പാക്കുക_കമാന്_ഡ് import പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം,ആജ്ഞ

def നടപ്പിലാക്കുക():
    ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം_പദവി=പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'build/verification/swing';ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം_പദവി.mkdir(parents=True,exist_ok=True)
    ക്ലാസ്_പാത=പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'build/verification/new-java';ക്ലാസ്_പാത.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'dist/jkoros-native-korean.jar'),'-d',str(ക്ലാസ്_പാത),str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'시험/자바/스윙시험.java'),str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'시험/자바/한글창시험.java')])
    నిర్ధారణ_నివేదిక={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'build/kernel8.img').read_bytes()).hexdigest()};ലോഗ്_രേഖ=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        ഡാറ്റാ_പദവി=subprocess.Popen(ആജ്ഞ()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        సెలక్టర్_a916db4e=selectors.DefaultSelector();సెలక్టర్_a916db4e.register(ഡാറ്റാ_പദവി.stdout,selectors.EVENT_READ)
        def കൈകാര്യംചെയ്യല്_ഇവന്റ്(초단위=.1):
            for 누름값,_ in సెలక్టర్_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:ലോഗ്_രേഖ.extend(둘째값)
            assert b'PANIC:' not in ലോഗ്_രേഖ and b'HALTED' not in ലോഗ്_രേഖ,ലോഗ്_രേഖ[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            അവസാനിപ്പിക്കുക_ഓഫ്_സെറ്റ്=time.monotonic()+초단위
            while 확인표시 not in ലോഗ്_രേഖ[현재위치:]:
                if time.monotonic()>അവസാനിപ്പിക്കുക_ഓഫ്_സെറ്റ് or ഡാറ്റാ_പദവി.poll() is not None:raise AssertionError(ലോഗ്_രേഖ[현재위치:].decode('utf-8','replace'))
                കൈകാര്യംചെയ്യല്_ഇവന്റ്()
            return bytes(ലോഗ്_രേഖ[현재위치:])
        def അയയ്ക്കുക(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(ലോഗ്_രേഖ);ഡാറ്റാ_പദവി.stdin.write(둘째값);ഡാറ്റാ_പദവി.stdin.flush();return 기다리기(확인표시,현재위치)
        def ഷെല്(സ്ട്രിംഗ്_ഡാറ്റാ):return അയയ്ക്കുക((സ്ട്രിംഗ്_ഡാറ്റാ+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def എളുപ്പവഴി_മൂല്യം(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def ക്ലിക്ക്_ചെയ്യുക_ബട്ടണ്(x_ഏകോപനം,Y_ബട്ടൺ_ഏകോപനം):return bytes([30,1,1,x_ഏകോപനം&255,x_ഏകോപനം>>8,Y_ബട്ടൺ_ഏകോപനം&255,Y_ബട്ടൺ_ഏകോപനം>>8,30,1,0,x_ഏകോപനം&255,x_ഏകോപനം>>8,Y_ബട്ടൺ_ഏകോപനം&255,Y_ബട്ടൺ_ഏകോപനം>>8])
        def കമാന്_ഡ്_മോഡ്():
            ഡാറ്റാ_പദവി.stdin.write(b'\x1b');ഡാറ്റാ_പദവി.stdin.flush();അവസാനിപ്പിക്കുക_ഓഫ്_സെറ്റ്=time.monotonic()+.2
            while time.monotonic()<അവസാനിപ്പിക്കുക_ഓഫ്_സെറ്റ്:കൈകാര്യംചെയ്യല്_ഇവന്റ്(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            ഷെല്('terminal');കൈകാര്യംചെയ്യല്_ഇവന്റ്(.3)
            ഡാറ്റാ=(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'build/verification/new-java/스윙시험.class').read_bytes()
            അയയ്ക്കുക('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(ഡാറ്റാ),64):അയയ്ക്കുക(ഡാറ്റാ[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            അയയ്ക്കുക(b'.\n')
            അയയ്ക്കുക('java 스윙시험\n'.encode(),b'SWING READY')
            അവസാനിപ്പിക്കുക_ഓഫ്_സെറ്റ്=time.monotonic()+3
            while time.monotonic()<അവസാനിപ്പിക്കുക_ഓഫ്_സെറ്റ്:കൈകാര്യംചെയ്യല്_ഇവന്റ്(.1)
            # JFrame centered at (120,100), content at y=130.
            അയയ്ക്കുക(ക്ലിക്ക്_ചെയ്യുക_ബട്ടണ്(200,210),b'',)  # focus JTextField
            ഡാറ്റാ_പദവി.stdin.write('누리'.encode());ഡാറ്റാ_പദവി.stdin.flush()
            അവസാനിപ്പിക്കുക_ഓഫ്_സെറ്റ്=time.monotonic()+.3
            while time.monotonic()<അവസാനിപ്പിക്കുക_ഓഫ്_സെറ്റ്:കൈകാര്യംചെയ്യല്_ഇവന്റ്(.05)
            അളവ്=അയയ്ക്കുക(ക്ലിക്ക്_ചെയ്യുക_ബട്ടണ്(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(ലോഗ്_രേഖ)-len(അളവ്))
            അയയ്ക്കുക(എളുപ്പവഴി_മൂല്യം(1),b'TERMINAL FOCUS 2')
            അളവ്=ഷെല്('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in അളവ്
            അയയ്ക്കുക(ക്ലിക്ക്_ചെയ്യുക_ബട്ടണ്(180,12),b'TERMINAL FOCUS 1')
            അവസാനിപ്പിക്കുക_ഓഫ്_സെറ്റ്=time.monotonic()+.3
            while time.monotonic()<അവസാനിപ്പിക്കുക_ഓഫ്_സെറ്റ്:കൈകാര്യംചെയ്യല്_ഇവന്റ്(.05)
            with socket.socket(socket.AF_UNIX) as പ്രതീകകോഡ്:
                പ്രതീകകോഡ്.settimeout(10);പ്രതീകകോഡ്.connect(str(모의제어접속))
                with പ്രതീകകോഡ്.makefile('rwb') as ഫയല്_എന്_ട്രി:
                    json.loads(ഫയല്_എന്_ട്രി.readline())
                    for HTTP_അപേക്ഷ_മൂല്യം in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം_പദവി/'native-swing.png'),'format':'png'}}):
                        ഫയല്_എന്_ട്രി.write((json.dumps(HTTP_അപേക്ഷ_മൂല്യം)+'\n').encode());ഫയല്_എന്_ട്രി.flush()
                        while True:
                            반환값=json.loads(ഫയല്_എന്_ട്രി.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            അയയ്ക്കുക(ക്ലിക്ക്_ചെയ്യുക_ബട്ടണ്(505,115))
            ഷെല്('echo SWING_CLOSED_OK')
            ഡാറ്റാ=(ക്ലാസ്_പാത/'한글창시험.class').read_bytes()
            അയയ്ക്കുക('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(ഡാറ്റാ),64):അയയ്ക്കുക(ഡാറ്റാ[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            അയയ്ക്കുക(b'.\n')
            അയയ്ക്കുക('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            അയയ്ക്കുക(ക്ലിക്ക്_ചെയ്യുക_ബട്ടണ്(200,255),'KOREAN SWING CLICK പേരു്'.encode())
            അയയ്ക്കുക(ക്ലിക്ക്_ചെയ്യുക_ബട്ടണ്(505,115))
            ഷെല്('echo KOREAN_SWING_CLOSED_OK')
            నిర్ధారణ_నివేదిక.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','한국어 ജാലകം/ബട്ടണ്/동작알림/ഇവന്റ്_ക്യൂ directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if ഡാറ്റാ_പദവി.poll() is None:ഡാറ്റാ_പദവി.terminate()
            try:ഡാറ്റാ_പദവി.wait(timeout=5)
            except subprocess.TimeoutExpired:ഡാറ്റാ_പദവി.kill();ഡാറ്റാ_പദവി.wait()
            సెలక్టర్_a916db4e.close();ഡാറ്റാ_പദവി.stdin.close();ഡാറ്റാ_പദവി.stdout.close();(ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം_പദവി/'serial.log').write_bytes(ലോഗ്_രേഖ);(ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം_പദവി/'report.json').write_text(json.dumps(నిర్ధారణ_నివేదిక,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':നടപ്പിലാക്കുക()
