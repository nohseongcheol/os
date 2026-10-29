#!/usr/bin/env python3
"""자체 커널의 شيل, 프로세스 입출력, Unicode GUI 터미널을 اصلي_ڪوائف raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from تعميل_ڪرڻ_حڪم import 기준, حڪم


def هلائڻ():
    출력결과 = 기준 / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    ڪارگر_رپورٽ = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        عمل_a7054519 = subprocess.Popen(حڪم()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(عمل_a7054519.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            ڪوائف=bytearray(); ختم_ڪريو_آف_سيٽ=time.monotonic()+시간제한
            while 확인표시 not in ڪوائف:
                if time.monotonic()>ختم_ڪريو_آف_سيٽ or عمل_a7054519.poll() is not None: raise AssertionError('UART timeout/exit: '+ڪوائف.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: ڪوائف.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in ڪوائف or b'FAIL ' in ڪوائف: raise AssertionError(ڪوائف)
            return ڪوائف.decode('utf-8','replace').replace('\r\n','\n')
        def اي_ميل(ڪوائف, 확인표시=b'jkoros-native> '):
            عمل_a7054519.stdin.write(ڪوائف); عمل_a7054519.stdin.flush(); return 수신하기(확인표시)
        def شيل(لڪير, *예상결과):
            결과=اي_ميل(لڪير.encode()+b'\n')
            for قدر in 예상결과: assert قدر in 결과, (لڪير,قدر,결과)
            return 결과
        def فائل(نالو):
            متن=شيل('hex '+نالو,'HEX BEGIN','HEX END'); 찾은결과=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',متن,re.S)
            ڪوائف=bytes.fromhex(''.join(찾은결과.group(2).split())); assert len(ڪوائف)==int(찾은결과.group(1)); return ڪوائف
        try:
            수신하기(b'jkoros-native> ')
            شيل('mkdir 작업; cd 작업; pwd','/작업')
            شيل('mkdir 하위; echo "한글 ڪوائف 😀" > 인사.txt')
            assert فائل('인사.txt')=='한글 ڪوائف 😀\n'.encode()
            شيل('cp 인사.txt نقل_قدر.txt; mv نقل_قدر.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 ڪوائف 😀')
            شيل('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 ڪوائف 😀','/작업/하위')
            شيل('cd ..; rmdir 하위; echo $?','1\n')
            شيل('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            شيل('cp 인사.txt 인사.txt; echo $?','1\n'); assert فائل('인사.txt')=='한글 ڪوائف 😀\n'.encode()
            شيل('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in فائل('인사.txt')
            شيل("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert فائل('리터럴')=='$인사\n누리\n'.encode()
            شيل('echo one > بيان_قدر; echo two >> بيان_قدر; echo three >> بيان_قدر')
            شيل('cat < بيان_قدر | grep t | tee 추림 | wc -l','2\n'); assert فائل('추림')==b'two\nthree\n'
            شيل('head -n 1 بيان_قدر > 앞; tail -n 1 بيان_قدر > واپس_قدر'); assert فائل('앞')==b'one\n'; assert فائل('뒤')==b'three\n'
            شيل('grep absent بيان_قدر; echo $?','1\n')
            شيل('echo untouched > حفاظت_ڪريو_قدر')
            شيل('echo destroyed > حفاظت_ڪريو_قدر |','명령이 빠졌습니다'); assert فائل('حفاظت_ڪريو_قدر')==b'untouched\n'
            شيل('echo "oops','따옴표가 닫히지 않았습니다')
            شيل('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            شيل('echo bad 2> حفاظت_ڪريو_قدر','번호를 지정한 فائل 서술자 입출력 سوئچ_موڊ'); assert فائل('حفاظت_ڪريو_قدر')==b'untouched\n'
            شيل('rm 빈파일 리터럴 بيان_قدر 추림 앞 واپس_قدر حفاظت_ڪريو_قدر')
            ڪارگر_رپورٽ['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            شيل("python -c 'print(123)' | wc -c",'4\n')
            شيل("python -c 'print(456)' > ائپ_f5044b9b.txt"); assert فائل('ائپ_f5044b9b.txt')==b'456\n'
            شيل("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            شيل("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < ائپ_f5044b9b.txt", "b'456\\n'", "b''")
            شيل("python -c 'print(\"x\"*17000)' | wc -c", 'نقص -28')
            شيل('echo recovered | wc -c','10\n')
            شيل("python -c 'import jkoros; print(jkoros.read("+'"/작업/ائپ_f5044b9b.txt"'+"))'",'456','exit 0')
            شيل('cd /; javac Hello.java','Compiled:','exit 0')
            شيل('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in فائل('/작업/자바.txt')
            شيل('cd 작업; echo "echo script > 실행결과" > حڪم.sh; echo "false || echo recovered >> 실행결과" >> حڪم.sh; sh حڪم.sh')
            assert فائل('실행결과')==b'script\nrecovered\n'
            شيل('rm 실행결과; echo "exit 7" > خارج_ڪريو_ائپ.sh; sh خارج_ڪريو_ائپ.sh; echo $?','7\n')
            شيل('rm خارج_ڪريو_ائپ.sh حڪم.sh ائپ_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            ڪارگر_رپورٽ['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            شيل('echo history-proof','history-proof')
            결과=اي_ميل(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert 결과.count('history-proof')>=2, 결과
            اي_ميل(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            결과=اي_ميل(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in 결과, 결과
            결과=اي_ميل(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in 결과,결과
            결과=اي_ميل('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in 결과,결과
            긴글='한글'*50
            결과=اي_ميل(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in 결과
            شيل('terminal','TERMINAL READY')
            شيل('clear')
            شيل('echo "한글 터미널 ABC xyz 012 😀"','한글 터미널 ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as گراهڪ:
                گراهڪ.settimeout(10); گراهڪ.connect(str(모의제어접속))
                with گراهڪ.makefile('rwb') as اسٽريم_قدر:
                    json.loads(اسٽريم_قدر.readline())
                    def 호출(نالو,دليل_ترتيب=None):
                        نيٽ_ورڪ_پيغام={'execute':نالو}
                        if دليل_ترتيب: نيٽ_ورڪ_پيغام['arguments']=دليل_ترتيب
                        اسٽريم_قدر.write((json.dumps(نيٽ_ورڪ_پيغام)+'\n').encode()); اسٽريم_قدر.flush()
                        while True:
                            جواب_ڏيو=json.loads(اسٽريم_قدر.readline())
                            if 'error' in جواب_ڏيو: raise AssertionError(جواب_ڏيو)
                            if 'return' in جواب_ڏيو: return جواب_ڏيو['return']
                    호출('qmp_capabilities')
                    نقش=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(نقش),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    ڪوائف=نقش.read_bytes().split(b'\n',3)[3]
                    def پيل(x_رطبو,세로좌표): return tuple(ڪوائف[(세로좌표*640+x_رطبو)*3:(세로좌표*640+x_رطبو)*3+3])
                    assert پيل(12,48)==(32,80,144),پيل(12,48)
                    assert len(set(پيل(x_رطبو,세로좌표) for 세로좌표 in range(100,116) for x_رطبو in range(24,56)))>1,'Hangul glyphs missing'
                    شيل('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    شيل("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(نقش),'format':'ppm'})
                    복원자료=نقش.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    شيل('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): شيل('echo scroll-'+str(순번),'scroll-'+str(순번))
                    اي_ميل(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    결과=اي_ميل(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in 결과,결과
                    شيل('rm visible.txt')
                    호출('quit')
            عمل_a7054519.wait(timeout=5)
            ڪارگر_رپورٽ['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            ڪارگر_رپورٽ['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if عمل_a7054519.poll() is None:
                عمل_a7054519.terminate()
                try: عمل_a7054519.wait(timeout=5)
                except subprocess.TimeoutExpired: عمل_a7054519.kill(); عمل_a7054519.wait()
            준비살피미.close(); عمل_a7054519.stdin.close(); عمل_a7054519.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(ڪارگر_رپورٽ,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': هلائڻ()
