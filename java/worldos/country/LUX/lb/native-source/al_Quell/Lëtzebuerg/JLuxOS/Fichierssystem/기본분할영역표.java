// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lëtzebuerg.JLuxOS.Fichierssystem;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 Standardwäert 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class Partitioun_VALUE {
        private final int 종류;
        private final long Start_Beräich;
        private final long Beräich_COUNT;

        Partitioun_VALUE(int 종류, long Start_Beräich, long Beräich_COUNT) {
            this.종류 = 종류;
            this.Start_Beräich = Start_Beräich;
            this.Beräich_COUNT = Beräich_COUNT;
        }

        public int 종류() { return 종류; }
        public long Start_Beräich() { return Start_Beräich; }
        public long Beräich_COUNT() { return Beräich_COUNT; }
    }

    public List<Partitioun_VALUE> 읽기(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<Partitioun_VALUE> Mooss = new ArrayList<Partitioun_VALUE>();
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            int positionéieren = 446 + INDEX * 16;
            int 종류 = 첫구역[positionéieren + 4] & 0xff;
            long Laf = 작은순서정수(첫구역, positionéieren + 8);
            long d_Gréisst_veränneren = 작은순서정수(첫구역, positionéieren + 12);
            if (종류 != 0 && d_Gréisst_veränneren != 0) {
                Mooss.add(new Partitioun_VALUE(종류, Laf, d_Gréisst_veränneren));
            }
        }
        return Collections.unmodifiableList(Mooss);
    }

    private long 작은순서정수(byte[] Daten, int positionéieren) {
        return (Daten[positionéieren] & 0xffL)
                | ((Daten[positionéieren + 1] & 0xffL) << 8)
                | ((Daten[positionéieren + 2] & 0xffL) << 16)
                | ((Daten[positionéieren + 3] & 0xffL) << 24);
    }
}

