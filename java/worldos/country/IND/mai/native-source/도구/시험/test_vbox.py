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

    def __call__(self, आर्गुमेंट्स):
        आर्गुमेंट्स = list(map(str, आर्गुमेंट्स))
        self.명령들.append(आर्गुमेंट्स)
        if self.실패 == आर्गुमेंट्स[1] or (आर्गुमेंट्स[0] == 'make' and self.실패 == 'make'):
            self.실패 = None
            raise 모듈.실행오류('시험용 실패')
        if आर्गुमेंट्स[0] == 'make':
            पथ = self.뿌리 / 'os/build/kernel.iso'
            पथ.parent.mkdir(parents=True, exist_ok=True)
            पथ.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        क्रिया = आर्गुमेंट्स[1]
        if क्रिया == 'list':
            return '\n'.join('"{}" {{{}}}'.format(값['name'], 번호) for 번호, 값 in self.가상기계들.items())
        if क्रिया == 'createvm':
            번호, नाम = आर्गुमेंट्स[आर्गुमेंट्स.index('--uuid') + 1], आर्गुमेंट्स[आर्गुमेंट्स.index('--name') + 1]
            self.가상기계들[번호] = {'UUID': 번호, 'name': नाम, 'VMState': 'poweroff',
                'CfgFile': str(self.뿌리 / '.vbox/machines' / नाम / (नाम + '.vbox')), 'owner': None}
            return ''
        기계 = self.가상기계들[आर्गुमेंट्स[2]]
        if क्रिया == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(नाम), json.dumps(값)) for नाम, 값 in 기계.items() if नाम != 'owner')
        if क्रिया == 'getextradata': return 'Value: ' + 기계['owner'] if 기계['owner'] else 'No value set!'
        if क्रिया == 'setextradata': 기계['owner'] = आर्गुमेंट्स[4]
        elif क्रिया == 'storagectl': 기계['storagecontrollername0'] = 'JKOROS IDE'
        elif क्रिया == 'storageattach': 기계['JKOROS IDE-0-0'] = आर्गुमेंट्स[आर्गुमेंट्स.index('--medium') + 1]
        elif क्रिया == 'startvm': 기계['VMState'] = 'running'
        elif क्रिया == 'controlvm':
            assert आर्गुमेंट्स[3] == 'resume'
            기계['VMState'] = 'running'
        elif क्रिया != 'modifyvm': raise AssertionError(आर्गुमेंट्स)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.뿌리 = Path(self.임시.name)
        (self.뿌리 / '.vbox').mkdir()
        self.상자 = 가짜상자(self.뿌리)
        self.실행 = 모듈.실행기(self.뿌리, 'jkoros operating system', कमांड=self.상자)

    def 만들기(self):
        결과 = self.실행.실행()
        self.상자.명령들.clear()
        return self.상자.가상기계들[결과['uuid']]

    def 변경없음(self):
        self.assertTrue(all(कमांड[0] == 'VBoxManage' and कमांड[1] in ('list', 'showvminfo', 'getextradata') for कमांड in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        결과 = self.실행.실행()
        self.assertEqual(결과['state'], 'running')
        self.assertTrue(Path(결과['iso']).is_file())
        self.assertTrue(any('--nic1' in कमांड and 'none' in कमांड for कमांड in self.상자.명령들))
        self.assertFalse(any('hdd' in कमांड or 'discardstate' in कमांड or 'createmedium' in कमांड for कमांड in self.상자.명령들))

    def test_실행중유지(self):
        self.만들기()
        self.assertEqual(self.실행.실행()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        기계 = self.만들기()
        기계['VMState'] = 'saved'
        로그 = self.실행.पथ(self.실행.पढ़ू()['serial_log'])
        로그.write_text('saved log')
        self.실행.실행()
        self.assertFalse(any(कमांड[0] == 'make' or कमांड[1] == 'modifyvm' for कमांड in self.상자.명령들))
        self.assertEqual([पथ.read_text() for पथ in 로그.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.만들기()['VMState'] = 'paused'
        self.실행.실행()
        self.assertTrue(any(कमांड[1] == 'controlvm' and कमांड[3] == 'resume' for कमांड in self.상자.명령들))
        self.assertFalse(any(कमांड[0] == 'make' for कमांड in self.상자.명령들))

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
        self.assertFalse(any(कमांड[1] == 'createvm' for कमांड in self.상자.명령들))

    def test_보존ISO변조거부(self):
        기계 = self.만들기()
        기계['VMState'] = 'poweroff'
        Path(기계['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(모듈.실행오류): self.실행.실행()

    def test_상태미생성(self):
        self.assertEqual(self.실행.상태보기()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for पथ in ('../outside', '/tmp/outside'):
            with self.assertRaises(모듈.실행오류): self.실행.पथ(पथ)
        (self.뿌리 / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(모듈.실행오류): self.실행.पथ('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        결과 = 모듈.속성('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(결과['VMState'], 'running')
        self.assertEqual(결과['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
