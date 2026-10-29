// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ኤርትራ.JEriOS.ናይ_ፋይል_ስርዓት;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 ንቡር_ዋጋ 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class ጉዚ_ዋጋ {
        private final int 종류;
        private final long ጀምር_ክፋል;
        private final long 구역수;

        ጉዚ_ዋጋ(int 종류, long ጀምር_ክፋል, long 구역수) {
            this.종류 = 종류;
            this.ጀምር_ክፋል = ጀምር_ክፋል;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long ጀምር_ክፋል() { return ጀምር_ክፋል; }
        public long 구역수() { return 구역수; }
    }

    public List<ጉዚ_ዋጋ> 읽기(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<ጉዚ_ዋጋ> 결과 = new ArrayList<ጉዚ_ዋጋ>();
        for (int መሐበሪ = 0; መሐበሪ < 4; መሐበሪ++) {
            int 위치 = 446 + መሐበሪ * 16;
            int 종류 = 첫구역[위치 + 4] & 0xff;
            long ኣኺድ = 작은순서정수(첫구역, 위치 + 8);
            long መጠን = 작은순서정수(첫구역, 위치 + 12);
            if (종류 != 0 && መጠን != 0) {
                결과.add(new ጉዚ_ዋጋ(종류, ኣኺድ, መጠን));
            }
        }
        return Collections.unmodifiableList(결과);
    }

    private long 작은순서정수(byte[] ሓበሬታ, int 위치) {
        return (ሓበሬታ[위치] & 0xffL)
                | ((ሓበሬታ[위치 + 1] & 0xffL) << 8)
                | ((ሓበሬታ[위치 + 2] & 0xffL) << 16)
                | ((ሓበሬታ[위치 + 3] & 0xffL) << 24);
    }
}

