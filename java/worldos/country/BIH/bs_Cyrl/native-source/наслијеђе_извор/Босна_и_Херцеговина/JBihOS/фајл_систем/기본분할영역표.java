// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Босна_и_Херцеговина.JBihOS.фајл_систем;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 задана_вриједност 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class партиција_вриједност {
        private final int 종류;
        private final long почети_секција;
        private final long 구역수;

        партиција_вриједност(int 종류, long почети_секција, long 구역수) {
            this.종류 = 종류;
            this.почети_секција = почети_секција;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long почети_секција() { return почети_секција; }
        public long 구역수() { return 구역수; }
    }

    public List<партиција_вриједност> 읽기(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<партиција_вриједност> 결과 = new ArrayList<партиција_вриједност>();
        for (int индекс = 0; индекс < 4; индекс++) {
            int 위치 = 446 + индекс * 16;
            int 종류 = 첫구역[위치 + 4] & 0xff;
            long 시작 = 작은순서정수(첫구역, 위치 + 8);
            long подесити_величину = 작은순서정수(첫구역, 위치 + 12);
            if (종류 != 0 && подесити_величину != 0) {
                결과.add(new партиција_вриједност(종류, 시작, подесити_величину));
            }
        }
        return Collections.unmodifiableList(결과);
    }

    private long 작은순서정수(byte[] подаци, int 위치) {
        return (подаци[위치] & 0xffL)
                | ((подаци[위치 + 1] & 0xffL) << 8)
                | ((подаци[위치 + 2] & 0xffL) << 16)
                | ((подаци[위치 + 3] & 0xffL) << 24);
    }
}

