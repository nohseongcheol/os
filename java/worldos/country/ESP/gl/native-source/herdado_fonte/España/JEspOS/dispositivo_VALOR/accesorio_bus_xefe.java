// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package España.JEspOS.dispositivo_VALOR;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI dispositivo_VALOR 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class accesorio_bus_xefe {
    public static final class dispositivo_VALOR {
        private final int 판매자식별자;
        private final int 장치식별자;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public dispositivo_VALOR(int 판매자식별자, int 장치식별자, int 입출력바탕, int 개입중단번호) {
            this.판매자식별자 = 판매자식별자;
            this.장치식별자 = 장치식별자;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int 판매자식별자() { return 판매자식별자; }
        public int 장치식별자() { return 장치식별자; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<dispositivo_VALOR> Dispositivos_Lista = new ArrayList<dispositivo_VALOR>();

    public void 발견(dispositivo_VALOR dispositivo_VALOR) {
        Dispositivos_Lista.add(dispositivo_VALOR);
    }

    public List<dispositivo_VALOR> Dispositivos_Lista() {
        return Collections.unmodifiableList(Dispositivos_Lista);
    }

    public dispositivo_VALOR Busca_introdución(int 판매자식별자, int 장치식별자) {
        for (dispositivo_VALOR 후보 : Dispositivos_Lista) {
            if (후보.판매자식별자 == 판매자식별자 && 후보.장치식별자 == 장치식별자) {
                return 후보;
            }
        }
        return null;
    }
}

