// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Espainia.JEspOS.fitxategi_sistema;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian exekutatu_komando 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class sekzio_balio {
        private final int 종류;
        private final int marka_balio;
        private final int helbide;
        private final int fitxategi_kargu;
        private final int Tamaina;

        sekzio_balio(int 종류, int marka_balio, int helbide, int fitxategi_kargu, int Tamaina) {
            this.종류 = 종류;
            this.marka_balio = marka_balio;
            this.helbide = helbide;
            this.fitxategi_kargu = fitxategi_kargu;
            this.Tamaina = Tamaina;
        }

        public int 종류() {
            return 종류;
        }

        public int marka_balio() {
            return marka_balio;
        }

        public int helbide() {
            return helbide;
        }

        public int fitxategi_kargu() {
            return fitxategi_kargu;
        }

        public int Tamaina() {
            return Tamaina;
        }
    }

    public static final class irudi {
        private final int HASI_helbide;
        private final List<sekzio_balio> 구역들;

        irudi(int HASI_helbide, List<sekzio_balio> 구역들) {
            this.HASI_helbide = HASI_helbide;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int HASI_helbide() {
            return HASI_helbide;
        }

        public List<sekzio_balio> 구역들() {
            return 구역들;
        }
    }

    public irudi 검사(byte[] datuak) {
        if (datuak == null || datuak.length < 52
                || datuak[0] != 0x7f || datuak[1] != 'E' || datuak[2] != 'L' || datuak[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (datuak[4] != 1 || datuak[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int HASI_helbide = analizatu_osoko_zenbaki(datuak, 24);
        int sekzio_taula_kargu = analizatu_osoko_zenbaki(datuak, 32);
        int 구역항목크기 = 짧은정수읽기(datuak, 46);
        int sekzio_ZENBATU = 짧은정수읽기(datuak, 48);
        if (구역항목크기 < 40 || sekzio_taula_kargu < 0
                || (long) sekzio_taula_kargu + (long) 구역항목크기 * sekzio_ZENBATU > datuak.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<sekzio_balio> 구역들 = new ArrayList<sekzio_balio>();
        for (int INDIZE = 0; INDIZE < sekzio_ZENBATU; INDIZE++) {
            int Posizioa = sekzio_taula_kargu + INDIZE * 구역항목크기;
            int 종류 = analizatu_osoko_zenbaki(datuak, Posizioa + 4);
            int marka_balio = analizatu_osoko_zenbaki(datuak, Posizioa + 8);
            int helbide = analizatu_osoko_zenbaki(datuak, Posizioa + 12);
            int fitxategi_kargu = analizatu_osoko_zenbaki(datuak, Posizioa + 16);
            int Tamaina = analizatu_osoko_zenbaki(datuak, Posizioa + 20);
            if (Tamaina < 0 || (종류 != 8 && ((long) fitxategi_kargu + Tamaina > datuak.length || fitxategi_kargu < 0))) {
                throw new IllegalArgumentException("ELF sekzio_balio datuak 범위가 올바르지 않습니다.");
            }
            구역들.add(new sekzio_balio(종류, marka_balio, helbide, fitxategi_kargu, Tamaina));
        }
        return new irudi(HASI_helbide, 구역들);
    }

    private int analizatu_osoko_zenbaki(byte[] datuak, int Posizioa) {
        if (Posizioa < 0 || Posizioa > datuak.length - 4) {
            throw new IllegalArgumentException("ELF osoko_zenbaki 범위를 벗어났습니다.");
        }
        return (datuak[Posizioa] & 0xff)
                | ((datuak[Posizioa + 1] & 0xff) << 8)
                | ((datuak[Posizioa + 2] & 0xff) << 16)
                | ((datuak[Posizioa + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] datuak, int Posizioa) {
        if (Posizioa < 0 || Posizioa > datuak.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 osoko_zenbaki 범위를 벗어났습니다.");
        }
        return (datuak[Posizioa] & 0xff) | ((datuak[Posizioa + 1] & 0xff) << 8);
    }
}
