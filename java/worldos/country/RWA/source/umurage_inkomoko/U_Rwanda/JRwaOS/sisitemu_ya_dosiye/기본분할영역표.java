// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package U_Rwanda.JRwaOS.sisitemu_ya_dosiye;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 agaciro_gasanzweho 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class igice_cya_disiki_agaciro {
        private final int 종류;
        private final long Itangira_igice;
        private final long 구역수;

        igice_cya_disiki_agaciro(int 종류, long Itangira_igice, long 구역수) {
            this.종류 = 종류;
            this.Itangira_igice = Itangira_igice;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long Itangira_igice() { return Itangira_igice; }
        public long 구역수() { return 구역수; }
    }

    public List<igice_cya_disiki_agaciro> 읽기(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<igice_cya_disiki_agaciro> 결과 = new ArrayList<igice_cya_disiki_agaciro>();
        for (int umugerekashakiro = 0; umugerekashakiro < 4; umugerekashakiro++) {
            int 위치 = 446 + umugerekashakiro * 16;
            int 종류 = 첫구역[위치 + 4] & 0xff;
            long ihuriro = 작은순서정수(첫구역, 위치 + 8);
            long Ingano = 작은순서정수(첫구역, 위치 + 12);
            if (종류 != 0 && Ingano != 0) {
                결과.add(new igice_cya_disiki_agaciro(종류, ihuriro, Ingano));
            }
        }
        return Collections.unmodifiableList(결과);
    }

    private long 작은순서정수(byte[] amakurushingiro, int 위치) {
        return (amakurushingiro[위치] & 0xffL)
                | ((amakurushingiro[위치 + 1] & 0xffL) << 8)
                | ((amakurushingiro[위치 + 2] & 0xffL) << 16)
                | ((amakurushingiro[위치 + 3] & 0xffL) << 24);
    }
}

