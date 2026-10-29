import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

پێناسە_نرخ = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
모듈 = importlib.util.module_from_spec(پێناسە_نرخ)
پێناسە_نرخ.loader.exec_module(모듈)


class 가짜상자:
    def __init__(self, 뿌리):
        self.뿌리 = 뿌리
        self.명령들 = []
        self.가상기계들 = {}
        self.شکستهێنان_نرخ = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.شکستهێنان_نرخ == 인수[1] or (인수[0] == 'make' and self.شکستهێنان_نرخ == 'make'):
            self.شکستهێنان_نرخ = None
            raise 모듈.실행오류('시험용 شکستهێنان_نرخ')
        if 인수[0] == 'make':
            گوزەر = self.뿌리 / 'os/build/kernel.iso'
            گوزەر.parent.mkdir(parents=True, exist_ok=True)
            گوزەر.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        ئاکشن = 인수[1]
        if ئاکشن == 'list':
            return '\n'.join('"{}" {{{}}}'.format(نرخ['name'], پێرست) for پێرست, نرخ in self.가상기계들.items())
        if ئاکشن == 'createvm':
            پێرست, ناو = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[پێرست] = {'UUID': پێرست, 'name': ناو, 'VMState': 'poweroff',
                'CfgFile': str(self.뿌리 / '.vbox/machines' / ناو / (ناو + '.vbox')), 'owner': None}
            return ''
        مەکینه = self.가상기계들[인수[2]]
        if ئاکشن == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(ناو), json.dumps(نرخ)) for ناو, نرخ in مەکینه.items() if ناو != 'owner')
        if ئاکشن == 'getextradata': return 'Value: ' + مەکینه['owner'] if مەکینه['owner'] else 'No value set!'
        if ئاکشن == 'setextradata': مەکینه['owner'] = 인수[4]
        elif ئاکشن == 'storagectl': مەکینه['storagecontrollername0'] = 'JKOROS IDE'
        elif ئاکشن == 'storageattach': مەکینه['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif ئاکشن == 'startvm': مەکینه['VMState'] = 'running'
        elif ئاکشن == 'controlvm':
            assert 인수[3] == 'resume'
            مەکینه['VMState'] = 'running'
        elif ئاکشن != 'modifyvm': raise AssertionError(인수)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.뿌리 = Path(self.임시.name)
        (self.뿌리 / '.vbox').mkdir()
        self.상자 = 가짜상자(self.뿌리)
        self.جێبەجێکردن_فەرمان = 모듈.بەرنامە_ئەندامی_ستاف(self.뿌리, 'jkoros operating system', فەرمان=self.상자)

    def دروستکردن_تێنووسین(self):
        결과 = self.جێبەجێکردن_فەرمان.جێبەجێکردن_فەرمان()
        self.상자.명령들.clear()
        return self.상자.가상기계들[결과['uuid']]

    def 변경없음(self):
        self.assertTrue(all(فەرمان[0] == 'VBoxManage' and فەرمان[1] in ('list', 'showvminfo', 'getextradata') for فەرمان in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        결과 = self.جێبەجێکردن_فەرمان.جێبەجێکردن_فەرمان()
        self.assertEqual(결과['state'], 'running')
        self.assertTrue(Path(결과['iso']).is_file())
        self.assertTrue(any('--nic1' in فەرمان and 'none' in فەرمان for فەرمان in self.상자.명령들))
        self.assertFalse(any('hdd' in فەرمان or 'discardstate' in فەرمان or 'createmedium' in فەرمان for فەرمان in self.상자.명령들))

    def test_실행중유지(self):
        self.دروستکردن_تێنووسین()
        self.assertEqual(self.جێبەجێکردن_فەرمان.جێبەجێکردن_فەرمان()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        مەکینه = self.دروستکردن_تێنووسین()
        مەکینه['VMState'] = 'saved'
        تۆمار_نرخ = self.جێبەجێکردن_فەرمان.گوزەر(self.جێبەجێکردن_فەرمان.읽기()['serial_log'])
        تۆمار_نرخ.write_text('saved log')
        self.جێبەجێکردن_فەرمان.جێبەجێکردن_فەرمان()
        self.assertFalse(any(فەرمان[0] == 'make' or فەرمان[1] == 'modifyvm' for فەرمان in self.상자.명령들))
        self.assertEqual([گوزەر.read_text() for گوزەر in تۆمار_نرخ.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.دروستکردن_تێنووسین()['VMState'] = 'paused'
        self.جێبەجێکردن_فەرمان.جێبەجێکردن_فەرمان()
        self.assertTrue(any(فەرمان[1] == 'controlvm' and فەرمان[3] == 'resume' for فەرمان in self.상자.명령들))
        self.assertFalse(any(فەرمان[0] == 'make' for فەرمان in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(모듈.실행오류): self.جێبەجێکردن_فەرمان.جێبەجێکردن_فەرمان()
        self.변경없음()

    def test_소유표식거부(self):
        self.دروستکردن_تێنووسین()['owner'] = 'someone-else'
        with self.assertRaises(모듈.실행오류): self.جێبەجێکردن_فەرمان.جێبەجێکردن_فەرمان()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.دروستکردن_تێنووسین()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(모듈.실행오류): self.جێبەجێکردن_فەرمان.جێبەجێکردن_فەرمان()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        مەکینه = self.دروستکردن_تێنووسین()
        مەکینه['VMState'] = 'poweroff'
        مەکینه['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(모듈.실행오류): self.جێبەجێکردن_فەرمان.جێبەجێکردن_فەرمان()
        self.변경없음()

    def test_전환중거부(self):
        self.دروستکردن_تێنووسین()['VMState'] = 'saving'
        with self.assertRaises(모듈.실행오류): self.جێبەجێکردن_فەرمان.جێبەجێکردن_فەرمان()
        self.변경없음()

    def test_등록해제거부(self):
        self.دروستکردن_تێنووسین()
        self.상자.가상기계들.clear()
        with self.assertRaises(모듈.실행오류): self.جێبەجێکردن_فەرمان.جێبەجێکردن_فەرمان()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        مەکینه = self.دروستکردن_تێنووسین()
        مەکینه['VMState'] = 'poweroff'
        이전 = dict(مەکینه)
        self.상자.شکستهێنان_نرخ = 'make'
        with self.assertRaises(모듈.실행오류): self.جێبەجێکردن_فەرمان.جێبەجێکردن_فەرمان()
        self.assertEqual(مەکینه, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.شکستهێنان_نرخ = 'setextradata'
        with self.assertRaises(모듈.실행오류): self.جێبەجێکردن_فەرمان.جێبەجێکردن_فەرمان()
        self.상자.명령들.clear()
        self.assertEqual(self.جێبەجێکردن_فەرمان.جێبەجێکردن_فەرمان()['state'], 'running')
        self.assertFalse(any(فەرمان[1] == 'createvm' for فەرمان in self.상자.명령들))

    def test_보존ISO변조거부(self):
        مەکینه = self.دروستکردن_تێنووسین()
        مەکینه['VMState'] = 'poweroff'
        Path(مەکینه['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(모듈.실행오류): self.جێبەجێکردن_فەرمان.جێبەجێکردن_فەرمان()

    def test_상태미생성(self):
        self.assertEqual(self.جێبەجێکردن_فەرمان.نیشاندان_دۆخ()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for گوزەر in ('../outside', '/tmp/outside'):
            with self.assertRaises(모듈.실행오류): self.جێبەجێکردن_فەرمان.گوزەر(گوزەر)
        (self.뿌리 / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(모듈.실행오류): self.جێبەجێکردن_فەرمان.گوزەر('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        결과 = 모듈.تایبەتمەندی_نرخ('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(결과['VMState'], 'running')
        self.assertEqual(결과['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
