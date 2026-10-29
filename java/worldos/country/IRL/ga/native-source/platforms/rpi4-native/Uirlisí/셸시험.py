#!/usr/bin/env python3
"""자체 커널의 blaosc, 프로세스 I_O, Unicode GUI 터미널을 iarbhír_sonraí raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from Rith_ordú import teilgean_fréamh, Ordú


def Rith_2():
    출력결과 = teilgean_fréamh / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    bailíochtú_tuairisc = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((teilgean_fréamh / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Próiseas = subprocess.Popen(Ordú()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Próiseas.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            sonraí=bytearray(); cuir_deireadh_le_OFFSET=time.monotonic()+시간제한
            while 확인표시 not in sonraí:
                if time.monotonic()>cuir_deireadh_le_OFFSET or Próiseas.poll() is not None: raise AssertionError('UART timeout/exit: '+sonraí.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: sonraí.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in sonraí or b'FAIL ' in sonraí: raise AssertionError(sonraí)
            return sonraí.decode('utf-8','replace').replace('\r\n','\n')
        def seol(sonraí, 확인표시=b'jkoros-native> '):
            Próiseas.stdin.write(sonraí); Próiseas.stdin.flush(); return 수신하기(확인표시)
        def blaosc(Líne, *예상결과):
            tomhas=seol(Líne.encode()+b'\n')
            for VALUE in 예상결과: assert VALUE in tomhas, (Líne,VALUE,tomhas)
            return tomhas
        def Comhad(Ainm):
            Téacs=blaosc('hex '+Ainm,'HEX BEGIN','HEX END'); SEARCH_tomhas=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',Téacs,re.S)
            sonraí=bytes.fromhex(''.join(SEARCH_tomhas.group(2).split())); assert len(sonraí)==int(SEARCH_tomhas.group(1)); return sonraí
        try:
            수신하기(b'jkoros-native> ')
            blaosc('mkdir 작업; cd 작업; pwd','/작업')
            blaosc('mkdir 하위; echo "한글 sonraí 😀" > 인사.txt')
            assert Comhad('인사.txt')=='한글 sonraí 😀\n'.encode()
            blaosc('cp 인사.txt ásc_VALUE.txt; mv ásc_VALUE.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 sonraí 😀')
            blaosc('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 sonraí 😀','/작업/하위')
            blaosc('cd ..; rmdir 하위; echo $?','1\n')
            blaosc('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            blaosc('cp 인사.txt 인사.txt; echo $?','1\n'); assert Comhad('인사.txt')=='한글 sonraí 😀\n'.encode()
            blaosc('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in Comhad('인사.txt')
            blaosc("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Comhad('리터럴')=='$인사\n누리\n'.encode()
            blaosc('echo one > ráiteas_VALUE; echo two >> ráiteas_VALUE; echo three >> ráiteas_VALUE')
            blaosc('cat < ráiteas_VALUE | grep t | tee 추림 | wc -l','2\n'); assert Comhad('추림')==b'two\nthree\n'
            blaosc('head -n 1 ráiteas_VALUE > 앞; tail -n 1 ráiteas_VALUE > Siar_VALUE'); assert Comhad('앞')==b'one\n'; assert Comhad('뒤')==b'three\n'
            blaosc('grep absent ráiteas_VALUE; echo $?','1\n')
            blaosc('echo untouched > cosain_VALUE')
            blaosc('echo destroyed > cosain_VALUE |','명령이 빠졌습니다'); assert Comhad('cosain_VALUE')==b'untouched\n'
            blaosc('echo "oops','따옴표가 닫히지 않았습니다')
            blaosc('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            blaosc('echo bad 2> cosain_VALUE','번호를 지정한 Comhad 서술자 I_O SWITCH_mód'); assert Comhad('cosain_VALUE')==b'untouched\n'
            blaosc('rm 빈파일 리터럴 ráiteas_VALUE 추림 앞 Siar_VALUE cosain_VALUE')
            bailíochtú_tuairisc['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            blaosc("python -c 'print(123)' | wc -c",'4\n')
            blaosc("python -c 'print(456)' > clár_f5044b9b.txt"); assert Comhad('clár_f5044b9b.txt')==b'456\n'
            blaosc("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            blaosc("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < clár_f5044b9b.txt", "b'456\\n'", "b''")
            blaosc("python -c 'print(\"x\"*17000)' | wc -c", 'ERREÁID -28')
            blaosc('echo recovered | wc -c','10\n')
            blaosc("python -c 'import jkoros; print(jkoros.read("+'"/작업/clár_f5044b9b.txt"'+"))'",'456','exit 0')
            blaosc('cd /; javac Hello.java','Compiled:','exit 0')
            blaosc('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in Comhad('/작업/자바.txt')
            blaosc('cd 작업; echo "echo script > 실행결과" > Ordú.sh; echo "false || echo recovered >> 실행결과" >> Ordú.sh; sh Ordú.sh')
            assert Comhad('실행결과')==b'script\nrecovered\n'
            blaosc('rm 실행결과; echo "exit 7" > scoir_clár.sh; sh scoir_clár.sh; echo $?','7\n')
            blaosc('rm scoir_clár.sh Ordú.sh clár_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            bailíochtú_tuairisc['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            blaosc('echo history-proof','history-proof')
            tomhas=seol(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert tomhas.count('history-proof')>=2, tomhas
            seol(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            tomhas=seol(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in tomhas, tomhas
            tomhas=seol(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in tomhas,tomhas
            tomhas=seol('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in tomhas,tomhas
            긴글='한글'*50
            tomhas=seol(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in tomhas
            blaosc('terminal','TERMINAL READY')
            blaosc('clear')
            blaosc('echo "한글 Teirminéal ABC xyz 012 😀"','한글 Teirminéal ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as cliant:
                cliant.settimeout(10); cliant.connect(str(모의제어접속))
                with cliant.makefile('rwb') as sruth_VALUE:
                    json.loads(sruth_VALUE.readline())
                    def 호출(Ainm,argóint_ARRAY=None):
                        Líonra_teachtaireacht={'execute':Ainm}
                        if argóint_ARRAY: Líonra_teachtaireacht['arguments']=argóint_ARRAY
                        sruth_VALUE.write((json.dumps(Líonra_teachtaireacht)+'\n').encode()); sruth_VALUE.flush()
                        while True:
                            freagair=json.loads(sruth_VALUE.readline())
                            if 'error' in freagair: raise AssertionError(freagair)
                            if 'return' in freagair: return freagair['return']
                    호출('qmp_capabilities')
                    IMAGE=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(IMAGE),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    sonraí=IMAGE.read_bytes().split(b'\n',3)[3]
                    def picteilín(x_chomhordanáid,세로좌표): return tuple(sonraí[(세로좌표*640+x_chomhordanáid)*3:(세로좌표*640+x_chomhordanáid)*3+3])
                    assert picteilín(12,48)==(32,80,144),picteilín(12,48)
                    assert len(set(picteilín(x_chomhordanáid,세로좌표) for 세로좌표 in range(100,116) for x_chomhordanáid in range(24,56)))>1,'Hangul glyphs missing'
                    blaosc('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    blaosc("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(IMAGE),'format':'ppm'})
                    복원자료=IMAGE.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    blaosc('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): blaosc('echo scroll-'+str(순번),'scroll-'+str(순번))
                    seol(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    tomhas=seol(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in tomhas,tomhas
                    blaosc('rm visible.txt')
                    호출('quit')
            Próiseas.wait(timeout=5)
            bailíochtú_tuairisc['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            bailíochtú_tuairisc['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Próiseas.poll() is None:
                Próiseas.terminate()
                try: Próiseas.wait(timeout=5)
                except subprocess.TimeoutExpired: Próiseas.kill(); Próiseas.wait()
            준비살피미.close(); Próiseas.stdin.close(); Próiseas.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(bailíochtú_tuairisc,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': Rith_2()
