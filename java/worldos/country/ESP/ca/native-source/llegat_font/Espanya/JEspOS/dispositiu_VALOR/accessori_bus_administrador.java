// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Espanya.JEspOS.dispositiu_VALOR;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI dispositiu_VALOR 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class accessori_bus_administrador {
    public static final class dispositiu_VALOR {
        private final int proveïdor_identificador;
        private final int dispositiu_identificador;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public dispositiu_VALOR(int proveïdor_identificador, int dispositiu_identificador, int 입출력바탕, int 개입중단번호) {
            this.proveïdor_identificador = proveïdor_identificador;
            this.dispositiu_identificador = dispositiu_identificador;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int proveïdor_identificador() { return proveïdor_identificador; }
        public int dispositiu_identificador() { return dispositiu_identificador; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<dispositiu_VALOR> Dispositius_Llista = new ArrayList<dispositiu_VALOR>();

    public void 발견(dispositiu_VALOR dispositiu_VALOR) {
        Dispositius_Llista.add(dispositiu_VALOR);
    }

    public List<dispositiu_VALOR> Dispositius_Llista() {
        return Collections.unmodifiableList(Dispositius_Llista);
    }

    public dispositiu_VALOR BUSCA_introducció(int proveïdor_identificador, int dispositiu_identificador) {
        for (dispositiu_VALOR 후보 : Dispositius_Llista) {
            if (후보.proveïdor_identificador == proveïdor_identificador && 후보.dispositiu_identificador == dispositiu_identificador) {
                return 후보;
            }
        }
        return null;
    }
}

