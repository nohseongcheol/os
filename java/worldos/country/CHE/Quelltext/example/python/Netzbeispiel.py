from Deutsch import Ausgabe, datagrammÖffnen, externDatagrammSenden, datagrammEmpfangen, netzwerkSchließen, millisekunden
from Deutsch import SystemFehler, VersuchenErneutFehler, textKodieren, befehlArgumente, Ganzzahl
endpunkt = datagrammÖffnen(0)
try:
    datagramm = textKodieren("PYTHON UDP Deutsch")
    externDatagrammSenden(endpunkt, "10.0.2.2", Ganzzahl(befehlArgumente[1]), datagramm)
    ausführenVorgang = millisekunden()
    while True:
        try:
            antwort, portWert = datagrammEmpfangen(endpunkt)
            break
        except SystemFehler as fehler:
            if fehler.Nummer != VersuchenErneutFehler or millisekunden() - ausführenVorgang >= 700:
                raise
    assert antwort == datagramm
    Ausgabe("PYTHON 네트워크 überprüfen: UDP Deutsch")
finally:
    netzwerkSchließen(endpunkt)
