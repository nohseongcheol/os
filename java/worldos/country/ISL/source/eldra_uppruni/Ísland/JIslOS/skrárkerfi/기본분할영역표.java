// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ísland.JIslOS.skrárkerfi;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 sjálfgildi 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class sneið_VALUE {
        private final int 종류;
        private final long Opna_hluti;
        private final long hluti_COUNT;

        sneið_VALUE(int 종류, long Opna_hluti, long hluti_COUNT) {
            this.종류 = 종류;
            this.Opna_hluti = Opna_hluti;
            this.hluti_COUNT = hluti_COUNT;
        }

        public int 종류() { return 종류; }
        public long Opna_hluti() { return Opna_hluti; }
        public long hluti_COUNT() { return hluti_COUNT; }
    }

    public List<sneið_VALUE> Lestur(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<sneið_VALUE> NIÐURSTAÐA = new ArrayList<sneið_VALUE>();
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            int Staðsetning = 446 + INDEX * 16;
            int 종류 = 첫구역[Staðsetning + 4] & 0xff;
            long Keyra_2 = 작은순서정수(첫구역, Staðsetning + 8);
            long Stærð = 작은순서정수(첫구역, Staðsetning + 12);
            if (종류 != 0 && Stærð != 0) {
                NIÐURSTAÐA.add(new sneið_VALUE(종류, Keyra_2, Stærð));
            }
        }
        return Collections.unmodifiableList(NIÐURSTAÐA);
    }

    private long 작은순서정수(byte[] gögn, int Staðsetning) {
        return (gögn[Staðsetning] & 0xffL)
                | ((gögn[Staðsetning + 1] & 0xffL) << 8)
                | ((gögn[Staðsetning + 2] & 0xffL) << 16)
                | ((gögn[Staðsetning + 3] & 0xffL) << 24);
    }
}

