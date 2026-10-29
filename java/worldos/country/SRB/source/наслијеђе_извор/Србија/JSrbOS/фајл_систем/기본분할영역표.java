// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Србија.JSrbOS.фајл_систем;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 задана_вриједност 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class партиција_вриједност {
        private final int 종류;
        private final long Старт_одељак;
        private final long 구역수;

        партиција_вриједност(int 종류, long Старт_одељак, long 구역수) {
            this.종류 = 종류;
            this.Старт_одељак = Старт_одељак;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long Старт_одељак() { return Старт_одељак; }
        public long 구역수() { return 구역수; }
    }

    public List<партиција_вриједност> Чита(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<партиција_вриједност> ИСХОД = new ArrayList<партиција_вриједност>();
        for (int индекс = 0; индекс < 4; индекс++) {
            int Положај = 446 + индекс * 16;
            int 종류 = 첫구역[Положај + 4] & 0xff;
            long Покрени = 작은순서정수(첫구역, Положај + 8);
            long Величина = 작은순서정수(첫구역, Положај + 12);
            if (종류 != 0 && Величина != 0) {
                ИСХОД.add(new партиција_вриједност(종류, Покрени, Величина));
            }
        }
        return Collections.unmodifiableList(ИСХОД);
    }

    private long 작은순서정수(byte[] подаци, int Положај) {
        return (подаци[Положај] & 0xffL)
                | ((подаци[Положај + 1] & 0xffL) << 8)
                | ((подаци[Положај + 2] & 0xffL) << 16)
                | ((подаци[Положај + 3] & 0xffL) << 24);
    }
}

