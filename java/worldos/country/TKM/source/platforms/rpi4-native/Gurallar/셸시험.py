#!/usr/bin/env python3
"""자체 커널의 gabyjak, 프로세스 I_O, Unicode GUI 터미널을 hakyky_maglumat raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from ýerine_ýetir_buýruk import 기준, buýruk


def Bitir():
    출력결과 = 기준 / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    barlag_hasabat = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Proses = subprocess.Popen(buýruk()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Proses.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            maglumat=bytearray(); tamamla_Süýşüriş=time.monotonic()+시간제한
            while 확인표시 not in maglumat:
                if time.monotonic()>tamamla_Süýşüriş or Proses.poll() is not None: raise AssertionError('UART timeout/exit: '+maglumat.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: maglumat.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in maglumat or b'FAIL ' in maglumat: raise AssertionError(maglumat)
            return maglumat.decode('utf-8','replace').replace('\r\n','\n')
        def iber(maglumat, 확인표시=b'jkoros-native> '):
            Proses.stdin.write(maglumat); Proses.stdin.flush(); return 수신하기(확인표시)
        def gabyjak(setir, *예상결과):
            결과=iber(setir.encode()+b'\n')
            for baha in 예상결과: assert baha in 결과, (setir,baha,결과)
            return 결과
        def Faýl(Ad):
            Metin=gabyjak('hex '+Ad,'HEX BEGIN','HEX END'); 찾은결과=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',Metin,re.S)
            maglumat=bytes.fromhex(''.join(찾은결과.group(2).split())); assert len(maglumat)==int(찾은결과.group(1)); return maglumat
        try:
            수신하기(b'jkoros-native> ')
            gabyjak('mkdir 작업; cd 작업; pwd','/작업')
            gabyjak('mkdir 하위; echo "한글 maglumat 😀" > 인사.txt')
            assert Faýl('인사.txt')=='한글 maglumat 😀\n'.encode()
            gabyjak('cp 인사.txt synp_baha.txt; mv synp_baha.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 maglumat 😀')
            gabyjak('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 maglumat 😀','/작업/하위')
            gabyjak('cd ..; rmdir 하위; echo $?','1\n')
            gabyjak('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            gabyjak('cp 인사.txt 인사.txt; echo $?','1\n'); assert Faýl('인사.txt')=='한글 maglumat 😀\n'.encode()
            gabyjak('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in Faýl('인사.txt')
            gabyjak("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Faýl('리터럴')=='$인사\n누리\n'.encode()
            gabyjak('echo one > beýannama_baha; echo two >> beýannama_baha; echo three >> beýannama_baha')
            gabyjak('cat < beýannama_baha | grep t | tee 추림 | wc -l','2\n'); assert Faýl('추림')==b'two\nthree\n'
            gabyjak('head -n 1 beýannama_baha > 앞; tail -n 1 beýannama_baha > Yza_baha'); assert Faýl('앞')==b'one\n'; assert Faýl('뒤')==b'three\n'
            gabyjak('grep absent beýannama_baha; echo $?','1\n')
            gabyjak('echo untouched > gora_baha')
            gabyjak('echo destroyed > gora_baha |','명령이 빠졌습니다'); assert Faýl('gora_baha')==b'untouched\n'
            gabyjak('echo "oops','따옴표가 닫히지 않았습니다')
            gabyjak('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            gabyjak('echo bad 2> gora_baha','번호를 지정한 Faýl 서술자 I_O calşyr_reje'); assert Faýl('gora_baha')==b'untouched\n'
            gabyjak('rm 빈파일 리터럴 beýannama_baha 추림 앞 Yza_baha gora_baha')
            barlag_hasabat['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            gabyjak("python -c 'print(123)' | wc -c",'4\n')
            gabyjak("python -c 'print(456)' > programma_f5044b9b.txt"); assert Faýl('programma_f5044b9b.txt')==b'456\n'
            gabyjak("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            gabyjak("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < programma_f5044b9b.txt", "b'456\\n'", "b''")
            gabyjak("python -c 'print(\"x\"*17000)' | wc -c", 'Hata -28')
            gabyjak('echo recovered | wc -c','10\n')
            gabyjak("python -c 'import jkoros; print(jkoros.read("+'"/작업/programma_f5044b9b.txt"'+"))'",'456','exit 0')
            gabyjak('cd /; javac Hello.java','Compiled:','exit 0')
            gabyjak('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in Faýl('/작업/자바.txt')
            gabyjak('cd 작업; echo "echo script > 실행결과" > buýruk.sh; echo "false || echo recovered >> 실행결과" >> buýruk.sh; sh buýruk.sh')
            assert Faýl('실행결과')==b'script\nrecovered\n'
            gabyjak('rm 실행결과; echo "exit 7" > çyk_programma.sh; sh çyk_programma.sh; echo $?','7\n')
            gabyjak('rm çyk_programma.sh buýruk.sh programma_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            barlag_hasabat['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            gabyjak('echo history-proof','history-proof')
            결과=iber(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert 결과.count('history-proof')>=2, 결과
            iber(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            결과=iber(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in 결과, 결과
            결과=iber(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in 결과,결과
            결과=iber('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in 결과,결과
            긴글='한글'*50
            결과=iber(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in 결과
            gabyjak('terminal','TERMINAL READY')
            gabyjak('clear')
            gabyjak('echo "한글 터미널 ABC xyz 012 😀"','한글 터미널 ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as müşderi:
                müşderi.settimeout(10); müşderi.connect(str(모의제어접속))
                with müşderi.makefile('rwb') as Stream_baha:
                    json.loads(Stream_baha.readline())
                    def 호출(Ad,argument_ARRAY=None):
                        Tor_habar={'execute':Ad}
                        if argument_ARRAY: Tor_habar['arguments']=argument_ARRAY
                        Stream_baha.write((json.dumps(Tor_habar)+'\n').encode()); Stream_baha.flush()
                        while True:
                            jogap_bermek=json.loads(Stream_baha.readline())
                            if 'error' in jogap_bermek: raise AssertionError(jogap_bermek)
                            if 'return' in jogap_bermek: return jogap_bermek['return']
                    호출('qmp_capabilities')
                    surat=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(surat),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    maglumat=surat.read_bytes().split(b'\n',3)[3]
                    def pel(x_koordinatasy,세로좌표): return tuple(maglumat[(세로좌표*640+x_koordinatasy)*3:(세로좌표*640+x_koordinatasy)*3+3])
                    assert pel(12,48)==(32,80,144),pel(12,48)
                    assert len(set(pel(x_koordinatasy,세로좌표) for 세로좌표 in range(100,116) for x_koordinatasy in range(24,56)))>1,'Hangul glyphs missing'
                    gabyjak('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    gabyjak("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(surat),'format':'ppm'})
                    복원자료=surat.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    gabyjak('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): gabyjak('echo scroll-'+str(순번),'scroll-'+str(순번))
                    iber(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    결과=iber(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in 결과,결과
                    gabyjak('rm visible.txt')
                    호출('quit')
            Proses.wait(timeout=5)
            barlag_hasabat['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            barlag_hasabat['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Proses.poll() is None:
                Proses.terminate()
                try: Proses.wait(timeout=5)
                except subprocess.TimeoutExpired: Proses.kill(); Proses.wait()
            준비살피미.close(); Proses.stdin.close(); Proses.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(barlag_hasabat,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': Bitir()
