// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Y_Deyrnas_Unedig.JGbrOS.system_ffeiliau;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 gwerth_diofyn 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class rhaniad_VALUE {
        private final int 종류;
        private final long START_adran;
        private final long adran_COUNT;

        rhaniad_VALUE(int 종류, long START_adran, long adran_COUNT) {
            this.종류 = 종류;
            this.START_adran = START_adran;
            this.adran_COUNT = adran_COUNT;
        }

        public int 종류() { return 종류; }
        public long START_adran() { return START_adran; }
        public long adran_COUNT() { return adran_COUNT; }
    }

    public List<rhaniad_VALUE> Darllen(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<rhaniad_VALUE> mesur = new ArrayList<rhaniad_VALUE>();
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            int safle = 446 + INDEX * 16;
            int 종류 = 첫구역[safle + 4] & 0xff;
            long Gweithredu_2 = 작은순서정수(첫구역, safle + 8);
            long Maint = 작은순서정수(첫구역, safle + 12);
            if (종류 != 0 && Maint != 0) {
                mesur.add(new rhaniad_VALUE(종류, Gweithredu_2, Maint));
            }
        }
        return Collections.unmodifiableList(mesur);
    }

    private long 작은순서정수(byte[] data, int safle) {
        return (data[safle] & 0xffL)
                | ((data[safle + 1] & 0xffL) << 8)
                | ((data[safle + 2] & 0xffL) << 16)
                | ((data[safle + 3] & 0xffL) << 24);
    }
}

