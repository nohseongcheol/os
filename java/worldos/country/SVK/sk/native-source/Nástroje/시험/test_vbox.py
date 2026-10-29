import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Definícia_VALUE = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
modul_VALUE = importlib.util.module_from_spec(Definícia_VALUE)
Definícia_VALUE.loader.exec_module(modul_VALUE)


class 가짜상자:
    def __init__(self, koreň_VALUE):
        self.koreň_VALUE = koreň_VALUE
        self.명령들 = []
        self.가상기계들 = {}
        self.zlyhanie_VALUE = None

    def __call__(self, Argumenty):
        Argumenty = list(map(str, Argumenty))
        self.명령들.append(Argumenty)
        if self.zlyhanie_VALUE == Argumenty[1] or (Argumenty[0] == 'make' and self.zlyhanie_VALUE == 'make'):
            self.zlyhanie_VALUE = None
            raise modul_VALUE.실행오류('시험용 zlyhanie_VALUE')
        if Argumenty[0] == 'make':
            Cesta = self.koreň_VALUE / 'os/build/kernel.iso'
            Cesta.parent.mkdir(parents=True, exist_ok=True)
            Cesta.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Akcia = Argumenty[1]
        if Akcia == 'list':
            return '\n'.join('"{}" {{{}}}'.format(VALUE['name'], INDEX) for INDEX, VALUE in self.가상기계들.items())
        if Akcia == 'createvm':
            INDEX, Názov = Argumenty[Argumenty.index('--uuid') + 1], Argumenty[Argumenty.index('--name') + 1]
            self.가상기계들[INDEX] = {'UUID': INDEX, 'name': Názov, 'VMState': 'poweroff',
                'CfgFile': str(self.koreň_VALUE / '.vbox/machines' / Názov / (Názov + '.vbox')), 'owner': None}
            return ''
        počítač_5eb260fa = self.가상기계들[Argumenty[2]]
        if Akcia == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Názov), json.dumps(VALUE)) for Názov, VALUE in počítač_5eb260fa.items() if Názov != 'owner')
        if Akcia == 'getextradata': return 'Value: ' + počítač_5eb260fa['owner'] if počítač_5eb260fa['owner'] else 'No value set!'
        if Akcia == 'setextradata': počítač_5eb260fa['owner'] = Argumenty[4]
        elif Akcia == 'storagectl': počítač_5eb260fa['storagecontrollername0'] = 'JKOROS IDE'
        elif Akcia == 'storageattach': počítač_5eb260fa['JKOROS IDE-0-0'] = Argumenty[Argumenty.index('--medium') + 1]
        elif Akcia == 'startvm': počítač_5eb260fa['VMState'] = 'running'
        elif Akcia == 'controlvm':
            assert Argumenty[3] == 'resume'
            počítač_5eb260fa['VMState'] = 'running'
        elif Akcia != 'modifyvm': raise AssertionError(Argumenty)
        return ''


