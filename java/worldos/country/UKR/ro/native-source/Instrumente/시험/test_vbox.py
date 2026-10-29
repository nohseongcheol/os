import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Definiție_VALUE = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
modul_VALUE = importlib.util.module_from_spec(Definiție_VALUE)
Definiție_VALUE.loader.exec_module(modul_VALUE)


class 가짜상자:
    def __init__(self, rădăcină_VALUE):
        self.rădăcină_VALUE = rădăcină_VALUE
        self.명령들 = []
        self.Mașini_virtuale = {}
        self.eroare_VALUE = None

    def __call__(self, Argumente):
        Argumente = list(map(str, Argumente))
        self.명령들.append(Argumente)
        if self.eroare_VALUE == Argumente[1] or (Argumente[0] == 'make' and self.eroare_VALUE == 'make'):
            self.eroare_VALUE = None
            raise modul_VALUE.executare_eroare('시험용 eroare_VALUE')
        if Argumente[0] == 'make':
            Cale = self.rădăcină_VALUE / 'os/build/kernel.iso'
            Cale.parent.mkdir(parents=True, exist_ok=True)
            Cale.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Acțiuni = Argumente[1]
        if Acțiuni == 'list':
            return '\n'.join('"{}" {{{}}}'.format(VALUE['name'], INDEX) for INDEX, VALUE in self.Mașini_virtuale.items())
        if Acțiuni == 'createvm':
            INDEX, Nume = Argumente[Argumente.index('--uuid') + 1], Argumente[Argumente.index('--name') + 1]
            self.Mașini_virtuale[INDEX] = {'UUID': INDEX, 'name': Nume, 'VMState': 'poweroff',
                'CfgFile': str(self.rădăcină_VALUE / '.vbox/machines' / Nume / (Nume + '.vbox')), 'owner': None}
            return ''
        mașină = self.Mașini_virtuale[Argumente[2]]
        if Acțiuni == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Nume), json.dumps(VALUE)) for Nume, VALUE in mașină.items() if Nume != 'owner')
        if Acțiuni == 'getextradata': return 'Value: ' + mașină['owner'] if mașină['owner'] else 'No value set!'
        if Acțiuni == 'setextradata': mașină['owner'] = Argumente[4]
        elif Acțiuni == 'storagectl': mașină['storagecontrollername0'] = 'JKOROS IDE'
        elif Acțiuni == 'storageattach': mașină['JKOROS IDE-0-0'] = Argumente[Argumente.index('--medium') + 1]
        elif Acțiuni == 'startvm': mașină['VMState'] = 'running'
        elif Acțiuni == 'controlvm':
            assert Argumente[3] == 'resume'
            mașină['VMState'] = 'running'
        elif Acțiuni != 'modifyvm': raise AssertionError(Argumente)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.rădăcină_VALUE = Path(self.임시.name)
        (self.rădăcină_VALUE / '.vbox').mkdir()
        self.상자 = 가짜상자(self.rădăcină_VALUE)
        self.executa_comandă = modul_VALUE.program_ecrane_de_lansare(self.rădăcină_VALUE, 'jkoros operating system', Comandă=self.상자)

    def crea_intrare(self):
        KR = self.executa_comandă.executa_comandă()
        self.상자.명령들.clear()
        return self.상자.Mașini_virtuale[KR['uuid']]

    def 변경없음(self):
        self.assertTrue(all(Comandă[0] == 'VBoxManage' and Comandă[1] in ('list', 'showvminfo', 'getextradata') for Comandă in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        KR = self.executa_comandă.executa_comandă()
        self.assertEqual(KR['state'], 'running')
        self.assertTrue(Path(KR['iso']).is_file())
        self.assertTrue(any('--nic1' in Comandă and 'none' in Comandă for Comandă in self.상자.명령들))
        self.assertFalse(any('hdd' in Comandă or 'discardstate' in Comandă or 'createmedium' in Comandă for Comandă in self.상자.명령들))

    def test_실행중유지(self):
        self.crea_intrare()
        self.assertEqual(self.executa_comandă.executa_comandă()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        mașină = self.crea_intrare()
        mașină['VMState'] = 'saved'
        LOG_VALUE = self.executa_comandă.Cale(self.executa_comandă.Citire()['serial_log'])
        LOG_VALUE.write_text('saved log')
        self.executa_comandă.executa_comandă()
        self.assertFalse(any(Comandă[0] == 'make' or Comandă[1] == 'modifyvm' for Comandă in self.상자.명령들))
        self.assertEqual([Cale.read_text() for Cale in LOG_VALUE.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.crea_intrare()['VMState'] = 'paused'
        self.executa_comandă.executa_comandă()
        self.assertTrue(any(Comandă[1] == 'controlvm' and Comandă[3] == 'resume' for Comandă in self.상자.명령들))
        self.assertFalse(any(Comandă[0] == 'make' for Comandă in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.Mașini_virtuale[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(modul_VALUE.executare_eroare): self.executa_comandă.executa_comandă()
        self.변경없음()

    def test_소유표식거부(self):
        self.crea_intrare()['owner'] = 'someone-else'
        with self.assertRaises(modul_VALUE.executare_eroare): self.executa_comandă.executa_comandă()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.crea_intrare()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(modul_VALUE.executare_eroare): self.executa_comandă.executa_comandă()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        mașină = self.crea_intrare()
        mașină['VMState'] = 'poweroff'
        mașină['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(modul_VALUE.executare_eroare): self.executa_comandă.executa_comandă()
        self.변경없음()

    def test_전환중거부(self):
        self.crea_intrare()['VMState'] = 'saving'
        with self.assertRaises(modul_VALUE.executare_eroare): self.executa_comandă.executa_comandă()
        self.변경없음()

    def test_등록해제거부(self):
        self.crea_intrare()
        self.상자.Mașini_virtuale.clear()
        with self.assertRaises(modul_VALUE.executare_eroare): self.executa_comandă.executa_comandă()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        mașină = self.crea_intrare()
        mașină['VMState'] = 'poweroff'
        Anteriorul_element = dict(mașină)
        self.상자.eroare_VALUE = 'make'
        with self.assertRaises(modul_VALUE.executare_eroare): self.executa_comandă.executa_comandă()
        self.assertEqual(mașină, Anteriorul_element)

    def test_중단된소유표식설정복구(self):
        self.상자.eroare_VALUE = 'setextradata'
        with self.assertRaises(modul_VALUE.executare_eroare): self.executa_comandă.executa_comandă()
        self.상자.명령들.clear()
        self.assertEqual(self.executa_comandă.executa_comandă()['state'], 'running')
        self.assertFalse(any(Comandă[1] == 'createvm' for Comandă in self.상자.명령들))

    def test_보존ISO변조거부(self):
        mașină = self.crea_intrare()
        mașină['VMState'] = 'poweroff'
        Path(mașină['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(modul_VALUE.executare_eroare): self.executa_comandă.executa_comandă()

    def test_상태미생성(self):
        self.assertEqual(self.executa_comandă.afișa_Stare()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for Cale in ('../outside', '/tmp/outside'):
            with self.assertRaises(modul_VALUE.executare_eroare): self.executa_comandă.Cale(Cale)
        (self.rădăcină_VALUE / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(modul_VALUE.executare_eroare): self.executa_comandă.Cale('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        KR = modul_VALUE.atribut_VALUE('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(KR['VMState'], 'running')
        self.assertEqual(KR['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
