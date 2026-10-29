from Deutsch import SystemFehler, VersuchenErneutFehler, datagrammÖffnen, datagrammEmpfangen, netzwerkSchließen, dateiLesen, Ausgabe

endpunkt = datagrammÖffnen(0)
try:
    try:
        datagrammEmpfangen(endpunkt)
        raise AssertionError("비어 있는 datagramm 대기에서 예외가 필요합니다.")
    except SystemFehler as fehler:
        assert fehler.Nummer == VersuchenErneutFehler
        assert fehler.beschreibung == "Betriebssystem 작업에 실패했습니다."
        Ausgabe("Deutsch datagramm ausnahme überprüfen")
finally:
    netzwerkSchließen(endpunkt)
try:
    dateiLesen("/없는파일")
except SystemFehler as fehler:
    assert fehler.Nummer == 2
    Ausgabe("Deutsch Datei ausnahme überprüfen")
else:
    raise AssertionError("Datei fehlendMethode 예외가 필요합니다.")
