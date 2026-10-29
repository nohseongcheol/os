// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package San_Marino.JSmrOS.file_system;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 valore_predefinito 분할 영역을 읽는다. */
public final class partizione_primaria_tabella {
    public static final class partizione_VALORE {
        private final int Kind_VALORE;
        private final long START_sezione;
        private final long sezione_CONTA_NUMERI;

        partizione_VALORE(int Kind_VALORE, long START_sezione, long sezione_CONTA_NUMERI) {
            this.Kind_VALORE = Kind_VALORE;
            this.START_sezione = START_sezione;
            this.sezione_CONTA_NUMERI = sezione_CONTA_NUMERI;
        }

        public int Kind_VALORE() { return Kind_VALORE; }
        public long START_sezione() { return START_sezione; }
        public long sezione_CONTA_NUMERI() { return sezione_CONTA_NUMERI; }
    }

    public List<partizione_VALORE> Lettura(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<partizione_VALORE> risultato = new ArrayList<partizione_VALORE>();
        for (int INDICE = 0; INDICE < 4; INDICE++) {
            int posizione = 446 + INDICE * 16;
            int Kind_VALORE = 첫구역[posizione + 4] & 0xff;
            long avvia = little_endian_intero(첫구역, posizione + 8);
            long Dimensione = little_endian_intero(첫구역, posizione + 12);
            if (Kind_VALORE != 0 && Dimensione != 0) {
                risultato.add(new partizione_VALORE(Kind_VALORE, avvia, Dimensione));
            }
        }
        return Collections.unmodifiableList(risultato);
    }

    private long little_endian_intero(byte[] dati, int posizione) {
        return (dati[posizione] & 0xffL)
                | ((dati[posizione + 1] & 0xffL) << 8)
                | ((dati[posizione + 2] & 0xffL) << 16)
                | ((dati[posizione + 3] & 0xffL) << 24);
    }
}

