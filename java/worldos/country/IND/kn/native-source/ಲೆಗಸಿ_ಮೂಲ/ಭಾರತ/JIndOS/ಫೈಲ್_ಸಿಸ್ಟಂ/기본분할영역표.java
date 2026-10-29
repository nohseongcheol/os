// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ಭಾರತ.JIndOS.ಫೈಲ್_ಸಿಸ್ಟಂ;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 ಅಕ್ಷಮ_ಬೆಲೆ 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class ವಿಭಜನೆ_ಮೌಲ್ಯ {
        private final int 종류;
        private final long ಆರಂಭಿಸು_ವಿಭಾಗ;
        private final long 구역수;

        ವಿಭಜನೆ_ಮೌಲ್ಯ(int 종류, long ಆರಂಭಿಸು_ವಿಭಾಗ, long 구역수) {
            this.종류 = 종류;
            this.ಆರಂಭಿಸು_ವಿಭಾಗ = ಆರಂಭಿಸು_ವಿಭಾಗ;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long ಆರಂಭಿಸು_ವಿಭಾಗ() { return ಆರಂಭಿಸು_ವಿಭಾಗ; }
        public long 구역수() { return 구역수; }
    }

    public List<ವಿಭಜನೆ_ಮೌಲ್ಯ> ಓದು(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<ವಿಭಜನೆ_ಮೌಲ್ಯ> ಮಾಪನ = new ArrayList<ವಿಭಜನೆ_ಮೌಲ್ಯ>();
        for (int ಪದಸೂಚಿ = 0; ಪದಸೂಚಿ < 4; ಪದಸೂಚಿ++) {
            int ಸ್ಥಾನ = 446 + ಪದಸೂಚಿ * 16;
            int 종류 = 첫구역[ಸ್ಥಾನ + 4] & 0xff;
            long ಚಲಾಯಿಸು_2 = 작은순서정수(첫구역, ಸ್ಥಾನ + 8);
            long ಗಾತ್ರ = 작은순서정수(첫구역, ಸ್ಥಾನ + 12);
            if (종류 != 0 && ಗಾತ್ರ != 0) {
                ಮಾಪನ.add(new ವಿಭಜನೆ_ಮೌಲ್ಯ(종류, ಚಲಾಯಿಸು_2, ಗಾತ್ರ));
            }
        }
        return Collections.unmodifiableList(ಮಾಪನ);
    }

    private long 작은순서정수(byte[] ಡೇಟಾ, int ಸ್ಥಾನ) {
        return (ಡೇಟಾ[ಸ್ಥಾನ] & 0xffL)
                | ((ಡೇಟಾ[ಸ್ಥಾನ + 1] & 0xffL) << 8)
                | ((ಡೇಟಾ[ಸ್ಥಾನ + 2] & 0xffL) << 16)
                | ((ಡೇಟಾ[ಸ್ಥಾನ + 3] & 0xffL) << 24);
    }
}

