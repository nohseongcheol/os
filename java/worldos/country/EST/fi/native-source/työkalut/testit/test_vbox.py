import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Määritelmä_ARVO = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
moduuli_ARVO = importlib.util.module_from_spec(Määritelmä_ARVO)
Määritelmä_ARVO.loader.exec_module(moduuli_ARVO)


class 가짜상자:
    def __init__(self, juuri_ARVO):
        self.juuri_ARVO = juuri_ARVO
        self.명령들 = []
        self.Näennäiskoneet = {}
        self.virhe_ARVO = None

    def __call__(self, argumentit):
        argumentit = list(map(str, argumentit))
        self.명령들.append(argumentit)
        if self.virhe_ARVO == argumentit[1] or (argumentit[0] == 'make' and self.virhe_ARVO == 'make'):
            self.virhe_ARVO = None
            raise moduuli_ARVO.suoritus_virhe('시험용 virhe_ARVO')
        if argumentit[0] == 'make':
            polku_2 = self.juuri_ARVO / 'os/build/kernel.iso'
            polku_2.parent.mkdir(parents=True, exist_ok=True)
            polku_2.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Toiminto = argumentit[1]
        if Toiminto == 'list':
            return '\n'.join('"{}" {{{}}}'.format(ARVO['name'], INDEKSI) for INDEKSI, ARVO in self.Näennäiskoneet.items())
        if Toiminto == 'createvm':
            INDEKSI, Nimi = argumentit[argumentit.index('--uuid') + 1], argumentit[argumentit.index('--name') + 1]
            self.Näennäiskoneet[INDEKSI] = {'UUID': INDEKSI, 'name': Nimi, 'VMState': 'poweroff',
                'CfgFile': str(self.juuri_ARVO / '.vbox/machines' / Nimi / (Nimi + '.vbox')), 'owner': None}
            return ''
        kone = self.Näennäiskoneet[argumentit[2]]
        if Toiminto == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Nimi), json.dumps(ARVO)) for Nimi, ARVO in kone.items() if Nimi != 'owner')
        if Toiminto == 'getextradata': return 'Value: ' + kone['owner'] if kone['owner'] else 'No value set!'
        if Toiminto == 'setextradata': kone['owner'] = argumentit[4]
        elif Toiminto == 'storagectl': kone['storagecontrollername0'] = 'JKOROS IDE'
        elif Toiminto == 'storageattach': kone['JKOROS IDE-0-0'] = argumentit[argumentit.index('--medium') + 1]
        elif Toiminto == 'startvm': kone['VMState'] = 'running'
        elif Toiminto == 'controlvm':
            assert argumentit[3] == 'resume'
            kone['VMState'] = 'running'
        elif Toiminto != 'modifyvm': raise AssertionError(argumentit)
        return ''


