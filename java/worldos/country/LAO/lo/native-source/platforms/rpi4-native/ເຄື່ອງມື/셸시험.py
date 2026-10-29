#!/usr/bin/env python3
"""자체 커널의 ເຊລ, 프로세스 ໄອ_ໂອ, Unicode GUI 터미널을 ຕົວ_ຈິງ_ຂໍ້ມູນ raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ import ໂຄງ_ການ_ເລກຮາກ, ຄໍາສັ່ງ_1f12b8e2


def ແລ່ນ():
    출력결과 = ໂຄງ_ການ_ເລກຮາກ / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    ໃຊ້ໄດ້_ລາຍງານ = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((ໂຄງ_ການ_ເລກຮາກ / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        ຂະ_ບວນ_ການ = subprocess.Popen(ຄໍາສັ່ງ_1f12b8e2()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(ຂະ_ບວນ_ການ.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            ຂໍ້ມູນ=bytearray(); ຈົບ_ອອບເຊັດ=time.monotonic()+시간제한
            while 확인표시 not in ຂໍ້ມູນ:
                if time.monotonic()>ຈົບ_ອອບເຊັດ or ຂະ_ບວນ_ການ.poll() is not None: raise AssertionError('UART timeout/exit: '+ຂໍ້ມູນ.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: ຂໍ້ມູນ.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in ຂໍ້ມູນ or b'FAIL ' in ຂໍ້ມູນ: raise AssertionError(ຂໍ້ມູນ)
            return ຂໍ້ມູນ.decode('utf-8','replace').replace('\r\n','\n')
        def ສົ່ງ(ຂໍ້ມູນ, 확인표시=b'jkoros-native> '):
            ຂະ_ບວນ_ການ.stdin.write(ຂໍ້ມູນ); ຂະ_ບວນ_ການ.stdin.flush(); return 수신하기(확인표시)
        def ເຊລ(ສາຍ, *예상결과):
            ມາດຕະການ=ສົ່ງ(ສາຍ.encode()+b'\n')
            for ຄ່າ in 예상결과: assert ຄ່າ in ມາດຕະການ, (ສາຍ,ຄ່າ,ມາດຕະການ)
            return ມາດຕະການ
        def ຟາຍ(ຊື່):
            ຂໍ້ຄວາມ=ເຊລ('hex '+ຊື່,'HEX BEGIN','HEX END'); ຊອກຫາ_ມາດຕະການ=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',ຂໍ້ຄວາມ,re.S)
            ຂໍ້ມູນ=bytes.fromhex(''.join(ຊອກຫາ_ມາດຕະການ.group(2).split())); assert len(ຂໍ້ມູນ)==int(ຊອກຫາ_ມາດຕະການ.group(1)); return ຂໍ້ມູນ
        try:
            수신하기(b'jkoros-native> ')
            ເຊລ('mkdir 작업; cd 작업; pwd','/작업')
            ເຊລ('mkdir 하위; echo "한글 ຂໍ້ມູນ 😀" > 인사.txt')
            assert ຟາຍ('인사.txt')=='한글 ຂໍ້ມູນ 😀\n'.encode()
            ເຊລ('cp 인사.txt ກ່າຍ_ຄ່າ.txt; mv ກ່າຍ_ຄ່າ.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 ຂໍ້ມູນ 😀')
            ເຊລ('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 ຂໍ້ມູນ 😀','/작업/하위')
            ເຊລ('cd ..; rmdir 하위; echo $?','1\n')
            ເຊລ('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            ເຊລ('cp 인사.txt 인사.txt; echo $?','1\n'); assert ຟາຍ('인사.txt')=='한글 ຂໍ້ມູນ 😀\n'.encode()
            ເຊລ('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in ຟາຍ('인사.txt')
            ເຊລ("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert ຟາຍ('리터럴')=='$인사\n누리\n'.encode()
            ເຊລ('echo one > ຄໍາສັ່ງ_ຄ່າ; echo two >> ຄໍາສັ່ງ_ຄ່າ; echo three >> ຄໍາສັ່ງ_ຄ່າ')
            ເຊລ('cat < ຄໍາສັ່ງ_ຄ່າ | grep t | tee 추림 | wc -l','2\n'); assert ຟາຍ('추림')==b'two\nthree\n'
            ເຊລ('head -n 1 ຄໍາສັ່ງ_ຄ່າ > ດ້ານຫນ້າ_ຄ່າ; tail -n 1 ຄໍາສັ່ງ_ຄ່າ > ກັບ_ຄືນ_ຄ່າ'); assert ຟາຍ('앞')==b'one\n'; assert ຟາຍ('뒤')==b'three\n'
            ເຊລ('grep absent ຄໍາສັ່ງ_ຄ່າ; echo $?','1\n')
            ເຊລ('echo untouched > ປົກປ້ອງ_ຄ່າ')
            ເຊລ('echo destroyed > ປົກປ້ອງ_ຄ່າ |','명령이 빠졌습니다'); assert ຟາຍ('ປົກປ້ອງ_ຄ່າ')==b'untouched\n'
            ເຊລ('echo "oops','따옴표가 닫히지 않았습니다')
            ເຊລ('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            ເຊລ('echo bad 2> ປົກປ້ອງ_ຄ່າ','번호를 지정한 ຟາຍ 서술자 ໄອ_ໂອ ສະວິດ_ໂຫມດ'); assert ຟາຍ('ປົກປ້ອງ_ຄ່າ')==b'untouched\n'
            ເຊລ('rm 빈파일 리터럴 ຄໍາສັ່ງ_ຄ່າ 추림 ດ້ານຫນ້າ_ຄ່າ ກັບ_ຄືນ_ຄ່າ ປົກປ້ອງ_ຄ່າ')
            ໃຊ້ໄດ້_ລາຍງານ['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            ເຊລ("python -c 'print(123)' | wc -c",'4\n')
            ເຊລ("python -c 'print(456)' > ແອັບ_f5044b9b.txt"); assert ຟາຍ('ແອັບ_f5044b9b.txt')==b'456\n'
            ເຊລ("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            ເຊລ("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < ແອັບ_f5044b9b.txt", "b'456\\n'", "b''")
            ເຊລ("python -c 'print(\"x\"*17000)' | wc -c", 'ຂໍ້ຜິດພາດ -28')
            ເຊລ('echo recovered | wc -c','10\n')
            ເຊລ("python -c 'import jkoros; print(jkoros.read("+'"/작업/ແອັບ_f5044b9b.txt"'+"))'",'456','exit 0')
            ເຊລ('cd /; javac Hello.java','Compiled:','exit 0')
            ເຊລ('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in ຟາຍ('/작업/자바.txt')
            ເຊລ('cd 작업; echo "echo script > 실행결과" > ຄໍາສັ່ງ_1f12b8e2.sh; echo "false || echo recovered >> 실행결과" >> ຄໍາສັ່ງ_1f12b8e2.sh; sh ຄໍາສັ່ງ_1f12b8e2.sh')
            assert ຟາຍ('실행결과')==b'script\nrecovered\n'
            ເຊລ('rm 실행결과; echo "exit 7" > ອອກ_ແອັບ.sh; sh ອອກ_ແອັບ.sh; echo $?','7\n')
            ເຊລ('rm ອອກ_ແອັບ.sh ຄໍາສັ່ງ_1f12b8e2.sh ແອັບ_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            ໃຊ້ໄດ້_ລາຍງານ['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            ເຊລ('echo history-proof','history-proof')
            ມາດຕະການ=ສົ່ງ(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert ມາດຕະການ.count('history-proof')>=2, ມາດຕະການ
            ສົ່ງ(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            ມາດຕະການ=ສົ່ງ(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in ມາດຕະການ, ມາດຕະການ
            ມາດຕະການ=ສົ່ງ(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in ມາດຕະການ,ມາດຕະການ
            ມາດຕະການ=ສົ່ງ('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in ມາດຕະການ,ມາດຕະການ
            긴글='한글'*50
            ມາດຕະການ=ສົ່ງ(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in ມາດຕະການ
            ເຊລ('terminal','TERMINAL READY')
            ເຊລ('clear')
            ເຊລ('echo "한글 ເທີມີນໍ ABC xyz 012 😀"','한글 ເທີມີນໍ ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as ລູກຂ່າຍ:
                ລູກຂ່າຍ.settimeout(10); ລູກຂ່າຍ.connect(str(모의제어접속))
                with ລູກຂ່າຍ.makefile('rwb') as ສະຕຣີມ_ຄ່າ:
                    json.loads(ສະຕຣີມ_ຄ່າ.readline())
                    def 호출(ຊື່,ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ=None):
                        ເຄືອຂ່າຍ_ອີເມວ={'execute':ຊື່}
                        if ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ: ເຄືອຂ່າຍ_ອີເມວ['arguments']=ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ
                        ສະຕຣີມ_ຄ່າ.write((json.dumps(ເຄືອຂ່າຍ_ອີເມວ)+'\n').encode()); ສະຕຣີມ_ຄ່າ.flush()
                        while True:
                            ຕອບກັບ=json.loads(ສະຕຣີມ_ຄ່າ.readline())
                            if 'error' in ຕອບກັບ: raise AssertionError(ຕອບກັບ)
                            if 'return' in ຕອບກັບ: return ຕອບກັບ['return']
                    호출('qmp_capabilities')
                    ຮູບ=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(ຮູບ),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    ຂໍ້ມູນ=ຮູບ.read_bytes().split(b'\n',3)[3]
                    def ເປ_ລ(ຈຸດ_ພິ_ກັດ_x,ປຸ່ມ_Y_ຈຸດປະສານ): return tuple(ຂໍ້ມູນ[(ປຸ່ມ_Y_ຈຸດປະສານ*640+ຈຸດ_ພິ_ກັດ_x)*3:(ປຸ່ມ_Y_ຈຸດປະສານ*640+ຈຸດ_ພິ_ກັດ_x)*3+3])
                    assert ເປ_ລ(12,48)==(32,80,144),ເປ_ລ(12,48)
                    assert len(set(ເປ_ລ(ຈຸດ_ພິ_ກັດ_x,ປຸ່ມ_Y_ຈຸດປະສານ) for ປຸ່ມ_Y_ຈຸດປະສານ in range(100,116) for ຈຸດ_ພິ_ກັດ_x in range(24,56)))>1,'Hangul glyphs missing'
                    ເຊລ('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    ເຊລ("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(ຮູບ),'format':'ppm'})
                    복원자료=ຮູບ.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    ເຊລ('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): ເຊລ('echo scroll-'+str(순번),'scroll-'+str(순번))
                    ສົ່ງ(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    ມາດຕະການ=ສົ່ງ(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in ມາດຕະການ,ມາດຕະການ
                    ເຊລ('rm visible.txt')
                    호출('quit')
            ຂະ_ບວນ_ການ.wait(timeout=5)
            ໃຊ້ໄດ້_ລາຍງານ['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            ໃຊ້ໄດ້_ລາຍງານ['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if ຂະ_ບວນ_ການ.poll() is None:
                ຂະ_ບວນ_ການ.terminate()
                try: ຂະ_ບວນ_ການ.wait(timeout=5)
                except subprocess.TimeoutExpired: ຂະ_ບວນ_ການ.kill(); ຂະ_ບວນ_ການ.wait()
            준비살피미.close(); ຂະ_ບວນ_ການ.stdin.close(); ຂະ_ບວນ_ການ.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(ໃຊ້ໄດ້_ລາຍງານ,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': ແລ່ນ()
