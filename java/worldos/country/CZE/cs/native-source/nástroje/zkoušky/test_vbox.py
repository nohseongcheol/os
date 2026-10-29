import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Definice_HODNOTA = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
modul_HODNOTA = importlib.util.module_from_spec(Definice_HODNOTA)
Definice_HODNOTA.loader.exec_module(modul_HODNOTA)


class 가짜상자:
    def __init__(self, kořen_HODNOTA):
        self.kořen_HODNOTA = kořen_HODNOTA
        self.명령들 = []
        self.Virtual_Machines = {}
        self.selhání_HODNOTA = None

    def __call__(self, argumenty):
        argumenty = list(map(str, argumenty))
        self.명령들.append(argumenty)
        if self.selhání_HODNOTA == argumenty[1] or (argumenty[0] == 'make' and self.selhání_HODNOTA == 'make'):
            self.selhání_HODNOTA = None
            raise modul_HODNOTA.spuštění_chyba_3f02a041('시험용 selhání_HODNOTA')
        if argumenty[0] == 'make':
            cesta_2 = self.kořen_HODNOTA / 'os/build/kernel.iso'
            cesta_2.parent.mkdir(parents=True, exist_ok=True)
            cesta_2.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Akce = argumenty[1]
        if Akce == 'list':
            return '\n'.join('"{}" {{{}}}'.format(HODNOTA['name'], INDEX) for INDEX, HODNOTA in self.Virtual_Machines.items())
        if Akce == 'createvm':
            INDEX, Název = argumenty[argumenty.index('--uuid') + 1], argumenty[argumenty.index('--name') + 1]
            self.Virtual_Machines[INDEX] = {'UUID': INDEX, 'name': Název, 'VMState': 'poweroff',
                'CfgFile': str(self.kořen_HODNOTA / '.vbox/machines' / Název / (Název + '.vbox')), 'owner': None}
            return ''
        počítač = self.Virtual_Machines[argumenty[2]]
        if Akce == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Název), json.dumps(HODNOTA)) for Název, HODNOTA in počítač.items() if Název != 'owner')
        if Akce == 'getextradata': return 'Value: ' + počítač['owner'] if počítač['owner'] else 'No value set!'
        if Akce == 'setextradata': počítač['owner'] = argumenty[4]
        elif Akce == 'storagectl': počítač['storagecontrollername0'] = 'JKOROS IDE'
        elif Akce == 'storageattach': počítač['JKOROS IDE-0-0'] = argumenty[argumenty.index('--medium') + 1]
        elif Akce == 'startvm': počítač['VMState'] = 'running'
        elif Akce == 'controlvm':
            assert argumenty[3] == 'resume'
            počítač['VMState'] = 'running'
        elif Akce != 'modifyvm': raise AssertionError(argumenty)
        return ''


