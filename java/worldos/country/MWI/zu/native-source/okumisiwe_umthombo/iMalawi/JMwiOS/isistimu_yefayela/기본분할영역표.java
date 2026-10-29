// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package iMalawi.JMwiOS.isistimu_yefayela;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 inani_elimisiwe 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class ukwahlukanisa_inani {
        private final int 종류;
        private final long qala_isigaba;
        private final long 구역수;

        ukwahlukanisa_inani(int 종류, long qala_isigaba, long 구역수) {
            this.종류 = 종류;
            this.qala_isigaba = qala_isigaba;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long qala_isigaba() { return qala_isigaba; }
        public long 구역수() { return 구역수; }
    }

    public List<ukwahlukanisa_inani> Funda(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<ukwahlukanisa_inani> 결과 = new ArrayList<ukwahlukanisa_inani>();
        for (int thola_inkomba = 0; thola_inkomba < 4; thola_inkomba++) {
            int 위치 = 446 + thola_inkomba * 16;
            int 종류 = 첫구역[위치 + 4] & 0xff;
            long Sebenzisa = 작은순서정수(첫구역, 위치 + 8);
            long Ubungako = 작은순서정수(첫구역, 위치 + 12);
            if (종류 != 0 && Ubungako != 0) {
                결과.add(new ukwahlukanisa_inani(종류, Sebenzisa, Ubungako));
            }
        }
        return Collections.unmodifiableList(결과);
    }

    private long 작은순서정수(byte[] imininingwane, int 위치) {
        return (imininingwane[위치] & 0xffL)
                | ((imininingwane[위치 + 1] & 0xffL) << 8)
                | ((imininingwane[위치 + 2] & 0xffL) << 16)
                | ((imininingwane[위치 + 3] & 0xffL) << 24);
    }
}

