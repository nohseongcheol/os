import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

መግለጺ_ዋጋ = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
모듈 = importlib.util.module_from_spec(መግለጺ_ዋጋ)
መግለጺ_ዋጋ.loader.exec_module(모듈)


class 가짜상자:
    def __init__(self, 뿌리):
        self.뿌리 = 뿌리
        self.명령들 = []
        self.가상기계들 = {}
        self.ፍሽለት_ዋጋ = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.ፍሽለት_ዋጋ == 인수[1] or (인수[0] == 'make' and self.ፍሽለት_ዋጋ == 'make'):
            self.ፍሽለት_ዋጋ = None
            raise 모듈.실행오류('시험용 ፍሽለት_ዋጋ')
        if 인수[0] == 'make':
            መገዲ = self.뿌리 / 'os/build/kernel.iso'
            መገዲ.parent.mkdir(parents=True, exist_ok=True)
            መገዲ.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        ስጉምቲ = 인수[1]
        if ስጉምቲ == 'list':
            return '\n'.join('"{}" {{{}}}'.format(ዋጋ['name'], መሐበሪ) for መሐበሪ, ዋጋ in self.가상기계들.items())
        if ስጉምቲ == 'createvm':
            መሐበሪ, ሽም = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[መሐበሪ] = {'UUID': መሐበሪ, 'name': ሽም, 'VMState': 'poweroff',
                'CfgFile': str(self.뿌리 / '.vbox/machines' / ሽም / (ሽም + '.vbox')), 'owner': None}
            return ''
        ማሽን = self.가상기계들[인수[2]]
        if ስጉምቲ == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(ሽም), json.dumps(ዋጋ)) for ሽም, ዋጋ in ማሽን.items() if ሽም != 'owner')
        if ስጉምቲ == 'getextradata': return 'Value: ' + ማሽን['owner'] if ማሽን['owner'] else 'No value set!'
        if ስጉምቲ == 'setextradata': ማሽን['owner'] = 인수[4]
        elif ስጉምቲ == 'storagectl': ማሽን['storagecontrollername0'] = 'JKOROS IDE'
        elif ስጉምቲ == 'storageattach': ማሽን['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif ስጉምቲ == 'startvm': ማሽን['VMState'] = 'running'
        elif ስጉምቲ == 'controlvm':
            assert 인수[3] == 'resume'
            ማሽን['VMState'] = 'running'
        elif ስጉምቲ != 'modifyvm': raise AssertionError(인수)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.뿌리 = Path(self.임시.name)
        (self.뿌리 / '.vbox').mkdir()
        self.상자 = 가짜상자(self.뿌리)
        self.ተግብር_ትእዛዝ = 모듈.መተግበሪ_ተመዛዚ_መተግበሪ(self.뿌리, 'jkoros operating system', ትእዛዝ=self.상자)

    def ፍጠር_ምእታው(self):
        결과 = self.ተግብር_ትእዛዝ.ተግብር_ትእዛዝ()
        self.상자.명령들.clear()
        return self.상자.가상기계들[결과['uuid']]

    def 변경없음(self):
        self.assertTrue(all(ትእዛዝ[0] == 'VBoxManage' and ትእዛዝ[1] in ('list', 'showvminfo', 'getextradata') for ትእዛዝ in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        결과 = self.ተግብር_ትእዛዝ.ተግብር_ትእዛዝ()
        self.assertEqual(결과['state'], 'running')
        self.assertTrue(Path(결과['iso']).is_file())
        self.assertTrue(any('--nic1' in ትእዛዝ and 'none' in ትእዛዝ for ትእዛዝ in self.상자.명령들))
        self.assertFalse(any('hdd' in ትእዛዝ or 'discardstate' in ትእዛዝ or 'createmedium' in ትእዛዝ for ትእዛዝ in self.상자.명령들))

    def test_실행중유지(self):
        self.ፍጠር_ምእታው()
        self.assertEqual(self.ተግብር_ትእዛዝ.ተግብር_ትእዛዝ()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        ማሽን = self.ፍጠር_ምእታው()
        ማሽን['VMState'] = 'saved'
        ምዝጉብ_ዋጋ = self.ተግብር_ትእዛዝ.መገዲ(self.ተግብር_ትእዛዝ.읽기()['serial_log'])
        ምዝጉብ_ዋጋ.write_text('saved log')
        self.ተግብር_ትእዛዝ.ተግብር_ትእዛዝ()
        self.assertFalse(any(ትእዛዝ[0] == 'make' or ትእዛዝ[1] == 'modifyvm' for ትእዛዝ in self.상자.명령들))
        self.assertEqual([መገዲ.read_text() for መገዲ in ምዝጉብ_ዋጋ.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.ፍጠር_ምእታው()['VMState'] = 'paused'
        self.ተግብር_ትእዛዝ.ተግብር_ትእዛዝ()
        self.assertTrue(any(ትእዛዝ[1] == 'controlvm' and ትእዛዝ[3] == 'resume' for ትእዛዝ in self.상자.명령들))
        self.assertFalse(any(ትእዛዝ[0] == 'make' for ትእዛዝ in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(모듈.실행오류): self.ተግብር_ትእዛዝ.ተግብር_ትእዛዝ()
        self.변경없음()

    def test_소유표식거부(self):
        self.ፍጠር_ምእታው()['owner'] = 'someone-else'
        with self.assertRaises(모듈.실행오류): self.ተግብር_ትእዛዝ.ተግብር_ትእዛዝ()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.ፍጠር_ምእታው()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(모듈.실행오류): self.ተግብር_ትእዛዝ.ተግብር_ትእዛዝ()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        ማሽን = self.ፍጠር_ምእታው()
        ማሽን['VMState'] = 'poweroff'
        ማሽን['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(모듈.실행오류): self.ተግብር_ትእዛዝ.ተግብር_ትእዛዝ()
        self.변경없음()

    def test_전환중거부(self):
        self.ፍጠር_ምእታው()['VMState'] = 'saving'
        with self.assertRaises(모듈.실행오류): self.ተግብር_ትእዛዝ.ተግብር_ትእዛዝ()
        self.변경없음()

    def test_등록해제거부(self):
        self.ፍጠር_ምእታው()
        self.상자.가상기계들.clear()
        with self.assertRaises(모듈.실행오류): self.ተግብር_ትእዛዝ.ተግብር_ትእዛዝ()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        ማሽን = self.ፍጠር_ምእታው()
        ማሽን['VMState'] = 'poweroff'
        이전 = dict(ማሽን)
        self.상자.ፍሽለት_ዋጋ = 'make'
        with self.assertRaises(모듈.실행오류): self.ተግብር_ትእዛዝ.ተግብር_ትእዛዝ()
        self.assertEqual(ማሽን, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.ፍሽለት_ዋጋ = 'setextradata'
        with self.assertRaises(모듈.실행오류): self.ተግብር_ትእዛዝ.ተግብር_ትእዛዝ()
        self.상자.명령들.clear()
        self.assertEqual(self.ተግብር_ትእዛዝ.ተግብር_ትእዛዝ()['state'], 'running')
        self.assertFalse(any(ትእዛዝ[1] == 'createvm' for ትእዛዝ in self.상자.명령들))

    def test_보존ISO변조거부(self):
        ማሽን = self.ፍጠር_ምእታው()
        ማሽን['VMState'] = 'poweroff'
        Path(ማሽን['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(모듈.실행오류): self.ተግብር_ትእዛዝ.ተግብር_ትእዛዝ()

    def test_상태미생성(self):
        self.assertEqual(self.ተግብር_ትእዛዝ.ኣርእይ_ደረጃ()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for መገዲ in ('../outside', '/tmp/outside'):
            with self.assertRaises(모듈.실행오류): self.ተግብር_ትእዛዝ.መገዲ(መገዲ)
        (self.뿌리 / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(모듈.실행오류): self.ተግብር_ትእዛዝ.መገዲ('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        결과 = 모듈.ባህሪ_ዋጋ('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(결과['VMState'], 'running')
        self.assertEqual(결과['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
