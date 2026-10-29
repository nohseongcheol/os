// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nijeriya.JNgaOS.tsarin_fayil_a_kwamfuta;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian gudanar_Umarni 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class Sashi_Daraja {
        private final int 종류;
        private final int Tuta_Daraja;
        private final int imel;
        private final int 파일위치;
        private final int Girma;

        Sashi_Daraja(int 종류, int Tuta_Daraja, int imel, int 파일위치, int Girma) {
            this.종류 = 종류;
            this.Tuta_Daraja = Tuta_Daraja;
            this.imel = imel;
            this.파일위치 = 파일위치;
            this.Girma = Girma;
        }

        public int 종류() {
            return 종류;
        }

        public int Tuta_Daraja() {
            return Tuta_Daraja;
        }

        public int imel() {
            return imel;
        }

        public int 파일위치() {
            return 파일위치;
        }

        public int Girma() {
            return Girma;
        }
    }

    public static final class Hoto {
        private final int Fara_imel;
        private final List<Sashi_Daraja> 구역들;

        Hoto(int Fara_imel, List<Sashi_Daraja> 구역들) {
            this.Fara_imel = Fara_imel;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int Fara_imel() {
            return Fara_imel;
        }

        public List<Sashi_Daraja> 구역들() {
            return 구역들;
        }
    }

    public Hoto 검사(byte[] Tarin_bayani) {
        if (Tarin_bayani == null || Tarin_bayani.length < 52
                || Tarin_bayani[0] != 0x7f || Tarin_bayani[1] != 'E' || Tarin_bayani[2] != 'L' || Tarin_bayani[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (Tarin_bayani[4] != 1 || Tarin_bayani[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int Fara_imel = Daddatse_Lamba_mara(Tarin_bayani, 24);
        int 구역표위치 = Daddatse_Lamba_mara(Tarin_bayani, 32);
        int Sashi_Mashigar_bayanai_girma = 짧은정수읽기(Tarin_bayani, 46);
        int 구역수 = 짧은정수읽기(Tarin_bayani, 48);
        if (Sashi_Mashigar_bayanai_girma < 40 || 구역표위치 < 0
                || (long) 구역표위치 + (long) Sashi_Mashigar_bayanai_girma * 구역수 > Tarin_bayani.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<Sashi_Daraja> 구역들 = new ArrayList<Sashi_Daraja>();
        for (int Indes = 0; Indes < 구역수; Indes++) {
            int 위치 = 구역표위치 + Indes * Sashi_Mashigar_bayanai_girma;
            int 종류 = Daddatse_Lamba_mara(Tarin_bayani, 위치 + 4);
            int Tuta_Daraja = Daddatse_Lamba_mara(Tarin_bayani, 위치 + 8);
            int imel = Daddatse_Lamba_mara(Tarin_bayani, 위치 + 12);
            int 파일위치 = Daddatse_Lamba_mara(Tarin_bayani, 위치 + 16);
            int Girma = Daddatse_Lamba_mara(Tarin_bayani, 위치 + 20);
            if (Girma < 0 || (종류 != 8 && ((long) 파일위치 + Girma > Tarin_bayani.length || 파일위치 < 0))) {
                throw new IllegalArgumentException("ELF Sashi_Daraja Tarin_bayani 범위가 올바르지 않습니다.");
            }
            구역들.add(new Sashi_Daraja(종류, Tuta_Daraja, imel, 파일위치, Girma));
        }
        return new Hoto(Fara_imel, 구역들);
    }

    private int Daddatse_Lamba_mara(byte[] Tarin_bayani, int 위치) {
        if (위치 < 0 || 위치 > Tarin_bayani.length - 4) {
            throw new IllegalArgumentException("ELF Lamba_mara 범위를 벗어났습니다.");
        }
        return (Tarin_bayani[위치] & 0xff)
                | ((Tarin_bayani[위치 + 1] & 0xff) << 8)
                | ((Tarin_bayani[위치 + 2] & 0xff) << 16)
                | ((Tarin_bayani[위치 + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] Tarin_bayani, int 위치) {
        if (위치 < 0 || 위치 > Tarin_bayani.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 Lamba_mara 범위를 벗어났습니다.");
        }
        return (Tarin_bayani[위치] & 0xff) | ((Tarin_bayani[위치 + 1] & 0xff) << 8);
    }
}
