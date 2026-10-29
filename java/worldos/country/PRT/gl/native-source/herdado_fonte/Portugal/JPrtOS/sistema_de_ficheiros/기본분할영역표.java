// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Portugal.JPrtOS.sistema_de_ficheiros;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 valor_predefinido 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class partición_VALOR {
        private final int 종류;
        private final long START_sección;
        private final long sección_CONTAR;

        partición_VALOR(int 종류, long START_sección, long sección_CONTAR) {
            this.종류 = 종류;
            this.START_sección = START_sección;
            this.sección_CONTAR = sección_CONTAR;
        }

        public int 종류() { return 종류; }
        public long START_sección() { return START_sección; }
        public long sección_CONTAR() { return sección_CONTAR; }
    }

    public List<partición_VALOR> Lectura(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<partición_VALOR> RESULTANTE = new ArrayList<partición_VALOR>();
        for (int ÍNDICE = 0; ÍNDICE < 4; ÍNDICE++) {
            int Posición = 446 + ÍNDICE * 16;
            int 종류 = 첫구역[Posición + 4] & 0xff;
            long Executar_2 = 작은순서정수(첫구역, Posición + 8);
            long Tamaño = 작은순서정수(첫구역, Posición + 12);
            if (종류 != 0 && Tamaño != 0) {
                RESULTANTE.add(new partición_VALOR(종류, Executar_2, Tamaño));
            }
        }
        return Collections.unmodifiableList(RESULTANTE);
    }

    private long 작은순서정수(byte[] datos, int Posición) {
        return (datos[Posición] & 0xffL)
                | ((datos[Posición + 1] & 0xffL) << 8)
                | ((datos[Posición + 2] & 0xffL) << 16)
                | ((datos[Posición + 3] & 0xffL) << 24);
    }
}

