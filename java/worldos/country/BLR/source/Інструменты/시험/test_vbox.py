import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Азначэнне_значэнне = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
модуль_значэнне = importlib.util.module_from_spec(Азначэнне_значэнне)
Азначэнне_значэнне.loader.exec_module(модуль_значэнне)


class 가짜상자:
    def __init__(self, 뿌리):
        self.뿌리 = 뿌리
        self.명령들 = []
        self.가상기계들 = {}
        self.няўдача_значэнне = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.няўдача_значэнне == 인수[1] or (인수[0] == 'make' and self.няўдача_значэнне == 'make'):
            self.няўдача_значэнне = None
            raise модуль_значэнне.실행오류('시험용 няўдача_значэнне')
        if 인수[0] == 'make':
            ШЛЯХ = self.뿌리 / 'os/build/kernel.iso'
            ШЛЯХ.parent.mkdir(parents=True, exist_ok=True)
            ШЛЯХ.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Дзеянне = 인수[1]
        if Дзеянне == 'list':
            return '\n'.join('"{}" {{{}}}'.format(значэнне['name'], індэкс) for індэкс, значэнне in self.가상기계들.items())
        if Дзеянне == 'createvm':
            індэкс, Назва = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[індэкс] = {'UUID': індэкс, 'name': Назва, 'VMState': 'poweroff',
                'CfgFile': str(self.뿌리 / '.vbox/machines' / Назва / (Назва + '.vbox')), 'owner': None}
            return ''
        камп_ютар = self.가상기계들[인수[2]]
        if Дзеянне == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Назва), json.dumps(значэнне)) for Назва, значэнне in камп_ютар.items() if Назва != 'owner')
        if Дзеянне == 'getextradata': return 'Value: ' + камп_ютар['owner'] if камп_ютар['owner'] else 'No value set!'
        if Дзеянне == 'setextradata': камп_ютар['owner'] = 인수[4]
        elif Дзеянне == 'storagectl': камп_ютар['storagecontrollername0'] = 'JKOROS IDE'
        elif Дзеянне == 'storageattach': камп_ютар['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif Дзеянне == 'startvm': камп_ютар['VMState'] = 'running'
        elif Дзеянне == 'controlvm':
            assert 인수[3] == 'resume'
            камп_ютар['VMState'] = 'running'
        elif Дзеянне != 'modifyvm': raise AssertionError(인수)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.뿌리 = Path(self.임시.name)
        (self.뿌리 / '.vbox').mkdir()
        self.상자 = 가짜상자(self.뿌리)
        self.выканаць_каманда = модуль_значэнне.праграма_выклік_праграм(self.뿌리, 'jkoros operating system', Загад=self.상자)

    def стварыць_увядзенне(self):
        결과 = self.выканаць_каманда.выканаць_каманда()
        self.상자.명령들.clear()
        return self.상자.가상기계들[결과['uuid']]

    def 변경없음(self):
        self.assertTrue(all(Загад[0] == 'VBoxManage' and Загад[1] in ('list', 'showvminfo', 'getextradata') for Загад in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        결과 = self.выканаць_каманда.выканаць_каманда()
        self.assertEqual(결과['state'], 'running')
        self.assertTrue(Path(결과['iso']).is_file())
        self.assertTrue(any('--nic1' in Загад and 'none' in Загад for Загад in self.상자.명령들))
        self.assertFalse(any('hdd' in Загад or 'discardstate' in Загад or 'createmedium' in Загад for Загад in self.상자.명령들))

    def test_실행중유지(self):
        self.стварыць_увядзенне()
        self.assertEqual(self.выканаць_каманда.выканаць_каманда()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        камп_ютар = self.стварыць_увядзенне()
        камп_ютар['VMState'] = 'saved'
        журнал_значэнне = self.выканаць_каманда.ШЛЯХ(self.выканаць_каманда.Чытанне()['serial_log'])
        журнал_значэнне.write_text('saved log')
        self.выканаць_каманда.выканаць_каманда()
        self.assertFalse(any(Загад[0] == 'make' or Загад[1] == 'modifyvm' for Загад in self.상자.명령들))
        self.assertEqual([ШЛЯХ.read_text() for ШЛЯХ in журнал_значэнне.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.стварыць_увядзенне()['VMState'] = 'paused'
        self.выканаць_каманда.выканаць_каманда()
        self.assertTrue(any(Загад[1] == 'controlvm' and Загад[3] == 'resume' for Загад in self.상자.명령들))
        self.assertFalse(any(Загад[0] == 'make' for Загад in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(модуль_значэнне.실행오류): self.выканаць_каманда.выканаць_каманда()
        self.변경없음()

    def test_소유표식거부(self):
        self.стварыць_увядзенне()['owner'] = 'someone-else'
        with self.assertRaises(модуль_значэнне.실행오류): self.выканаць_каманда.выканаць_каманда()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.стварыць_увядзенне()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(модуль_значэнне.실행오류): self.выканаць_каманда.выканаць_каманда()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        камп_ютар = self.стварыць_увядзенне()
        камп_ютар['VMState'] = 'poweroff'
        камп_ютар['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(модуль_значэнне.실행오류): self.выканаць_каманда.выканаць_каманда()
        self.변경없음()

    def test_전환중거부(self):
        self.стварыць_увядзенне()['VMState'] = 'saving'
        with self.assertRaises(модуль_значэнне.실행오류): self.выканаць_каманда.выканаць_каманда()
        self.변경없음()

    def test_등록해제거부(self):
        self.стварыць_увядзенне()
        self.상자.가상기계들.clear()
        with self.assertRaises(модуль_значэнне.실행오류): self.выканаць_каманда.выканаць_каманда()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        камп_ютар = self.стварыць_увядзенне()
        камп_ютар['VMState'] = 'poweroff'
        이전 = dict(камп_ютар)
        self.상자.няўдача_значэнне = 'make'
        with self.assertRaises(модуль_значэнне.실행오류): self.выканаць_каманда.выканаць_каманда()
        self.assertEqual(камп_ютар, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.няўдача_значэнне = 'setextradata'
        with self.assertRaises(модуль_значэнне.실행오류): self.выканаць_каманда.выканаць_каманда()
        self.상자.명령들.clear()
        self.assertEqual(self.выканаць_каманда.выканаць_каманда()['state'], 'running')
        self.assertFalse(any(Загад[1] == 'createvm' for Загад in self.상자.명령들))

    def test_보존ISO변조거부(self):
        камп_ютар = self.стварыць_увядзенне()
        камп_ютар['VMState'] = 'poweroff'
        Path(камп_ютар['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(модуль_значэнне.실행오류): self.выканаць_каманда.выканаць_каманда()

    def test_상태미생성(self):
        self.assertEqual(self.выканаць_каманда.паказаць_стан()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for ШЛЯХ in ('../outside', '/tmp/outside'):
            with self.assertRaises(модуль_значэнне.실행오류): self.выканаць_каманда.ШЛЯХ(ШЛЯХ)
        (self.뿌리 / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(модуль_значэнне.실행오류): self.выканаць_каманда.ШЛЯХ('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        결과 = модуль_значэнне.атрыбут_значэнне('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(결과['VMState'], 'running')
        self.assertEqual(결과['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
