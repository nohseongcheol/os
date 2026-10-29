// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Россия.JRusOS.Челтәр_Стәк;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 байт_VALUE 순서와 검사합 도구다. */
public final class Челтәр_Кораллар {
    private Челтәр_Кораллар() {
    }

    public static int 큰순서짧은정수(byte[] мәгълүмат, int урнаштыру) {
        범위확인(мәгълүмат, урнаштыру, 2);
        return ((мәгълүмат[урнаштыру] & 0xff) << 8) | (мәгълүмат[урнаштыру + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] мәгълүмат, int урнаштыру) {
        범위확인(мәгълүмат, урнаштыру, 4);
        return ((long) (мәгълүмат[урнаштыру] & 0xff) << 24)
                | ((long) (мәгълүмат[урнаштыру + 1] & 0xff) << 16)
                | ((long) (мәгълүмат[урнаштыру + 2] & 0xff) << 8)
                | (мәгълүмат[урнаштыру + 3] & 0xffL);
    }

    public static int 인터넷검사합(byte[] мәгълүмат, int эшләтү, int озынлык_VALUE) {
        범위확인(мәгълүмат, эшләтү, озынлык_VALUE);
        long SUM_VALUE = 0;
        int 끝 = эшләтү + озынлык_VALUE;
        int урнаштыру = эшләтү;
        while (урнаштыру + 1 < 끝) {
            SUM_VALUE += 큰순서짧은정수(мәгълүмат, урнаштыру);
            урнаштыру += 2;
        }
        if (урнаштыру < 끝) {
            SUM_VALUE += (мәгълүмат[урнаштыру] & 0xff) << 8;
        }
        while ((SUM_VALUE >>> 16) != 0) {
            SUM_VALUE = (SUM_VALUE & 0xffff) + (SUM_VALUE >>> 16);
        }
        return (int) (~SUM_VALUE) & 0xffff;
    }

    public static boolean 이더넷틀인가(byte[] мәгълүмат) {
        return мәгълүмат != null && мәгълүмат.length >= 14;
    }

    public static int Ethernet_UPPER_протокол(byte[] мәгълүмат) {
        if (!이더넷틀인가(мәгълүмат)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(мәгълүмат, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] мәгълүмат, int урнаштыру) {
        if (мәгълүмат == null || урнаштыру < 0 || мәгълүмат.length - урнаштыру < 20) {
            return false;
        }
        int версия_VALUE = (мәгълүмат[урнаштыру] >>> 4) & 0xf;
        int Башлама_озынлык = (мәгълүмат[урнаштыру] & 0xf) * 4;
        return версия_VALUE == 4 && Башлама_озынлык >= 20 && мәгълүмат.length - урнаштыру >= Башлама_озынлык;
    }

    private static void 범위확인(byte[] мәгълүмат, int эшләтү, int озынлык_VALUE) {
        if (мәгълүмат == null || эшләтү < 0 || озынлык_VALUE < 0 || эшләтү > мәгълүмат.length - озынлык_VALUE) {
            throw new IllegalArgumentException("Челтәр_Стәк мәгълүмат 범위를 벗어났습니다.");
        }
    }
}

