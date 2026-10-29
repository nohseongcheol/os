#!/usr/bin/env python3
"""자체 커널의 ਸ਼ੈਲ, 프로세스 ਦਾਖਲ_ਹੋਣਾ_ਬਾਹਰ_ਆਉਣਾ, Unicode GUI 터미널을 ਅਸਲ_ਸਮੱਗਰੀ raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ import ਪ੍ਰੋਜੈਕਟ_ਰੂਟ, ਕਮਾਂਡ


def ਚਲਾਓ_2():
    출력결과 = ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    ਮਾਨਤਾ_ਵਿਵਰਨ = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        ਪਰੋਸੈੱਸ = subprocess.Popen(ਕਮਾਂਡ()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(ਪਰੋਸੈੱਸ.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            ਸਮੱਗਰੀ=bytearray(); ਅੰਤ_ਔਫਸੈਟ=time.monotonic()+시간제한
            while 확인표시 not in ਸਮੱਗਰੀ:
                if time.monotonic()>ਅੰਤ_ਔਫਸੈਟ or ਪਰੋਸੈੱਸ.poll() is not None: raise AssertionError('UART timeout/exit: '+ਸਮੱਗਰੀ.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: ਸਮੱਗਰੀ.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in ਸਮੱਗਰੀ or b'FAIL ' in ਸਮੱਗਰੀ: raise AssertionError(ਸਮੱਗਰੀ)
            return ਸਮੱਗਰੀ.decode('utf-8','replace').replace('\r\n','\n')
        def ਈਮੇਲ(ਸਮੱਗਰੀ, 확인표시=b'jkoros-native> '):
            ਪਰੋਸੈੱਸ.stdin.write(ਸਮੱਗਰੀ); ਪਰੋਸੈੱਸ.stdin.flush(); return 수신하기(확인표시)
        def ਸ਼ੈਲ(ਲਾਈਨ, *예상결과):
            ਮਾਪ=ਈਮੇਲ(ਲਾਈਨ.encode()+b'\n')
            for ਕੀਮਤ in 예상결과: assert ਕੀਮਤ in ਮਾਪ, (ਲਾਈਨ,ਕੀਮਤ,ਮਾਪ)
            return ਮਾਪ
        def ਫਾਇਲ(ਨਾਂ):
            ਟੈਕਸਟ=ਸ਼ੈਲ('hex '+ਨਾਂ,'HEX BEGIN','HEX END'); ਖੋਜ_ਮਾਪ=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',ਟੈਕਸਟ,re.S)
            ਸਮੱਗਰੀ=bytes.fromhex(''.join(ਖੋਜ_ਮਾਪ.group(2).split())); assert len(ਸਮੱਗਰੀ)==int(ਖੋਜ_ਮਾਪ.group(1)); return ਸਮੱਗਰੀ
        try:
            수신하기(b'jkoros-native> ')
            ਸ਼ੈਲ('mkdir 작업; cd 작업; pwd','/작업')
            ਸ਼ੈਲ('mkdir 하위; echo "한글 ਸਮੱਗਰੀ 😀" > 인사.txt')
            assert ਫਾਇਲ('인사.txt')=='한글 ਸਮੱਗਰੀ 😀\n'.encode()
            ਸ਼ੈਲ('cp 인사.txt ਇਨਸਟੈਂਸ_ਕੀਮਤ.txt; mv ਇਨਸਟੈਂਸ_ਕੀਮਤ.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 ਸਮੱਗਰੀ 😀')
            ਸ਼ੈਲ('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 ਸਮੱਗਰੀ 😀','/작업/하위')
            ਸ਼ੈਲ('cd ..; rmdir 하위; echo $?','1\n')
            ਸ਼ੈਲ('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            ਸ਼ੈਲ('cp 인사.txt 인사.txt; echo $?','1\n'); assert ਫਾਇਲ('인사.txt')=='한글 ਸਮੱਗਰੀ 😀\n'.encode()
            ਸ਼ੈਲ('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in ਫਾਇਲ('인사.txt')
            ਸ਼ੈਲ("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert ਫਾਇਲ('리터럴')=='$인사\n누리\n'.encode()
            ਸ਼ੈਲ('echo one > ਸਟੇਟਮੈਂਟ_ਕੀਮਤ; echo two >> ਸਟੇਟਮੈਂਟ_ਕੀਮਤ; echo three >> ਸਟੇਟਮੈਂਟ_ਕੀਮਤ')
            ਸ਼ੈਲ('cat < ਸਟੇਟਮੈਂਟ_ਕੀਮਤ | grep t | tee 추림 | wc -l','2\n'); assert ਫਾਇਲ('추림')==b'two\nthree\n'
            ਸ਼ੈਲ('head -n 1 ਸਟੇਟਮੈਂਟ_ਕੀਮਤ > 앞; tail -n 1 ਸਟੇਟਮੈਂਟ_ਕੀਮਤ > ਪਿਛਲਾ_ਕੀਮਤ'); assert ਫਾਇਲ('앞')==b'one\n'; assert ਫਾਇਲ('뒤')==b'three\n'
            ਸ਼ੈਲ('grep absent ਸਟੇਟਮੈਂਟ_ਕੀਮਤ; echo $?','1\n')
            ਸ਼ੈਲ('echo untouched > ਰੱਖਿਆ_ਕਰਨੀ_ਕੀਮਤ')
            ਸ਼ੈਲ('echo destroyed > ਰੱਖਿਆ_ਕਰਨੀ_ਕੀਮਤ |','명령이 빠졌습니다'); assert ਫਾਇਲ('ਰੱਖਿਆ_ਕਰਨੀ_ਕੀਮਤ')==b'untouched\n'
            ਸ਼ੈਲ('echo "oops','따옴표가 닫히지 않았습니다')
            ਸ਼ੈਲ('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            ਸ਼ੈਲ('echo bad 2> ਰੱਖਿਆ_ਕਰਨੀ_ਕੀਮਤ','번호를 지정한 ਫਾਇਲ 서술자 ਦਾਖਲ_ਹੋਣਾ_ਬਾਹਰ_ਆਉਣਾ ਸਵਿੱਚ_ਮੋਡ'); assert ਫਾਇਲ('ਰੱਖਿਆ_ਕਰਨੀ_ਕੀਮਤ')==b'untouched\n'
            ਸ਼ੈਲ('rm 빈파일 리터럴 ਸਟੇਟਮੈਂਟ_ਕੀਮਤ 추림 앞 ਪਿਛਲਾ_ਕੀਮਤ ਰੱਖਿਆ_ਕਰਨੀ_ਕੀਮਤ')
            ਮਾਨਤਾ_ਵਿਵਰਨ['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            ਸ਼ੈਲ("python -c 'print(123)' | wc -c",'4\n')
            ਸ਼ੈਲ("python -c 'print(456)' > ਐਪਲੀਕੇਸ਼_f5044b9b.txt"); assert ਫਾਇਲ('ਐਪਲੀਕੇਸ਼_f5044b9b.txt')==b'456\n'
            ਸ਼ੈਲ("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            ਸ਼ੈਲ("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < ਐਪਲੀਕੇਸ਼_f5044b9b.txt", "b'456\\n'", "b''")
            ਸ਼ੈਲ("python -c 'print(\"x\"*17000)' | wc -c", 'ਗਲਤੀ -28')
            ਸ਼ੈਲ('echo recovered | wc -c','10\n')
            ਸ਼ੈਲ("python -c 'import jkoros; print(jkoros.read("+'"/작업/ਐਪਲੀਕੇਸ਼_f5044b9b.txt"'+"))'",'456','exit 0')
            ਸ਼ੈਲ('cd /; javac Hello.java','Compiled:','exit 0')
            ਸ਼ੈਲ('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in ਫਾਇਲ('/작업/자바.txt')
            ਸ਼ੈਲ('cd 작업; echo "echo script > 실행결과" > ਕਮਾਂਡ.sh; echo "false || echo recovered >> 실행결과" >> ਕਮਾਂਡ.sh; sh ਕਮਾਂਡ.sh')
            assert ਫਾਇਲ('실행결과')==b'script\nrecovered\n'
            ਸ਼ੈਲ('rm 실행결과; echo "exit 7" > ਨਿਕਾਸ_ਐਪਲੀਕੇਸ਼.sh; sh ਨਿਕਾਸ_ਐਪਲੀਕੇਸ਼.sh; echo $?','7\n')
            ਸ਼ੈਲ('rm ਨਿਕਾਸ_ਐਪਲੀਕੇਸ਼.sh ਕਮਾਂਡ.sh ਐਪਲੀਕੇਸ਼_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            ਮਾਨਤਾ_ਵਿਵਰਨ['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            ਸ਼ੈਲ('echo history-proof','history-proof')
            ਮਾਪ=ਈਮੇਲ(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert ਮਾਪ.count('history-proof')>=2, ਮਾਪ
            ਈਮੇਲ(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            ਮਾਪ=ਈਮੇਲ(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in ਮਾਪ, ਮਾਪ
            ਮਾਪ=ਈਮੇਲ(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in ਮਾਪ,ਮਾਪ
            ਮਾਪ=ਈਮੇਲ('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in ਮਾਪ,ਮਾਪ
            긴글='한글'*50
            ਮਾਪ=ਈਮੇਲ(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in ਮਾਪ
            ਸ਼ੈਲ('terminal','TERMINAL READY')
            ਸ਼ੈਲ('clear')
            ਸ਼ੈਲ('echo "한글 ਟਰਮੀਨਲ ABC xyz 012 😀"','한글 ਟਰਮੀਨਲ ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as ਗਾਹਕ:
                ਗਾਹਕ.settimeout(10); ਗਾਹਕ.connect(str(모의제어접속))
                with ਗਾਹਕ.makefile('rwb') as ਸਟ੍ਰੀਮ_ਕੀਮਤ:
                    json.loads(ਸਟ੍ਰੀਮ_ਕੀਮਤ.readline())
                    def 호출(ਨਾਂ,ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ=None):
                        ਨੈਟਵਰਕ_ਸੁਨੇਹਾ={'execute':ਨਾਂ}
                        if ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ: ਨੈਟਵਰਕ_ਸੁਨੇਹਾ['arguments']=ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ
                        ਸਟ੍ਰੀਮ_ਕੀਮਤ.write((json.dumps(ਨੈਟਵਰਕ_ਸੁਨੇਹਾ)+'\n').encode()); ਸਟ੍ਰੀਮ_ਕੀਮਤ.flush()
                        while True:
                            ਜਵਾਬ_ਦਿਓ=json.loads(ਸਟ੍ਰੀਮ_ਕੀਮਤ.readline())
                            if 'error' in ਜਵਾਬ_ਦਿਓ: raise AssertionError(ਜਵਾਬ_ਦਿਓ)
                            if 'return' in ਜਵਾਬ_ਦਿਓ: return ਜਵਾਬ_ਦਿਓ['return']
                    호출('qmp_capabilities')
                    ਤਸਵੀਰ=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(ਤਸਵੀਰ),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    ਸਮੱਗਰੀ=ਤਸਵੀਰ.read_bytes().split(b'\n',3)[3]
                    def ਬਿੰਦੂ(x_ਕੌਔਰਡੀਨੇਟ,세로좌표): return tuple(ਸਮੱਗਰੀ[(세로좌표*640+x_ਕੌਔਰਡੀਨੇਟ)*3:(세로좌표*640+x_ਕੌਔਰਡੀਨੇਟ)*3+3])
                    assert ਬਿੰਦੂ(12,48)==(32,80,144),ਬਿੰਦੂ(12,48)
                    assert len(set(ਬਿੰਦੂ(x_ਕੌਔਰਡੀਨੇਟ,세로좌표) for 세로좌표 in range(100,116) for x_ਕੌਔਰਡੀਨੇਟ in range(24,56)))>1,'Hangul glyphs missing'
                    ਸ਼ੈਲ('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    ਸ਼ੈਲ("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(ਤਸਵੀਰ),'format':'ppm'})
                    복원자료=ਤਸਵੀਰ.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    ਸ਼ੈਲ('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): ਸ਼ੈਲ('echo scroll-'+str(순번),'scroll-'+str(순번))
                    ਈਮੇਲ(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    ਮਾਪ=ਈਮੇਲ(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in ਮਾਪ,ਮਾਪ
                    ਸ਼ੈਲ('rm visible.txt')
                    호출('quit')
            ਪਰੋਸੈੱਸ.wait(timeout=5)
            ਮਾਨਤਾ_ਵਿਵਰਨ['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            ਮਾਨਤਾ_ਵਿਵਰਨ['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if ਪਰੋਸੈੱਸ.poll() is None:
                ਪਰੋਸੈੱਸ.terminate()
                try: ਪਰੋਸੈੱਸ.wait(timeout=5)
                except subprocess.TimeoutExpired: ਪਰੋਸੈੱਸ.kill(); ਪਰੋਸੈੱਸ.wait()
            준비살피미.close(); ਪਰੋਸੈੱਸ.stdin.close(); ਪਰੋਸੈੱਸ.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(ਮਾਨਤਾ_ਵਿਵਰਨ,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': ਚਲਾਓ_2()
