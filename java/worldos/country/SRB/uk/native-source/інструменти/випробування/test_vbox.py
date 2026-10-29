import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Визначення_значення = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
модуль_значення = importlib.util.module_from_spec(Визначення_значення)
Визначення_значення.loader.exec_module(модуль_значення)


class 가짜상자:
    def __init__(self, корінь_значення):
        self.корінь_значення = корінь_значення
        self.명령들 = []
        self.가상기계들 = {}
        self.неполадка_значення = None

    def __call__(self, аргументи):
        аргументи = list(map(str, аргументи))
        self.명령들.append(аргументи)
        if self.неполадка_значення == аргументи[1] or (аргументи[0] == 'make' and self.неполадка_значення == 'make'):
            self.неполадка_значення = None
            raise модуль_значення.실행오류('시험용 неполадка_значення')
        if аргументи[0] == 'make':
            шлях = self.корінь_значення / 'os/build/kernel.iso'
            шлях.parent.mkdir(parents=True, exist_ok=True)
            шлях.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Дія = аргументи[1]
        if Дія == 'list':
            return '\n'.join('"{}" {{{}}}'.format(значення['name'], індекс) for індекс, значення in self.가상기계들.items())
        if Дія == 'createvm':
            індекс, Назва = аргументи[аргументи.index('--uuid') + 1], аргументи[аргументи.index('--name') + 1]
            self.가상기계들[індекс] = {'UUID': індекс, 'name': Назва, 'VMState': 'poweroff',
                'CfgFile': str(self.корінь_значення / '.vbox/machines' / Назва / (Назва + '.vbox')), 'owner': None}
            return ''
        комп_ютер = self.가상기계들[аргументи[2]]
        if Дія == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Назва), json.dumps(значення)) for Назва, значення in комп_ютер.items() if Назва != 'owner')
        if Дія == 'getextradata': return 'Value: ' + комп_ютер['owner'] if комп_ютер['owner'] else 'No value set!'
        if Дія == 'setextradata': комп_ютер['owner'] = аргументи[4]
        elif Дія == 'storagectl': комп_ютер['storagecontrollername0'] = 'JKOROS IDE'
        elif Дія == 'storageattach': комп_ютер['JKOROS IDE-0-0'] = аргументи[аргументи.index('--medium') + 1]
        elif Дія == 'startvm': комп_ютер['VMState'] = 'running'
        elif Дія == 'controlvm':
            assert аргументи[3] == 'resume'
            комп_ютер['VMState'] = 'running'
        elif Дія != 'modifyvm': raise AssertionError(аргументи)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.корінь_значення = Path(self.임시.name)
        (self.корінь_значення / '.vbox').mkdir()
        self.상자 = 가짜상자(self.корінь_значення)
        self.Виконати_команда = модуль_значення.програма_запускач(self.корінь_значення, 'jkoros operating system', команда=self.상자)

    def Створення_запис(self):
        результат = self.Виконати_команда.Виконати_команда()
        self.상자.명령들.clear()
        return self.상자.가상기계들[результат['uuid']]

    def 변경없음(self):
        self.assertTrue(all(команда[0] == 'VBoxManage' and команда[1] in ('list', 'showvminfo', 'getextradata') for команда in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        результат = self.Виконати_команда.Виконати_команда()
        self.assertEqual(результат['state'], 'running')
        self.assertTrue(Path(результат['iso']).is_file())
        self.assertTrue(any('--nic1' in команда and 'none' in команда for команда in self.상자.명령들))
        self.assertFalse(any('hdd' in команда or 'discardstate' in команда or 'createmedium' in команда for команда in self.상자.명령들))

    def test_실행중유지(self):
        self.Створення_запис()
        self.assertEqual(self.Виконати_команда.Виконати_команда()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        комп_ютер = self.Створення_запис()
        комп_ютер['VMState'] = 'saved'
        журнал_значення = self.Виконати_команда.шлях(self.Виконати_команда.Читання()['serial_log'])
        журнал_значення.write_text('saved log')
        self.Виконати_команда.Виконати_команда()
        self.assertFalse(any(команда[0] == 'make' or команда[1] == 'modifyvm' for команда in self.상자.명령들))
        self.assertEqual([шлях.read_text() for шлях in журнал_значення.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.Створення_запис()['VMState'] = 'paused'
        self.Виконати_команда.Виконати_команда()
        self.assertTrue(any(команда[1] == 'controlvm' and команда[3] == 'resume' for команда in self.상자.명령들))
        self.assertFalse(any(команда[0] == 'make' for команда in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(модуль_значення.실행오류): self.Виконати_команда.Виконати_команда()
        self.변경없음()

    def test_소유표식거부(self):
        self.Створення_запис()['owner'] = 'someone-else'
        with self.assertRaises(модуль_значення.실행오류): self.Виконати_команда.Виконати_команда()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.Створення_запис()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(модуль_значення.실행오류): self.Виконати_команда.Виконати_команда()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        комп_ютер = self.Створення_запис()
        комп_ютер['VMState'] = 'poweroff'
        комп_ютер['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(модуль_значення.실행오류): self.Виконати_команда.Виконати_команда()
        self.변경없음()

    def test_전환중거부(self):
        self.Створення_запис()['VMState'] = 'saving'
        with self.assertRaises(модуль_значення.실행오류): self.Виконати_команда.Виконати_команда()
        self.변경없음()

    def test_등록해제거부(self):
        self.Створення_запис()
        self.상자.가상기계들.clear()
        with self.assertRaises(модуль_значення.실행오류): self.Виконати_команда.Виконати_команда()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        комп_ютер = self.Створення_запис()
        комп_ютер['VMState'] = 'poweroff'
        이전 = dict(комп_ютер)
        self.상자.неполадка_значення = 'make'
        with self.assertRaises(модуль_значення.실행오류): self.Виконати_команда.Виконати_команда()
        self.assertEqual(комп_ютер, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.неполадка_значення = 'setextradata'
        with self.assertRaises(модуль_значення.실행오류): self.Виконати_команда.Виконати_команда()
        self.상자.명령들.clear()
        self.assertEqual(self.Виконати_команда.Виконати_команда()['state'], 'running')
        self.assertFalse(any(команда[1] == 'createvm' for команда in self.상자.명령들))

    def test_보존ISO변조거부(self):
        комп_ютер = self.Створення_запис()
        комп_ютер['VMState'] = 'poweroff'
        Path(комп_ютер['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(модуль_значення.실행오류): self.Виконати_команда.Виконати_команда()

    def test_상태미생성(self):
        self.assertEqual(self.Виконати_команда.показувати_Стан()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for шлях in ('../outside', '/tmp/outside'):
            with self.assertRaises(модуль_значення.실행오류): self.Виконати_команда.шлях(шлях)
        (self.корінь_значення / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(модуль_значення.실행오류): self.Виконати_команда.шлях('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        результат = модуль_значення.атрибут_значення('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(результат['VMState'], 'running')
        self.assertEqual(результат['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
