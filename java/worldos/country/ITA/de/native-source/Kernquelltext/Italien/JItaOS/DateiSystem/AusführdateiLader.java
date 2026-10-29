// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italien.JItaOS.DateiSystem;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** Prüft Kopf und Ladesegmente von ELF32-Programmen mit Little-Endian-Bytereihenfolge. */
public final class AusführdateiLader {
    public static final class abschnittWert {
        private final int artWert;
        private final int merkmalbitWert;
        private final int adresse;
        private final int dateiPosition;
        private final int größe;

        abschnittWert(int artWert, int merkmalbitWert, int adresse, int dateiPosition, int größe) {
            this.artWert = artWert;
            this.merkmalbitWert = merkmalbitWert;
            this.adresse = adresse;
            this.dateiPosition = dateiPosition;
            this.größe = größe;
        }

        public int artWert() {
            return artWert;
        }

        public int merkmalbitWert() {
            return merkmalbitWert;
        }

        public int adresse() {
            return adresse;
        }

        public int dateiPosition() {
            return dateiPosition;
        }

        public int größe() {
            return größe;
        }
    }

    public static final class abbild {
        private final int adresseStarten;
        private final List<abschnittWert> abschnitteListe;

        abbild(int adresseStarten, List<abschnittWert> abschnitteListe) {
            this.adresseStarten = adresseStarten;
            this.abschnitteListe = Collections.unmodifiableList(abschnitteListe);
        }

        public int adresseStarten() {
            return adresseStarten;
        }

        public List<abschnittWert> abschnitteListe() {
            return abschnitteListe;
        }
    }

    public abbild Prüfpunkte(byte[] Daten) {
        if (Daten == null || Daten.length < 52
                || Daten[0] != 0x7f || Daten[1] != 'E' || Daten[2] != 'L' || Daten[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (Daten[4] != 1 || Daten[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int adresseStarten = ganzzahlAnalysieren(Daten, 24);
        int abschnittTabellePosition = ganzzahlAnalysieren(Daten, 32);
        int abschnittEintragGröße = kurzGanzzahlLesen(Daten, 46);
        int abschnittAnzahl = kurzGanzzahlLesen(Daten, 48);
        if (abschnittEintragGröße < 40 || abschnittTabellePosition < 0
                || (long) abschnittTabellePosition + (long) abschnittEintragGröße * abschnittAnzahl > Daten.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<abschnittWert> abschnitteListe = new ArrayList<abschnittWert>();
        for (int Nummer = 0; Nummer < abschnittAnzahl; Nummer++) {
            int position = abschnittTabellePosition + Nummer * abschnittEintragGröße;
            int artWert = ganzzahlAnalysieren(Daten, position + 4);
            int merkmalbitWert = ganzzahlAnalysieren(Daten, position + 8);
            int adresse = ganzzahlAnalysieren(Daten, position + 12);
            int dateiPosition = ganzzahlAnalysieren(Daten, position + 16);
            int größe = ganzzahlAnalysieren(Daten, position + 20);
            if (größe < 0 || (artWert != 8 && ((long) dateiPosition + größe > Daten.length || dateiPosition < 0))) {
                throw new IllegalArgumentException("ELF abschnittWert Daten 범위가 올바르지 않습니다.");
            }
            abschnitteListe.add(new abschnittWert(artWert, merkmalbitWert, adresse, dateiPosition, größe));
        }
        return new abbild(adresseStarten, abschnitteListe);
    }

    private int ganzzahlAnalysieren(byte[] Daten, int position) {
        if (position < 0 || position > Daten.length - 4) {
            throw new IllegalArgumentException("ELF Ganzzahl 범위를 벗어났습니다.");
        }
        return (Daten[position] & 0xff)
                | ((Daten[position + 1] & 0xff) << 8)
                | ((Daten[position + 2] & 0xff) << 16)
                | ((Daten[position + 3] & 0xff) << 24);
    }

    private int kurzGanzzahlLesen(byte[] Daten, int position) {
        if (position < 0 || position > Daten.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 Ganzzahl 범위를 벗어났습니다.");
        }
        return (Daten[position] & 0xff) | ((Daten[position + 1] & 0xff) << 8);
    }
}
