"""ຕົວ_ຈິງ_ຂໍ້ມູນ ELF ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ + OpenJDK ມາດຕະການ 대조. 임시 시험 자료만 생성한다."""
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
        self.ກຸ່ມຂໍ້ມູນ_ຄ່າ = Path(self.임시.name)

    def ສ້າງ_ແຫຼ່ງທີ່ມາ(self, ແຫຼ່ງທີ່ມາ, 추가=None, 성공=True, ເປົ້າ_ຫມາຍ='linux', 내보냄=None):
        ທາງໂຄຈອນ_ລາຍຊື່ = []
        for ຊື່, ເນື້ອໃນ_ຄ່າ_cb0f2404 in dict({'시험': ແຫຼ່ງທີ່ມາ}, **(추가 or {})).items():
            ທາງໂຄຈອນ = self.ກຸ່ມຂໍ້ມູນ_ຄ່າ / (ຊື່ + '.java')
            ທາງໂຄຈອນ.write_text(ເນື້ອໃນ_ຄ່າ_cb0f2404, encoding='utf-8')
            ທາງໂຄຈອນ_ລາຍຊື່.append(str(ທາງໂຄຈອນ))
        ຄໍາສັ່ງ_1f12b8e2 = [sys.executable, str(컴파일러), '--target', ເປົ້າ_ຫມາຍ, '--entry', '시험.ແລ່ນ', '-o', str(self.ກຸ່ມຂໍ້ມູນ_ຄ່າ / 'native')]
        if 내보냄 is not None: ຄໍາສັ່ງ_1f12b8e2 += ['--export', 내보냄]
        ມາດຕະການ = subprocess.run(ຄໍາສັ່ງ_1f12b8e2 + ທາງໂຄຈອນ_ລາຍຊື່,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        if 성공:
            self.assertEqual(ມາດຕະການ.returncode, 0, ມາດຕະການ.stderr.decode('utf-8'))
        else:
            self.assertNotEqual(ມາດຕະການ.returncode, 0)
            self.assertIn('ສ້າງ_ແຫຼ່ງທີ່ມາ ຂໍ້ຜິດພາດ'.encode(), ມາດຕະການ.stderr)
        return ມາດຕະການ

    def 실행결과(self):
        return subprocess.run([str(self.ກຸ່ມຂໍ້ມູນ_ຄ່າ / 'native')], timeout=5).returncode

    def 자바대조(self, ແຫຼ່ງທີ່ມາ, 추가=None):
        self.ສ້າງ_ແຫຼ່ງທີ່ມາ(ແຫຼ່ງທີ່ມາ, 추가)
        (self.ກຸ່ມຂໍ້ມູນ_ຄ່າ / 'ໂຮສ.java').write_text(
            'public class ໂຮສ { public static void main(String[] 인수) { System.exit(시험.ແລ່ນ()); } }', encoding='utf-8')
        subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(self.ກຸ່ມຂໍ້ມູນ_ຄ່າ)] +
                       [str(ທາງໂຄຈອນ) for ທາງໂຄຈອນ in self.ກຸ່ມຂໍ້ມູນ_ຄ່າ.glob('*.java')], check=True, timeout=30)
        기대 = subprocess.run(['java', '-cp', str(self.ກຸ່ມຂໍ້ມູນ_ຄ່າ), 'ໂຮສ'], timeout=5).returncode
        ຕົວ_ຈິງ_ຂໍ້ມູນ = self.실행결과()
        self.assertGreaterEqual(ຕົວ_ຈິງ_ຂໍ້ມູນ, 0, '신호로 종료됨 (샌드박스의 32비트 syscall 제한 여부 확인)')
        self.assertEqual(ຕົວ_ຈິງ_ຂໍ້ມູນ, 기대)

    def test_정수연산과이동(self):
        self.자바대조('''public class 시험 {
            static int 섞기(int 가, int 나) {
                return ((가 + 나) ^ (가 - 나) ^ (가 * 나) ^ (가 & 나) ^ (가 | 나))
                    + (가 << 나) + (가 >> 나) + (가 >>> 나);
            }
            public static int ແລ່ນ() {
                int 합 = 7;
                int ຄ່າ = 12345;
                for (int ດັດຊະນີ = -65; ດັດຊະນີ <= 65; ດັດຊະນີ++) {
                    ຄ່າ = ຄ່າ * 1664525 + 1013904223;
                    합 = 합 * 31 + 섞기(ຄ່າ, ດັດຊະນີ);
                    합 += (byte)ຄ່າ + (short)ຄ່າ + (char)ຄ່າ;
                }
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_나눗셈극값(self):
        self.자바대조('''public class 시험 {
            static int[] ຄ່າ = {0, 1, -1, 7, -7, 2147483647, -2147483648};
            public static int ແລ່ນ() {
                int 합 = 13;
                for (int 가 = 0; 가 < ຄ່າ.length; 가++)
                    for (int 나 = 1; 나 < ຄ່າ.length; 나++)
                        합 = 합 * 31 + ຄ່າ[가] / ຄ່າ[나] + ຄ່າ[가] % ຄ່າ[나];
                return (합 & 0x7fffffff) % 251;
            }
        }''')

    def test_배열과참조(self):
        self.자바대조('''public class 시험 {
            static int[] ສ້າງ_ເຂົ້າໃນ(int ຂະ_ຫນາດ) { return new int[ຂະ_ຫນາດ]; }
            public static int ແລ່ນ() {
                int[] 가 = ສ້າງ_ເຂົ້າໃນ(8); int[] 나 = 가; int[] ຫວ່າງ_ເປົ່າ_ວັດ_ຖຸ = new int[0];
                if (가 != 나 || 가 == null || ຫວ່າງ_ເປົ່າ_ວັດ_ຖຸ.length != 0 || 가[7] != 0) return 99;
                int ຄ່າ = (가[2] = 40); 가[2]++; ++가[3]; 가[2] += 7;
                return ຄ່າ + 나[2] + 나[3];
            }
        }''')

    def test_정적필드와인수순서(self):
        self.자바대조('''public class 시험 {
            static int ຄ່າ = 보조.초기값();
            static int 계산(int 가, int 나, int 다, int 라, int 마) {
                return 가 + 나 * 2 + 다 * 3 + 라 * 4 + 마 * 5;
            }
            public static int ແລ່ນ() { return 계산(1, 2, 3, 4, ຄ່າ) + 보조.읽기(); }
        }''', {'보조': '''public class 보조 {
            static int ຄ່າ = 3;
            static int 초기값() { return ++ຄ່າ; }
            static int 읽기() { return ຄ່າ; }
        }'''})

    def test_초기화순환(self):
        self.자바대조('''public class 시험 {
            static int ຄ່າ = 보조.읽기() + 1;
            public static int ແລ່ນ() { return ຄ່າ * 10 + 보조.읽기(); }
        }''', {'보조': '''public class 보조 {
            static int ຄ່າ = 시험.ຄ່າ + 2;
            static int 읽기() { return ຄ່າ; }
        }'''})

    def test_문자열수정유티에프(self):
        self.자바대조('''public class 시험 {
            static String ຂໍ້ຄວາມ = "한글\\u0000😀";
            public static int ແລ່ນ() {
                if (ຂໍ້ຄວາມ != "한글\\u0000😀") return 99;
                return (ຂໍ້ຄວາມ.length() + ຂໍ້ຄວາມ.charAt(2) + ຂໍ້ຄວາມ.charAt(3) + ຂໍ້ຄວາມ.charAt(4)) % 251;
            }
        }''')

    def test_switch와재귀(self):
        self.자바대조('''public class 시험 {
            static int ແຟັກ_ຕໍ_ຣຽ_ລ(int ຄ່າ) { return ຄ່າ <= 1 ? 1 : ຄ່າ * ແຟັກ_ຕໍ_ຣຽ_ລ(ຄ່າ - 1); }
            static int 연속(int ຄ່າ) {
                switch (ຄ່າ) { case 0: return 3; case 1: return 5; case 2: return 7; default: return 11; }
            }
            static int 드문(int ຄ່າ) {
                switch (ຄ່າ) { case -1000: return 17; case 5000: return 23; default: return 31; }
            }
            public static int ແລ່ນ() { return (ແຟັກ_ຕໍ_ຣຽ_ລ(5) + 연속(0) + 연속(2) + 연속(9) + 드문(-1000) + 드문(0)) % 251; }
        }''')

    def test_wide지역변수(self):
        ການປະກາດ = '\n'.join('int ຄ່າ{} = {};'.format(ດັດຊະນີ, ດັດຊະນີ) for ດັດຊະນີ in range(270))
        덧셈 = '+'.join('ຄ່າ{}'.format(ດັດຊະນີ) for ດັດຊະນີ in range(270))
        self.자바대조('public class 시험 { public static int ແລ່ນ() {' + ການປະກາດ +
                    'ຄ່າ_269 += 300; return (' + 덧셈 + ') % 251; } }')

    def test_런타임오류번호(self):
        경우들 = [
            ('int 영 = 0; return 1 / 영;', 101),
            ('int[] ຄ່າ = null; return ຄ່າ.length;', 102),
            ('int[] ຄ່າ = new int[1]; return ຄ່າ[1];', 103),
            ('int[] ຄ່າ = new int[1]; ຄ່າ[-1] = 3; return 0;', 103),
            ('int ຄ່າ = -1; return new int[ຄ່າ].length;', 104),
            ('return new int[65536].length;', 105),
            ('int[] 가 = new int[65535]; return new int[1].length;', 105),
        ]
        for ເນື້ອໃນ_ຄ່າ, 기대 in 경우들:
            with self.subTest(ເນື້ອໃນ_ຄ່າ=ເນື້ອໃນ_ຄ່າ):
                self.ສ້າງ_ແຫຼ່ງທີ່ມາ('public class 시험 { public static int ແລ່ນ() { ' + ເນື້ອໃນ_ຄ່າ + ' } }')
                self.assertEqual(self.실행결과(), 기대)

    def test_미지원기능거부(self):
        경우들 = [
            'static long ຄ່າ; public static int ແລ່ນ() { return 0; }',
            'public static int ແລ່ນ() { Object ຄ່າ = new Object(); return 0; }',
            'public static int ແລ່ນ() { System.out.println("hello"); return 0; }',
            'public static int ແລ່ນ() { try { return 1; } catch (Exception ຂໍ້ຜິດພາດ) { return 2; } }',
            'public static synchronized int ແລ່ນ() { return 0; }',
            'public static int ແລ່ນ() { return new byte[3].length; }',
            'static native int 외부(); public static int ແລ່ນ() { return 외부(); }',
            'int ຄ່າ; public static int ແລ່ນ() { return 0; }',
        ]
        for ເນື້ອໃນ_ຄ່າ in 경우들:
            with self.subTest(ເນື້ອໃນ_ຄ່າ=ເນື້ອໃນ_ຄ່າ):
                self.ສ້າງ_ແຫຼ່ງທີ່ມາ('public class 시험 { ' + ເນື້ອໃນ_ຄ່າ + ' }', 성공=False)

    def test_실패시기존출력보존(self):
        출력 = self.ກຸ່ມຂໍ້ມູນ_ຄ່າ / 'native'
        출력.write_bytes(b'original-output')
        self.ສ້າງ_ແຫຼ່ງທີ່ມາ('public class 시험 { public static int ແລ່ນ() { return missing; } }', 성공=False)
        self.assertEqual(출력.read_bytes(), b'original-output')

    def test_ELF와독립실행(self):
        self.ສ້າງ_ແຫຼ່ງທີ່ມາ('public class 시험 { public static int ແລ່ນ() { return 37; } }')
        self.assertEqual((self.ກຸ່ມຂໍ້ມູນ_ຄ່າ / 'native').read_bytes()[:5], b'\x7fELF\x01')
        ຄົ້ນຫາ_ຕາຕະລາງ = subprocess.check_output(['readelf', '-l', str(self.ກຸ່ມຂໍ້ມູນ_ຄ່າ / 'native')])
        self.assertNotIn(b'INTERP', ຄົ້ນຫາ_ຕາຕະລາງ)
        self.assertEqual(self.실행결과(), 37)

    def test_사용자ELF와ABI분리(self):
        self.ສ້າງ_ແຫຼ່ງທີ່ມາ('public class 시험 { public static int ແລ່ນ() { return ຜູ້ໃຊ້.실행권한(); } }',
                    {'ຜູ້ໃຊ້': 'public class ຜູ້ໃຊ້ { public static native int 실행권한(); }'}, ເປົ້າ_ຫມາຍ='user')
        ຂໍ້ມູນ = (self.ກຸ່ມຂໍ້ມູນ_ຄ່າ / 'native').read_bytes()
        self.assertEqual(ຂໍ້ມູນ[:5], b'\x7fELF\x01')
        import struct
        self.assertGreaterEqual(struct.unpack_from('<I', ຂໍ້ມູນ, 24)[0], 0x04000000)
        self.assertNotIn(b'INTERP', subprocess.check_output(['readelf', '-l', str(self.ກຸ່ມຂໍ້ມູນ_ຄ່າ / 'native')]))
        # ຜູ້ໃຊ້ ELF는 Linux syscall ABI가 아니므로 호스트에서 실행하지 않는다.
        self.ສ້າງ_ແຫຼ່ງທີ່ມາ('public class 시험 { public static int ແລ່ນ() { return ມືຖື_ຄ່າ.포트읽기(1); } }',
                    {'ມືຖື_ຄ່າ': 'public class ມືຖື_ຄ່າ { public static native int 포트읽기(int ຄ່າ); }'}, 성공=False, ເປົ້າ_ຫມາຍ='user')

    def test_내보내기검증(self):
        ແຫຼ່ງທີ່ມາ = 'public class 시험 { public static int ແລ່ນ() { return 0; } static int 호출(int ຄ່າ) { return ຄ່າ; } }'
        self.ສ້າງ_ແຫຼ່ງທີ່ມາ(ແຫຼ່ງທີ່ມາ, ເປົ້າ_ຫມາຍ='kernel', 내보냄='kernel_dispatch=시험.호출')
        self.assertIn(b'kernel_dispatch', subprocess.check_output(['nm', str(self.ກຸ່ມຂໍ້ມູນ_ຄ່າ / 'native')]))
        self.ສ້າງ_ແຫຼ່ງທີ່ມາ(ແຫຼ່ງທີ່ມາ, 성공=False, 내보냄='bad;name=시험.호출')
        self.ສ້າງ_ແຫຼ່ງທີ່ມາ(ແຫຼ່ງທີ່ມາ, 성공=False, 내보냄='missing=시험.없음')


if __name__ == '__main__':
    unittest.main()
