// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ಭಾರತ.JIndOS.ಫೈಲ್_ಸಿಸ್ಟಂ;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian ಪೂರೈಸು_ಆದೇಶ 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class ವಿಭಾಗ_ಮೌಲ್ಯ {
        private final int 종류;
        private final int ಫ್ಲ್ಯಾಗ್_ಮೌಲ್ಯ;
        private final int ಇಮೇಲ್;
        private final int ಫೈಲ್_ಹುದ್ದೆ;
        private final int ಗಾತ್ರ;

        ವಿಭಾಗ_ಮೌಲ್ಯ(int 종류, int ಫ್ಲ್ಯಾಗ್_ಮೌಲ್ಯ, int ಇಮೇಲ್, int ಫೈಲ್_ಹುದ್ದೆ, int ಗಾತ್ರ) {
            this.종류 = 종류;
            this.ಫ್ಲ್ಯಾಗ್_ಮೌಲ್ಯ = ಫ್ಲ್ಯಾಗ್_ಮೌಲ್ಯ;
            this.ಇಮೇಲ್ = ಇಮೇಲ್;
            this.ಫೈಲ್_ಹುದ್ದೆ = ಫೈಲ್_ಹುದ್ದೆ;
            this.ಗಾತ್ರ = ಗಾತ್ರ;
        }

        public int 종류() {
            return 종류;
        }

        public int ಫ್ಲ್ಯಾಗ್_ಮೌಲ್ಯ() {
            return ಫ್ಲ್ಯಾಗ್_ಮೌಲ್ಯ;
        }

        public int ಇಮೇಲ್() {
            return ಇಮೇಲ್;
        }

        public int ಫೈಲ್_ಹುದ್ದೆ() {
            return ಫೈಲ್_ಹುದ್ದೆ;
        }

        public int ಗಾತ್ರ() {
            return ಗಾತ್ರ;
        }
    }

    public static final class ಇಮೇಜ್ {
        private final int ಆರಂಭಿಸು_ಇಮೇಲ್;
        private final List<ವಿಭಾಗ_ಮೌಲ್ಯ> 구역들;

        ಇಮೇಜ್(int ಆರಂಭಿಸು_ಇಮೇಲ್, List<ವಿಭಾಗ_ಮೌಲ್ಯ> 구역들) {
            this.ಆರಂಭಿಸು_ಇಮೇಲ್ = ಆರಂಭಿಸು_ಇಮೇಲ್;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int ಆರಂಭಿಸು_ಇಮೇಲ್() {
            return ಆರಂಭಿಸು_ಇಮೇಲ್;
        }

        public List<ವಿಭಾಗ_ಮೌಲ್ಯ> 구역들() {
            return 구역들;
        }
    }

    public ಇಮೇಜ್ 검사(byte[] ಡೇಟಾ) {
        if (ಡೇಟಾ == null || ಡೇಟಾ.length < 52
                || ಡೇಟಾ[0] != 0x7f || ಡೇಟಾ[1] != 'E' || ಡೇಟಾ[2] != 'L' || ಡೇಟಾ[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (ಡೇಟಾ[4] != 1 || ಡೇಟಾ[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int ಆರಂಭಿಸು_ಇಮೇಲ್ = ಪಾರ್ಸ್_ಮಾಡಿ_ಪೂರ್ಣಸಂಖ್ಯೆ(ಡೇಟಾ, 24);
        int ವಿಭಾಗ_ಕೋಷ್ಟಕ_ಹುದ್ದೆ = ಪಾರ್ಸ್_ಮಾಡಿ_ಪೂರ್ಣಸಂಖ್ಯೆ(ಡೇಟಾ, 32);
        int ವಿಭಾಗ_ನಮೂದು_ಗಾತ್ರಿಸು = 짧은정수읽기(ಡೇಟಾ, 46);
        int 구역수 = 짧은정수읽기(ಡೇಟಾ, 48);
        if (ವಿಭಾಗ_ನಮೂದು_ಗಾತ್ರಿಸು < 40 || ವಿಭಾಗ_ಕೋಷ್ಟಕ_ಹುದ್ದೆ < 0
                || (long) ವಿಭಾಗ_ಕೋಷ್ಟಕ_ಹುದ್ದೆ + (long) ವಿಭಾಗ_ನಮೂದು_ಗಾತ್ರಿಸು * 구역수 > ಡೇಟಾ.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<ವಿಭಾಗ_ಮೌಲ್ಯ> 구역들 = new ArrayList<ವಿಭಾಗ_ಮೌಲ್ಯ>();
        for (int ಪದಸೂಚಿ = 0; ಪದಸೂಚಿ < 구역수; ಪದಸೂಚಿ++) {
            int ಸ್ಥಾನ = ವಿಭಾಗ_ಕೋಷ್ಟಕ_ಹುದ್ದೆ + ಪದಸೂಚಿ * ವಿಭಾಗ_ನಮೂದು_ಗಾತ್ರಿಸು;
            int 종류 = ಪಾರ್ಸ್_ಮಾಡಿ_ಪೂರ್ಣಸಂಖ್ಯೆ(ಡೇಟಾ, ಸ್ಥಾನ + 4);
            int ಫ್ಲ್ಯಾಗ್_ಮೌಲ್ಯ = ಪಾರ್ಸ್_ಮಾಡಿ_ಪೂರ್ಣಸಂಖ್ಯೆ(ಡೇಟಾ, ಸ್ಥಾನ + 8);
            int ಇಮೇಲ್ = ಪಾರ್ಸ್_ಮಾಡಿ_ಪೂರ್ಣಸಂಖ್ಯೆ(ಡೇಟಾ, ಸ್ಥಾನ + 12);
            int ಫೈಲ್_ಹುದ್ದೆ = ಪಾರ್ಸ್_ಮಾಡಿ_ಪೂರ್ಣಸಂಖ್ಯೆ(ಡೇಟಾ, ಸ್ಥಾನ + 16);
            int ಗಾತ್ರ = ಪಾರ್ಸ್_ಮಾಡಿ_ಪೂರ್ಣಸಂಖ್ಯೆ(ಡೇಟಾ, ಸ್ಥಾನ + 20);
            if (ಗಾತ್ರ < 0 || (종류 != 8 && ((long) ಫೈಲ್_ಹುದ್ದೆ + ಗಾತ್ರ > ಡೇಟಾ.length || ಫೈಲ್_ಹುದ್ದೆ < 0))) {
                throw new IllegalArgumentException("ELF ವಿಭಾಗ_ಮೌಲ್ಯ ಡೇಟಾ 범위가 올바르지 않습니다.");
            }
            구역들.add(new ವಿಭಾಗ_ಮೌಲ್ಯ(종류, ಫ್ಲ್ಯಾಗ್_ಮೌಲ್ಯ, ಇಮೇಲ್, ಫೈಲ್_ಹುದ್ದೆ, ಗಾತ್ರ));
        }
        return new ಇಮೇಜ್(ಆರಂಭಿಸು_ಇಮೇಲ್, 구역들);
    }

    private int ಪಾರ್ಸ್_ಮಾಡಿ_ಪೂರ್ಣಸಂಖ್ಯೆ(byte[] ಡೇಟಾ, int ಸ್ಥಾನ) {
        if (ಸ್ಥಾನ < 0 || ಸ್ಥಾನ > ಡೇಟಾ.length - 4) {
            throw new IllegalArgumentException("ELF ಪೂರ್ಣಸಂಖ್ಯೆ 범위를 벗어났습니다.");
        }
        return (ಡೇಟಾ[ಸ್ಥಾನ] & 0xff)
                | ((ಡೇಟಾ[ಸ್ಥಾನ + 1] & 0xff) << 8)
                | ((ಡೇಟಾ[ಸ್ಥಾನ + 2] & 0xff) << 16)
                | ((ಡೇಟಾ[ಸ್ಥಾನ + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] ಡೇಟಾ, int ಸ್ಥಾನ) {
        if (ಸ್ಥಾನ < 0 || ಸ್ಥಾನ > ಡೇಟಾ.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 ಪೂರ್ಣಸಂಖ್ಯೆ 범위를 벗어났습니다.");
        }
        return (ಡೇಟಾ[ಸ್ಥಾನ] & 0xff) | ((ಡೇಟಾ[ಸ್ಥಾನ + 1] & 0xff) << 8);
    }
}
