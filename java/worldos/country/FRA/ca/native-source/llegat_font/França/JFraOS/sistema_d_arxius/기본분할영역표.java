// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package França.JFraOS.sistema_d_arxius;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 valor_per_defecte 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class partició_VALOR {
        private final int 종류;
        private final long Inici_secció;
        private final long secció_COMPT;

        partició_VALOR(int 종류, long Inici_secció, long secció_COMPT) {
            this.종류 = 종류;
            this.Inici_secció = Inici_secció;
            this.secció_COMPT = secció_COMPT;
        }

        public int 종류() { return 종류; }
        public long Inici_secció() { return Inici_secció; }
        public long secció_COMPT() { return secció_COMPT; }
    }

    public List<partició_VALOR> Lectura(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<partició_VALOR> RESULTAT = new ArrayList<partició_VALOR>();
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            int Posició = 446 + INDEX * 16;
            int 종류 = 첫구역[Posició + 4] & 0xff;
            long Executa_2 = 작은순서정수(첫구역, Posició + 8);
            long Mida = 작은순서정수(첫구역, Posició + 12);
            if (종류 != 0 && Mida != 0) {
                RESULTAT.add(new partició_VALOR(종류, Executa_2, Mida));
            }
        }
        return Collections.unmodifiableList(RESULTAT);
    }

    private long 작은순서정수(byte[] dades, int Posició) {
        return (dades[Posició] & 0xffL)
                | ((dades[Posició + 1] & 0xffL) << 8)
                | ((dades[Posició + 2] & 0xffL) << 16)
                | ((dades[Posició + 3] & 0xffL) << 24);
    }
}

