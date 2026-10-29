// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ኢትዮጵያ.JEthOS.መረብ_ክምር;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 ባይት_እሴት 순서와 ድምር_ፍተሻ 도구다. */
public final class መረብ_መሳሪያዎች {
    private መረብ_መሳሪያዎች() {
    }

    public static int 큰순서짧은정수(byte[] ውሂብ, int አካባቢ) {
        범위확인(ውሂብ, አካባቢ, 2);
        return ((ውሂብ[አካባቢ] & 0xff) << 8) | (ውሂብ[አካባቢ + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] ውሂብ, int አካባቢ) {
        범위확인(ውሂብ, አካባቢ, 4);
        return ((long) (ውሂብ[አካባቢ] & 0xff) << 24)
                | ((long) (ውሂብ[አካባቢ + 1] & 0xff) << 16)
                | ((long) (ውሂብ[አካባቢ + 2] & 0xff) << 8)
                | (ውሂብ[አካባቢ + 3] & 0xffL);
    }

    public static int ክላውድ_ድምር_ፍተሻ(byte[] ውሂብ, int ማስኬጃ, int ርዝመት_እሴት) {
        범위확인(ውሂብ, ማስኬጃ, ርዝመት_እሴት);
        long 합 = 0;
        int 끝 = ማስኬጃ + ርዝመት_እሴት;
        int አካባቢ = ማስኬጃ;
        while (አካባቢ + 1 < 끝) {
            합 += 큰순서짧은정수(ውሂብ, አካባቢ);
            አካባቢ += 2;
        }
        if (አካባቢ < 끝) {
            합 += (ውሂብ[አካባቢ] & 0xff) << 8;
        }
        while ((합 >>> 16) != 0) {
            합 = (합 & 0xffff) + (합 >>> 16);
        }
        return (int) (~합) & 0xffff;
    }

    public static boolean የመረጃ_ቴክኖሎጂ_ኢተርኔት_ማዕቀፍ(byte[] ውሂብ) {
        return ውሂብ != null && ውሂብ.length >= 14;
    }

    public static int 이더넷상위규약(byte[] ውሂብ) {
        if (!የመረጃ_ቴክኖሎጂ_ኢተርኔት_ማዕቀፍ(ውሂብ)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(ውሂብ, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] ውሂብ, int አካባቢ) {
        if (ውሂብ == null || አካባቢ < 0 || ውሂብ.length - አካባቢ < 20) {
            return false;
        }
        int ስሪት_እሴት = (ውሂብ[አካባቢ] >>> 4) & 0xf;
        int ርእስ_ርዝመት = (ውሂብ[አካባቢ] & 0xf) * 4;
        return ስሪት_እሴት == 4 && ርእስ_ርዝመት >= 20 && ውሂብ.length - አካባቢ >= ርእስ_ርዝመት;
    }

    private static void 범위확인(byte[] ውሂብ, int ማስኬጃ, int ርዝመት_እሴት) {
        if (ውሂብ == null || ማስኬጃ < 0 || ርዝመት_እሴት < 0 || ማስኬጃ > ውሂብ.length - ርዝመት_እሴት) {
            throw new IllegalArgumentException("መረብ_ክምር ውሂብ 범위를 벗어났습니다.");
        }
    }
}