class test_spustiť(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.koreň_VALUE = Path(self.임시.name)
        (self.koreň_VALUE / '.vbox').mkdir()
        self.상자 = 가짜상자(self.koreň_VALUE)
        self.Vykonať_príkaz = modul_VALUE.program_spúšťač(self.koreň_VALUE, 'jkoros operating system', Príkaz=self.상자)

    def Create_položka(self):
        KR = self.Vykonať_príkaz.Vykonať_príkaz()
        self.상자.명령들.clear()
        return self.상자.가상기계들[KR['uuid']]

    def 변경없음(self):
        self.assertTrue(all(Príkaz[0] == 'VBoxManage' and Príkaz[1] in ('list', 'showvminfo', 'getextradata') for Príkaz in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        KR = self.Vykonať_príkaz.Vykonať_príkaz()
        self.assertEqual(KR['state'], 'running')
        self.assertTrue(Path(KR['iso']).is_file())
        self.assertTrue(any('--nic1' in Príkaz and 'none' in Príkaz for Príkaz in self.상자.명령들))
        self.assertFalse(any('hdd' in Príkaz or 'discardstate' in Príkaz or 'createmedium' in Príkaz for Príkaz in self.상자.명령들))

    def test_실행중유지(self):
        self.Create_položka()
        self.assertEqual(self.Vykonať_príkaz.Vykonať_príkaz()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        počítač_5eb260fa = self.Create_položka()
        počítač_5eb260fa['VMState'] = 'saved'
        LOG_VALUE = self.Vykonať_príkaz.Cesta(self.Vykonať_príkaz.Čítanie()['serial_log'])
        LOG_VALUE.write_text('saved log')
        self.Vykonať_príkaz.Vykonať_príkaz()
        self.assertFalse(any(Príkaz[0] == 'make' or Príkaz[1] == 'modifyvm' for Príkaz in self.상자.명령들))
        self.assertEqual([Cesta.read_text() for Cesta in LOG_VALUE.parent.glob('before-resume-*.log')], ['saved log'])

    def test_Pozastaviť_AND_životopis(self):
        self.Create_položka()['VMState'] = 'paused'
        self.Vykonať_príkaz.Vykonať_príkaz()
        self.assertTrue(any(Príkaz[1] == 'controlvm' and Príkaz[3] == 'resume' for Príkaz in self.상자.명령들))
        self.assertFalse(any(Príkaz[0] == 'make' for Príkaz in self.상자.명령들))

    def test_Iné_virtuálny_počítač_názov_kolízia(self):
        self.상자.가상기계들[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(modul_VALUE.실행오류): self.Vykonať_príkaz.Vykonať_príkaz()
        self.변경없음()

    def test_소유표식거부(self):
        self.Create_položka()['owner'] = 'someone-else'
        with self.assertRaises(modul_VALUE.실행오류): self.Vykonať_príkaz.Vykonať_príkaz()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.Create_položka()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(modul_VALUE.실행오류): self.Vykonať_príkaz.Vykonať_príkaz()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        počítač_5eb260fa = self.Create_položka()
        počítač_5eb260fa['VMState'] = 'poweroff'
        počítač_5eb260fa['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(modul_VALUE.실행오류): self.Vykonať_príkaz.Vykonať_príkaz()
        self.변경없음()

    def test_전환중거부(self):
        self.Create_položka()['VMState'] = 'saving'
        with self.assertRaises(modul_VALUE.실행오류): self.Vykonať_príkaz.Vykonať_príkaz()
        self.변경없음()

    def test_등록해제거부(self):
        self.Create_položka()
        self.상자.가상기계들.clear()
        with self.assertRaises(modul_VALUE.실행오류): self.Vykonať_príkaz.Vykonať_príkaz()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        počítač_5eb260fa = self.Create_položka()
        počítač_5eb260fa['VMState'] = 'poweroff'
        이전 = dict(počítač_5eb260fa)
        self.상자.zlyhanie_VALUE = 'make'
        with self.assertRaises(modul_VALUE.실행오류): self.Vykonať_príkaz.Vykonať_príkaz()
        self.assertEqual(počítač_5eb260fa, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.zlyhanie_VALUE = 'setextradata'
        with self.assertRaises(modul_VALUE.실행오류): self.Vykonať_príkaz.Vykonať_príkaz()
        self.상자.명령들.clear()
        self.assertEqual(self.Vykonať_príkaz.Vykonať_príkaz()['state'], 'running')
        self.assertFalse(any(Príkaz[1] == 'createvm' for Príkaz in self.상자.명령들))

    def test_보존ISO변조거부(self):
        počítač_5eb260fa = self.Create_položka()
        počítač_5eb260fa['VMState'] = 'poweroff'
        Path(počítač_5eb260fa['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(modul_VALUE.실행오류): self.Vykonať_príkaz.Vykonať_príkaz()

    def test_상태미생성(self):
        self.assertEqual(self.Vykonať_príkaz.zobraziť_Stav()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for Cesta in ('../outside', '/tmp/outside'):
            with self.assertRaises(modul_VALUE.실행오류): self.Vykonať_príkaz.Cesta(Cesta)
        (self.koreň_VALUE / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(modul_VALUE.실행오류): self.Vykonať_príkaz.Cesta('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        KR = modul_VALUE.atribút_VALUE('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(KR['VMState'], 'running')
        self.assertEqual(KR['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
