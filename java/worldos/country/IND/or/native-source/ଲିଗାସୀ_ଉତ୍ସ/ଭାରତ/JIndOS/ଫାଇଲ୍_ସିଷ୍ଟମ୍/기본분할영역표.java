// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ଭାରତ.JIndOS.ଫାଇଲ୍_ସିଷ୍ଟମ୍;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 ଡିଫଲ୍ଟ_ମାନ 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class ବିଭାଜନ_ମୂଲ୍ୟ {
        private final int 종류;
        private final long ଆରମ୍ଭ_ବିଭାଗ;
        private final long 구역수;

        ବିଭାଜନ_ମୂଲ୍ୟ(int 종류, long ଆରମ୍ଭ_ବିଭାଗ, long 구역수) {
            this.종류 = 종류;
            this.ଆରମ୍ଭ_ବିଭାଗ = ଆରମ୍ଭ_ବିଭାଗ;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long ଆରମ୍ଭ_ବିଭାଗ() { return ଆରମ୍ଭ_ବିଭାଗ; }
        public long 구역수() { return 구역수; }
    }

    public List<ବିଭାଜନ_ମୂଲ୍ୟ> ପଢନ୍ତୁ(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<ବିଭାଜନ_ମୂଲ୍ୟ> ମାପ = new ArrayList<ବିଭାଜନ_ମୂଲ୍ୟ>();
        for (int ଅନୁକ୍ରମଣିକା = 0; ଅନୁକ୍ରମଣିକା < 4; ଅନୁକ୍ରମଣିକା++) {
            int ଅବସ୍ଥାନ = 446 + ଅନୁକ୍ରମଣିକା * 16;
            int 종류 = 첫구역[ଅବସ୍ଥାନ + 4] & 0xff;
            long ଚଳାନ୍ତୁ = 작은순서정수(첫구역, ଅବସ୍ଥାନ + 8);
            long ଆକାର = 작은순서정수(첫구역, ଅବସ୍ଥାନ + 12);
            if (종류 != 0 && ଆକାର != 0) {
                ମାପ.add(new ବିଭାଜନ_ମୂଲ୍ୟ(종류, ଚଳାନ୍ତୁ, ଆକାର));
            }
        }
        return Collections.unmodifiableList(ମାପ);
    }

    private long 작은순서정수(byte[] ଡାଟା, int ଅବସ୍ଥାନ) {
        return (ଡାଟା[ଅବସ୍ଥାନ] & 0xffL)
                | ((ଡାଟା[ଅବସ୍ଥାନ + 1] & 0xffL) << 8)
                | ((ଡାଟା[ଅବସ୍ଥାନ + 2] & 0xffL) << 16)
                | ((ଡାଟା[ଅବସ୍ଥାନ + 3] & 0xffL) << 24);
    }
}

