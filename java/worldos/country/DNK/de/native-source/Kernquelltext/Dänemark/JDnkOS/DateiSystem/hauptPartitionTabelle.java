// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Dänemark.JDnkOS.DateiSystem;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** Liest die vier primären Partitionen eines DOS-MBR. */
public final class hauptPartitionTabelle {
    public static final class partitionWert {
        private final int artWert;
        private final long abschnittStarten;
        private final long abschnittAnzahl;

        partitionWert(int artWert, long abschnittStarten, long abschnittAnzahl) {
            this.artWert = artWert;
            this.abschnittStarten = abschnittStarten;
            this.abschnittAnzahl = abschnittAnzahl;
        }

        public int artWert() { return artWert; }
        public long abschnittStarten() { return abschnittStarten; }
        public long abschnittAnzahl() { return abschnittAnzahl; }
    }

    public List<partitionWert> lesen(byte[] ersterAbschnitt) {
        if (ersterAbschnitt == null || ersterAbschnitt.length < 512
                || (ersterAbschnitt[510] & 0xff) != 0x55 || (ersterAbschnitt[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<partitionWert> ergebnis = new ArrayList<partitionWert>();
        for (int Nummer = 0; Nummer < 4; Nummer++) {
            int position = 446 + Nummer * 16;
            int artWert = ersterAbschnitt[position + 4] & 0xff;
            long ausführenVorgang = kleinByteordnungGanzzahl(ersterAbschnitt, position + 8);
            long größe = kleinByteordnungGanzzahl(ersterAbschnitt, position + 12);
            if (artWert != 0 && größe != 0) {
                ergebnis.add(new partitionWert(artWert, ausführenVorgang, größe));
            }
        }
        return Collections.unmodifiableList(ergebnis);
    }

    private long kleinByteordnungGanzzahl(byte[] Daten, int position) {
        return (Daten[position] & 0xffL)
                | ((Daten[position + 1] & 0xffL) << 8)
                | ((Daten[position + 2] & 0xffL) << 16)
                | ((Daten[position + 3] & 0xffL) << 24);
    }
}

