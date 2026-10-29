// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nijar.JNerOS.tsarin_fayil_a_kwamfuta;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 Tanadaddiyar_daraja 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class Shamakin_faifai_Daraja {
        private final int 종류;
        private final long Fara_Sashi;
        private final long 구역수;

        Shamakin_faifai_Daraja(int 종류, long Fara_Sashi, long 구역수) {
            this.종류 = 종류;
            this.Fara_Sashi = Fara_Sashi;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long Fara_Sashi() { return Fara_Sashi; }
        public long 구역수() { return 구역수; }
    }

    public List<Shamakin_faifai_Daraja> Yi_Karatu(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<Shamakin_faifai_Daraja> 결과 = new ArrayList<Shamakin_faifai_Daraja>();
        for (int Indes = 0; Indes < 4; Indes++) {
            int 위치 = 446 + Indes * 16;
            int 종류 = 첫구역[위치 + 4] & 0xff;
            long Tafiyar_da = 작은순서정수(첫구역, 위치 + 8);
            long Girma = 작은순서정수(첫구역, 위치 + 12);
            if (종류 != 0 && Girma != 0) {
                결과.add(new Shamakin_faifai_Daraja(종류, Tafiyar_da, Girma));
            }
        }
        return Collections.unmodifiableList(결과);
    }

    private long 작은순서정수(byte[] Tarin_bayani, int 위치) {
        return (Tarin_bayani[위치] & 0xffL)
                | ((Tarin_bayani[위치 + 1] & 0xffL) << 8)
                | ((Tarin_bayani[위치 + 2] & 0xffL) << 16)
                | ((Tarin_bayani[위치 + 3] & 0xffL) << 24);
    }
}

