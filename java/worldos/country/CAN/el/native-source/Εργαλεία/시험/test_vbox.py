import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Ορισμός_τιμή = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
μονάδα_τιμή = importlib.util.module_from_spec(Ορισμός_τιμή)
Ορισμός_τιμή.loader.exec_module(μονάδα_τιμή)


class 가짜상자:
    def __init__(self, ρίζα_τιμή):
        self.ρίζα_τιμή = ρίζα_τιμή
        self.명령들 = []
        self.Εικονικές_μηχανές = {}
        self.αποτυχία_τιμή = None

    def __call__(self, Παράμετροι):
        Παράμετροι = list(map(str, Παράμετροι))
        self.명령들.append(Παράμετροι)
        if self.αποτυχία_τιμή == Παράμετροι[1] or (Παράμετροι[0] == 'make' and self.αποτυχία_τιμή == 'make'):
            self.αποτυχία_τιμή = None
            raise μονάδα_τιμή.εκτέλεση_σφάλμα('시험용 αποτυχία_τιμή')
        if Παράμετροι[0] == 'make':
            ΔΙΑΔΡΟΜΗ = self.ρίζα_τιμή / 'os/build/kernel.iso'
            ΔΙΑΔΡΟΜΗ.parent.mkdir(parents=True, exist_ok=True)
            ΔΙΑΔΡΟΜΗ.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Ενέργεια = Παράμετροι[1]
        if Ενέργεια == 'list':
            return '\n'.join('"{}" {{{}}}'.format(τιμή['name'], Ευρετήριο) for Ευρετήριο, τιμή in self.Εικονικές_μηχανές.items())
        if Ενέργεια == 'createvm':
            Ευρετήριο, Όνομα = Παράμετροι[Παράμετροι.index('--uuid') + 1], Παράμετροι[Παράμετροι.index('--name') + 1]
            self.Εικονικές_μηχανές[Ευρετήριο] = {'UUID': Ευρετήριο, 'name': Όνομα, 'VMState': 'poweroff',
                'CfgFile': str(self.ρίζα_τιμή / '.vbox/machines' / Όνομα / (Όνομα + '.vbox')), 'owner': None}
            return ''
        υπολογιστής_5eb260fa = self.Εικονικές_μηχανές[Παράμετροι[2]]
        if Ενέργεια == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Όνομα), json.dumps(τιμή)) for Όνομα, τιμή in υπολογιστής_5eb260fa.items() if Όνομα != 'owner')
        if Ενέργεια == 'getextradata': return 'Value: ' + υπολογιστής_5eb260fa['owner'] if υπολογιστής_5eb260fa['owner'] else 'No value set!'
        if Ενέργεια == 'setextradata': υπολογιστής_5eb260fa['owner'] = Παράμετροι[4]
        elif Ενέργεια == 'storagectl': υπολογιστής_5eb260fa['storagecontrollername0'] = 'JKOROS IDE'
        elif Ενέργεια == 'storageattach': υπολογιστής_5eb260fa['JKOROS IDE-0-0'] = Παράμετροι[Παράμετροι.index('--medium') + 1]
        elif Ενέργεια == 'startvm': υπολογιστής_5eb260fa['VMState'] = 'running'
        elif Ενέργεια == 'controlvm':
            assert Παράμετροι[3] == 'resume'
            υπολογιστής_5eb260fa['VMState'] = 'running'
        elif Ενέργεια != 'modifyvm': raise AssertionError(Παράμετροι)
        return ''


