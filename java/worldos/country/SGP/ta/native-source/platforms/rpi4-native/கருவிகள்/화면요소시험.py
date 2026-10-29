#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from இயக்கு_கட்டளை import திட்டப்பணி_மூலம்,கட்டளை

def செயல்படுத்துக():
    இலக்கு_மதிப்பு_நிலை=திட்டப்பணி_மூலம்/'build/verification/swing';இலக்கு_மதிப்பு_நிலை.mkdir(parents=True,exist_ok=True)
    பிரிவு_பாதை=திட்டப்பணி_மூலம்/'build/verification/new-java';பிரிவு_பாதை.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(திட்டப்பணி_மூலம்/'dist/jkoros-native-korean.jar'),'-d',str(பிரிவு_பாதை),str(திட்டப்பணி_மூலம்/'시험/자바/스윙시험.java'),str(திட்டப்பணி_மூலம்/'시험/자바/한글창시험.java')])
    செல்லுபடியாக்கம்_அறிக்கை={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((திட்டப்பணி_மூலம்/'build/kernel8.img').read_bytes()).hexdigest()};பதிவு_பதிவு=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        தரவு_நிலை=subprocess.Popen(கட்டளை()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        தேர்வி_a916db4e=selectors.DefaultSelector();தேர்வி_a916db4e.register(தரவு_நிலை.stdout,selectors.EVENT_READ)
        def நடத்தி_நிகழ்வு(초단위=.1):
            for 누름값,_ in தேர்வி_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:பதிவு_பதிவு.extend(둘째값)
            assert b'PANIC:' not in பதிவு_பதிவு and b'HALTED' not in பதிவு_பதிவு,பதிவு_பதிவு[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            முடி_ஆஃப்செட்=time.monotonic()+초단위
            while 확인표시 not in பதிவு_பதிவு[현재위치:]:
                if time.monotonic()>முடி_ஆஃப்செட் or தரவு_நிலை.poll() is not None:raise AssertionError(பதிவு_பதிவு[현재위치:].decode('utf-8','replace'))
                நடத்தி_நிகழ்வு()
            return bytes(பதிவு_பதிவு[현재위치:])
        def அனுப்பு(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(பதிவு_பதிவு);தரவு_நிலை.stdin.write(둘째값);தரவு_நிலை.stdin.flush();return 기다리기(확인표시,현재위치)
        def கூடு(சரம்_தரவு):return அனுப்பு((சரம்_தரவு+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def குறுக்குவழி_மதிப்பு(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def கிளிக்_செய்_பொத்தான்(x_ஒத்ததரமுள்ளது,Y_பொத்தான்_அச்சுத்_தொகுப்பு):return bytes([30,1,1,x_ஒத்ததரமுள்ளது&255,x_ஒத்ததரமுள்ளது>>8,Y_பொத்தான்_அச்சுத்_தொகுப்பு&255,Y_பொத்தான்_அச்சுத்_தொகுப்பு>>8,30,1,0,x_ஒத்ததரமுள்ளது&255,x_ஒத்ததரமுள்ளது>>8,Y_பொத்தான்_அச்சுத்_தொகுப்பு&255,Y_பொத்தான்_அச்சுத்_தொகுப்பு>>8])
        def கட்டளை_பயன்முறை():
            தரவு_நிலை.stdin.write(b'\x1b');தரவு_நிலை.stdin.flush();முடி_ஆஃப்செட்=time.monotonic()+.2
            while time.monotonic()<முடி_ஆஃப்செட்:நடத்தி_நிகழ்வு(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            கூடு('terminal');நடத்தி_நிகழ்வு(.3)
            தரவு=(திட்டப்பணி_மூலம்/'build/verification/new-java/스윙시험.class').read_bytes()
            அனுப்பு('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(தரவு),64):அனுப்பு(தரவு[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            அனுப்பு(b'.\n')
            அனுப்பு('java 스윙시험\n'.encode(),b'SWING READY')
            முடி_ஆஃப்செட்=time.monotonic()+3
            while time.monotonic()<முடி_ஆஃப்செட்:நடத்தி_நிகழ்வு(.1)
            # JFrame centered at (120,100), content at y=130.
            அனுப்பு(கிளிக்_செய்_பொத்தான்(200,210),b'',)  # focus JTextField
            தரவு_நிலை.stdin.write('누리'.encode());தரவு_நிலை.stdin.flush()
            முடி_ஆஃப்செட்=time.monotonic()+.3
            while time.monotonic()<முடி_ஆஃப்செட்:நடத்தி_நிகழ்வு(.05)
            அளவிடக்கூடியது=அனுப்பு(கிளிக்_செய்_பொத்தான்(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(பதிவு_பதிவு)-len(அளவிடக்கூடியது))
            அனுப்பு(குறுக்குவழி_மதிப்பு(1),b'TERMINAL FOCUS 2')
            அளவிடக்கூடியது=கூடு('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in அளவிடக்கூடியது
            அனுப்பு(கிளிக்_செய்_பொத்தான்(180,12),b'TERMINAL FOCUS 1')
            முடி_ஆஃப்செட்=time.monotonic()+.3
            while time.monotonic()<முடி_ஆஃப்செட்:நடத்தி_நிகழ்வு(.05)
            with socket.socket(socket.AF_UNIX) as எழுத்துக்குறி_குறியீடு:
                எழுத்துக்குறி_குறியீடு.settimeout(10);எழுத்துக்குறி_குறியீடு.connect(str(모의제어접속))
                with எழுத்துக்குறி_குறியீடு.makefile('rwb') as கோப்பு_உள்ளீடு:
                    json.loads(கோப்பு_உள்ளீடு.readline())
                    for HTTP_வேண்டுதல்_மதிப்பு in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(இலக்கு_மதிப்பு_நிலை/'native-swing.png'),'format':'png'}}):
                        கோப்பு_உள்ளீடு.write((json.dumps(HTTP_வேண்டுதல்_மதிப்பு)+'\n').encode());கோப்பு_உள்ளீடு.flush()
                        while True:
                            반환값=json.loads(கோப்பு_உள்ளீடு.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            அனுப்பு(கிளிக்_செய்_பொத்தான்(505,115))
            கூடு('echo SWING_CLOSED_OK')
            தரவு=(பிரிவு_பாதை/'한글창시험.class').read_bytes()
            அனுப்பு('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(தரவு),64):அனுப்பு(தரவு[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            அனுப்பு(b'.\n')
            அனுப்பு('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            அனுப்பு(கிளிக்_செய்_பொத்தான்(200,255),'KOREAN SWING CLICK பெயர்'.encode())
            அனுப்பு(கிளிக்_செய்_பொத்தான்(505,115))
            கூடு('echo KOREAN_SWING_CLOSED_OK')
            செல்லுபடியாக்கம்_அறிக்கை.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','தமிழ் சாளரம்/பொத்தான்/동작알림/நிகழ்வு_சாரை directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if தரவு_நிலை.poll() is None:தரவு_நிலை.terminate()
            try:தரவு_நிலை.wait(timeout=5)
            except subprocess.TimeoutExpired:தரவு_நிலை.kill();தரவு_நிலை.wait()
            தேர்வி_a916db4e.close();தரவு_நிலை.stdin.close();தரவு_நிலை.stdout.close();(இலக்கு_மதிப்பு_நிலை/'serial.log').write_bytes(பதிவு_பதிவு);(இலக்கு_மதிப்பு_நிலை/'report.json').write_text(json.dumps(செல்லுபடியாக்கம்_அறிக்கை,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':செயல்படுத்துக()
