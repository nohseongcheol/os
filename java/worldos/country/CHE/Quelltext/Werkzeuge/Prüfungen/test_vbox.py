import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

definitionWert = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / 'VirtualBox.py'))
modulWert = importlib.util.module_from_spec(definitionWert)
definitionWert.loader.exec_module(modulWert)


class NachbildungKasten:
    def __init__(self, wurzelWert):
        self.wurzelWert = wurzelWert
        self.befehleListe = []
        self.virtuellMaschinen = {}
        self.fehlschlagWert = None

    def __call__(self, argumente):
        argumente = list(map(str, argumente))
        self.befehleListe.append(argumente)
        if self.fehlschlagWert == argumente[1] or (argumente[0] == 'make' and self.fehlschlagWert == 'make'):
            self.fehlschlagWert = None
            raise modulWert.ausführungFehler('시험용 fehlschlagWert')
        if argumente[0] == 'make':
            pfad = self.wurzelWert / 'os/build/kernel.iso'
            pfad.parent.mkdir(parents=True, exist_ok=True)
            pfad.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        aktion = argumente[1]
        if aktion == 'list':
            return '\n'.join('"{}" {{{}}}'.format(Wert['name'], Nummer) for Nummer, Wert in self.virtuellMaschinen.items())
        if aktion == 'createvm':
            Nummer, Name = argumente[argumente.index('--uuid') + 1], argumente[argumente.index('--name') + 1]
            self.virtuellMaschinen[Nummer] = {'UUID': Nummer, 'name': Name, 'VMState': 'poweroff',
                'CfgFile': str(self.wurzelWert / '.vbox/machines' / Name / (Name + '.vbox')), 'owner': None}
            return ''
        maschine = self.virtuellMaschinen[argumente[2]]
        if aktion == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(Name), json.dumps(Wert)) for Name, Wert in maschine.items() if Name != 'owner')
        if aktion == 'getextradata': return 'Value: ' + maschine['owner'] if maschine['owner'] else 'No value set!'
        if aktion == 'setextradata': maschine['owner'] = argumente[4]
        elif aktion == 'storagectl': maschine['storagecontrollername0'] = 'JKOROS IDE'
        elif aktion == 'storageattach': maschine['JKOROS IDE-0-0'] = argumente[argumente.index('--medium') + 1]
        elif aktion == 'startvm': maschine['VMState'] = 'running'
        elif aktion == 'controlvm':
            assert argumente[3] == 'resume'
            maschine['VMState'] = 'running'
        elif aktion != 'modifyvm': raise AssertionError(argumente)
        return ''


