#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from לבצע_פקודה import לשקף_בסיס,פקודה

def הפעלה():
    יעד_ערך_עמדה=לשקף_בסיס/'build/verification/swing';יעד_ערך_עמדה.mkdir(parents=True,exist_ok=True)
    כיתה_נתיב=לשקף_בסיס/'build/verification/new-java';כיתה_נתיב.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(לשקף_בסיס/'dist/jkoros-native-korean.jar'),'-d',str(כיתה_נתיב),str(לשקף_בסיס/'시험/자바/מוסיקת_סווינג_נסה.java'),str(לשקף_בסיס/'시험/자바/한글창시험.java')])
    אימות_דוח={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((לשקף_בסיס/'build/kernel8.img').read_bytes()).hexdigest()};לרשום_שיא=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        נתונים_עמדה=subprocess.Popen(פקודה()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        בורר_a916db4e=selectors.DefaultSelector();בורר_a916db4e.register(נתונים_עמדה.stdout,selectors.EVENT_READ)
        def נקודת_אחיזה_אירוע(초단위=.1):
            for 누름값,_ in בורר_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:לרשום_שיא.extend(둘째값)
            assert b'PANIC:' not in לרשום_שיא and b'HALTED' not in לרשום_שיא,לרשום_שיא[-2048:]
        def 기다리기(סמן,נוכחי_עמדה,초단위=50):
            סיים_שיחה_היסט=time.monotonic()+초단위
            while סמן not in לרשום_שיא[נוכחי_עמדה:]:
                if time.monotonic()>סיים_שיחה_היסט or נתונים_עמדה.poll() is not None:raise AssertionError(לרשום_שיא[נוכחי_עמדה:].decode('utf-8','replace'))
                נקודת_אחיזה_אירוע()
            return bytes(לרשום_שיא[נוכחי_עמדה:])
        def שלח(둘째값,סמן=b'jkoros-native> '):
            נוכחי_עמדה=len(לרשום_שיא);נתונים_עמדה.stdin.write(둘째값);נתונים_עמדה.stdin.flush();return 기다리기(סמן,נוכחי_עמדה)
        def מעטפת(מחרוזת_נתונים):return שלח((מחרוזת_נתונים+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def קיצור_דרך_ערך(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def לחץ_מקש(קואורדינטת_x,세로좌표):return bytes([30,1,1,קואורדינטת_x&255,קואורדינטת_x>>8,세로좌표&255,세로좌표>>8,30,1,0,קואורדינטת_x&255,קואורדינטת_x>>8,세로좌표&255,세로좌표>>8])
        def פקודה_מצב():
            נתונים_עמדה.stdin.write(b'\x1b');נתונים_עמדה.stdin.flush();סיים_שיחה_היסט=time.monotonic()+.2
            while time.monotonic()<סיים_שיחה_היסט:נקודת_אחיזה_אירוע(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            מעטפת('terminal');נקודת_אחיזה_אירוע(.3)
            נתונים=(לשקף_בסיס/'build/verification/new-java/מוסיקת_סווינג_נסה.class').read_bytes()
            שלח('load מוסיקת_סווינג_נסה.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(נתונים),64):שלח(נתונים[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            שלח(b'.\n')
            שלח('java מוסיקת_סווינג_נסה\n'.encode(),b'SWING READY')
            סיים_שיחה_היסט=time.monotonic()+3
            while time.monotonic()<סיים_שיחה_היסט:נקודת_אחיזה_אירוע(.1)
            # JFrame centered at (120,100), content at y=130.
            שלח(לחץ_מקש(200,210),b'',)  # focus JTextField
            נתונים_עמדה.stdin.write('누리'.encode());נתונים_עמדה.stdin.flush()
            סיים_שיחה_היסט=time.monotonic()+.3
            while time.monotonic()<סיים_שיחה_היסט:נקודת_אחיזה_אירוע(.05)
            תוצאה=שלח(לחץ_מקש(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(לרשום_שיא)-len(תוצאה))
            שלח(קיצור_דרך_ערך(1),b'TERMINAL FOCUS 2')
            תוצאה=מעטפת('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in תוצאה
            שלח(לחץ_מקש(180,12),b'TERMINAL FOCUS 1')
            סיים_שיחה_היסט=time.monotonic()+.3
            while time.monotonic()<סיים_שיחה_היסט:נקודת_אחיזה_אירוע(.05)
            with socket.socket(socket.AF_UNIX) as נקודת_קוד:
                נקודת_קוד.settimeout(10);נקודת_קוד.connect(str(모의제어접속))
                with נקודת_קוד.makefile('rwb') as קובץ_ערך:
                    json.loads(קובץ_ערך.readline())
                    for בקשה_ערך in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(יעד_ערך_עמדה/'native-swing.png'),'format':'png'}}):
                        קובץ_ערך.write((json.dumps(בקשה_ערך)+'\n').encode());קובץ_ערך.flush()
                        while True:
                            반환값=json.loads(קובץ_ערך.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            שלח(לחץ_מקש(505,115))
            מעטפת('echo SWING_CLOSED_OK')
            נתונים=(כיתה_נתיב/'한글창시험.class').read_bytes()
            שלח('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(נתונים),64):שלח(נתונים[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            שלח(b'.\n')
            שלח('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            שלח(לחץ_מקש(200,255),'KOREAN SWING CLICK שם'.encode())
            שלח(לחץ_מקש(505,115))
            מעטפת('echo KOREAN_SWING_CLOSED_OK')
            אימות_דוח.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','עברית חלון/לחצן/המלצה_הודעה/אירוע_תור directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if נתונים_עמדה.poll() is None:נתונים_עמדה.terminate()
            try:נתונים_עמדה.wait(timeout=5)
            except subprocess.TimeoutExpired:נתונים_עמדה.kill();נתונים_עמדה.wait()
            בורר_a916db4e.close();נתונים_עמדה.stdin.close();נתונים_עמדה.stdout.close();(יעד_ערך_עמדה/'serial.log').write_bytes(לרשום_שיא);(יעד_ערך_עמדה/'report.json').write_text(json.dumps(אימות_דוח,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':הפעלה()
