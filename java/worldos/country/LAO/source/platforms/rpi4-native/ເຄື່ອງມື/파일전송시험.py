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
from ເຄືອຂ່າຍ_ຕົວເຊື່ອມ import ເຄືອຂ່າຍ_ຕົວເຊື່ອມ
from ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ import ໂຄງ_ການ_ເລກຮາກ, ຄໍາສັ່ງ_1f12b8e2
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def ແລ່ນ():
    ມາດຕະການ_ຂໍ້ມູນ = ໂຄງ_ການ_ເລກຮາກ / 'build/verification/ftp'; ມາດຕະການ_ຂໍ້ມູນ.mkdir(parents=True, exist_ok=True)
    ໃຊ້ໄດ້_ລາຍງານ = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((ໂຄງ_ການ_ເລກຮາກ / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = ມາດຕະການ_ຂໍ້ມູນ / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] 인수) throws Exception { 한국어.자체.출력.ຂຽນ_ສາຍ("JAR ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ: " + 인수[0]); 한국어.자체.ຟາຍ.ຂຽນ("jar.txt", "자체 ແກນກາງ_ຄ່າ ຟາຍ"); 한국어.자체.출력.ຂຽນ_ສາຍ(한국어.자체.ຟາຍ.읽기("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(ໂຄງ_ການ_ເລກຮາກ/'build/java-library/classes'), '-d', str(ມາດຕະການ_ຂໍ້ມູນ), str(자바원문)])
    ການສໍາເນົາ = io.BytesIO()
    with zipfile.ZipFile(ການສໍາເນົາ, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(ມາດຕະການ_ຂໍ້ມູນ/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); ຫມາຍເລກພອດ = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버연결접속번호 = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with ເຄືອຂ່າຍ_ຕົວເຊື່ອມ(ຫມາຍເລກພອດ, ['tcp:{}:9300'.format(서버연결접속번호), 'udp:{}:9301'.format(서버전문접속번호)], ບັນທຶກ_ba7b8054=True) as ຕົວເຊື່ອມ:
        ຂະ_ບວນ_ການ = subprocess.Popen(ຄໍາສັ່ງ_1f12b8e2() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + ຕົວເຊື່ອມ.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        ຕົວ_ໃຊ້_ເລືອກ = selectors.DefaultSelector(); ຕົວ_ໃຊ້_ເລືອກ.register(ຂະ_ບວນ_ການ.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            ຂໍ້ມູນ = bytearray(); ຈົບ_ອອບເຊັດ = time.monotonic() + 시간제한
            while 확인표시 not in ຂໍ້ມູນ:
                if time.monotonic() > ຈົບ_ອອບເຊັດ or ຂະ_ບວນ_ການ.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + ຂໍ້ມູນ.decode('utf-8', 'replace'))
                for 누름값, _ in ຕົວ_ໃຊ້_ເລືອກ.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: ຂໍ້ມູນ.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in ຂໍ້ມູນ or b'FAIL ' in ຂໍ້ມູນ: raise AssertionError(ຂໍ້ມູນ)
            return ຂໍ້ມູນ.decode('utf-8', 'replace').replace('\r\n', '\n')
        def ເຊລ(ສາຍ):
            ຂະ_ບວນ_ການ.stdin.write(ສາຍ.encode() + b'\n'); ຂະ_ບວນ_ການ.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in ເຊລ('ftpd start')
            ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່ = ftplib.FTP(); ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.encoding = 'utf-8'; ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.connect('127.0.0.1', ຫມາຍເລກພອດ, timeout=20); ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.login()
            ນ້ໍາຫນັກບັນທຸກ_ຂໍ້ມູນ = bytes(range(256)) * 32
            ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.storbinary('STOR binary.dat', io.BytesIO(ນ້ໍາຫນັກບັນທຸກ_ຂໍ້ມູນ))
            ມາດຕະການ = bytearray(); ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.retrbinary('RETR binary.dat', ມາດຕະການ.extend)
            assert ມາດຕະການ == ນ້ໍາຫນັກບັນທຸກ_ຂໍ້ມູນ; assert ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.size('binary.dat') == len(ນ້ໍາຫນັກບັນທຸກ_ຂໍ້ມູນ)
            ໃຊ້ໄດ້_ລາຍງານ['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in ເຊລ('cat 한글.txt')
            assert '한글.txt' in ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.nlst()
            assert dict(ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            ໃຊ້ໄດ້_ລາຍງານ['checks'].append('UTF-8 filename and content visible in guest shell')
            try: ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            ມາດຕະການ = bytearray(); ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.retrbinary('RETR binary.dat', ມາດຕະການ.extend); assert ມາດຕະການ == ນ້ໍາຫນັກບັນທຸກ_ຂໍ້ມູນ
            ໃຊ້ໄດ້_ລາຍງານ['checks'].append('oversized replacement rejected; previous file preserved')
            with ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.transfercmd('STOR pending.txt') as ໂອນອອກ_ໄຟລ໌:
                # A control command must not change the active upload's destination.
                assert ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.size('binary.dat') == len(ນ້ໍາຫນັກບັນທຸກ_ຂໍ້ມູນ)
                ໂອນອອກ_ໄຟລ໌.sendall(b'UPLOAD TARGET PRESERVED')
            assert ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.voidresp().startswith('226')
            ມາດຕະການ = bytearray(); ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.retrbinary('RETR pending.txt', ມາດຕະການ.extend)
            assert ມາດຕະການ == b'UPLOAD TARGET PRESERVED'
            ມາດຕະການ = bytearray(); ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.retrbinary('RETR binary.dat', ມາດຕະການ.extend)
            assert ມາດຕະການ == ນ້ໍາຫນັກບັນທຸກ_ຂໍ້ມູນ
            ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.delete('pending.txt')
            ໃຊ້ໄດ້_ລາຍງານ['checks'].append('interleaved SIZE cannot change the active STOR destination')
            ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.storbinary('STOR 인사.jar', io.BytesIO(ການສໍາເນົາ.getvalue()))
            ຂໍ້ຄວາມ = ເຊລ('java -jar 인사.jar 누리')
            assert 'JAR ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ: 누리' in ຂໍ້ຄວາມ and '자체 ແກນກາງ_ຄ່າ ຟາຍ' in ຂໍ້ຄວາມ and 'exit 0' in ຂໍ້ຄວາມ, ຂໍ້ຄວາມ
            ຂໍ້ຄວາມ = ເຊລ('./인사.jar 세상')
            assert 'JAR ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ: 세상' in ຂໍ້ຄວາມ and 'exit 0' in ຂໍ້ຄວາມ, ຂໍ້ຄວາມ
            ໃຊ້ໄດ້_ລາຍງານ['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct ຂໍ້ມູນ { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct ຂໍ້ມູນ ຄ່າ = {합(10), 1.25}; if (ຄ່າ.수 != 55 || ຄ່າ.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = ສ້າງ_ຟາຍ("cc.txt", ອ່ານ_ຂຽນ | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; ຂຽນ_ຟາຍ_ຂໍ້ມູນ(문서, 인사, sizeof(인사)-1); ປິດ_ຟາຍ(문서); ຂຽນ_ຟາຍ_ຂໍ້ມູນ(1, 인사, sizeof(인사)-1); return 0; }\n'
            ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            ຂໍ້ຄວາມ = ເຊລ('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in ຂໍ້ຄວາມ and 'exit 0' in ຂໍ້ຄວາມ, ຂໍ້ຄວາມ
            ຂໍ້ຄວາມ = ເຊລ('run 한글.elf'); assert 'CC NATIVE PASS' in ຂໍ້ຄວາມ and 'exit 0' in ຂໍ້ຄວາມ, ຂໍ້ຄວາມ
            assert 'CC NATIVE PASS' in ເຊລ('cat cc.txt')
            실행파일 = bytearray(); ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.storbinary('STOR ກ່າຍ_ຄ່າ.elf', io.BytesIO(실행파일)); ຂໍ້ຄວາມ = ເຊລ('run ກ່າຍ_ຄ່າ.elf'); assert 'CC NATIVE PASS' in ຂໍ້ຄວາມ and 'exit 0' in ຂໍ້ຄວາມ, ຂໍ້ຄວາມ
            ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.storbinary('STOR ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ', io.BytesIO(실행파일)); ຂໍ້ຄວາມ=ເຊລ('./ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ');assert 'CC NATIVE PASS' in ຂໍ້ຄວາມ and 'exit 0' in ຂໍ້ຄວາມ,ຂໍ້ຄວາມ
            ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.storbinary('STOR ຊື່.txt', io.BytesIO(실행파일)); ຂໍ້ຄວາມ=ເຊລ('./ຊື່.txt');assert 'CC NATIVE PASS' in ຂໍ້ຄວາມ and 'exit 0' in ຂໍ້ຄວາມ,ຂໍ້ຄວາມ
            ເຊລ('rm ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ ຊື່.txt')
            ໃຊ້ໄດ້_ລາຍງານ['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            ເຊລ('rm binary.dat 한글.txt 한글.c 한글.elf ກ່າຍ_ຄ່າ.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(ມາດຕະການ_ຂໍ້ມູນ/'linux-reference')
            ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            ຂໍ້ຄວາມ=ເຊລ('./리눅스인사');assert 'exit -8' in ຂໍ້ຄວາມ,ຂໍ້ຄວາມ
            ຂໍ້ຄວາມ=ເຊລ('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in ຂໍ້ຄວາມ,ຂໍ້ຄວາມ
            assert 'LINUX ELF FILE IO' in ເຊລ('cat linux.txt')
            ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.delete('리눅스인사');ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.delete('linux.txt')
            ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in ເຊລ('./거짓.elf');ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.delete('거짓.elf')
            ໃຊ້ໄດ້_ລາຍງານ['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = ມາດຕະການ_ຂໍ້ມູນ/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket ເຊື່ອມຕໍ່ = 한국어.자체.연결통신.ເຊື່ອມຕໍ່("10.0.2.2", Integer.parseInt(args[0]));
 ເຊື່ອມຕໍ່.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] ແຫຼ່ງທີ່ມາ = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<ແຫຼ່ງທີ່ມາ.length;i++) if (ເຊື່ອມຕໍ່.getInputStream().read() != (ແຫຼ່ງທີ່ມາ[i]&255)) throw new RuntimeException("TCP mismatch");
 ເຊື່ອມຕໍ່.close();
 DatagramSocket 종단 = 한국어.자체.통신.ສ້າງ(0); 한국어.자체.통신.대기시간(종단, 500);
 한국어.자체.통신.ສົ່ງ(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!한국어.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(ໂຄງ_ການ_ເລກຮາກ/'build/java-library/classes'),'-d',str(ມາດຕະການ_ຂໍ້ມູນ),str(통신원문)])
                ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.storbinary('STOR 바깥통신.class', io.BytesIO((ມາດຕະການ_ຂໍ້ມູນ/'바깥통신.class').read_bytes()))
                ຂໍ້ຄວາມ = ເຊລ('java 바깥통신 {} {}'.format(되돌림서버항목.ທີຊີພີ_ຜອດ, 되돌림서버항목.ຢູດີພີ_ຜອດ))
                assert 'EXTERNAL TCP UDP PASS' in ຂໍ້ຄວາມ and '10.0.2.2' in ຂໍ້ຄວາມ and 'exit 0' in ຂໍ້ຄວາມ, ຂໍ້ຄວາມ
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            ໃຊ້ໄດ້_ລາຍງານ['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.delete('바깥통신.class')
            서버원문=ມາດຕະການ_ຂໍ້ມູນ/'서버시험.java'
            서버원문.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket 서버 = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket ແຂກ_ຄ່າ = 서버.accept();
  ແຂກ_ຄ່າ.getOutputStream().write(ແຂກ_ຄ່າ.getInputStream().read()+1); ແຂກ_ຄ່າ.close(); 서버.close();
  byte[] ເນື້ອໃນ_ຄ່າ_cb0f2404 = new byte[8]; DatagramPacket 전문 = new DatagramPacket(ເນື້ອໃນ_ຄ່າ_cb0f2404, ເນື້ອໃນ_ຄ່າ_cb0f2404.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(ມາດຕະການ_ຂໍ້ມູນ),str(서버원문)])
            ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.storbinary('STOR 서버시험.class',io.BytesIO((ມາດຕະການ_ຂໍ້ມູນ/'서버시험.class').read_bytes()))
            ຂະ_ບວນ_ການ.stdin.write('java 서버시험\n'.encode());ຂະ_ບວນ_ການ.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',서버연결접속번호),timeout=5) as ລຸ້ນດຽວກັນ_ຄ່າ:
                ລຸ້ນດຽວກັນ_ຄ່າ.sendall(b'A');assert ລຸ້ນດຽວກັນ_ຄ່າ.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as ລຸ້ນດຽວກັນ_ຄ່າ:
                ລຸ້ນດຽວກັນ_ຄ່າ.settimeout(5);ລຸ້ນດຽວກັນ_ຄ່າ.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert ລຸ້ນດຽວກັນ_ຄ່າ.recvfrom(512)[0]==b'UDP-IN'
            ຂໍ້ຄວາມ=수신하기();assert 'INBOUND TCP UDP PASS' in ຂໍ້ຄວາມ and 'exit 0' in ຂໍ້ຄວາມ,ຂໍ້ຄວາມ
            ໃຊ້ໄດ້_ລາຍງານ['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.delete('서버시험.class')
            명령열 = 'public class 빛 { public static void main(String[] 인수) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } 한국어.자체.출력.수쓰기(합); 한국어.자체.ຟາຍ.ຂຽນ("aot.txt", "한글 AOT ຟາຍ 😀"); 한국어.자체.출력.ຂຽນ_ສາຍ(한국어.자체.ຟາຍ.읽기("aot.txt")); } }'
            ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            ຂໍ້ຄວາມ = ເຊລ('javac 빛.java'); assert 'exit 0' in ຂໍ້ຄວາມ and 'Compiled:' in ຂໍ້ຄວາມ, ຂໍ້ຄວາມ
            ຂໍ້ຄວາມ = ເຊລ('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in ຂໍ້ຄວາມ and 'exit 0' in ຂໍ້ຄວາມ, ຂໍ້ຄວາມ
            ຂໍ້ຄວາມ = ເຊລ('run 빛.elf'); assert '\n55\n' in ຂໍ້ຄວາມ and '한글 AOT ຟາຍ 😀' in ຂໍ້ຄວາມ and 'exit 0' in ຂໍ້ຄວາມ, ຂໍ້ຄວາມ
            자체실행파일 = bytearray(); ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            ຂໍ້ຄວາມ = ເຊລ('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in ຂໍ້ຄວາມ and 'unsupported' in ຂໍ້ຄວາມ, ຂໍ້ຄວາມ
            보존자료 = bytearray(); ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            ຂໍ້ຄວາມ = ເຊລ('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in ຂໍ້ຄວາມ and 'exit 0' in ຂໍ້ຄວາມ, ຂໍ້ຄວາມ
            ຂໍ້ຄວາມ = ເຊລ('run 빛.elf'); assert '\n55\n' in ຂໍ້ຄວາມ and '한글 AOT ຟາຍ 😀' in ຂໍ້ຄວາມ and 'exit 0' in ຂໍ້ຄວາມ, ຂໍ້ຄວາມ
            ໃຊ້ໄດ້_ລາຍງານ['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            ໃຊ້ໄດ້_ລາຍງານ['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            ກໍານົດເອງ_ແຫຼ່ງທີ່ມາ=ມາດຕະການ_ຂໍ້ມູນ/'정적시험.java'
            ກໍານົດເອງ_ແຫຼ່ງທີ່ມາ.write_text('''public class 정적시험 {
 static int ໂຄງ_ການ_ເລກຮາກ = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] 인수) {
  int[] ຄ່າ = new int[] {ໂຄງ_ການ_ເລກຮາກ, 합(10)};
  System.out.println(ຄ່າ[0] + ຄ່າ[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(ມາດຕະການ_ຂໍ້ມູນ),str(ກໍານົດເອງ_ແຫຼ່ງທີ່ມາ)])
            ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.storbinary('STOR 정적시험.class',io.BytesIO((ມາດຕະການ_ຂໍ້ມູນ/'정적시험.class').read_bytes()))
            ຂໍ້ຄວາມ=ເຊລ('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in ຂໍ້ຄວາມ,ຂໍ້ຄວາມ
            ຂໍ້ຄວາມ=ເຊລ('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in ຂໍ້ຄວາມ,ຂໍ້ຄວາມ
            ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.delete('정적시험.class');ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.delete('정적시험.elf')
            ໃຊ້ໄດ້_ລາຍງານ['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(ການສໍາເນົາ.getvalue());손상자료[14]^=1
            ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            ຂໍ້ຄວາມ=ເຊລ('java -jar 인사.jar');assert 'Main-Class\nexit 1' in ຂໍ້ຄວາມ,ຂໍ້ຄວາມ
            ໃຊ້ໄດ້_ລາຍງານ['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.quit(); assert 'FTP stopped' in ເຊລ('ftpd stop')
            assert not ຕົວເຊື່ອມ.ຂໍ້ຜິດພາດ, ຕົວເຊື່ອມ.ຂໍ້ຜິດພາດ
            ໃຊ້ໄດ້_ລາຍງານ.update(passed=True, frames_to_guest=ຕົວເຊື່ອມ.커널수신틀수, frames_from_guest=ຕົວເຊື່ອມ.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in ຕົວ_ໃຊ້_ເລືອກ.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            ຕົວເຊື່ອມ.ຢຸດຊົ່ວຄາວ_ງານ.set()
            ຂະ_ບວນ_ການ.terminate()
            try: ຂະ_ບວນ_ການ.wait(timeout=5)
            except subprocess.TimeoutExpired: ຂະ_ບວນ_ການ.kill(); ຂະ_ບວນ_ການ.wait()
            ຕົວ_ໃຊ້_ເລືອກ.close(); ຂະ_ບວນ_ການ.stdin.close(); ຂະ_ບວນ_ການ.stdout.close()
            ໃຊ້ໄດ້_ລາຍງານ['bridge_error'] = ຕົວເຊື່ອມ.ຂໍ້ຜິດພາດ
            ໃຊ້ໄດ້_ລາຍງານ['frames_to_guest'] = ຕົວເຊື່ອມ.커널수신틀수; ໃຊ້ໄດ້_ລາຍງານ['frames_from_guest'] = ຕົວເຊື່ອມ.커널발신틀수
            (ມາດຕະການ_ຂໍ້ມູນ/'packets.json').write_text(json.dumps(ຕົວເຊື່ອມ.추적기록,indent=2)+'\n')
            (ມາດຕະການ_ຂໍ້ມູນ / 'serial.log').write_bytes(대화기록)
            (ມາດຕະການ_ຂໍ້ມູນ / 'report.json').write_text(json.dumps(ໃຊ້ໄດ້_ລາຍງານ, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': ແລ່ນ()
