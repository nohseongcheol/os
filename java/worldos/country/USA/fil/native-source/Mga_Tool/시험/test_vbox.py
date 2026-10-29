import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Kahulugan_VALUE = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
module_VALUE = importlib.util.module_from_spec(Kahulugan_VALUE)
Kahulugan_VALUE.loader.exec_module(module_VALUE)


class 가짜상자:
    def __init__(self, root_VALUE):
        self.root_VALUE = root_VALUE
        self.명령들 = []
        self.가상기계들 = {}
        self.pagpalya_VALUE = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.pagpalya_VALUE == 인수[1] or (인수[0] == 'make' and self.pagpalya_VALUE == 'make'):
            self.pagpalya_VALUE = None
            raise module_VALUE.실행오류('시험용 pagpalya_VALUE')
        if 인수[0] == 'make':
            path = self.root_VALUE / 'os/build/kernel.iso'
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        aksyon = 인수[1]
        if aksyon == 'list':
            return '\n'.join('"{}" {{{}}}'.format(VALUE['name'], INDEX) for INDEX, VALUE in self.가상기계들.items())
        if aksyon == 'createvm':
            INDEX, pangalan = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[INDEX] = {'UUID': INDEX, 'name': pangalan, 'VMState': 'poweroff',
                'CfgFile': str(self.root_VALUE / '.vbox/machines' / pangalan / (pangalan + '.vbox')), 'owner': None}
            return ''
        machine = self.가상기계들[인수[2]]
        if aksyon == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(pangalan), json.dumps(VALUE)) for pangalan, VALUE in machine.items() if pangalan != 'owner')
        if aksyon == 'getextradata': return 'Value: ' + machine['owner'] if machine['owner'] else 'No value set!'
        if aksyon == 'setextradata': machine['owner'] = 인수[4]
        elif aksyon == 'storagectl': machine['storagecontrollername0'] = 'JKOROS IDE'
        elif aksyon == 'storageattach': machine['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif aksyon == 'startvm': machine['VMState'] = 'running'
        elif aksyon == 'controlvm':
            assert 인수[3] == 'resume'
            machine['VMState'] = 'running'
        elif aksyon != 'modifyvm': raise AssertionError(인수)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.root_VALUE = Path(self.임시.name)
        (self.root_VALUE / '.vbox').mkdir()
        self.상자 = 가짜상자(self.root_VALUE)
        self.Mag_execute_utos = module_VALUE.app_launcher(self.root_VALUE, 'jkoros operating system', utos=self.상자)

    def Create_pagpasok(self):
        sukat = self.Mag_execute_utos.Mag_execute_utos()
        self.상자.명령들.clear()
        return self.상자.가상기계들[sukat['uuid']]

    def 변경없음(self):
        self.assertTrue(all(utos[0] == 'VBoxManage' and utos[1] in ('list', 'showvminfo', 'getextradata') for utos in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        sukat = self.Mag_execute_utos.Mag_execute_utos()
        self.assertEqual(sukat['state'], 'running')
        self.assertTrue(Path(sukat['iso']).is_file())
        self.assertTrue(any('--nic1' in utos and 'none' in utos for utos in self.상자.명령들))
        self.assertFalse(any('hdd' in utos or 'discardstate' in utos or 'createmedium' in utos for utos in self.상자.명령들))

    def test_실행중유지(self):
        self.Create_pagpasok()
        self.assertEqual(self.Mag_execute_utos.Mag_execute_utos()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        machine = self.Create_pagpasok()
        machine['VMState'] = 'saved'
        LOG_VALUE = self.Mag_execute_utos.path(self.Mag_execute_utos.읽기()['serial_log'])
        LOG_VALUE.write_text('saved log')
        self.Mag_execute_utos.Mag_execute_utos()
        self.assertFalse(any(utos[0] == 'make' or utos[1] == 'modifyvm' for utos in self.상자.명령들))
        self.assertEqual([path.read_text() for path in LOG_VALUE.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.Create_pagpasok()['VMState'] = 'paused'
        self.Mag_execute_utos.Mag_execute_utos()
        self.assertTrue(any(utos[1] == 'controlvm' and utos[3] == 'resume' for utos in self.상자.명령들))
        self.assertFalse(any(utos[0] == 'make' for utos in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(module_VALUE.실행오류): self.Mag_execute_utos.Mag_execute_utos()
        self.변경없음()

    def test_소유표식거부(self):
        self.Create_pagpasok()['owner'] = 'someone-else'
        with self.assertRaises(module_VALUE.실행오류): self.Mag_execute_utos.Mag_execute_utos()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.Create_pagpasok()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(module_VALUE.실행오류): self.Mag_execute_utos.Mag_execute_utos()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        machine = self.Create_pagpasok()
        machine['VMState'] = 'poweroff'
        machine['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(module_VALUE.실행오류): self.Mag_execute_utos.Mag_execute_utos()
        self.변경없음()

    def test_전환중거부(self):
        self.Create_pagpasok()['VMState'] = 'saving'
        with self.assertRaises(module_VALUE.실행오류): self.Mag_execute_utos.Mag_execute_utos()
        self.변경없음()

    def test_등록해제거부(self):
        self.Create_pagpasok()
        self.상자.가상기계들.clear()
        with self.assertRaises(module_VALUE.실행오류): self.Mag_execute_utos.Mag_execute_utos()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        machine = self.Create_pagpasok()
        machine['VMState'] = 'poweroff'
        이전 = dict(machine)
        self.상자.pagpalya_VALUE = 'make'
        with self.assertRaises(module_VALUE.실행오류): self.Mag_execute_utos.Mag_execute_utos()
        self.assertEqual(machine, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.pagpalya_VALUE = 'setextradata'
        with self.assertRaises(module_VALUE.실행오류): self.Mag_execute_utos.Mag_execute_utos()
        self.상자.명령들.clear()
        self.assertEqual(self.Mag_execute_utos.Mag_execute_utos()['state'], 'running')
        self.assertFalse(any(utos[1] == 'createvm' for utos in self.상자.명령들))

    def test_보존ISO변조거부(self):
        machine = self.Create_pagpasok()
        machine['VMState'] = 'poweroff'
        Path(machine['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(module_VALUE.실행오류): self.Mag_execute_utos.Mag_execute_utos()

    def test_상태미생성(self):
        self.assertEqual(self.Mag_execute_utos.ipakita_katayuan()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for path in ('../outside', '/tmp/outside'):
            with self.assertRaises(module_VALUE.실행오류): self.Mag_execute_utos.path(path)
        (self.root_VALUE / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(module_VALUE.실행오류): self.Mag_execute_utos.path('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        sukat = module_VALUE.katangian_VALUE('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(sukat['VMState'], 'running')
        self.assertEqual(sukat['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
