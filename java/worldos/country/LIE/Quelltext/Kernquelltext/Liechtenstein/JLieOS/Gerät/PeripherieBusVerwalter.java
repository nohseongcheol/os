// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Liechtenstein.JLieOS.Gerät;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** Verwaltet Ergebnisse der PCI-Gerätesuche sowie BAR/IRQ-Werte. */
public final class PeripherieBusVerwalter {
    public static final class Gerät {
        private final int lieferantBezeichner;
        private final int gerätBezeichner;
        private final int einAusgabeBasis;
        private final int unterbrechenNummer;

        public Gerät(int lieferantBezeichner, int gerätBezeichner, int einAusgabeBasis, int unterbrechenNummer) {
            this.lieferantBezeichner = lieferantBezeichner;
            this.gerätBezeichner = gerätBezeichner;
            this.einAusgabeBasis = einAusgabeBasis;
            this.unterbrechenNummer = unterbrechenNummer;
        }

        public int lieferantBezeichner() { return lieferantBezeichner; }
        public int gerätBezeichner() { return gerätBezeichner; }
        public int einAusgabeBasis() { return einAusgabeBasis; }
        public int unterbrechenNummer() { return unterbrechenNummer; }
    }

    private final List<Gerät> geräteListe = new ArrayList<Gerät>();

    public void entdecktWert(Gerät Gerät) {
        geräteListe.add(Gerät);
    }

    public List<Gerät> geräteListe() {
        return Collections.unmodifiableList(geräteListe);
    }

    public Gerät eintragFinden(int lieferantBezeichner, int gerätBezeichner) {
        for (Gerät kandidat : geräteListe) {
            if (kandidat.lieferantBezeichner == lieferantBezeichner && kandidat.gerätBezeichner == gerätBezeichner) {
                return kandidat;
            }
        }
        return null;
    }
}

