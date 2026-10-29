// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ኢትዮጵያ.JEthOS.የፋይል_ስርዓት;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 ነባሪ_እሴት 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class ክፍልፍል_እሴት {
        private final int 종류;
        private final long ጀምር_ክፍል;
        private final long 구역수;

        ክፍልፍል_እሴት(int 종류, long ጀምር_ክፍል, long 구역수) {
            this.종류 = 종류;
            this.ጀምር_ክፍል = ጀምር_ክፍል;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long ጀምር_ክፍል() { return ጀምር_ክፍል; }
        public long 구역수() { return 구역수; }
    }

    public List<ክፍልፍል_እሴት> ማንበቢያ(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<ክፍልፍል_እሴት> ልኬት = new ArrayList<ክፍልፍል_እሴት>();
        for (int መረጃ_ጠቆመ = 0; መረጃ_ጠቆመ < 4; መረጃ_ጠቆመ++) {
            int አካባቢ = 446 + መረጃ_ጠቆመ * 16;
            int 종류 = 첫구역[አካባቢ + 4] & 0xff;
            long ማስኬጃ = 작은순서정수(첫구역, አካባቢ + 8);
            long መጠን = 작은순서정수(첫구역, አካባቢ + 12);
            if (종류 != 0 && መጠን != 0) {
                ልኬት.add(new ክፍልፍል_እሴት(종류, ማስኬጃ, መጠን));
            }
        }
        return Collections.unmodifiableList(ልኬት);
    }

    private long 작은순서정수(byte[] ውሂብ, int አካባቢ) {
        return (ውሂብ[አካባቢ] & 0xffL)
                | ((ውሂብ[አካባቢ + 1] & 0xffL) << 8)
                | ((ውሂብ[አካባቢ + 2] & 0xffL) << 16)
                | ((ውሂብ[አካባቢ + 3] & 0xffL) << 24);
    }
}

