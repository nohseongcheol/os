// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Северна_Македонија.JMkdOS.Мрежа_Купче;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 бајт_VALUE 순서와 контролна_сума 도구다. */
public final class Мрежа_Алатки {
    private Мрежа_Алатки() {
    }

    public static int 큰순서짧은정수(byte[] податоци, int Позиција) {
        범위확인(податоци, Позиција, 2);
        return ((податоци[Позиција] & 0xff) << 8) | (податоци[Позиција + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] податоци, int Позиција) {
        범위확인(податоци, Позиција, 4);
        return ((long) (податоци[Позиција] & 0xff) << 24)
                | ((long) (податоци[Позиција + 1] & 0xff) << 16)
                | ((long) (податоци[Позиција + 2] & 0xff) << 8)
                | (податоци[Позиција + 3] & 0xffL);
    }

    public static int облак_контролна_сума(byte[] податоци, int Изврши_2, int должина_VALUE) {
        범위확인(податоци, Изврши_2, должина_VALUE);
        long SUM_VALUE = 0;
        int 끝 = Изврши_2 + должина_VALUE;
        int Позиција = Изврши_2;
        while (Позиција + 1 < 끝) {
            SUM_VALUE += 큰순서짧은정수(податоци, Позиција);
            Позиција += 2;
        }
        if (Позиција < 끝) {
            SUM_VALUE += (податоци[Позиција] & 0xff) << 8;
        }
        while ((SUM_VALUE >>> 16) != 0) {
            SUM_VALUE = (SUM_VALUE & 0xffff) + (SUM_VALUE >>> 16);
        }
        return (int) (~SUM_VALUE) & 0xffff;
    }

    public static boolean информатичка_технологија_Етернет_врами(byte[] податоци) {
        return податоци != null && податоци.length >= 14;
    }

    public static int Етернет_UPPER_протокол(byte[] податоци) {
        if (!информатичка_технологија_Етернет_врами(податоци)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(податоци, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] податоци, int Позиција) {
        if (податоци == null || Позиција < 0 || податоци.length - Позиција < 20) {
            return false;
        }
        int верзија_VALUE = (податоци[Позиција] >>> 4) & 0xf;
        int Заглавие_должина = (податоци[Позиција] & 0xf) * 4;
        return верзија_VALUE == 4 && Заглавие_должина >= 20 && податоци.length - Позиција >= Заглавие_должина;
    }

    private static void 범위확인(byte[] податоци, int Изврши_2, int должина_VALUE) {
        if (податоци == null || Изврши_2 < 0 || должина_VALUE < 0 || Изврши_2 > податоци.length - должина_VALUE) {
            throw new IllegalArgumentException("Мрежа_Купче податоци 범위를 벗어났습니다.");
        }
    }
}

