#!/usr/bin/env python3
"""자체 커널의 nkọwannyemiwu, 프로세스 I_O, Unicode GUI 터미널을 ǹdịnezie_datà raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from mee_nnyemiwu import 기준, Ntiiwu


def Bido():
    출력결과 = 기준 / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    nkwèputaonòdù_akụkọ = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        ùsòrò = subprocess.Popen(Ntiiwu()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(ùsòrò.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            datà=bytearray(); mèdebe_Nnokwata=time.monotonic()+시간제한
            while 확인표시 not in datà:
                if time.monotonic()>mèdebe_Nnokwata or ùsòrò.poll() is not None: raise AssertionError('UART timeout/exit: '+datà.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: datà.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in datà or b'FAIL ' in datà: raise AssertionError(datà)
            return datà.decode('utf-8','replace').replace('\r\n','\n')
        def zìga(datà, 확인표시=b'jkoros-native> '):
            ùsòrò.stdin.write(datà); ùsòrò.stdin.flush(); return 수신하기(확인표시)
        def nkọwannyemiwu(ahịrī, *예상결과):
            결과=zìga(ahịrī.encode()+b'\n')
            for valuu in 예상결과: assert valuu in 결과, (ahịrī,valuu,결과)
            return 결과
        def Faịlụ(Aha):
            SMS=nkọwannyemiwu('hex '+Aha,'HEX BEGIN','HEX END'); 찾은결과=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',SMS,re.S)
            datà=bytes.fromhex(''.join(찾은결과.group(2).split())); assert len(datà)==int(찾은결과.group(1)); return datà
        try:
            수신하기(b'jkoros-native> ')
            nkọwannyemiwu('mkdir 작업; cd 작업; pwd','/작업')
            nkọwannyemiwu('mkdir 하위; echo "한글 datà 😀" > 인사.txt')
            assert Faịlụ('인사.txt')=='한글 datà 😀\n'.encode()
            nkọwannyemiwu('cp 인사.txt ṅomie_valuu.txt; mv ṅomie_valuu.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 datà 😀')
            nkọwannyemiwu('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 datà 😀','/작업/하위')
            nkọwannyemiwu('cd ..; rmdir 하위; echo $?','1\n')
            nkọwannyemiwu('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            nkọwannyemiwu('cp 인사.txt 인사.txt; echo $?','1\n'); assert Faịlụ('인사.txt')=='한글 datà 😀\n'.encode()
            nkọwannyemiwu('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in Faịlụ('인사.txt')
            nkọwannyemiwu("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Faịlụ('리터럴')=='$인사\n누리\n'.encode()
            nkọwannyemiwu('echo one > nkwupute_valuu; echo two >> nkwupute_valuu; echo three >> nkwupute_valuu')
            nkọwannyemiwu('cat < nkwupute_valuu | grep t | tee 추림 | wc -l','2\n'); assert Faịlụ('추림')==b'two\nthree\n'
            nkọwannyemiwu('head -n 1 nkwupute_valuu > 앞; tail -n 1 nkwupute_valuu > Àzụ_valuu'); assert Faịlụ('앞')==b'one\n'; assert Faịlụ('뒤')==b'three\n'
            nkọwannyemiwu('grep absent nkwupute_valuu; echo $?','1\n')
            nkọwannyemiwu('echo untouched > nchedo_valuu')
            nkọwannyemiwu('echo destroyed > nchedo_valuu |','명령이 빠졌습니다'); assert Faịlụ('nchedo_valuu')==b'untouched\n'
            nkọwannyemiwu('echo "oops','따옴표가 닫히지 않았습니다')
            nkọwannyemiwu('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            nkọwannyemiwu('echo bad 2> nchedo_valuu','번호를 지정한 Faịlụ 서술자 I_O ngbanwụ_moòdù'); assert Faịlụ('nchedo_valuu')==b'untouched\n'
            nkọwannyemiwu('rm 빈파일 리터럴 nkwupute_valuu 추림 앞 Àzụ_valuu nchedo_valuu')
            nkwèputaonòdù_akụkọ['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            nkọwannyemiwu("python -c 'print(123)' | wc -c",'4\n')
            nkọwannyemiwu("python -c 'print(456)' > app_f5044b9b.txt"); assert Faịlụ('app_f5044b9b.txt')==b'456\n'
            nkọwannyemiwu("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            nkọwannyemiwu("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < app_f5044b9b.txt", "b'456\\n'", "b''")
            nkọwannyemiwu("python -c 'print(\"x\"*17000)' | wc -c", 'mmejọ -28')
            nkọwannyemiwu('echo recovered | wc -c','10\n')
            nkọwannyemiwu("python -c 'import jkoros; print(jkoros.read("+'"/작업/app_f5044b9b.txt"'+"))'",'456','exit 0')
            nkọwannyemiwu('cd /; javac Hello.java','Compiled:','exit 0')
            nkọwannyemiwu('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in Faịlụ('/작업/자바.txt')
            nkọwannyemiwu('cd 작업; echo "echo script > 실행결과" > Ntiiwu.sh; echo "false || echo recovered >> 실행결과" >> Ntiiwu.sh; sh Ntiiwu.sh')
            assert Faịlụ('실행결과')==b'script\nrecovered\n'
            nkọwannyemiwu('rm 실행결과; echo "exit 7" > pụọ_app.sh; sh pụọ_app.sh; echo $?','7\n')
            nkọwannyemiwu('rm pụọ_app.sh Ntiiwu.sh app_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            nkwèputaonòdù_akụkọ['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            nkọwannyemiwu('echo history-proof','history-proof')
            결과=zìga(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert 결과.count('history-proof')>=2, 결과
            zìga(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            결과=zìga(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in 결과, 결과
            결과=zìga(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in 결과,결과
            결과=zìga('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in 결과,결과
            긴글='한글'*50
            결과=zìga(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in 결과
            nkọwannyemiwu('terminal','TERMINAL READY')
            nkọwannyemiwu('clear')
            nkọwannyemiwu('echo "한글 터미널 ABC xyz 012 😀"','한글 터미널 ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as klayènt:
                klayènt.settimeout(10); klayènt.connect(str(모의제어접속))
                with klayènt.makefile('rwb') as agịrị_valuu:
                    json.loads(agịrị_valuu.readline())
                    def 호출(Aha,agụment_MKPOKỌTA=None):
                        Netwọọkụ_ozi={'execute':Aha}
                        if agụment_MKPOKỌTA: Netwọọkụ_ozi['arguments']=agụment_MKPOKỌTA
                        agịrị_valuu.write((json.dumps(Netwọọkụ_ozi)+'\n').encode()); agịrị_valuu.flush()
                        while True:
                            nzaghachi=json.loads(agịrị_valuu.readline())
                            if 'error' in nzaghachi: raise AssertionError(nzaghachi)
                            if 'return' in nzaghachi: return nzaghachi['return']
                    호출('qmp_capabilities')
                    foto=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(foto),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    datà=foto.read_bytes().split(b'\n',3)[3]
                    def pel(ngakọrịta_x,세로좌표): return tuple(datà[(세로좌표*640+ngakọrịta_x)*3:(세로좌표*640+ngakọrịta_x)*3+3])
                    assert pel(12,48)==(32,80,144),pel(12,48)
                    assert len(set(pel(ngakọrịta_x,세로좌표) for 세로좌표 in range(100,116) for ngakọrịta_x in range(24,56)))>1,'Hangul glyphs missing'
                    nkọwannyemiwu('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    nkọwannyemiwu("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(foto),'format':'ppm'})
                    복원자료=foto.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    nkọwannyemiwu('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): nkọwannyemiwu('echo scroll-'+str(순번),'scroll-'+str(순번))
                    zìga(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    결과=zìga(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in 결과,결과
                    nkọwannyemiwu('rm visible.txt')
                    호출('quit')
            ùsòrò.wait(timeout=5)
            nkwèputaonòdù_akụkọ['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            nkwèputaonòdù_akụkọ['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if ùsòrò.poll() is None:
                ùsòrò.terminate()
                try: ùsòrò.wait(timeout=5)
                except subprocess.TimeoutExpired: ùsòrò.kill(); ùsòrò.wait()
            준비살피미.close(); ùsòrò.stdin.close(); ùsòrò.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(nkwèputaonòdù_akụkọ,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': Bido()
