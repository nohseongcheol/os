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

    def __call__(self, Argumentoj):
        Argumentoj = list(map(str, Argumentoj))
        self.명령들.append(Argumentoj)
        if self.실패 == Argumentoj[1] or (Argumentoj[0] == 'make' and self.실패 == 'make'):
            self.실패 = None
            raise 모듈.실행오류('시험용 실패')
        if Argumentoj[0] == 'make':
            Vojo = self.뿌리 / 'os/build/kernel.iso'
            Vojo.parent.mkdir(parents=True, exist_ok=True)
            Vojo.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Ago = Argumentoj[1]
        if Ago == 'list':
            return '\n'.join('"{}" {{{}}}'.format(값['name'], 번호) for 번호, 값 in self.가상기계들.items())
        if Ago == 'createvm':
            번호, Nomo = Argumentoj[Argumentoj.index('--uuid') + 1], Argumentoj[Argumentoj.index('--name') + 1]
            self.가상기계들[번호] = {'UUID': 번호, 'name': Nomo, 'VMState': 'poweroff',
                'CfgFile': str(self.뿌리 / '.vbox/machines' / Nomo / (Nomo + '.vbox')), 'owner': None}
            return ''
        기계 = self.가상기계들[Argumentoj[2]]
        if Ago == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Nomo), json.dumps(값)) for Nomo, 값 in 기계.items() if Nomo != 'owner')
        if Ago == 'getextradata': return 'Value: ' + 기계['owner'] if 기계['owner'] else 'No value set!'
        if Ago == 'setextradata': 기계['owner'] = Argumentoj[4]
        elif Ago == 'storagectl': 기계['storagecontrollername0'] = 'JKOROS IDE'
        elif Ago == 'storageattach': 기계['JKOROS IDE-0-0'] = Argumentoj[Argumentoj.index('--medium') + 1]
        elif Ago == 'startvm': 기계['VMState'] = 'running'
        elif Ago == 'controlvm':
            assert Argumentoj[3] == 'resume'
            기계['VMState'] = 'running'
        elif Ago != 'modifyvm': raise AssertionError(Argumentoj)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.뿌리 = Path(self.임시.name)
        (self.뿌리 / '.vbox').mkdir()
        self.상자 = 가짜상자(self.뿌리)
        self.실행 = 모듈.실행기(self.뿌리, 'jkoros operating system', Komando=self.상자)

    def 만들기(self):
        결과 = self.실행.실행()
        self.상자.명령들.clear()
        return self.상자.가상기계들[결과['uuid']]

    def 변경없음(self):
        self.assertTrue(all(Komando[0] == 'VBoxManage' and Komando[1] in ('list', 'showvminfo', 'getextradata') for Komando in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        결과 = self.실행.실행()
        self.assertEqual(결과['state'], 'running')
        self.assertTrue(Path(결과['iso']).is_file())
        self.assertTrue(any('--nic1' in Komando and 'none' in Komando for Komando in self.상자.명령들))
        self.assertFalse(any('hdd' in Komando or 'discardstate' in Komando or 'createmedium' in Komando for Komando in self.상자.명령들))

    def test_실행중유지(self):
        self.만들기()
        self.assertEqual(self.실행.실행()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        기계 = self.만들기()
        기계['VMState'] = 'saved'
        로그 = self.실행.Vojo(self.실행.Lego()['serial_log'])
        로그.write_text('saved log')
        self.실행.실행()
        self.assertFalse(any(Komando[0] == 'make' or Komando[1] == 'modifyvm' for Komando in self.상자.명령들))
        self.assertEqual([Vojo.read_text() for Vojo in 로그.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.만들기()['VMState'] = 'paused'
        self.실행.실행()
        self.assertTrue(any(Komando[1] == 'controlvm' and Komando[3] == 'resume' for Komando in self.상자.명령들))
        self.assertFalse(any(Komando[0] == 'make' for Komando in self.상자.명령들))

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
        self.assertFalse(any(Komando[1] == 'createvm' for Komando in self.상자.명령들))

    def test_보존ISO변조거부(self):
        기계 = self.만들기()
        기계['VMState'] = 'poweroff'
        Path(기계['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(모듈.실행오류): self.실행.실행()

    def test_상태미생성(self):
        self.assertEqual(self.실행.상태보기()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for Vojo in ('../outside', '/tmp/outside'):
            with self.assertRaises(모듈.실행오류): self.실행.Vojo(Vojo)
        (self.뿌리 / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(모듈.실행오류): self.실행.Vojo('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        결과 = 모듈.속성('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(결과['VMState'], 'running')
        self.assertEqual(결과['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
