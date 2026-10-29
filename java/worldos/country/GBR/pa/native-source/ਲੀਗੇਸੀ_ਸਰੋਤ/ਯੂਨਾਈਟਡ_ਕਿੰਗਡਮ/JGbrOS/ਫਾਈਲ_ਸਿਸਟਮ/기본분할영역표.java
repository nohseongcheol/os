// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ਯੂਨਾਈਟਡ_ਕਿੰਗਡਮ.JGbrOS.ਫਾਈਲ_ਸਿਸਟਮ;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 ਡਿਫੌਲਟ_ਵੈਲਯੂ 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class ਵੰਡ_ਕੀਮਤ {
        private final int 종류;
        private final long ਸੁਰੂ_ਵਿਭਾਗ;
        private final long 구역수;

        ਵੰਡ_ਕੀਮਤ(int 종류, long ਸੁਰੂ_ਵਿਭਾਗ, long 구역수) {
            this.종류 = 종류;
            this.ਸੁਰੂ_ਵਿਭਾਗ = ਸੁਰੂ_ਵਿਭਾਗ;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long ਸੁਰੂ_ਵਿਭਾਗ() { return ਸੁਰੂ_ਵਿਭਾਗ; }
        public long 구역수() { return 구역수; }
    }

    public List<ਵੰਡ_ਕੀਮਤ> ਪੜ੍ਹਨ(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<ਵੰਡ_ਕੀਮਤ> ਮਾਪ = new ArrayList<ਵੰਡ_ਕੀਮਤ>();
        for (int ਅਨੁਕ੍ਰਮਣਿਕਾ = 0; ਅਨੁਕ੍ਰਮਣਿਕਾ < 4; ਅਨੁਕ੍ਰਮਣਿਕਾ++) {
            int ਸਥਿਤੀ = 446 + ਅਨੁਕ੍ਰਮਣਿਕਾ * 16;
            int 종류 = 첫구역[ਸਥਿਤੀ + 4] & 0xff;
            long ਚਲਾਓ_2 = 작은순서정수(첫구역, ਸਥਿਤੀ + 8);
            long ਆਕਾਰ = 작은순서정수(첫구역, ਸਥਿਤੀ + 12);
            if (종류 != 0 && ਆਕਾਰ != 0) {
                ਮਾਪ.add(new ਵੰਡ_ਕੀਮਤ(종류, ਚਲਾਓ_2, ਆਕਾਰ));
            }
        }
        return Collections.unmodifiableList(ਮਾਪ);
    }

    private long 작은순서정수(byte[] ਸਮੱਗਰੀ, int ਸਥਿਤੀ) {
        return (ਸਮੱਗਰੀ[ਸਥਿਤੀ] & 0xffL)
                | ((ਸਮੱਗਰੀ[ਸਥਿਤੀ + 1] & 0xffL) << 8)
                | ((ਸਮੱਗਰੀ[ਸਥਿਤੀ + 2] & 0xffL) << 16)
                | ((ਸਮੱਗਰੀ[ਸਥਿਤੀ + 3] & 0xffL) << 24);
    }
}

