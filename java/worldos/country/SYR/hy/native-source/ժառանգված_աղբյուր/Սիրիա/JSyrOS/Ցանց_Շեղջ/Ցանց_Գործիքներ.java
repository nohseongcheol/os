// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Սիրիա.JSyrOS.Ցանց_Շեղջ;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 բայթ_արժեք 순서와 검사합 도구다. */
public final class Ցանց_Գործիքներ {
    private Ցանց_Գործիքներ() {
    }

    public static int 큰순서짧은정수(byte[] տվյալ, int Դիրք) {
        범위확인(տվյալ, Դիրք, 2);
        return ((տվյալ[Դիրք] & 0xff) << 8) | (տվյալ[Դիրք + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] տվյալ, int Դիրք) {
        범위확인(տվյալ, Դիրք, 4);
        return ((long) (տվյալ[Դիրք] & 0xff) << 24)
                | ((long) (տվյալ[Դիրք + 1] & 0xff) << 16)
                | ((long) (տվյալ[Դիրք + 2] & 0xff) << 8)
                | (տվյալ[Դիրք + 3] & 0xffL);
    }

    public static int 인터넷검사합(byte[] տվյալ, int Գործարկել, int տեւողություն_արժեք) {
        범위확인(տվյալ, Գործարկել, տեւողություն_արժեք);
        long 합 = 0;
        int 끝 = Գործարկել + տեւողություն_արժեք;
        int Դիրք = Գործարկել;
        while (Դիրք + 1 < 끝) {
            합 += 큰순서짧은정수(տվյալ, Դիրք);
            Դիրք += 2;
        }
        if (Դիրք < 끝) {
            합 += (տվյալ[Դիրք] & 0xff) << 8;
        }
        while ((합 >>> 16) != 0) {
            합 = (합 & 0xffff) + (합 >>> 16);
        }
        return (int) (~합) & 0xffff;
    }

    public static boolean 이더넷틀인가(byte[] տվյալ) {
        return տվյալ != null && տվյալ.length >= 14;
    }

    public static int 이더넷상위규약(byte[] տվյալ) {
        if (!이더넷틀인가(տվյալ)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(տվյալ, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] տվյալ, int Դիրք) {
        if (տվյալ == null || Դիրք < 0 || տվյալ.length - Դիրք < 20) {
            return false;
        }
        int տարբերակ_արժեք = (տվյալ[Դիրք] >>> 4) & 0xf;
        int Վերնագիր_տեւողություն = (տվյալ[Դիրք] & 0xf) * 4;
        return տարբերակ_արժեք == 4 && Վերնագիր_տեւողություն >= 20 && տվյալ.length - Դիրք >= Վերնագիր_տեւողություն;
    }

    private static void 범위확인(byte[] տվյալ, int Գործարկել, int տեւողություն_արժեք) {
        if (տվյալ == null || Գործարկել < 0 || տեւողություն_արժեք < 0 || Գործարկել > տվյալ.length - տեւողություն_արժեք) {
            throw new IllegalArgumentException("Ցանց_Շեղջ տվյալ 범위를 벗어났습니다.");
        }
    }
}

