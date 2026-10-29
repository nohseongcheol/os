import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Определение_ЗНАЧЕН = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
модуль_ЗНАЧЕН = importlib.util.module_from_spec(Определение_ЗНАЧЕН)
Определение_ЗНАЧЕН.loader.exec_module(модуль_ЗНАЧЕН)


class 가짜상자:
    def __init__(self, корень_ЗНАЧЕН):
        self.корень_ЗНАЧЕН = корень_ЗНАЧЕН
        self.명령들 = []
        self.Виртуальные_машины = {}
        self.сбой_ЗНАЧЕН = None

    def __call__(self, аргументы):
        аргументы = list(map(str, аргументы))
        self.명령들.append(аргументы)
        if self.сбой_ЗНАЧЕН == аргументы[1] or (аргументы[0] == 'make' and self.сбой_ЗНАЧЕН == 'make'):
            self.сбой_ЗНАЧЕН = None
            raise модуль_ЗНАЧЕН.выполнение_ошибка('시험용 сбой_ЗНАЧЕН')
        if аргументы[0] == 'make':
            путь = self.корень_ЗНАЧЕН / 'os/build/kernel.iso'
            путь.parent.mkdir(parents=True, exist_ok=True)
            путь.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Действие = аргументы[1]
        if Действие == 'list':
            return '\n'.join('"{}" {{{}}}'.format(ЗНАЧЕН['name'], ИНДЕКС) for ИНДЕКС, ЗНАЧЕН in self.Виртуальные_машины.items())
        if Действие == 'createvm':
            ИНДЕКС, Название = аргументы[аргументы.index('--uuid') + 1], аргументы[аргументы.index('--name') + 1]
            self.Виртуальные_машины[ИНДЕКС] = {'UUID': ИНДЕКС, 'name': Название, 'VMState': 'poweroff',
                'CfgFile': str(self.корень_ЗНАЧЕН / '.vbox/machines' / Название / (Название + '.vbox')), 'owner': None}
            return ''
        компьютер_5eb260fa = self.Виртуальные_машины[аргументы[2]]
        if Действие == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Название), json.dumps(ЗНАЧЕН)) for Название, ЗНАЧЕН in компьютер_5eb260fa.items() if Название != 'owner')
        if Действие == 'getextradata': return 'Value: ' + компьютер_5eb260fa['owner'] if компьютер_5eb260fa['owner'] else 'No value set!'
        if Действие == 'setextradata': компьютер_5eb260fa['owner'] = аргументы[4]
        elif Действие == 'storagectl': компьютер_5eb260fa['storagecontrollername0'] = 'JKOROS IDE'
        elif Действие == 'storageattach': компьютер_5eb260fa['JKOROS IDE-0-0'] = аргументы[аргументы.index('--medium') + 1]
        elif Действие == 'startvm': компьютер_5eb260fa['VMState'] = 'running'
        elif Действие == 'controlvm':
            assert аргументы[3] == 'resume'
            компьютер_5eb260fa['VMState'] = 'running'
        elif Действие != 'modifyvm': raise AssertionError(аргументы)
        return ''


