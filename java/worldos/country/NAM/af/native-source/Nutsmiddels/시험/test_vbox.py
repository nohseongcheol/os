import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Definisie_VALUE = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
module_VALUE = importlib.util.module_from_spec(Definisie_VALUE)
Definisie_VALUE.loader.exec_module(module_VALUE)


class 가짜상자:
    def __init__(self, wortel_VALUE):
        self.wortel_VALUE = wortel_VALUE
        self.명령들 = []
        self.가상기계들 = {}
        self.faling_VALUE = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.faling_VALUE == 인수[1] or (인수[0] == 'make' and self.faling_VALUE == 'make'):
            self.faling_VALUE = None
            raise module_VALUE.실행오류('시험용 faling_VALUE')
        if 인수[0] == 'make':
            Pad = self.wortel_VALUE / 'os/build/kernel.iso'
            Pad.parent.mkdir(parents=True, exist_ok=True)
            Pad.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Aksie = 인수[1]
        if Aksie == 'list':
            return '\n'.join('"{}" {{{}}}'.format(VALUE['name'], INDEX) for INDEX, VALUE in self.가상기계들.items())
        if Aksie == 'createvm':
            INDEX, Naam = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[INDEX] = {'UUID': INDEX, 'name': Naam, 'VMState': 'poweroff',
                'CfgFile': str(self.wortel_VALUE / '.vbox/machines' / Naam / (Naam + '.vbox')), 'owner': None}
            return ''
        masjien = self.가상기계들[인수[2]]
        if Aksie == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Naam), json.dumps(VALUE)) for Naam, VALUE in masjien.items() if Naam != 'owner')
        if Aksie == 'getextradata': return 'Value: ' + masjien['owner'] if masjien['owner'] else 'No value set!'
        if Aksie == 'setextradata': masjien['owner'] = 인수[4]
        elif Aksie == 'storagectl': masjien['storagecontrollername0'] = 'JKOROS IDE'
        elif Aksie == 'storageattach': masjien['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif Aksie == 'startvm': masjien['VMState'] = 'running'
        elif Aksie == 'controlvm':
            assert 인수[3] == 'resume'
            masjien['VMState'] = 'running'
        elif Aksie != 'modifyvm': raise AssertionError(인수)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.wortel_VALUE = Path(self.임시.name)
        (self.wortel_VALUE / '.vbox').mkdir()
        self.상자 = 가짜상자(self.wortel_VALUE)
        self.uitvoer_bevel = module_VALUE.program_oopmaker(self.wortel_VALUE, 'jkoros operating system', Opdrag=self.상자)

    def Skep_inskrywing(self):
        maatreël = self.uitvoer_bevel.uitvoer_bevel()
        self.상자.명령들.clear()
        return self.상자.가상기계들[maatreël['uuid']]

    def 변경없음(self):
        self.assertTrue(all(Opdrag[0] == 'VBoxManage' and Opdrag[1] in ('list', 'showvminfo', 'getextradata') for Opdrag in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        maatreël = self.uitvoer_bevel.uitvoer_bevel()
        self.assertEqual(maatreël['state'], 'running')
        self.assertTrue(Path(maatreël['iso']).is_file())
        self.assertTrue(any('--nic1' in Opdrag and 'none' in Opdrag for Opdrag in self.상자.명령들))
        self.assertFalse(any('hdd' in Opdrag or 'discardstate' in Opdrag or 'createmedium' in Opdrag for Opdrag in self.상자.명령들))

    def test_실행중유지(self):
        self.Skep_inskrywing()
        self.assertEqual(self.uitvoer_bevel.uitvoer_bevel()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        masjien = self.Skep_inskrywing()
        masjien['VMState'] = 'saved'
        LOG_VALUE = self.uitvoer_bevel.Pad(self.uitvoer_bevel.Lees()['serial_log'])
        LOG_VALUE.write_text('saved log')
        self.uitvoer_bevel.uitvoer_bevel()
        self.assertFalse(any(Opdrag[0] == 'make' or Opdrag[1] == 'modifyvm' for Opdrag in self.상자.명령들))
        self.assertEqual([Pad.read_text() for Pad in LOG_VALUE.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.Skep_inskrywing()['VMState'] = 'paused'
        self.uitvoer_bevel.uitvoer_bevel()
        self.assertTrue(any(Opdrag[1] == 'controlvm' and Opdrag[3] == 'resume' for Opdrag in self.상자.명령들))
        self.assertFalse(any(Opdrag[0] == 'make' for Opdrag in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(module_VALUE.실행오류): self.uitvoer_bevel.uitvoer_bevel()
        self.변경없음()

    def test_소유표식거부(self):
        self.Skep_inskrywing()['owner'] = 'someone-else'
        with self.assertRaises(module_VALUE.실행오류): self.uitvoer_bevel.uitvoer_bevel()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.Skep_inskrywing()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(module_VALUE.실행오류): self.uitvoer_bevel.uitvoer_bevel()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        masjien = self.Skep_inskrywing()
        masjien['VMState'] = 'poweroff'
        masjien['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(module_VALUE.실행오류): self.uitvoer_bevel.uitvoer_bevel()
        self.변경없음()

    def test_전환중거부(self):
        self.Skep_inskrywing()['VMState'] = 'saving'
        with self.assertRaises(module_VALUE.실행오류): self.uitvoer_bevel.uitvoer_bevel()
        self.변경없음()

    def test_등록해제거부(self):
        self.Skep_inskrywing()
        self.상자.가상기계들.clear()
        with self.assertRaises(module_VALUE.실행오류): self.uitvoer_bevel.uitvoer_bevel()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        masjien = self.Skep_inskrywing()
        masjien['VMState'] = 'poweroff'
        이전 = dict(masjien)
        self.상자.faling_VALUE = 'make'
        with self.assertRaises(module_VALUE.실행오류): self.uitvoer_bevel.uitvoer_bevel()
        self.assertEqual(masjien, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.faling_VALUE = 'setextradata'
        with self.assertRaises(module_VALUE.실행오류): self.uitvoer_bevel.uitvoer_bevel()
        self.상자.명령들.clear()
        self.assertEqual(self.uitvoer_bevel.uitvoer_bevel()['state'], 'running')
        self.assertFalse(any(Opdrag[1] == 'createvm' for Opdrag in self.상자.명령들))

    def test_보존ISO변조거부(self):
        masjien = self.Skep_inskrywing()
        masjien['VMState'] = 'poweroff'
        Path(masjien['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(module_VALUE.실행오류): self.uitvoer_bevel.uitvoer_bevel()

    def test_상태미생성(self):
        self.assertEqual(self.uitvoer_bevel.wys_stand()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for Pad in ('../outside', '/tmp/outside'):
            with self.assertRaises(module_VALUE.실행오류): self.uitvoer_bevel.Pad(Pad)
        (self.wortel_VALUE / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(module_VALUE.실행오류): self.uitvoer_bevel.Pad('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        maatreël = module_VALUE.kenmerk_VALUE('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(maatreël['VMState'], 'running')
        self.assertEqual(maatreël['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
