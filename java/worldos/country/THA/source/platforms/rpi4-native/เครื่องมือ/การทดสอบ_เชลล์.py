#!/usr/bin/env python3
"""เอง 커널의 เชลล์, 프로세스 รับเข้า_ส่งออก, Unicode GUI 터미널을 ค่าจริง_ข้อมูล raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from ดําเนินการ_คําสั่ง import แสดง_ราก, คําสั่ง


def เรียกใช้งาน():
    ผลผลิต = แสดง_ราก / 'build/verification/shell'; ผลผลิต.mkdir(parents=True, exist_ok=True)
    การตรวจสอบความถูกต้อง_รายงาน = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((แสดง_ราก / 'build/kernel8.img').read_bytes()).hexdigest()}
    การถอดความ = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        โพรเซส = subprocess.Popen(คําสั่ง()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(โพรเซส.stdout,selectors.EVENT_READ)
        def รับ_อีเมล(มาร์กเกอร์, 시간제한=45):
            ข้อมูล=bytearray(); สิ้นสุดการโทร_ออฟเซต=time.monotonic()+시간제한
            while มาร์กเกอร์ not in ข้อมูล:
                if time.monotonic()>สิ้นสุดการโทร_ออฟเซต or โพรเซส.poll() is not None: raise AssertionError('UART timeout/exit: '+ข้อมูล.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: ข้อมูล.extend(조각); การถอดความ.extend(조각)
                if b'PANIC:' in ข้อมูล or b'FAIL ' in ข้อมูล: raise AssertionError(ข้อมูล)
            return ข้อมูล.decode('utf-8','replace').replace('\r\n','\n')
        def ส่ง(ข้อมูล, มาร์กเกอร์=b'jkoros-native> '):
            โพรเซส.stdin.write(ข้อมูล); โพรเซส.stdin.flush(); return รับ_อีเมล(มาร์กเกอร์)
        def เชลล์(บรรทัด, *예상결과):
            ผลลัพธ์=ส่ง(บรรทัด.encode()+b'\n')
            for ค่า in 예상결과: assert ค่า in ผลลัพธ์, (บรรทัด,ค่า,ผลลัพธ์)
            return ผลลัพธ์
        def แฟ้ม(ชื่อ):
            ข้อความ=เชลล์('hex '+ชื่อ,'HEX BEGIN','HEX END'); ค้นหา_เมตริก=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',ข้อความ,re.S)
            ข้อมูล=bytes.fromhex(''.join(ค้นหา_เมตริก.group(2).split())); assert len(ข้อมูล)==int(ค้นหา_เมตริก.group(1)); return ข้อมูล
        try:
            รับ_อีเมล(b'jkoros-native> ')
            เชลล์('mkdir 작업; cd 작업; pwd','/작업')
            เชลล์('mkdir 하위; echo "한글 ข้อมูล 😀" > 인사.txt')
            assert แฟ้ม('인사.txt')=='한글 ข้อมูล 😀\n'.encode()
            เชลล์('cp 인사.txt คัดลอก_ค่า.txt; mv คัดลอก_ค่า.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 ข้อมูล 😀')
            เชลล์('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 ข้อมูล 😀','/작업/하위')
            เชลล์('cd ..; rmdir 하위; echo $?','1\n')
            เชลล์('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            เชลล์('cp 인사.txt 인사.txt; echo $?','1\n'); assert แฟ้ม('인사.txt')=='한글 ข้อมูล 😀\n'.encode()
            เชลล์('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in แฟ้ม('인사.txt')
            เชลล์("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert แฟ้ม('리터럴')=='$인사\n누리\n'.encode()
            เชลล์('echo one > คําสั่ง_ค่า; echo two >> คําสั่ง_ค่า; echo three >> คําสั่ง_ค่า')
            เชลล์('cat < คําสั่ง_ค่า | grep t | tee 추림 | wc -l','2\n'); assert แฟ้ม('추림')==b'two\nthree\n'
            เชลล์('head -n 1 คําสั่ง_ค่า > กล้องหน้า_ค่า; tail -n 1 คําสั่ง_ค่า > ย้อนกลับ_ค่า'); assert แฟ้ม('앞')==b'one\n'; assert แฟ้ม('뒤')==b'three\n'
            เชลล์('grep absent คําสั่ง_ค่า; echo $?','1\n')
            เชลล์('echo untouched > ป้องกัน_ค่า')
            เชลล์('echo destroyed > ป้องกัน_ค่า |','명령이 빠졌습니다'); assert แฟ้ม('ป้องกัน_ค่า')==b'untouched\n'
            เชลล์('echo "oops','따옴표가 닫히지 않았습니다')
            เชลล์('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            เชลล์('echo bad 2> ป้องกัน_ค่า','번호를 지정한 แฟ้ม 서술자 รับเข้า_ส่งออก สลับ_โหมด'); assert แฟ้ม('ป้องกัน_ค่า')==b'untouched\n'
            เชลล์('rm 빈파일 리터럴 คําสั่ง_ค่า 추림 กล้องหน้า_ค่า ย้อนกลับ_ค่า ป้องกัน_ค่า')
            การตรวจสอบความถูกต้อง_รายงาน['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            เชลล์("python -c 'print(123)' | wc -c",'4\n')
            เชลล์("python -c 'print(456)' > แอป_f5044b9b.txt"); assert แฟ้ม('แอป_f5044b9b.txt')==b'456\n'
            เชลล์("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            เชลล์("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < แอป_f5044b9b.txt", "b'456\\n'", "b''")
            เชลล์("python -c 'print(\"x\"*17000)' | wc -c", 'ข้อผิดพลาด -28')
            เชลล์('echo recovered | wc -c','10\n')
            เชลล์("python -c 'import jkoros; print(jkoros.read("+'"/작업/แอป_f5044b9b.txt"'+"))'",'456','exit 0')
            เชลล์('cd /; javac Hello.java','Compiled:','exit 0')
            เชลล์('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in แฟ้ม('/작업/자바.txt')
            เชลล์('cd 작업; echo "echo script > 실행결과" > คําสั่ง.sh; echo "false || echo recovered >> 실행결과" >> คําสั่ง.sh; sh คําสั่ง.sh')
            assert แฟ้ม('실행결과')==b'script\nrecovered\n'
            เชลล์('rm 실행결과; echo "exit 7" > ออก_แอป.sh; sh ออก_แอป.sh; echo $?','7\n')
            เชลล์('rm ออก_แอป.sh คําสั่ง.sh แอป_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            การตรวจสอบความถูกต้อง_รายงาน['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            เชลล์('echo history-proof','history-proof')
            ผลลัพธ์=ส่ง(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert ผลลัพธ์.count('history-proof')>=2, ผลลัพธ์
            ส่ง(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            ผลลัพธ์=ส่ง(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in ผลลัพธ์, ผลลัพธ์
            ผลลัพธ์=ส่ง(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in ผลลัพธ์,ผลลัพธ์
            ผลลัพธ์=ส่ง('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in ผลลัพธ์,ผลลัพธ์
            긴글='한글'*50
            ผลลัพธ์=ส่ง(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in ผลลัพธ์
            เชลล์('terminal','TERMINAL READY')
            เชลล์('clear')
            เชลล์('echo "한글 เทอร์มินัล ABC xyz 012 😀"','한글 เทอร์มินัล ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as ไคลเอ็นต์:
                ไคลเอ็นต์.settimeout(10); ไคลเอ็นต์.connect(str(모의제어접속))
                with ไคลเอ็นต์.makefile('rwb') as สตรีม_ค่า:
                    json.loads(สตรีม_ค่า.readline())
                    def 호출(ชื่อ,อาร์กิวเมนต์_อาร์เรย์=None):
                        เครือข่าย_อีเมล={'execute':ชื่อ}
                        if อาร์กิวเมนต์_อาร์เรย์: เครือข่าย_อีเมล['arguments']=อาร์กิวเมนต์_อาร์เรย์
                        สตรีม_ค่า.write((json.dumps(เครือข่าย_อีเมล)+'\n').encode()); สตรีม_ค่า.flush()
                        while True:
                            ตอบกลับ=json.loads(สตรีม_ค่า.readline())
                            if 'error' in ตอบกลับ: raise AssertionError(ตอบกลับ)
                            if 'return' in ตอบกลับ: return ตอบกลับ['return']
                    호출('qmp_capabilities')
                    รูป=ผลผลิต/'terminal.ppm'; 호출('screendump',{'filename':str(รูป),'format':'ppm'})
                    호출('screendump',{'filename':str(ผลผลิต/'terminal.png'),'format':'png'})
                    ข้อมูล=รูป.read_bytes().split(b'\n',3)[3]
                    def พิกเซล(พิกัดแกน_x,세로좌표): return tuple(ข้อมูล[(세로좌표*640+พิกัดแกน_x)*3:(세로좌표*640+พิกัดแกน_x)*3+3])
                    assert พิกเซล(12,48)==(32,80,144),พิกเซล(12,48)
                    assert len(set(พิกเซล(พิกัดแกน_x,세로좌표) for 세로좌표 in range(100,116) for พิกัดแกน_x in range(24,56)))>1,'Hangul glyphs missing'
                    เชลล์('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    เชลล์("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(รูป),'format':'ppm'})
                    복원자료=รูป.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    เชลล์('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): เชลล์('echo scroll-'+str(순번),'scroll-'+str(순번))
                    ส่ง(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(ผลผลิต/'terminal-scroll.png'),'format':'png'})
                    ผลลัพธ์=ส่ง(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in ผลลัพธ์,ผลลัพธ์
                    เชลล์('rm visible.txt')
                    호출('quit')
            โพรเซส.wait(timeout=5)
            การตรวจสอบความถูกต้อง_รายงาน['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            การตรวจสอบความถูกต้อง_รายงาน['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if โพรเซส.poll() is None:
                โพรเซส.terminate()
                try: โพรเซส.wait(timeout=5)
                except subprocess.TimeoutExpired: โพรเซส.kill(); โพรเซส.wait()
            준비살피미.close(); โพรเซส.stdin.close(); โพรเซส.stdout.close()
            (ผลผลิต/'serial.log').write_bytes(การถอดความ)
            (ผลผลิต/'report.json').write_text(json.dumps(การตรวจสอบความถูกต้อง_รายงาน,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': เรียกใช้งาน()
