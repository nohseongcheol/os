#!/usr/bin/env python3
"""자체 커널의 бүрхүүл, 프로세스 оролт_гаралт, Unicode GUI 터미널을 бодит_өгөгдөл raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from Гүйцэтгэх_команд import 기준, Тушаал


def Ажиллуулах():
    출력결과 = 기준 / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    баталгаажуулалт_тайлан = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        үйл_явц = subprocess.Popen(Тушаал()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(үйл_явц.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            өгөгдөл=bytearray(); дуусгах_Оффсет=time.monotonic()+시간제한
            while 확인표시 not in өгөгдөл:
                if time.monotonic()>дуусгах_Оффсет or үйл_явц.poll() is not None: raise AssertionError('UART timeout/exit: '+өгөгдөл.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: өгөгдөл.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in өгөгдөл or b'FAIL ' in өгөгдөл: raise AssertionError(өгөгдөл)
            return өгөгдөл.decode('utf-8','replace').replace('\r\n','\n')
        def илгээх(өгөгдөл, 확인표시=b'jkoros-native> '):
            үйл_явц.stdin.write(өгөгдөл); үйл_явц.stdin.flush(); return 수신하기(확인표시)
        def бүрхүүл(Шугам, *예상결과):
            결과=илгээх(Шугам.encode()+b'\n')
            for утга in 예상결과: assert утга in 결과, (Шугам,утга,결과)
            return 결과
        def Файл(Нэр):
            Бичвэр=бүрхүүл('hex '+Нэр,'HEX BEGIN','HEX END'); 찾은결과=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',Бичвэр,re.S)
            өгөгдөл=bytes.fromhex(''.join(찾은결과.group(2).split())); assert len(өгөгдөл)==int(찾은결과.group(1)); return өгөгдөл
        try:
            수신하기(b'jkoros-native> ')
            бүрхүүл('mkdir 작업; cd 작업; pwd','/작업')
            бүрхүүл('mkdir 하위; echo "한글 өгөгдөл 😀" > 인사.txt')
            assert Файл('인사.txt')=='한글 өгөгдөл 😀\n'.encode()
            бүрхүүл('cp 인사.txt хуулах_утга.txt; mv хуулах_утга.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 өгөгдөл 😀')
            бүрхүүл('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 өгөгдөл 😀','/작업/하위')
            бүрхүүл('cd ..; rmdir 하위; echo $?','1\n')
            бүрхүүл('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            бүрхүүл('cp 인사.txt 인사.txt; echo $?','1\n'); assert Файл('인사.txt')=='한글 өгөгдөл 😀\n'.encode()
            бүрхүүл('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in Файл('인사.txt')
            бүрхүүл("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Файл('리터럴')=='$인사\n누리\n'.encode()
            бүрхүүл('echo one > тайлан_утга; echo two >> тайлан_утга; echo three >> тайлан_утга')
            бүрхүүл('cat < тайлан_утга | grep t | tee 추림 | wc -l','2\n'); assert Файл('추림')==b'two\nthree\n'
            бүрхүүл('head -n 1 тайлан_утга > 앞; tail -n 1 тайлан_утга > Буцах_утга'); assert Файл('앞')==b'one\n'; assert Файл('뒤')==b'three\n'
            бүрхүүл('grep absent тайлан_утга; echo $?','1\n')
            бүрхүүл('echo untouched > хамгаалах_утга')
            бүрхүүл('echo destroyed > хамгаалах_утга |','명령이 빠졌습니다'); assert Файл('хамгаалах_утга')==b'untouched\n'
            бүрхүүл('echo "oops','따옴표가 닫히지 않았습니다')
            бүрхүүл('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            бүрхүүл('echo bad 2> хамгаалах_утга','번호를 지정한 Файл 서술자 оролт_гаралт шилжих_горим'); assert Файл('хамгаалах_утга')==b'untouched\n'
            бүрхүүл('rm 빈파일 리터럴 тайлан_утга 추림 앞 Буцах_утга хамгаалах_утга')
            баталгаажуулалт_тайлан['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            бүрхүүл("python -c 'print(123)' | wc -c",'4\n')
            бүрхүүл("python -c 'print(456)' > програм_f5044b9b.txt"); assert Файл('програм_f5044b9b.txt')==b'456\n'
            бүрхүүл("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            бүрхүүл("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < програм_f5044b9b.txt", "b'456\\n'", "b''")
            бүрхүүл("python -c 'print(\"x\"*17000)' | wc -c", 'Алдаа -28')
            бүрхүүл('echo recovered | wc -c','10\n')
            бүрхүүл("python -c 'import jkoros; print(jkoros.read("+'"/작업/програм_f5044b9b.txt"'+"))'",'456','exit 0')
            бүрхүүл('cd /; javac Hello.java','Compiled:','exit 0')
            бүрхүүл('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in Файл('/작업/자바.txt')
            бүрхүүл('cd 작업; echo "echo script > 실행결과" > Тушаал.sh; echo "false || echo recovered >> 실행결과" >> Тушаал.sh; sh Тушаал.sh')
            assert Файл('실행결과')==b'script\nrecovered\n'
            бүрхүүл('rm 실행결과; echo "exit 7" > Гарах_програм.sh; sh Гарах_програм.sh; echo $?','7\n')
            бүрхүүл('rm Гарах_програм.sh Тушаал.sh програм_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            баталгаажуулалт_тайлан['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            бүрхүүл('echo history-proof','history-proof')
            결과=илгээх(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert 결과.count('history-proof')>=2, 결과
            илгээх(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            결과=илгээх(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in 결과, 결과
            결과=илгээх(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in 결과,결과
            결과=илгээх('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in 결과,결과
            긴글='한글'*50
            결과=илгээх(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in 결과
            бүрхүүл('terminal','TERMINAL READY')
            бүрхүүл('clear')
            бүрхүүл('echo "한글 Терминал ABC xyz 012 😀"','한글 Терминал ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as клиент:
                клиент.settimeout(10); клиент.connect(str(모의제어접속))
                with клиент.makefile('rwb') as урсгал_утга:
                    json.loads(урсгал_утга.readline())
                    def 호출(Нэр,аргумент_олонлог=None):
                        Сүлжээ_мэдээлэл={'execute':Нэр}
                        if аргумент_олонлог: Сүлжээ_мэдээлэл['arguments']=аргумент_олонлог
                        урсгал_утга.write((json.dumps(Сүлжээ_мэдээлэл)+'\n').encode()); урсгал_утга.flush()
                        while True:
                            хариулах=json.loads(урсгал_утга.readline())
                            if 'error' in хариулах: raise AssertionError(хариулах)
                            if 'return' in хариулах: return хариулах['return']
                    호출('qmp_capabilities')
                    зураг=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(зураг),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    өгөгдөл=зураг.read_bytes().split(b'\n',3)[3]
                    def нягтрал(х_координат,세로좌표): return tuple(өгөгдөл[(세로좌표*640+х_координат)*3:(세로좌표*640+х_координат)*3+3])
                    assert нягтрал(12,48)==(32,80,144),нягтрал(12,48)
                    assert len(set(нягтрал(х_координат,세로좌표) for 세로좌표 in range(100,116) for х_координат in range(24,56)))>1,'Hangul glyphs missing'
                    бүрхүүл('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    бүрхүүл("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(зураг),'format':'ppm'})
                    복원자료=зураг.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    бүрхүүл('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): бүрхүүл('echo scroll-'+str(순번),'scroll-'+str(순번))
                    илгээх(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    결과=илгээх(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in 결과,결과
                    бүрхүүл('rm visible.txt')
                    호출('quit')
            үйл_явц.wait(timeout=5)
            баталгаажуулалт_тайлан['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            баталгаажуулалт_тайлан['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if үйл_явц.poll() is None:
                үйл_явц.terminate()
                try: үйл_явц.wait(timeout=5)
                except subprocess.TimeoutExpired: үйл_явц.kill(); үйл_явц.wait()
            준비살피미.close(); үйл_явц.stdin.close(); үйл_явц.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(баталгаажуулалт_тайлан,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': Ажиллуулах()
