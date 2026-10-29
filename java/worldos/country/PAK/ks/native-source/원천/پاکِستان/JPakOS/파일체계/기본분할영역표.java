// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package پاکِستان.JPakOS.파일체계;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 기본 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class 분할영역 {
        private final int 종류;
        private final long 시작구역;
        private final long 구역수;

        분할영역(int 종류, long 시작구역, long 구역수) {
            this.종류 = 종류;
            this.시작구역 = 시작구역;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long 시작구역() { return 시작구역; }
        public long 구역수() { return 구역수; }
    }

    public List<분할영역> 읽기(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<분할영역> 결과 = new ArrayList<분할영역>();
        for (int 번호 = 0; 번호 < 4; 번호++) {
            int जाय_प्य्यटठ = 446 + 번호 * 16;
            int 종류 = 첫구역[जाय_प्य्यटठ + 4] & 0xff;
            long 시작 = 작은순서정수(첫구역, जाय_प्य्यटठ + 8);
            long नाप = 작은순서정수(첫구역, जाय_प्य्यटठ + 12);
            if (종류 != 0 && नाप != 0) {
                결과.add(new 분할영역(종류, 시작, नाप));
            }
        }
        return Collections.unmodifiableList(결과);
    }

    private long 작은순서정수(byte[] 자료, int जाय_प्य्यटठ) {
        return (자료[जाय_प्य्यटठ] & 0xffL)
                | ((자료[जाय_प्य्यटठ + 1] & 0xffL) << 8)
                | ((자료[जाय_प्य्यटठ + 2] & 0xffL) << 16)
                | ((자료[जाय_प्य्यटठ + 3] & 0xffL) << 24);
    }
}

