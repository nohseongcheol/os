// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ශ්_රී_ලංකාව.JLkaOS.ගොනු_පද්ධතිය;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 පෙරනිමි_අගය 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class පංගුව_අගය {
        private final int 종류;
        private final long ඇරඹුම_අංශය;
        private final long 구역수;

        පංගුව_අගය(int 종류, long ඇරඹුම_අංශය, long 구역수) {
            this.종류 = 종류;
            this.ඇරඹුම_අංශය = ඇරඹුම_අංශය;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long ඇරඹුම_අංශය() { return ඇරඹුම_අංශය; }
        public long 구역수() { return 구역수; }
    }

    public List<පංගුව_අගය> කියවීම(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<පංගුව_අගය> 결과 = new ArrayList<පංගුව_අගය>();
        for (int සූචිය = 0; සූචිය < 4; සූචිය++) {
            int පිහිටීම = 446 + සූචිය * 16;
            int 종류 = 첫구역[පිහිටීම + 4] & 0xff;
            long ක්_රියාත්මක_කරන්න_2 = 작은순서정수(첫구역, පිහිටීම + 8);
            long ප්_රමාණය = 작은순서정수(첫구역, පිහිටීම + 12);
            if (종류 != 0 && ප්_රමාණය != 0) {
                결과.add(new පංගුව_අගය(종류, ක්_රියාත්මක_කරන්න_2, ප්_රමාණය));
            }
        }
        return Collections.unmodifiableList(결과);
    }

    private long 작은순서정수(byte[] දත්ත, int පිහිටීම) {
        return (දත්ත[පිහිටීම] & 0xffL)
                | ((දත්ත[පිහිටීම + 1] & 0xffL) << 8)
                | ((දත්ත[පිහිටීම + 2] & 0xffL) << 16)
                | ((දත්ත[පිහිටීම + 3] & 0xffL) << 24);
    }
}

