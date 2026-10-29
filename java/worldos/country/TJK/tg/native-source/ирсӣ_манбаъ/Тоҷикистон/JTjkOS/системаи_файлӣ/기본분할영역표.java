// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Тоҷикистон.JTjkOS.системаи_файлӣ;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 қимати_пешфарз 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class қисмбандӣ_қимат {
        private final int 종류;
        private final long Оғоз_қисмат;
        private final long 구역수;

        қисмбандӣ_қимат(int 종류, long Оғоз_қисмат, long 구역수) {
            this.종류 = 종류;
            this.Оғоз_қисмат = Оғоз_қисмат;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long Оғоз_қисмат() { return Оғоз_қисмат; }
        public long 구역수() { return 구역수; }
    }

    public List<қисмбандӣ_қимат> Хондан(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<қисмбандӣ_қимат> 결과 = new ArrayList<қисмбандӣ_қимат>();
        for (int индекс = 0; индекс < 4; индекс++) {
            int 위치 = 446 + индекс * 16;
            int 종류 = 첫구역[위치 + 4] & 0xff;
            long порча = 작은순서정수(첫구역, 위치 + 8);
            long андоза_кардан = 작은순서정수(첫구역, 위치 + 12);
            if (종류 != 0 && андоза_кардан != 0) {
                결과.add(new қисмбандӣ_қимат(종류, порча, андоза_кардан));
            }
        }
        return Collections.unmodifiableList(결과);
    }

    private long 작은순서정수(byte[] иттилоот, int 위치) {
        return (иттилоот[위치] & 0xffL)
                | ((иттилоот[위치 + 1] & 0xffL) << 8)
                | ((иттилоот[위치 + 2] & 0xffL) << 16)
                | ((иттилоот[위치 + 3] & 0xffL) << 24);
    }
}

