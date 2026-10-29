// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ಭಾರತ.JIndOS.ನೆಟ್_ವರ್ಕ್_ಸ್ಟ್ಯಾಕ್;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 ಬೈಟ್_ಮೌಲ್ಯ 순서와 검사합 도구다. */
public final class ನೆಟ್_ವರ್ಕ್_ಪರಿಕರಗಳು {
    private ನೆಟ್_ವರ್ಕ್_ಪರಿಕರಗಳು() {
    }

    public static int 큰순서짧은정수(byte[] ಡೇಟಾ, int ಸ್ಥಾನ) {
        범위확인(ಡೇಟಾ, ಸ್ಥಾನ, 2);
        return ((ಡೇಟಾ[ಸ್ಥಾನ] & 0xff) << 8) | (ಡೇಟಾ[ಸ್ಥಾನ + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] ಡೇಟಾ, int ಸ್ಥಾನ) {
        범위확인(ಡೇಟಾ, ಸ್ಥಾನ, 4);
        return ((long) (ಡೇಟಾ[ಸ್ಥಾನ] & 0xff) << 24)
                | ((long) (ಡೇಟಾ[ಸ್ಥಾನ + 1] & 0xff) << 16)
                | ((long) (ಡೇಟಾ[ಸ್ಥಾನ + 2] & 0xff) << 8)
                | (ಡೇಟಾ[ಸ್ಥಾನ + 3] & 0xffL);
    }

    public static int 인터넷검사합(byte[] ಡೇಟಾ, int ಚಲಾಯಿಸು_2, int ಉದ್ದ_ಮೌಲ್ಯ) {
        범위확인(ಡೇಟಾ, ಚಲಾಯಿಸು_2, ಉದ್ದ_ಮೌಲ್ಯ);
        long 합 = 0;
        int 끝 = ಚಲಾಯಿಸು_2 + ಉದ್ದ_ಮೌಲ್ಯ;
        int ಸ್ಥಾನ = ಚಲಾಯಿಸು_2;
        while (ಸ್ಥಾನ + 1 < 끝) {
            합 += 큰순서짧은정수(ಡೇಟಾ, ಸ್ಥಾನ);
            ಸ್ಥಾನ += 2;
        }
        if (ಸ್ಥಾನ < 끝) {
            합 += (ಡೇಟಾ[ಸ್ಥಾನ] & 0xff) << 8;
        }
        while ((합 >>> 16) != 0) {
            합 = (합 & 0xffff) + (합 >>> 16);
        }
        return (int) (~합) & 0xffff;
    }

    public static boolean ಮಾಹಿತಿ_ತಂತ್ರಜ್ಞಾನ_ಇಥರ್ನೆಟ್_ಫ್ರೇಮ್(byte[] ಡೇಟಾ) {
        return ಡೇಟಾ != null && ಡೇಟಾ.length >= 14;
    }

    public static int 이더넷상위규약(byte[] ಡೇಟಾ) {
        if (!ಮಾಹಿತಿ_ತಂತ್ರಜ್ಞಾನ_ಇಥರ್ನೆಟ್_ಫ್ರೇಮ್(ಡೇಟಾ)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(ಡೇಟಾ, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] ಡೇಟಾ, int ಸ್ಥಾನ) {
        if (ಡೇಟಾ == null || ಸ್ಥಾನ < 0 || ಡೇಟಾ.length - ಸ್ಥಾನ < 20) {
            return false;
        }
        int ಆವೃತ್ತಿ_ಮೌಲ್ಯ = (ಡೇಟಾ[ಸ್ಥಾನ] >>> 4) & 0xf;
        int ಶಿರೋಲೇಖ_ಉದ್ದ = (ಡೇಟಾ[ಸ್ಥಾನ] & 0xf) * 4;
        return ಆವೃತ್ತಿ_ಮೌಲ್ಯ == 4 && ಶಿರೋಲೇಖ_ಉದ್ದ >= 20 && ಡೇಟಾ.length - ಸ್ಥಾನ >= ಶಿರೋಲೇಖ_ಉದ್ದ;
    }

    private static void 범위확인(byte[] ಡೇಟಾ, int ಚಲಾಯಿಸು_2, int ಉದ್ದ_ಮೌಲ್ಯ) {
        if (ಡೇಟಾ == null || ಚಲಾಯಿಸು_2 < 0 || ಉದ್ದ_ಮೌಲ್ಯ < 0 || ಚಲಾಯಿಸು_2 > ಡೇಟಾ.length - ಉದ್ದ_ಮೌಲ್ಯ) {
            throw new IllegalArgumentException("ನೆಟ್_ವರ್ಕ್_ಸ್ಟ್ಯಾಕ್ ಡೇಟಾ 범위를 벗어났습니다.");
        }
    }
}