class тестовый_запуск(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.корень_ЗНАЧЕН = Path(self.임시.name)
        (self.корень_ЗНАЧЕН / '.vbox').mkdir()
        self.상자 = 가짜상자(self.корень_ЗНАЧЕН)
        self.실행 = модуль_ЗНАЧЕН.программа_Launcher(self.корень_ЗНАЧЕН, 'jkoros operating system', команда=self.상자)

    def Create_ввод(self):
        результат = self.실행.실행()
        self.상자.명령들.clear()
        return self.상자.Виртуальные_машины[результат['uuid']]

    def 변경없음(self):
        self.assertTrue(all(команда[0] == 'VBoxManage' and команда[1] in ('list', 'showvminfo', 'getextradata') for команда in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        результат = self.실행.실행()
        self.assertEqual(результат['state'], 'running')
        self.assertTrue(Path(результат['iso']).is_file())
        self.assertTrue(any('--nic1' in команда and 'none' in команда for команда in self.상자.명령들))
        self.assertFalse(any('hdd' in команда or 'discardstate' in команда or 'createmedium' in команда for команда in self.상자.명령들))

    def test_실행중유지(self):
        self.Create_ввод()
        self.assertEqual(self.실행.실행()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        компьютер_5eb260fa = self.Create_ввод()
        компьютер_5eb260fa['VMState'] = 'saved'
        LOG_ЗНАЧЕН = self.실행.путь(self.실행.Чтение()['serial_log'])
        LOG_ЗНАЧЕН.write_text('saved log')
        self.실행.실행()
        self.assertFalse(any(команда[0] == 'make' or команда[1] == 'modifyvm' for команда in self.상자.명령들))
        self.assertEqual([путь.read_text() for путь in LOG_ЗНАЧЕН.parent.glob('before-resume-*.log')], ['saved log'])

    def тест_пауза_И_резюме(self):
        self.Create_ввод()['VMState'] = 'paused'
        self.실행.실행()
        self.assertTrue(any(команда[1] == 'controlvm' and команда[3] == 'resume' for команда in self.상자.명령들))
        self.assertFalse(any(команда[0] == 'make' for команда in self.상자.명령들))

    def тест_другое_VM_имя_конфликт(self):
        self.상자.Виртуальные_машины[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(модуль_ЗНАЧЕН.выполнение_ошибка): self.실행.실행()
        self.변경없음()

    def test_소유표식거부(self):
        self.Create_ввод()['owner'] = 'someone-else'
        with self.assertRaises(модуль_ЗНАЧЕН.выполнение_ошибка): self.실행.실행()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.Create_ввод()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(модуль_ЗНАЧЕН.выполнение_ошибка): self.실행.실행()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        компьютер_5eb260fa = self.Create_ввод()
        компьютер_5eb260fa['VMState'] = 'poweroff'
        компьютер_5eb260fa['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(модуль_ЗНАЧЕН.выполнение_ошибка): self.실행.실행()
        self.변경없음()

    def test_전환중거부(self):
        self.Create_ввод()['VMState'] = 'saving'
        with self.assertRaises(модуль_ЗНАЧЕН.выполнение_ошибка): self.실행.실행()
        self.변경없음()

    def test_등록해제거부(self):
        self.Create_ввод()
        self.상자.Виртуальные_машины.clear()
        with self.assertRaises(модуль_ЗНАЧЕН.выполнение_ошибка): self.실행.실행()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        компьютер_5eb260fa = self.Create_ввод()
        компьютер_5eb260fa['VMState'] = 'poweroff'
        Назад_товар = dict(компьютер_5eb260fa)
        self.상자.сбой_ЗНАЧЕН = 'make'
        with self.assertRaises(модуль_ЗНАЧЕН.выполнение_ошибка): self.실행.실행()
        self.assertEqual(компьютер_5eb260fa, Назад_товар)

    def test_중단된소유표식설정복구(self):
        self.상자.сбой_ЗНАЧЕН = 'setextradata'
        with self.assertRaises(модуль_ЗНАЧЕН.выполнение_ошибка): self.실행.실행()
        self.상자.명령들.clear()
        self.assertEqual(self.실행.실행()['state'], 'running')
        self.assertFalse(any(команда[1] == 'createvm' for команда in self.상자.명령들))

    def test_보존ISO변조거부(self):
        компьютер_5eb260fa = self.Create_ввод()
        компьютер_5eb260fa['VMState'] = 'poweroff'
        Path(компьютер_5eb260fa['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(модуль_ЗНАЧЕН.выполнение_ошибка): self.실행.실행()

    def test_상태미생성(self):
        self.assertEqual(self.실행.выпуск_Состояние()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for путь in ('../outside', '/tmp/outside'):
            with self.assertRaises(модуль_ЗНАЧЕН.выполнение_ошибка): self.실행.путь(путь)
        (self.корень_ЗНАЧЕН / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(модуль_ЗНАЧЕН.выполнение_ошибка): self.실행.путь('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        результат = модуль_ЗНАЧЕН.значение_атрибута('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(результат['VMState'], 'running')
        self.assertEqual(результат['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
