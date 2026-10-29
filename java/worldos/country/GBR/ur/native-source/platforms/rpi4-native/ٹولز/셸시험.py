#!/usr/bin/env python3
"""اپنا 커널의 شیل, 프로세스 ان_پٹ_آؤٹ_پٹ, Unicode GUI 터미널을 اصل_کوائف raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from نفاذ_کریں_حکم import عکس_ڈالنا_روٹ, حکم


def چلائیں():
    출력결과 = عکس_ڈالنا_روٹ / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    توثیق_رپورٹ = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((عکس_ڈالنا_روٹ / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        عمل_کاری = subprocess.Popen(حکم()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(عمل_کاری.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            کوائف=bytearray(); اختتام_آفسٹ=time.monotonic()+시간제한
            while 확인표시 not in کوائف:
                if time.monotonic()>اختتام_آفسٹ or عمل_کاری.poll() is not None: raise AssertionError('UART timeout/exit: '+کوائف.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: کوائف.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in کوائف or b'FAIL ' in کوائف: raise AssertionError(کوائف)
            return کوائف.decode('utf-8','replace').replace('\r\n','\n')
        def بھیجیں(کوائف, 확인표시=b'jkoros-native> '):
            عمل_کاری.stdin.write(کوائف); عمل_کاری.stdin.flush(); return 수신하기(확인표시)
        def شیل(اندراج_کی_سطر, *예상결과):
            پیمائش=بھیجیں(اندراج_کی_سطر.encode()+b'\n')
            for قدر in 예상결과: assert قدر in پیمائش, (اندراج_کی_سطر,قدر,پیمائش)
            return پیمائش
        def فائل_کا_نام(نام):
            متن=شیل('hex '+نام,'HEX BEGIN','HEX END'); تلاش_پیمائش=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',متن,re.S)
            کوائف=bytes.fromhex(''.join(تلاش_پیمائش.group(2).split())); assert len(کوائف)==int(تلاش_پیمائش.group(1)); return کوائف
        try:
            수신하기(b'jkoros-native> ')
            شیل('mkdir 작업; cd 작업; pwd','/작업')
            شیل('mkdir 하위; echo "한글 کوائف 😀" > 인사.txt')
            assert فائل_کا_نام('인사.txt')=='한글 کوائف 😀\n'.encode()
            شیل('cp 인사.txt نقل_قدر.txt; mv نقل_قدر.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 کوائف 😀')
            شیل('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 کوائف 😀','/작업/하위')
            شیل('cd ..; rmdir 하위; echo $?','1\n')
            شیل('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            شیل('cp 인사.txt 인사.txt; echo $?','1\n'); assert فائل_کا_نام('인사.txt')=='한글 کوائف 😀\n'.encode()
            شیل('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in فائل_کا_نام('인사.txt')
            شیل("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert فائل_کا_نام('리터럴')=='$인사\n누리\n'.encode()
            شیل('echo one > بیان_قدر; echo two >> بیان_قدر; echo three >> بیان_قدر')
            شیل('cat < بیان_قدر | grep t | tee 추림 | wc -l','2\n'); assert فائل_کا_نام('추림')==b'two\nthree\n'
            شیل('head -n 1 بیان_قدر > 앞; tail -n 1 بیان_قدر > واپس_قدر'); assert فائل_کا_نام('앞')==b'one\n'; assert فائل_کا_نام('뒤')==b'three\n'
            شیل('grep absent بیان_قدر; echo $?','1\n')
            شیل('echo untouched > بچانا_قدر')
            شیل('echo destroyed > بچانا_قدر |','명령이 빠졌습니다'); assert فائل_کا_نام('بچانا_قدر')==b'untouched\n'
            شیل('echo "oops','따옴표가 닫히지 않았습니다')
            شیل('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            شیل('echo bad 2> بچانا_قدر','번호를 지정한 فائل_کا_نام 서술자 ان_پٹ_آؤٹ_پٹ سوئچ_موڈ'); assert فائل_کا_نام('بچانا_قدر')==b'untouched\n'
            شیل('rm 빈파일 리터럴 بیان_قدر 추림 앞 واپس_قدر بچانا_قدر')
            توثیق_رپورٹ['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            شیل("python -c 'print(123)' | wc -c",'4\n')
            شیل("python -c 'print(456)' > ایپ_f5044b9b.txt"); assert فائل_کا_نام('ایپ_f5044b9b.txt')==b'456\n'
            شیل("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            شیل("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < ایپ_f5044b9b.txt", "b'456\\n'", "b''")
            شیل("python -c 'print(\"x\"*17000)' | wc -c", 'غلطی -28')
            شیل('echo recovered | wc -c','10\n')
            شیل("python -c 'import jkoros; print(jkoros.read("+'"/작업/ایپ_f5044b9b.txt"'+"))'",'456','exit 0')
            شیل('cd /; javac Hello.java','Compiled:','exit 0')
            شیل('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in فائل_کا_نام('/작업/자바.txt')
            شیل('cd 작업; echo "echo script > 실행결과" > حکم.sh; echo "false || echo recovered >> 실행결과" >> حکم.sh; sh حکم.sh')
            assert فائل_کا_نام('실행결과')==b'script\nrecovered\n'
            شیل('rm 실행결과; echo "exit 7" > خروج_ایپ.sh; sh خروج_ایپ.sh; echo $?','7\n')
            شیل('rm خروج_ایپ.sh حکم.sh ایپ_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            توثیق_رپورٹ['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            شیل('echo history-proof','history-proof')
            پیمائش=بھیجیں(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert پیمائش.count('history-proof')>=2, پیمائش
            بھیجیں(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            پیمائش=بھیجیں(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in پیمائش, پیمائش
            پیمائش=بھیجیں(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in پیمائش,پیمائش
            پیمائش=بھیجیں('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in پیمائش,پیمائش
            긴글='한글'*50
            پیمائش=بھیجیں(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in پیمائش
            شیل('terminal','TERMINAL READY')
            شیل('clear')
            شیل('echo "한글 حکم_کی_تشریح_کرنے_والا ABC xyz 012 😀"','한글 حکم_کی_تشریح_کرنے_والا ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as کلائنٹ:
                کلائنٹ.settimeout(10); کلائنٹ.connect(str(모의제어접속))
                with کلائنٹ.makefile('rwb') as بہاؤ_قدر:
                    json.loads(بہاؤ_قدر.readline())
                    def 호출(نام,دلائل_لڑی=None):
                        نیٹ_ورک_پیغام={'execute':نام}
                        if دلائل_لڑی: نیٹ_ورک_پیغام['arguments']=دلائل_لڑی
                        بہاؤ_قدر.write((json.dumps(نیٹ_ورک_پیغام)+'\n').encode()); بہاؤ_قدر.flush()
                        while True:
                            جواب_دیں=json.loads(بہاؤ_قدر.readline())
                            if 'error' in جواب_دیں: raise AssertionError(جواب_دیں)
                            if 'return' in جواب_دیں: return جواب_دیں['return']
                    호출('qmp_capabilities')
                    نقش=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(نقش),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    کوائف=نقش.read_bytes().split(b'\n',3)[3]
                    def پکسل(ایکس_مربوط,세로좌표): return tuple(کوائف[(세로좌표*640+ایکس_مربوط)*3:(세로좌표*640+ایکس_مربوط)*3+3])
                    assert پکسل(12,48)==(32,80,144),پکسل(12,48)
                    assert len(set(پکسل(ایکس_مربوط,세로좌표) for 세로좌표 in range(100,116) for ایکس_مربوط in range(24,56)))>1,'Hangul glyphs missing'
                    شیل('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    شیل("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(نقش),'format':'ppm'})
                    복원자료=نقش.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    شیل('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): شیل('echo scroll-'+str(순번),'scroll-'+str(순번))
                    بھیجیں(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    پیمائش=بھیجیں(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in پیمائش,پیمائش
                    شیل('rm visible.txt')
                    호출('quit')
            عمل_کاری.wait(timeout=5)
            توثیق_رپورٹ['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            توثیق_رپورٹ['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if عمل_کاری.poll() is None:
                عمل_کاری.terminate()
                try: عمل_کاری.wait(timeout=5)
                except subprocess.TimeoutExpired: عمل_کاری.kill(); عمل_کاری.wait()
            준비살피미.close(); عمل_کاری.stdin.close(); عمل_کاری.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(توثیق_رپورٹ,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': چلائیں()
