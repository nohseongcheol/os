// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ਕੀਨੀਆ.JKenOS.ਨੈਟਵਰਕ_ਸਟੈਕ;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 ਬਾਈਟ_ਕੀਮਤ 순서와 검사합 도구다. */
public final class ਨੈਟਵਰਕ_ਸਾਧਨ {
    private ਨੈਟਵਰਕ_ਸਾਧਨ() {
    }

    public static int 큰순서짧은정수(byte[] ਸਮੱਗਰੀ, int ਸਥਿਤੀ) {
        범위확인(ਸਮੱਗਰੀ, ਸਥਿਤੀ, 2);
        return ((ਸਮੱਗਰੀ[ਸਥਿਤੀ] & 0xff) << 8) | (ਸਮੱਗਰੀ[ਸਥਿਤੀ + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] ਸਮੱਗਰੀ, int ਸਥਿਤੀ) {
        범위확인(ਸਮੱਗਰੀ, ਸਥਿਤੀ, 4);
        return ((long) (ਸਮੱਗਰੀ[ਸਥਿਤੀ] & 0xff) << 24)
                | ((long) (ਸਮੱਗਰੀ[ਸਥਿਤੀ + 1] & 0xff) << 16)
                | ((long) (ਸਮੱਗਰੀ[ਸਥਿਤੀ + 2] & 0xff) << 8)
                | (ਸਮੱਗਰੀ[ਸਥਿਤੀ + 3] & 0xffL);
    }

    public static int 인터넷검사합(byte[] ਸਮੱਗਰੀ, int ਚਲਾਓ_2, int ਲੰਬਾਈ_ਕੀਮਤ) {
        범위확인(ਸਮੱਗਰੀ, ਚਲਾਓ_2, ਲੰਬਾਈ_ਕੀਮਤ);
        long 합 = 0;
        int 끝 = ਚਲਾਓ_2 + ਲੰਬਾਈ_ਕੀਮਤ;
        int ਸਥਿਤੀ = ਚਲਾਓ_2;
        while (ਸਥਿਤੀ + 1 < 끝) {
            합 += 큰순서짧은정수(ਸਮੱਗਰੀ, ਸਥਿਤੀ);
            ਸਥਿਤੀ += 2;
        }
        if (ਸਥਿਤੀ < 끝) {
            합 += (ਸਮੱਗਰੀ[ਸਥਿਤੀ] & 0xff) << 8;
        }
        while ((합 >>> 16) != 0) {
            합 = (합 & 0xffff) + (합 >>> 16);
        }
        return (int) (~합) & 0xffff;
    }

    public static boolean 이더넷틀인가(byte[] ਸਮੱਗਰੀ) {
        return ਸਮੱਗਰੀ != null && ਸਮੱਗਰੀ.length >= 14;
    }

    public static int 이더넷상위규약(byte[] ਸਮੱਗਰੀ) {
        if (!이더넷틀인가(ਸਮੱਗਰੀ)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(ਸਮੱਗਰੀ, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] ਸਮੱਗਰੀ, int ਸਥਿਤੀ) {
        if (ਸਮੱਗਰੀ == null || ਸਥਿਤੀ < 0 || ਸਮੱਗਰੀ.length - ਸਥਿਤੀ < 20) {
            return false;
        }
        int ਵਰਜ਼ਨ_ਕੀਮਤ = (ਸਮੱਗਰੀ[ਸਥਿਤੀ] >>> 4) & 0xf;
        int ਸਿਰਲੇਖ_ਲੰਬਾਈ = (ਸਮੱਗਰੀ[ਸਥਿਤੀ] & 0xf) * 4;
        return ਵਰਜ਼ਨ_ਕੀਮਤ == 4 && ਸਿਰਲੇਖ_ਲੰਬਾਈ >= 20 && ਸਮੱਗਰੀ.length - ਸਥਿਤੀ >= ਸਿਰਲੇਖ_ਲੰਬਾਈ;
    }

    private static void 범위확인(byte[] ਸਮੱਗਰੀ, int ਚਲਾਓ_2, int ਲੰਬਾਈ_ਕੀਮਤ) {
        if (ਸਮੱਗਰੀ == null || ਚਲਾਓ_2 < 0 || ਲੰਬਾਈ_ਕੀਮਤ < 0 || ਚਲਾਓ_2 > ਸਮੱਗਰੀ.length - ਲੰਬਾਈ_ਕੀਮਤ) {
            throw new IllegalArgumentException("ਨੈਟਵਰਕ_ਸਟੈਕ ਸਮੱਗਰੀ 범위를 벗어났습니다.");
        }
    }
}