class testi_suorittaa(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.juuri_ARVO = Path(self.임시.name)
        (self.juuri_ARVO / '.vbox').mkdir()
        self.상자 = 가짜상자(self.juuri_ARVO)
        self.Suorita_komento = moduuli_ARVO.ohjelma_sovellusvalikko(self.juuri_ARVO, 'jkoros operating system', komento=self.상자)

    def Luo_merkintä(self):
        TULOS = self.Suorita_komento.Suorita_komento()
        self.상자.명령들.clear()
        return self.상자.Näennäiskoneet[TULOS['uuid']]

    def 변경없음(self):
        self.assertTrue(all(komento[0] == 'VBoxManage' and komento[1] in ('list', 'showvminfo', 'getextradata') for komento in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        TULOS = self.Suorita_komento.Suorita_komento()
        self.assertEqual(TULOS['state'], 'running')
        self.assertTrue(Path(TULOS['iso']).is_file())
        self.assertTrue(any('--nic1' in komento and 'none' in komento for komento in self.상자.명령들))
        self.assertFalse(any('hdd' in komento or 'discardstate' in komento or 'createmedium' in komento for komento in self.상자.명령들))

    def test_실행중유지(self):
        self.Luo_merkintä()
        self.assertEqual(self.Suorita_komento.Suorita_komento()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        kone = self.Luo_merkintä()
        kone['VMState'] = 'saved'
        LOG_ARVO = self.Suorita_komento.polku_2(self.Suorita_komento.Luku()['serial_log'])
        LOG_ARVO.write_text('saved log')
        self.Suorita_komento.Suorita_komento()
        self.assertFalse(any(komento[0] == 'make' or komento[1] == 'modifyvm' for komento in self.상자.명령들))
        self.assertEqual([polku_2.read_text() for polku_2 in LOG_ARVO.parent.glob('before-resume-*.log')], ['saved log'])

    def testi_Keskeytä_JA_jatka(self):
        self.Luo_merkintä()['VMState'] = 'paused'
        self.Suorita_komento.Suorita_komento()
        self.assertTrue(any(komento[1] == 'controlvm' and komento[3] == 'resume' for komento in self.상자.명령들))
        self.assertFalse(any(komento[0] == 'make' for komento in self.상자.명령들))

    def testi_muut_VM_nimi_ristiriita(self):
        self.상자.Näennäiskoneet[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(moduuli_ARVO.suoritus_virhe): self.Suorita_komento.Suorita_komento()
        self.변경없음()

    def test_소유표식거부(self):
        self.Luo_merkintä()['owner'] = 'someone-else'
        with self.assertRaises(moduuli_ARVO.suoritus_virhe): self.Suorita_komento.Suorita_komento()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.Luo_merkintä()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(moduuli_ARVO.suoritus_virhe): self.Suorita_komento.Suorita_komento()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        kone = self.Luo_merkintä()
        kone['VMState'] = 'poweroff'
        kone['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(moduuli_ARVO.suoritus_virhe): self.Suorita_komento.Suorita_komento()
        self.변경없음()

    def test_전환중거부(self):
        self.Luo_merkintä()['VMState'] = 'saving'
        with self.assertRaises(moduuli_ARVO.suoritus_virhe): self.Suorita_komento.Suorita_komento()
        self.변경없음()

    def test_등록해제거부(self):
        self.Luo_merkintä()
        self.상자.Näennäiskoneet.clear()
        with self.assertRaises(moduuli_ARVO.suoritus_virhe): self.Suorita_komento.Suorita_komento()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        kone = self.Luo_merkintä()
        kone['VMState'] = 'poweroff'
        Edellinen_kohde = dict(kone)
        self.상자.virhe_ARVO = 'make'
        with self.assertRaises(moduuli_ARVO.suoritus_virhe): self.Suorita_komento.Suorita_komento()
        self.assertEqual(kone, Edellinen_kohde)

    def test_중단된소유표식설정복구(self):
        self.상자.virhe_ARVO = 'setextradata'
        with self.assertRaises(moduuli_ARVO.suoritus_virhe): self.Suorita_komento.Suorita_komento()
        self.상자.명령들.clear()
        self.assertEqual(self.Suorita_komento.Suorita_komento()['state'], 'running')
        self.assertFalse(any(komento[1] == 'createvm' for komento in self.상자.명령들))

    def test_보존ISO변조거부(self):
        kone = self.Luo_merkintä()
        kone['VMState'] = 'poweroff'
        Path(kone['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(moduuli_ARVO.suoritus_virhe): self.Suorita_komento.Suorita_komento()

    def test_상태미생성(self):
        self.assertEqual(self.Suorita_komento.näyttää_Tila()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for polku_2 in ('../outside', '/tmp/outside'):
            with self.assertRaises(moduuli_ARVO.suoritus_virhe): self.Suorita_komento.polku_2(polku_2)
        (self.juuri_ARVO / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(moduuli_ARVO.suoritus_virhe): self.Suorita_komento.polku_2('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        TULOS = moduuli_ARVO.määritteen_arvo('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(TULOS['VMState'], 'running')
        self.assertEqual(TULOS['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
