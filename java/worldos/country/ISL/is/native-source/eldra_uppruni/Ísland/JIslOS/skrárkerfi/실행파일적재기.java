// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ísland.JIslOS.skrárkerfi;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian keyra_skipun 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class hluti_VALUE {
        private final int 종류;
        private final int flagg_VALUE;
        private final int slóð;
        private final int skrá_staða_2aa21a9a;
        private final int Stærð;

        hluti_VALUE(int 종류, int flagg_VALUE, int slóð, int skrá_staða_2aa21a9a, int Stærð) {
            this.종류 = 종류;
            this.flagg_VALUE = flagg_VALUE;
            this.slóð = slóð;
            this.skrá_staða_2aa21a9a = skrá_staða_2aa21a9a;
            this.Stærð = Stærð;
        }

        public int 종류() {
            return 종류;
        }

        public int flagg_VALUE() {
            return flagg_VALUE;
        }

        public int slóð() {
            return slóð;
        }

        public int skrá_staða_2aa21a9a() {
            return skrá_staða_2aa21a9a;
        }

        public int Stærð() {
            return Stærð;
        }
    }

    public static final class mynd {
        private final int Opna_slóð;
        private final List<hluti_VALUE> 구역들;

        mynd(int Opna_slóð, List<hluti_VALUE> 구역들) {
            this.Opna_slóð = Opna_slóð;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int Opna_slóð() {
            return Opna_slóð;
        }

        public List<hluti_VALUE> 구역들() {
            return 구역들;
        }
    }

    public mynd 검사(byte[] gögn) {
        if (gögn == null || gögn.length < 52
                || gögn[0] != 0x7f || gögn[1] != 'E' || gögn[2] != 'L' || gögn[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (gögn[4] != 1 || gögn[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int Opna_slóð = þátta_heiltala(gögn, 24);
        int hluti_tafla_staða = þátta_heiltala(gögn, 32);
        int hluti_færsla_breyta_stærð = 짧은정수읽기(gögn, 46);
        int hluti_COUNT = 짧은정수읽기(gögn, 48);
        if (hluti_færsla_breyta_stærð < 40 || hluti_tafla_staða < 0
                || (long) hluti_tafla_staða + (long) hluti_færsla_breyta_stærð * hluti_COUNT > gögn.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<hluti_VALUE> 구역들 = new ArrayList<hluti_VALUE>();
        for (int INDEX = 0; INDEX < hluti_COUNT; INDEX++) {
            int Staðsetning = hluti_tafla_staða + INDEX * hluti_færsla_breyta_stærð;
            int 종류 = þátta_heiltala(gögn, Staðsetning + 4);
            int flagg_VALUE = þátta_heiltala(gögn, Staðsetning + 8);
            int slóð = þátta_heiltala(gögn, Staðsetning + 12);
            int skrá_staða_2aa21a9a = þátta_heiltala(gögn, Staðsetning + 16);
            int Stærð = þátta_heiltala(gögn, Staðsetning + 20);
            if (Stærð < 0 || (종류 != 8 && ((long) skrá_staða_2aa21a9a + Stærð > gögn.length || skrá_staða_2aa21a9a < 0))) {
                throw new IllegalArgumentException("ELF hluti_VALUE gögn 범위가 올바르지 않습니다.");
            }
            구역들.add(new hluti_VALUE(종류, flagg_VALUE, slóð, skrá_staða_2aa21a9a, Stærð));
        }
        return new mynd(Opna_slóð, 구역들);
    }

    private int þátta_heiltala(byte[] gögn, int Staðsetning) {
        if (Staðsetning < 0 || Staðsetning > gögn.length - 4) {
            throw new IllegalArgumentException("ELF heiltala 범위를 벗어났습니다.");
        }
        return (gögn[Staðsetning] & 0xff)
                | ((gögn[Staðsetning + 1] & 0xff) << 8)
                | ((gögn[Staðsetning + 2] & 0xff) << 16)
                | ((gögn[Staðsetning + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] gögn, int Staðsetning) {
        if (Staðsetning < 0 || Staðsetning > gögn.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 heiltala 범위를 벗어났습니다.");
        }
        return (gögn[Staðsetning] & 0xff) | ((gögn[Staðsetning + 1] & 0xff) << 8);
    }
}
