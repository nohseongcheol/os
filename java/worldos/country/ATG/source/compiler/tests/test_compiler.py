"""actualData ELF executeCommand + OpenJDK result 대조. temporaryValue tests 자료만 생성한다."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

Compiler = Path(__file__).resolve().parents[1] / 'Compiler.py'


class testNative(unittest.TestCase):
    def setUp(self):
        self.temporaryValue = tempfile.TemporaryDirectory(prefix='jkoros-compiler-test-')
        self.addCleanup(self.temporaryValue.cleanup)
        self.directoryValue = Path(self.temporaryValue.name)

    def compileSource(self, source, appendEntry=None, successValue=True, targetValue='linux', exportedValue=None):
        pathList = []
        for name, contentValue in dict({'tests': source}, **(appendEntry or {})).items():
            path = self.directoryValue / (name + '.java')
            path.write_text(contentValue, encoding='utf-8')
            pathList.append(str(path))
        command = [sys.executable, str(Compiler), '--target', targetValue, '--entry', 'tests.run', '-o', str(self.directoryValue / 'native')]
        if exportedValue is not None: command += ['--export', exportedValue]
        result = subprocess.run(command + pathList,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if successValue:
            self.assertEqual(result.returncode, 0, result.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('compileSource error'.encode(), result.stderr)
        return result

    def executionResult(self):
        return subprocess.run([str(self.directoryValue / 'native')], timeout=5).returncode

    def javaComparison(self, source, appendEntry=None):
        self.compileSource(source, appendEntry)
        (self.directoryValue / 'Host.java').write_text(
            'public class Host { public static void main(String[] arguments) { System.exit(tests.run()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.directoryValue)] +
                       [str(path) for path in self.directoryValue.glob('*.java')], check=True, timeout=30)
        expectation = subprocess.run(['java', '-cp', str(self.directoryValue), 'Host'], timeout=5).returncode
        actualData = self.executionResult()
        self.assertGreaterEqual(actualData, 0, '신호로 hasExited (샌드박스의 32비트 syscall limitValue 여부 verify)')
        self.assertEqual(actualData, expectation)

    def test_integer_arithmetic_and_shifts(self):
        self.javaComparison('''public class tests {
            static int mixArithmetic(int firstOperand, int secondOperand) {
                return ((firstOperand + secondOperand) ^ (firstOperand - secondOperand) ^ (firstOperand * secondOperand) ^ (firstOperand & secondOperand) ^ (firstOperand | secondOperand))
                    + (firstOperand << secondOperand) + (firstOperand >> secondOperand) + (firstOperand >>> secondOperand);
            }
            public static int run() {
                int sumValue = 7;
                int value = 12345;
                for (int index = -65; index <= 65; index++) {
                    value = value * 1664525 + 1013904223;
                    sumValue = sumValue * 31 + mixArithmetic(value, index);
                    sumValue += (byte)value + (short)value + (char)value;
                }
                return (sumValue & 0x7fffffff) % 251;
            }
        }''')

    def test_division_extreme_values(self):
        self.javaComparison('''public class tests {
            static int[] value = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int run() {
                int sumValue = 13;
                for (int firstOperand = 0; firstOperand < value.length; firstOperand++)
                    for (int secondOperand = 1; secondOperand < value.length; secondOperand++)
                        sumValue = sumValue * 31 + value[firstOperand] / value[secondOperand] + value[firstOperand] % value[secondOperand];
                return (sumValue & 0x7fffffff) % 251;
            }
        }''')

    def test_arrays_and_references(self):
        self.javaComparison('''public class tests {
            static int[] createEntry(int size) { return new int[size]; }
            public static int run() {
                int[] firstOperand = createEntry(8); int[] secondOperand = firstOperand; int[] emptyObject = new int[0];
                if (firstOperand != secondOperand || firstOperand == null || emptyObject.length != 0 || firstOperand[7] != 0) return 99;
                int value = (firstOperand[2] = 40); firstOperand[2]++; ++firstOperand[3]; firstOperand[2] += 7;
                return value + secondOperand[2] + secondOperand[3];
            }
        }''')

    def test_static_fields_and_argument_order(self):
        self.javaComparison('''public class tests {
            static int value = auxiliaryValue.initialValue();
            static int calculation(int firstOperand, int secondOperand, int thirdOperand, int fourthOperand, int fifthOperand) {
                return firstOperand + secondOperand * 2 + thirdOperand * 3 + fourthOperand * 4 + fifthOperand * 5;
            }
            public static int run() { return calculation(1, 2, 3, 4, value) + auxiliaryValue.read(); }
        }''', {'auxiliaryValue': '''public class auxiliaryValue {
            static int value = 3;
            static int initialValue() { return ++value; }
            static int read() { return value; }
        }'''})

    def test_initialization_cycle(self):
        self.javaComparison('''public class tests {
            static int value = auxiliaryValue.read() + 1;
            public static int run() { return value * 10 + auxiliaryValue.read(); }
        }''', {'auxiliaryValue': '''public class auxiliaryValue {
            static int value = tests.value + 2;
            static int read() { return value; }
        }'''})

    def test_modified_utf8_strings(self):
        self.javaComparison('''public class tests {
            static String text = "한글\\u0000😀";
            public static int run() {
                if (text != "한글\\u0000😀") return 99;
                return (text.length() + text.charAt(2) + text.charAt(3) + text.charAt(4)) % 251;
            }
        }''')

    def test_switch_and_recursion(self):
        self.javaComparison('''public class tests {
            static int factorial(int value) { return value <= 1 ? 1 : value * factorial(value - 1); }
            static int denseSwitchCases(int value) {
                switch (value) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int sparseSwitchCases(int value) {
                switch (value) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int run() { return (factorial(5) + denseSwitchCases(0) + denseSwitchCases(2) + denseSwitchCases(9) + sparseSwitchCases(-1000) + sparseSwitchCases(0)) % 251; }
        }''')

    def test_wide_local_variables(self):
        Declaration = '\n'.join('int value{} = {};'.format(index, index) for index in range(270))
        additionResult = '+'.join('value{}'.format(index) for index in range(270))
        self.javaComparison('public class tests { public static int run() {' + Declaration +
                    'value269 += 300; return (' + additionResult + ') % 251; } }')

    def test_runtime_error_numbers(self):
        caseEntries = [
            ('int zeroOperand = 0; return 1 / zeroOperand;', 101),
            ('int[] value = null; return value.length;', 102),
            ('int[] value = new int[1]; return value[1];', 103),
            ('int[] value = new int[1]; value[-1] = 3; return 0;', 103),
            ('int value = -1; return new int[value].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] firstOperand = new int[65535]; return new int[1].length;', 105),
        ]
        for bodyValue, expectation in caseEntries:
            with self.subTest(bodyValue=bodyValue):
                self.compileSource('public class tests { public static int run() { ' + bodyValue + ' } }')
                self.assertEqual(self.executionResult(), expectation)

    def test_unsupported_feature_rejected(self):
        caseEntries = [
            'static long value; public static int run() { return 0; }',
            'public static int run() { Object value = new Object(); return 0; }',
            'public static int run() { System.out.println("hello"); return 0; }',
            'public static int run() { try { return 1; } catch (Exception error) { return 2; } }',
            'public static synchronized int run() { return 0; }',
            'public static int run() { return new byte[3].length; }',
            'static native int externalValue(); public static int run() { return externalValue(); }',
            'int value; public static int run() { return 0; }',
        ]
        for bodyValue in caseEntries:
            with self.subTest(bodyValue=bodyValue):
                self.compileSource('public class tests { ' + bodyValue + ' }', successValue=False)

    def test_existing_output_preserved_on_failure(self):
        Output = self.directoryValue / 'native'
        Output.write_bytes(b'original-output')
        self.compileSource('public class tests { public static int run() { return missing; } }', successValue=False)
        self.assertEqual(Output.read_bytes(), b'original-output')

    def test_elf_and_standalone_execution(self):
        self.compileSource('public class tests { public static int run() { return 37; } }')
        self.assertEqual((self.directoryValue / 'native').read_bytes()[:5], b'\x7fELF\x01')
        lookupTable = subprocess.check_output(['readelf', '-l', str(self.directoryValue / 'native')])
        self.assertNotIn(b'INTERP', lookupTable)
        self.assertEqual(self.executionResult(), 37)

    def test_user_elf_and_abi_separation(self):
        self.compileSource('public class tests { public static int run() { return User.executionPermission(); } }',
                    {'User': 'public class User { public static native int executionPermission(); }'}, targetValue='user')
        data = (self.directoryValue / 'native').read_bytes()
        self.assertEqual(data[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', data, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.directoryValue / 'native')]))
        # User ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.compileSource('public class tests { public static int run() { return deviceValue.readHardwarePort(1); } }',
                    {'deviceValue': 'public class deviceValue { public static native int readHardwarePort(int value); }'}, successValue=False, targetValue='user')

    def test_export_validation(self):
        source = 'public class tests { public static int run() { return 0; } static int invoke(int value) { return value; } }'
        self.compileSource(source, targetValue='kernel', exportedValue='kernel_dispatch=tests.invoke')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.directoryValue / 'native')]))
        self.compileSource(source, successValue=False, exportedValue='bad;name=tests.invoke')
        self.compileSource(source, successValue=False, exportedValue='missing=tests.missingMethod')


if __name__ == '__main__':
    unittest.main()
