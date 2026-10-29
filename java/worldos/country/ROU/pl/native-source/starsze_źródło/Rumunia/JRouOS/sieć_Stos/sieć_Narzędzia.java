// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Rumunia.JRouOS.sieć_Stos;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 bajt_WARTOŚĆ 순서와 suma_kontrolna 도구다. */
public final class sieć_Narzędzia {
    private sieć_Narzędzia() {
    }

    public static int 큰순서짧은정수(byte[] dane, int pozycja) {
        czek_zakres(dane, pozycja, 2);
        return ((dane[pozycja] & 0xff) << 8) | (dane[pozycja + 1] & 0xff);
    }

    public static long big_endian_liczba_całkowita(byte[] dane, int pozycja) {
        czek_zakres(dane, pozycja, 4);
        return ((long) (dane[pozycja] & 0xff) << 24)
                | ((long) (dane[pozycja + 1] & 0xff) << 16)
                | ((long) (dane[pozycja + 2] & 0xff) << 8)
                | (dane[pozycja + 3] & 0xffL);
    }

    public static int chmura_suma_kontrolna(byte[] dane, int Uruchom_2, int długość_WARTOŚĆ) {
        czek_zakres(dane, Uruchom_2, długość_WARTOŚĆ);
        long SUMA_WARTOŚĆ = 0;
        int 끝 = Uruchom_2 + długość_WARTOŚĆ;
        int pozycja = Uruchom_2;
        while (pozycja + 1 < 끝) {
            SUMA_WARTOŚĆ += 큰순서짧은정수(dane, pozycja);
            pozycja += 2;
        }
        if (pozycja < 끝) {
            SUMA_WARTOŚĆ += (dane[pozycja] & 0xff) << 8;
        }
        while ((SUMA_WARTOŚĆ >>> 16) != 0) {
            SUMA_WARTOŚĆ = (SUMA_WARTOŚĆ & 0xffff) + (SUMA_WARTOŚĆ >>> 16);
        }
        return (int) (~SUMA_WARTOŚĆ) & 0xffff;
    }

    public static boolean systemy_informacyjne_Ethernet_kadr(byte[] dane) {
        return dane != null && dane.length >= 14;
    }

    public static int Ethernet_LITERY_WIELKIE_protokół(byte[] dane) {
        if (!systemy_informacyjne_Ethernet_kadr(dane)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(dane, 12);
    }

    public static boolean systemy_informacyjne_IPV_4_protokół(byte[] dane, int pozycja) {
        if (dane == null || pozycja < 0 || dane.length - pozycja < 20) {
            return false;
        }
        int wersja_WARTOŚĆ = (dane[pozycja] >>> 4) & 0xf;
        int Nagłówek_długość = (dane[pozycja] & 0xf) * 4;
        return wersja_WARTOŚĆ == 4 && Nagłówek_długość >= 20 && dane.length - pozycja >= Nagłówek_długość;
    }

    private static void czek_zakres(byte[] dane, int Uruchom_2, int długość_WARTOŚĆ) {
        if (dane == null || Uruchom_2 < 0 || długość_WARTOŚĆ < 0 || Uruchom_2 > dane.length - długość_WARTOŚĆ) {
            throw new IllegalArgumentException("sieć_Stos dane 범위를 벗어났습니다.");
        }
    }
}

