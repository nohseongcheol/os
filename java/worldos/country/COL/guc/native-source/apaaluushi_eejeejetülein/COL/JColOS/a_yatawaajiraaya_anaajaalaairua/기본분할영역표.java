// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package COL.JColOS.a_yatawaajiraaya_anaajaalaairua;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 ajutuu_aneekuushitüjülia 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class alüjülee_ajutuu {
        private final int 종류;
        private final long achuwalaa_alüjalee;
        private final long 구역수;

        alüjülee_ajutuu(int 종류, long achuwalaa_alüjalee, long 구역수) {
            this.종류 = 종류;
            this.achuwalaa_alüjalee = achuwalaa_alüjalee;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long achuwalaa_alüjalee() { return achuwalaa_alüjalee; }
        public long 구역수() { return 구역수; }
    }

    public List<alüjülee_ajutuu> 읽기(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<alüjülee_ajutuu> 결과 = new ArrayList<alüjülee_ajutuu>();
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < 4; ee_iyatialujuna++) {
            int 위치 = 446 + ee_iyatialujuna * 16;
            int 종류 = 첫구역[위치 + 4] & 0xff;
            long 시작 = 작은순서정수(첫구역, 위치 + 8);
            long 크기 = 작은순서정수(첫구역, 위치 + 12);
            if (종류 != 0 && 크기 != 0) {
                결과.add(new alüjülee_ajutuu(종류, 시작, 크기));
            }
        }
        return Collections.unmodifiableList(결과);
    }

    private long 작은순서정수(byte[] atijaaya, int 위치) {
        return (atijaaya[위치] & 0xffL)
                | ((atijaaya[위치 + 1] & 0xffL) << 8)
                | ((atijaaya[위치 + 2] & 0xffL) << 16)
                | ((atijaaya[위치 + 3] & 0xffL) << 24);
    }
}

