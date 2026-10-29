// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Msumbiji.JMozOS.mfumo_ya_mafaili;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 hali_ya_chaguo_msingi 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class kitenga_thamani {
        private final int 종류;
        private final long Anza_sehemu;
        private final long 구역수;

        kitenga_thamani(int 종류, long Anza_sehemu, long 구역수) {
            this.종류 = 종류;
            this.Anza_sehemu = Anza_sehemu;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long Anza_sehemu() { return Anza_sehemu; }
        public long 구역수() { return 구역수; }
    }

    public List<kitenga_thamani> 읽기(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<kitenga_thamani> 결과 = new ArrayList<kitenga_thamani>();
        for (int kielezo = 0; kielezo < 4; kielezo++) {
            int 위치 = 446 + kielezo * 16;
            int 종류 = 첫구역[위치 + 4] & 0xff;
            long endesha = 작은순서정수(첫구역, 위치 + 8);
            long panga_ukubwa = 작은순서정수(첫구역, 위치 + 12);
            if (종류 != 0 && panga_ukubwa != 0) {
                결과.add(new kitenga_thamani(종류, endesha, panga_ukubwa));
            }
        }
        return Collections.unmodifiableList(결과);
    }

    private long 작은순서정수(byte[] data, int 위치) {
        return (data[위치] & 0xffL)
                | ((data[위치 + 1] & 0xffL) << 8)
                | ((data[위치 + 2] & 0xffL) << 16)
                | ((data[위치 + 3] & 0xffL) << 24);
    }
}

