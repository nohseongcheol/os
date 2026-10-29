import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

giáTrịĐịnhNghĩa = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / 'VirtualBox.py'))
giáTrịMôĐun = importlib.util.module_from_spec(giáTrịĐịnhNghĩa)
giáTrịĐịnhNghĩa.loader.exec_module(giáTrịMôĐun)


class HộpGiả:
    def __init__(self, giáTrịGốcCây):
        self.giáTrịGốcCây = giáTrịGốcCây
        self.danhSáchCácLệnh = []
        self.cácMáyẢo = {}
        self.giáTrịSựThấtBại = None

    def __call__(self, cácĐốiSố):
        cácĐốiSố = list(map(str, cácĐốiSố))
        self.danhSáchCácLệnh.append(cácĐốiSố)
        if self.giáTrịSựThấtBại == cácĐốiSố[1] or (cácĐốiSố[0] == 'make' and self.giáTrịSựThấtBại == 'make'):
            self.giáTrịSựThấtBại = None
            raise giáTrịMôĐun.lỗiViệcThựcThi('시험용 giáTrịSựThấtBại')
        if cácĐốiSố[0] == 'make':
            đườngDẫn = self.giáTrịGốcCây / 'os/build/kernel.iso'
            đườngDẫn.parent.mkdir(parents=True, exist_ok=True)
            đườngDẫn.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        hànhĐộng = cácĐốiSố[1]
        if hànhĐộng == 'list':
            return '\n'.join('"{}" {{{}}}'.format(giáTrị['name'], sốHiệu) for sốHiệu, giáTrị in self.cácMáyẢo.items())
        if hànhĐộng == 'createvm':
            sốHiệu, tên = cácĐốiSố[cácĐốiSố.index('--uuid') + 1], cácĐốiSố[cácĐốiSố.index('--name') + 1]
            self.cácMáyẢo[sốHiệu] = {'UUID': sốHiệu, 'name': tên, 'VMState': 'poweroff',
                'CfgFile': str(self.giáTrịGốcCây / '.vbox/machines' / tên / (tên + '.vbox')), 'owner': None}
            return ''
        máy = self.cácMáyẢo[cácĐốiSố[2]]
        if hànhĐộng == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(tên), json.dumps(giáTrị)) for tên, giáTrị in máy.items() if tên != 'owner')
        if hànhĐộng == 'getextradata': return 'Value: ' + máy['owner'] if máy['owner'] else 'No value set!'
        if hànhĐộng == 'setextradata': máy['owner'] = cácĐốiSố[4]
        elif hànhĐộng == 'storagectl': máy['storagecontrollername0'] = 'JKOROS IDE'
        elif hànhĐộng == 'storageattach': máy['JKOROS IDE-0-0'] = cácĐốiSố[cácĐốiSố.index('--medium') + 1]
        elif hànhĐộng == 'startvm': máy['VMState'] = 'running'
        elif hànhĐộng == 'controlvm':
            assert cácĐốiSố[3] == 'resume'
            máy['VMState'] = 'running'
        elif hànhĐộng != 'modifyvm': raise AssertionError(cácĐốiSố)
        return ''


