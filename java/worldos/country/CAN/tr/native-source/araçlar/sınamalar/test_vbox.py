import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

Tanım_değer = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / '가상상자.py'))
modül_değer = importlib.util.module_from_spec(Tanım_değer)
Tanım_değer.loader.exec_module(modül_değer)


class 가짜상자:
    def __init__(self, kök_değer):
        self.kök_değer = kök_değer
        self.명령들 = []
        self.Sanal_Makineler = {}
        self.hata_değer = None

    def __call__(self, bağımsız_değişkenler):
        bağımsız_değişkenler = list(map(str, bağımsız_değişkenler))
        self.명령들.append(bağımsız_değişkenler)
        if self.hata_değer == bağımsız_değişkenler[1] or (bağımsız_değişkenler[0] == 'make' and self.hata_değer == 'make'):
            self.hata_değer = None
            raise modül_değer.yürütme_hata('시험용 hata_değer')
        if bağımsız_değişkenler[0] == 'make':
            yol = self.kök_değer / 'os/build/kernel.iso'
            yol.parent.mkdir(parents=True, exist_ok=True)
            yol.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        Eylem = bağımsız_değişkenler[1]
        if Eylem == 'list':
            return '\n'.join('"{}" {{{}}}'.format(değer['name'], Dizin) for Dizin, değer in self.Sanal_Makineler.items())
        if Eylem == 'createvm':
            Dizin, İsim = bağımsız_değişkenler[bağımsız_değişkenler.index('--uuid') + 1], bağımsız_değişkenler[bağımsız_değişkenler.index('--name') + 1]
            self.Sanal_Makineler[Dizin] = {'UUID': Dizin, 'name': İsim, 'VMState': 'poweroff',
                'CfgFile': str(self.kök_değer / '.vbox/machines' / İsim / (İsim + '.vbox')), 'owner': None}
            return ''
        makine = self.Sanal_Makineler[bağımsız_değişkenler[2]]
        if Eylem == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(İsim), json.dumps(değer)) for İsim, değer in makine.items() if İsim != 'owner')
        if Eylem == 'getextradata': return 'Value: ' + makine['owner'] if makine['owner'] else 'No value set!'
        if Eylem == 'setextradata': makine['owner'] = bağımsız_değişkenler[4]
        elif Eylem == 'storagectl': makine['storagecontrollername0'] = 'JKOROS IDE'
        elif Eylem == 'storageattach': makine['JKOROS IDE-0-0'] = bağımsız_değişkenler[bağımsız_değişkenler.index('--medium') + 1]
        elif Eylem == 'startvm': makine['VMState'] = 'running'
        elif Eylem == 'controlvm':
            assert bağımsız_değişkenler[3] == 'resume'
            makine['VMState'] = 'running'
        elif Eylem != 'modifyvm': raise AssertionError(bağımsız_değişkenler)
        return ''