class ausführenVorgangPrüfung(unittest.TestCase):
    def setUp(self):
        self.vorläufigWert = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.vorläufigWert.cleanup)
        self.wurzelWert = Path(self.vorläufigWert.name)
        (self.wurzelWert / '.vbox').mkdir()
        self.kastenWert = NachbildungKasten(self.wurzelWert)
        self.befehlAusführen = modulWert.ProgrammStarter(self.wurzelWert, 'jkoros operating system', befehl=self.kastenWert)

    def eintragErstellen(self):
        ergebnis = self.befehlAusführen.befehlAusführen()
        self.kastenWert.befehleListe.clear()
        return self.kastenWert.virtuellMaschinen[ergebnis['uuid']]

    def istUnverändert(self):
        self.assertTrue(all(befehl[0] == 'VBoxManage' and befehl[1] in ('list', 'showvminfo', 'getextradata') for befehl in self.kastenWert.befehleListe))

    def anfänglichErstellungUndOptischStartvorgangPrüfung(self):
        ergebnis = self.befehlAusführen.befehlAusführen()
        self.assertEqual(ergebnis['state'], 'running')
        self.assertTrue(Path(ergebnis['iso']).is_file())
        self.assertTrue(any('--nic1' in befehl and 'none' in befehl for befehl in self.kastenWert.befehleListe))
        self.assertFalse(any('hdd' in befehl or 'discardstate' in befehl or 'createmedium' in befehl for befehl in self.kastenWert.befehleListe))

    def laufendVirtuelleMaschineBewahrtPrüfung(self):
        self.eintragErstellen()
        self.assertEqual(self.befehlAusführen.befehlAusführen()['state'], 'running')
        self.istUnverändert()

    def gespeichertStatuswertFortführenUndProtokolldateiBewahrungPrüfung(self):
        maschine = self.eintragErstellen()
        maschine['VMState'] = 'saved'
        protokolldateiWert = self.befehlAusführen.pfad(self.befehlAusführen.lesen()['serial_log'])
        protokolldateiWert.write_text('saved log')
        self.befehlAusführen.befehlAusführen()
        self.assertFalse(any(befehl[0] == 'make' or befehl[1] == 'modifyvm' for befehl in self.kastenWert.befehleListe))
        self.assertEqual([pfad.read_text() for pfad in protokolldateiWert.parent.glob('before-resume-*.log')], ['saved log'])

    def pausierenUndFortführenPrüfung(self):
        self.eintragErstellen()['VMState'] = 'paused'
        self.befehlAusführen.befehlAusführen()
        self.assertTrue(any(befehl[1] == 'controlvm' and befehl[3] == 'resume' for befehl in self.kastenWert.befehleListe))
        self.assertFalse(any(befehl[0] == 'make' for befehl in self.kastenWert.befehleListe))

    def andererVirtuelleMaschineNameKollisionPrüfung(self):
        self.kastenWert.virtuellMaschinen[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(modulWert.ausführungFehler): self.befehlAusführen.befehlAusführen()
        self.istUnverändert()

    def eigentumMarkierungZurückgewiesenPrüfung(self):
        self.eintragErstellen()['owner'] = 'someone-else'
        with self.assertRaises(modulWert.ausführungFehler): self.befehlAusführen.befehlAusführen()
        self.istUnverändert()

    def andererEinstellungenPfadZurückgewiesenPrüfung(self):
        self.eintragErstellen()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(modulWert.ausführungFehler): self.befehlAusführen.befehlAusführen()
        self.istUnverändert()

    def zusätzlichBenutzerPlatteBewahrtPrüfung(self):
        maschine = self.eintragErstellen()
        maschine['VMState'] = 'poweroff'
        maschine['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(modulWert.ausführungFehler): self.befehlAusführen.befehlAusführen()
        self.istUnverändert()

    def übergangZurückgewiesenPrüfung(self):
        self.eintragErstellen()['VMState'] = 'saving'
        with self.assertRaises(modulWert.ausführungFehler): self.befehlAusführen.befehlAusführen()
        self.istUnverändert()

    def abmeldenZurückgewiesenPrüfung(self):
        self.eintragErstellen()
        self.kastenWert.virtuellMaschinen.clear()
        with self.assertRaises(modulWert.ausführungFehler): self.befehlAusführen.befehlAusführen()
        self.istUnverändert()

    def virtuelleMaschineBewahrtEingeschaltetErzeugenAbbildFehlschlagPrüfung(self):
        maschine = self.eintragErstellen()
        maschine['VMState'] = 'poweroff'
        vorherigElementeintrag = dict(maschine)
        self.kastenWert.fehlschlagWert = 'make'
        with self.assertRaises(modulWert.ausführungFehler): self.befehlAusführen.befehlAusführen()
        self.assertEqual(maschine, vorherigElementeintrag)

    def unterbrochenEigentumMarkierungWiederherstellungPrüfung(self):
        self.kastenWert.fehlschlagWert = 'setextradata'
        with self.assertRaises(modulWert.ausführungFehler): self.befehlAusführen.befehlAusführen()
        self.kastenWert.befehleListe.clear()
        self.assertEqual(self.befehlAusführen.befehlAusführen()['state'], 'running')
        self.assertFalse(any(befehl[1] == 'createvm' for befehl in self.kastenWert.befehleListe))

    def bewahrtISOVerfälschungZurückgewiesenPrüfung(self):
        maschine = self.eintragErstellen()
        maschine['VMState'] = 'poweroff'
        Path(maschine['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(modulWert.ausführungFehler): self.befehlAusführen.befehlAusführen()

    def keinStatuswertErstelltPrüfung(self):
        self.assertEqual(self.befehlAusführen.statuswertAnzeigen()['state'], 'not-created')
        self.assertFalse(self.kastenWert.befehleListe)

    def pfadMaskierenZurückgewiesenPrüfung(self):
        for pfad in ('../outside', '/tmp/outside'):
            with self.assertRaises(modulWert.ausführungFehler): self.befehlAusführen.pfad(pfad)
        (self.wurzelWert / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(modulWert.ausführungFehler): self.befehlAusführen.pfad('media/kernel.iso')

    def virtualBox52ZusammengesetztObjektEigenschaftenPrüfung(self):
        ergebnis = modulWert.attributWert('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(ergebnis['VMState'], 'running')
        self.assertEqual(ergebnis['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
