// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Թուրքիա.JTurOS.նիշքային_համակարգ;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 սկզբնադիր_արժեք 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class մասնաբաժին_արժեք {
        private final int 종류;
        private final long Մեկնարկ_խումբ;
        private final long 구역수;

        մասնաբաժին_արժեք(int 종류, long Մեկնարկ_խումբ, long 구역수) {
            this.종류 = 종류;
            this.Մեկնարկ_խումբ = Մեկնարկ_խումբ;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long Մեկնարկ_խումբ() { return Մեկնարկ_խումբ; }
        public long 구역수() { return 구역수; }
    }

    public List<մասնաբաժին_արժեք> Ընթերցում(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<մասնաբաժին_արժեք> չափ = new ArrayList<մասնաբաժին_արժեք>();
        for (int դասիչ = 0; դասիչ < 4; դասիչ++) {
            int Դիրք = 446 + դասիչ * 16;
            int 종류 = 첫구역[Դիրք + 4] & 0xff;
            long Գործարկել = 작은순서정수(첫구역, Դիրք + 8);
            long Չափս = 작은순서정수(첫구역, Դիրք + 12);
            if (종류 != 0 && Չափս != 0) {
                չափ.add(new մասնաբաժին_արժեք(종류, Գործարկել, Չափս));
            }
        }
        return Collections.unmodifiableList(չափ);
    }

    private long 작은순서정수(byte[] տվյալ, int Դիրք) {
        return (տվյալ[Դիրք] & 0xffL)
                | ((տվյալ[Դիրք + 1] & 0xffL) << 8)
                | ((տվյալ[Դիրք + 2] & 0xffL) << 16)
                | ((տվյալ[Դիրք + 3] & 0xffL) << 24);
    }
}

