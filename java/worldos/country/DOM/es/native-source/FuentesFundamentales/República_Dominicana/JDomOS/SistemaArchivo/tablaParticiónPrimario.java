// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package República_Dominicana.JDomOS.SistemaArchivo;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** Lee las cuatro particiones primarias de un MBR de DOS. */
public final class tablaParticiónPrimario {
    public static final class valorPartición {
        private final int valorClaseTipo;
        private final long iniciarSección;
        private final long númeroElementosSección;

        valorPartición(int valorClaseTipo, long iniciarSección, long númeroElementosSección) {
            this.valorClaseTipo = valorClaseTipo;
            this.iniciarSección = iniciarSección;
            this.númeroElementosSección = númeroElementosSección;
        }

        public int valorClaseTipo() { return valorClaseTipo; }
        public long iniciarSección() { return iniciarSección; }
        public long númeroElementosSección() { return númeroElementosSección; }
    }

    public List<valorPartición> leer(byte[] secciónPrimero) {
        if (secciónPrimero == null || secciónPrimero.length < 512
                || (secciónPrimero[510] & 0xff) != 0x55 || (secciónPrimero[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<valorPartición> resultado = new ArrayList<valorPartición>();
        for (int número = 0; número < 4; número++) {
            int posición = 446 + número * 16;
            int valorClaseTipo = secciónPrimero[posición + 4] & 0xff;
            long ponerEnMarcha = enteroValorOrdenBytesPequeño(secciónPrimero, posición + 8);
            long tamaño = enteroValorOrdenBytesPequeño(secciónPrimero, posición + 12);
            if (valorClaseTipo != 0 && tamaño != 0) {
                resultado.add(new valorPartición(valorClaseTipo, ponerEnMarcha, tamaño));
            }
        }
        return Collections.unmodifiableList(resultado);
    }

    private long enteroValorOrdenBytesPequeño(byte[] Datos, int posición) {
        return (Datos[posición] & 0xffL)
                | ((Datos[posición + 1] & 0xffL) << 8)
                | ((Datos[posición + 2] & 0xffL) << 16)
                | ((Datos[posición + 3] & 0xffL) << 24);
    }
}

