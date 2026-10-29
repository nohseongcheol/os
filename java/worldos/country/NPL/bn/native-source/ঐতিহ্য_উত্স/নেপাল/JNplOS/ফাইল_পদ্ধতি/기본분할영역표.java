// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package নেপাল.JNplOS.ফাইল_পদ্ধতি;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 অমনোনীত_মান 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class বিভাজন_মান {
        private final int 종류;
        private final long শুরু_শাখা;
        private final long 구역수;

        বিভাজন_মান(int 종류, long শুরু_শাখা, long 구역수) {
            this.종류 = 종류;
            this.শুরু_শাখা = শুরু_শাখা;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long শুরু_শাখা() { return শুরু_শাখা; }
        public long 구역수() { return 구역수; }
    }

    public List<বিভাজন_মান> পড়া(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<বিভাজন_মান> পরিমাপ = new ArrayList<বিভাজন_মান>();
        for (int সূচি = 0; সূচি < 4; সূচি++) {
            int অবস্থান = 446 + সূচি * 16;
            int 종류 = 첫구역[অবস্থান + 4] & 0xff;
            long চালনা = 작은순서정수(첫구역, অবস্থান + 8);
            long আকার = 작은순서정수(첫구역, অবস্থান + 12);
            if (종류 != 0 && আকার != 0) {
                পরিমাপ.add(new বিভাজন_মান(종류, চালনা, আকার));
            }
        }
        return Collections.unmodifiableList(পরিমাপ);
    }

    private long 작은순서정수(byte[] ডাটা, int অবস্থান) {
        return (ডাটা[অবস্থান] & 0xffL)
                | ((ডাটা[অবস্থান + 1] & 0xffL) << 8)
                | ((ডাটা[অবস্থান + 2] & 0xffL) << 16)
                | ((ডাটা[অবস্থান + 3] & 0xffL) << 24);
    }
}

