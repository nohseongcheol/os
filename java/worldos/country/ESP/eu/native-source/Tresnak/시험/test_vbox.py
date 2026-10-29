import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Definizioa_balio = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
modulu_balio = importlib.util.module_from_spec(Definizioa_balio)
Definizioa_balio.loader.exec_module(modulu_balio)


class 가짜상자:
    def __init__(self, erro_balio):
        self.erro_balio = erro_balio
        self.명령들 = []
        self.가상기계들 = {}
        self.hutsegite_balio = None

    def __call__(self, Argumentuak):
        Argumentuak = list(map(str, Argumentuak))
        self.명령들.append(Argumentuak)
        if self.hutsegite_balio == Argumentuak[1] or (Argumentuak[0] == 'make' and self.hutsegite_balio == 'make'):
            self.hutsegite_balio = None
            raise modulu_balio.실행오류('시험용 hutsegite_balio')
        if Argumentuak[0] == 'make':
            Bide_izena = self.erro_balio / 'os/build/kernel.iso'
            Bide_izena.parent.mkdir(parents=True, exist_ok=True)
            Bide_izena.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Ekintza = Argumentuak[1]
        if Ekintza == 'list':
            return '\n'.join('"{}" {{{}}}'.format(balio['name'], INDIZE) for INDIZE, balio in self.가상기계들.items())
        if Ekintza == 'createvm':
            INDIZE, Izena = Argumentuak[Argumentuak.index('--uuid') + 1], Argumentuak[Argumentuak.index('--name') + 1]
            self.가상기계들[INDIZE] = {'UUID': INDIZE, 'name': Izena, 'VMState': 'poweroff',
                'CfgFile': str(self.erro_balio / '.vbox/machines' / Izena / (Izena + '.vbox')), 'owner': None}
            return ''
        gailu = self.가상기계들[Argumentuak[2]]
        if Ekintza == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Izena), json.dumps(balio)) for Izena, balio in gailu.items() if Izena != 'owner')
        if Ekintza == 'getextradata': return 'Value: ' + gailu['owner'] if gailu['owner'] else 'No value set!'
        if Ekintza == 'setextradata': gailu['owner'] = Argumentuak[4]
        elif Ekintza == 'storagectl': gailu['storagecontrollername0'] = 'JKOROS IDE'
        elif Ekintza == 'storageattach': gailu['JKOROS IDE-0-0'] = Argumentuak[Argumentuak.index('--medium') + 1]
        elif Ekintza == 'startvm': gailu['VMState'] = 'running'
        elif Ekintza == 'controlvm':
            assert Argumentuak[3] == 'resume'
            gailu['VMState'] = 'running'
        elif Ekintza != 'modifyvm': raise AssertionError(Argumentuak)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.erro_balio = Path(self.임시.name)
        (self.erro_balio / '.vbox').mkdir()
        self.상자 = 가짜상자(self.erro_balio)
        self.exekutatu_komando = modulu_balio.aplik_abiarazle(self.erro_balio, 'jkoros operating system', Komandoa=self.상자)

    def sortu_sarrera(self):
        EMAITZA = self.exekutatu_komando.exekutatu_komando()
        self.상자.명령들.clear()
        return self.상자.가상기계들[EMAITZA['uuid']]

    def 변경없음(self):
        self.assertTrue(all(Komandoa[0] == 'VBoxManage' and Komandoa[1] in ('list', 'showvminfo', 'getextradata') for Komandoa in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        EMAITZA = self.exekutatu_komando.exekutatu_komando()
        self.assertEqual(EMAITZA['state'], 'running')
        self.assertTrue(Path(EMAITZA['iso']).is_file())
        self.assertTrue(any('--nic1' in Komandoa and 'none' in Komandoa for Komandoa in self.상자.명령들))
        self.assertFalse(any('hdd' in Komandoa or 'discardstate' in Komandoa or 'createmedium' in Komandoa for Komandoa in self.상자.명령들))

    def test_실행중유지(self):
        self.sortu_sarrera()
        self.assertEqual(self.exekutatu_komando.exekutatu_komando()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        gailu = self.sortu_sarrera()
        gailu['VMState'] = 'saved'
        LOG_balio = self.exekutatu_komando.Bide_izena(self.exekutatu_komando.Irakurri()['serial_log'])
        LOG_balio.write_text('saved log')
        self.exekutatu_komando.exekutatu_komando()
        self.assertFalse(any(Komandoa[0] == 'make' or Komandoa[1] == 'modifyvm' for Komandoa in self.상자.명령들))
        self.assertEqual([Bide_izena.read_text() for Bide_izena in LOG_balio.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.sortu_sarrera()['VMState'] = 'paused'
        self.exekutatu_komando.exekutatu_komando()
        self.assertTrue(any(Komandoa[1] == 'controlvm' and Komandoa[3] == 'resume' for Komandoa in self.상자.명령들))
        self.assertFalse(any(Komandoa[0] == 'make' for Komandoa in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(modulu_balio.실행오류): self.exekutatu_komando.exekutatu_komando()
        self.변경없음()

    def test_소유표식거부(self):
        self.sortu_sarrera()['owner'] = 'someone-else'
        with self.assertRaises(modulu_balio.실행오류): self.exekutatu_komando.exekutatu_komando()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.sortu_sarrera()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(modulu_balio.실행오류): self.exekutatu_komando.exekutatu_komando()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        gailu = self.sortu_sarrera()
        gailu['VMState'] = 'poweroff'
        gailu['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(modulu_balio.실행오류): self.exekutatu_komando.exekutatu_komando()
        self.변경없음()

    def test_전환중거부(self):
        self.sortu_sarrera()['VMState'] = 'saving'
        with self.assertRaises(modulu_balio.실행오류): self.exekutatu_komando.exekutatu_komando()
        self.변경없음()

    def test_등록해제거부(self):
        self.sortu_sarrera()
        self.상자.가상기계들.clear()
        with self.assertRaises(modulu_balio.실행오류): self.exekutatu_komando.exekutatu_komando()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        gailu = self.sortu_sarrera()
        gailu['VMState'] = 'poweroff'
        이전 = dict(gailu)
        self.상자.hutsegite_balio = 'make'
        with self.assertRaises(modulu_balio.실행오류): self.exekutatu_komando.exekutatu_komando()
        self.assertEqual(gailu, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.hutsegite_balio = 'setextradata'
        with self.assertRaises(modulu_balio.실행오류): self.exekutatu_komando.exekutatu_komando()
        self.상자.명령들.clear()
        self.assertEqual(self.exekutatu_komando.exekutatu_komando()['state'], 'running')
        self.assertFalse(any(Komandoa[1] == 'createvm' for Komandoa in self.상자.명령들))

    def test_보존ISO변조거부(self):
        gailu = self.sortu_sarrera()
        gailu['VMState'] = 'poweroff'
        Path(gailu['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(modulu_balio.실행오류): self.exekutatu_komando.exekutatu_komando()

    def test_상태미생성(self):
        self.assertEqual(self.exekutatu_komando.erakutsi_Egoera()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for Bide_izena in ('../outside', '/tmp/outside'):
            with self.assertRaises(modulu_balio.실행오류): self.exekutatu_komando.Bide_izena(Bide_izena)
        (self.erro_balio / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(modulu_balio.실행오류): self.exekutatu_komando.Bide_izena('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        EMAITZA = modulu_balio.atributu_balio('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(EMAITZA['VMState'], 'running')
        self.assertEqual(EMAITZA['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