class testovací_běh(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.kořen_HODNOTA = Path(self.임시.name)
        (self.kořen_HODNOTA / '.vbox').mkdir()
        self.상자 = 가짜상자(self.kořen_HODNOTA)
        self.Provést_příkaz = modul_HODNOTA.program_Launcher(self.kořen_HODNOTA, 'jkoros operating system', příkaz=self.상자)

    def Create_položka(self):
        VÝSLEDEK = self.Provést_příkaz.Provést_příkaz()
        self.상자.명령들.clear()
        return self.상자.Virtual_Machines[VÝSLEDEK['uuid']]

    def 변경없음(self):
        self.assertTrue(all(příkaz[0] == 'VBoxManage' and příkaz[1] in ('list', 'showvminfo', 'getextradata') for příkaz in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        VÝSLEDEK = self.Provést_příkaz.Provést_příkaz()
        self.assertEqual(VÝSLEDEK['state'], 'running')
        self.assertTrue(Path(VÝSLEDEK['iso']).is_file())
        self.assertTrue(any('--nic1' in příkaz and 'none' in příkaz for příkaz in self.상자.명령들))
        self.assertFalse(any('hdd' in příkaz or 'discardstate' in příkaz or 'createmedium' in příkaz for příkaz in self.상자.명령들))

    def test_실행중유지(self):
        self.Create_položka()
        self.assertEqual(self.Provést_příkaz.Provést_příkaz()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        počítač = self.Create_položka()
        počítač['VMState'] = 'saved'
        LOGZ_HODNOTA = self.Provést_příkaz.cesta_2(self.Provést_příkaz.Čtení()['serial_log'])
        LOGZ_HODNOTA.write_text('saved log')
        self.Provést_příkaz.Provést_příkaz()
        self.assertFalse(any(příkaz[0] == 'make' or příkaz[1] == 'modifyvm' for příkaz in self.상자.명령들))
        self.assertEqual([cesta_2.read_text() for cesta_2 in LOGZ_HODNOTA.parent.glob('before-resume-*.log')], ['saved log'])

    def test_Pozastavit_A_pokračovat(self):
        self.Create_položka()['VMState'] = 'paused'
        self.Provést_příkaz.Provést_příkaz()
        self.assertTrue(any(příkaz[1] == 'controlvm' and příkaz[3] == 'resume' for příkaz in self.상자.명령들))
        self.assertFalse(any(příkaz[0] == 'make' for příkaz in self.상자.명령들))

    def test_Jiný_virtuální_počítač_název_kolize(self):
        self.상자.Virtual_Machines[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(modul_HODNOTA.spuštění_chyba_3f02a041): self.Provést_příkaz.Provést_příkaz()
        self.변경없음()

    def test_소유표식거부(self):
        self.Create_položka()['owner'] = 'someone-else'
        with self.assertRaises(modul_HODNOTA.spuštění_chyba_3f02a041): self.Provést_příkaz.Provést_příkaz()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.Create_položka()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(modul_HODNOTA.spuštění_chyba_3f02a041): self.Provést_příkaz.Provést_příkaz()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        počítač = self.Create_položka()
        počítač['VMState'] = 'poweroff'
        počítač['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(modul_HODNOTA.spuštění_chyba_3f02a041): self.Provést_příkaz.Provést_příkaz()
        self.변경없음()

    def test_전환중거부(self):
        self.Create_položka()['VMState'] = 'saving'
        with self.assertRaises(modul_HODNOTA.spuštění_chyba_3f02a041): self.Provést_příkaz.Provést_příkaz()
        self.변경없음()

    def test_등록해제거부(self):
        self.Create_položka()
        self.상자.Virtual_Machines.clear()
        with self.assertRaises(modul_HODNOTA.spuštění_chyba_3f02a041): self.Provést_příkaz.Provést_příkaz()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        počítač = self.Create_položka()
        počítač['VMState'] = 'poweroff'
        Předchozí_zboží = dict(počítač)
        self.상자.selhání_HODNOTA = 'make'
        with self.assertRaises(modul_HODNOTA.spuštění_chyba_3f02a041): self.Provést_příkaz.Provést_příkaz()
        self.assertEqual(počítač, Předchozí_zboží)

    def test_중단된소유표식설정복구(self):
        self.상자.selhání_HODNOTA = 'setextradata'
        with self.assertRaises(modul_HODNOTA.spuštění_chyba_3f02a041): self.Provést_příkaz.Provést_příkaz()
        self.상자.명령들.clear()
        self.assertEqual(self.Provést_příkaz.Provést_příkaz()['state'], 'running')
        self.assertFalse(any(příkaz[1] == 'createvm' for příkaz in self.상자.명령들))

    def test_보존ISO변조거부(self):
        počítač = self.Create_položka()
        počítač['VMState'] = 'poweroff'
        Path(počítač['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(modul_HODNOTA.spuštění_chyba_3f02a041): self.Provést_příkaz.Provést_příkaz()

    def test_상태미생성(self):
        self.assertEqual(self.Provést_příkaz.zobrazit_Stav()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for cesta_2 in ('../outside', '/tmp/outside'):
            with self.assertRaises(modul_HODNOTA.spuštění_chyba_3f02a041): self.Provést_příkaz.cesta_2(cesta_2)
        (self.kořen_HODNOTA / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(modul_HODNOTA.spuštění_chyba_3f02a041): self.Provést_příkaz.cesta_2('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        VÝSLEDEK = modul_HODNOTA.hodnota_atributu('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(VÝSLEDEK['VMState'], 'running')
        self.assertEqual(VÝSLEDEK['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
