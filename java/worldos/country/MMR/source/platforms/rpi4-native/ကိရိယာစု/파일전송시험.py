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
from ကွန်ရက်တံတား import ကွန်ရက်တံတား
from စက်မောင်း import စီမံကိန်းအမြစ်, အမိန့်
from 되돌림시험서버 import 되돌림시험서버
from ELFစမ်းသပ် import 리눅스예제


def လုပ်ဆောင်():
    ရလဒ်ဒေတာ = စီမံကိန်းအမြစ် / 'build/verification/ftp'; ရလဒ်ဒေတာ.mkdir(parents=True, exist_ok=True)
    검증기록 = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((စီမံကိန်းအမြစ် / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    Javaမူရင်းကုဒ် = ရလဒ်ဒေတာ / 'အထုပ်စမ်းသပ်.java'
    Javaမူရင်းကုဒ်.write_text('public class အထုပ်စမ်းသပ် { public static void main(String[] အချက်များ) throws Exception { မြန်မာ.ကိုယ်ပိုင်.အထွက်.စာကြောင်းထုတ်("JAR စက်မောင်း: " + အချက်များ[0]); မြန်မာ.ကိုယ်ပိုင်.ဖိုင်.ရေး("jar.txt", "ကိုယ်ပိုင် အူတိုင်တန်ဖိုး ဖိုင်"); မြန်မာ.ကိုယ်ပိုင်.အထွက်.စာကြောင်းထုတ်(မြန်မာ.ကိုယ်ပိုင်.ဖိုင်.ဖတ်("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(စီမံကိန်းအမြစ်/'build/java-library/classes'), '-d', str(ရလဒ်ဒေတာ), str(Javaမူရင်းကုဒ်)])
    မော်ကွန်း = io.BytesIO()
    with zipfile.ZipFile(မော်ကွန်း, 'w', zipfile.ZIP_DEFLATED) as Javaအထုပ်:
        Javaအထုပ်.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: အထုပ်စမ်းသပ်\r\n\r\n')
        Javaအထုပ်.write(str(ရလဒ်ဒေတာ/'အထုပ်စမ်းသပ်.class'), 'အထုပ်စမ်းသပ်.class')
    with socket.socket() as ယာယီ:
        ယာယီ.bind(('127.0.0.1', 0)); ဆက်သွယ်ပေါက်ကိန်း = ယာယီ.getsockname()[1]
    with socket.socket() as ယာယီ:
        ယာယီ.bind(('127.0.0.1', 0)); ဝန်ဆောင်စက်စီးကြောင်းဆက်သွယ်ပေါက် = ယာယီ.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as ယာယီ:
        ယာယီ.bind(('127.0.0.1', 0)); ဝန်ဆောင်စက်ဒေတာစာဆက်သွယ်ပေါက် = ယာယီ.getsockname()[1]
    with ကွန်ရက်တံတား(ဆက်သွယ်ပေါက်ကိန်း, ['tcp:{}:9300'.format(ဝန်ဆောင်စက်စီးကြောင်းဆက်သွယ်ပေါက်), 'udp:{}:9301'.format(ဝန်ဆောင်စက်ဒေတာစာဆက်သွယ်ပေါက်)], 포착여부=True) as တံတား:
        실행과정 = subprocess.Popen(အမိန့်() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + တံတား.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        준비선택기 = selectors.DefaultSelector(); 준비선택기.register(실행과정.stdout, selectors.EVENT_READ)
        def စာပို့ချက်လက်ခံရယူ(확인표시=b'jkoros-native> ', လုပ်ဆောင်မှုအချိန်လွန်=60):
            ဒေတာ = bytearray(); အဆုံးအရွေ့ = time.monotonic() + လုပ်ဆောင်မှုအချိန်လွန်
            while 확인표시 not in ဒေတာ:
                if time.monotonic() > အဆုံးအရွေ့ or 실행과정.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + ဒေတာ.decode('utf-8', 'replace'))
                for 누름값, _ in 준비선택기.select(.1):
                    အစိတ်အပိုင်း = 누름값.fileobj.read(4096)
                    if အစိတ်အပိုင်း: ဒေတာ.extend(အစိတ်အပိုင်း); 대화기록.extend(အစိတ်အပိုင်း)
                if b'PANIC:' in ဒေတာ or b'FAIL ' in ဒေတာ: raise AssertionError(ဒေတာ)
            return ဒေတာ.decode('utf-8', 'replace').replace('\r\n', '\n')
        def အမိန့်ဝင်း(စာကြောင်း):
            실행과정.stdin.write(စာကြောင်း.encode() + b'\n'); 실행과정.stdin.flush(); return စာပို့ချက်လက်ခံရယူ()
        try:
            စာပို့ချက်လက်ခံရယူ(); assert 'FTP listening' in အမိန့်ဝင်း('ftpd start')
            ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု = ftplib.FTP(); ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.encoding = 'utf-8'; ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.connect('127.0.0.1', ဆက်သွယ်ပေါက်ကိန်း, timeout=20); ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.login()
            내용자료 = bytes(range(256)) * 32
            ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.storbinary('STOR binary.dat', io.BytesIO(내용자료))
            ရလဒ် = bytearray(); ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.retrbinary('RETR binary.dat', ရလဒ်.extend)
            assert ရလဒ် == 내용자료; assert ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.size('binary.dat') == len(내용자료)
            검증기록['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in အမိန့်ဝင်း('cat 한글.txt')
            assert '한글.txt' in ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.nlst()
            assert dict(ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            검증기록['checks'].append('UTF-8 filename and content visible in guest shell')
            try: ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            ရလဒ် = bytearray(); ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.retrbinary('RETR binary.dat', ရလဒ်.extend); assert ရလဒ် == 내용자료
            검증기록['checks'].append('oversized replacement rejected; previous file preserved')
            with ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.transfercmd('STOR pending.txt') as ဖိုင်တင်:
                # A control command must not change the active upload's destination.
                assert ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.size('binary.dat') == len(내용자료)
                ဖိုင်တင်.sendall(b'UPLOAD TARGET PRESERVED')
            assert ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.voidresp().startswith('226')
            ရလဒ် = bytearray(); ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.retrbinary('RETR pending.txt', ရလဒ်.extend)
            assert ရလဒ် == b'UPLOAD TARGET PRESERVED'
            ရလဒ် = bytearray(); ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.retrbinary('RETR binary.dat', ရလဒ်.extend)
            assert ရလဒ် == 내용자료
            ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.delete('pending.txt')
            검증기록['checks'].append('interleaved SIZE cannot change the active STOR destination')
            ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.storbinary('STOR နှုတ်ဆက်.jar', io.BytesIO(မော်ကွန်း.getvalue()))
            စာသား = အမိန့်ဝင်း('java -jar နှုတ်ဆက်.jar 누리')
            assert 'JAR စက်မောင်း: 누리' in စာသား and 'ကိုယ်ပိုင် အူတိုင်တန်ဖိုး ဖိုင်' in စာသား and 'exit 0' in စာသား, စာသား
            စာသား = အမိန့်ဝင်း('./နှုတ်ဆက်.jar 세상')
            assert 'JAR စက်မောင်း: 세상' in စာသား and 'exit 0' in စာသား, စာသား
            검증기록['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            မူရင်းဒေတာ = '#include <파일규약.h>\nstruct ဒေတာ { int ကိန်းတန်ဖိုး; double 비율; };\nint စုစုပေါင်းတန်ဖိုး(int n) { return n ? n + စုစုပေါင်းတန်ဖိုး(n-1) : 0; }\nint main(void) { struct ဒေတာ တန်ဖိုး = {စုစုပေါင်းတန်ဖိုး(10), 1.25}; if (တန်ဖိုး.ကိန်းတန်ဖိုး != 55 || တန်ဖိုး.비율 * 2 != 2.5) return 3; const char နှုတ်ဆက်[] = "CC NATIVE PASS\\n"; int စာတမ်း = ဖိုင်ဖွင့်("cc.txt", ဖတ်ရေး | 없으면만들기 | 내용비우기, 0600); if (စာတမ်း < 0) return 1; ဖိုင်ဒေတာရေး(စာတမ်း, နှုတ်ဆက်, sizeof(နှုတ်ဆက်)-1); ဖိုင်ပိတ်(စာတမ်း); ဖိုင်ဒေတာရေး(1, နှုတ်ဆက်, sizeof(နှုတ်ဆက်)-1); return 0; }\n'
            ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.storbinary('STOR ဟန်ဂုစာသား.c', io.BytesIO(မူရင်းဒေတာ.encode()))
            စာသား = အမိန့်ဝင်း('cc ဟန်ဂုစာသား.c -o ဟန်ဂုစာသား.elf'); assert 'Compiled native ARM64 ELF:' in စာသား and 'exit 0' in စာသား, စာသား
            စာသား = အမိန့်ဝင်း('run ဟန်ဂုစာသား.elf'); assert 'CC NATIVE PASS' in စာသား and 'exit 0' in စာသား, စာသား
            assert 'CC NATIVE PASS' in အမိန့်ဝင်း('cat cc.txt')
            စက်ဖိုင်ဖိုင် = bytearray(); ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.retrbinary('RETR ဟန်ဂုစာသား.elf', စက်ဖိုင်ဖိုင်.extend)
            assert စက်ဖိုင်ဖိုင်[:4] == b'\x7fELF' and စက်ဖိုင်ဖိုင်[18:20] == b'\xb7\x00'
            ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.storbinary('STOR တန်ဖိုးမိတ္တူကူး.elf', io.BytesIO(စက်ဖိုင်ဖိုင်)); စာသား = အမိန့်ဝင်း('run တန်ဖိုးမိတ္တူကူး.elf'); assert 'CC NATIVE PASS' in စာသား and 'exit 0' in စာသား, စာသား
            ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.storbinary('STOR စက်မောင်း', io.BytesIO(စက်ဖိုင်ဖိုင်)); စာသား=အမိန့်ဝင်း('./စက်မောင်း');assert 'CC NATIVE PASS' in စာသား and 'exit 0' in စာသား,စာသား
            ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.storbinary('STOR အမည်.txt', io.BytesIO(စက်ဖိုင်ဖိုင်)); စာသား=အမိန့်ဝင်း('./အမည်.txt');assert 'CC NATIVE PASS' in စာသား and 'exit 0' in စာသား,စာသား
            အမိန့်ဝင်း('rm စက်မောင်း အမည်.txt')
            검증기록['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            အမိန့်ဝင်း('rm binary.dat ဟန်ဂုစာသား.txt ဟန်ဂုစာသား.c ဟန်ဂုစာသား.elf တန်ဖိုးမိတ္တူကူး.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(ရလဒ်ဒေတာ/'linux-reference')
            ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            စာသား=အမိန့်ဝင်း('./리눅스인사');assert 'exit -8' in စာသား,စာသား
            စာသား=အမိန့်ဝင်း('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in စာသား,စာသား
            assert 'LINUX ELF FILE IO' in အမိန့်ဝင်း('cat linux.txt')
            ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.delete('리눅스인사');ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.delete('linux.txt')
            ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.storbinary('STOR မှားတန်ဖိုး.elf',io.BytesIO(b'plain text'))
            assert '실행할 ကိန်းတန်ဖိုး 없습니다:' in အမိန့်ဝင်း('./မှားတန်ဖိုး.elf');ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.delete('မှားတန်ဖိုး.elf')
            검증기록['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as ပြန်ပို့ဝန်ဆောင်စက်အချက်:
                통신원문 = ရလဒ်ဒေတာ/'ပြင်ပဆက်သွယ်မှု.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class ပြင်ပဆက်သွယ်မှု { public static void main(String[] args) throws Exception {
 Socket ချိတ်ဆက် = မြန်မာ.ကိုယ်ပိုင်.ချိတ်ဆက်သယ်ပို့.ချိတ်ဆက်("10.0.2.2", Integer.parseInt(args[0]));
 ချိတ်ဆက်.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] မူရင်းကုဒ် = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<မူရင်းကုဒ်.length;i++) if (ချိတ်ဆက်.getInputStream().read() != (မူရင်းကုဒ်[i]&255)) throw new RuntimeException("TCP mismatch");
 ချိတ်ဆက်.close();
 DatagramSocket ဆုံးမှတ် = မြန်မာ.ကိုယ်ပိုင်.ဆက်သွယ်မှု.ဖွင့်(0); မြန်မာ.ကိုယ်ပိုင်.ဆက်သွယ်မှု.စောင့်ချိန်(ဆုံးမှတ်, 500);
 မြန်မာ.ကိုယ်ပိုင်.ဆက်သွယ်မှု.ပို့(ဆုံးမှတ်, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!မြန်မာ.ကိုယ်ပိုင်.ဆက်သွယ်မှု.လက်ခံ(ဆုံးမှတ်).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 ဆုံးမှတ်.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(စီမံကိန်းအမြစ်/'build/java-library/classes'),'-d',str(ရလဒ်ဒေတာ),str(통신원문)])
                ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.storbinary('STOR ပြင်ပဆက်သွယ်မှု.class', io.BytesIO((ရလဒ်ဒေတာ/'ပြင်ပဆက်သွယ်မှု.class').read_bytes()))
                စာသား = အမိန့်ဝင်း('java ပြင်ပဆက်သွယ်မှု {} {}'.format(ပြန်ပို့ဝန်ဆောင်စက်အချက်.TCPဆက်သွယ်ပေါက်, ပြန်ပို့ဝန်ဆောင်စက်အချက်.UDPဆက်သွယ်ပေါက်))
                assert 'EXTERNAL TCP UDP PASS' in စာသား and '10.0.2.2' in စာသား and 'exit 0' in စာသား, စာသား
                assert ပြန်ပို့ဝန်ဆောင်စက်အချက်.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, ပြန်ပို့ဝန်ဆောင်စက်အချက်.수신됨
                assert not ပြန်ပို့ဝန်ဆောင်စက်အချက်.အမှားများ, ပြန်ပို့ဝန်ဆောင်စက်အချက်.အမှားများ
            검증기록['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.delete('ပြင်ပဆက်သွယ်မှု.class')
            ဝန်ဆောင်စက်မူရင်းကုဒ်=ရလဒ်ဒေတာ/'ဝန်ဆောင်စက်စမ်းသပ်.java'
            ဝန်ဆောင်စက်မူရင်းကုဒ်.write_text('''import java.net.*; public class ဝန်ဆောင်စက်စမ်းသပ် {
 public static void main(String[] args) throws Exception {
  ServerSocket ဝန်ဆောင်စက်တန်ဖိုး = new ServerSocket(9300); DatagramSocket ဆုံးမှတ် = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket ဧည့်သည်တန်ဖိုး = ဝန်ဆောင်စက်တန်ဖိုး.accept();
  ဧည့်သည်တန်ဖိုး.getOutputStream().write(ဧည့်သည်တန်ဖိုး.getInputStream().read()+1); ဧည့်သည်တန်ဖိုး.close(); ဝန်ဆောင်စက်တန်ဖိုး.close();
  byte[] အကြောင်းအရာတန်ဖိုး = new byte[8]; DatagramPacket ဒေတာစာ = new DatagramPacket(အကြောင်းအရာတန်ဖိုး, အကြောင်းအရာတန်ဖိုး.length); ဆုံးမှတ်.receive(ဒေတာစာ);
  ဆုံးမှတ်.send(ဒေတာစာ); ဆုံးမှတ်.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(ရလဒ်ဒေတာ),str(ဝန်ဆောင်စက်မူရင်းကုဒ်)])
            ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.storbinary('STOR ဝန်ဆောင်စက်စမ်းသပ်.class',io.BytesIO((ရလဒ်ဒေတာ/'ဝန်ဆောင်စက်စမ်းသပ်.class').read_bytes()))
            실행과정.stdin.write('java ဝန်ဆောင်စက်စမ်းသပ်\n'.encode());실행과정.stdin.flush();စာပို့ချက်လက်ခံရယူ(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',ဝန်ဆောင်စက်စီးကြောင်းဆက်သွယ်ပေါက်),timeout=5) as တစ်ဖက်တန်ဖိုး:
                တစ်ဖက်တန်ဖိုး.sendall(b'A');assert တစ်ဖက်တန်ဖိုး.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as တစ်ဖက်တန်ဖိုး:
                တစ်ဖက်တန်ဖိုး.settimeout(5);တစ်ဖက်တန်ဖိုး.sendto(b'UDP-IN',('127.0.0.1',ဝန်ဆောင်စက်ဒေတာစာဆက်သွယ်ပေါက်));assert တစ်ဖက်တန်ဖိုး.recvfrom(512)[0]==b'UDP-IN'
            စာသား=စာပို့ချက်လက်ခံရယူ();assert 'INBOUND TCP UDP PASS' in စာသား and 'exit 0' in စာသား,စာသား
            검증기록['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.delete('ဝန်ဆောင်စက်စမ်းသပ်.class')
            စက်ညွှန်ကြားချက်အစဉ်လိုက် = 'public class အလင်း { public static void main(String[] အချက်များ) throws Exception { int စုစုပေါင်းတန်ဖိုး = 0; int ကိန်းတန်ဖိုး = 1; while (ကိန်းတန်ဖိုး <= 10) { စုစုပေါင်းတန်ဖိုး = စုစုပေါင်းတန်ဖိုး + ကိန်းတန်ဖိုး; ကိန်းတန်ဖိုး = ကိန်းတန်ဖိုး + 1; } မြန်မာ.ကိုယ်ပိုင်.အထွက်.ကိန်းထုတ်(စုစုပေါင်းတန်ဖိုး); မြန်မာ.ကိုယ်ပိုင်.ဖိုင်.ရေး("aot.txt", "한글 AOT ဖိုင် 😀"); မြန်မာ.ကိုယ်ပိုင်.အထွက်.စာကြောင်းထုတ်(မြန်မာ.ကိုယ်ပိုင်.ဖိုင်.ဖတ်("aot.txt")); } }'
            ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.storbinary('STOR အလင်း.java', io.BytesIO(စက်ညွှန်ကြားချက်အစဉ်လိုက်.encode()))
            စာသား = အမိန့်ဝင်း('javac အလင်း.java'); assert 'exit 0' in စာသား and 'Compiled:' in စာသား, စာသား
            စာသား = အမိန့်ဝင်း('jaot အလင်း.class -o အလင်း.elf'); assert 'AOT compiled native ARM64 ELF:' in စာသား and 'exit 0' in စာသား, စာသား
            စာသား = အမိန့်ဝင်း('run အလင်း.elf'); assert '\n55\n' in စာသား and '한글 AOT ဖိုင် 😀' in စာသား and 'exit 0' in စာသား, စာသား
            ကိုယ်ပိုင်စက်ဖိုင် = bytearray(); ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.retrbinary('RETR အလင်း.elf', ကိုယ်ပိုင်စက်ဖိုင်.extend)
            စာသား = အမိန့်ဝင်း('jaot နှုတ်ဆက်.jar -o အလင်း.elf'); assert 'exit 1' in စာသား and 'unsupported' in စာသား, စာသား
            보존자료 = bytearray(); ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.retrbinary('RETR အလင်း.elf', 보존자료.extend); assert ကိုယ်ပိုင်စက်ဖိုင် == 보존자료
            ဘိုက်ကုဒ် = bytearray(); ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.retrbinary('RETR အလင်း.class', ဘိုက်ကုဒ်.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as Javaအထုပ်:
                Javaအထုပ်.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: အလင်း\r\n\r\n')
                Javaအထုပ်.writestr('အလင်း.class', ဘိုက်ကုဒ်)
            ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.storbinary('STOR အလင်း.jar', io.BytesIO(묶인자료.getvalue()))
            စာသား = အမိန့်ဝင်း('jaot အလင်း.jar -o အလင်း.elf'); assert 'AOT compiled native ARM64 ELF:' in စာသား and 'exit 0' in စာသား, စာသား
            စာသား = အမိန့်ဝင်း('run အလင်း.elf'); assert '\n55\n' in စာသား and '한글 AOT ဖိုင် 😀' in စာသား and 'exit 0' in စာသား, စာသား
            검증기록['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            검증기록['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            တည်ငြိမ်မူရင်းကုဒ်=ရလဒ်ဒေတာ/'တည်ငြိမ်စမ်းသပ်.java'
            တည်ငြိမ်မူရင်းကုဒ်.write_text('''public class တည်ငြိမ်စမ်းသပ် {
 static int စီမံကိန်းအမြစ် = 3;
 static int စုစုပေါင်းတန်ဖိုး(int n) { return n == 0 ? 0 : n + စုစုပေါင်းတန်ဖိုး(n-1); }
 public static void main(String[] အချက်များ) {
  int[] တန်ဖိုး = new int[] {စီမံကိန်းအမြစ်, စုစုပေါင်းတန်ဖိုး(10)};
  System.out.println(တန်ဖိုး[0] + တန်ဖိုး[1]); System.out.println(အချက်များ[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(ရလဒ်ဒေတာ),str(တည်ငြိမ်မူရင်းကုဒ်)])
            ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.storbinary('STOR တည်ငြိမ်စမ်းသပ်.class',io.BytesIO((ရလဒ်ဒေတာ/'တည်ငြိမ်စမ်းသပ်.class').read_bytes()))
            စာသား=အမိန့်ဝင်း('jaot တည်ငြိမ်စမ်းသပ်.class -o တည်ငြိမ်စမ်းသပ်.elf');assert 'exit 0' in စာသား,စာသား
            စာသား=အမိန့်ဝင်း('run တည်ငြိမ်စမ်းသပ်.elf 한글인수');assert '\n58\n한글인수\nexit 0' in စာသား,စာသား
            ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.delete('တည်ငြိမ်စမ်းသပ်.class');ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.delete('တည်ငြိမ်စမ်းသပ်.elf')
            검증기록['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(မော်ကွန်း.getvalue());손상자료[14]^=1
            ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.storbinary('STOR နှုတ်ဆက်.jar',io.BytesIO(손상자료))
            စာသား=အမိန့်ဝင်း('java -jar နှုတ်ဆက်.jar');assert 'Main-Class\nexit 1' in စာသား,စာသား
            검증기록['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            ဖိုင်လွှဲပြောင်းချိတ်ဆက်မှု.quit(); assert 'FTP stopped' in အမိန့်ဝင်း('ftpd stop')
            assert not တံတား.အမှား, တံတား.အမှား
            검증기록.update(passed=True, frames_to_guest=တံတား.커널수신틀수, frames_from_guest=တံတား.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in 준비선택기.select(0):
                အစိတ်အပိုင်း=누름값.fileobj.read(65536)
                if အစိတ်အပိုင်း: 대화기록.extend(အစိတ်အပိုင်း)
            တံတား.ခဏရပ်ဖြစ်ရပ်.set()
            실행과정.terminate()
            try: 실행과정.wait(timeout=5)
            except subprocess.TimeoutExpired: 실행과정.kill(); 실행과정.wait()
            준비선택기.close(); 실행과정.stdin.close(); 실행과정.stdout.close()
            검증기록['bridge_error'] = တံတား.အမှား
            검증기록['frames_to_guest'] = တံတား.커널수신틀수; 검증기록['frames_from_guest'] = တံတား.커널발신틀수
            (ရလဒ်ဒေတာ/'packets.json').write_text(json.dumps(တံတား.ခြေရာမှတ်တမ်း,indent=2)+'\n')
            (ရလဒ်ဒေတာ / 'serial.log').write_bytes(대화기록)
            (ရလဒ်ဒေတာ / 'report.json').write_text(json.dumps(검증기록, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': လုပ်ဆောင်()
