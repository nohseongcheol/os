// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Naịjịrịa.JNgaOS.sistèm_ọbọakwụkwo;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 Ngwa_ihe_dịadị 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class nkègasiōhèrè_valuu {
        private final int 종류;
        private final long Mbido_nkebì;
        private final long 구역수;

        nkègasiōhèrè_valuu(int 종류, long Mbido_nkebì, long 구역수) {
            this.종류 = 종류;
            this.Mbido_nkebì = Mbido_nkebì;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long Mbido_nkebì() { return Mbido_nkebì; }
        public long 구역수() { return 구역수; }
    }

    public List<nkègasiōhèrè_valuu> Wepụta_ọzi(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<nkègasiōhèrè_valuu> 결과 = new ArrayList<nkègasiōhèrè_valuu>();
        for (int indèks = 0; indèks < 4; indèks++) {
            int 위치 = 446 + indèks * 16;
            int 종류 = 첫구역[위치 + 4] & 0xff;
            long Bido = 작은순서정수(첫구역, 위치 + 8);
            long Ụhara = 작은순서정수(첫구역, 위치 + 12);
            if (종류 != 0 && Ụhara != 0) {
                결과.add(new nkègasiōhèrè_valuu(종류, Bido, Ụhara));
            }
        }
        return Collections.unmodifiableList(결과);
    }

    private long 작은순서정수(byte[] datà, int 위치) {
        return (datà[위치] & 0xffL)
                | ((datà[위치 + 1] & 0xffL) << 8)
                | ((datà[위치 + 2] & 0xffL) << 16)
                | ((datà[위치 + 3] & 0xffL) << 24);
    }
}

