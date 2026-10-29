// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Francia.JFraOS.cellulare_VALORE;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI cellulare_VALORE 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class accessorio_bus_manager {
    public static final class cellulare_VALORE {
        private final int fornitore_identificatore;
        private final int cellulare_identificatore;
        private final int 입출력바탕;
        private final int IRQ_numero;

        public cellulare_VALORE(int fornitore_identificatore, int cellulare_identificatore, int 입출력바탕, int IRQ_numero) {
            this.fornitore_identificatore = fornitore_identificatore;
            this.cellulare_identificatore = cellulare_identificatore;
            this.입출력바탕 = 입출력바탕;
            this.IRQ_numero = IRQ_numero;
        }

        public int fornitore_identificatore() { return fornitore_identificatore; }
        public int cellulare_identificatore() { return cellulare_identificatore; }
        public int 입출력바탕() { return 입출력바탕; }
        public int IRQ_numero() { return IRQ_numero; }
    }

    private final List<cellulare_VALORE> Dispositivi_elenco = new ArrayList<cellulare_VALORE>();

    public void 발견(cellulare_VALORE cellulare_VALORE) {
        Dispositivi_elenco.add(cellulare_VALORE);
    }

    public List<cellulare_VALORE> Dispositivi_elenco() {
        return Collections.unmodifiableList(Dispositivi_elenco);
    }

    public cellulare_VALORE TROVA_voce(int fornitore_identificatore, int cellulare_identificatore) {
        for (cellulare_VALORE candidato : Dispositivi_elenco) {
            if (candidato.fornitore_identificatore == fornitore_identificatore && candidato.cellulare_identificatore == cellulare_identificatore) {
                return candidato;
            }
        }
        return null;
    }
}

