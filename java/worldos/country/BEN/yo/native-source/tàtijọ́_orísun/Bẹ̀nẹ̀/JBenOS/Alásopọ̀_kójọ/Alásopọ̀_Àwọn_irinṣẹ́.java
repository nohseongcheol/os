// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Bẹ̀nẹ̀.JBenOS.Alásopọ̀_kójọ;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 báìtì_iye 순서와 검사합 도구다. */
public final class Alásopọ̀_Àwọn_irinṣẹ́ {
    private Alásopọ̀_Àwọn_irinṣẹ́() {
    }

    public static int 큰순서짧은정수(byte[] détà, int 위치) {
        범위확인(détà, 위치, 2);
        return ((détà[위치] & 0xff) << 8) | (détà[위치 + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] détà, int 위치) {
        범위확인(détà, 위치, 4);
        return ((long) (détà[위치] & 0xff) << 24)
                | ((long) (détà[위치 + 1] & 0xff) << 16)
                | ((long) (détà[위치 + 2] & 0xff) << 8)
                | (détà[위치 + 3] & 0xffL);
    }

    public static int 인터넷검사합(byte[] détà, int Rọ́ọ̀nù, int gígùn_iye) {
        범위확인(détà, Rọ́ọ̀nù, gígùn_iye);
        long 합 = 0;
        int 끝 = Rọ́ọ̀nù + gígùn_iye;
        int 위치 = Rọ́ọ̀nù;
        while (위치 + 1 < 끝) {
            합 += 큰순서짧은정수(détà, 위치);
            위치 += 2;
        }
        if (위치 < 끝) {
            합 += (détà[위치] & 0xff) << 8;
        }
        while ((합 >>> 16) != 0) {
            합 = (합 & 0xffff) + (합 >>> 16);
        }
        return (int) (~합) & 0xffff;
    }

    public static boolean 이더넷틀인가(byte[] détà) {
        return détà != null && détà.length >= 14;
    }

    public static int 이더넷상위규약(byte[] détà) {
        if (!이더넷틀인가(détà)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(détà, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] détà, int 위치) {
        if (détà == null || 위치 < 0 || détà.length - 위치 < 20) {
            return false;
        }
        int ẹ̀yà_iye = (détà[위치] >>> 4) & 0xf;
        int àkọlé_gígùn = (détà[위치] & 0xf) * 4;
        return ẹ̀yà_iye == 4 && àkọlé_gígùn >= 20 && détà.length - 위치 >= àkọlé_gígùn;
    }

    private static void 범위확인(byte[] détà, int Rọ́ọ̀nù, int gígùn_iye) {
        if (détà == null || Rọ́ọ̀nù < 0 || gígùn_iye < 0 || Rọ́ọ̀nù > détà.length - gígùn_iye) {
            throw new IllegalArgumentException("Alásopọ̀_kójọ détà 범위를 벗어났습니다.");
        }
    }
}

