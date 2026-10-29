#!/usr/bin/env python3
"""Run all examples in the real combined VNC + SLIP/FTP native VM."""
import ftplib
import hashlib
import io
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from מחשב_שולחני_הצג import 정확한값
from 예제되돌림서버 import הד_שרתים
from לבצע_פקודה import לשקף_בסיס


def נסה_שפה(שפה,הד_שרת_ערך,תוצאה_נתונים):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));העברת_קבצים_מספר_יציאה=임시자원.getsockname()[1]
    תהליך=subprocess.Popen(['python3',str(לשקף_בסיס/'כלים/לבצע_פקודה.py'),'--desktop','--network','--port','0','--ftp-port',str(העברת_קבצים_מספר_יציאה)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    בורר=selectors.DefaultSelector();בורר.register(תהליך.stdout,selectors.EVENT_READ)
    תמליל=bytearray();לקוח=None;העברת_קבצים_קשר=None
    def לקבל_דואר(סמן,הפעלה=0):
        סיים_שיחה_היסט=time.monotonic()+60
        while סמן not in תמליל[הפעלה:]:
            if time.monotonic()>סיים_שיחה_היסט or תהליך.poll() is not None:raise AssertionError(תמליל[הפעלה:].decode('utf-8','replace'))
            for 누름값,_ in בורר.select(.1):
                נתונים=누름값.fileobj.read(65536)
                if נתונים:תמליל.extend(נתונים)
        return תמליל[הפעלה:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(סימן_ערך,누르는중=True):לקוח.sendall(struct.pack('>BBHI',4,int(누르는중),0,סימן_ערך))
    def התחל_היסט(שורה):
        הפעלה=len(תמליל)
        for נקודת_קוד in שורה+'\n':
            סימן_ערך=0xff0d if נקודת_קוד=='\n' else ord(נקודת_קוד) if ord(נקודת_קוד)<256 else 0x1000000|ord(נקודת_קוד)
            누름값(סימן_ערך);누름값(סימן_ערך,False)
        return הפעלה
    def מעטפת(שורה):return לקבל_דואר(b'jkoros-native> ',התחל_היסט(שורה))
    def לבצע_פקודה(שורה,예상결과):
        טקסט=מעטפת(שורה);assert 예상결과 in טקסט and 'exit 0' in טקסט,(שורה,טקסט)
        return טקסט
    def 화소들():
        לקוח.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            אזור_ערך=정확한값(לקוח,1)[0]
            if אזור_ערך==2:continue
            if אזור_ערך==3:
                개수=struct.unpack('>I',정확한값(לקוח,7)[3:])[0];정확한값(לקוח,개수);continue
            assert אזור_ערך==0,אזור_ערך
            항목수=struct.unpack('>H',정확한값(לקוח,3)[1:])[0]
            for _ in range(항목수):
                קואורדינטת_x,세로좌표,너비값,נדרש_גובה_ערך,ערכת_תווים=struct.unpack('>HHHHi',정확한값(לקוח,12));assert ערכת_תווים==0,ערכת_תווים
                נתונים=정확한값(לקוח,너비값*נדרש_גובה_ערך*4)
                for שורה_עמדה in range(נדרש_גובה_ערך):
                    for עמודה_עמדה in range(너비값):
                        원본자료=(שורה_עמדה*너비값+עמודה_עמדה)*4;יעד=((세로좌표+שורה_עמדה)*640+קואורדינטת_x+עמודה_עמדה)*3
                        빛삼원색[יעד:יעד+3]=bytes((נתונים[원본자료+2],נתונים[원본자료+1],נתונים[원본자료]))
            if 항목수:return 빛삼원색
    try:
        לקבל_דואר(b'TERMINAL READY');לקבל_דואר(b'jkoros-native> ',תמליל.rfind(b'TERMINAL READY'))
        מספר_יציאה=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',תמליל).group(1))
        לקוח=socket.create_connection(('127.0.0.1',מספר_יציאה),timeout=10)
        assert 정확한값(לקוח,12)==b'RFB 003.008\n';לקוח.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(לקוח,정확한값(לקוח,1)[0]);לקוח.sendall(b'\x01');assert 정확한값(לקוח,4)==b'\0'*4
        לקוח.sendall(b'\x01');초기값=정확한값(לקוח,24);정확한값(לקוח,struct.unpack('>I',초기값[20:])[0])
        לקוח.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        לקוח.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in מעטפת('ftpd start')
        העברת_קבצים_קשר=ftplib.FTP();העברת_קבצים_קשר.encoding='utf-8';העברת_קבצים_קשר.connect('127.0.0.1',העברת_קבצים_מספר_יציאה,timeout=20);העברת_קבצים_קשר.login()
        מטען_נתונים=('GUI와 FTP 동시 שימוש_ערך '+שפה+' 😀\n').encode()
        העברת_קבצים_קשר.storbinary('STOR 함께.txt',io.BytesIO(מטען_נתונים))
        assert מטען_נתונים.decode().strip() in מעטפת('cat /함께.txt')
        받은수=bytearray();העברת_קבצים_קשר.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==מטען_נתונים;העברת_קבצים_קשר.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        שלח_רשימה=מעטפת('ls /example')
        assert all(שם in שלח_רשימה for שם in ('java/','c/','python/','README.md')),שלח_רשימה
        if שפה=='java':
            חבילה_מניפסט=json.loads((לשקף_בסיס/'build/examples/manifest.json').read_text())
            for נתיב,נקודת_כניסה in חבילה_מניפסט.items():
                מעטפת('cp '+נתיב+' /example-check.bin')
                תוכן_ערך=bytearray();העברת_קבצים_קשר.retrbinary('RETR example-check.bin',תוכן_ערך.extend)
                assert len(תוכן_ערך)==נקודת_כניסה['bytes'] and hashlib.sha256(תוכן_ערך).hexdigest()==נקודת_כניסה['sha256'],נתיב
            העברת_קבצים_קשר.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            בינארי=bytes(range(256))*64
            העברת_קבצים_קשר.storbinary('STOR boundary.bin',io.BytesIO(בינארי))
            תוכן_ערך=bytearray();העברת_קבצים_קשר.retrbinary('RETR boundary.bin',תוכן_ערך.extend)
            assert תוכן_ערך==בינארי and 'boundary.bin' in העברת_קבצים_קשר.nlst()
            מעטפת('cp /boundary.bin /boundary-copy.bin')
            תוכן_ערך=bytearray();העברת_קבצים_קשר.retrbinary('RETR boundary-copy.bin',תוכן_ערך.extend)
            assert תוכן_ערך==בינארי
            העברת_קבצים_קשר.delete('boundary.bin');העברת_קבצים_קשר.delete('boundary-copy.bin')
        assert 'דוגמתפלט' in מעטפת('ls /example/'+שפה)
        מעטפת('cd /example/'+שפה)
        שם_טבלה={'java':'JAVA','c':'C','python':'PYTHON'}[שפה]
        예상파일=שם_טבלה+' קובץ: 한글 נתונים 😀\n'
        if שפה=='java':
            לבצע_פקודה('javac דוגמתפלט.java','Compiled:');לבצע_פקודה('java דוגמתפלט','JAVA פלטטקסט: 안녕하세요 😀')
            לבצע_פקודה('javac דוגמתקובץ.java','Compiled:');לבצע_פקודה('java דוגמתקובץ',예상파일)
            לבצע_פקודה('java דוגמתרשת {} {}'.format(הד_שרת_ערך.יציאת_TCP,הד_שרת_ערך.פרוטוקול_יחידת_נתונים_של_משתמש_הסב),'JAVA 네트워크 ודא_אמת: TCP UDP 한글')
            גרפיקה_פקודה='java דוגמתציור'
        elif שפה=='c':
            for שם,전달값,예상결과 in [('פלטטקסט','', 'C פלטטקסט: 안녕하세요 😀'),('קובץ','',예상파일),
                    ('네트워크',' '+str(הד_שרת_ערך.פרוטוקול_יחידת_נתונים_של_משתמש_הסב),'C 네트워크 ודא_אמת: UDP 한글')]:
                לבצע_פקודה('cc '+שם+'예제.c -o לבצע_פקודה','Compiled native ARM64 ELF:')
                לבצע_פקודה('./לבצע_פקודה'+전달값,예상결과)
            לבצע_פקודה('cc דוגמתציור.c -o לבצע_פקודה','Compiled native ARM64 ELF:');גרפיקה_פקודה='./לבצע_פקודה'
        else:
            for שם,전달값,예상결과 in [('פלטטקסט','','PYTHON פלטטקסט: 안녕하세요 😀'),('קובץ','',예상파일),
                    ('네트워크',' '+str(הד_שרת_ערך.פרוטוקול_יחידת_נתונים_של_משתמש_הסב),'PYTHON 네트워크 ודא_אמת: UDP 한글')]:
                לבצע_פקודה('python '+שם+'예제.py'+전달값,예상결과)
            גרפיקה_פקודה='python דוגמתציור.py'
        התחל_ציור=התחל_היסט(גרפיקה_פקודה)
        טקסט=לקבל_דואר('그림을 확인한 הקודם_ערך Enter를 누르세요.\r\n'.encode(),התחל_ציור)
        assert שם_טבלה+' 그래픽: 빨강 초록 파랑' in טקסט and 'exit 0' not in טקסט,טקסט
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        העברת_קבצים_קשר.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();העברת_קבצים_קשר.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';העברת_קבצים_קשר.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            היסט_ערך=(세로좌표*640+610)*3;assert tuple(빛삼원색[היסט_ערך:היסט_ערך+3])==색상,(שפה,세로좌표,tuple(빛삼원색[היסט_ערך:היסט_ערך+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(תוצאה_נתונים/(שפה+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in לקבל_דואר(b'jkoros-native> ',התחל_ציור)
        if שפה=='java':
            התחל_חלון=התחל_היסט('java דוגמתחלון')
            לקבל_דואר('GUI 예제 להכין: דוגמתחלון'.encode(),התחל_חלון)
            def לחץ_ערך(가로,אנכי_עמדה):
                for לחצן in (1,0):לקוח.sendall(struct.pack('>BBHH',5,לחצן,가로,אנכי_עמדה))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            לחץ_ערך(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for תו_ערך in '한글':누름값(0x1000000|ord(תו_ערך));누름값(0x1000000|ord(תו_ערך),False)
            for 횟수 in (1,2):
                הפעלה=len(תמליל);לחץ_ערך(180,242)
                לקבל_דואר(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),הפעלה)
            time.sleep(.3)
            חלון_ציור=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=חלון_ציור.crop((110,272,530,300)).tobytes()
            חלון_ציור.save(str(תוצאה_נתונים/'java-swing.png'))
            הפעלה=len(תמליל);לחץ_ערך(535,105)
            assert 'exit 0' in לקבל_דואר(b'jkoros-native> ',הפעלה)
        # Download the guest-created bytes through FTP in the same GUI VM.
        קובץ_ערך_שם={'java':'java.txt','c':'c.txt','python':'python.txt'}[שפה]
        מעטפת('cp '+קובץ_ערך_שם+' /לאמת.txt')
        받은수=bytearray();העברת_קבצים_קשר.retrbinary('RETR לאמת.txt',받은수.extend);assert 받은수==예상파일.encode()
        מעטפת('echo preserved > דוגמתפלט.'+('py' if שפה=='python' else שפה))
        assert 'EXAMPLES READY' in מעטפת('example '+שפה)
        assert '\npreserved\n' in מעטפת('cat דוגמתפלט.'+('py' if שפה=='python' else שפה))
        assert '한/אפס_אופרנד מקש_ערך, Shift+Space 또는 F9' in מעטפת('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in מעטפת('echo GUI NETWORK TOGETHER')
        העברת_קבצים_קשר.quit();העברת_קבצים_קשר=None;assert 'FTP stopped' in מעטפת('ftpd stop')
        print('PASS '+שפה+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if העברת_קבצים_קשר:
            try:העברת_קבצים_קשר.close()
            except OSError:pass
        if לקוח:לקוח.close()
        תהליך.terminate()
        try:תהליך.wait(timeout=8)
        except subprocess.TimeoutExpired:תהליך.kill();תהליך.wait()
        בורר.close();תהליך.stdout.close();(תוצאה_נתונים/(שפה+'-serial.log')).write_bytes(תמליל)


def הפעלה():
    תוצאה_נתונים=לשקף_בסיס/'build/verification/examples';תוצאה_נתונים.mkdir(parents=True,exist_ok=True)
    אימות_דוח={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((לשקף_בסיס/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with הד_שרתים() as הד_שרת_ערך:
            for שפה in ('java','c','python'):
                נסה_שפה(שפה,הד_שרת_ערך,תוצאה_נתונים);אימות_דוח['languages'].append(שפה)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert הד_שרת_ערך.수신됨==[(אזור_ערך,נתונים.encode()) for אזור_ערך,נתונים in 예상결과],הד_שרת_ערך.수신됨
            אימות_דוח['host_network_payloads']=[{'protocol':אזור_ערך,'text':נתונים.decode()} for אזור_ערך,נתונים in הד_שרת_ערך.수신됨]
        אימות_דוח.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(תוצאה_נתונים/'report.json').write_text(json.dumps(אימות_דוח,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':הפעלה()
