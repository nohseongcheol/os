import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Tərif_VALUE = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
modul_VALUE = importlib.util.module_from_spec(Tərif_VALUE)
Tərif_VALUE.loader.exec_module(modul_VALUE)


class 가짜상자:
    def __init__(self, kök_VALUE):
        self.kök_VALUE = kök_VALUE
        self.명령들 = []
        self.가상기계들 = {}
        self.xəta_VALUE = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.xəta_VALUE == 인수[1] or (인수[0] == 'make' and self.xəta_VALUE == 'make'):
            self.xəta_VALUE = None
            raise modul_VALUE.실행오류('시험용 xəta_VALUE')
        if 인수[0] == 'make':
            Cığır = self.kök_VALUE / 'os/build/kernel.iso'
            Cığır.parent.mkdir(parents=True, exist_ok=True)
            Cığır.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Gedişat = 인수[1]
        if Gedişat == 'list':
            return '\n'.join('"{}" {{{}}}'.format(VALUE['name'], INDEX) for INDEX, VALUE in self.가상기계들.items())
        if Gedişat == 'createvm':
            INDEX, Ad = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[INDEX] = {'UUID': INDEX, 'name': Ad, 'VMState': 'poweroff',
                'CfgFile': str(self.kök_VALUE / '.vbox/machines' / Ad / (Ad + '.vbox')), 'owner': None}
            return ''
        maşın = self.가상기계들[인수[2]]
        if Gedişat == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Ad), json.dumps(VALUE)) for Ad, VALUE in maşın.items() if Ad != 'owner')
        if Gedişat == 'getextradata': return 'Value: ' + maşın['owner'] if maşın['owner'] else 'No value set!'
        if Gedişat == 'setextradata': maşın['owner'] = 인수[4]
        elif Gedişat == 'storagectl': maşın['storagecontrollername0'] = 'JKOROS IDE'
        elif Gedişat == 'storageattach': maşın['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif Gedişat == 'startvm': maşın['VMState'] = 'running'
        elif Gedişat == 'controlvm':
            assert 인수[3] == 'resume'
            maşın['VMState'] = 'running'
        elif Gedişat != 'modifyvm': raise AssertionError(인수)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.kök_VALUE = Path(self.임시.name)
        (self.kök_VALUE / '.vbox').mkdir()
        self.상자 = 가짜상자(self.kök_VALUE)
        self.icra_etmək_əmr = modul_VALUE.proqram_işəsalma(self.kök_VALUE, 'jkoros operating system', Əmr=self.상자)

    def yarat_daxiletmə(self):
        ölçü = self.icra_etmək_əmr.icra_etmək_əmr()
        self.상자.명령들.clear()
        return self.상자.가상기계들[ölçü['uuid']]

    def 변경없음(self):
        self.assertTrue(all(Əmr[0] == 'VBoxManage' and Əmr[1] in ('list', 'showvminfo', 'getextradata') for Əmr in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        ölçü = self.icra_etmək_əmr.icra_etmək_əmr()
        self.assertEqual(ölçü['state'], 'running')
        self.assertTrue(Path(ölçü['iso']).is_file())
        self.assertTrue(any('--nic1' in Əmr and 'none' in Əmr for Əmr in self.상자.명령들))
        self.assertFalse(any('hdd' in Əmr or 'discardstate' in Əmr or 'createmedium' in Əmr for Əmr in self.상자.명령들))

    def test_실행중유지(self):
        self.yarat_daxiletmə()
        self.assertEqual(self.icra_etmək_əmr.icra_etmək_əmr()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        maşın = self.yarat_daxiletmə()
        maşın['VMState'] = 'saved'
        LOG_VALUE = self.icra_etmək_əmr.Cığır(self.icra_etmək_əmr.Oxuma()['serial_log'])
        LOG_VALUE.write_text('saved log')
        self.icra_etmək_əmr.icra_etmək_əmr()
        self.assertFalse(any(Əmr[0] == 'make' or Əmr[1] == 'modifyvm' for Əmr in self.상자.명령들))
        self.assertEqual([Cığır.read_text() for Cığır in LOG_VALUE.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.yarat_daxiletmə()['VMState'] = 'paused'
        self.icra_etmək_əmr.icra_etmək_əmr()
        self.assertTrue(any(Əmr[1] == 'controlvm' and Əmr[3] == 'resume' for Əmr in self.상자.명령들))
        self.assertFalse(any(Əmr[0] == 'make' for Əmr in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(modul_VALUE.실행오류): self.icra_etmək_əmr.icra_etmək_əmr()
        self.변경없음()

    def test_소유표식거부(self):
        self.yarat_daxiletmə()['owner'] = 'someone-else'
        with self.assertRaises(modul_VALUE.실행오류): self.icra_etmək_əmr.icra_etmək_əmr()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.yarat_daxiletmə()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(modul_VALUE.실행오류): self.icra_etmək_əmr.icra_etmək_əmr()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        maşın = self.yarat_daxiletmə()
        maşın['VMState'] = 'poweroff'
        maşın['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(modul_VALUE.실행오류): self.icra_etmək_əmr.icra_etmək_əmr()
        self.변경없음()

    def test_전환중거부(self):
        self.yarat_daxiletmə()['VMState'] = 'saving'
        with self.assertRaises(modul_VALUE.실행오류): self.icra_etmək_əmr.icra_etmək_əmr()
        self.변경없음()

    def test_등록해제거부(self):
        self.yarat_daxiletmə()
        self.상자.가상기계들.clear()
        with self.assertRaises(modul_VALUE.실행오류): self.icra_etmək_əmr.icra_etmək_əmr()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        maşın = self.yarat_daxiletmə()
        maşın['VMState'] = 'poweroff'
        이전 = dict(maşın)
        self.상자.xəta_VALUE = 'make'
        with self.assertRaises(modul_VALUE.실행오류): self.icra_etmək_əmr.icra_etmək_əmr()
        self.assertEqual(maşın, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.xəta_VALUE = 'setextradata'
        with self.assertRaises(modul_VALUE.실행오류): self.icra_etmək_əmr.icra_etmək_əmr()
        self.상자.명령들.clear()
        self.assertEqual(self.icra_etmək_əmr.icra_etmək_əmr()['state'], 'running')
        self.assertFalse(any(Əmr[1] == 'createvm' for Əmr in self.상자.명령들))

    def test_보존ISO변조거부(self):
        maşın = self.yarat_daxiletmə()
        maşın['VMState'] = 'poweroff'
        Path(maşın['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(modul_VALUE.실행오류): self.icra_etmək_əmr.icra_etmək_əmr()

    def test_상태미생성(self):
        self.assertEqual(self.icra_etmək_əmr.göstərmək_vəziyyət()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for Cığır in ('../outside', '/tmp/outside'):
            with self.assertRaises(modul_VALUE.실행오류): self.icra_etmək_əmr.Cığır(Cığır)
        (self.kök_VALUE / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(modul_VALUE.실행오류): self.icra_etmək_əmr.Cığır('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        ölçü = modul_VALUE.atribut_VALUE('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(ölçü['VMState'], 'running')
        self.assertEqual(ölçü['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
