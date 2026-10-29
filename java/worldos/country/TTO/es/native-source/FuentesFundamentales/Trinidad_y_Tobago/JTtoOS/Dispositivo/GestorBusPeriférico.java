// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Trinidad_y_Tobago.JTtoOS.Dispositivo;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** Gestiona los resultados de búsqueda de dispositivos PCI y los valores BAR/IRQ. */
public final class GestorBusPeriférico {
    public static final class Dispositivo {
        private final int identificadorProveedor;
        private final int identificadorDispositivo;
        private final int baseEntradaSalida;
        private final int númeroInterrumpir;

        public Dispositivo(int identificadorProveedor, int identificadorDispositivo, int baseEntradaSalida, int númeroInterrumpir) {
            this.identificadorProveedor = identificadorProveedor;
            this.identificadorDispositivo = identificadorDispositivo;
            this.baseEntradaSalida = baseEntradaSalida;
            this.númeroInterrumpir = númeroInterrumpir;
        }

        public int identificadorProveedor() { return identificadorProveedor; }
        public int identificadorDispositivo() { return identificadorDispositivo; }
        public int baseEntradaSalida() { return baseEntradaSalida; }
        public int númeroInterrumpir() { return númeroInterrumpir; }
    }

    private final List<Dispositivo> listaDispositivos = new ArrayList<Dispositivo>();

    public void valorDescubierto(Dispositivo Dispositivo) {
        listaDispositivos.add(Dispositivo);
    }

    public List<Dispositivo> listaDispositivos() {
        return Collections.unmodifiableList(listaDispositivos);
    }

    public Dispositivo encontrarEntradaElemento(int identificadorProveedor, int identificadorDispositivo) {
        for (Dispositivo candidato : listaDispositivos) {
            if (candidato.identificadorProveedor == identificadorProveedor && candidato.identificadorDispositivo == identificadorDispositivo) {
                return candidato;
            }
        }
        return null;
    }
}

