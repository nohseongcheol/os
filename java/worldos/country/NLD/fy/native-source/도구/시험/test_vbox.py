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

    def __call__(self, Arguminten):
        Arguminten = list(map(str, Arguminten))
        self.명령들.append(Arguminten)
        if self.실패 == Arguminten[1] or (Arguminten[0] == 'make' and self.실패 == 'make'):
            self.실패 = None
            raise 모듈.실행오류('시험용 실패')
        if Arguminten[0] == 'make':
            경로 = self.뿌리 / 'os/build/kernel.iso'
            경로.parent.mkdir(parents=True, exist_ok=True)
            경로.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Aksje = Arguminten[1]
        if Aksje == 'list':
            return '\n'.join('"{}" {{{}}}'.format(값['name'], 번호) for 번호, 값 in self.가상기계들.items())
        if Aksje == 'createvm':
            번호, Namme = Arguminten[Arguminten.index('--uuid') + 1], Arguminten[Arguminten.index('--name') + 1]
            self.가상기계들[번호] = {'UUID': 번호, 'name': Namme, 'VMState': 'poweroff',
                'CfgFile': str(self.뿌리 / '.vbox/machines' / Namme / (Namme + '.vbox')), 'owner': None}
            return ''
        기계 = self.가상기계들[Arguminten[2]]
        if Aksje == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Namme), json.dumps(값)) for Namme, 값 in 기계.items() if Namme != 'owner')
        if Aksje == 'getextradata': return 'Value: ' + 기계['owner'] if 기계['owner'] else 'No value set!'
        if Aksje == 'setextradata': 기계['owner'] = Arguminten[4]
        elif Aksje == 'storagectl': 기계['storagecontrollername0'] = 'JKOROS IDE'
        elif Aksje == 'storageattach': 기계['JKOROS IDE-0-0'] = Arguminten[Arguminten.index('--medium') + 1]
        elif Aksje == 'startvm': 기계['VMState'] = 'running'
        elif Aksje == 'controlvm':
            assert Arguminten[3] == 'resume'
            기계['VMState'] = 'running'
        elif Aksje != 'modifyvm': raise AssertionError(Arguminten)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.뿌리 = Path(self.임시.name)
        (self.뿌리 / '.vbox').mkdir()
        self.상자 = 가짜상자(self.뿌리)
        self.실행 = 모듈.실행기(self.뿌리, 'jkoros operating system', Kommando=self.상자)

    def 만들기(self):
        결과 = self.실행.실행()
        self.상자.명령들.clear()
        return self.상자.가상기계들[결과['uuid']]

    def 변경없음(self):
        self.assertTrue(all(Kommando[0] == 'VBoxManage' and Kommando[1] in ('list', 'showvminfo', 'getextradata') for Kommando in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        결과 = self.실행.실행()
        self.assertEqual(결과['state'], 'running')
        self.assertTrue(Path(결과['iso']).is_file())
        self.assertTrue(any('--nic1' in Kommando and 'none' in Kommando for Kommando in self.상자.명령들))
        self.assertFalse(any('hdd' in Kommando or 'discardstate' in Kommando or 'createmedium' in Kommando for Kommando in self.상자.명령들))

    def test_실행중유지(self):
        self.만들기()
        self.assertEqual(self.실행.실행()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        기계 = self.만들기()
        기계['VMState'] = 'saved'
        로그 = self.실행.경로(self.실행.Lêze()['serial_log'])
        로그.write_text('saved log')
        self.실행.실행()
        self.assertFalse(any(Kommando[0] == 'make' or Kommando[1] == 'modifyvm' for Kommando in self.상자.명령들))
        self.assertEqual([경로.read_text() for 경로 in 로그.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.만들기()['VMState'] = 'paused'
        self.실행.실행()
        self.assertTrue(any(Kommando[1] == 'controlvm' and Kommando[3] == 'resume' for Kommando in self.상자.명령들))
        self.assertFalse(any(Kommando[0] == 'make' for Kommando in self.상자.명령들))

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
        self.assertFalse(any(Kommando[1] == 'createvm' for Kommando in self.상자.명령들))

    def test_보존ISO변조거부(self):
        기계 = self.만들기()
        기계['VMState'] = 'poweroff'
        Path(기계['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(모듈.실행오류): self.실행.실행()

    def test_상태미생성(self):
        self.assertEqual(self.실행.상태보기()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for 경로 in ('../outside', '/tmp/outside'):
            with self.assertRaises(모듈.실행오류): self.실행.경로(경로)
        (self.뿌리 / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(모듈.실행오류): self.실행.경로('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        결과 = 모듈.속성('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(결과['VMState'], 'running')
        self.assertEqual(결과['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
