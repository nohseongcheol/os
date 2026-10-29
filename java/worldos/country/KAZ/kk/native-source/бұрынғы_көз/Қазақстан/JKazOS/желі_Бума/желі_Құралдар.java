// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Қазақстан.JKazOS.желі_Бума;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 байт_мән 순서와 тексеру_қорытындысы 도구다. */
public final class желі_Құралдар {
    private желі_Құралдар() {
    }

    public static int 큰순서짧은정수(byte[] деректер, int Орны) {
        чек_ауқым(деректер, Орны, 2);
        return ((деректер[Орны] & 0xff) << 8) | (деректер[Орны + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] деректер, int Орны) {
        чек_ауқым(деректер, Орны, 4);
        return ((long) (деректер[Орны] & 0xff) << 24)
                | ((long) (деректер[Орны + 1] & 0xff) << 16)
                | ((long) (деректер[Орны + 2] & 0xff) << 8)
                | (деректер[Орны + 3] & 0xffL);
    }

    public static int бұлт_тексеру_қорытындысы(byte[] деректер, int Орындау_2, int ұзындық_мән) {
        чек_ауқым(деректер, Орындау_2, ұзындық_мән);
        long 합 = 0;
        int 끝 = Орындау_2 + ұзындық_мән;
        int Орны = Орындау_2;
        while (Орны + 1 < 끝) {
            합 += 큰순서짧은정수(деректер, Орны);
            Орны += 2;
        }
        if (Орны < 끝) {
            합 += (деректер[Орны] & 0xff) << 8;
        }
        while ((합 >>> 16) != 0) {
            합 = (합 & 0xffff) + (합 >>> 16);
        }
        return (int) (~합) & 0xffff;
    }

    public static boolean 이더넷틀인가(byte[] деректер) {
        return деректер != null && деректер.length >= 14;
    }

    public static int 이더넷상위규약(byte[] деректер) {
        if (!이더넷틀인가(деректер)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(деректер, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] деректер, int Орны) {
        if (деректер == null || Орны < 0 || деректер.length - Орны < 20) {
            return false;
        }
        int нұсқа_мән = (деректер[Орны] >>> 4) & 0xf;
        int Тақырып_ұзындық = (деректер[Орны] & 0xf) * 4;
        return нұсқа_мән == 4 && Тақырып_ұзындық >= 20 && деректер.length - Орны >= Тақырып_ұзындық;
    }

    private static void чек_ауқым(byte[] деректер, int Орындау_2, int ұзындық_мән) {
        if (деректер == null || Орындау_2 < 0 || ұзындық_мән < 0 || Орындау_2 > деректер.length - ұзындық_мән) {
            throw new IllegalArgumentException("желі_Бума деректер 범위를 벗어났습니다.");
        }
    }
}

