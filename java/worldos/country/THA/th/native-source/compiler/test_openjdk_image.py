#!/usr/bin/env python3
"""Execute a source-built host JDK; this is deliberately not a native-kernel test."""
import argparse
import json
from pathlib import Path
import subprocess
from openjdk_probe import digest

SOURCE = r'''
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.net.*;
import java.io.*;
import javax.swing.*;
public class ดั้งเดิม_รุ่น_การทดสอบ {
    public static void main(String[] อาร์กิวเมนต์) throws Exception {
        Path 문서 = Files.createTempFile("한글-", ".txt");
        Files.writeString(문서, "안녕하세요 😀", StandardCharsets.UTF_8);
        if (!Files.readString(문서).equals("안녕하세요 😀")) throw new AssertionError("file");
        Files.delete(문서);
        long หมายเลข = 0x123456789abcdef0L;
        if (Long.reverseBytes(Long.reverseBytes(หมายเลข)) != หมายเลข || Math.sqrt(81.0) != 9.0)
            throw new AssertionError("numeric");
        try (ServerSocket เซิร์ฟเวอร์_ค่า = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Throwable[] ข้อผิดพลาด = new Throwable[1];
            Thread 작업 = new Thread(() -> {
                try (Socket เชื่อมต่อ = new Socket(InetAddress.getLoopbackAddress(), เซิร์ฟเวอร์_ค่า.getLocalPort())) {
                    new DataOutputStream(เชื่อมต่อ.getOutputStream()).writeUTF("한글 소켓");
                } catch (Throwable e) { ข้อผิดพลาด[0] = e; }
            });
            เซิร์ฟเวอร์_ค่า.setSoTimeout(10000); 작업.start();
            try (Socket 받은연결 = เซิร์ฟเวอร์_ค่า.accept()) {
                받은연결.setSoTimeout(10000);
                if (!new DataInputStream(받은연결.getInputStream()).readUTF().equals("한글 소켓"))
                    throw new AssertionError("socket");
            }
            작업.join(10000);
            if (작업.isAlive() || ข้อผิดพลาด[0] != null) throw new AssertionError("thread", ข้อผิดพลาด[0]);
        }
        SwingUtilities.invokeAndWait(() -> {
            boolean[] 눌림 = {false};
            JButton ปุ่ม = new JButton("한글 ปุ่ม");
            ปุ่ม.addActionListener(e -> 눌림[0] = true); ปุ่ม.doClick();
            if (!눌림[0] || !SwingUtilities.isEventDispatchThread()) throw new AssertionError("Swing");
            if (อาร์กิวเมนต์.length != 0) {
                JFrame หน้าต่าง = new JFrame("OpenJDK เอง สร้าง 시험");
                หน้าต่าง.add(ปุ่ม); หน้าต่าง.pack(); หน้าต่าง.setVisible(true); หน้าต่าง.dispose();
            }
        });
        System.out.println("OpenJDK SOURCE SMOKE PASS");
    }
}
'''


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--jdk', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--window', action='store_true', help='Also create a JFrame; requires DISPLAY')
    args = p.parse_args(); jdk = args.jdk.resolve(); out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    report = {'passed': False, 'executed_on': 'build host Linux', 'own_kernel_tested': False,
              'jdk': str(jdk), 'window_tested': args.window,
              'java_sha256': digest(jdk / 'bin/java'), 'libjvm_sha256': digest(jdk / 'lib/server/libjvm.so')}
    path = out / 'report.json'; path.write_text(json.dumps(report, indent=2) + '\n')
    try:
        report['java_version'] = subprocess.check_output([str(jdk / 'bin/java'), '-version'], stderr=subprocess.STDOUT, timeout=30).decode()
        report['javac_version'] = subprocess.check_output([str(jdk / 'bin/javac'), '-version'], stderr=subprocess.STDOUT, timeout=30).decode()
        source = out / 'ดั้งเดิม_รุ่น_การทดสอบ.java'; source.write_text(SOURCE, encoding='utf-8')
        subprocess.check_call([str(jdk / 'bin/javac'), '-encoding', 'UTF-8', '-d', str(out), str(source)], timeout=60)
        cmd = [str(jdk / 'bin/java'), '-Xverify:all', '-Djava.awt.headless=' + ('false' if args.window else 'true'), '-cp', str(out), 'ดั้งเดิม_รุ่น_การทดสอบ']
        if args.window: cmd += ['window']
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=60).decode()
        (out / 'program.log').write_text(result)
        if 'OpenJDK SOURCE SMOKE PASS' not in result: raise RuntimeError(result)
        report.update(passed=True, checks=['source-built java and javac execute', 'long/double and standard library',
            'Unicode file IO', 'native Java Thread plus Linux loopback TCP', 'Swing EDT and ActionListener'])
        if args.window: report['checks'].append('headful JFrame create/show/dispose')
        print(result.strip())
    finally:
        path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': main()
