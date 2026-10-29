import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Definicija_VALUE = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
modul_VALUE = importlib.util.module_from_spec(Definicija_VALUE)
Definicija_VALUE.loader.exec_module(modul_VALUE)


class 가짜상자:
    def __init__(self, koren_VALUE):
        self.koren_VALUE = koren_VALUE
        self.명령들 = []
        self.가상기계들 = {}
        self.otkazivanje_VALUE = None

    def __call__(self, 인수):
        인수 = list(map(str, 인수))
        self.명령들.append(인수)
        if self.otkazivanje_VALUE == 인수[1] or (인수[0] == 'make' and self.otkazivanje_VALUE == 'make'):
            self.otkazivanje_VALUE = None
            raise modul_VALUE.실행오류('시험용 otkazivanje_VALUE')
        if 인수[0] == 'make':
            putanja = self.koren_VALUE / 'os/build/kernel.iso'
            putanja.parent.mkdir(parents=True, exist_ok=True)
            putanja.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        radnja = 인수[1]
        if radnja == 'list':
            return '\n'.join('"{}" {{{}}}'.format(VALUE['name'], INDEX) for INDEX, VALUE in self.가상기계들.items())
        if radnja == 'createvm':
            INDEX, ime = 인수[인수.index('--uuid') + 1], 인수[인수.index('--name') + 1]
            self.가상기계들[INDEX] = {'UUID': INDEX, 'name': ime, 'VMState': 'poweroff',
                'CfgFile': str(self.koren_VALUE / '.vbox/machines' / ime / (ime + '.vbox')), 'owner': None}
            return ''
        računar = self.가상기계들[인수[2]]
        if radnja == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(ime), json.dumps(VALUE)) for ime, VALUE in računar.items() if ime != 'owner')
        if radnja == 'getextradata': return 'Value: ' + računar['owner'] if računar['owner'] else 'No value set!'
        if radnja == 'setextradata': računar['owner'] = 인수[4]
        elif radnja == 'storagectl': računar['storagecontrollername0'] = 'JKOROS IDE'
        elif radnja == 'storageattach': računar['JKOROS IDE-0-0'] = 인수[인수.index('--medium') + 1]
        elif radnja == 'startvm': računar['VMState'] = 'running'
        elif radnja == 'controlvm':
            assert 인수[3] == 'resume'
            računar['VMState'] = 'running'
        elif radnja != 'modifyvm': raise AssertionError(인수)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.koren_VALUE = Path(self.임시.name)
        (self.koren_VALUE / '.vbox').mkdir()
        self.상자 = 가짜상자(self.koren_VALUE)
        self.Izvrši_komanda = modul_VALUE.program_pokretač(self.koren_VALUE, 'jkoros operating system', komanda=self.상자)

    def Create_stavka(self):
        KR = self.Izvrši_komanda.Izvrši_komanda()
        self.상자.명령들.clear()
        return self.상자.가상기계들[KR['uuid']]

    def 변경없음(self):
        self.assertTrue(all(komanda[0] == 'VBoxManage' and komanda[1] in ('list', 'showvminfo', 'getextradata') for komanda in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        KR = self.Izvrši_komanda.Izvrši_komanda()
        self.assertEqual(KR['state'], 'running')
        self.assertTrue(Path(KR['iso']).is_file())
        self.assertTrue(any('--nic1' in komanda and 'none' in komanda for komanda in self.상자.명령들))
        self.assertFalse(any('hdd' in komanda or 'discardstate' in komanda or 'createmedium' in komanda for komanda in self.상자.명령들))

    def test_실행중유지(self):
        self.Create_stavka()
        self.assertEqual(self.Izvrši_komanda.Izvrši_komanda()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        računar = self.Create_stavka()
        računar['VMState'] = 'saved'
        LOG_VALUE = self.Izvrši_komanda.putanja(self.Izvrši_komanda.읽기()['serial_log'])
        LOG_VALUE.write_text('saved log')
        self.Izvrši_komanda.Izvrši_komanda()
        self.assertFalse(any(komanda[0] == 'make' or komanda[1] == 'modifyvm' for komanda in self.상자.명령들))
        self.assertEqual([putanja.read_text() for putanja in LOG_VALUE.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.Create_stavka()['VMState'] = 'paused'
        self.Izvrši_komanda.Izvrši_komanda()
        self.assertTrue(any(komanda[1] == 'controlvm' and komanda[3] == 'resume' for komanda in self.상자.명령들))
        self.assertFalse(any(komanda[0] == 'make' for komanda in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(modul_VALUE.실행오류): self.Izvrši_komanda.Izvrši_komanda()
        self.변경없음()

    def test_소유표식거부(self):
        self.Create_stavka()['owner'] = 'someone-else'
        with self.assertRaises(modul_VALUE.실행오류): self.Izvrši_komanda.Izvrši_komanda()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.Create_stavka()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(modul_VALUE.실행오류): self.Izvrši_komanda.Izvrši_komanda()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        računar = self.Create_stavka()
        računar['VMState'] = 'poweroff'
        računar['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(modul_VALUE.실행오류): self.Izvrši_komanda.Izvrši_komanda()
        self.변경없음()

    def test_전환중거부(self):
        self.Create_stavka()['VMState'] = 'saving'
        with self.assertRaises(modul_VALUE.실행오류): self.Izvrši_komanda.Izvrši_komanda()
        self.변경없음()

    def test_등록해제거부(self):
        self.Create_stavka()
        self.상자.가상기계들.clear()
        with self.assertRaises(modul_VALUE.실행오류): self.Izvrši_komanda.Izvrši_komanda()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        računar = self.Create_stavka()
        računar['VMState'] = 'poweroff'
        이전 = dict(računar)
        self.상자.otkazivanje_VALUE = 'make'
        with self.assertRaises(modul_VALUE.실행오류): self.Izvrši_komanda.Izvrši_komanda()
        self.assertEqual(računar, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.otkazivanje_VALUE = 'setextradata'
        with self.assertRaises(modul_VALUE.실행오류): self.Izvrši_komanda.Izvrši_komanda()
        self.상자.명령들.clear()
        self.assertEqual(self.Izvrši_komanda.Izvrši_komanda()['state'], 'running')
        self.assertFalse(any(komanda[1] == 'createvm' for komanda in self.상자.명령들))

    def test_보존ISO변조거부(self):
        računar = self.Create_stavka()
        računar['VMState'] = 'poweroff'
        Path(računar['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(modul_VALUE.실행오류): self.Izvrši_komanda.Izvrši_komanda()

    def test_상태미생성(self):
        self.assertEqual(self.Izvrši_komanda.emisija_Status()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for putanja in ('../outside', '/tmp/outside'):
            with self.assertRaises(modul_VALUE.실행오류): self.Izvrši_komanda.putanja(putanja)
        (self.koren_VALUE / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(modul_VALUE.실행오류): self.Izvrši_komanda.putanja('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        KR = modul_VALUE.atribut_VALUE('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(KR['VMState'], 'running')
        self.assertEqual(KR['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
