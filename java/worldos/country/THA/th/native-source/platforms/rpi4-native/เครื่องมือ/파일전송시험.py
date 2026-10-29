#!/usr/bin/env python3
"""Real host TCP client -> SLIP -> bare-metal lwIP -> FTP -> Java VFS."""
import ftplib
import hashlib
import io
import json
import selectors
import socket
import subprocess
import time
import zipfile
from บริดจ์_3de4fe3a import บริดจ์_3de4fe3a
from ดําเนินการ_คําสั่ง import แสดง_ราก, คําสั่ง
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def เรียกใช้งาน():
    เมตริก_ข้อมูล = แสดง_ราก / 'build/verification/ftp'; เมตริก_ข้อมูล.mkdir(parents=True, exist_ok=True)
    การตรวจสอบความถูกต้อง_รายงาน = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((แสดง_ราก / 'build/kernel8.img').read_bytes()).hexdigest()}
    การถอดความ = bytearray()
    자바원문 = เมตริก_ข้อมูล / 'การทดสอบ_รวม.java'
    자바원문.write_text('public class การทดสอบ_รวม { public static void main(String[] อาร์กิวเมนต์) throws Exception { ไทย.เอง.ข้อความออก.줄쓰기("JAR ดําเนินการ_คําสั่ง: " + อาร์กิวเมนต์[0]); ไทย.เอง.แฟ้ม.เขียน("jar.txt", "เอง เคอร์เนล_ค่า แฟ้ม"); ไทย.เอง.ข้อความออก.줄쓰기(ไทย.เอง.แฟ้ม.อ่าน("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(แสดง_ราก/'build/java-library/classes'), '-d', str(เมตริก_ข้อมูล), str(자바원문)])
    เก็บถาวร = io.BytesIO()
    with zipfile.ZipFile(เก็บถาวร, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: การทดสอบ_รวม\r\n\r\n')
        자바꾸러미.write(str(เมตริก_ข้อมูล/'การทดสอบ_รวม.class'), 'การทดสอบ_รวม.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); หมายเลขพอร์ต = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); เซิร์ฟเวอร์_สตรีม_แปลง = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); เซิร์ฟเวอร์_เดตาแกรม_แปลง = 임시자원.getsockname()[1]
    with บริดจ์_3de4fe3a(หมายเลขพอร์ต, ['tcp:{}:9300'.format(เซิร์ฟเวอร์_สตรีม_แปลง), 'udp:{}:9301'.format(เซิร์ฟเวอร์_เดตาแกรม_แปลง)], จับ=True) as บริดจ์:
        โพรเซส = subprocess.Popen(คําสั่ง() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + บริดจ์.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        ตัวเลือก_582fe3b9 = selectors.DefaultSelector(); ตัวเลือก_582fe3b9.register(โพรเซส.stdout, selectors.EVENT_READ)
        def รับ_อีเมล(มาร์กเกอร์=b'jkoros-native> ', 시간제한=60):
            ข้อมูล = bytearray(); สิ้นสุดการโทร_ออฟเซต = time.monotonic() + 시간제한
            while มาร์กเกอร์ not in ข้อมูล:
                if time.monotonic() > สิ้นสุดการโทร_ออฟเซต or โพรเซส.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + ข้อมูล.decode('utf-8', 'replace'))
                for 누름값, _ in ตัวเลือก_582fe3b9.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: ข้อมูล.extend(조각); การถอดความ.extend(조각)
                if b'PANIC:' in ข้อมูล or b'FAIL ' in ข้อมูล: raise AssertionError(ข้อมูล)
            return ข้อมูล.decode('utf-8', 'replace').replace('\r\n', '\n')
        def เชลล์(บรรทัด):
            โพรเซส.stdin.write(บรรทัด.encode() + b'\n'); โพรเซส.stdin.flush(); return รับ_อีเมล()
        try:
            รับ_อีเมล(); assert 'FTP listening' in เชลล์('ftpd start')
            การถ่ายโอนแฟ้ม_เพื่อน = ftplib.FTP(); การถ่ายโอนแฟ้ม_เพื่อน.encoding = 'utf-8'; การถ่ายโอนแฟ้ม_เพื่อน.connect('127.0.0.1', หมายเลขพอร์ต, timeout=20); การถ่ายโอนแฟ้ม_เพื่อน.login()
            ส่วนข้อมูล_ข้อมูล = bytes(range(256)) * 32
            การถ่ายโอนแฟ้ม_เพื่อน.storbinary('STOR binary.dat', io.BytesIO(ส่วนข้อมูล_ข้อมูล))
            ผลลัพธ์ = bytearray(); การถ่ายโอนแฟ้ม_เพื่อน.retrbinary('RETR binary.dat', ผลลัพธ์.extend)
            assert ผลลัพธ์ == ส่วนข้อมูล_ข้อมูล; assert การถ่ายโอนแฟ้ม_เพื่อน.size('binary.dat') == len(ส่วนข้อมูล_ข้อมูล)
            การตรวจสอบความถูกต้อง_รายงาน['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            การถ่ายโอนแฟ้ม_เพื่อน.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in เชลล์('cat 한글.txt')
            assert '한글.txt' in การถ่ายโอนแฟ้ม_เพื่อน.nlst()
            assert dict(การถ่ายโอนแฟ้ม_เพื่อน.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            การตรวจสอบความถูกต้อง_รายงาน['checks'].append('UTF-8 filename and content visible in guest shell')
            try: การถ่ายโอนแฟ้ม_เพื่อน.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            ผลลัพธ์ = bytearray(); การถ่ายโอนแฟ้ม_เพื่อน.retrbinary('RETR binary.dat', ผลลัพธ์.extend); assert ผลลัพธ์ == ส่วนข้อมูล_ข้อมูล
            การตรวจสอบความถูกต้อง_รายงาน['checks'].append('oversized replacement rejected; previous file preserved')
            with การถ่ายโอนแฟ้ม_เพื่อน.transfercmd('STOR pending.txt') as อัปโหลด_ไฟล์:
                # A control command must not change the active upload's destination.
                assert การถ่ายโอนแฟ้ม_เพื่อน.size('binary.dat') == len(ส่วนข้อมูล_ข้อมูล)
                อัปโหลด_ไฟล์.sendall(b'UPLOAD TARGET PRESERVED')
            assert การถ่ายโอนแฟ้ม_เพื่อน.voidresp().startswith('226')
            ผลลัพธ์ = bytearray(); การถ่ายโอนแฟ้ม_เพื่อน.retrbinary('RETR pending.txt', ผลลัพธ์.extend)
            assert ผลลัพธ์ == b'UPLOAD TARGET PRESERVED'
            ผลลัพธ์ = bytearray(); การถ่ายโอนแฟ้ม_เพื่อน.retrbinary('RETR binary.dat', ผลลัพธ์.extend)
            assert ผลลัพธ์ == ส่วนข้อมูล_ข้อมูล
            การถ่ายโอนแฟ้ม_เพื่อน.delete('pending.txt')
            การตรวจสอบความถูกต้อง_รายงาน['checks'].append('interleaved SIZE cannot change the active STOR destination')
            การถ่ายโอนแฟ้ม_เพื่อน.storbinary('STOR 인사.jar', io.BytesIO(เก็บถาวร.getvalue()))
            ข้อความ = เชลล์('java -jar 인사.jar 누리')
            assert 'JAR ดําเนินการ_คําสั่ง: 누리' in ข้อความ and 'เอง เคอร์เนล_ค่า แฟ้ม' in ข้อความ and 'exit 0' in ข้อความ, ข้อความ
            ข้อความ = เชลล์('./인사.jar 세상')
            assert 'JAR ดําเนินการ_คําสั่ง: 세상' in ข้อความ and 'exit 0' in ข้อความ, ข้อความ
            การตรวจสอบความถูกต้อง_รายงาน['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct ข้อมูล { int หมายเลข; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct ข้อมูล ค่า = {합(10), 1.25}; if (ค่า.หมายเลข != 55 || ค่า.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = เปิด_แฟ้ม("cc.txt", 읽고쓰기 | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; 파일자료쓰기(문서, 인사, sizeof(인사)-1); ปิด_แฟ้ม(문서); 파일자료쓰기(1, 인사, sizeof(인사)-1); return 0; }\n'
            การถ่ายโอนแฟ้ม_เพื่อน.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            ข้อความ = เชลล์('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in ข้อความ and 'exit 0' in ข้อความ, ข้อความ
            ข้อความ = เชลล์('run 한글.elf'); assert 'CC NATIVE PASS' in ข้อความ and 'exit 0' in ข้อความ, ข้อความ
            assert 'CC NATIVE PASS' in เชลล์('cat cc.txt')
            แฟ้มปฏิบัติการ = bytearray(); การถ่ายโอนแฟ้ม_เพื่อน.retrbinary('RETR 한글.elf', แฟ้มปฏิบัติการ.extend)
            assert แฟ้มปฏิบัติการ[:4] == b'\x7fELF' and แฟ้มปฏิบัติการ[18:20] == b'\xb7\x00'
            การถ่ายโอนแฟ้ม_เพื่อน.storbinary('STOR คัดลอก_ค่า.elf', io.BytesIO(แฟ้มปฏิบัติการ)); ข้อความ = เชลล์('run คัดลอก_ค่า.elf'); assert 'CC NATIVE PASS' in ข้อความ and 'exit 0' in ข้อความ, ข้อความ
            การถ่ายโอนแฟ้ม_เพื่อน.storbinary('STOR ดําเนินการ_คําสั่ง', io.BytesIO(แฟ้มปฏิบัติการ)); ข้อความ=เชลล์('./ดําเนินการ_คําสั่ง');assert 'CC NATIVE PASS' in ข้อความ and 'exit 0' in ข้อความ,ข้อความ
            การถ่ายโอนแฟ้ม_เพื่อน.storbinary('STOR ชื่อ.txt', io.BytesIO(แฟ้มปฏิบัติการ)); ข้อความ=เชลล์('./ชื่อ.txt');assert 'CC NATIVE PASS' in ข้อความ and 'exit 0' in ข้อความ,ข้อความ
            เชลล์('rm ดําเนินการ_คําสั่ง ชื่อ.txt')
            การตรวจสอบความถูกต้อง_รายงาน['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            เชลล์('rm binary.dat 한글.txt 한글.c 한글.elf คัดลอก_ค่า.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(เมตริก_ข้อมูล/'linux-reference')
            การถ่ายโอนแฟ้ม_เพื่อน.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            ข้อความ=เชลล์('./리눅스인사');assert 'exit -8' in ข้อความ,ข้อความ
            ข้อความ=เชลล์('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in ข้อความ,ข้อความ
            assert 'LINUX ELF FILE IO' in เชลล์('cat linux.txt')
            การถ่ายโอนแฟ้ม_เพื่อน.delete('리눅스인사');การถ่ายโอนแฟ้ม_เพื่อน.delete('linux.txt')
            การถ่ายโอนแฟ้ม_เพื่อน.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 หมายเลข 없습니다:' in เชลล์('./거짓.elf');การถ่ายโอนแฟ้ม_เพื่อน.delete('거짓.elf')
            การตรวจสอบความถูกต้อง_รายงาน['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                สุทธิ_แหล่ง = เมตริก_ข้อมูล/'바깥통신.java'
                สุทธิ_แหล่ง.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket เชื่อมต่อ = ไทย.เอง.เพื่อน_การโอนถ่ายข้อมูล.เชื่อมต่อ("10.0.2.2", Integer.parseInt(args[0]));
 เชื่อมต่อ.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] รหัสต้นฉบับ = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<รหัสต้นฉบับ.length;i++) if (เชื่อมต่อ.getInputStream().read() != (รหัสต้นฉบับ[i]&255)) throw new RuntimeException("TCP mismatch");
 เชื่อมต่อ.close();
 DatagramSocket ปลายทาง = ไทย.เอง.통신.เปิด(0); ไทย.เอง.통신.대기시간(ปลายทาง, 500);
 ไทย.เอง.통신.ส่ง(ปลายทาง, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!ไทย.เอง.통신.รับ(ปลายทาง).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 ปลายทาง.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(แสดง_ราก/'build/java-library/classes'),'-d',str(เมตริก_ข้อมูล),str(สุทธิ_แหล่ง)])
                การถ่ายโอนแฟ้ม_เพื่อน.storbinary('STOR 바깥통신.class', io.BytesIO((เมตริก_ข้อมูล/'바깥통신.class').read_bytes()))
                ข้อความ = เชลล์('java 바깥통신 {} {}'.format(되돌림서버항목.연결접속번호, 되돌림서버항목.전문접속번호))
                assert 'EXTERNAL TCP UDP PASS' in ข้อความ and '10.0.2.2' in ข้อความ and 'exit 0' in ข้อความ, ข้อความ
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            การตรวจสอบความถูกต้อง_รายงาน['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            การถ่ายโอนแฟ้ม_เพื่อน.delete('바깥통신.class')
            เซิร์ฟเวอร์_แหล่ง=เมตริก_ข้อมูล/'เซิร์ฟเวอร์_การทดสอบ.java'
            เซิร์ฟเวอร์_แหล่ง.write_text('''import java.net.*; public class เซิร์ฟเวอร์_การทดสอบ {
 public static void main(String[] args) throws Exception {
  ServerSocket เซิร์ฟเวอร์_ค่า = new ServerSocket(9300); DatagramSocket ปลายทาง = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket ผู้เยี่ยมชม_ค่า = เซิร์ฟเวอร์_ค่า.accept();
  ผู้เยี่ยมชม_ค่า.getOutputStream().write(ผู้เยี่ยมชม_ค่า.getInputStream().read()+1); ผู้เยี่ยมชม_ค่า.close(); เซิร์ฟเวอร์_ค่า.close();
  byte[] เนื้อหา_ค่า = new byte[8]; DatagramPacket เดตาแกรม = new DatagramPacket(เนื้อหา_ค่า, เนื้อหา_ค่า.length); ปลายทาง.receive(เดตาแกรม);
  ปลายทาง.send(เดตาแกรม); ปลายทาง.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(เมตริก_ข้อมูล),str(เซิร์ฟเวอร์_แหล่ง)])
            การถ่ายโอนแฟ้ม_เพื่อน.storbinary('STOR เซิร์ฟเวอร์_การทดสอบ.class',io.BytesIO((เมตริก_ข้อมูล/'เซิร์ฟเวอร์_การทดสอบ.class').read_bytes()))
            โพรเซส.stdin.write('java เซิร์ฟเวอร์_การทดสอบ\n'.encode());โพรเซส.stdin.flush();รับ_อีเมล(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',เซิร์ฟเวอร์_สตรีม_แปลง),timeout=5) as ชั้น_ค่า:
                ชั้น_ค่า.sendall(b'A');assert ชั้น_ค่า.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as ชั้น_ค่า:
                ชั้น_ค่า.settimeout(5);ชั้น_ค่า.sendto(b'UDP-IN',('127.0.0.1',เซิร์ฟเวอร์_เดตาแกรม_แปลง));assert ชั้น_ค่า.recvfrom(512)[0]==b'UDP-IN'
            ข้อความ=รับ_อีเมล();assert 'INBOUND TCP UDP PASS' in ข้อความ and 'exit 0' in ข้อความ,ข้อความ
            การตรวจสอบความถูกต้อง_รายงาน['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            การถ่ายโอนแฟ้ม_เพื่อน.delete('เซิร์ฟเวอร์_การทดสอบ.class')
            명령열 = 'public class 빛 { public static void main(String[] อาร์กิวเมนต์) throws Exception { int 합 = 0; int หมายเลข = 1; while (หมายเลข <= 10) { 합 = 합 + หมายเลข; หมายเลข = หมายเลข + 1; } ไทย.เอง.ข้อความออก.수쓰기(합); ไทย.เอง.แฟ้ม.เขียน("aot.txt", "한글 AOT แฟ้ม 😀"); ไทย.เอง.ข้อความออก.줄쓰기(ไทย.เอง.แฟ้ม.อ่าน("aot.txt")); } }'
            การถ่ายโอนแฟ้ม_เพื่อน.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            ข้อความ = เชลล์('javac 빛.java'); assert 'exit 0' in ข้อความ and 'Compiled:' in ข้อความ, ข้อความ
            ข้อความ = เชลล์('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in ข้อความ and 'exit 0' in ข้อความ, ข้อความ
            ข้อความ = เชลล์('run 빛.elf'); assert '\n55\n' in ข้อความ and '한글 AOT แฟ้ม 😀' in ข้อความ and 'exit 0' in ข้อความ, ข้อความ
            ดั้งเดิม = bytearray(); การถ่ายโอนแฟ้ม_เพื่อน.retrbinary('RETR 빛.elf', ดั้งเดิม.extend)
            ข้อความ = เชลล์('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in ข้อความ and 'unsupported' in ข้อความ, ข้อความ
            보존자료 = bytearray(); การถ่ายโอนแฟ้ม_เพื่อน.retrbinary('RETR 빛.elf', 보존자료.extend); assert ดั้งเดิม == 보존자료
            바이트코드 = bytearray(); การถ่ายโอนแฟ้ม_เพื่อน.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            การถ่ายโอนแฟ้ม_เพื่อน.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            ข้อความ = เชลล์('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in ข้อความ and 'exit 0' in ข้อความ, ข้อความ
            ข้อความ = เชลล์('run 빛.elf'); assert '\n55\n' in ข้อความ and '한글 AOT แฟ้ม 😀' in ข้อความ and 'exit 0' in ข้อความ, ข้อความ
            การตรวจสอบความถูกต้อง_รายงาน['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            การตรวจสอบความถูกต้อง_รายงาน['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            คงที่_แหล่ง=เมตริก_ข้อมูล/'คงที่_การทดสอบ.java'
            คงที่_แหล่ง.write_text('''public class คงที่_การทดสอบ {
 static int แสดง_ราก = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] อาร์กิวเมนต์) {
  int[] ค่า = new int[] {แสดง_ราก, 합(10)};
  System.out.println(ค่า[0] + ค่า[1]); System.out.println(อาร์กิวเมนต์[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(เมตริก_ข้อมูล),str(คงที่_แหล่ง)])
            การถ่ายโอนแฟ้ม_เพื่อน.storbinary('STOR คงที่_การทดสอบ.class',io.BytesIO((เมตริก_ข้อมูล/'คงที่_การทดสอบ.class').read_bytes()))
            ข้อความ=เชลล์('jaot คงที่_การทดสอบ.class -o คงที่_การทดสอบ.elf');assert 'exit 0' in ข้อความ,ข้อความ
            ข้อความ=เชลล์('run คงที่_การทดสอบ.elf 한글인수');assert '\n58\n한글인수\nexit 0' in ข้อความ,ข้อความ
            การถ่ายโอนแฟ้ม_เพื่อน.delete('คงที่_การทดสอบ.class');การถ่ายโอนแฟ้ม_เพื่อน.delete('คงที่_การทดสอบ.elf')
            การตรวจสอบความถูกต้อง_รายงาน['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(เก็บถาวร.getvalue());손상자료[14]^=1
            การถ่ายโอนแฟ้ม_เพื่อน.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            ข้อความ=เชลล์('java -jar 인사.jar');assert 'Main-Class\nexit 1' in ข้อความ,ข้อความ
            การตรวจสอบความถูกต้อง_รายงาน['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            การถ่ายโอนแฟ้ม_เพื่อน.quit(); assert 'FTP stopped' in เชลล์('ftpd stop')
            assert not บริดจ์.ข้อผิดพลาด, บริดจ์.ข้อผิดพลาด
            การตรวจสอบความถูกต้อง_รายงาน.update(passed=True, frames_to_guest=บริดจ์.커널수신틀수, frames_from_guest=บริดจ์.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in ตัวเลือก_582fe3b9.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: การถอดความ.extend(조각)
            บริดจ์.หยุดชั่วคราว_กิจกรรม.set()
            โพรเซส.terminate()
            try: โพรเซส.wait(timeout=5)
            except subprocess.TimeoutExpired: โพรเซส.kill(); โพรเซส.wait()
            ตัวเลือก_582fe3b9.close(); โพรเซส.stdin.close(); โพรเซส.stdout.close()
            การตรวจสอบความถูกต้อง_รายงาน['bridge_error'] = บริดจ์.ข้อผิดพลาด
            การตรวจสอบความถูกต้อง_รายงาน['frames_to_guest'] = บริดจ์.커널수신틀수; การตรวจสอบความถูกต้อง_รายงาน['frames_from_guest'] = บริดจ์.커널발신틀수
            (เมตริก_ข้อมูล/'packets.json').write_text(json.dumps(บริดจ์.แฟ้มบันทึกการติดตาม,indent=2)+'\n')
            (เมตริก_ข้อมูล / 'serial.log').write_bytes(การถอดความ)
            (เมตริก_ข้อมูล / 'report.json').write_text(json.dumps(การตรวจสอบความถูกต้อง_รายงาน, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': เรียกใช้งาน()
