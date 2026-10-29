// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ELesotho.JLsoOS.uhlobo_loseto_lwefayile;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 ixabiso_elisisiseko 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class ukwahlulwahlulwa_ixabiso {
        private final int 종류;
        private final long qala_icandelo;
        private final long 구역수;

        ukwahlulwahlulwa_ixabiso(int 종류, long qala_icandelo, long 구역수) {
            this.종류 = 종류;
            this.qala_icandelo = qala_icandelo;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long qala_icandelo() { return qala_icandelo; }
        public long 구역수() { return 구역수; }
    }

    public List<ukwahlulwahlulwa_ixabiso> Funda(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<ukwahlulwahlulwa_ixabiso> 결과 = new ArrayList<ukwahlulwahlulwa_ixabiso>();
        for (int indeksa = 0; indeksa < 4; indeksa++) {
            int 위치 = 446 + indeksa * 16;
            int 종류 = 첫구역[위치 + 4] & 0xff;
            long Phumeza = 작은순서정수(첫구역, 위치 + 8);
            long Ubukhulu = 작은순서정수(첫구역, 위치 + 12);
            if (종류 != 0 && Ubukhulu != 0) {
                결과.add(new ukwahlulwahlulwa_ixabiso(종류, Phumeza, Ubukhulu));
            }
        }
        return Collections.unmodifiableList(결과);
    }

    private long 작은순서정수(byte[] iingcombolo, int 위치) {
        return (iingcombolo[위치] & 0xffL)
                | ((iingcombolo[위치 + 1] & 0xffL) << 8)
                | ((iingcombolo[위치 + 2] & 0xffL) << 16)
                | ((iingcombolo[위치 + 3] & 0xffL) << 24);
    }
}

