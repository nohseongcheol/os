#!/usr/bin/env python3
"""ذاتي 커널의 셸, 프로세스 إدخال_إخراج, Unicode GUI 터미널을 الفعلي_بيانات raspi4b에서 اختبارات."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from ينفذ_أمر import يعرض_جذر, أمر


def تشغيل():
    الناتج = يعرض_جذر / 'build/verification/shell'; الناتج.mkdir(parents=True, exist_ok=True)
    التحقق_من_صحة_إبلاغ = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((يعرض_جذر / 'build/kernel8.img').read_bytes()).hexdigest()}
    نسخة_مكتوبة = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        عملية = subprocess.Popen(أمر()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(عملية.stdout,selectors.EVENT_READ)
        def يستلم_رسالة(علامة, 시간제한=45):
            بيانات=bytearray(); إنهاء_مكالمة_إزاحة=time.monotonic()+시간제한
            while علامة not in بيانات:
                if time.monotonic()>إنهاء_مكالمة_إزاحة or عملية.poll() is not None: raise AssertionError('UART timeout/exit: '+بيانات.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: بيانات.extend(조각); نسخة_مكتوبة.extend(조각)
                if b'PANIC:' in بيانات or b'FAIL ' in بيانات: raise AssertionError(بيانات)
            return بيانات.decode('utf-8','replace').replace('\r\n','\n')
        def يرسل(بيانات, علامة=b'jkoros-native> '):
            عملية.stdin.write(بيانات); عملية.stdin.flush(); return يستلم_رسالة(علامة)
        def 셸(سطر, *예상결과):
            نتيجة=يرسل(سطر.encode()+b'\n')
            for قيمة in 예상결과: assert قيمة in نتيجة, (سطر,قيمة,نتيجة)
            return نتيجة
        def ملف(اسم):
            نص=셸('hex '+اسم,'HEX BEGIN','HEX END'); بحث_مقياس=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',نص,re.S)
            بيانات=bytes.fromhex(''.join(بحث_مقياس.group(2).split())); assert len(بيانات)==int(بحث_مقياس.group(1)); return بيانات
        try:
            يستلم_رسالة(b'jkoros-native> ')
            셸('mkdir 작업; cd 작업; pwd','/작업')
            셸('mkdir 하위; echo "한글 بيانات 😀" > 인사.txt')
            assert ملف('인사.txt')=='한글 بيانات 😀\n'.encode()
            셸('cp 인사.txt مثيل_قيمة.txt; mv مثيل_قيمة.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 بيانات 😀')
            셸('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 بيانات 😀','/작업/하위')
            셸('cd ..; rmdir 하위; echo $?','1\n')
            셸('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            셸('cp 인사.txt 인사.txt; echo $?','1\n'); assert ملف('인사.txt')=='한글 بيانات 😀\n'.encode()
            셸('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in ملف('인사.txt')
            셸("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert ملف('리터럴')=='$인사\n누리\n'.encode()
            셸('echo one > كشف_قيمة; echo two >> كشف_قيمة; echo three >> كشف_قيمة')
            셸('cat < كشف_قيمة | grep t | tee 추림 | wc -l','2\n'); assert ملف('추림')==b'two\nthree\n'
            셸('head -n 1 كشف_قيمة > الكاميرا_الأمامية_قيمة; tail -n 1 كشف_قيمة > عودة_قيمة'); assert ملف('앞')==b'one\n'; assert ملف('뒤')==b'three\n'
            셸('grep absent كشف_قيمة; echo $?','1\n')
            셸('echo untouched > يحمي_قيمة')
            셸('echo destroyed > يحمي_قيمة |','명령이 빠졌습니다'); assert ملف('يحمي_قيمة')==b'untouched\n'
            셸('echo "oops','따옴표가 닫히지 않았습니다')
            셸('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            셸('echo bad 2> يحمي_قيمة','번호를 지정한 ملف 서술자 إدخال_إخراج تبديل_الوضع'); assert ملف('يحمي_قيمة')==b'untouched\n'
            셸('rm 빈파일 리터럴 كشف_قيمة 추림 الكاميرا_الأمامية_قيمة عودة_قيمة يحمي_قيمة')
            التحقق_من_صحة_إبلاغ['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            셸("python -c 'print(123)' | wc -c",'4\n')
            셸("python -c 'print(456)' > تطبيق_f5044b9b.txt"); assert ملف('تطبيق_f5044b9b.txt')==b'456\n'
            셸("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            셸("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < تطبيق_f5044b9b.txt", "b'456\\n'", "b''")
            셸("python -c 'print(\"x\"*17000)' | wc -c", 'خطأ -28')
            셸('echo recovered | wc -c','10\n')
            셸("python -c 'import jkoros; print(jkoros.read("+'"/작업/تطبيق_f5044b9b.txt"'+"))'",'456','exit 0')
            셸('cd /; javac Hello.java','Compiled:','exit 0')
            셸('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in ملف('/작업/자바.txt')
            셸('cd 작업; echo "echo script > 실행결과" > أمر.sh; echo "false || echo recovered >> 실행결과" >> أمر.sh; sh أمر.sh')
            assert ملف('실행결과')==b'script\nrecovered\n'
            셸('rm 실행결과; echo "exit 7" > خروج_تطبيق.sh; sh خروج_تطبيق.sh; echo $?','7\n')
            셸('rm خروج_تطبيق.sh أمر.sh تطبيق_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            التحقق_من_صحة_إبلاغ['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            셸('echo history-proof','history-proof')
            نتيجة=يرسل(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert نتيجة.count('history-proof')>=2, نتيجة
            يرسل(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            نتيجة=يرسل(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in نتيجة, نتيجة
            نتيجة=يرسل(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in نتيجة,نتيجة
            نتيجة=يرسل('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in نتيجة,نتيجة
            긴글='한글'*50
            نتيجة=يرسل(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in نتيجة
            셸('terminal','TERMINAL READY')
            셸('clear')
            셸('echo "한글 طرفية ABC xyz 012 😀"','한글 طرفية ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as عميل:
                عميل.settimeout(10); عميل.connect(str(모의제어접속))
                with عميل.makefile('rwb') as بث_قيمة:
                    json.loads(بث_قيمة.readline())
                    def 호출(اسم,وسيطة_صفيف=None):
                        شبكة_رسالة={'execute':اسم}
                        if وسيطة_صفيف: شبكة_رسالة['arguments']=وسيطة_صفيف
                        بث_قيمة.write((json.dumps(شبكة_رسالة)+'\n').encode()); بث_قيمة.flush()
                        while True:
                            رد=json.loads(بث_قيمة.readline())
                            if 'error' in رد: raise AssertionError(رد)
                            if 'return' in رد: return رد['return']
                    호출('qmp_capabilities')
                    صورة=الناتج/'terminal.ppm'; 호출('screendump',{'filename':str(صورة),'format':'ppm'})
                    호출('screendump',{'filename':str(الناتج/'terminal.png'),'format':'png'})
                    بيانات=صورة.read_bytes().split(b'\n',3)[3]
                    def عنصر_صورة(الإحداثي_س,الزر_Y_إحداثيات): return tuple(بيانات[(الزر_Y_إحداثيات*640+الإحداثي_س)*3:(الزر_Y_إحداثيات*640+الإحداثي_س)*3+3])
                    assert عنصر_صورة(12,48)==(32,80,144),عنصر_صورة(12,48)
                    assert len(set(عنصر_صورة(الإحداثي_س,الزر_Y_إحداثيات) for الزر_Y_إحداثيات in range(100,116) for الإحداثي_س in range(24,56)))>1,'Hangul glyphs missing'
                    셸('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    셸("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(صورة),'format':'ppm'})
                    복원자료=صورة.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    셸('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): 셸('echo scroll-'+str(순번),'scroll-'+str(순번))
                    يرسل(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(الناتج/'terminal-scroll.png'),'format':'png'})
                    نتيجة=يرسل(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in نتيجة,نتيجة
                    셸('rm visible.txt')
                    호출('quit')
            عملية.wait(timeout=5)
            التحقق_من_صحة_إبلاغ['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            التحقق_من_صحة_إبلاغ['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if عملية.poll() is None:
                عملية.terminate()
                try: عملية.wait(timeout=5)
                except subprocess.TimeoutExpired: عملية.kill(); عملية.wait()
            준비살피미.close(); عملية.stdin.close(); عملية.stdout.close()
            (الناتج/'serial.log').write_bytes(نسخة_مكتوبة)
            (الناتج/'report.json').write_text(json.dumps(التحقق_من_صحة_إبلاغ,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': تشغيل()
