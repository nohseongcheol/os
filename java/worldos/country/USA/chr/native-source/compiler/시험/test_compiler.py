"""ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ ELF ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ + OpenJDK 결과 대조. 임시 시험 자료만 생성한다."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

컴파일러 = Path(__file__).resolve().parents[1] / '컴파일러.py'


class 네이티브시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-compiler-test-')
        self.addCleanup(self.임시.cleanup)
        self.ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ = Path(self.임시.name)

    def ᎪᏢᏍᎩ_ᎦᏟᏌᏅᎯ(self, ᎦᏟᏌᏅᎯ_0201f362, 추가=None, 성공=True, ᎠᏉᏅᏗᎢ='linux', 내보냄=None):
        ᎠᏍᏓᏩᏛᏍᏗ_ᏕᎦᏅᏅᏛ = []
        for ᏚᏙᎥᎢ, ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ in dict({'시험': ᎦᏟᏌᏅᎯ_0201f362}, **(추가 or {})).items():
            ᎠᏍᏓᏩᏛᏍᏗ = self.ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ / (ᏚᏙᎥᎢ + '.java')
            ᎠᏍᏓᏩᏛᏍᏗ.write_text(ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ, encoding='utf-8')
            ᎠᏍᏓᏩᏛᏍᏗ_ᏕᎦᏅᏅᏛ.append(str(ᎠᏍᏓᏩᏛᏍᏗ))
        ᎤᏁᏤᎸᎩ = [sys.executable, str(컴파일러), '--target', ᎠᏉᏅᏗᎢ, '--entry', '시험.ᎠᎢᏎᏍᏗ', '-o', str(self.ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ / 'native')]
        if 내보냄 is not None: ᎤᏁᏤᎸᎩ += ['--export', 내보냄]
        결과 = subprocess.run(ᎤᏁᏤᎸᎩ + ᎠᏍᏓᏩᏛᏍᏗ_ᏕᎦᏅᏅᏛ,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(결과.returncode, 0, 결과.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(결과.returncode, 0)
            self.assertIn('ᎪᏢᏍᎩ_ᎦᏟᏌᏅᎯ ᎦᎵᏓᏍᏔᏅ'.encode(), 결과.stderr)
        return 결과

    def 실행결과(self):
        return subprocess.run([str(self.ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ / 'native')], timeout=5).returncode

    def 자바대조(self, ᎦᏟᏌᏅᎯ_0201f362, 추가=None):
        self.ᎪᏢᏍᎩ_ᎦᏟᏌᏅᎯ(ᎦᏟᏌᏅᎯ_0201f362, 추가)
        (self.ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ / 'ᎠᏁᏢᏍᎩ.java').write_text(
            'public class ᎠᏁᏢᏍᎩ { public static void main(String[] 인수) { System.exit(시험.ᎠᎢᏎᏍᏗ()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ)] +
                       [str(ᎠᏍᏓᏩᏛᏍᏗ) for ᎠᏍᏓᏩᏛᏍᏗ in self.ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ), 'ᎠᏁᏢᏍᎩ'], timeout=5).returncode
        ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ = self.실행결과()
        self.assertGreaterEqual(ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 ᎰᎯᏳᏓ)')
        self.assertEqual(ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int ᎠᎢᏎᏍᏗ() {
                int 합 = 7;
                int ᏧᎬᏩᎶᏗᏯ = 12345;
                for (int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ = -65; ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ <= 65; ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ++) {
                    ᏧᎬᏩᎶᏗᏯ = ᏧᎬᏩᎶᏗᏯ * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(ᏧᎬᏩᎶᏗᏯ, ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ);
                    합 += (byte)ᏧᎬᏩᎶᏗᏯ + (short)ᏧᎬᏩᎶᏗᏯ + (char)ᏧᎬᏩᎶᏗᏯ;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] ᏧᎬᏩᎶᏗᏯ = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int ᎠᎢᏎᏍᏗ() {
                int 합 = 13;
                for (int 가 = 0; 가 < ᏧᎬᏩᎶᏗᏯ.length; 가++)
                    for (int 나 = 1; 나 < ᏧᎬᏩᎶᏗᏯ.length; 나++)
                        합 = 합 * 31 + ᏧᎬᏩᎶᏗᏯ[가] / ᏧᎬᏩᎶᏗᏯ[나] + ᏧᎬᏩᎶᏗᏯ[가] % ᏧᎬᏩᎶᏗᏯ[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] 만들기(int ᎢᎩᏓ) { return new int[ᎢᎩᏓ]; }
            public static int ᎠᎢᏎᏍᏗ() {
                int[] 가 = 만들기(8); int[] 나 = 가; int[] 빈것 = new int[0];
                if (가 != 나 || 가 == null || 빈것.length != 0 || 가[7] != 0) return 99;
                int ᏧᎬᏩᎶᏗᏯ = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return ᏧᎬᏩᎶᏗᏯ + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int ᏧᎬᏩᎶᏗᏯ = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int ᎠᎢᏎᏍᏗ() { return 계산(1, 2, 3, 4, ᏧᎬᏩᎶᏗᏯ) + 보조.읽기(); }
        }''', {'보조': '''public class 보조 {
            static int ᏧᎬᏩᎶᏗᏯ = 3;
            static int 초기값() { return ++ᏧᎬᏩᎶᏗᏯ; }
            static int 읽기() { return ᏧᎬᏩᎶᏗᏯ; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int ᏧᎬᏩᎶᏗᏯ = 보조.읽기() + 1;
            public static int ᎠᎢᏎᏍᏗ() { return ᏧᎬᏩᎶᏗᏯ * 10 + 보조.읽기(); }
        }''', {'보조': '''public class 보조 {
            static int ᏧᎬᏩᎶᏗᏯ = 시험.ᏧᎬᏩᎶᏗᏯ + 2;
            static int 읽기() { return ᏧᎬᏩᎶᏗᏯ; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String ᎠᎪᎵᏰᏗ = "한글\\u0000😀";
            public static int ᎠᎢᏎᏍᏗ() {
                if (ᎠᎪᎵᏰᏗ != "한글\\u0000😀") return 99;
                return (ᎠᎪᎵᏰᏗ.length() + ᎠᎪᎵᏰᏗ.charAt(2) + ᎠᎪᎵᏰᏗ.charAt(3) + ᎠᎪᎵᏰᏗ.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int 계승(int ᏧᎬᏩᎶᏗᏯ) { return ᏧᎬᏩᎶᏗᏯ <= 1 ? 1 : ᏧᎬᏩᎶᏗᏯ * 계승(ᏧᎬᏩᎶᏗᏯ - 1); }
            static int 연속(int ᏧᎬᏩᎶᏗᏯ) {
                switch (ᏧᎬᏩᎶᏗᏯ) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int ᏧᎬᏩᎶᏗᏯ) {
                switch (ᏧᎬᏩᎶᏗᏯ) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int ᎠᎢᏎᏍᏗ() { return (계승(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        선언 = '\n'.join('int ᏧᎬᏩᎶᏗᏯ{} = {};'.format(ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ, ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ) for ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ in range(270))
        덧셈 = '+'.join('ᏧᎬᏩᎶᏗᏯ{}'.format(ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ) for ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ in range(270))
        self.자바대조('public class 시험 { public static int ᎠᎢᏎᏍᏗ() {' + 선언 +
                    'ᏧᎬᏩᎶᏗᏯ_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] ᏧᎬᏩᎶᏗᏯ = null; return ᏧᎬᏩᎶᏗᏯ.length;', 102),
            ('int[] ᏧᎬᏩᎶᏗᏯ = new int[1]; return ᏧᎬᏩᎶᏗᏯ[1];', 103),
            ('int[] ᏧᎬᏩᎶᏗᏯ = new int[1]; ᏧᎬᏩᎶᏗᏯ[-1] = 3; return 0;', 103),
            ('int ᏧᎬᏩᎶᏗᏯ = -1; return new int[ᏧᎬᏩᎶᏗᏯ].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for 몸체, 기대 in 경우들:
            with self.subTest(몸체=몸체):
                self.ᎪᏢᏍᎩ_ᎦᏟᏌᏅᎯ('public class 시험 { public static int ᎠᎢᏎᏍᏗ() { ' + 몸체 + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long ᏧᎬᏩᎶᏗᏯ; public static int ᎠᎢᏎᏍᏗ() { return 0; }',
            'public static int ᎠᎢᏎᏍᏗ() { Object ᏧᎬᏩᎶᏗᏯ = new Object(); return 0; }',
            'public static int ᎠᎢᏎᏍᏗ() { System.out.println("hello"); return 0; }',
            'public static int ᎠᎢᏎᏍᏗ() { try { return 1; } catch (Exception ᎦᎵᏓᏍᏔᏅ) { return 2; } }',
            'public static synchronized int ᎠᎢᏎᏍᏗ() { return 0; }',
            'public static int ᎠᎢᏎᏍᏗ() { return new byte[3].length; }',
            'static native int 외부(); public static int ᎠᎢᏎᏍᏗ() { return 외부(); }',
            'int ᏧᎬᏩᎶᏗᏯ; public static int ᎠᎢᏎᏍᏗ() { return 0; }',
        ]
        for 몸체 in 경우들:
            with self.subTest(몸체=몸체):
                self.ᎪᏢᏍᎩ_ᎦᏟᏌᏅᎯ('public class 시험 { ' + 몸체 + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        출력 = self.ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ / 'native'
        출력.write_bytes(b'original-output')
        self.ᎪᏢᏍᎩ_ᎦᏟᏌᏅᎯ('public class 시험 { public static int ᎠᎢᏎᏍᏗ() { return missing; } }', 성공=False)
        self.assertEqual(출력.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.ᎪᏢᏍᎩ_ᎦᏟᏌᏅᎯ('public class 시험 { public static int ᎠᎢᏎᏍᏗ() { return 37; } }')
        self.assertEqual((self.ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ / 'native').read_bytes()[:5], b'\x7fELF\x01')
        표 = subprocess.check_output(['readelf', '-l', str(self.ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ / 'native')])
        self.assertNotIn(b'INTERP', 표)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.ᎪᏢᏍᎩ_ᎦᏟᏌᏅᎯ('public class 시험 { public static int ᎠᎢᏎᏍᏗ() { return ᎬᏗᏍᎩ.실행권한(); } }',
                    {'ᎬᏗᏍᎩ': 'public class ᎬᏗᏍᎩ { public static native int 실행권한(); }'}, ᎠᏉᏅᏗᎢ='user')
        ᎦᏟᏌᏅᎯ = (self.ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ / 'native').read_bytes()
        self.assertEqual(ᎦᏟᏌᏅᎯ[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', ᎦᏟᏌᏅᎯ, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ / 'native')]))
        # ᎬᏗᏍᎩ ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.ᎪᏢᏍᎩ_ᎦᏟᏌᏅᎯ('public class 시험 { public static int ᎠᎢᏎᏍᏗ() { return ᎠᏂᎩᏍᎩ_ᏧᎬᏩᎶᏗᏯ.포트읽기(1); } }',
                    {'ᎠᏂᎩᏍᎩ_ᏧᎬᏩᎶᏗᏯ': 'public class ᎠᏂᎩᏍᎩ_ᏧᎬᏩᎶᏗᏯ { public static native int 포트읽기(int ᏧᎬᏩᎶᏗᏯ); }'}, 성공=False, ᎠᏉᏅᏗᎢ='user')

    def ᎠᏓᎪᎵᏰᏍᎩ_ᏫᎦᏌᏙᎣᏍᏗ_ᎤᏙᎯᏳᏒᎢ(self):
        ᎦᏟᏌᏅᎯ_0201f362 = 'public class 시험 { public static int ᎠᎢᏎᏍᏗ() { return 0; } static int 호출(int ᏧᎬᏩᎶᏗᏯ) { return ᏧᎬᏩᎶᏗᏯ; } }'
        self.ᎪᏢᏍᎩ_ᎦᏟᏌᏅᎯ(ᎦᏟᏌᏅᎯ_0201f362, ᎠᏉᏅᏗᎢ='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.ᎠᏓᏎᎮᎯ_ᏫᎦᎷᎯᏍᏗ_ᏧᎬᏩᎶᏗᏯ / 'native')]))
        self.ᎪᏢᏍᎩ_ᎦᏟᏌᏅᎯ(ᎦᏟᏌᏅᎯ_0201f362, 성공=False, 내보냄='bad;name=시험.호출')
        self.ᎪᏢᏍᎩ_ᎦᏟᏌᏅᎯ(ᎦᏟᏌᏅᎯ_0201f362, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
