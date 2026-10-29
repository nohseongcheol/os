import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

definīcija_VALUE = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
modulis_VALUE = importlib.util.module_from_spec(definīcija_VALUE)
definīcija_VALUE.loader.exec_module(modulis_VALUE)


class 가짜상자:
    def __init__(self, sakne_VALUE):
        self.sakne_VALUE = sakne_VALUE
        self.명령들 = []
        self.가상기계들 = {}
        self.kļūme_VALUE = None

    def __call__(self, Parametri):
        Parametri = list(map(str, Parametri))
        self.명령들.append(Parametri)
        if self.kļūme_VALUE == Parametri[1] or (Parametri[0] == 'make' and self.kļūme_VALUE == 'make'):
            self.kļūme_VALUE = None
            raise modulis_VALUE.실행오류('시험용 kļūme_VALUE')
        if Parametri[0] == 'make':
            CEĻŠ = self.sakne_VALUE / 'os/build/kernel.iso'
            CEĻŠ.parent.mkdir(parents=True, exist_ok=True)
            CEĻŠ.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Darbība = Parametri[1]
        if Darbība == 'list':
            return '\n'.join('"{}" {{{}}}'.format(VALUE['name'], INDEX) for INDEX, VALUE in self.가상기계들.items())
        if Darbība == 'createvm':
            INDEX, Nosaukums = Parametri[Parametri.index('--uuid') + 1], Parametri[Parametri.index('--name') + 1]
            self.가상기계들[INDEX] = {'UUID': INDEX, 'name': Nosaukums, 'VMState': 'poweroff',
                'CfgFile': str(self.sakne_VALUE / '.vbox/machines' / Nosaukums / (Nosaukums + '.vbox')), 'owner': None}
            return ''
        mašīna = self.가상기계들[Parametri[2]]
        if Darbība == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Nosaukums), json.dumps(VALUE)) for Nosaukums, VALUE in mašīna.items() if Nosaukums != 'owner')
        if Darbība == 'getextradata': return 'Value: ' + mašīna['owner'] if mašīna['owner'] else 'No value set!'
        if Darbība == 'setextradata': mašīna['owner'] = Parametri[4]
        elif Darbība == 'storagectl': mašīna['storagecontrollername0'] = 'JKOROS IDE'
        elif Darbība == 'storageattach': mašīna['JKOROS IDE-0-0'] = Parametri[Parametri.index('--medium') + 1]
        elif Darbība == 'startvm': mašīna['VMState'] = 'running'
        elif Darbība == 'controlvm':
            assert Parametri[3] == 'resume'
            mašīna['VMState'] = 'running'
        elif Darbība != 'modifyvm': raise AssertionError(Parametri)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.sakne_VALUE = Path(self.임시.name)
        (self.sakne_VALUE / '.vbox').mkdir()
        self.상자 = 가짜상자(self.sakne_VALUE)
        self.Izpildīt_komanda = modulis_VALUE.programma_palaidējs(self.sakne_VALUE, 'jkoros operating system', Komanda=self.상자)

    def atvērt_ievade(self):
        mērs = self.Izpildīt_komanda.Izpildīt_komanda()
        self.상자.명령들.clear()
        return self.상자.가상기계들[mērs['uuid']]

    def 변경없음(self):
        self.assertTrue(all(Komanda[0] == 'VBoxManage' and Komanda[1] in ('list', 'showvminfo', 'getextradata') for Komanda in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        mērs = self.Izpildīt_komanda.Izpildīt_komanda()
        self.assertEqual(mērs['state'], 'running')
        self.assertTrue(Path(mērs['iso']).is_file())
        self.assertTrue(any('--nic1' in Komanda and 'none' in Komanda for Komanda in self.상자.명령들))
        self.assertFalse(any('hdd' in Komanda or 'discardstate' in Komanda or 'createmedium' in Komanda for Komanda in self.상자.명령들))

    def test_실행중유지(self):
        self.atvērt_ievade()
        self.assertEqual(self.Izpildīt_komanda.Izpildīt_komanda()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        mašīna = self.atvērt_ievade()
        mašīna['VMState'] = 'saved'
        LOG_VALUE = self.Izpildīt_komanda.CEĻŠ(self.Izpildīt_komanda.Lasīt()['serial_log'])
        LOG_VALUE.write_text('saved log')
        self.Izpildīt_komanda.Izpildīt_komanda()
        self.assertFalse(any(Komanda[0] == 'make' or Komanda[1] == 'modifyvm' for Komanda in self.상자.명령들))
        self.assertEqual([CEĻŠ.read_text() for CEĻŠ in LOG_VALUE.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.atvērt_ievade()['VMState'] = 'paused'
        self.Izpildīt_komanda.Izpildīt_komanda()
        self.assertTrue(any(Komanda[1] == 'controlvm' and Komanda[3] == 'resume' for Komanda in self.상자.명령들))
        self.assertFalse(any(Komanda[0] == 'make' for Komanda in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(modulis_VALUE.실행오류): self.Izpildīt_komanda.Izpildīt_komanda()
        self.변경없음()

    def test_소유표식거부(self):
        self.atvērt_ievade()['owner'] = 'someone-else'
        with self.assertRaises(modulis_VALUE.실행오류): self.Izpildīt_komanda.Izpildīt_komanda()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.atvērt_ievade()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(modulis_VALUE.실행오류): self.Izpildīt_komanda.Izpildīt_komanda()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        mašīna = self.atvērt_ievade()
        mašīna['VMState'] = 'poweroff'
        mašīna['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(modulis_VALUE.실행오류): self.Izpildīt_komanda.Izpildīt_komanda()
        self.변경없음()

    def test_전환중거부(self):
        self.atvērt_ievade()['VMState'] = 'saving'
        with self.assertRaises(modulis_VALUE.실행오류): self.Izpildīt_komanda.Izpildīt_komanda()
        self.변경없음()

    def test_등록해제거부(self):
        self.atvērt_ievade()
        self.상자.가상기계들.clear()
        with self.assertRaises(modulis_VALUE.실행오류): self.Izpildīt_komanda.Izpildīt_komanda()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        mašīna = self.atvērt_ievade()
        mašīna['VMState'] = 'poweroff'
        이전 = dict(mašīna)
        self.상자.kļūme_VALUE = 'make'
        with self.assertRaises(modulis_VALUE.실행오류): self.Izpildīt_komanda.Izpildīt_komanda()
        self.assertEqual(mašīna, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.kļūme_VALUE = 'setextradata'
        with self.assertRaises(modulis_VALUE.실행오류): self.Izpildīt_komanda.Izpildīt_komanda()
        self.상자.명령들.clear()
        self.assertEqual(self.Izpildīt_komanda.Izpildīt_komanda()['state'], 'running')
        self.assertFalse(any(Komanda[1] == 'createvm' for Komanda in self.상자.명령들))

    def test_보존ISO변조거부(self):
        mašīna = self.atvērt_ievade()
        mašīna['VMState'] = 'poweroff'
        Path(mašīna['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(modulis_VALUE.실행오류): self.Izpildīt_komanda.Izpildīt_komanda()

    def test_상태미생성(self):
        self.assertEqual(self.Izpildīt_komanda.rādīt_Statuss()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for CEĻŠ in ('../outside', '/tmp/outside'):
            with self.assertRaises(modulis_VALUE.실행오류): self.Izpildīt_komanda.CEĻŠ(CEĻŠ)
        (self.sakne_VALUE / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(modulis_VALUE.실행오류): self.Izpildīt_komanda.CEĻŠ('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        mērs = modulis_VALUE.atribūts_VALUE('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(mērs['VMState'], 'running')
        self.assertEqual(mērs['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
