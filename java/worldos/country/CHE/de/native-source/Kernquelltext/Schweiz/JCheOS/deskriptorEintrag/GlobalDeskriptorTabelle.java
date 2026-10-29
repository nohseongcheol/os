// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Schweiz.JCheOS.deskriptorEintrag;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** Bewahrt Einstellungen der globalen x86-Deskriptortabelle und des Aufgabenstatussegments auf. */
public final class GlobalDeskriptorTabelle {
    public static final class fragmentWert {
        private final int hintergrundWert;
        private final int grenzstelleGrenzwert;
        private final int zugriffWert;

        fragmentWert(int hintergrundWert, int grenzstelleGrenzwert, int zugriffWert) {
            this.hintergrundWert = hintergrundWert;
            this.grenzstelleGrenzwert = grenzstelleGrenzwert;
            this.zugriffWert = zugriffWert;
        }

        public int hintergrundWert() { return hintergrundWert; }
        public int grenzstelleGrenzwert() { return grenzstelleGrenzwert; }
        public int zugriffWert() { return zugriffWert; }
    }

    private final List<fragmentWert> fragmenteListe = new ArrayList<fragmentWert>();

    public int eintragAnhängen(int hintergrundWert, int grenzstelleGrenzwert, int zugriffWert) {
        fragmenteListe.add(new fragmentWert(hintergrundWert, grenzstelleGrenzwert, zugriffWert));
        return (fragmenteListe.size() - 1) * 8;
    }

    public List<fragmentWert> fragmenteListe() {
        return Collections.unmodifiableList(fragmenteListe);
    }

    public void standardwertWertSetzen() {
        fragmenteListe.clear();
        eintragAnhängen(0, 0, 0);
        eintragAnhängen(0, 0xfffff, 0x9a);
        eintragAnhängen(0, 0xfffff, 0x92);
        eintragAnhängen(0, 0xfffff, 0xfa);
        eintragAnhängen(0, 0xfffff, 0xf2);
    }
}

