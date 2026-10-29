// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Senegaal.JSenOS.barabu_boolebdenc_yu_ñu_bennal;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 xayma_bi_teew 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class Pàccale_xëyma {
        private final int 종류;
        private final long Door_dog;
        private final long 구역수;

        Pàccale_xëyma(int 종류, long Door_dog, long 구역수) {
            this.종류 = 종류;
            this.Door_dog = Door_dog;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long Door_dog() { return Door_dog; }
        public long 구역수() { return 구역수; }
    }

    public List<Pàccale_xëyma> 읽기(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<Pàccale_xëyma> 결과 = new ArrayList<Pàccale_xëyma>();
        for (int àlluwa_tur = 0; àlluwa_tur < 4; àlluwa_tur++) {
            int 위치 = 446 + àlluwa_tur * 16;
            int 종류 = 첫구역[위치 + 4] & 0xff;
            long daw = 작은순서정수(첫구역, 위치 + 8);
            long tolluwaay = 작은순서정수(첫구역, 위치 + 12);
            if (종류 != 0 && tolluwaay != 0) {
                결과.add(new Pàccale_xëyma(종류, daw, tolluwaay));
            }
        }
        return Collections.unmodifiableList(결과);
    }

    private long 작은순서정수(byte[] mbir, int 위치) {
        return (mbir[위치] & 0xffL)
                | ((mbir[위치 + 1] & 0xffL) << 8)
                | ((mbir[위치 + 2] & 0xffL) << 16)
                | ((mbir[위치 + 3] & 0xffL) << 24);
    }
}

