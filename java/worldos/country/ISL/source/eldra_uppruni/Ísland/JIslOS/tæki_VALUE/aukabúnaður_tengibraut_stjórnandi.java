// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ísland.JIslOS.tæki_VALUE;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI tæki_VALUE 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class aukabúnaður_tengibraut_stjórnandi {
    public static final class tæki_VALUE {
        private final int söluaðili_auðkenni;
        private final int tæki_auðkenni;
        private final int 입출력바탕;
        private final int IRQ_númer;

        public tæki_VALUE(int söluaðili_auðkenni, int tæki_auðkenni, int 입출력바탕, int IRQ_númer) {
            this.söluaðili_auðkenni = söluaðili_auðkenni;
            this.tæki_auðkenni = tæki_auðkenni;
            this.입출력바탕 = 입출력바탕;
            this.IRQ_númer = IRQ_númer;
        }

        public int söluaðili_auðkenni() { return söluaðili_auðkenni; }
        public int tæki_auðkenni() { return tæki_auðkenni; }
        public int 입출력바탕() { return 입출력바탕; }
        public int IRQ_númer() { return IRQ_númer; }
    }

    private final List<tæki_VALUE> Tæki_Listi = new ArrayList<tæki_VALUE>();

    public void 발견(tæki_VALUE tæki_VALUE) {
        Tæki_Listi.add(tæki_VALUE);
    }

    public List<tæki_VALUE> Tæki_Listi() {
        return Collections.unmodifiableList(Tæki_Listi);
    }

    public tæki_VALUE FIND_færsla(int söluaðili_auðkenni, int tæki_auðkenni) {
        for (tæki_VALUE 후보 : Tæki_Listi) {
            if (후보.söluaðili_auðkenni == söluaðili_auðkenni && 후보.tæki_auðkenni == tæki_auðkenni) {
                return 후보;
            }
        }
        return null;
    }
}

