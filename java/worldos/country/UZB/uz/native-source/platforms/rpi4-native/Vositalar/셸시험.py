#!/usr/bin/env python3
"""자체 커널의 qobiq, 프로세스 I_O, Unicode GUI 터미널을 real_ma_lumotlar raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from bajarmoq_buyruq import Project_ildiz, Buyruq


def Bajarish():
    출력결과 = Project_ildiz / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    tasdiq_hisobot = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((Project_ildiz / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Jarayon = subprocess.Popen(Buyruq()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Jarayon.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            ma_lumotlar=bytearray(); to_xtatmoq_OFFSET=time.monotonic()+시간제한
            while 확인표시 not in ma_lumotlar:
                if time.monotonic()>to_xtatmoq_OFFSET or Jarayon.poll() is not None: raise AssertionError('UART timeout/exit: '+ma_lumotlar.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: ma_lumotlar.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in ma_lumotlar or b'FAIL ' in ma_lumotlar: raise AssertionError(ma_lumotlar)
            return ma_lumotlar.decode('utf-8','replace').replace('\r\n','\n')
        def yuborish(ma_lumotlar, 확인표시=b'jkoros-native> '):
            Jarayon.stdin.write(ma_lumotlar); Jarayon.stdin.flush(); return 수신하기(확인표시)
        def qobiq(satr, *예상결과):
            o_lchov=yuborish(satr.encode()+b'\n')
            for VALUE in 예상결과: assert VALUE in o_lchov, (satr,VALUE,o_lchov)
            return o_lchov
        def Fayl(Nomi):
            Matn=qobiq('hex '+Nomi,'HEX BEGIN','HEX END'); Izlash_o_lchov=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',Matn,re.S)
            ma_lumotlar=bytes.fromhex(''.join(Izlash_o_lchov.group(2).split())); assert len(ma_lumotlar)==int(Izlash_o_lchov.group(1)); return ma_lumotlar
        try:
            수신하기(b'jkoros-native> ')
            qobiq('mkdir 작업; cd 작업; pwd','/작업')
            qobiq('mkdir 하위; echo "한글 ma_lumotlar 😀" > 인사.txt')
            assert Fayl('인사.txt')=='한글 ma_lumotlar 😀\n'.encode()
            qobiq('cp 인사.txt namuna_VALUE.txt; mv namuna_VALUE.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 ma_lumotlar 😀')
            qobiq('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 ma_lumotlar 😀','/작업/하위')
            qobiq('cd ..; rmdir 하위; echo $?','1\n')
            qobiq('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            qobiq('cp 인사.txt 인사.txt; echo $?','1\n'); assert Fayl('인사.txt')=='한글 ma_lumotlar 😀\n'.encode()
            qobiq('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in Fayl('인사.txt')
            qobiq("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Fayl('리터럴')=='$인사\n누리\n'.encode()
            qobiq('echo one > bayonot_VALUE; echo two >> bayonot_VALUE; echo three >> bayonot_VALUE')
            qobiq('cat < bayonot_VALUE | grep t | tee 추림 | wc -l','2\n'); assert Fayl('추림')==b'two\nthree\n'
            qobiq('head -n 1 bayonot_VALUE > old_kamera_VALUE; tail -n 1 bayonot_VALUE > Orqaga_VALUE'); assert Fayl('앞')==b'one\n'; assert Fayl('뒤')==b'three\n'
            qobiq('grep absent bayonot_VALUE; echo $?','1\n')
            qobiq('echo untouched > himoya_qilmoq_VALUE')
            qobiq('echo destroyed > himoya_qilmoq_VALUE |','명령이 빠졌습니다'); assert Fayl('himoya_qilmoq_VALUE')==b'untouched\n'
            qobiq('echo "oops','따옴표가 닫히지 않았습니다')
            qobiq('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            qobiq('echo bad 2> himoya_qilmoq_VALUE','번호를 지정한 Fayl 서술자 I_O SWITCH_MODE'); assert Fayl('himoya_qilmoq_VALUE')==b'untouched\n'
            qobiq('rm 빈파일 리터럴 bayonot_VALUE 추림 old_kamera_VALUE Orqaga_VALUE himoya_qilmoq_VALUE')
            tasdiq_hisobot['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            qobiq("python -c 'print(123)' | wc -c",'4\n')
            qobiq("python -c 'print(456)' > ilova_f5044b9b.txt"); assert Fayl('ilova_f5044b9b.txt')==b'456\n'
            qobiq("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            qobiq("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < ilova_f5044b9b.txt", "b'456\\n'", "b''")
            qobiq("python -c 'print(\"x\"*17000)' | wc -c", 'Xato -28')
            qobiq('echo recovered | wc -c','10\n')
            qobiq("python -c 'import jkoros; print(jkoros.read("+'"/작업/ilova_f5044b9b.txt"'+"))'",'456','exit 0')
            qobiq('cd /; javac Hello.java','Compiled:','exit 0')
            qobiq('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in Fayl('/작업/자바.txt')
            qobiq('cd 작업; echo "echo script > 실행결과" > Buyruq.sh; echo "false || echo recovered >> 실행결과" >> Buyruq.sh; sh Buyruq.sh')
            assert Fayl('실행결과')==b'script\nrecovered\n'
            qobiq('rm 실행결과; echo "exit 7" > Chiqish_ilova.sh; sh Chiqish_ilova.sh; echo $?','7\n')
            qobiq('rm Chiqish_ilova.sh Buyruq.sh ilova_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            tasdiq_hisobot['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            qobiq('echo history-proof','history-proof')
            o_lchov=yuborish(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert o_lchov.count('history-proof')>=2, o_lchov
            yuborish(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            o_lchov=yuborish(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in o_lchov, o_lchov
            o_lchov=yuborish(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in o_lchov,o_lchov
            o_lchov=yuborish('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in o_lchov,o_lchov
            긴글='한글'*50
            o_lchov=yuborish(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in o_lchov
            qobiq('terminal','TERMINAL READY')
            qobiq('clear')
            qobiq('echo "한글 Terminal ABC xyz 012 😀"','한글 Terminal ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as mijoz:
                mijoz.settimeout(10); mijoz.connect(str(모의제어접속))
                with mijoz.makefile('rwb') as oqim_VALUE:
                    json.loads(oqim_VALUE.readline())
                    def 호출(Nomi,dalil_ARRAY=None):
                        Tarmoq_xabar={'execute':Nomi}
                        if dalil_ARRAY: Tarmoq_xabar['arguments']=dalil_ARRAY
                        oqim_VALUE.write((json.dumps(Tarmoq_xabar)+'\n').encode()); oqim_VALUE.flush()
                        while True:
                            javob_berish=json.loads(oqim_VALUE.readline())
                            if 'error' in javob_berish: raise AssertionError(javob_berish)
                            if 'return' in javob_berish: return javob_berish['return']
                    호출('qmp_capabilities')
                    rasm=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(rasm),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    ma_lumotlar=rasm.read_bytes().split(b'\n',3)[3]
                    def piksel(x_koordinata,Y_tugmasi_koordinat): return tuple(ma_lumotlar[(Y_tugmasi_koordinat*640+x_koordinata)*3:(Y_tugmasi_koordinat*640+x_koordinata)*3+3])
                    assert piksel(12,48)==(32,80,144),piksel(12,48)
                    assert len(set(piksel(x_koordinata,Y_tugmasi_koordinat) for Y_tugmasi_koordinat in range(100,116) for x_koordinata in range(24,56)))>1,'Hangul glyphs missing'
                    qobiq('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    qobiq("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(rasm),'format':'ppm'})
                    복원자료=rasm.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    qobiq('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): qobiq('echo scroll-'+str(순번),'scroll-'+str(순번))
                    yuborish(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    o_lchov=yuborish(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in o_lchov,o_lchov
                    qobiq('rm visible.txt')
                    호출('quit')
            Jarayon.wait(timeout=5)
            tasdiq_hisobot['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            tasdiq_hisobot['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Jarayon.poll() is None:
                Jarayon.terminate()
                try: Jarayon.wait(timeout=5)
                except subprocess.TimeoutExpired: Jarayon.kill(); Jarayon.wait()
            준비살피미.close(); Jarayon.stdin.close(); Jarayon.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(tasdiq_hisobot,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': Bajarish()