class test_çalıştırması(unittest.TestCase):
    def setUp(self):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.임시.cleanup)
        self.kök_değer = Path(self.임시.name)
        (self.kök_değer / '.vbox').mkdir()
        self.상자 = 가짜상자(self.kök_değer)
        self.yürütmek_komut = modül_değer.program_Launcher(self.kök_değer, 'jkoros operating system', komut=self.상자)

    def açmak_girdi(self):
        sonuç = self.yürütmek_komut.yürütmek_komut()
        self.상자.명령들.clear()
        return self.상자.Sanal_Makineler[sonuç['uuid']]

    def 변경없음(self):
        self.assertTrue(all(komut[0] == 'VBoxManage' and komut[1] in ('list', 'showvminfo', 'getextradata') for komut in self.상자.명령들))

    def test_첫생성과광학부팅(self):
        sonuç = self.yürütmek_komut.yürütmek_komut()
        self.assertEqual(sonuç['state'], 'running')
        self.assertTrue(Path(sonuç['iso']).is_file())
        self.assertTrue(any('--nic1' in komut and 'none' in komut for komut in self.상자.명령들))
        self.assertFalse(any('hdd' in komut or 'discardstate' in komut or 'createmedium' in komut for komut in self.상자.명령들))

    def test_실행중유지(self):
        self.açmak_girdi()
        self.assertEqual(self.yürütmek_komut.yürütmek_komut()['state'], 'running')
        self.변경없음()

    def test_저장상태재개와로그보존(self):
        makine = self.açmak_girdi()
        makine['VMState'] = 'saved'
        LOG_değer = self.yürütmek_komut.yol(self.yürütmek_komut.Okuma()['serial_log'])
        LOG_değer.write_text('saved log')
        self.yürütmek_komut.yürütmek_komut()
        self.assertFalse(any(komut[0] == 'make' or komut[1] == 'modifyvm' for komut in self.상자.명령들))
        self.assertEqual([yol.read_text() for yol in LOG_değer.parent.glob('before-resume-*.log')], ['saved log'])

    def test_Duraklat_VE_özgeçmiş(self):
        self.açmak_girdi()['VMState'] = 'paused'
        self.yürütmek_komut.yürütmek_komut()
        self.assertTrue(any(komut[1] == 'controlvm' and komut[3] == 'resume' for komut in self.상자.명령들))
        self.assertFalse(any(komut[0] == 'make' for komut in self.상자.명령들))

    def test_Diğer_VM_ad_çarpışma(self):
        self.상자.Sanal_Makineler[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(modül_değer.yürütme_hata): self.yürütmek_komut.yürütmek_komut()
        self.변경없음()

    def test_소유표식거부(self):
        self.açmak_girdi()['owner'] = 'someone-else'
        with self.assertRaises(modül_değer.yürütme_hata): self.yürütmek_komut.yürütmek_komut()
        self.변경없음()

    def test_다른설정경로거부(self):
        self.açmak_girdi()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(modül_değer.yürütme_hata): self.yürütmek_komut.yürütmek_komut()
        self.변경없음()

    def test_사용자추가디스크보존(self):
        makine = self.açmak_girdi()
        makine['VMState'] = 'poweroff'
        makine['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(modül_değer.yürütme_hata): self.yürütmek_komut.yürütmek_komut()
        self.변경없음()

    def test_전환중거부(self):
        self.açmak_girdi()['VMState'] = 'saving'
        with self.assertRaises(modül_değer.yürütme_hata): self.yürütmek_komut.yürütmek_komut()
        self.변경없음()

    def test_등록해제거부(self):
        self.açmak_girdi()
        self.상자.Sanal_Makineler.clear()
        with self.assertRaises(modül_değer.yürütme_hata): self.yürütmek_komut.yürütmek_komut()
        self.변경없음()

    def test_빌드실패시VM유지(self):
        makine = self.açmak_girdi()
        makine['VMState'] = 'poweroff'
        Önceki_öğe = dict(makine)
        self.상자.hata_değer = 'make'
        with self.assertRaises(modül_değer.yürütme_hata): self.yürütmek_komut.yürütmek_komut()
        self.assertEqual(makine, Önceki_öğe)

    def test_중단된소유표식설정복구(self):
        self.상자.hata_değer = 'setextradata'
        with self.assertRaises(modül_değer.yürütme_hata): self.yürütmek_komut.yürütmek_komut()
        self.상자.명령들.clear()
        self.assertEqual(self.yürütmek_komut.yürütmek_komut()['state'], 'running')
        self.assertFalse(any(komut[1] == 'createvm' for komut in self.상자.명령들))

    def test_보존ISO변조거부(self):
        makine = self.açmak_girdi()
        makine['VMState'] = 'poweroff'
        Path(makine['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(modül_değer.yürütme_hata): self.yürütmek_komut.yürütmek_komut()

    def test_상태미생성(self):
        self.assertEqual(self.yürütmek_komut.şov_Durum()['state'], 'not-created')
        self.assertFalse(self.상자.명령들)

    def test_경로탈출거부(self):
        for yol in ('../outside', '/tmp/outside'):
            with self.assertRaises(modül_değer.yürütme_hata): self.yürütmek_komut.yol(yol)
        (self.kök_değer / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(modül_değer.yürütme_hata): self.yürütmek_komut.yol('media/kernel.iso')

    def test_VirtualBox52복합속성(self):
        sonuç = modül_değer.öznitelik_değer('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(sonuç['VMState'], 'running')
        self.assertEqual(sonuç['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
