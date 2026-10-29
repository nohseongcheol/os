// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Malta.JMltOS.sistema_tal_fajls;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 valur_default 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class taqsima_VALUE {
        private final int 종류;
        private final long Bidu_taqsima;
        private final long taqsima_COUNT;

        taqsima_VALUE(int 종류, long Bidu_taqsima, long taqsima_COUNT) {
            this.종류 = 종류;
            this.Bidu_taqsima = Bidu_taqsima;
            this.taqsima_COUNT = taqsima_COUNT;
        }

        public int 종류() { return 종류; }
        public long Bidu_taqsima() { return Bidu_taqsima; }
        public long taqsima_COUNT() { return taqsima_COUNT; }
    }

    public List<taqsima_VALUE> 읽기(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<taqsima_VALUE> miżura = new ArrayList<taqsima_VALUE>();
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            int pożizzjoni = 446 + INDEX * 16;
            int 종류 = 첫구역[pożizzjoni + 4] & 0xff;
            long serje = 작은순서정수(첫구역, pożizzjoni + 8);
            long daqqas = 작은순서정수(첫구역, pożizzjoni + 12);
            if (종류 != 0 && daqqas != 0) {
                miżura.add(new taqsima_VALUE(종류, serje, daqqas));
            }
        }
        return Collections.unmodifiableList(miżura);
    }

    private long 작은순서정수(byte[] data, int pożizzjoni) {
        return (data[pożizzjoni] & 0xffL)
                | ((data[pożizzjoni + 1] & 0xffL) << 8)
                | ((data[pożizzjoni + 2] & 0xffL) << 16)
                | ((data[pożizzjoni + 3] & 0xffL) << 24);
    }
}

