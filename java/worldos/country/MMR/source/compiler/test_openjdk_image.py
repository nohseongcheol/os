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
public class ကိုယ်ပိုင်တည်ဆောက်စမ်းသပ် {
    public static void main(String[] အချက်များ) throws Exception {
        Path စာတမ်း = Files.createTempFile("한글-", ".txt");
        Files.writeString(စာတမ်း, "안녕하세요 😀", StandardCharsets.UTF_8);
        if (!Files.readString(စာတမ်း).equals("안녕하세요 😀")) throw new AssertionError("file");
        Files.delete(စာတမ်း);
        long ကိန်းတန်ဖိုး = 0x123456789abcdef0L;
        if (Long.reverseBytes(Long.reverseBytes(ကိန်းတန်ဖိုး)) != ကိန်းတန်ဖိုး || Math.sqrt(81.0) != 9.0)
            throw new AssertionError("numeric");
        try (ServerSocket ဝန်ဆောင်စက်တန်ဖိုး = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Throwable[] အမှား = new Throwable[1];
            Thread အလုပ် = new Thread(() -> {
                try (Socket ချိတ်ဆက် = new Socket(InetAddress.getLoopbackAddress(), ဝန်ဆောင်စက်တန်ဖိုး.getLocalPort())) {
                    new DataOutputStream(ချိတ်ဆက်.getOutputStream()).writeUTF("한글 ကွန်ရက်ပေါက်တန်ဖိုး");
                } catch (Throwable e) { အမှား[0] = e; }
            });
            ဝန်ဆောင်စက်တန်ဖိုး.setSoTimeout(10000); အလုပ်.start();
            try (Socket 받은연결 = ဝန်ဆောင်စက်တန်ဖိုး.accept()) {
                받은연결.setSoTimeout(10000);
                if (!new DataInputStream(받은연결.getInputStream()).readUTF().equals("한글 ကွန်ရက်ပေါက်တန်ဖိုး"))
                    throw new AssertionError("socket");
            }
            အလုပ်.join(10000);
            if (အလုပ်.isAlive() || အမှား[0] != null) throw new AssertionError("thread", အမှား[0]);
        }
        SwingUtilities.invokeAndWait(() -> {
            boolean[] 눌림 = {false};
            JButton ခလုတ် = new JButton("한글 ခလုတ်");
            ခလုတ်.addActionListener(e -> 눌림[0] = true); ခလုတ်.doClick();
            if (!눌림[0] || !SwingUtilities.isEventDispatchThread()) throw new AssertionError("Swing");
            if (အချက်များ.length != 0) {
                JFrame ဝင်း = new JFrame("OpenJDK ကိုယ်ပိုင် တည်ဆောက် စမ်းသပ်မှု");
                ဝင်း.add(ခလုတ်); ဝင်း.pack(); ဝင်း.setVisible(true); ဝင်း.dispose();
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
        source = out / 'ကိုယ်ပိုင်တည်ဆောက်စမ်းသပ်.java'; source.write_text(SOURCE, encoding='utf-8')
        subprocess.check_call([str(jdk / 'bin/javac'), '-encoding', 'UTF-8', '-d', str(out), str(source)], timeout=60)
        cmd = [str(jdk / 'bin/java'), '-Xverify:all', '-Djava.awt.headless=' + ('false' if args.window else 'true'), '-cp', str(out), 'ကိုယ်ပိုင်တည်ဆောက်စမ်းသပ်']
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
