import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Definisi_VALUE = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
modul_VALUE = importlib.util.module_from_spec(Definisi_VALUE)
Definisi_VALUE.loader.exec_module(modul_VALUE)


class 가짜상자:
    def __init__(self, akar_VALUE):
        self.akar_VALUE = akar_VALUE
        self.명령들 = []
        self.Virtual_Machines = {}
        self.kegagalan_VALUE = None

    def __call__(self, argumen):
        argumen = list(map(str, argumen))
        self.명령들.append(argumen)
        if self.kegagalan_VALUE == argumen[1] or (argumen[0] == 'make' and self.kegagalan_VALUE == 'make'):
            self.kegagalan_VALUE = None
            raise modul_VALUE.실행오류('시험용 kegagalan_VALUE')
        if argumen[0] == 'make':
            jalur = self.akar_VALUE / 'os/build/kernel.iso'
            jalur.parent.mkdir(parents=True, exist_ok=True)
            jalur.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Aksi = argumen[1]
        if Aksi == 'list':
            return '\n'.join('"{}" {{{}}}'.format(VALUE['name'], INDEX) for INDEX, VALUE in self.Virtual_Machines.items())
        if Aksi == 'createvm':
            INDEX, Nama_2 = argumen[argumen.index('--uuid') + 1], argumen[argumen.index('--name') + 1]
            self.Virtual_Machines[INDEX] = {'UUID': INDEX, 'name': Nama_2, 'VMState': 'poweroff',
                'CfgFile': str(self.akar_VALUE / '.vbox/machines' / Nama_2 / (Nama_2 + '.vbox')), 'owner': None}
            return ''
        mesin = self.Virtual_Machines[argumen[2]]
        if Aksi == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Nama_2), json.dumps(VALUE)) for Nama_2, VALUE in mesin.items() if Nama_2 != 'owner')
        if Aksi == 'getextradata': return 'Value: ' + mesin['owner'] if mesin['owner'] else 'No value set!'
        if Aksi == 'setextradata': mesin['owner'] = argumen[4]
        elif Aksi == 'storagectl': mesin['storagecontrollername0'] = 'JKOROS IDE'
        elif Aksi == 'storageattach': mesin['JKOROS IDE-0-0'] = argumen[argumen.index('--medium') + 1]
        elif Aksi == 'startvm': mesin['VMState'] = 'running'
        elif Aksi == 'controlvm':
            assert argumen[3] == 'resume'
            mesin['VMState'] = 'running'
        elif Aksi != 'modifyvm': raise AssertionError(argumen)
        return ''


class 실행시험(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.akar_VALUE = Path(self.임시.name)
        (self.akar_VALUE / '.vbox').mkdir()
        self.상자 = 가짜상자(self.akar_VALUE)
        self.Jalankan_perintah = modul_VALUE.apl_peluncur(self.akar_VALUE, 'jkoros operating system', perintah=self.상자)

    def Buat_entri(self):
        hasil = self.Jalankan_perintah.Jalankan_perintah()
        self.상자.명령들.clear()
        return self.상자.Virtual_Machines[hasil['uuid']]

    def 변경없음(self):
        self.assertTrue(all(perintah[0] == 'VBoxManage' and perintah[1] in ('list', 'showvminfo', 'getextradata') for perintah in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        hasil = self.Jalankan_perintah.Jalankan_perintah()
        self.assertEqual(hasil['state'], 'running')
        self.assertTrue(Path(hasil['iso']).is_file())
        self.assertTrue(any('--nic1' in perintah and 'none' in perintah for perintah in self.상자.명령들))
        self.assertFalse(any('hdd' in perintah or 'discardstate' in perintah or 'createmedium' in perintah for perintah in self.상자.명령들))

    def test_실행중유지(self):
        self.Buat_entri()
        self.assertEqual(self.Jalankan_perintah.Jalankan_perintah()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        mesin = self.Buat_entri()
        mesin['VMState'] = 'saved'
        LOG_VALUE = self.Jalankan_perintah.jalur(self.Jalankan_perintah.Baca()['serial_log'])
        LOG_VALUE.write_text('saved log')
        self.Jalankan_perintah.Jalankan_perintah()
        self.assertFalse(any(perintah[0] == 'make' or perintah[1] == 'modifyvm' for perintah in self.상자.명령들))
        self.assertEqual([jalur.read_text() for jalur in LOG_VALUE.parent.glob('before-resume-*.log')], ['saved log'])

    def test_일시정지재개(self):
        self.Buat_entri()['VMState'] = 'paused'
        self.Jalankan_perintah.Jalankan_perintah()
        self.assertTrue(any(perintah[1] == 'controlvm' and perintah[3] == 'resume' for perintah in self.상자.명령들))
        self.assertFalse(any(perintah[0] == 'make' for perintah in self.상자.명령들))

    def test_다른VM이름충돌(self):
        self.상자.Virtual_Machines[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(modul_VALUE.실행오류): self.Jalankan_perintah.Jalankan_perintah()
        self.변경없음()

    def test_소유표식거부(self):
        self.Buat_entri()['owner'] = 'someone-else'
        with self.assertRaises(modul_VALUE.실행오류): self.Jalankan_perintah.Jalankan_perintah()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.Buat_entri()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(modul_VALUE.실행오류): self.Jalankan_perintah.Jalankan_perintah()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        mesin = self.Buat_entri()
        mesin['VMState'] = 'poweroff'
        mesin['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(modul_VALUE.실행오류): self.Jalankan_perintah.Jalankan_perintah()
        self.변경없음()

    def test_전환중거부(self):
        self.Buat_entri()['VMState'] = 'saving'
        with self.assertRaises(modul_VALUE.실행오류): self.Jalankan_perintah.Jalankan_perintah()
        self.변경없음()

    def test_등록해제거부(self):
        self.Buat_entri()
        self.상자.Virtual_Machines.clear()
        with self.assertRaises(modul_VALUE.실행오류): self.Jalankan_perintah.Jalankan_perintah()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        mesin = self.Buat_entri()
        mesin['VMState'] = 'poweroff'
        이전 = dict(mesin)
        self.상자.kegagalan_VALUE = 'make'
        with self.assertRaises(modul_VALUE.실행오류): self.Jalankan_perintah.Jalankan_perintah()
        self.assertEqual(mesin, 이전)

    def test_중단된소유표식설정복구(self):
        self.상자.kegagalan_VALUE = 'setextradata'
        with self.assertRaises(modul_VALUE.실행오류): self.Jalankan_perintah.Jalankan_perintah()
        self.상자.명령들.clear()
        self.assertEqual(self.Jalankan_perintah.Jalankan_perintah()['state'], 'running')
        self.assertFalse(any(perintah[1] == 'createvm' for perintah in self.상자.명령들))

    def test_보존ISO변조거부(self):
        mesin = self.Buat_entri()
        mesin['VMState'] = 'poweroff'
        Path(mesin['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(modul_VALUE.실행오류): self.Jalankan_perintah.Jalankan_perintah()

    def test_상태미생성(self):
        self.assertEqual(self.Jalankan_perintah.show_Status()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for jalur in ('../outside', '/tmp/outside'):
            with self.assertRaises(modul_VALUE.실행오류): self.Jalankan_perintah.jalur(jalur)
        (self.akar_VALUE / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(modul_VALUE.실행오류): self.Jalankan_perintah.jalur('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        hasil = modul_VALUE.nilai_atribut('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(hasil['VMState'], 'running')
        self.assertEqual(hasil['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