class thửChạy(unittest.TestCase):
    def setUp(self):
        self.giáTrịTạm = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.giáTrịTạm.cleanup)
        self.giáTrịGốcCây = Path(self.giáTrịTạm.name)
        (self.giáTrịGốcCây / '.vbox').mkdir()
        self.giáTrịHộp = HộpGiả(self.giáTrịGốcCây)
        self.thựcThiLệnh = giáTrịMôĐun.TrìnhKhởiChạyChươngTrình(self.giáTrịGốcCây, 'jkoros operating system', lệnh=self.giáTrịHộp)

    def tạoMục(self):
        kếtQuả = self.thựcThiLệnh.thựcThiLệnh()
        self.giáTrịHộp.danhSáchCácLệnh.clear()
        return self.giáTrịHộp.cácMáyẢo[kếtQuả['uuid']]

    def làGiữNguyênTrạng(self):
        self.assertTrue(all(lệnh[0] == 'VBoxManage' and lệnh[1] in ('list', 'showvminfo', 'getextradata') for lệnh in self.giáTrịHộp.danhSáchCácLệnh))

    def thửKhởiĐộngQuangHọcVàViệcTạoBanĐầu(self):
        kếtQuả = self.thựcThiLệnh.thựcThiLệnh()
        self.assertEqual(kếtQuả['state'], 'running')
        self.assertTrue(Path(kếtQuả['iso']).is_file())
        self.assertTrue(any('--nic1' in lệnh and 'none' in lệnh for lệnh in self.giáTrịHộp.danhSáchCácLệnh))
        self.assertFalse(any('hdd' in lệnh or 'discardstate' in lệnh or 'createmedium' in lệnh for lệnh in self.giáTrịHộp.danhSáchCácLệnh))

    def thửĐãGiữNguyênMáyẢoGọnĐangChạy(self):
        self.tạoMục()
        self.assertEqual(self.thựcThiLệnh.thựcThiLệnh()['state'], 'running')
        self.làGiữNguyênTrạng()

    def thửViệcGiữNguyênNhậtKýVàTiếpDiễnTrạngTháiĐãLưu(self):
        máy = self.tạoMục()
        máy['VMState'] = 'saved'
        giáTrịNhậtKý = self.thựcThiLệnh.đườngDẫn(self.thựcThiLệnh.đọc()['serial_log'])
        giáTrịNhậtKý.write_text('saved log')
        self.thựcThiLệnh.thựcThiLệnh()
        self.assertFalse(any(lệnh[0] == 'make' or lệnh[1] == 'modifyvm' for lệnh in self.giáTrịHộp.danhSáchCácLệnh))
        self.assertEqual([đườngDẫn.read_text() for đườngDẫn in giáTrịNhậtKý.parent.glob('before-resume-*.log')], ['saved log'])

    def thửTiếpDiễnVàTạmDừng(self):
        self.tạoMục()['VMState'] = 'paused'
        self.thựcThiLệnh.thựcThiLệnh()
        self.assertTrue(any(lệnh[1] == 'controlvm' and lệnh[3] == 'resume' for lệnh in self.giáTrịHộp.danhSáchCácLệnh))
        self.assertFalse(any(lệnh[0] == 'make' for lệnh in self.giáTrịHộp.danhSáchCácLệnh))

    def thửXungĐộtTênMáyẢoGọnKhác(self):
        self.giáTrịHộp.cácMáyẢo[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(giáTrịMôĐun.lỗiViệcThựcThi): self.thựcThiLệnh.thựcThiLệnh()
        self.làGiữNguyênTrạng()

    def thửĐãTừChốiDấuMốcQuyềnSởHữu(self):
        self.tạoMục()['owner'] = 'someone-else'
        with self.assertRaises(giáTrịMôĐun.lỗiViệcThựcThi): self.thựcThiLệnh.thựcThiLệnh()
        self.làGiữNguyênTrạng()

    def thửĐãTừChốiĐườngDẫnCácThiếtLậpKhác(self):
        self.tạoMục()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(giáTrịMôĐun.lỗiViệcThựcThi): self.thựcThiLệnh.thựcThiLệnh()
        self.làGiữNguyênTrạng()

    def thửĐãGiữNguyênĐĩaNgườiDùngBổSung(self):
        máy = self.tạoMục()
        máy['VMState'] = 'poweroff'
        máy['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(giáTrịMôĐun.lỗiViệcThựcThi): self.thựcThiLệnh.thựcThiLệnh()
        self.làGiữNguyênTrạng()

    def thửĐãTừChốiChuyểnTrạngThái(self):
        self.tạoMục()['VMState'] = 'saving'
        with self.assertRaises(giáTrịMôĐun.lỗiViệcThựcThi): self.thựcThiLệnh.thựcThiLệnh()
        self.làGiữNguyênTrạng()

    def thửĐãTừChốiHủyĐăngKý(self):
        self.tạoMục()
        self.giáTrịHộp.cácMáyẢo.clear()
        with self.assertRaises(giáTrịMôĐun.lỗiViệcThựcThi): self.thựcThiLệnh.thựcThiLệnh()
        self.làGiữNguyênTrạng()

    def thửSựThấtBạiXâyDựngBậtTrạngTháiĐãGiữNguyênMáyẢoGọn(self):
        máy = self.tạoMục()
        máy['VMState'] = 'poweroff'
        phầnMụcTrướcĐó = dict(máy)
        self.giáTrịHộp.giáTrịSựThấtBại = 'make'
        with self.assertRaises(giáTrịMôĐun.lỗiViệcThựcThi): self.thựcThiLệnh.thựcThiLệnh()
        self.assertEqual(máy, phầnMụcTrướcĐó)

    def thửViệcKhôiPhụcDấuMốcQuyềnSởHữuĐãBịNgắt(self):
        self.giáTrịHộp.giáTrịSựThấtBại = 'setextradata'
        with self.assertRaises(giáTrịMôĐun.lỗiViệcThựcThi): self.thựcThiLệnh.thựcThiLệnh()
        self.giáTrịHộp.danhSáchCácLệnh.clear()
        self.assertEqual(self.thựcThiLệnh.thựcThiLệnh()['state'], 'running')
        self.assertFalse(any(lệnh[1] == 'createvm' for lệnh in self.giáTrịHộp.danhSáchCácLệnh))

    def thửĐãTừChốiCanThiệpTráiPhépISOĐãGiữNguyên(self):
        máy = self.tạoMục()
        máy['VMState'] = 'poweroff'
        Path(máy['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(giáTrịMôĐun.lỗiViệcThựcThi): self.thựcThiLệnh.thựcThiLệnh()

    def thửĐãTạoTrạngTháiKhôngCó(self):
        self.assertEqual(self.thựcThiLệnh.hiệnTrạngThái()['state'], 'not-created')
        self.assertFalse(self.giáTrịHộp.danhSáchCácLệnh)

    def thửĐãTừChốiThoátĐườngDẫn(self):
        for đườngDẫn in ('../outside', '/tmp/outside'):
            with self.assertRaises(giáTrịMôĐun.lỗiViệcThựcThi): self.thựcThiLệnh.đườngDẫn(đườngDẫn)
        (self.giáTrịGốcCây / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(giáTrịMôĐun.lỗiViệcThựcThi): self.thựcThiLệnh.đườngDẫn('media/kernel.iso')

    def thửCácĐặcTínhTổngHợp52VirtualBox(self):
        kếtQuả = giáTrịMôĐun.giáTrịThuộcTính('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(kếtQuả['VMState'], 'running')
        self.assertEqual(kếtQuả['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
