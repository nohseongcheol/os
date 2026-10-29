// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package கனடா.JCanOS.கோப்பு_முறைமை;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 இயல்புநிலை_மதிப்பு 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class பகுதிப்பிரிப்பு_மதிப்பு {
        private final int 종류;
        private final long தொடங்கு_பிரிவு;
        private final long 구역수;

        பகுதிப்பிரிப்பு_மதிப்பு(int 종류, long தொடங்கு_பிரிவு, long 구역수) {
            this.종류 = 종류;
            this.தொடங்கு_பிரிவு = தொடங்கு_பிரிவு;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long தொடங்கு_பிரிவு() { return தொடங்கு_பிரிவு; }
        public long 구역수() { return 구역수; }
    }

    public List<பகுதிப்பிரிப்பு_மதிப்பு> படி(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<பகுதிப்பிரிப்பு_மதிப்பு> அளவிடக்கூடியது = new ArrayList<பகுதிப்பிரிப்பு_மதிப்பு>();
        for (int அடைவு = 0; அடைவு < 4; அடைவு++) {
            int இடம் = 446 + அடைவு * 16;
            int 종류 = 첫구역[இடம் + 4] & 0xff;
            long செயல்படுத்துக = 작은순서정수(첫구역, இடம் + 8);
            long அளவு = 작은순서정수(첫구역, இடம் + 12);
            if (종류 != 0 && அளவு != 0) {
                அளவிடக்கூடியது.add(new பகுதிப்பிரிப்பு_மதிப்பு(종류, செயல்படுத்துக, அளவு));
            }
        }
        return Collections.unmodifiableList(அளவிடக்கூடியது);
    }

    private long 작은순서정수(byte[] தரவு, int இடம்) {
        return (தரவு[இடம்] & 0xffL)
                | ((தரவு[இடம் + 1] & 0xffL) << 8)
                | ((தரவு[இடம் + 2] & 0xffL) << 16)
                | ((தரவு[இடம் + 3] & 0xffL) << 24);
    }
}

