// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Frankreich.JFraOS.DateiSystem;

import java.util.HashMap;
import java.util.Map;

/** Bewahrt pro Prozess eigene Deskriptoren und gemeinsam nutzbare Beschreibungen geöffneter Dateien auf. */
public final class dateiDeskriptorTabelle {
    private static final int höchstwertDeskriptor = 32;

    private static final class deskriptorEintrag {
        private final DateiSystem.geöffnetDatei geöffnetDatei;
        private boolean eingeschaltetAusführungsvorgangSchließen;

        deskriptorEintrag(DateiSystem.geöffnetDatei geöffnetDatei) {
            this.geöffnetDatei = geöffnetDatei;
        }
    }

    private final DateiSystem DateiSystem;
    private final Map<Integer, deskriptorEintrag> deskriptorEinträge = new HashMap<Integer, deskriptorEintrag>();

    public dateiDeskriptorTabelle(DateiSystem DateiSystem) {
        this.DateiSystem = DateiSystem;
    }

    public int öffnen(String Name) {
        DateiSystem.geöffnetDatei geöffnetDatei = DateiSystem.öffnen(Name);
        if (geöffnetDatei == null) {
            return -2;
        }
        int Nummer = leerwertIndex(3);
        if (Nummer < 0) {
            return -24;
        }
        deskriptorEinträge.put(Integer.valueOf(Nummer), new deskriptorEintrag(geöffnetDatei));
        return Nummer;
    }

    public int lesen(int Nummer, byte[] zielEmpfangen, int größe) {
        deskriptorEintrag eintragWert = deskriptorEinträge.get(Integer.valueOf(Nummer));
        if (eintragWert == null) {
            return -9;
        }
        if (größe < 0 || größe > zielEmpfangen.length) {
            return -22;
        }
        int restwertDaten = eintragWert.geöffnetDatei.Daten.length - eintragWert.geöffnetDatei.position;
        int größeLesen = Math.min(größe, Math.max(restwertDaten, 0));
        System.arraycopy(eintragWert.geöffnetDatei.Daten, eintragWert.geöffnetDatei.position, zielEmpfangen, 0, größeLesen);
        eintragWert.geöffnetDatei.position += größeLesen;
        return größeLesen;
    }

    public int bewegenPosition(int Nummer, int entfernungWert, int projektWurzel) {
        deskriptorEintrag eintragWert = deskriptorEinträge.get(Integer.valueOf(Nummer));
        if (eintragWert == null) {
            return -9;
        }
        int hintergrundWert;
        if (projektWurzel == 0) {
            hintergrundWert = 0;
        } else if (projektWurzel == 1) {
            hintergrundWert = eintragWert.geöffnetDatei.position;
        } else if (projektWurzel == 2) {
            hintergrundWert = eintragWert.geöffnetDatei.Daten.length;
        } else {
            return -22;
        }
        int neuPosition = hintergrundWert + entfernungWert;
        if (neuPosition < 0) {
            return -22;
        }
        eintragWert.geöffnetDatei.position = neuPosition;
        return neuPosition;
    }

    public int schließen(int Nummer) {
        deskriptorEintrag eintragWert = deskriptorEinträge.remove(Integer.valueOf(Nummer));
        if (eintragWert == null) {
            return -9;
        }
        eintragWert.geöffnetDatei.verweisAnzahl--;
        return 0;
    }

    public int geklontDeskriptor(int Nummer, int mindestwertNummer) {
        deskriptorEintrag eintragWert = deskriptorEinträge.get(Integer.valueOf(Nummer));
        if (eintragWert == null) {
            return -9;
        }
        int neuNummer = leerwertIndex(mindestwertNummer);
        if (neuNummer < 0) {
            return -24;
        }
        eintragWert.geöffnetDatei.verweisAnzahl++;
        deskriptorEinträge.put(Integer.valueOf(neuNummer), new deskriptorEintrag(eintragWert.geöffnetDatei));
        return neuNummer;
    }

    public int duplikatAnStelle(int Nummer, int neuNummer) {
        if (Nummer == neuNummer) {
            return deskriptorEinträge.containsKey(Integer.valueOf(Nummer)) ? Nummer : -9;
        }
        if (neuNummer < 0 || neuNummer >= höchstwertDeskriptor) {
            return -9;
        }
        deskriptorEintrag ursprünglich = deskriptorEinträge.get(Integer.valueOf(Nummer));
        if (ursprünglich == null) {
            return -9;
        }
        if (deskriptorEinträge.containsKey(Integer.valueOf(neuNummer))) {
            schließen(neuNummer);
        }
        ursprünglich.geöffnetDatei.verweisAnzahl++;
        deskriptorEinträge.put(Integer.valueOf(neuNummer), new deskriptorEintrag(ursprünglich.geöffnetDatei));
        return neuNummer;
    }

    public int schließenEingeschaltetAusführungsvorgangSetzen(int Nummer, boolean Wert) {
        deskriptorEintrag eintragWert = deskriptorEinträge.get(Integer.valueOf(Nummer));
        if (eintragWert == null) {
            return -9;
        }
        eintragWert.eingeschaltetAusführungsvorgangSchließen = Wert;
        return 0;
    }

    public int eingeschaltetAusführungsvorgangWertSchließen(int Nummer) {
        deskriptorEintrag eintragWert = deskriptorEinträge.get(Integer.valueOf(Nummer));
        if (eintragWert == null) {
            return -9;
        }
        return eintragWert.eingeschaltetAusführungsvorgangSchließen ? 1 : 0;
    }

    public dateiInformation systemInformation(int Nummer) {
        if (Nummer >= 0 && Nummer <= 2) {
            return new dateiInformation(0, 0020666);
        }
        deskriptorEintrag eintragWert = deskriptorEinträge.get(Integer.valueOf(Nummer));
        if (eintragWert == null) {
            return null;
        }
        return new dateiInformation(eintragWert.geöffnetDatei.Daten.length, 0100444);
    }

    public void eingeschaltetAusführungsvorgangSchließen() {
        Integer[] nummerListe = deskriptorEinträge.keySet().toArray(new Integer[0]);
        for (Integer Nummer : nummerListe) {
            deskriptorEintrag eintragWert = deskriptorEinträge.get(Nummer);
            if (eintragWert != null && eintragWert.eingeschaltetAusführungsvorgangSchließen) {
                schließen(Nummer.intValue());
            }
        }
    }

    public boolean istÖffnen(int Nummer) {
        return deskriptorEinträge.containsKey(Integer.valueOf(Nummer));
    }

    public dateiDeskriptorTabelle klonenWert() {
        dateiDeskriptorTabelle ergebnis = new dateiDeskriptorTabelle(DateiSystem);
        for (Map.Entry<Integer, deskriptorEintrag> eintragWert : deskriptorEinträge.entrySet()) {
            eintragWert.getValue().geöffnetDatei.verweisAnzahl++;
            deskriptorEintrag neuDeskriptor = new deskriptorEintrag(eintragWert.getValue().geöffnetDatei);
            neuDeskriptor.eingeschaltetAusführungsvorgangSchließen = eintragWert.getValue().eingeschaltetAusführungsvorgangSchließen;
            ergebnis.deskriptorEinträge.put(eintragWert.getKey(), neuDeskriptor);
        }
        return ergebnis;
    }

    private int leerwertIndex(int mindestwertNummer) {
        for (int Nummer = Math.max(0, mindestwertNummer); Nummer < höchstwertDeskriptor; Nummer++) {
            if (!deskriptorEinträge.containsKey(Integer.valueOf(Nummer))) {
                return Nummer;
            }
        }
        return -1;
    }
}
