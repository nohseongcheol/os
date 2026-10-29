// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Curaçao.JCuwOS.mobiel_WAARDE;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI mobiel_WAARDE 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class accessoire_bus_Manager {
    public static final class mobiel_WAARDE {
        private final int leverancier_id;
        private final int mobiel_id;
        private final int 입출력바탕;
        private final int IRQ_nummer;

        public mobiel_WAARDE(int leverancier_id, int mobiel_id, int 입출력바탕, int IRQ_nummer) {
            this.leverancier_id = leverancier_id;
            this.mobiel_id = mobiel_id;
            this.입출력바탕 = 입출력바탕;
            this.IRQ_nummer = IRQ_nummer;
        }

        public int leverancier_id() { return leverancier_id; }
        public int mobiel_id() { return mobiel_id; }
        public int 입출력바탕() { return 입출력바탕; }
        public int IRQ_nummer() { return IRQ_nummer; }
    }

    private final List<mobiel_WAARDE> Apparaten_Lijst = new ArrayList<mobiel_WAARDE>();

    public void 발견(mobiel_WAARDE mobiel_WAARDE) {
        Apparaten_Lijst.add(mobiel_WAARDE);
    }

    public List<mobiel_WAARDE> Apparaten_Lijst() {
        return Collections.unmodifiableList(Apparaten_Lijst);
    }

    public mobiel_WAARDE Zoeken_invoer(int leverancier_id, int mobiel_id) {
        for (mobiel_WAARDE sollicitant : Apparaten_Lijst) {
            if (sollicitant.leverancier_id == leverancier_id && sollicitant.mobiel_id == mobiel_id) {
                return sollicitant;
            }
        }
        return null;
    }
}

