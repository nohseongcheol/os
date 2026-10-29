// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Curazao.JCuwOS.entradaElementoDescriptor;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** Conserva la configuración de la tabla global de descriptores x86 y del segmento de estado de tarea. */
public final class TablaDescriptorGlobal {
    public static final class valorFragmento {
        private final int valorFondo;
        private final int límiteFrontera;
        private final int valorAcceso;

        valorFragmento(int valorFondo, int límiteFrontera, int valorAcceso) {
            this.valorFondo = valorFondo;
            this.límiteFrontera = límiteFrontera;
            this.valorAcceso = valorAcceso;
        }

        public int valorFondo() { return valorFondo; }
        public int límiteFrontera() { return límiteFrontera; }
        public int valorAcceso() { return valorAcceso; }
    }

    private final List<valorFragmento> listaFragmentos = new ArrayList<valorFragmento>();

    public int añadirFinalEntradaElemento(int valorFondo, int límiteFrontera, int valorAcceso) {
        listaFragmentos.add(new valorFragmento(valorFondo, límiteFrontera, valorAcceso));
        return (listaFragmentos.size() - 1) * 8;
    }

    public List<valorFragmento> listaFragmentos() {
        return Collections.unmodifiableList(listaFragmentos);
    }

    public void establecerValorPredeterminado() {
        listaFragmentos.clear();
        añadirFinalEntradaElemento(0, 0, 0);
        añadirFinalEntradaElemento(0, 0xfffff, 0x9a);
        añadirFinalEntradaElemento(0, 0xfffff, 0x92);
        añadirFinalEntradaElemento(0, 0xfffff, 0xfa);
        añadirFinalEntradaElemento(0, 0xfffff, 0xf2);
    }
}

