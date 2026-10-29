// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package កម្ពុជា.JKhmOS.ឯកសារនៃប្រព័ន្ធ;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 តំលៃស្វ័យប្រវត្តិ 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class បំណែក_តំលៃ {
        private final int 종류;
        private final long ផ្តើម_ផ្នែក;
        private final long 구역수;

        បំណែក_តំលៃ(int 종류, long ផ្តើម_ផ្នែក, long 구역수) {
            this.종류 = 종류;
            this.ផ្តើម_ផ្នែក = ផ្តើម_ផ្នែក;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long ផ្តើម_ផ្នែក() { return ផ្តើម_ផ្នែក; }
        public long 구역수() { return 구역수; }
    }

    public List<បំណែក_តំលៃ> អាន(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<បំណែក_តំលៃ> ការវាស់វែង = new ArrayList<បំណែក_តំលៃ>();
        for (int សន្ទស្សន៏ = 0; សន្ទស្សន៏ < 4; សន្ទស្សន៏++) {
            int កំណត់ទីតាំង = 446 + សន្ទស្សន៏ * 16;
            int 종류 = 첫구역[កំណត់ទីតាំង + 4] & 0xff;
            long រត់ = 작은순서정수(첫구역, កំណត់ទីតាំង + 8);
            long ដាក់ទំហំ = 작은순서정수(첫구역, កំណត់ទីតាំង + 12);
            if (종류 != 0 && ដាក់ទំហំ != 0) {
                ការវាស់វែង.add(new បំណែក_តំលៃ(종류, រត់, ដាក់ទំហំ));
            }
        }
        return Collections.unmodifiableList(ការវាស់វែង);
    }

    private long 작은순서정수(byte[] ទិន្នន័យ, int កំណត់ទីតាំង) {
        return (ទិន្នន័យ[កំណត់ទីតាំង] & 0xffL)
                | ((ទិន្នន័យ[កំណត់ទីតាំង + 1] & 0xffL) << 8)
                | ((ទិន្នន័យ[កំណត់ទីតាំង + 2] & 0xffL) << 16)
                | ((ទិន្នន័យ[កំណត់ទីតាំង + 3] & 0xffL) << 24);
    }
}

