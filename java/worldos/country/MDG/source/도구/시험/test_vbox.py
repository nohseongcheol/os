import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

정의 = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
모듈 = importlib.util.module_from_spec(정의)
정의.loader.exec_module(모듈)


class 가짜상자:
    def __init__(self, 뿌리):
        self.뿌리 = 뿌리
        self.명령들 = []
        self.가상기계들 = {}
        self.실패 = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.실패 == 인수[1] or (인수[0] == 'make' and self.실패 == 'make'):
            self.실패 = None
            raise 모듈.실행오류('시험용 실패')
        if 인수[0] == 'make':
            LALANA = self.뿌리 / 'os/build/kernel.iso'
            LALANA.parent.mkdir(parents=True, exist_ok=True)
            LALANA.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Asa = 인수[1]
        if Asa == 'list':
            return '\n'.join('"{}" {{{}}}'.format(값['name'], 번호) for 번호, 값 in self.가상기계들.items())
        if Asa == 'createvm':
            번호, Anarana = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[번호] = {'UUID': 번호, 'name': Anarana, 'VMState': 'poweroff',
                'CfgFile': str(self.뿌리 / '.vbox/machines' / Anarana / (Anarana + '.vbox')), 'owner': None}
            return ''
        기계 = self.가상기계들[인수[2]]
        if Asa == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Anarana), json.dumps(값)) for Anarana, 값 in 기계.items() if Anarana != 'owner')
        if Asa == 'getextradata': return 'Value: ' + 기계['owner'] if 기계['owner'] else 'No value set!'
        if Asa == 'setextradata': 기계['owner'] = 인수[4]
        elif Asa == 'storagectl': 기계['storagecontrollername0'] = 'JKOROS IDE'
        elif Asa == 'storageattach': 기계['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif Asa == 'startvm': 기계['VMState'] = 'running'
        elif Asa == 'controlvm':
            assert 인수[3] == 'resume'
            기계['VMState'] = 'running'
        elif Asa != 'modifyvm': raise AssertionError(인수)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.뿌리 = Path(self.임시.name)
        (self.뿌리 / '.vbox').mkdir()
        self.상자 = 가짜상자(self.뿌리)
        self.실행 = 모듈.실행기(self.뿌리, 'jkoros operating system', Baiko=self.상자)

    def 만들기(self):
        결과 = self.실행.실행()
        self.상자.명령들.clear()
        return self.상자.가상기계들[결과['uuid']]

    def 변경없음(self):
        self.assertTrue(all(Baiko[0] == 'VBoxManage' and Baiko[1] in ('list', 'showvminfo', 'getextradata') for Baiko in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        결과 = self.실행.실행()
        self.assertEqual(결과['state'], 'running')
        self.assertTrue(Path(결과['iso']).is_file())
        self.assertTrue(any('--nic1' in Baiko and 'none' in Baiko for Baiko in self.상자.명령들))
        self.assertFalse(any('hdd' in Baiko or 'discardstate' in Baiko or 'createmedium' in Baiko for Baiko in self.상자.명령들))

    def test_실행중유지(self):
        self.만들기()
        self.assertEqual(self.실행.실행()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        기계 = self.만들기()
        기계['VMState'] = 'saved'
        로그 = self.실행.LALANA(self.실행.Mamaky()['serial_log'])
        로그.write_text('saved log')
        self.실행.실행()
        self.assertFalse(any(Baiko[0] == 'make' or Baiko[1] == 'modifyvm' for Baiko in self.상자.명령들))
        self.assertEqual([LALANA.read_text() for LALANA in 로그.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.만들기()['VMState'] = 'paused'
        self.실행.실행()
        self.assertTrue(any(Baiko[1] == 'controlvm' and Baiko[3] == 'resume' for Baiko in self.상자.명령들))
        self.assertFalse(any(Baiko[0] == 'make' for Baiko in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(모듈.실행오류): self.실행.실행()
        self.변경없음()

    def test_소유표식거부(self):
        self.만들기()['owner'] = 'someone-else'
        with self.assertRaises(모듈.실행오류): self.실행.실행()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.만들기()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(모듈.실행오류): self.실행.실행()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        기계 = self.만들기()
        기계['VMState'] = 'poweroff'
        기계['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(모듈.실행오류): self.실행.실행()
        self.변경없음()

    def test_전환중거부(self):
        self.만들기()['VMState'] = 'saving'
        with self.assertRaises(모듈.실행오류): self.실행.실행()
        self.변경없음()

    def test_등록해제거부(self):
        self.만들기()
        self.상자.가상기계들.clear()
        with self.assertRaises(모듈.실행오류): self.실행.실행()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        기계 = self.만들기()
        기계['VMState'] = 'poweroff'
        이전 = dict(기계)
        self.상자.실패 = 'make'
        with self.assertRaises(모듈.실행오류): self.실행.실행()
        self.assertEqual(기계, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.실패 = 'setextradata'
        with self.assertRaises(모듈.실행오류): self.실행.실행()
        self.상자.명령들.clear()
        self.assertEqual(self.실행.실행()['state'], 'running')
        self.assertFalse(any(Baiko[1] == 'createvm' for Baiko in self.상자.명령들))

    def test_보존ISO변조거부(self):
        기계 = self.만들기()
        기계['VMState'] = 'poweroff'
        Path(기계['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(모듈.실행오류): self.실행.실행()

    def test_상태미생성(self):
        self.assertEqual(self.실행.상태보기()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for LALANA in ('../outside', '/tmp/outside'):
            with self.assertRaises(모듈.실행오류): self.실행.LALANA(LALANA)
        (self.뿌리 / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(모듈.실행오류): self.실행.LALANA('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        결과 = 모듈.속성('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(결과['VMState'], 'running')
        self.assertEqual(결과['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
