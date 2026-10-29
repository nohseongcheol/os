// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italien.JItaOS.Speicherraum;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** Stellt 4-KiB-Seitenabbildung und Kopieren beim Schreiben bereit. */
public final class SeiteVerwalter {
    public static final int seiteGröße = 4096;

    private static final class seiteWert {
        private byte[] Daten = new byte[seiteGröße];
        private int verweisAnzahl = 1;
        private boolean kannSchreiben = true;
        private boolean eingeschaltetSchreibenKopieren;
    }

    public static final class AdresseRaum {
        private final Map<Integer, seiteWert> seiteTabelle = new HashMap<Integer, seiteWert>();
    }

    public AdresseRaum neuAdresseRaum() {
        return new AdresseRaum();
    }

    public void abbildungSeite(AdresseRaum adresseGebiet, int virtuellAdresse, boolean kannSchreiben) {
        int Nummer = seiteNummer(virtuellAdresse);
        seiteWert neuSeite = new seiteWert();
        neuSeite.kannSchreiben = kannSchreiben;
        adresseGebiet.seiteTabelle.put(Integer.valueOf(Nummer), neuSeite);
    }

    public AdresseRaum klonenKopierenEingeschaltetSchreiben(AdresseRaum ursprünglich) {
        AdresseRaum geklontWert = new AdresseRaum();
        for (Map.Entry<Integer, seiteWert> eintragWert : ursprünglich.seiteTabelle.entrySet()) {
            seiteWert geteiltSeite = eintragWert.getValue();
            geteiltSeite.verweisAnzahl++;
            if (geteiltSeite.kannSchreiben) {
                geteiltSeite.kannSchreiben = false;
                geteiltSeite.eingeschaltetSchreibenKopieren = true;
            }
            geklontWert.seiteTabelle.put(eintragWert.getKey(), geteiltSeite);
        }
        return geklontWert;
    }

    public byte byteWertLesen(AdresseRaum adresseGebiet, int virtuellAdresse) {
        seiteWert zielobjektWert = seiteFinden(adresseGebiet, virtuellAdresse);
        return zielobjektWert.Daten[Math.floorMod(virtuellAdresse, seiteGröße)];
    }

    public void byteWertSchreiben(AdresseRaum adresseGebiet, int virtuellAdresse, byte Wert) {
        int Nummer = seiteNummer(virtuellAdresse);
        seiteWert zielobjektWert = seiteFinden(adresseGebiet, virtuellAdresse);
        if (!zielobjektWert.kannSchreiben) {
            if (!zielobjektWert.eingeschaltetSchreibenKopieren) {
                throw new IllegalStateException("lesen 전용 쪽입니다.");
            }
            zielobjektWert = privatSeiteErstellen(adresseGebiet, Nummer, zielobjektWert);
        }
        zielobjektWert.Daten[Math.floorMod(virtuellAdresse, seiteGröße)] = Wert;
    }

    public void privatBereichSchreiben(AdresseRaum adresseGebiet, int adresseStarten, int größe) {
        if (größe < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int endeAdresse = Math.addExact(adresseStarten, größe);
        for (int adresse = adresseStarten; adresse < endeAdresse; adresse = (seiteNummer(adresse) + 1) * seiteGröße) {
            int Nummer = seiteNummer(adresse);
            seiteWert zielobjektWert = seiteFinden(adresseGebiet, adresse);
            if (zielobjektWert.eingeschaltetSchreibenKopieren) {
                privatSeiteErstellen(adresseGebiet, Nummer, zielobjektWert);
            } else {
                zielobjektWert.kannSchreiben = true;
            }
        }
    }

    public void bereichSchreiben(AdresseRaum adresseGebiet, int adresseStarten, byte[] Daten) {
        for (int Nummer = 0; Nummer < Daten.length; Nummer++) {
            byteWertSchreiben(adresseGebiet, adresseStarten + Nummer, Daten[Nummer]);
        }
    }

    private seiteWert privatSeiteErstellen(AdresseRaum adresseGebiet, int Nummer, seiteWert geteiltSeite) {
        seiteWert privatSeite = new seiteWert();
        privatSeite.Daten = Arrays.copyOf(geteiltSeite.Daten, geteiltSeite.Daten.length);
        privatSeite.kannSchreiben = true;
        privatSeite.eingeschaltetSchreibenKopieren = false;
        geteiltSeite.verweisAnzahl--;
        adresseGebiet.seiteTabelle.put(Integer.valueOf(Nummer), privatSeite);
        return privatSeite;
    }

    private seiteWert seiteFinden(AdresseRaum adresseGebiet, int adresse) {
        seiteWert zielobjektWert = adresseGebiet.seiteTabelle.get(Integer.valueOf(seiteNummer(adresse)));
        if (zielobjektWert == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return zielobjektWert;
    }

    private int seiteNummer(int adresse) {
        if (adresse < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return adresse / seiteGröße;
    }
}

