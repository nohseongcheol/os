#!/usr/bin/env python3
"""자체 커널의 ഷെല്, 프로세스 ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്, Unicode GUI 터미널을 വാസ്തവമായ_ഡാറ്റാ raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from നടപ്പാക്കുക_കമാന്_ഡ് import പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം, ആജ്ഞ


def നടപ്പിലാക്കുക():
    출력결과 = പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    నిర్ధారణ_నివేదిక = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        പ്രക്രിയ = subprocess.Popen(ആജ്ഞ()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(പ്രക്രിയ.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            ഡാറ്റാ=bytearray(); അവസാനിപ്പിക്കുക_ഓഫ്_സെറ്റ്=time.monotonic()+시간제한
            while 확인표시 not in ഡാറ്റാ:
                if time.monotonic()>അവസാനിപ്പിക്കുക_ഓഫ്_സെറ്റ് or പ്രക്രിയ.poll() is not None: raise AssertionError('UART timeout/exit: '+ഡാറ്റാ.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: ഡാറ്റാ.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in ഡാറ്റാ or b'FAIL ' in ഡാറ്റാ: raise AssertionError(ഡാറ്റാ)
            return ഡാറ്റാ.decode('utf-8','replace').replace('\r\n','\n')
        def അയയ്ക്കുക(ഡാറ്റാ, 확인표시=b'jkoros-native> '):
            പ്രക്രിയ.stdin.write(ഡാറ്റാ); പ്രക്രിയ.stdin.flush(); return 수신하기(확인표시)
        def ഷെല്(ലൈൻ, *예상결과):
            അളവ്=അയയ്ക്കുക(ലൈൻ.encode()+b'\n')
            for മൂല്യം in 예상결과: assert മൂല്യം in അളവ്, (ലൈൻ,മൂല്യം,അളവ്)
            return അളവ്
        def ഫയല്(പേരു്):
            പദാവലി=ഷെല്('hex '+പേരു്,'HEX BEGIN','HEX END'); തിരയൽ_അളവ്=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',പദാവലി,re.S)
            ഡാറ്റാ=bytes.fromhex(''.join(തിരയൽ_അളവ്.group(2).split())); assert len(ഡാറ്റാ)==int(തിരയൽ_അളവ്.group(1)); return ഡാറ്റാ
        try:
            수신하기(b'jkoros-native> ')
            ഷെല്('mkdir 작업; cd 작업; pwd','/작업')
            ഷെല്('mkdir 하위; echo "한글 ഡാറ്റാ 😀" > 인사.txt')
            assert ഫയല്('인사.txt')=='한글 ഡാറ്റാ 😀\n'.encode()
            ഷെല്('cp 인사.txt ദൃഷ്ടാന്തം_മൂല്യം.txt; mv ദൃഷ്ടാന്തം_മൂല്യം.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 ഡാറ്റാ 😀')
            ഷെല്('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 ഡാറ്റാ 😀','/작업/하위')
            ഷെല്('cd ..; rmdir 하위; echo $?','1\n')
            ഷെല്('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            ഷെല്('cp 인사.txt 인사.txt; echo $?','1\n'); assert ഫയല്('인사.txt')=='한글 ഡാറ്റാ 😀\n'.encode()
            ഷെല്('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in ഫയല്('인사.txt')
            ഷെല്("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert ഫയല്('리터럴')=='$인사\n누리\n'.encode()
            ഷെല്('echo one > പ്രസ്താവന_മൂല്യം; echo two >> പ്രസ്താവന_മൂല്യം; echo three >> പ്രസ്താവന_മൂല്യം')
            ഷെല്('cat < പ്രസ്താവന_മൂല്യം | grep t | tee 추림 | wc -l','2\n'); assert ഫയല്('추림')==b'two\nthree\n'
            ഷെല്('head -n 1 പ്രസ്താവന_മൂല്യം > മുൻവശം_മൂല്യം; tail -n 1 പ്രസ്താവന_മൂല്യം > പിന്നിലേക്ക്_മൂല്യം'); assert ഫയല്('앞')==b'one\n'; assert ഫയല്('뒤')==b'three\n'
            ഷെല്('grep absent പ്രസ്താവന_മൂല്യം; echo $?','1\n')
            ഷെല്('echo untouched > പരിരക്ഷിക്കുക_മൂല്യം')
            ഷെല്('echo destroyed > പരിരക്ഷിക്കുക_മൂല്യം |','명령이 빠졌습니다'); assert ഫയല്('പരിരക്ഷിക്കുക_മൂല്യം')==b'untouched\n'
            ഷെല്('echo "oops','따옴표가 닫히지 않았습니다')
            ഷെല്('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            ഷെല്('echo bad 2> പരിരക്ഷിക്കുക_മൂല്യം','번호를 지정한 ഫയല് 서술자 ഇന്_പുട്ട്_ഔട്ട്_പുട്ട് സ്വിച്ച്_മോഡ്'); assert ഫയല്('പരിരക്ഷിക്കുക_മൂല്യം')==b'untouched\n'
            ഷെല്('rm 빈파일 리터럴 പ്രസ്താവന_മൂല്യം 추림 മുൻവശം_മൂല്യം പിന്നിലേക്ക്_മൂല്യം പരിരക്ഷിക്കുക_മൂല്യം')
            నిర్ధారణ_నివేదిక['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            ഷെല്("python -c 'print(123)' | wc -c",'4\n')
            ഷെല്("python -c 'print(456)' > പ്രോഗ്രാം_f5044b9b.txt"); assert ഫയല്('പ്രോഗ്രാം_f5044b9b.txt')==b'456\n'
            ഷെല്("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            ഷെല്("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < പ്രോഗ്രാം_f5044b9b.txt", "b'456\\n'", "b''")
            ഷെല്("python -c 'print(\"x\"*17000)' | wc -c", 'പിശക് -28')
            ഷെല്('echo recovered | wc -c','10\n')
            ഷെല്("python -c 'import jkoros; print(jkoros.read("+'"/작업/പ്രോഗ്രാം_f5044b9b.txt"'+"))'",'456','exit 0')
            ഷെല്('cd /; javac Hello.java','Compiled:','exit 0')
            ഷെല്('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in ഫയല്('/작업/자바.txt')
            ഷെല്('cd 작업; echo "echo script > 실행결과" > ആജ്ഞ.sh; echo "false || echo recovered >> 실행결과" >> ആജ്ഞ.sh; sh ആജ്ഞ.sh')
            assert ഫയല്('실행결과')==b'script\nrecovered\n'
            ഷെല്('rm 실행결과; echo "exit 7" > പുറത്തുകടക്കൽ_പ്രോഗ്രാം.sh; sh പുറത്തുകടക്കൽ_പ്രോഗ്രാം.sh; echo $?','7\n')
            ഷെല്('rm പുറത്തുകടക്കൽ_പ്രോഗ്രാം.sh ആജ്ഞ.sh പ്രോഗ്രാം_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            నిర్ధారణ_నివేదిక['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            ഷെല്('echo history-proof','history-proof')
            അളവ്=അയയ്ക്കുക(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert അളവ്.count('history-proof')>=2, അളവ്
            അയയ്ക്കുക(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            അളവ്=അയയ്ക്കുക(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in അളവ്, അളവ്
            അളവ്=അയയ്ക്കുക(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in അളവ്,അളവ്
            അളവ്=അയയ്ക്കുക('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in അളവ്,അളവ്
            긴글='한글'*50
            അളവ്=അയയ്ക്കുക(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in അളവ്
            ഷെല്('terminal','TERMINAL READY')
            ഷെല്('clear')
            ഷെല്('echo "한글 ടെ_ര്മിനല് ABC xyz 012 😀"','한글 ടെ_ര്മിനല് ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as ക്ലയന്_റ്:
                ക്ലയന്_റ്.settimeout(10); ക്ലയന്_റ്.connect(str(모의제어접속))
                with ക്ലയന്_റ്.makefile('rwb') as സ്ട്രീം_മൂല്യം:
                    json.loads(സ്ട്രീം_മൂല്യം.readline())
                    def 호출(പേരു്,ആര്_ഗ്യുമെന്_റ്_അരേ=None):
                        നെറ്റ്_വർക്ക്_ഇമെയിൽ={'execute':പേരു്}
                        if ആര്_ഗ്യുമെന്_റ്_അരേ: നെറ്റ്_വർക്ക്_ഇമെയിൽ['arguments']=ആര്_ഗ്യുമെന്_റ്_അരേ
                        സ്ട്രീം_മൂല്യം.write((json.dumps(നെറ്റ്_വർക്ക്_ഇമെയിൽ)+'\n').encode()); സ്ട്രീം_മൂല്യം.flush()
                        while True:
                            മറുപടി_നൽകുക=json.loads(സ്ട്രീം_മൂല്യം.readline())
                            if 'error' in മറുപടി_നൽകുക: raise AssertionError(മറുപടി_നൽകുക)
                            if 'return' in മറുപടി_നൽകുക: return മറുപടി_നൽകുക['return']
                    호출('qmp_capabilities')
                    ഇമേജ്=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(ഇമേജ്),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    ഡാറ്റാ=ഇമേജ്.read_bytes().split(b'\n',3)[3]
                    def പെല്(x_ഏകോപനം,Y_ബട്ടൺ_ഏകോപനം): return tuple(ഡാറ്റാ[(Y_ബട്ടൺ_ഏകോപനം*640+x_ഏകോപനം)*3:(Y_ബട്ടൺ_ഏകോപനം*640+x_ഏകോപനം)*3+3])
                    assert പെല്(12,48)==(32,80,144),പെല്(12,48)
                    assert len(set(പെല്(x_ഏകോപനം,Y_ബട്ടൺ_ഏകോപനം) for Y_ബട്ടൺ_ഏകോപനം in range(100,116) for x_ഏകോപനം in range(24,56)))>1,'Hangul glyphs missing'
                    ഷെല്('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    ഷെല്("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(ഇമേജ്),'format':'ppm'})
                    복원자료=ഇമേജ്.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    ഷെല്('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): ഷെല്('echo scroll-'+str(순번),'scroll-'+str(순번))
                    അയയ്ക്കുക(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    അളവ്=അയയ്ക്കുക(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in അളവ്,അളവ്
                    ഷെല്('rm visible.txt')
                    호출('quit')
            പ്രക്രിയ.wait(timeout=5)
            నిర్ధారణ_నివేదిక['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            నిర్ధారణ_నివేదిక['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if പ്രക്രിയ.poll() is None:
                പ്രക്രിയ.terminate()
                try: പ്രക്രിയ.wait(timeout=5)
                except subprocess.TimeoutExpired: പ്രക്രിയ.kill(); പ്രക്രിയ.wait()
            준비살피미.close(); പ്രക്രിയ.stdin.close(); പ്രക്രിയ.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(నిర్ధారణ_నివేదిక,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': നടപ്പിലാക്കുക()
