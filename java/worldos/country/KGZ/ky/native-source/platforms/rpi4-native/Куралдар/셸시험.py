#!/usr/bin/env python3
"""자체 커널의 сырты, 프로세스 киргизүү_чыгаруу, Unicode GUI 터미널을 актуалдуу_берилмелер raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from аткаруу_буйрук import 기준, Команда


def Жүргүзүү():
    출력결과 = 기준 / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    ырастоо_отчет = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Процесси = subprocess.Popen(Команда()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Процесси.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            берилмелер=bytearray(); аяктоо_Жылбышуу=time.monotonic()+시간제한
            while 확인표시 not in берилмелер:
                if time.monotonic()>аяктоо_Жылбышуу or Процесси.poll() is not None: raise AssertionError('UART timeout/exit: '+берилмелер.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: берилмелер.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in берилмелер or b'FAIL ' in берилмелер: raise AssertionError(берилмелер)
            return берилмелер.decode('utf-8','replace').replace('\r\n','\n')
        def жөнөтүү(берилмелер, 확인표시=b'jkoros-native> '):
            Процесси.stdin.write(берилмелер); Процесси.stdin.flush(); return 수신하기(확인표시)
        def сырты(сап, *예상결과):
            결과=жөнөтүү(сап.encode()+b'\n')
            for маани in 예상결과: assert маани in 결과, (сап,маани,결과)
            return 결과
        def Файл(Аты):
            Текст=сырты('hex '+Аты,'HEX BEGIN','HEX END'); 찾은결과=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',Текст,re.S)
            берилмелер=bytes.fromhex(''.join(찾은결과.group(2).split())); assert len(берилмелер)==int(찾은결과.group(1)); return берилмелер
        try:
            수신하기(b'jkoros-native> ')
            сырты('mkdir 작업; cd 작업; pwd','/작업')
            сырты('mkdir 하위; echo "한글 берилмелер 😀" > 인사.txt')
            assert Файл('인사.txt')=='한글 берилмелер 😀\n'.encode()
            сырты('cp 인사.txt даана_маани.txt; mv даана_маани.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 берилмелер 😀')
            сырты('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 берилмелер 😀','/작업/하위')
            сырты('cd ..; rmdir 하위; echo $?','1\n')
            сырты('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            сырты('cp 인사.txt 인사.txt; echo $?','1\n'); assert Файл('인사.txt')=='한글 берилмелер 😀\n'.encode()
            сырты('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in Файл('인사.txt')
            сырты("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Файл('리터럴')=='$인사\n누리\n'.encode()
            сырты('echo one > отчет_маани; echo two >> отчет_маани; echo three >> отчет_маани')
            сырты('cat < отчет_маани | grep t | tee 추림 | wc -l','2\n'); assert Файл('추림')==b'two\nthree\n'
            сырты('head -n 1 отчет_маани > 앞; tail -n 1 отчет_маани > Артка_маани'); assert Файл('앞')==b'one\n'; assert Файл('뒤')==b'three\n'
            сырты('grep absent отчет_маани; echo $?','1\n')
            сырты('echo untouched > коргоо_маани')
            сырты('echo destroyed > коргоо_маани |','명령이 빠졌습니다'); assert Файл('коргоо_маани')==b'untouched\n'
            сырты('echo "oops','따옴표가 닫히지 않았습니다')
            сырты('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            сырты('echo bad 2> коргоо_маани','번호를 지정한 Файл 서술자 киргизүү_чыгаруу котормо_режим'); assert Файл('коргоо_маани')==b'untouched\n'
            сырты('rm 빈파일 리터럴 отчет_маани 추림 앞 Артка_маани коргоо_маани')
            ырастоо_отчет['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            сырты("python -c 'print(123)' | wc -c",'4\n')
            сырты("python -c 'print(456)' > програм_f5044b9b.txt"); assert Файл('програм_f5044b9b.txt')==b'456\n'
            сырты("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            сырты("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < програм_f5044b9b.txt", "b'456\\n'", "b''")
            сырты("python -c 'print(\"x\"*17000)' | wc -c", 'Ката -28')
            сырты('echo recovered | wc -c','10\n')
            сырты("python -c 'import jkoros; print(jkoros.read("+'"/작업/програм_f5044b9b.txt"'+"))'",'456','exit 0')
            сырты('cd /; javac Hello.java','Compiled:','exit 0')
            сырты('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in Файл('/작업/자바.txt')
            сырты('cd 작업; echo "echo script > 실행결과" > Команда.sh; echo "false || echo recovered >> 실행결과" >> Команда.sh; sh Команда.sh')
            assert Файл('실행결과')==b'script\nrecovered\n'
            сырты('rm 실행결과; echo "exit 7" > Чыгуу_програм.sh; sh Чыгуу_програм.sh; echo $?','7\n')
            сырты('rm Чыгуу_програм.sh Команда.sh програм_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            ырастоо_отчет['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            сырты('echo history-proof','history-proof')
            결과=жөнөтүү(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert 결과.count('history-proof')>=2, 결과
            жөнөтүү(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            결과=жөнөтүү(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in 결과, 결과
            결과=жөнөтүү(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in 결과,결과
            결과=жөнөтүү('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in 결과,결과
            긴글='한글'*50
            결과=жөнөтүү(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in 결과
            сырты('terminal','TERMINAL READY')
            сырты('clear')
            сырты('echo "한글 Терминал ABC xyz 012 😀"','한글 Терминал ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as керектөөчү:
                керектөөчү.settimeout(10); керектөөчү.connect(str(모의제어접속))
                with керектөөчү.makefile('rwb') as агым_маани:
                    json.loads(агым_маани.readline())
                    def 호출(Аты,аргумент_МАССИВ=None):
                        Желе_билдирүү={'execute':Аты}
                        if аргумент_МАССИВ: Желе_билдирүү['arguments']=аргумент_МАССИВ
                        агым_маани.write((json.dumps(Желе_билдирүү)+'\n').encode()); агым_маани.flush()
                        while True:
                            жооп_берүү=json.loads(агым_маани.readline())
                            if 'error' in жооп_берүү: raise AssertionError(жооп_берүү)
                            if 'return' in жооп_берүү: return жооп_берүү['return']
                    호출('qmp_capabilities')
                    сүрөт=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(сүрөт),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    берилмелер=сүрөт.read_bytes().split(b'\n',3)[3]
                    def пиксел(x_координата,세로좌표): return tuple(берилмелер[(세로좌표*640+x_координата)*3:(세로좌표*640+x_координата)*3+3])
                    assert пиксел(12,48)==(32,80,144),пиксел(12,48)
                    assert len(set(пиксел(x_координата,세로좌표) for 세로좌표 in range(100,116) for x_координата in range(24,56)))>1,'Hangul glyphs missing'
                    сырты('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    сырты("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(сүрөт),'format':'ppm'})
                    복원자료=сүрөт.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    сырты('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): сырты('echo scroll-'+str(순번),'scroll-'+str(순번))
                    жөнөтүү(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    결과=жөнөтүү(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in 결과,결과
                    сырты('rm visible.txt')
                    호출('quit')
            Процесси.wait(timeout=5)
            ырастоо_отчет['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            ырастоо_отчет['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Процесси.poll() is None:
                Процесси.terminate()
                try: Процесси.wait(timeout=5)
                except subprocess.TimeoutExpired: Процесси.kill(); Процесси.wait()
            준비살피미.close(); Процесси.stdin.close(); Процесси.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(ырастоо_отчет,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': Жүргүзүү()
