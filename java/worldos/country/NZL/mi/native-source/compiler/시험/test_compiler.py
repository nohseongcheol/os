"""tūturu_raraunga ELF kawe_tono + OpenJDK mēhua 대조. 임시 시험 자료만 생성한다."""
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
        self.whaiaronga_uara = Path(self.임시.name)

    def hanga_pūtake(self, pūtake, 추가=None, 성공=True, ūnga='linux', 내보냄=None):
        ara_Rārangi = []
        for Ingoa, Ihirangi_uara in dict({'시험': pūtake}, **(추가 or {})).items():
            ara = self.whaiaronga_uara / (Ingoa + '.java')
            ara.write_text(Ihirangi_uara, encoding='utf-8')
            ara_Rārangi.append(str(ara))
        tono = [sys.executable, str(컴파일러), '--target', ūnga, '--entry', '시험.whakahaere', '-o', str(self.whaiaronga_uara / 'native')]
        if 내보냄 is not None: tono += ['--export', 내보냄]
        mēhua = subprocess.run(tono + ara_Rārangi,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(mēhua.returncode, 0, mēhua.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(mēhua.returncode, 0)
            self.assertIn('hanga_pūtake Pōhēhē'.encode(), mēhua.stderr)
        return mēhua

    def 실행결과(self):
        return subprocess.run([str(self.whaiaronga_uara / 'native')], timeout=5).returncode

    def 자바대조(self, pūtake, 추가=None):
        self.hanga_pūtake(pūtake, 추가)
        (self.whaiaronga_uara / 'taurima.java').write_text(
            'public class taurima { public static void main(String[] 인수) { System.exit(시험.whakahaere()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.whaiaronga_uara)] +
                       [str(ara) for ara in self.whaiaronga_uara.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.whaiaronga_uara), 'taurima'], timeout=5).returncode
        tūturu_raraunga = self.실행결과()
        self.assertGreaterEqual(tūturu_raraunga, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 manatoko)')
        self.assertEqual(tūturu_raraunga, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int whakahaere() {
                int SUM_uara = 7;
                int uara = 12345;
                for (int INDEX = -65; INDEX <= 65; INDEX++) {
                    uara = uara * 1664525 + 1013904223;
                    SUM_uara = SUM_uara * 31 + 섞기(uara, INDEX);
                    SUM_uara += (byte)uara + (short)uara + (char)uara;
                }
                return (SUM_uara & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] uara = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int whakahaere() {
                int SUM_uara = 13;
                for (int 가 = 0; 가 < uara.length; 가++)
                    for (int 나 = 1; 나 < uara.length; 나++)
                        SUM_uara = SUM_uara * 31 + uara[가] / uara[나] + uara[가] % uara[나];
                return (SUM_uara & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] Waihanga_tāurunga(int rahi) { return new int[rahi]; }
            public static int whakahaere() {
                int[] 가 = Waihanga_tāurunga(8); int[] 나 = 가; int[] putua_ahanoa = new int[0];
                if (가 != 나 || 가 == null || putua_ahanoa.length != 0 || 가[7] != 0) return 99;
                int uara = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return uara + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int uara = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int whakahaere() { return 계산(1, 2, 3, 4, uara) + 보조.Pānuitia(); }
        }''', {'보조': '''public class 보조 {
            static int uara = 3;
            static int 초기값() { return ++uara; }
            static int Pānuitia() { return uara; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int uara = 보조.Pānuitia() + 1;
            public static int whakahaere() { return uara * 10 + 보조.Pānuitia(); }
        }''', {'보조': '''public class 보조 {
            static int uara = 시험.uara + 2;
            static int Pānuitia() { return uara; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String Ngā_kupu = "한글\\u0000😀";
            public static int whakahaere() {
                if (Ngā_kupu != "한글\\u0000😀") return 99;
                return (Ngā_kupu.length() + Ngā_kupu.charAt(2) + Ngā_kupu.charAt(3) + Ngā_kupu.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int huarea(int uara) { return uara <= 1 ? 1 : uara * huarea(uara - 1); }
            static int 연속(int uara) {
                switch (uara) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int uara) {
                switch (uara) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int whakahaere() { return (huarea(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        선언 = '\n'.join('int uara{} = {};'.format(INDEX, INDEX) for INDEX in range(270))
        덧셈 = '+'.join('uara{}'.format(INDEX) for INDEX in range(270))
        self.자바대조('public class 시험 { public static int whakahaere() {' + 선언 +
                    'uara_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] uara = null; return uara.length;', 102),
            ('int[] uara = new int[1]; return uara[1];', 103),
            ('int[] uara = new int[1]; uara[-1] = 3; return 0;', 103),
            ('int uara = -1; return new int[uara].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for 몸체, 기대 in 경우들:
            with self.subTest(몸체=몸체):
                self.hanga_pūtake('public class 시험 { public static int whakahaere() { ' + 몸체 + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long uara; public static int whakahaere() { return 0; }',
            'public static int whakahaere() { Object uara = new Object(); return 0; }',
            'public static int whakahaere() { System.out.println("hello"); return 0; }',
            'public static int whakahaere() { try { return 1; } catch (Exception Pōhēhē) { return 2; } }',
            'public static synchronized int whakahaere() { return 0; }',
            'public static int whakahaere() { return new byte[3].length; }',
            'static native int 외부(); public static int whakahaere() { return 외부(); }',
            'int uara; public static int whakahaere() { return 0; }',
        ]
        for 몸체 in 경우들:
            with self.subTest(몸체=몸체):
                self.hanga_pūtake('public class 시험 { ' + 몸체 + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        출력 = self.whaiaronga_uara / 'native'
        출력.write_bytes(b'original-output')
        self.hanga_pūtake('public class 시험 { public static int whakahaere() { return missing; } }', 성공=False)
        self.assertEqual(출력.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.hanga_pūtake('public class 시험 { public static int whakahaere() { return 37; } }')
        self.assertEqual((self.whaiaronga_uara / 'native').read_bytes()[:5], b'\x7fELF\x01')
        Rapu_ripanga = subprocess.check_output(['readelf', '-l', str(self.whaiaronga_uara / 'native')])
        self.assertNotIn(b'INTERP', Rapu_ripanga)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.hanga_pūtake('public class 시험 { public static int whakahaere() { return kaiwhakamahi.실행권한(); } }',
                    {'kaiwhakamahi': 'public class kaiwhakamahi { public static native int 실행권한(); }'}, ūnga='user')
        raraunga = (self.whaiaronga_uara / 'native').read_bytes()
        self.assertEqual(raraunga[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', raraunga, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.whaiaronga_uara / 'native')]))
        # kaiwhakamahi ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.hanga_pūtake('public class 시험 { public static int whakahaere() { return pūkoro_uara.포트읽기(1); } }',
                    {'pūkoro_uara': 'public class pūkoro_uara { public static native int 포트읽기(int uara); }'}, 성공=False, ūnga='user')

    def test_내보내기검증(self):
        pūtake = 'public class 시험 { public static int whakahaere() { return 0; } static int 호출(int uara) { return uara; } }'
        self.hanga_pūtake(pūtake, ūnga='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.whaiaronga_uara / 'native')]))
        self.hanga_pūtake(pūtake, 성공=False, 내보냄='bad;name=시험.호출')
        self.hanga_pūtake(pūtake, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
