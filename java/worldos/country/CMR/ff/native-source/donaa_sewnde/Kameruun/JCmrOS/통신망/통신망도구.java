// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Kameruun.JCmrOS.통신망;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 oktee_njaru 순서와 검사합 도구다. */
public final class 통신망도구 {
    private 통신망도구() {
    }

    public static int 큰순서짧은정수(byte[] keɓe, int 위치) {
        범위확인(keɓe, 위치, 2);
        return ((keɓe[위치] & 0xff) << 8) | (keɓe[위치 + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] keɓe, int 위치) {
        범위확인(keɓe, 위치, 4);
        return ((long) (keɓe[위치] & 0xff) << 24)
                | ((long) (keɓe[위치 + 1] & 0xff) << 16)
                | ((long) (keɓe[위치 + 2] & 0xff) << 8)
                | (keɓe[위치 + 3] & 0xffL);
    }

    public static int 인터넷검사합(byte[] keɓe, int huutoraade, int njuuteendi_njaru) {
        범위확인(keɓe, huutoraade, njuuteendi_njaru);
        long 합 = 0;
        int 끝 = huutoraade + njuuteendi_njaru;
        int 위치 = huutoraade;
        while (위치 + 1 < 끝) {
            합 += 큰순서짧은정수(keɓe, 위치);
            위치 += 2;
        }
        if (위치 < 끝) {
            합 += (keɓe[위치] & 0xff) << 8;
        }
        while ((합 >>> 16) != 0) {
            합 = (합 & 0xffff) + (합 >>> 16);
        }
        return (int) (~합) & 0xffff;
    }

    public static boolean 이더넷틀인가(byte[] keɓe) {
        return keɓe != null && keɓe.length >= 14;
    }

    public static int 이더넷상위규약(byte[] keɓe) {
        if (!이더넷틀인가(keɓe)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(keɓe, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] keɓe, int 위치) {
        if (keɓe == null || 위치 < 0 || keɓe.length - 위치 < 20) {
            return false;
        }
        int yamre_njaru = (keɓe[위치] >>> 4) & 0xf;
        int meetalol_hello_njuuteendi = (keɓe[위치] & 0xf) * 4;
        return yamre_njaru == 4 && meetalol_hello_njuuteendi >= 20 && keɓe.length - 위치 >= meetalol_hello_njuuteendi;
    }

    private static void 범위확인(byte[] keɓe, int huutoraade, int njuuteendi_njaru) {
        if (keɓe == null || huutoraade < 0 || njuuteendi_njaru < 0 || huutoraade > keɓe.length - njuuteendi_njaru) {
            throw new IllegalArgumentException("통신망 keɓe 범위를 벗어났습니다.");
        }
    }
}

