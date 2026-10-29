// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package عێراق.JIrqOS.سیستمی_فایل;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 بەهای_گریمانە 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class پارچەبەند_نرخ {
        private final int 종류;
        private final long دەستپێك_بەش;
        private final long 구역수;

        پارچەبەند_نرخ(int 종류, long دەستپێك_بەش, long 구역수) {
            this.종류 = 종류;
            this.دەستپێك_بەش = دەستپێك_بەش;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long دەستپێك_بەش() { return دەستپێك_بەش; }
        public long 구역수() { return 구역수; }
    }

    public List<پارچەبەند_نرخ> 읽기(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<پارچەبەند_نرخ> 결과 = new ArrayList<پارچەبەند_نرخ>();
        for (int پێرست = 0; پێرست < 4; پێرست++) {
            int 위치 = 446 + پێرست * 16;
            int 종류 = 첫구역[위치 + 4] & 0xff;
            long ڕادان = 작은순서정수(첫구역, 위치 + 8);
            long گۆڕینی_ئەندازە = 작은순서정수(첫구역, 위치 + 12);
            if (종류 != 0 && گۆڕینی_ئەندازە != 0) {
                결과.add(new پارچەبەند_نرخ(종류, ڕادان, گۆڕینی_ئەندازە));
            }
        }
        return Collections.unmodifiableList(결과);
    }

    private long 작은순서정수(byte[] دەیتا, int 위치) {
        return (دەیتا[위치] & 0xffL)
                | ((دەیتا[위치 + 1] & 0xffL) << 8)
                | ((دەیتا[위치 + 2] & 0xffL) << 16)
                | ((دەیتا[위치 + 3] & 0xffL) << 24);
    }
}

