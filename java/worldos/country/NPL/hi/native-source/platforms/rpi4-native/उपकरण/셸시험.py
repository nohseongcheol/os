#!/usr/bin/env python3
"""निज 커널의 शेल, 프로세스 इनपुट_आउटपुट, Unicode GUI 터미널을 वास्तविक_डेटा raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from निष्पादित_करें_आदेश import प्रोजेक्ट_करें_मूल, आदेश


def चलाएँ():
    출력결과 = प्रोजेक्ट_करें_मूल / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    प्रमाणीकरण_रिपोर्ट = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((प्रोजेक्ट_करें_मूल / 'build/kernel8.img').read_bytes()).hexdigest()}
    बोला_गया_पाठ = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        प्रक्रिया = subprocess.Popen(आदेश()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        तैयारी_मॉनीटर=selectors.DefaultSelector(); तैयारी_मॉनीटर.register(प्रक्रिया.stdout,selectors.EVENT_READ)
        def 수신하기(मार्कर, 시간제한=45):
            आँकड़े=bytearray(); समाप्त_करें_ऑफ़सेट=time.monotonic()+시간제한
            while मार्कर not in आँकड़े:
                if time.monotonic()>समाप्त_करें_ऑफ़सेट or प्रक्रिया.poll() is not None: raise AssertionError('UART timeout/exit: '+आँकड़े.decode('utf-8','replace'))
                for 누름값,_ in तैयारी_मॉनीटर.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: आँकड़े.extend(조각); बोला_गया_पाठ.extend(조각)
                if b'PANIC:' in आँकड़े or b'FAIL ' in आँकड़े: raise AssertionError(आँकड़े)
            return आँकड़े.decode('utf-8','replace').replace('\r\n','\n')
        def भेजें(आँकड़े, मार्कर=b'jkoros-native> '):
            प्रक्रिया.stdin.write(आँकड़े); प्रक्रिया.stdin.flush(); return 수신하기(मार्कर)
        def शेल(पंक्ति, *예상결과):
            परिणाम=भेजें(पंक्ति.encode()+b'\n')
            for मान in 예상결과: assert मान in परिणाम, (पंक्ति,मान,परिणाम)
            return परिणाम
        def संचिका(नाम):
            पाठ=शेल('hex '+नाम,'HEX BEGIN','HEX END'); खोज_परिणाम=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',पाठ,re.S)
            आँकड़े=bytes.fromhex(''.join(खोज_परिणाम.group(2).split())); assert len(आँकड़े)==int(खोज_परिणाम.group(1)); return आँकड़े
        try:
            수신하기(b'jkoros-native> ')
            शेल('mkdir 작업; cd 작업; pwd','/작업')
            शेल('mkdir 하위; echo "한글 आँकड़े 😀" > अभिनन्दन_ae353e94.txt')
            assert संचिका('अभिनन्दन_ae353e94.txt')=='한글 आँकड़े 😀\n'.encode()
            शेल('cp अभिनन्दन_ae353e94.txt आवृत्ति_मान.txt; mv आवृत्ति_मान.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 आँकड़े 😀')
            शेल('cd 하위; cat ../अभिनन्दन_ae353e94.txt; cat /작업/अभिनन्दन_ae353e94.txt; pwd','한글 आँकड़े 😀','/작업/하위')
            शेल('cd ..; rmdir 하위; echo $?','1\n')
            शेल('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            शेल('cp अभिनन्दन_ae353e94.txt अभिनन्दन_ae353e94.txt; echo $?','1\n'); assert संचिका('अभिनन्दन_ae353e94.txt')=='한글 आँकड़े 😀\n'.encode()
            शेल('export अभिनन्दन_ae353e94=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in संचिका('अभिनन्दन_ae353e94.txt')
            शेल("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert संचिका('리터럴')=='$인사\n누리\n'.encode()
            शेल('echo one > स्टेटमेंट_मान; echo two >> स्टेटमेंट_मान; echo three >> स्टेटमेंट_मान')
            शेल('cat < स्टेटमेंट_मान | grep t | tee 추림 | wc -l','2\n'); assert संचिका('추림')==b'two\nthree\n'
            शेल('head -n 1 स्टेटमेंट_मान > सामने_मान; tail -n 1 स्टेटमेंट_मान > वापस_मान'); assert संचिका('앞')==b'one\n'; assert संचिका('뒤')==b'three\n'
            शेल('grep absent स्टेटमेंट_मान; echo $?','1\n')
            शेल('echo untouched > रक्षित_करें_मान')
            शेल('echo destroyed > रक्षित_करें_मान |','명령이 빠졌습니다'); assert संचिका('रक्षित_करें_मान')==b'untouched\n'
            शेल('echo "oops','따옴표가 닫히지 않았습니다')
            शेल('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            शेल('echo bad 2> रक्षित_करें_मान','번호를 지정한 संचिका 서술자 इनपुट_आउटपुट स्विच_मोड'); assert संचिका('रक्षित_करें_मान')==b'untouched\n'
            शेल('rm 빈파일 리터럴 स्टेटमेंट_मान 추림 सामने_मान वापस_मान रक्षित_करें_मान')
            प्रमाणीकरण_रिपोर्ट['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            शेल("python -c 'print(123)' | wc -c",'4\n')
            शेल("python -c 'print(456)' > ऐप_f5044b9b.txt"); assert संचिका('ऐप_f5044b9b.txt')==b'456\n'
            शेल("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            शेल("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < ऐप_f5044b9b.txt", "b'456\\n'", "b''")
            शेल("python -c 'print(\"x\"*17000)' | wc -c", 'त्रुटि -28')
            शेल('echo recovered | wc -c','10\n')
            शेल("python -c 'import jkoros; print(jkoros.read("+'"/작업/ऐप_f5044b9b.txt"'+"))'",'456','exit 0')
            शेल('cd /; javac Hello.java','Compiled:','exit 0')
            शेल('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in संचिका('/작업/자바.txt')
            शेल('cd 작업; echo "echo script > 실행결과" > आदेश.sh; echo "false || echo recovered >> 실행결과" >> आदेश.sh; sh आदेश.sh')
            assert संचिका('실행결과')==b'script\nrecovered\n'
            शेल('rm 실행결과; echo "exit 7" > निर्गमन_ऐप.sh; sh निर्गमन_ऐप.sh; echo $?','7\n')
            शेल('rm निर्गमन_ऐप.sh आदेश.sh ऐप_f5044b9b.txt 자바.txt अभिनन्दन_ae353e94.txt; cd /; rmdir 작업')
            प्रमाणीकरण_रिपोर्ट['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            शेल('echo history-proof','history-proof')
            परिणाम=भेजें(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert परिणाम.count('history-proof')>=2, परिणाम
            भेजें(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            परिणाम=भेजें(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in परिणाम, परिणाम
            परिणाम=भेजें(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in परिणाम,परिणाम
            परिणाम=भेजें('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in परिणाम,परिणाम
            긴글='한글'*50
            परिणाम=भेजें(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in परिणाम
            शेल('terminal','TERMINAL READY')
            शेल('clear')
            शेल('echo "한글 आदेशपटल ABC xyz 012 😀"','한글 आदेशपटल ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as क्लायंट:
                क्लायंट.settimeout(10); क्लायंट.connect(str(모의제어접속))
                with क्लायंट.makefile('rwb') as स्ट्रीम_मान:
                    json.loads(स्ट्रीम_मान.readline())
                    def 호출(नाम,तर्क_सरणी=None):
                        नेटवर्क_ईमेल={'execute':नाम}
                        if तर्क_सरणी: नेटवर्क_ईमेल['arguments']=तर्क_सरणी
                        स्ट्रीम_मान.write((json.dumps(नेटवर्क_ईमेल)+'\n').encode()); स्ट्रीम_मान.flush()
                        while True:
                            उत्तर=json.loads(स्ट्रीम_मान.readline())
                            if 'error' in उत्तर: raise AssertionError(उत्तर)
                            if 'return' in उत्तर: return उत्तर['return']
                    호출('qmp_capabilities')
                    छवि=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(छवि),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    आँकड़े=छवि.read_bytes().split(b'\n',3)[3]
                    def पिक्सेल(x_निर्देशांक,세로좌표): return tuple(आँकड़े[(세로좌표*640+x_निर्देशांक)*3:(세로좌표*640+x_निर्देशांक)*3+3])
                    assert पिक्सेल(12,48)==(32,80,144),पिक्सेल(12,48)
                    assert len(set(पिक्सेल(x_निर्देशांक,세로좌표) for 세로좌표 in range(100,116) for x_निर्देशांक in range(24,56)))>1,'Hangul glyphs missing'
                    शेल('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    शेल("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(छवि),'format':'ppm'})
                    복원자료=छवि.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    शेल('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): शेल('echo scroll-'+str(순번),'scroll-'+str(순번))
                    भेजें(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    परिणाम=भेजें(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in परिणाम,परिणाम
                    शेल('rm visible.txt')
                    호출('quit')
            प्रक्रिया.wait(timeout=5)
            प्रमाणीकरण_रिपोर्ट['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            प्रमाणीकरण_रिपोर्ट['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if प्रक्रिया.poll() is None:
                प्रक्रिया.terminate()
                try: प्रक्रिया.wait(timeout=5)
                except subprocess.TimeoutExpired: प्रक्रिया.kill(); प्रक्रिया.wait()
            तैयारी_मॉनीटर.close(); प्रक्रिया.stdin.close(); प्रक्रिया.stdout.close()
            (출력결과/'serial.log').write_bytes(बोला_गया_पाठ)
            (출력결과/'report.json').write_text(json.dumps(प्रमाणीकरण_रिपोर्ट,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': चलाएँ()
