#!/usr/bin/env python3
"""עצמי 커널의 מעטפת, 프로세스 קלט_פלט, Unicode GUI 터미널을 בפועל_נתונים raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from לבצע_פקודה import לשקף_בסיס, פקודה


def הפעלה():
    פלט = לשקף_בסיס / 'build/verification/shell'; פלט.mkdir(parents=True, exist_ok=True)
    אימות_דוח = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((לשקף_בסיס / 'build/kernel8.img').read_bytes()).hexdigest()}
    תמליל = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        תהליך = subprocess.Popen(פקודה()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(תהליך.stdout,selectors.EVENT_READ)
        def לקבל_דואר(סמן, 시간제한=45):
            נתונים=bytearray(); סיים_שיחה_היסט=time.monotonic()+시간제한
            while סמן not in נתונים:
                if time.monotonic()>סיים_שיחה_היסט or תהליך.poll() is not None: raise AssertionError('UART timeout/exit: '+נתונים.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: נתונים.extend(조각); תמליל.extend(조각)
                if b'PANIC:' in נתונים or b'FAIL ' in נתונים: raise AssertionError(נתונים)
            return נתונים.decode('utf-8','replace').replace('\r\n','\n')
        def שלח(נתונים, סמן=b'jkoros-native> '):
            תהליך.stdin.write(נתונים); תהליך.stdin.flush(); return לקבל_דואר(סמן)
        def מעטפת(שורה, *예상결과):
            תוצאה=שלח(שורה.encode()+b'\n')
            for ערך in 예상결과: assert ערך in תוצאה, (שורה,ערך,תוצאה)
            return תוצאה
        def קובץ(שם):
            טקסט=מעטפת('hex '+שם,'HEX BEGIN','HEX END'); חפש_תוצאה=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',טקסט,re.S)
            נתונים=bytes.fromhex(''.join(חפש_תוצאה.group(2).split())); assert len(נתונים)==int(חפש_תוצאה.group(1)); return נתונים
        try:
            לקבל_דואר(b'jkoros-native> ')
            מעטפת('mkdir 작업; cd 작업; pwd','/작업')
            מעטפת('mkdir 하위; echo "한글 נתונים 😀" > 인사.txt')
            assert קובץ('인사.txt')=='한글 נתונים 😀\n'.encode()
            מעטפת('cp 인사.txt מופע_ערך.txt; mv מופע_ערך.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 נתונים 😀')
            מעטפת('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 נתונים 😀','/작업/하위')
            מעטפת('cd ..; rmdir 하위; echo $?','1\n')
            מעטפת('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            מעטפת('cp 인사.txt 인사.txt; echo $?','1\n'); assert קובץ('인사.txt')=='한글 נתונים 😀\n'.encode()
            מעטפת('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in קובץ('인사.txt')
            מעטפת("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert קובץ('리터럴')=='$인사\n누리\n'.encode()
            מעטפת('echo one > דוח_ערך; echo two >> דוח_ערך; echo three >> דוח_ערך')
            מעטפת('cat < דוח_ערך | grep t | tee 추림 | wc -l','2\n'); assert קובץ('추림')==b'two\nthree\n'
            מעטפת('head -n 1 דוח_ערך > מצלמה_קדמית_ערך_ec1a6b96; tail -n 1 דוח_ערך > הקודם_ערך'); assert קובץ('앞')==b'one\n'; assert קובץ('뒤')==b'three\n'
            מעטפת('grep absent דוח_ערך; echo $?','1\n')
            מעטפת('echo untouched > הגן_ערך')
            מעטפת('echo destroyed > הגן_ערך |','명령이 빠졌습니다'); assert קובץ('הגן_ערך')==b'untouched\n'
            מעטפת('echo "oops','따옴표가 닫히지 않았습니다')
            מעטפת('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            מעטפת('echo bad 2> הגן_ערך','번호를 지정한 קובץ 서술자 קלט_פלט מתג_מצב'); assert קובץ('הגן_ערך')==b'untouched\n'
            מעטפת('rm 빈파일 리터럴 דוח_ערך 추림 מצלמה_קדמית_ערך_ec1a6b96 הקודם_ערך הגן_ערך')
            אימות_דוח['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            מעטפת("python -c 'print(123)' | wc -c",'4\n')
            מעטפת("python -c 'print(456)' > תוכנית_f5044b9b.txt"); assert קובץ('תוכנית_f5044b9b.txt')==b'456\n'
            מעטפת("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            מעטפת("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < תוכנית_f5044b9b.txt", "b'456\\n'", "b''")
            מעטפת("python -c 'print(\"x\"*17000)' | wc -c", 'שגיאה -28')
            מעטפת('echo recovered | wc -c','10\n')
            מעטפת("python -c 'import jkoros; print(jkoros.read("+'"/작업/תוכנית_f5044b9b.txt"'+"))'",'456','exit 0')
            מעטפת('cd /; javac Hello.java','Compiled:','exit 0')
            מעטפת('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in קובץ('/작업/자바.txt')
            מעטפת('cd 작업; echo "echo script > 실행결과" > פקודה.sh; echo "false || echo recovered >> 실행결과" >> פקודה.sh; sh פקודה.sh')
            assert קובץ('실행결과')==b'script\nrecovered\n'
            מעטפת('rm 실행결과; echo "exit 7" > יציאה_תוכנית.sh; sh יציאה_תוכנית.sh; echo $?','7\n')
            מעטפת('rm יציאה_תוכנית.sh פקודה.sh תוכנית_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            אימות_דוח['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            מעטפת('echo history-proof','history-proof')
            תוצאה=שלח(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert תוצאה.count('history-proof')>=2, תוצאה
            שלח(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            תוצאה=שלח(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in תוצאה, תוצאה
            תוצאה=שלח(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in תוצאה,תוצאה
            תוצאה=שלח('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in תוצאה,תוצאה
            긴글='한글'*50
            תוצאה=שלח(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in תוצאה
            מעטפת('terminal','TERMINAL READY')
            מעטפת('clear')
            מעטפת('echo "한글 מסוף ABC xyz 012 😀"','한글 מסוף ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as לקוח:
                לקוח.settimeout(10); לקוח.connect(str(모의제어접속))
                with לקוח.makefile('rwb') as זרם_ערך:
                    json.loads(זרם_ערך.readline())
                    def 호출(שם,ארגומנט_מערך=None):
                        רשת_דואר={'execute':שם}
                        if ארגומנט_מערך: רשת_דואר['arguments']=ארגומנט_מערך
                        זרם_ערך.write((json.dumps(רשת_דואר)+'\n').encode()); זרם_ערך.flush()
                        while True:
                            מענה=json.loads(זרם_ערך.readline())
                            if 'error' in מענה: raise AssertionError(מענה)
                            if 'return' in מענה: return מענה['return']
                    호출('qmp_capabilities')
                    תמונה=פלט/'terminal.ppm'; 호출('screendump',{'filename':str(תמונה),'format':'ppm'})
                    호출('screendump',{'filename':str(פלט/'terminal.png'),'format':'png'})
                    נתונים=תמונה.read_bytes().split(b'\n',3)[3]
                    def פיקסל(קואורדינטת_x,세로좌표): return tuple(נתונים[(세로좌표*640+קואורדינטת_x)*3:(세로좌표*640+קואורדינטת_x)*3+3])
                    assert פיקסל(12,48)==(32,80,144),פיקסל(12,48)
                    assert len(set(פיקסל(קואורדינטת_x,세로좌표) for 세로좌표 in range(100,116) for קואורדינטת_x in range(24,56)))>1,'Hangul glyphs missing'
                    מעטפת('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    מעטפת("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(תמונה),'format':'ppm'})
                    복원자료=תמונה.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    מעטפת('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): מעטפת('echo scroll-'+str(순번),'scroll-'+str(순번))
                    שלח(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(פלט/'terminal-scroll.png'),'format':'png'})
                    תוצאה=שלח(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in תוצאה,תוצאה
                    מעטפת('rm visible.txt')
                    호출('quit')
            תהליך.wait(timeout=5)
            אימות_דוח['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            אימות_דוח['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if תהליך.poll() is None:
                תהליך.terminate()
                try: תהליך.wait(timeout=5)
                except subprocess.TimeoutExpired: תהליך.kill(); תהליך.wait()
            준비살피미.close(); תהליך.stdin.close(); תהליך.stdout.close()
            (פלט/'serial.log').write_bytes(תמליל)
            (פלט/'report.json').write_text(json.dumps(אימות_דוח,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': הפעלה()
