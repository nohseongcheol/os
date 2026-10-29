// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Aotearoa.JNzlOS.pūnaha_kōnae;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 uara_taunoa 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class pātaki_uara {
        private final int 종류;
        private final long Start_wāhanga;
        private final long wāhanga_COUNT;

        pātaki_uara(int 종류, long Start_wāhanga, long wāhanga_COUNT) {
            this.종류 = 종류;
            this.Start_wāhanga = Start_wāhanga;
            this.wāhanga_COUNT = wāhanga_COUNT;
        }

        public int 종류() { return 종류; }
        public long Start_wāhanga() { return Start_wāhanga; }
        public long wāhanga_COUNT() { return wāhanga_COUNT; }
    }

    public List<pātaki_uara> Pānuitia(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<pātaki_uara> mēhua = new ArrayList<pātaki_uara>();
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            int tūranga = 446 + INDEX * 16;
            int 종류 = 첫구역[tūranga + 4] & 0xff;
            long whakahaere = 작은순서정수(첫구역, tūranga + 8);
            long rahi = 작은순서정수(첫구역, tūranga + 12);
            if (종류 != 0 && rahi != 0) {
                mēhua.add(new pātaki_uara(종류, whakahaere, rahi));
            }
        }
        return Collections.unmodifiableList(mēhua);
    }

    private long 작은순서정수(byte[] raraunga, int tūranga) {
        return (raraunga[tūranga] & 0xffL)
                | ((raraunga[tūranga + 1] & 0xffL) << 8)
                | ((raraunga[tūranga + 2] & 0xffL) << 16)
                | ((raraunga[tūranga + 3] & 0xffL) << 24);
    }
}

