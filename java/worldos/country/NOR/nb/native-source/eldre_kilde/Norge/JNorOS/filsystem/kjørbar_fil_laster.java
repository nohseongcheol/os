// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Norge.JNorOS.filsystem;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian Utfør_kommando 파일의 머리부와 적재 구역을 검증한다. */
public final class kjørbar_fil_laster {
    public static final class inndeling_VERDI {
        private final int 종류;
        private final int flagg_VERDI;
        private final int e_post;
        private final int Fil_plassere;
        private final int Størrelse;

        inndeling_VERDI(int 종류, int flagg_VERDI, int e_post, int Fil_plassere, int Størrelse) {
            this.종류 = 종류;
            this.flagg_VERDI = flagg_VERDI;
            this.e_post = e_post;
            this.Fil_plassere = Fil_plassere;
            this.Størrelse = Størrelse;
        }

        public int 종류() {
            return 종류;
        }

        public int flagg_VERDI() {
            return flagg_VERDI;
        }

        public int e_post() {
            return e_post;
        }

        public int Fil_plassere() {
            return Fil_plassere;
        }

        public int Størrelse() {
            return Størrelse;
        }
    }

    public static final class BILDE {
        private final int START_e_post;
        private final List<inndeling_VERDI> 구역들;

        BILDE(int START_e_post, List<inndeling_VERDI> 구역들) {
            this.START_e_post = START_e_post;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int START_e_post() {
            return START_e_post;
        }

        public List<inndeling_VERDI> 구역들() {
            return 구역들;
        }
    }

    public BILDE 검사(byte[] data) {
        if (data == null || data.length < 52
                || data[0] != 0x7f || data[1] != 'E' || data[2] != 'L' || data[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (data[4] != 1 || data[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int START_e_post = dele_opp_heltall(data, 24);
        int inndeling_tabell_plassere = dele_opp_heltall(data, 32);
        int inndeling_oppføring_skalere = 짧은정수읽기(data, 46);
        int inndeling_ANTALL = 짧은정수읽기(data, 48);
        if (inndeling_oppføring_skalere < 40 || inndeling_tabell_plassere < 0
                || (long) inndeling_tabell_plassere + (long) inndeling_oppføring_skalere * inndeling_ANTALL > data.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<inndeling_VERDI> 구역들 = new ArrayList<inndeling_VERDI>();
        for (int INDEKS = 0; INDEKS < inndeling_ANTALL; INDEKS++) {
            int Posisjon = inndeling_tabell_plassere + INDEKS * inndeling_oppføring_skalere;
            int 종류 = dele_opp_heltall(data, Posisjon + 4);
            int flagg_VERDI = dele_opp_heltall(data, Posisjon + 8);
            int e_post = dele_opp_heltall(data, Posisjon + 12);
            int Fil_plassere = dele_opp_heltall(data, Posisjon + 16);
            int Størrelse = dele_opp_heltall(data, Posisjon + 20);
            if (Størrelse < 0 || (종류 != 8 && ((long) Fil_plassere + Størrelse > data.length || Fil_plassere < 0))) {
                throw new IllegalArgumentException("ELF inndeling_VERDI data 범위가 올바르지 않습니다.");
            }
            구역들.add(new inndeling_VERDI(종류, flagg_VERDI, e_post, Fil_plassere, Størrelse));
        }
        return new BILDE(START_e_post, 구역들);
    }

    private int dele_opp_heltall(byte[] data, int Posisjon) {
        if (Posisjon < 0 || Posisjon > data.length - 4) {
            throw new IllegalArgumentException("ELF heltall 범위를 벗어났습니다.");
        }
        return (data[Posisjon] & 0xff)
                | ((data[Posisjon + 1] & 0xff) << 8)
                | ((data[Posisjon + 2] & 0xff) << 16)
                | ((data[Posisjon + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] data, int Posisjon) {
        if (Posisjon < 0 || Posisjon > data.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 heltall 범위를 벗어났습니다.");
        }
        return (data[Posisjon] & 0xff) | ((data[Posisjon + 1] & 0xff) << 8);
    }
}
