import jkoros
import Paquet
import sys

listeExistant = jkoros.read("/lib/.pip.json")
nombreÉlémentsÉlémentListe = 0
try:
    while True:
        jkoros.write("/가득%d" % nombreÉlémentsÉlémentListe, b"saved")
        nombreÉlémentsÉlémentListe += 1
except OSError as erreur:
    assert erreur.args[0] == 28
assert nombreÉlémentsÉlémentListe >= 2
for numéro in range(nombreÉlémentsÉlémentListe - 2, nombreÉlémentsÉlémentListe):
    jkoros.remove("/가득%d" % numéro)
try:
    Paquet.installerValeur("jkoros-space==1.0", int(sys.argv[1]))
except OSError as erreur:
    assert erreur.args[0] == 28
else:
    raise AssertionError("régionAdresse 부족 시 성공하면 안 됩니다.")
assert jkoros.read("/lib/.pip.json") == listeExistant
for numéro in range(4):
    assert jkoros.path_kind("/lib/space%d.py" % numéro) == 0
for numéro in range(nombreÉlémentsÉlémentListe - 2):
    assert jkoros.read("/가득%d" % numéro) == b"saved"
    jkoros.remove("/가득%d" % numéro)
print("Paquet régionAdresse 부족 pontRetourner vérifier")
