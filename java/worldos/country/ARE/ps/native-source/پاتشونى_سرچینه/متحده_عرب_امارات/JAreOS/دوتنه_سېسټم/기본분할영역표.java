// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package متحده_عرب_امارات.JAreOS.دوتنه_سېسټم;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 تلواله_ارزښت 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class وېش_ارزښت {
        private final int 종류;
        private final long پيل_برخه;
        private final long 구역수;

        وېش_ارزښت(int 종류, long پيل_برخه, long 구역수) {
            this.종류 = 종류;
            this.پيل_برخه = پيل_برخه;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long پيل_برخه() { return پيل_برخه; }
        public long 구역수() { return 구역수; }
    }

    public List<وېش_ارزښت> لوستل(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<وېش_ارزښت> 결과 = new ArrayList<وېش_ارزښت>();
        for (int لړیال = 0; لړیال < 4; لړیال++) {
            int ځای = 446 + لړیال * 16;
            int 종류 = 첫구역[ځای + 4] & 0xff;
            long ځغلول = 작은순서정수(첫구역, ځای + 8);
            long کچ = 작은순서정수(첫구역, ځای + 12);
            if (종류 != 0 && کچ != 0) {
                결과.add(new وېش_ارزښت(종류, ځغلول, کچ));
            }
        }
        return Collections.unmodifiableList(결과);
    }

    private long 작은순서정수(byte[] اومتوک, int ځای) {
        return (اومتوک[ځای] & 0xffL)
                | ((اومتوک[ځای + 1] & 0xffL) << 8)
                | ((اومتوک[ځای + 2] & 0xffL) << 16)
                | ((اومتوک[ځای + 3] & 0xffL) << 24);
    }
}

