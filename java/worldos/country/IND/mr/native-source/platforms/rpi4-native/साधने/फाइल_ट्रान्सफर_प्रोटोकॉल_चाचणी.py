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
from संचारजाळे_ब्रिज import संचारजाळे_ब्रिज
from आज्ञा_कार्यवाही_करा import प्रोजेक्ट_मूळ, आदेश
from प्रतिध्वनी_चाचणीसाधन import प्रतिध्वनी_चाचणीसाधन
from ईएलएफ_चाचणी import लिनक्स_उदाहरण


def सुरू_करा():
    मोजमाप_डेटा = प्रोजेक्ट_मूळ / 'build/verification/ftp'; मोजमाप_डेटा.mkdir(parents=True, exist_ok=True)
    पडताळणी_अहवाल = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((प्रोजेक्ट_मूळ / 'build/kernel8.img').read_bytes()).hexdigest()}
    सत्रलेख = bytearray()
    जावा_स्रोत = मोजमाप_डेटा / 'बंडल_चाचणी.java'
    जावा_स्रोत.write_text('public class बंडल_चाचणी { public static void main(String[] बाबी) throws Exception { मराठी.स्वकीय.आउटपुट.ओळ_लिहा("JAR आज्ञा_कार्यवाही_करा: " + बाबी[0]); मराठी.स्वकीय.फाइल.लेखन("jar.txt", "स्वकीय गाभा_मूल्य फाइल"); मराठी.स्वकीय.आउटपुट.ओळ_लिहा(मराठी.स्वकीय.फाइल.वाचन("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(प्रोजेक्ट_मूळ/'build/java-library/classes'), '-d', str(मोजमाप_डेटा), str(जावा_स्रोत)])
    संग्रह = io.BytesIO()
    with zipfile.ZipFile(संग्रह, 'w', zipfile.ZIP_DEFLATED) as जावा_बंडल:
        जावा_बंडल.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: बंडल_चाचणी\r\n\r\n')
        जावा_बंडल.write(str(मोजमाप_डेटा/'बंडल_चाचणी.class'), 'बंडल_चाचणी.class')
    with socket.socket() as तात्पुरते:
        तात्पुरते.bind(('127.0.0.1', 0)); पोर्ट_नंबर = तात्पुरते.getsockname()[1]
    with socket.socket() as तात्पुरते:
        तात्पुरते.bind(('127.0.0.1', 0)); सर्व्हर_प्रवाह_पॉर्ट = तात्पुरते.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as तात्पुरते:
        तात्पुरते.bind(('127.0.0.1', 0)); सर्व्हर_स्वतंत्रसंदेश_पॉर्ट = तात्पुरते.getsockname()[1]
    with संचारजाळे_ब्रिज(पोर्ट_नंबर, ['tcp:{}:9300'.format(सर्व्हर_प्रवाह_पॉर्ट), 'udp:{}:9301'.format(सर्व्हर_स्वतंत्रसंदेश_पॉर्ट)], कॅप्चर_करा=True) as ब्रिज:
        प्रक्रिया = subprocess.Popen(आदेश() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + ब्रिज.अग्रेषित_वितर्क(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        निवडक = selectors.DefaultSelector(); निवडक.register(प्रक्रिया.stdout, selectors.EVENT_READ)
        def संदेश_स्वीकारा(खूण=b'jkoros-native> ', निष्पादन_प्रतीक्षामर्यादा=60):
            डेटा = bytearray(); शेवट_करा_ऑफसेट = time.monotonic() + निष्पादन_प्रतीक्षामर्यादा
            while खूण not in डेटा:
                if time.monotonic() > शेवट_करा_ऑफसेट or प्रक्रिया.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + डेटा.decode('utf-8', 'replace'))
                for दाबलेले_मूल्य, _ in निवडक.select(.1):
                    तुकडा_मूल्य = दाबलेले_मूल्य.fileobj.read(4096)
                    if तुकडा_मूल्य: डेटा.extend(तुकडा_मूल्य); सत्रलेख.extend(तुकडा_मूल्य)
                if b'PANIC:' in डेटा or b'FAIL ' in डेटा: raise AssertionError(डेटा)
            return डेटा.decode('utf-8', 'replace').replace('\r\n', '\n')
        def शेल(ओळ):
            प्रक्रिया.stdin.write(ओळ.encode() + b'\n'); प्रक्रिया.stdin.flush(); return संदेश_स्वीकारा()
        try:
            संदेश_स्वीकारा(); assert 'FTP listening' in शेल('ftpd start')
            संचिका_स्थानांतर_कनेक्शन = ftplib.FTP(); संचिका_स्थानांतर_कनेक्शन.encoding = 'utf-8'; संचिका_स्थानांतर_कनेक्शन.connect('127.0.0.1', पोर्ट_नंबर, timeout=20); संचिका_स्थानांतर_कनेक्शन.login()
            पेलोड_डेटा = bytes(range(256)) * 32
            संचिका_स्थानांतर_कनेक्शन.storbinary('STOR binary.dat', io.BytesIO(पेलोड_डेटा))
            मोजमाप = bytearray(); संचिका_स्थानांतर_कनेक्शन.retrbinary('RETR binary.dat', मोजमाप.extend)
            assert मोजमाप == पेलोड_डेटा; assert संचिका_स्थानांतर_कनेक्शन.size('binary.dat') == len(पेलोड_डेटा)
            पडताळणी_अहवाल['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            संचिका_स्थानांतर_कनेक्शन.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in शेल('cat 한글.txt')
            assert '한글.txt' in संचिका_स्थानांतर_कनेक्शन.nlst()
            assert dict(संचिका_स्थानांतर_कनेक्शन.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            पडताळणी_अहवाल['checks'].append('UTF-8 filename and content visible in guest shell')
            try: संचिका_स्थानांतर_कनेक्शन.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as सहायक_प्रविष्टी: assert str(सहायक_प्रविष्टी).startswith('552'), str(सहायक_प्रविष्टी)
            else: raise AssertionError('oversized upload accepted')
            मोजमाप = bytearray(); संचिका_स्थानांतर_कनेक्शन.retrbinary('RETR binary.dat', मोजमाप.extend); assert मोजमाप == पेलोड_डेटा
            पडताळणी_अहवाल['checks'].append('oversized replacement rejected; previous file preserved')
            with संचिका_स्थानांतर_कनेक्शन.transfercmd('STOR pending.txt') as अपलोड_करा_संचिका:
                # A control command must not change the active upload's destination.
                assert संचिका_स्थानांतर_कनेक्शन.size('binary.dat') == len(पेलोड_डेटा)
                अपलोड_करा_संचिका.sendall(b'UPLOAD TARGET PRESERVED')
            assert संचिका_स्थानांतर_कनेक्शन.voidresp().startswith('226')
            मोजमाप = bytearray(); संचिका_स्थानांतर_कनेक्शन.retrbinary('RETR pending.txt', मोजमाप.extend)
            assert मोजमाप == b'UPLOAD TARGET PRESERVED'
            मोजमाप = bytearray(); संचिका_स्थानांतर_कनेक्शन.retrbinary('RETR binary.dat', मोजमाप.extend)
            assert मोजमाप == पेलोड_डेटा
            संचिका_स्थानांतर_कनेक्शन.delete('pending.txt')
            पडताळणी_अहवाल['checks'].append('interleaved SIZE cannot change the active STOR destination')
            संचिका_स्थानांतर_कनेक्शन.storbinary('STOR अभिवादन_ae353e94.jar', io.BytesIO(संग्रह.getvalue()))
            पाठ्य = शेल('java -jar अभिवादन_ae353e94.jar 누리')
            assert 'JAR आज्ञा_कार्यवाही_करा: 누리' in पाठ्य and 'स्वकीय गाभा_मूल्य फाइल' in पाठ्य and 'exit 0' in पाठ्य, पाठ्य
            पाठ्य = शेल('./अभिवादन_ae353e94.jar 세상')
            assert 'JAR आज्ञा_कार्यवाही_करा: 세상' in पाठ्य and 'exit 0' in पाठ्य, पाठ्य
            पडताळणी_अहवाल['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            मूळ_डेटा = '#include <संचिका_द्विमानजोडणी.h>\nstruct डेटा { int संख्या; double 비율; };\nint बेरीज_मूल्य(int n) { return n ? n + बेरीज_मूल्य(n-1) : 0; }\nint main(void) { struct डेटा मूल्य = {बेरीज_मूल्य(10), 1.25}; if (मूल्य.संख्या != 55 || मूल्य.비율 * 2 != 2.5) return 3; const char अभिवादन_ae353e94[] = "CC NATIVE PASS\\n"; int मार्गदर्शिका = संचिका_उघडा("cc.txt", वाचणे_लिहिणे | जर_अनुपस्थित_तयार_करा | छाटूनरिकामेकरा_सामुग्री, 0600); if (मार्गदर्शिका < 0) return 1; संचिका_डेटा_लिहा(मार्गदर्शिका, अभिवादन_ae353e94, sizeof(अभिवादन_ae353e94)-1); संचिका_मिटवा(मार्गदर्शिका); संचिका_डेटा_लिहा(1, अभिवादन_ae353e94, sizeof(अभिवादन_ae353e94)-1); return 0; }\n'
            संचिका_स्थानांतर_कनेक्शन.storbinary('STOR हांगुल_मजकूर.c', io.BytesIO(मूळ_डेटा.encode()))
            पाठ्य = शेल('cc हांगुल_मजकूर.c -o हांगुल_मजकूर.elf'); assert 'Compiled native ARM64 ELF:' in पाठ्य and 'exit 0' in पाठ्य, पाठ्य
            पाठ्य = शेल('run हांगुल_मजकूर.elf'); assert 'CC NATIVE PASS' in पाठ्य and 'exit 0' in पाठ्य, पाठ्य
            assert 'CC NATIVE PASS' in शेल('cat cc.txt')
            निष्पादनीय_संचिका = bytearray(); संचिका_स्थानांतर_कनेक्शन.retrbinary('RETR हांगुल_मजकूर.elf', निष्पादनीय_संचिका.extend)
            assert निष्पादनीय_संचिका[:4] == b'\x7fELF' and निष्पादनीय_संचिका[18:20] == b'\xb7\x00'
            संचिका_स्थानांतर_कनेक्शन.storbinary('STOR इन्स्टन्स_मूल्य.elf', io.BytesIO(निष्पादनीय_संचिका)); पाठ्य = शेल('run इन्स्टन्स_मूल्य.elf'); assert 'CC NATIVE PASS' in पाठ्य and 'exit 0' in पाठ्य, पाठ्य
            संचिका_स्थानांतर_कनेक्शन.storbinary('STOR आज्ञा_कार्यवाही_करा', io.BytesIO(निष्पादनीय_संचिका)); पाठ्य=शेल('./आज्ञा_कार्यवाही_करा');assert 'CC NATIVE PASS' in पाठ्य and 'exit 0' in पाठ्य,पाठ्य
            संचिका_स्थानांतर_कनेक्शन.storbinary('STOR नाव.txt', io.BytesIO(निष्पादनीय_संचिका)); पाठ्य=शेल('./नाव.txt');assert 'CC NATIVE PASS' in पाठ्य and 'exit 0' in पाठ्य,पाठ्य
            शेल('rm आज्ञा_कार्यवाही_करा नाव.txt')
            पडताळणी_अहवाल['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            शेल('rm binary.dat हांगुल_मजकूर.txt हांगुल_मजकूर.c हांगुल_मजकूर.elf इन्स्टन्स_मूल्य.elf cc.txt jar.txt')
            लिनक्स_संचिका,अपेक्षित=लिनक्स_उदाहरण(मोजमाप_डेटा/'linux-reference')
            संचिका_स्थानांतर_कनेक्शन.storbinary('STOR 리눅스인사',io.BytesIO(लिनक्स_संचिका.read_bytes()))
            पाठ्य=शेल('./리눅스인사');assert 'exit -8' in पाठ्य,पाठ्य
            पाठ्य=शेल('run --linux 리눅스인사 한글인수');assert अपेक्षित+'exit 0' in पाठ्य,पाठ्य
            assert 'LINUX ELF FILE IO' in शेल('cat linux.txt')
            संचिका_स्थानांतर_कनेक्शन.delete('리눅스인사');संचिका_स्थानांतर_कनेक्शन.delete('linux.txt')
            संचिका_स्थानांतर_कनेक्शन.storbinary('STOR असत्य_मूल्य.elf',io.BytesIO(b'plain text'))
            assert '실행할 संख्या 없습니다:' in शेल('./असत्य_मूल्य.elf');संचिका_स्थानांतर_कनेक्शन.delete('असत्य_मूल्य.elf')
            पडताळणी_अहवाल['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with प्रतिध्वनी_चाचणीसाधन() as प्रतिध्वनी_सर्व्हर_प्रविष्टी:
                जाळे_स्रोत = मोजमाप_डेटा/'बाह्य_संचार.java'
                जाळे_स्रोत.write_text('''import java.net.*; import java.io.*;
public class बाह्य_संचार { public static void main(String[] args) throws Exception {
 Socket जोडा = मराठी.स्वकीय.कनेक्शन_वाहतूक.जोडा("10.0.2.2", Integer.parseInt(args[0]));
 जोडा.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] स्रोत = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<स्रोत.length;i++) if (जोडा.getInputStream().read() != (स्रोत[i]&255)) throw new RuntimeException("TCP mismatch");
 जोडा.close();
 DatagramSocket संचारटोक = मराठी.स्वकीय.संचार.उघडा(0); मराठी.स्वकीय.संचार.प्रतीक्षामर्यादा(संचारटोक, 500);
 मराठी.स्वकीय.संचार.पाठवा(संचारटोक, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!मराठी.स्वकीय.संचार.स्वीकारा(संचारटोक).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 संचारटोक.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(प्रोजेक्ट_मूळ/'build/java-library/classes'),'-d',str(मोजमाप_डेटा),str(जाळे_स्रोत)])
                संचिका_स्थानांतर_कनेक्शन.storbinary('STOR बाह्य_संचार.class', io.BytesIO((मोजमाप_डेटा/'बाह्य_संचार.class').read_bytes()))
                पाठ्य = शेल('java बाह्य_संचार {} {}'.format(प्रतिध्वनी_सर्व्हर_प्रविष्टी.ट्रान्समिशन_कंट्रोल_प्रोटोकॉल_पॉर्ट, प्रतिध्वनी_सर्व्हर_प्रविष्टी.स्वतंत्रसंदेशसंचार_पॉर्ट))
                assert 'EXTERNAL TCP UDP PASS' in पाठ्य and '10.0.2.2' in पाठ्य and 'exit 0' in पाठ्य, पाठ्य
                assert प्रतिध्वनी_सर्व्हर_प्रविष्टी.आहे_स्वीकारलेले == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, प्रतिध्वनी_सर्व्हर_प्रविष्टी.आहे_स्वीकारलेले
                assert not प्रतिध्वनी_सर्व्हर_प्रविष्टी.त्रुटी_b805b1b5, प्रतिध्वनी_सर्व्हर_प्रविष्टी.त्रुटी_b805b1b5
            पडताळणी_अहवाल['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            संचिका_स्थानांतर_कनेक्शन.delete('बाह्य_संचार.class')
            सर्व्हर_स्रोत=मोजमाप_डेटा/'सर्व्हर_चाचणी.java'
            सर्व्हर_स्रोत.write_text('''import java.net.*; public class सर्व्हर_चाचणी {
 public static void main(String[] args) throws Exception {
  ServerSocket सर्व्हर_मूल्य = new ServerSocket(9300); DatagramSocket संचारटोक = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket अतिथी_मूल्य = सर्व्हर_मूल्य.accept();
  अतिथी_मूल्य.getOutputStream().write(अतिथी_मूल्य.getInputStream().read()+1); अतिथी_मूल्य.close(); सर्व्हर_मूल्य.close();
  byte[] सामुग्री_मूल्य = new byte[8]; DatagramPacket स्वतंत्रसंदेश = new DatagramPacket(सामुग्री_मूल्य, सामुग्री_मूल्य.length); संचारटोक.receive(स्वतंत्रसंदेश);
  संचारटोक.send(स्वतंत्रसंदेश); संचारटोक.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(मोजमाप_डेटा),str(सर्व्हर_स्रोत)])
            संचिका_स्थानांतर_कनेक्शन.storbinary('STOR सर्व्हर_चाचणी.class',io.BytesIO((मोजमाप_डेटा/'सर्व्हर_चाचणी.class').read_bytes()))
            प्रक्रिया.stdin.write('java सर्व्हर_चाचणी\n'.encode());प्रक्रिया.stdin.flush();संदेश_स्वीकारा(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',सर्व्हर_प्रवाह_पॉर्ट),timeout=5) as समकक्ष_मूल्य:
                समकक्ष_मूल्य.sendall(b'A');assert समकक्ष_मूल्य.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as समकक्ष_मूल्य:
                समकक्ष_मूल्य.settimeout(5);समकक्ष_मूल्य.sendto(b'UDP-IN',('127.0.0.1',सर्व्हर_स्वतंत्रसंदेश_पॉर्ट));assert समकक्ष_मूल्य.recvfrom(512)[0]==b'UDP-IN'
            पाठ्य=संदेश_स्वीकारा();assert 'INBOUND TCP UDP PASS' in पाठ्य and 'exit 0' in पाठ्य,पाठ्य
            पडताळणी_अहवाल['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            संचिका_स्थानांतर_कनेक्शन.delete('सर्व्हर_चाचणी.class')
            निर्देश_क्रम = 'public class रंग { public static void main(String[] बाबी) throws Exception { int बेरीज_मूल्य = 0; int संख्या = 1; while (संख्या <= 10) { बेरीज_मूल्य = बेरीज_मूल्य + संख्या; संख्या = संख्या + 1; } मराठी.स्वकीय.आउटपुट.संख्या_लिहा(बेरीज_मूल्य); मराठी.स्वकीय.फाइल.लेखन("aot.txt", "한글 AOT फाइल 😀"); मराठी.स्वकीय.आउटपुट.ओळ_लिहा(मराठी.स्वकीय.फाइल.वाचन("aot.txt")); } }'
            संचिका_स्थानांतर_कनेक्शन.storbinary('STOR रंग.java', io.BytesIO(निर्देश_क्रम.encode()))
            पाठ्य = शेल('javac रंग.java'); assert 'exit 0' in पाठ्य and 'Compiled:' in पाठ्य, पाठ्य
            पाठ्य = शेल('jaot रंग.class -o रंग.elf'); assert 'AOT compiled native ARM64 ELF:' in पाठ्य and 'exit 0' in पाठ्य, पाठ्य
            पाठ्य = शेल('run रंग.elf'); assert '\n55\n' in पाठ्य and '한글 AOT फाइल 😀' in पाठ्य and 'exit 0' in पाठ्य, पाठ्य
            स्वकीय_fd019377 = bytearray(); संचिका_स्थानांतर_कनेक्शन.retrbinary('RETR रंग.elf', स्वकीय_fd019377.extend)
            पाठ्य = शेल('jaot अभिवादन_ae353e94.jar -o रंग.elf'); assert 'exit 1' in पाठ्य and 'unsupported' in पाठ्य, पाठ्य
            जतनकेलेले_डेटा = bytearray(); संचिका_स्थानांतर_कनेक्शन.retrbinary('RETR रंग.elf', जतनकेलेले_डेटा.extend); assert स्वकीय_fd019377 == जतनकेलेले_डेटा
            बाइटसंहिता = bytearray(); संचिका_स्थानांतर_कनेक्शन.retrbinary('RETR रंग.class', बाइटसंहिता.extend)
            बांधलेले = io.BytesIO()
            with zipfile.ZipFile(बांधलेले, 'w', zipfile.ZIP_DEFLATED) as जावा_बंडल:
                जावा_बंडल.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: रंग\r\n\r\n')
                जावा_बंडल.writestr('रंग.class', बाइटसंहिता)
            संचिका_स्थानांतर_कनेक्शन.storbinary('STOR रंग.jar', io.BytesIO(बांधलेले.getvalue()))
            पाठ्य = शेल('jaot रंग.jar -o रंग.elf'); assert 'AOT compiled native ARM64 ELF:' in पाठ्य and 'exit 0' in पाठ्य, पाठ्य
            पाठ्य = शेल('run रंग.elf'); assert '\n55\n' in पाठ्य and '한글 AOT फाइल 😀' in पाठ्य and 'exit 0' in पाठ्य, पाठ्य
            पडताळणी_अहवाल['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            पडताळणी_अहवाल['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            स्थिर_स्रोत=मोजमाप_डेटा/'स्थिर_चाचणी.java'
            स्थिर_स्रोत.write_text('''public class स्थिर_चाचणी {
 static int प्रोजेक्ट_मूळ = 3;
 static int बेरीज_मूल्य(int n) { return n == 0 ? 0 : n + बेरीज_मूल्य(n-1); }
 public static void main(String[] बाबी) {
  int[] मूल्य = new int[] {प्रोजेक्ट_मूळ, बेरीज_मूल्य(10)};
  System.out.println(मूल्य[0] + मूल्य[1]); System.out.println(बाबी[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(मोजमाप_डेटा),str(स्थिर_स्रोत)])
            संचिका_स्थानांतर_कनेक्शन.storbinary('STOR स्थिर_चाचणी.class',io.BytesIO((मोजमाप_डेटा/'स्थिर_चाचणी.class').read_bytes()))
            पाठ्य=शेल('jaot स्थिर_चाचणी.class -o स्थिर_चाचणी.elf');assert 'exit 0' in पाठ्य,पाठ्य
            पाठ्य=शेल('run स्थिर_चाचणी.elf 한글인수');assert '\n58\n한글인수\nexit 0' in पाठ्य,पाठ्य
            संचिका_स्थानांतर_कनेक्शन.delete('स्थिर_चाचणी.class');संचिका_स्थानांतर_कनेक्शन.delete('स्थिर_चाचणी.elf')
            पडताळणी_अहवाल['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            मोडलेले=bytearray(संग्रह.getvalue());मोडलेले[14]^=1
            संचिका_स्थानांतर_कनेक्शन.storbinary('STOR अभिवादन_ae353e94.jar',io.BytesIO(मोडलेले))
            पाठ्य=शेल('java -jar अभिवादन_ae353e94.jar');assert 'Main-Class\nexit 1' in पाठ्य,पाठ्य
            पडताळणी_अहवाल['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            संचिका_स्थानांतर_कनेक्शन.quit(); assert 'FTP stopped' in शेल('ftpd stop')
            assert not ब्रिज.त्रुटी, ब्रिज.त्रुटी
            पडताळणी_अहवाल.update(passed=True, frames_to_guest=ब्रिज.चौकटी_कडे_अतिथी, frames_from_guest=ब्रिज.चौकटी_पासून_अतिथी)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for दाबलेले_मूल्य,_ in निवडक.select(0):
                तुकडा_मूल्य=दाबलेले_मूल्य.fileobj.read(65536)
                if तुकडा_मूल्य: सत्रलेख.extend(तुकडा_मूल्य)
            ब्रिज.विराम_इव्हेंट.set()
            प्रक्रिया.terminate()
            try: प्रक्रिया.wait(timeout=5)
            except subprocess.TimeoutExpired: प्रक्रिया.kill(); प्रक्रिया.wait()
            निवडक.close(); प्रक्रिया.stdin.close(); प्रक्रिया.stdout.close()
            पडताळणी_अहवाल['bridge_error'] = ब्रिज.त्रुटी
            पडताळणी_अहवाल['frames_to_guest'] = ब्रिज.चौकटी_कडे_अतिथी; पडताळणी_अहवाल['frames_from_guest'] = ब्रिज.चौकटी_पासून_अतिथी
            (मोजमाप_डेटा/'packets.json').write_text(json.dumps(ब्रिज.मागोवा_लॉग,indent=2)+'\n')
            (मोजमाप_डेटा / 'serial.log').write_bytes(सत्रलेख)
            (मोजमाप_डेटा / 'report.json').write_text(json.dumps(पडताळणी_अहवाल, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': सुरू_करा()
