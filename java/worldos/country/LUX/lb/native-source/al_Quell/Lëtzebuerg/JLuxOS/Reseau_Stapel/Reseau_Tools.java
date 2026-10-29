// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lëtzebuerg.JLuxOS.Reseau_Stapel;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 Byte_VALUE 순서와 검사합 도구다. */
public final class Reseau_Tools {
    private Reseau_Tools() {
    }

    public static int 큰순서짧은정수(byte[] Daten, int positionéieren) {
        범위확인(Daten, positionéieren, 2);
        return ((Daten[positionéieren] & 0xff) << 8) | (Daten[positionéieren + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] Daten, int positionéieren) {
        범위확인(Daten, positionéieren, 4);
        return ((long) (Daten[positionéieren] & 0xff) << 24)
                | ((long) (Daten[positionéieren + 1] & 0xff) << 16)
                | ((long) (Daten[positionéieren + 2] & 0xff) << 8)
                | (Daten[positionéieren + 3] & 0xffL);
    }

    public static int 인터넷검사합(byte[] Daten, int Laf, int Längt_VALUE) {
        범위확인(Daten, Laf, Längt_VALUE);
        long SUM_VALUE = 0;
        int 끝 = Laf + Längt_VALUE;
        int positionéieren = Laf;
        while (positionéieren + 1 < 끝) {
            SUM_VALUE += 큰순서짧은정수(Daten, positionéieren);
            positionéieren += 2;
        }
        if (positionéieren < 끝) {
            SUM_VALUE += (Daten[positionéieren] & 0xff) << 8;
        }
        while ((SUM_VALUE >>> 16) != 0) {
            SUM_VALUE = (SUM_VALUE & 0xffff) + (SUM_VALUE >>> 16);
        }
        return (int) (~SUM_VALUE) & 0xffff;
    }

    public static boolean 이더넷틀인가(byte[] Daten) {
        return Daten != null && Daten.length >= 14;
    }

    public static int Ethernet_UPPER_Protokoll(byte[] Daten) {
        if (!이더넷틀인가(Daten)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(Daten, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] Daten, int positionéieren) {
        if (Daten == null || positionéieren < 0 || Daten.length - positionéieren < 20) {
            return false;
        }
        int Versioun_VALUE = (Daten[positionéieren] >>> 4) & 0xf;
        int En_tête_Längt = (Daten[positionéieren] & 0xf) * 4;
        return Versioun_VALUE == 4 && En_tête_Längt >= 20 && Daten.length - positionéieren >= En_tête_Längt;
    }

    private static void 범위확인(byte[] Daten, int Laf, int Längt_VALUE) {
        if (Daten == null || Laf < 0 || Längt_VALUE < 0 || Laf > Daten.length - Längt_VALUE) {
            throw new IllegalArgumentException("Reseau_Stapel Daten 범위를 벗어났습니다.");
        }
    }
}

