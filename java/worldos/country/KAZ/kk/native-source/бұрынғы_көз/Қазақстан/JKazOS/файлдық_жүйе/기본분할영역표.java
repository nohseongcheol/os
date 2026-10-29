// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Қазақстан.JKazOS.файлдық_жүйе;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 әдепкі_мән 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class бөлім_мән {
        private final int 종류;
        private final long басы_бөлім;
        private final long 구역수;

        бөлім_мән(int 종류, long басы_бөлім, long 구역수) {
            this.종류 = 종류;
            this.басы_бөлім = басы_бөлім;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long басы_бөлім() { return басы_бөлім; }
        public long 구역수() { return 구역수; }
    }

    public List<бөлім_мән> Оқу(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<бөлім_мән> НӘТИЖЕ = new ArrayList<бөлім_мән>();
        for (int индекс = 0; индекс < 4; индекс++) {
            int Орны = 446 + индекс * 16;
            int 종류 = 첫구역[Орны + 4] & 0xff;
            long Орындау_2 = байттардың_тура_реті_бүтін_сан(첫구역, Орны + 8);
            long Өлшемі = байттардың_тура_реті_бүтін_сан(첫구역, Орны + 12);
            if (종류 != 0 && Өлшемі != 0) {
                НӘТИЖЕ.add(new бөлім_мән(종류, Орындау_2, Өлшемі));
            }
        }
        return Collections.unmodifiableList(НӘТИЖЕ);
    }

    private long байттардың_тура_реті_бүтін_сан(byte[] деректер, int Орны) {
        return (деректер[Орны] & 0xffL)
                | ((деректер[Орны + 1] & 0xffL) << 8)
                | ((деректер[Орны + 2] & 0xffL) << 16)
                | ((деректер[Орны + 3] & 0xffL) << 24);
    }
}

