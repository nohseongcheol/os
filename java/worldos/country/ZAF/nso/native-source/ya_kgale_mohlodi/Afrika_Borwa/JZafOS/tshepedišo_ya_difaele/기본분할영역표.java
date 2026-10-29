// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Afrika_Borwa.JZafOS.tshepedišo_ya_difaele;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 setsenywa_sa_tirelwa 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class karolo_ya_tisiki_boleng {
        private final int 종류;
        private final long Thomišo_karolo;
        private final long 구역수;

        karolo_ya_tisiki_boleng(int 종류, long Thomišo_karolo, long 구역수) {
            this.종류 = 종류;
            this.Thomišo_karolo = Thomišo_karolo;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long Thomišo_karolo() { return Thomišo_karolo; }
        public long 구역수() { return 구역수; }
    }

    public List<karolo_ya_tisiki_boleng> Bala(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<karolo_ya_tisiki_boleng> 결과 = new ArrayList<karolo_ya_tisiki_boleng>();
        for (int lokela = 0; lokela < 4; lokela++) {
            int 위치 = 446 + lokela * 16;
            int 종류 = 첫구역[위치 + 4] & 0xff;
            long Diriša = 작은순서정수(첫구역, 위치 + 8);
            long Bogolo = 작은순서정수(첫구역, 위치 + 12);
            if (종류 != 0 && Bogolo != 0) {
                결과.add(new karolo_ya_tisiki_boleng(종류, Diriša, Bogolo));
            }
        }
        return Collections.unmodifiableList(결과);
    }

    private long 작은순서정수(byte[] data, int 위치) {
        return (data[위치] & 0xffL)
                | ((data[위치 + 1] & 0xffL) << 8)
                | ((data[위치 + 2] & 0xffL) << 16)
                | ((data[위치 + 3] & 0xffL) << 24);
    }
}

