// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Noreg.JNorOS.filsystem;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian Utfør_kommando 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class del_VALUE {
        private final int 종류;
        private final int flagg_VALUE;
        private final int ADDRESS;
        private final int fil_plassere;
        private final int Storleik;

        del_VALUE(int 종류, int flagg_VALUE, int ADDRESS, int fil_plassere, int Storleik) {
            this.종류 = 종류;
            this.flagg_VALUE = flagg_VALUE;
            this.ADDRESS = ADDRESS;
            this.fil_plassere = fil_plassere;
            this.Storleik = Storleik;
        }

        public int 종류() {
            return 종류;
        }

        public int flagg_VALUE() {
            return flagg_VALUE;
        }

        public int ADDRESS() {
            return ADDRESS;
        }

        public int fil_plassere() {
            return fil_plassere;
        }

        public int Storleik() {
            return Storleik;
        }
    }

    public static final class IMAGE {
        private final int START_ADDRESS;
        private final List<del_VALUE> 구역들;

        IMAGE(int START_ADDRESS, List<del_VALUE> 구역들) {
            this.START_ADDRESS = START_ADDRESS;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int START_ADDRESS() {
            return START_ADDRESS;
        }

        public List<del_VALUE> 구역들() {
            return 구역들;
        }
    }

    public IMAGE 검사(byte[] data) {
        if (data == null || data.length < 52
                || data[0] != 0x7f || data[1] != 'E' || data[2] != 'L' || data[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (data[4] != 1 || data[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int START_ADDRESS = dele_opp_heiltal(data, 24);
        int del_tabell_plassere = dele_opp_heiltal(data, 32);
        int del_oppføring_endre_storleik = 짧은정수읽기(data, 46);
        int del_COUNT = 짧은정수읽기(data, 48);
        if (del_oppføring_endre_storleik < 40 || del_tabell_plassere < 0
                || (long) del_tabell_plassere + (long) del_oppføring_endre_storleik * del_COUNT > data.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<del_VALUE> 구역들 = new ArrayList<del_VALUE>();
        for (int INDEX = 0; INDEX < del_COUNT; INDEX++) {
            int Posisjon = del_tabell_plassere + INDEX * del_oppføring_endre_storleik;
            int 종류 = dele_opp_heiltal(data, Posisjon + 4);
            int flagg_VALUE = dele_opp_heiltal(data, Posisjon + 8);
            int ADDRESS = dele_opp_heiltal(data, Posisjon + 12);
            int fil_plassere = dele_opp_heiltal(data, Posisjon + 16);
            int Storleik = dele_opp_heiltal(data, Posisjon + 20);
            if (Storleik < 0 || (종류 != 8 && ((long) fil_plassere + Storleik > data.length || fil_plassere < 0))) {
                throw new IllegalArgumentException("ELF del_VALUE data 범위가 올바르지 않습니다.");
            }
            구역들.add(new del_VALUE(종류, flagg_VALUE, ADDRESS, fil_plassere, Storleik));
        }
        return new IMAGE(START_ADDRESS, 구역들);
    }

    private int dele_opp_heiltal(byte[] data, int Posisjon) {
        if (Posisjon < 0 || Posisjon > data.length - 4) {
            throw new IllegalArgumentException("ELF heiltal 범위를 벗어났습니다.");
        }
        return (data[Posisjon] & 0xff)
                | ((data[Posisjon + 1] & 0xff) << 8)
                | ((data[Posisjon + 2] & 0xff) << 16)
                | ((data[Posisjon + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] data, int Posisjon) {
        if (Posisjon < 0 || Posisjon > data.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 heiltal 범위를 벗어났습니다.");
        }
        return (data[Posisjon] & 0xff) | ((data[Posisjon + 1] & 0xff) << 8);
    }
}
