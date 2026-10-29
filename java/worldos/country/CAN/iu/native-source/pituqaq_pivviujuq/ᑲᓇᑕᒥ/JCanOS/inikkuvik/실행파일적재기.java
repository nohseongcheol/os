// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ᑲᓇᑕᒥ.JCanOS.inikkuvik;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian 실행 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class sukuttia_atuutilik {
        private final int 종류;
        private final int ujjiqsuut_atuutilik;
        private final int turaarut;
        private final int 파일위치;
        private final int anininga;

        sukuttia_atuutilik(int 종류, int ujjiqsuut_atuutilik, int turaarut, int 파일위치, int anininga) {
            this.종류 = 종류;
            this.ujjiqsuut_atuutilik = ujjiqsuut_atuutilik;
            this.turaarut = turaarut;
            this.파일위치 = 파일위치;
            this.anininga = anininga;
        }

        public int 종류() {
            return 종류;
        }

        public int ujjiqsuut_atuutilik() {
            return ujjiqsuut_atuutilik;
        }

        public int turaarut() {
            return turaarut;
        }

        public int 파일위치() {
            return 파일위치;
        }

        public int anininga() {
            return anininga;
        }
    }

    public static final class ajjinnguaq {
        private final int pigiarli_turaarut;
        private final List<sukuttia_atuutilik> 구역들;

        ajjinnguaq(int pigiarli_turaarut, List<sukuttia_atuutilik> 구역들) {
            this.pigiarli_turaarut = pigiarli_turaarut;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int pigiarli_turaarut() {
            return pigiarli_turaarut;
        }

        public List<sukuttia_atuutilik> 구역들() {
            return 구역들;
        }
    }

    public ajjinnguaq 검사(byte[] titiqqat) {
        if (titiqqat == null || titiqqat.length < 52
                || titiqqat[0] != 0x7f || titiqqat[1] != 'E' || titiqqat[2] != 'L' || titiqqat[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (titiqqat[4] != 1 || titiqqat[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int pigiarli_turaarut = agguqtuut_naasaut(titiqqat, 24);
        int 구역표위치 = agguqtuut_naasaut(titiqqat, 32);
        int sukuttia_Iliniku_anininga = 짧은정수읽기(titiqqat, 46);
        int 구역수 = 짧은정수읽기(titiqqat, 48);
        if (sukuttia_Iliniku_anininga < 40 || 구역표위치 < 0
                || (long) 구역표위치 + (long) sukuttia_Iliniku_anininga * 구역수 > titiqqat.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<sukuttia_atuutilik> 구역들 = new ArrayList<sukuttia_atuutilik>();
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < 구역수; nalunaiqsimavik++) {
            int 위치 = 구역표위치 + nalunaiqsimavik * sukuttia_Iliniku_anininga;
            int 종류 = agguqtuut_naasaut(titiqqat, 위치 + 4);
            int ujjiqsuut_atuutilik = agguqtuut_naasaut(titiqqat, 위치 + 8);
            int turaarut = agguqtuut_naasaut(titiqqat, 위치 + 12);
            int 파일위치 = agguqtuut_naasaut(titiqqat, 위치 + 16);
            int anininga = agguqtuut_naasaut(titiqqat, 위치 + 20);
            if (anininga < 0 || (종류 != 8 && ((long) 파일위치 + anininga > titiqqat.length || 파일위치 < 0))) {
                throw new IllegalArgumentException("ELF sukuttia_atuutilik titiqqat 범위가 올바르지 않습니다.");
            }
            구역들.add(new sukuttia_atuutilik(종류, ujjiqsuut_atuutilik, turaarut, 파일위치, anininga));
        }
        return new ajjinnguaq(pigiarli_turaarut, 구역들);
    }

    private int agguqtuut_naasaut(byte[] titiqqat, int 위치) {
        if (위치 < 0 || 위치 > titiqqat.length - 4) {
            throw new IllegalArgumentException("ELF naasaut 범위를 벗어났습니다.");
        }
        return (titiqqat[위치] & 0xff)
                | ((titiqqat[위치 + 1] & 0xff) << 8)
                | ((titiqqat[위치 + 2] & 0xff) << 16)
                | ((titiqqat[위치 + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] titiqqat, int 위치) {
        if (위치 < 0 || 위치 > titiqqat.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 naasaut 범위를 벗어났습니다.");
        }
        return (titiqqat[위치] & 0xff) | ((titiqqat[위치 + 1] & 0xff) << 8);
    }
}
