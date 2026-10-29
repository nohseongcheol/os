// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Сербія.JSrbOS.мережа_Стіс;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 байт_значення 순서와 контрольна_сума 도구다. */
public final class мережа_Інструменти {
    private мережа_Інструменти() {
    }

    public static int 큰순서짧은정수(byte[] дані, int позиція) {
        перевіряти_діапазон(дані, позиція, 2);
        return ((дані[позиція] & 0xff) << 8) | (дані[позиція + 1] & 0xff);
    }

    public static long із_зворотним_порядком_байтів_ціле_число(byte[] дані, int позиція) {
        перевіряти_діапазон(дані, позиція, 4);
        return ((long) (дані[позиція] & 0xff) << 24)
                | ((long) (дані[позиція + 1] & 0xff) << 16)
                | ((long) (дані[позиція + 2] & 0xff) << 8)
                | (дані[позиція + 3] & 0xffL);
    }

    public static int хмара_контрольна_сума(byte[] дані, int запустити, int 길이) {
        перевіряти_діапазон(дані, запустити, 길이);
        long 합 = 0;
        int 끝 = запустити + 길이;
        int позиція = запустити;
        while (позиція + 1 < 끝) {
            합 += 큰순서짧은정수(дані, позиція);
            позиція += 2;
        }
        if (позиція < 끝) {
            합 += (дані[позиція] & 0xff) << 8;
        }
        while ((합 >>> 16) != 0) {
            합 = (합 & 0xffff) + (합 >>> 16);
        }
        return (int) (~합) & 0xffff;
    }

    public static boolean 이더넷틀인가(byte[] дані) {
        return дані != null && дані.length >= 14;
    }

    public static int 이더넷상위규약(byte[] дані) {
        if (!이더넷틀인가(дані)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(дані, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] дані, int позиція) {
        if (дані == null || позиція < 0 || дані.length - позиція < 20) {
            return false;
        }
        int версія_значення = (дані[позиція] >>> 4) & 0xf;
        int 머리길이 = (дані[позиція] & 0xf) * 4;
        return версія_значення == 4 && 머리길이 >= 20 && дані.length - позиція >= 머리길이;
    }

    private static void перевіряти_діапазон(byte[] дані, int запустити, int 길이) {
        if (дані == null || запустити < 0 || 길이 < 0 || запустити > дані.length - 길이) {
            throw new IllegalArgumentException("мережа_Стіс дані 범위를 벗어났습니다.");
        }
    }
}

