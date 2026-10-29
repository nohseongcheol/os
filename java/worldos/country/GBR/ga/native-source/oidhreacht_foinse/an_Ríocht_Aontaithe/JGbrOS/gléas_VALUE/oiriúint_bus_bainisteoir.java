// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package an_Ríocht_Aontaithe.JGbrOS.gléas_VALUE;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI gléas_VALUE 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class oiriúint_bus_bainisteoir {
    public static final class gléas_VALUE {
        private final int 판매자식별자;
        private final int gléas_aitheantóir;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public gléas_VALUE(int 판매자식별자, int gléas_aitheantóir, int 입출력바탕, int 개입중단번호) {
            this.판매자식별자 = 판매자식별자;
            this.gléas_aitheantóir = gléas_aitheantóir;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int 판매자식별자() { return 판매자식별자; }
        public int gléas_aitheantóir() { return gléas_aitheantóir; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<gléas_VALUE> Gléasanna_Liosta = new ArrayList<gléas_VALUE>();

    public void 발견(gléas_VALUE gléas_VALUE) {
        Gléasanna_Liosta.add(gléas_VALUE);
    }

    public List<gléas_VALUE> Gléasanna_Liosta() {
        return Collections.unmodifiableList(Gléasanna_Liosta);
    }

    public gléas_VALUE FIND_iontráil(int 판매자식별자, int gléas_aitheantóir) {
        for (gléas_VALUE 후보 : Gléasanna_Liosta) {
            if (후보.판매자식별자 == 판매자식별자 && 후보.gléas_aitheantóir == gléas_aitheantóir) {
                return 후보;
            }
        }
        return null;
    }
}

