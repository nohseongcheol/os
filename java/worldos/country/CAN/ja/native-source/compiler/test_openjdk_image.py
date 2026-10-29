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
public class 自前構築試験 {
    public static void main(String[] 引数) throws Exception {
        Path 文書 = Files.createTempFile("한글-", ".txt");
        Files.writeString(文書, "안녕하세요 😀", StandardCharsets.UTF_8);
        if (!Files.readString(文書).equals("안녕하세요 😀")) throw new AssertionError("file");
        Files.delete(文書);
        long 数 = 0x123456789abcdef0L;
        if (Long.reverseBytes(Long.reverseBytes(数)) != 数 || Math.sqrt(81.0) != 9.0)
            throw new AssertionError("numeric");
        try (ServerSocket サーバー値 = new ServerSocket(0, 1, InetAddress.getLoopbackAddress())) {
            Throwable[] エラー = new Throwable[1];
            Thread 作業 = new Thread(() -> {
                try (Socket 接続 = new Socket(InetAddress.getLoopbackAddress(), サーバー値.getLocalPort())) {
                    new DataOutputStream(接続.getOutputStream()).writeUTF("한글 ソケット値");
                } catch (Throwable e) { エラー[0] = e; }
            });
            サーバー値.setSoTimeout(10000); 作業.start();
            try (Socket 受理済み接続状態 = サーバー値.accept()) {
                受理済み接続状態.setSoTimeout(10000);
                if (!new DataInputStream(受理済み接続状態.getInputStream()).readUTF().equals("한글 ソケット値"))
                    throw new AssertionError("socket");
            }
            作業.join(10000);
            if (作業.isAlive() || エラー[0] != null) throw new AssertionError("thread", エラー[0]);
        }
        SwingUtilities.invokeAndWait(() -> {
            boolean[] 判定押下済み = {false};
            JButton ボタン = new JButton("한글 ボタン");
            ボタン.addActionListener(e -> 判定押下済み[0] = true); ボタン.doClick();
            if (!判定押下済み[0] || !SwingUtilities.isEventDispatchThread()) throw new AssertionError("Swing");
            if (引数.length != 0) {
                JFrame 窓 = new JFrame("OpenJDK 内蔵 システム構築 試験");
                窓.add(ボタン); 窓.pack(); 窓.setVisible(true); 窓.dispose();
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
        source = out / '自前構築試験.java'; source.write_text(SOURCE, encoding='utf-8')
        subprocess.check_call([str(jdk / 'bin/javac'), '-encoding', 'UTF-8', '-d', str(out), str(source)], timeout=60)
        cmd = [str(jdk / 'bin/java'), '-Xverify:all', '-Djava.awt.headless=' + ('false' if args.window else 'true'), '-cp', str(out), '自前構築試験']
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
