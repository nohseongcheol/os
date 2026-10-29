// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package an_Ríocht_Aontaithe.JGbrOS.córas_comhad;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 luach_réamhshocraithe 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class deighilt_VALUE {
        private final int 종류;
        private final long Start_rannán;
        private final long rannán_COUNT;

        deighilt_VALUE(int 종류, long Start_rannán, long rannán_COUNT) {
            this.종류 = 종류;
            this.Start_rannán = Start_rannán;
            this.rannán_COUNT = rannán_COUNT;
        }

        public int 종류() { return 종류; }
        public long Start_rannán() { return Start_rannán; }
        public long rannán_COUNT() { return rannán_COUNT; }
    }

    public List<deighilt_VALUE> Léigh(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<deighilt_VALUE> tomhas = new ArrayList<deighilt_VALUE>();
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            int suíomh = 446 + INDEX * 16;
            int 종류 = 첫구역[suíomh + 4] & 0xff;
            long Rith_2 = 작은순서정수(첫구역, suíomh + 8);
            long Méid = 작은순서정수(첫구역, suíomh + 12);
            if (종류 != 0 && Méid != 0) {
                tomhas.add(new deighilt_VALUE(종류, Rith_2, Méid));
            }
        }
        return Collections.unmodifiableList(tomhas);
    }

    private long 작은순서정수(byte[] sonraí, int suíomh) {
        return (sonraí[suíomh] & 0xffL)
                | ((sonraí[suíomh + 1] & 0xffL) << 8)
                | ((sonraí[suíomh + 2] & 0xffL) << 16)
                | ((sonraí[suíomh + 3] & 0xffL) << 24);
    }
}

