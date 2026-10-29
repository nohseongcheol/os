// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ᑲᓇᑕᒥ.JCanOS.inikkuvik;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 Aturniliuvagiiqtut 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class ilaakuungajuq_atuutilik {
        private final int 종류;
        private final long pigiarli_sukuttia;
        private final long 구역수;

        ilaakuungajuq_atuutilik(int 종류, long pigiarli_sukuttia, long 구역수) {
            this.종류 = 종류;
            this.pigiarli_sukuttia = pigiarli_sukuttia;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long pigiarli_sukuttia() { return pigiarli_sukuttia; }
        public long 구역수() { return 구역수; }
    }

    public List<ilaakuungajuq_atuutilik> 읽기(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<ilaakuungajuq_atuutilik> 결과 = new ArrayList<ilaakuungajuq_atuutilik>();
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < 4; nalunaiqsimavik++) {
            int 위치 = 446 + nalunaiqsimavik * 16;
            int 종류 = 첫구역[위치 + 4] & 0xff;
            long 시작 = 작은순서정수(첫구역, 위치 + 8);
            long anininga = 작은순서정수(첫구역, 위치 + 12);
            if (종류 != 0 && anininga != 0) {
                결과.add(new ilaakuungajuq_atuutilik(종류, 시작, anininga));
            }
        }
        return Collections.unmodifiableList(결과);
    }

    private long 작은순서정수(byte[] titiqqat, int 위치) {
        return (titiqqat[위치] & 0xffL)
                | ((titiqqat[위치 + 1] & 0xffL) << 8)
                | ((titiqqat[위치 + 2] & 0xffL) << 16)
                | ((titiqqat[위치 + 3] & 0xffL) << 24);
    }
}