class εκτέλεση_δοκιμής(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.ρίζα_τιμή = Path(self.임시.name)
        (self.ρίζα_τιμή / '.vbox').mkdir()
        self.상자 = 가짜상자(self.ρίζα_τιμή)
        self.εκτελώ_εντολή = μονάδα_τιμή.εφαρμογή_εκκίνηση(self.ρίζα_τιμή, 'jkoros operating system', Εντολή=self.상자)

    def ανοίγω_καταχώρηση(self):
        μέτρηση = self.εκτελώ_εντολή.εκτελώ_εντολή()
        self.상자.명령들.clear()
        return self.상자.Εικονικές_μηχανές[μέτρηση['uuid']]

    def 변경없음(self):
        self.assertTrue(all(Εντολή[0] == 'VBoxManage' and Εντολή[1] in ('list', 'showvminfo', 'getextradata') for Εντολή in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        μέτρηση = self.εκτελώ_εντολή.εκτελώ_εντολή()
        self.assertEqual(μέτρηση['state'], 'running')
        self.assertTrue(Path(μέτρηση['iso']).is_file())
        self.assertTrue(any('--nic1' in Εντολή and 'none' in Εντολή for Εντολή in self.상자.명령들))
        self.assertFalse(any('hdd' in Εντολή or 'discardstate' in Εντολή or 'createmedium' in Εντολή for Εντολή in self.상자.명령들))

    def test_실행중유지(self):
        self.ανοίγω_καταχώρηση()
        self.assertEqual(self.εκτελώ_εντολή.εκτελώ_εντολή()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        υπολογιστής_5eb260fa = self.ανοίγω_καταχώρηση()
        υπολογιστής_5eb260fa['VMState'] = 'saved'
        καταγράφω_τιμή = self.εκτελώ_εντολή.ΔΙΑΔΡΟΜΗ(self.εκτελώ_εντολή.Ανάγνωση()['serial_log'])
        καταγράφω_τιμή.write_text('saved log')
        self.εκτελώ_εντολή.εκτελώ_εντολή()
        self.assertFalse(any(Εντολή[0] == 'make' or Εντολή[1] == 'modifyvm' for Εντολή in self.상자.명령들))
        self.assertEqual([ΔΙΑΔΡΟΜΗ.read_text() for ΔΙΑΔΡΟΜΗ in καταγράφω_τιμή.parent.glob('before-resume-*.log')], ['saved log'])

    def δοκιμή_Παύση_λογικό_ΚΑΙ_συνέχιση(self):
        self.ανοίγω_καταχώρηση()['VMState'] = 'paused'
        self.εκτελώ_εντολή.εκτελώ_εντολή()
        self.assertTrue(any(Εντολή[1] == 'controlvm' and Εντολή[3] == 'resume' for Εντολή in self.상자.명령들))
        self.assertFalse(any(Εντολή[0] == 'make' for Εντολή in self.상자.명령들))

    def δοκιμή_Άλλο_εικονική_μηχανή_όνομα_διένεξη(self):
        self.상자.Εικονικές_μηχανές[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(μονάδα_τιμή.εκτέλεση_σφάλμα): self.εκτελώ_εντολή.εκτελώ_εντολή()
        self.변경없음()

    def test_소유표식거부(self):
        self.ανοίγω_καταχώρηση()['owner'] = 'someone-else'
        with self.assertRaises(μονάδα_τιμή.εκτέλεση_σφάλμα): self.εκτελώ_εντολή.εκτελώ_εντολή()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.ανοίγω_καταχώρηση()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(μονάδα_τιμή.εκτέλεση_σφάλμα): self.εκτελώ_εντολή.εκτελώ_εντολή()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        υπολογιστής_5eb260fa = self.ανοίγω_καταχώρηση()
        υπολογιστής_5eb260fa['VMState'] = 'poweroff'
        υπολογιστής_5eb260fa['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(μονάδα_τιμή.εκτέλεση_σφάλμα): self.εκτελώ_εντολή.εκτελώ_εντολή()
        self.변경없음()

    def test_전환중거부(self):
        self.ανοίγω_καταχώρηση()['VMState'] = 'saving'
        with self.assertRaises(μονάδα_τιμή.εκτέλεση_σφάλμα): self.εκτελώ_εντολή.εκτελώ_εντολή()
        self.변경없음()

    def test_등록해제거부(self):
        self.ανοίγω_καταχώρηση()
        self.상자.Εικονικές_μηχανές.clear()
        with self.assertRaises(μονάδα_τιμή.εκτέλεση_σφάλμα): self.εκτελώ_εντολή.εκτελώ_εντολή()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        υπολογιστής_5eb260fa = self.ανοίγω_καταχώρηση()
        υπολογιστής_5eb260fa['VMState'] = 'poweroff'
        이전 = dict(υπολογιστής_5eb260fa)
        self.상자.αποτυχία_τιμή = 'make'
        with self.assertRaises(μονάδα_τιμή.εκτέλεση_σφάλμα): self.εκτελώ_εντολή.εκτελώ_εντολή()
        self.assertEqual(υπολογιστής_5eb260fa, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.αποτυχία_τιμή = 'setextradata'
        with self.assertRaises(μονάδα_τιμή.εκτέλεση_σφάλμα): self.εκτελώ_εντολή.εκτελώ_εντολή()
        self.상자.명령들.clear()
        self.assertEqual(self.εκτελώ_εντολή.εκτελώ_εντολή()['state'], 'running')
        self.assertFalse(any(Εντολή[1] == 'createvm' for Εντολή in self.상자.명령들))

    def test_보존ISO변조거부(self):
        υπολογιστής_5eb260fa = self.ανοίγω_καταχώρηση()
        υπολογιστής_5eb260fa['VMState'] = 'poweroff'
        Path(υπολογιστής_5eb260fa['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(μονάδα_τιμή.εκτέλεση_σφάλμα): self.εκτελώ_εντολή.εκτελώ_εντολή()

    def test_상태미생성(self):
        self.assertEqual(self.εκτελώ_εντολή.εμφανίζω_Κατάσταση()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for ΔΙΑΔΡΟΜΗ in ('../outside', '/tmp/outside'):
            with self.assertRaises(μονάδα_τιμή.εκτέλεση_σφάλμα): self.εκτελώ_εντολή.ΔΙΑΔΡΟΜΗ(ΔΙΑΔΡΟΜΗ)
        (self.ρίζα_τιμή / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(μονάδα_τιμή.εκτέλεση_σφάλμα): self.εκτελώ_εντολή.ΔΙΑΔΡΟΜΗ('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        μέτρηση = μονάδα_τιμή.χαρακτηριστικό_τιμή_286d43f0('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(μέτρηση['VMState'], 'running')
        self.assertEqual(μέτρηση['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
