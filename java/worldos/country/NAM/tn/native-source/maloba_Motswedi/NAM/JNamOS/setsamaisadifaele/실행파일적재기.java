// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package NAM.JNamOS.setsamaisadifaele;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian diragatsa_Taelo 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class karolo_Boleng {
        private final int 종류;
        private final int folaga_Boleng;
        private final int aterese;
        private final int 파일위치;
        private final int lekanya;

        karolo_Boleng(int 종류, int folaga_Boleng, int aterese, int 파일위치, int lekanya) {
            this.종류 = 종류;
            this.folaga_Boleng = folaga_Boleng;
            this.aterese = aterese;
            this.파일위치 = 파일위치;
            this.lekanya = lekanya;
        }

        public int 종류() {
            return 종류;
        }

        public int folaga_Boleng() {
            return folaga_Boleng;
        }

        public int aterese() {
            return aterese;
        }

        public int 파일위치() {
            return 파일위치;
        }

        public int lekanya() {
            return lekanya;
        }
    }

    public static final class Setshwantsho {
        private final int simolola_aterese;
        private final List<karolo_Boleng> 구역들;

        Setshwantsho(int simolola_aterese, List<karolo_Boleng> 구역들) {
            this.simolola_aterese = simolola_aterese;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int simolola_aterese() {
            return simolola_aterese;
        }

        public List<karolo_Boleng> 구역들() {
            return 구역들;
        }
    }

    public Setshwantsho 검사(byte[] tshedimosetso) {
        if (tshedimosetso == null || tshedimosetso.length < 52
                || tshedimosetso[0] != 0x7f || tshedimosetso[1] != 'E' || tshedimosetso[2] != 'L' || tshedimosetso[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (tshedimosetso[4] != 1 || tshedimosetso[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int simolola_aterese = go_lokolola_Palotlalo(tshedimosetso, 24);
        int 구역표위치 = go_lokolola_Palotlalo(tshedimosetso, 32);
        int karolo_tsenyo_lekanya = 짧은정수읽기(tshedimosetso, 46);
        int 구역수 = 짧은정수읽기(tshedimosetso, 48);
        if (karolo_tsenyo_lekanya < 40 || 구역표위치 < 0
                || (long) 구역표위치 + (long) karolo_tsenyo_lekanya * 구역수 > tshedimosetso.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<karolo_Boleng> 구역들 = new ArrayList<karolo_Boleng>();
        for (int tshupane = 0; tshupane < 구역수; tshupane++) {
            int 위치 = 구역표위치 + tshupane * karolo_tsenyo_lekanya;
            int 종류 = go_lokolola_Palotlalo(tshedimosetso, 위치 + 4);
            int folaga_Boleng = go_lokolola_Palotlalo(tshedimosetso, 위치 + 8);
            int aterese = go_lokolola_Palotlalo(tshedimosetso, 위치 + 12);
            int 파일위치 = go_lokolola_Palotlalo(tshedimosetso, 위치 + 16);
            int lekanya = go_lokolola_Palotlalo(tshedimosetso, 위치 + 20);
            if (lekanya < 0 || (종류 != 8 && ((long) 파일위치 + lekanya > tshedimosetso.length || 파일위치 < 0))) {
                throw new IllegalArgumentException("ELF karolo_Boleng tshedimosetso 범위가 올바르지 않습니다.");
            }
            구역들.add(new karolo_Boleng(종류, folaga_Boleng, aterese, 파일위치, lekanya));
        }
        return new Setshwantsho(simolola_aterese, 구역들);
    }

    private int go_lokolola_Palotlalo(byte[] tshedimosetso, int 위치) {
        if (위치 < 0 || 위치 > tshedimosetso.length - 4) {
            throw new IllegalArgumentException("ELF Palotlalo 범위를 벗어났습니다.");
        }
        return (tshedimosetso[위치] & 0xff)
                | ((tshedimosetso[위치 + 1] & 0xff) << 8)
                | ((tshedimosetso[위치 + 2] & 0xff) << 16)
                | ((tshedimosetso[위치 + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] tshedimosetso, int 위치) {
        if (위치 < 0 || 위치 > tshedimosetso.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 Palotlalo 범위를 벗어났습니다.");
        }
        return (tshedimosetso[위치] & 0xff) | ((tshedimosetso[위치 + 1] & 0xff) << 8);
    }
}
