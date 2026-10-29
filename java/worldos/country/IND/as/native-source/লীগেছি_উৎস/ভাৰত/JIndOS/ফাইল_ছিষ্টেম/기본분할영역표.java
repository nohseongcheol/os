// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ভাৰত.JIndOS.ফাইল_ছিষ্টেম;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 ডিফ_ল্ট_মান 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class বিভাজন_মান {
        private final int 종류;
        private final long আৰম্ভ_শাখা;
        private final long 구역수;

        বিভাজন_মান(int 종류, long আৰম্ভ_শাখা, long 구역수) {
            this.종류 = 종류;
            this.আৰম্ভ_শাখা = আৰম্ভ_শাখা;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long আৰম্ভ_শাখা() { return আৰম্ভ_শাখা; }
        public long 구역수() { return 구역수; }
    }

    public List<বিভাজন_মান> পড়া(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<বিভাজন_মান> পৰিমাপ = new ArrayList<বিভাজন_মান>();
        for (int ইনডেক্স = 0; ইনডেক্স < 4; ইনডেক্স++) {
            int অৱস্থান = 446 + ইনডেক্স * 16;
            int 종류 = 첫구역[অৱস্থান + 4] & 0xff;
            long সঞ্চালন = 작은순서정수(첫구역, অৱস্থান + 8);
            long মাপ = 작은순서정수(첫구역, অৱস্থান + 12);
            if (종류 != 0 && মাপ != 0) {
                পৰিমাপ.add(new বিভাজন_মান(종류, সঞ্চালন, মাপ));
            }
        }
        return Collections.unmodifiableList(পৰিমাপ);
    }

    private long 작은순서정수(byte[] ডাটা, int অৱস্থান) {
        return (ডাটা[অৱস্থান] & 0xffL)
                | ((ডাটা[অৱস্থান + 1] & 0xffL) << 8)
                | ((ডাটা[অৱস্থান + 2] & 0xffL) << 16)
                | ((ডাটা[অৱস্থান + 3] & 0xffL) << 24);
    }
}

