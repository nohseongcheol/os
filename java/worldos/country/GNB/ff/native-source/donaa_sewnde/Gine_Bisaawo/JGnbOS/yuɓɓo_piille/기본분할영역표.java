// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Gine_Bisaawo.JGnbOS.yuɓɓo_piille;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 lasli_njaru 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class dorƴol_njaru {
        private final int 종류;
        private final long huɓɓude_taƴre;
        private final long 구역수;

        dorƴol_njaru(int 종류, long huɓɓude_taƴre, long 구역수) {
            this.종류 = 종류;
            this.huɓɓude_taƴre = huɓɓude_taƴre;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long huɓɓude_taƴre() { return huɓɓude_taƴre; }
        public long 구역수() { return 구역수; }
    }

    public List<dorƴol_njaru> 읽기(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<dorƴol_njaru> 결과 = new ArrayList<dorƴol_njaru>();
        for (int joopirdu = 0; joopirdu < 4; joopirdu++) {
            int 위치 = 446 + joopirdu * 16;
            int 종류 = 첫구역[위치 + 4] & 0xff;
            long huutoraade = 작은순서정수(첫구역, 위치 + 8);
            long waylude_etannde = 작은순서정수(첫구역, 위치 + 12);
            if (종류 != 0 && waylude_etannde != 0) {
                결과.add(new dorƴol_njaru(종류, huutoraade, waylude_etannde));
            }
        }
        return Collections.unmodifiableList(결과);
    }

    private long 작은순서정수(byte[] keɓe, int 위치) {
        return (keɓe[위치] & 0xffL)
                | ((keɓe[위치 + 1] & 0xffL) << 8)
                | ((keɓe[위치 + 2] & 0xffL) << 16)
                | ((keɓe[위치 + 3] & 0xffL) << 24);
    }
}

