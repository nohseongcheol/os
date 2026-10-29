#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from לבצע_פקודה import לשקף_בסיס,פקודה

def הפעלה():
    יעד_ערך_עמדה=לשקף_בסיס/'build/verification/windows';יעד_ערך_עמדה.mkdir(parents=True,exist_ok=True)
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
            מעטפת('mkdir first; cd first; export NAME=one')
            שלח('vi 첫째.py\n'.encode(),b'NORMAL')
            שלח('i값 = 21\nprint(ערך * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            סיים_שיחה_היסט=time.monotonic()+3
            while time.monotonic()<סיים_שיחה_היסט:נקודת_אחיזה_אירוע(.1)
            שלח(קיצור_דרך_ערך(1),b'TERMINAL FOCUS 2');נקודת_אחיזה_אירוע(.2)
            assert b'/\r\n' in מעטפת('pwd')
            מעטפת('export NAME=two')
            שלח('vi 둘째.txt\n'.encode(),b'NORMAL')
            שלח('i두 번째 חלון\n'.encode(),b'INSERT')
            שלח(לחץ_מקש(180,12),b'TERMINAL FOCUS 1');נקודת_אחיזה_אירוע(.2)
            פקודה_מצב();שלח(b':wq\r')
            assert b'one:/first' in מעטפת('echo "$NAME:$PWD"')
            assert 'ערך = 21\r\nprint(ערך * 2)'.encode() in מעטפת('cat 첫째.py')
            תוצאה=מעטפת('python 첫째.py');assert b'42\r\n' in תוצאה,תוצאה
            # Close the first shell with its actual title-bar X; second editor resumes.
            שלח(לחץ_מקש(560,63),b'TERMINAL FOCUS 2');נקודת_אחיזה_אירוע(.2)
            פקודה_מצב();שלח(b':wq\r')
            assert b'two:/' in מעטפת('echo "$NAME:$PWD"')
            assert '두 번째 חלון'.encode() in מעטפת('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            שלח('vi 둘째.txt\n'.encode(),b'NORMAL');שלח(b'xu',b'NORMAL')
            שלח(b'iX',b'INSERT');פקודה_מצב();שלח(b':q\r',b'Unsaved')
            שלח(b':q!\r');assert '두 번째 חלון'.encode() in מעטפת('cat 둘째.txt')
            שלח(קיצור_דרך_ערך(1),b'TERMINAL FOCUS 1');נקודת_אחיזה_אירוע(.2)
            שלח(קיצור_דרך_ערך(1),b'TERMINAL FOCUS 3');נקודת_אחיזה_אירוע(.2)
            שלח(קיצור_דרך_ערך(1),b'TERMINAL FOCUS 4');נקודת_אחיזה_אירוע(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            נתונים_עמדה.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));נתונים_עמדה.stdin.flush()
            מעטפת('echo DRAGGED_OK')
            שלח('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            שלח('i저장하지 않은 נתונים'.encode(),b'INSERT')
            שלח(לחץ_מקש(578,97),b'TERMINAL FOCUS 3');נקודת_אחיזה_אירוע(.2)
            assert '버릴문서.txt'.encode() not in מעטפת('ls')
            שלח(קיצור_דרך_ערך(1),b'TERMINAL FOCUS 4');נקודת_אחיזה_אירוע(.2)
            מעטפת('echo REUSED_WINDOW_OK')
            הושלם_סכום=לרשום_שיא.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',הושלם_סכום)
            # UART completion precedes the next QEMU display refresh.
            סיים_שיחה_היסט=time.monotonic()+.3
            while time.monotonic()<סיים_שיחה_היסט:נקודת_אחיזה_אירוע(.05)
            with socket.socket(socket.AF_UNIX) as נקודת_קוד:
                נקודת_קוד.settimeout(10);נקודת_קוד.connect(str(모의제어접속))
                with נקודת_קוד.makefile('rwb') as קובץ_ערך:
                    json.loads(קובץ_ערך.readline())
                    for בקשה_ערך in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(יעד_ערך_עמדה/'four-terminals.png'),'format':'png'}}):
                        קובץ_ערך.write((json.dumps(בקשה_ערך)+'\n').encode());קובץ_ערך.flush()
                        while True:
                            반환값=json.loads(קובץ_ערך.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(יעד_ערך_עמדה/'four-terminals.png')).convert('RGB')
            for זוג_קואורדינטות,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(זוג_קואורדינטות)==색상,(זוג_קואורדינטות,화소들.getpixel(זוג_קואורדינטות))
            מעטפת('echo FOUR_WINDOWS_OK')
            אימות_דוח.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if נתונים_עמדה.poll() is None:נתונים_עמדה.terminate()
            try:נתונים_עמדה.wait(timeout=5)
            except subprocess.TimeoutExpired:נתונים_עמדה.kill();נתונים_עמדה.wait()
            בורר_a916db4e.close();נתונים_עמדה.stdin.close();נתונים_עמדה.stdout.close();(יעד_ערך_עמדה/'serial.log').write_bytes(לרשום_שיא);(יעד_ערך_עמדה/'report.json').write_text(json.dumps(אימות_דוח,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':הפעלה()
