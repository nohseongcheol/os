// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package భారతదేశం.JIndOS.ఫైల్_వ్యవస్థ;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 స్వయంసిద్ధ_విలువ 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class విభజన_మూల్యం {
        private final int 종류;
        private final long ప్రారంభం_విభాగం;
        private final long 구역수;

        విభజన_మూల్యం(int 종류, long ప్రారంభం_విభాగం, long 구역수) {
            this.종류 = 종류;
            this.ప్రారంభం_విభాగం = ప్రారంభం_విభాగం;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long ప్రారంభం_విభాగం() { return ప్రారంభం_విభాగం; }
        public long 구역수() { return 구역수; }
    }

    public List<విభజన_మూల్యం> చదువు(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<విభజన_మూల్యం> ప్రమాణం = new ArrayList<విభజన_మూల్యం>();
        for (int సూచీ = 0; సూచీ < 4; సూచీ++) {
            int స్థానము = 446 + సూచీ * 16;
            int 종류 = 첫구역[స్థానము + 4] & 0xff;
            long నడుపుము = 작은순서정수(첫구역, స్థానము + 8);
            long పరిమాణం = 작은순서정수(첫구역, స్థానము + 12);
            if (종류 != 0 && పరిమాణం != 0) {
                ప్రమాణం.add(new విభజన_మూల్యం(종류, నడుపుము, పరిమాణం));
            }
        }
        return Collections.unmodifiableList(ప్రమాణం);
    }

    private long 작은순서정수(byte[] డేటా, int స్థానము) {
        return (డేటా[స్థానము] & 0xffL)
                | ((డేటా[స్థానము + 1] & 0xffL) << 8)
                | ((డేటా[స్థానము + 2] & 0xffL) << 16)
                | ((డేటా[స్థానము + 3] & 0xffL) << 24);
    }
}

