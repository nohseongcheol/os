#!/usr/bin/env python3
"""ARM64 C 후단의 Java 의미를 OpenJDK ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ 결과와 비교한다.

ਅਸਲ_ਸਮੱਗਰੀ ARM64 ABI/ਤਜਵੀਜ_ਕੀਮਤ 부팅 시험은 platforms/rpi4-native/tools/test_boot.py에 있다.
"""
from pathlib import Path
import subprocess
import tempfile
import unittest
from arm64 import ARM64
from 컴파일러 import ਸ੍ਰੇਣੀ_ਕੀਮਤ, 컴파일오류

ROOT = Path(__file__).resolve().parent
SOURCE = r'''
final class State { static int count; static int value = initialize();
    static int initialize() { count++; return 23; }
}
public final class Sample {
    static int seed = 17;
    static int mix(int x, int y) {
        int v = x * 1103515245 + y;
        v ^= (v << (y & 63)) | (v >>> (y & 63));
        v += v >> ((y + 1) & 63);
        v ^= (byte)v; v += (short)x; v -= (char)y;
        return v;
    }
    static int sparse(int x) {
        switch (x) { case -100: return 11; case 99: return 17; case 10000: return 23; default: return 41; }
    }
    static int dense(int x) {
        switch (x) { case 0: return 7; case 1: return 9; case 2: return 13; case 3: return 17; default: return 19; }
    }
    static int[] echo(int[] a) { return a; }
    public static int entry() {
        int v = seed;
        for (int i = -40; i <= 40; i++) v = mix(v, i);
        int min = -2147483648, neg = -1;
        v ^= min / neg; v += min % neg;
        int[] a = new int[5];
        for (int i = 0; i < a.length; i++) a[i] = i * v;
        a[2]++; a[3] += 19;
        int[] b = echo(a), empty = null;
        if (a != b || empty != null || b == null) return 1001;
        if (a[0] != 0 || State.count != 1 || State.value != 23) return 1002;
        String s = "한글 😀";
        v += s.length() + s.charAt(0) + s.charAt(3);
        return v ^ a[2] ^ a[3] ^ sparse(-100) ^ sparse(99) ^ sparse(3) ^ dense(2) ^ dense(8);
    }
}
'''
HARNESS = r'''
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
extern int32_t java_entry(void);
void kernel_panic(const char *why) { fprintf(stderr, "PANIC: %s\n", why); exit(73); }
int main(void) { printf("%d\n", java_entry()); return 0; }
'''


class BackendTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='arm64-compiler-')
        self.path = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)

    def compile_java(self, source, driver=False):
        (self.path / 'Sample.java').write_text(source, encoding='utf-8')
        sources = [str(self.path / 'Sample.java')]
        if driver:
            (self.path / 'Driver.java').write_text('public class Driver { public static void main(String[] args) { System.out.println(Sample.entry()); } }')
            sources.append(str(self.path / 'Driver.java'))
        subprocess.check_call(['javac', '--release', '8', '-proc:none', '-encoding', 'UTF-8', '-d', str(self.path)] + sources)
        return [ਸ੍ਰੇਣੀ_ਕੀਮਤ(p) for p in sorted(self.path.glob('*.class')) if p.name != 'Driver.class']

    def run_generated(self, classes):
        output = ARM64(classes).generate('Sample.entry', [])
        (self.path / 'generated.c').write_text(output, encoding='utf-8')
        (self.path / 'harness.c').write_text(HARNESS)
        subprocess.check_call(['gcc', '-std=c11', '-O2', '-fPIE', '-pie', '-fsanitize=undefined',
            '-fno-sanitize-recover=all', str(self.path / 'generated.c'), str(self.path / 'harness.c'), '-o', str(self.path / 'program')])
        return subprocess.run([str(self.path / 'program')], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def test_matches_openjdk(self):
        classes = self.compile_java(SOURCE, driver=True)
        expected = subprocess.check_output(['java', '-cp', str(self.path), 'Driver'])
        actual = self.run_generated(classes)
        self.assertEqual(actual.returncode, 0, actual.stderr)
        self.assertEqual(actual.stdout, expected)

    def test_runtime_faults(self):
        fixtures = [
            ('int[] a = new int[1]; return a[1];', b'array bounds'),
            ('int[] a = null; return a.length;', b'null reference'),
            ('int zero = 0; return 3 / zero;', b'division by zero'),
            ('int n = -1; int[] a = new int[n]; return a.length;', b'array allocation')]
        for body, message in fixtures:
            with self.subTest(message=message):
                classes = self.compile_java('public final class Sample { public static int entry() {' + body + '} }')
                result = self.run_generated(classes)
                self.assertEqual(result.returncode, 73, result.stderr)
                self.assertIn(message, result.stderr)

    def test_unsupported_programs_fail(self):
        fixtures = [
            'public static int entry() { Object a = new Object(); return 0; }',
            'public static long entry() { return 1L; }',
            'public static int entry() { try { int[] a = null; return a.length; } catch (Exception e) { return 0; } }',
            'public static native int escape(); public static int entry() { return escape(); }']
        for methods in fixtures:
            with self.subTest(methods=methods):
                with self.assertRaises(컴파일오류):
                    ARM64(self.compile_java('public final class Sample {' + methods + '}')).generate('Sample.entry', [])

    def test_native_profiles_are_separate(self):
        classes = self.compile_java('final class ਬੋਰਡ { static native int 직렬읽기(); } '
            'public final class Sample { public static int entry() { return ਬੋਰਡ.직렬읽기(); } }')
        ARM64(classes, 'kernel').generate('Sample.entry', [])
        with self.assertRaises(컴파일오류):
            ARM64(classes, 'user').generate('Sample.entry', [])
        self.path = self.path / 'user'; self.path.mkdir()
        classes = self.compile_java('final class ਉਪਭੋਗਤਾ { static native int 도구번호(); } '
            'public final class Sample { public static int entry() { return ਉਪਭੋਗਤਾ.도구번호(); } }')
        ARM64(classes, 'user').generate('Sample.entry', [])
        with self.assertRaises(컴파일오류):
            ARM64(classes, 'kernel').generate('Sample.entry', [])


if __name__ == '__main__':
    unittest.main()
