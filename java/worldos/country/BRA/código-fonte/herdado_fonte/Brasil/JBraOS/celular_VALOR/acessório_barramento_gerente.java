// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Brasil.JBraOS.celular_VALOR;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI celular_VALOR 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class acessório_barramento_gerente {
    public static final class celular_VALOR {
        private final int fornecedor_identificador;
        private final int celular_identificador;
        private final int 입출력바탕;
        private final int IRQ_número;

        public celular_VALOR(int fornecedor_identificador, int celular_identificador, int 입출력바탕, int IRQ_número) {
            this.fornecedor_identificador = fornecedor_identificador;
            this.celular_identificador = celular_identificador;
            this.입출력바탕 = 입출력바탕;
            this.IRQ_número = IRQ_número;
        }

        public int fornecedor_identificador() { return fornecedor_identificador; }
        public int celular_identificador() { return celular_identificador; }
        public int 입출력바탕() { return 입출력바탕; }
        public int IRQ_número() { return IRQ_número; }
    }

    private final List<celular_VALOR> Dispositivos_Lista = new ArrayList<celular_VALOR>();

    public void 발견(celular_VALOR celular_VALOR) {
        Dispositivos_Lista.add(celular_VALOR);
    }

    public List<celular_VALOR> Dispositivos_Lista() {
        return Collections.unmodifiableList(Dispositivos_Lista);
    }

    public celular_VALOR PROCURAR_entrada(int fornecedor_identificador, int celular_identificador) {
        for (celular_VALOR candidato : Dispositivos_Lista) {
            if (candidato.fornecedor_identificador == fornecedor_identificador && candidato.celular_identificador == celular_identificador) {
                return candidato;
            }
        }
        return null;
    }
}

