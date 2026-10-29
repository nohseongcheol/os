// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package NAM.JNamOS.setsamaisadifaele;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 boleng_jo_bo_rulaganyeditsweng_ruri 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class karoganyo_Boleng {
        private final int 종류;
        private final long simolola_karolo;
        private final long 구역수;

        karoganyo_Boleng(int 종류, long simolola_karolo, long 구역수) {
            this.종류 = 종류;
            this.simolola_karolo = simolola_karolo;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long simolola_karolo() { return simolola_karolo; }
        public long 구역수() { return 구역수; }
    }

    public List<karoganyo_Boleng> 읽기(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<karoganyo_Boleng> 결과 = new ArrayList<karoganyo_Boleng>();
        for (int tshupane = 0; tshupane < 4; tshupane++) {
            int 위치 = 446 + tshupane * 16;
            int 종류 = 첫구역[위치 + 4] & 0xff;
            long dirisa = 작은순서정수(첫구역, 위치 + 8);
            long lekanya = 작은순서정수(첫구역, 위치 + 12);
            if (종류 != 0 && lekanya != 0) {
                결과.add(new karoganyo_Boleng(종류, dirisa, lekanya));
            }
        }
        return Collections.unmodifiableList(결과);
    }

    private long 작은순서정수(byte[] tshedimosetso, int 위치) {
        return (tshedimosetso[위치] & 0xffL)
                | ((tshedimosetso[위치 + 1] & 0xffL) << 8)
                | ((tshedimosetso[위치 + 2] & 0xffL) << 16)
                | ((tshedimosetso[위치 + 3] & 0xffL) << 24);
    }
}

