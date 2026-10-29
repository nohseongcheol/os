import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

ವಿವರಣೆ_ಮೌಲ್ಯ = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
ಮಾಡ್ಯೂಲ್_ಮೌಲ್ಯ = importlib.util.module_from_spec(ವಿವರಣೆ_ಮೌಲ್ಯ)
ವಿವರಣೆ_ಮೌಲ್ಯ.loader.exec_module(ಮಾಡ್ಯೂಲ್_ಮೌಲ್ಯ)


class 가짜상자:
    def __init__(self, ಮೂಲ_ಮೌಲ್ಯ):
        self.ಮೂಲ_ಮೌಲ್ಯ = ಮೂಲ_ಮೌಲ್ಯ
        self.명령들 = []
        self.가상기계들 = {}
        self.ವೈಫಲ್ಯ_ಮೌಲ್ಯ = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.ವೈಫಲ್ಯ_ಮೌಲ್ಯ == 인수[1] or (인수[0] == 'make' and self.ವೈಫಲ್ಯ_ಮೌಲ್ಯ == 'make'):
            self.ವೈಫಲ್ಯ_ಮೌಲ್ಯ = None
            raise ಮಾಡ್ಯೂಲ್_ಮೌಲ್ಯ.실행오류('시험용 ವೈಫಲ್ಯ_ಮೌಲ್ಯ')
        if 인수[0] == 'make':
            ಮಾರ್ಗ = self.ಮೂಲ_ಮೌಲ್ಯ / 'os/build/kernel.iso'
            ಮಾರ್ಗ.parent.mkdir(parents=True, exist_ok=True)
            ಮಾರ್ಗ.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        ಹಕ್ರಿಯೆ = 인수[1]
        if ಹಕ್ರಿಯೆ == 'list':
            return '\n'.join('"{}" {{{}}}'.format(ಮೌಲ್ಯ['name'], ಪದಸೂಚಿ) for ಪದಸೂಚಿ, ಮೌಲ್ಯ in self.가상기계들.items())
        if ಹಕ್ರಿಯೆ == 'createvm':
            ಪದಸೂಚಿ, ಹೆಸರು = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[ಪದಸೂಚಿ] = {'UUID': ಪದಸೂಚಿ, 'name': ಹೆಸರು, 'VMState': 'poweroff',
                'CfgFile': str(self.ಮೂಲ_ಮೌಲ್ಯ / '.vbox/machines' / ಹೆಸರು / (ಹೆಸರು + '.vbox')), 'owner': None}
            return ''
        ಯಂತ್ರ = self.가상기계들[인수[2]]
        if ಹಕ್ರಿಯೆ == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(ಹೆಸರು), json.dumps(ಮೌಲ್ಯ)) for ಹೆಸರು, ಮೌಲ್ಯ in ಯಂತ್ರ.items() if ಹೆಸರು != 'owner')
        if ಹಕ್ರಿಯೆ == 'getextradata': return 'Value: ' + ಯಂತ್ರ['owner'] if ಯಂತ್ರ['owner'] else 'No value set!'
        if ಹಕ್ರಿಯೆ == 'setextradata': ಯಂತ್ರ['owner'] = 인수[4]
        elif ಹಕ್ರಿಯೆ == 'storagectl': ಯಂತ್ರ['storagecontrollername0'] = 'JKOROS IDE'
        elif ಹಕ್ರಿಯೆ == 'storageattach': ಯಂತ್ರ['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif ಹಕ್ರಿಯೆ == 'startvm': ಯಂತ್ರ['VMState'] = 'running'
        elif ಹಕ್ರಿಯೆ == 'controlvm':
            assert 인수[3] == 'resume'
            ಯಂತ್ರ['VMState'] = 'running'
        elif ಹಕ್ರಿಯೆ != 'modifyvm': raise AssertionError(인수)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.ಮೂಲ_ಮೌಲ್ಯ = Path(self.임시.name)
        (self.ಮೂಲ_ಮೌಲ್ಯ / '.vbox').mkdir()
        self.상자 = 가짜상자(self.ಮೂಲ_ಮೌಲ್ಯ)
        self.ಪೂರೈಸು_ಆದೇಶ = ಮಾಡ್ಯೂಲ್_ಮೌಲ್ಯ.ಅಪ್ಲಿ_ಲಾಂಚರ್(self.ಮೂಲ_ಮೌಲ್ಯ, 'jkoros operating system', ಆಜ್ಞೆ=self.상자)

    def ರಚಿಸು_ನಮೂದು(self):
        ಮಾಪನ = self.ಪೂರೈಸು_ಆದೇಶ.ಪೂರೈಸು_ಆದೇಶ()
        self.상자.명령들.clear()
        return self.상자.가상기계들[ಮಾಪನ['uuid']]

    def 변경없음(self):
        self.assertTrue(all(ಆಜ್ಞೆ[0] == 'VBoxManage' and ಆಜ್ಞೆ[1] in ('list', 'showvminfo', 'getextradata') for ಆಜ್ಞೆ in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        ಮಾಪನ = self.ಪೂರೈಸು_ಆದೇಶ.ಪೂರೈಸು_ಆದೇಶ()
        self.assertEqual(ಮಾಪನ['state'], 'running')
        self.assertTrue(Path(ಮಾಪನ['iso']).is_file())
        self.assertTrue(any('--nic1' in ಆಜ್ಞೆ and 'none' in ಆಜ್ಞೆ for ಆಜ್ಞೆ in self.상자.명령들))
        self.assertFalse(any('hdd' in ಆಜ್ಞೆ or 'discardstate' in ಆಜ್ಞೆ or 'createmedium' in ಆಜ್ಞೆ for ಆಜ್ಞೆ in self.상자.명령들))

    def test_실행중유지(self):
        self.ರಚಿಸು_ನಮೂದು()
        self.assertEqual(self.ಪೂರೈಸು_ಆದೇಶ.ಪೂರೈಸು_ಆದೇಶ()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        ಯಂತ್ರ = self.ರಚಿಸು_ನಮೂದು()
        ಯಂತ್ರ['VMState'] = 'saved'
        ಲಾಗ್_ಮೌಲ್ಯ = self.ಪೂರೈಸು_ಆದೇಶ.ಮಾರ್ಗ(self.ಪೂರೈಸು_ಆದೇಶ.ಓದು()['serial_log'])
        ಲಾಗ್_ಮೌಲ್ಯ.write_text('saved log')
        self.ಪೂರೈಸು_ಆದೇಶ.ಪೂರೈಸು_ಆದೇಶ()
        self.assertFalse(any(ಆಜ್ಞೆ[0] == 'make' or ಆಜ್ಞೆ[1] == 'modifyvm' for ಆಜ್ಞೆ in self.상자.명령들))
        self.assertEqual([ಮಾರ್ಗ.read_text() for ಮಾರ್ಗ in ಲಾಗ್_ಮೌಲ್ಯ.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.ರಚಿಸು_ನಮೂದು()['VMState'] = 'paused'
        self.ಪೂರೈಸು_ಆದೇಶ.ಪೂರೈಸು_ಆದೇಶ()
        self.assertTrue(any(ಆಜ್ಞೆ[1] == 'controlvm' and ಆಜ್ಞೆ[3] == 'resume' for ಆಜ್ಞೆ in self.상자.명령들))
        self.assertFalse(any(ಆಜ್ಞೆ[0] == 'make' for ಆಜ್ಞೆ in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(ಮಾಡ್ಯೂಲ್_ಮೌಲ್ಯ.실행오류): self.ಪೂರೈಸು_ಆದೇಶ.ಪೂರೈಸು_ಆದೇಶ()
        self.변경없음()

    def test_소유표식거부(self):
        self.ರಚಿಸು_ನಮೂದು()['owner'] = 'someone-else'
        with self.assertRaises(ಮಾಡ್ಯೂಲ್_ಮೌಲ್ಯ.실행오류): self.ಪೂರೈಸು_ಆದೇಶ.ಪೂರೈಸು_ಆದೇಶ()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.ರಚಿಸು_ನಮೂದು()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(ಮಾಡ್ಯೂಲ್_ಮೌಲ್ಯ.실행오류): self.ಪೂರೈಸು_ಆದೇಶ.ಪೂರೈಸು_ಆದೇಶ()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        ಯಂತ್ರ = self.ರಚಿಸು_ನಮೂದು()
        ಯಂತ್ರ['VMState'] = 'poweroff'
        ಯಂತ್ರ['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(ಮಾಡ್ಯೂಲ್_ಮೌಲ್ಯ.실행오류): self.ಪೂರೈಸು_ಆದೇಶ.ಪೂರೈಸು_ಆದೇಶ()
        self.변경없음()

    def test_전환중거부(self):
        self.ರಚಿಸು_ನಮೂದು()['VMState'] = 'saving'
        with self.assertRaises(ಮಾಡ್ಯೂಲ್_ಮೌಲ್ಯ.실행오류): self.ಪೂರೈಸು_ಆದೇಶ.ಪೂರೈಸು_ಆದೇಶ()
        self.변경없음()

    def test_등록해제거부(self):
        self.ರಚಿಸು_ನಮೂದು()
        self.상자.가상기계들.clear()
        with self.assertRaises(ಮಾಡ್ಯೂಲ್_ಮೌಲ್ಯ.실행오류): self.ಪೂರೈಸು_ಆದೇಶ.ಪೂರೈಸು_ಆದೇಶ()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        ಯಂತ್ರ = self.ರಚಿಸು_ನಮೂದು()
        ಯಂತ್ರ['VMState'] = 'poweroff'
        이전 = dict(ಯಂತ್ರ)
        self.상자.ವೈಫಲ್ಯ_ಮೌಲ್ಯ = 'make'
        with self.assertRaises(ಮಾಡ್ಯೂಲ್_ಮೌಲ್ಯ.실행오류): self.ಪೂರೈಸು_ಆದೇಶ.ಪೂರೈಸು_ಆದೇಶ()
        self.assertEqual(ಯಂತ್ರ, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.ವೈಫಲ್ಯ_ಮೌಲ್ಯ = 'setextradata'
        with self.assertRaises(ಮಾಡ್ಯೂಲ್_ಮೌಲ್ಯ.실행오류): self.ಪೂರೈಸು_ಆದೇಶ.ಪೂರೈಸು_ಆದೇಶ()
        self.상자.명령들.clear()
        self.assertEqual(self.ಪೂರೈಸು_ಆದೇಶ.ಪೂರೈಸು_ಆದೇಶ()['state'], 'running')
        self.assertFalse(any(ಆಜ್ಞೆ[1] == 'createvm' for ಆಜ್ಞೆ in self.상자.명령들))

    def test_보존ISO변조거부(self):
        ಯಂತ್ರ = self.ರಚಿಸು_ನಮೂದು()
        ಯಂತ್ರ['VMState'] = 'poweroff'
        Path(ಯಂತ್ರ['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(ಮಾಡ್ಯೂಲ್_ಮೌಲ್ಯ.실행오류): self.ಪೂರೈಸು_ಆದೇಶ.ಪೂರೈಸು_ಆದೇಶ()

    def test_상태미생성(self):
        self.assertEqual(self.ಪೂರೈಸು_ಆದೇಶ.ಶೋ_ಸ್ಥಿತಿ()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for ಮಾರ್ಗ in ('../outside', '/tmp/outside'):
            with self.assertRaises(ಮಾಡ್ಯೂಲ್_ಮೌಲ್ಯ.실행오류): self.ಪೂರೈಸು_ಆದೇಶ.ಮಾರ್ಗ(ಮಾರ್ಗ)
        (self.ಮೂಲ_ಮೌಲ್ಯ / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(ಮಾಡ್ಯೂಲ್_ಮೌಲ್ಯ.실행오류): self.ಪೂರೈಸು_ಆದೇಶ.ಮಾರ್ಗ('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        ಮಾಪನ = ಮಾಡ್ಯೂಲ್_ಮೌಲ್ಯ.ವಿಶೇಷಣ_ಮೌಲ್ಯ('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(ಮಾಪನ['VMState'], 'running')
        self.assertEqual(ಮಾಪನ['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
