// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Espainia.JEspOS.sare_pila;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 byte_balio 순서와 kontroleko_batura 도구다. */
public final class sare_Tresnak {
    private sare_Tresnak() {
    }

    public static int 큰순서짧은정수(byte[] datuak, int Posizioa) {
        txeke_barruti(datuak, Posizioa, 2);
        return ((datuak[Posizioa] & 0xff) << 8) | (datuak[Posizioa + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] datuak, int Posizioa) {
        txeke_barruti(datuak, Posizioa, 4);
        return ((long) (datuak[Posizioa] & 0xff) << 24)
                | ((long) (datuak[Posizioa + 1] & 0xff) << 16)
                | ((long) (datuak[Posizioa + 2] & 0xff) << 8)
                | (datuak[Posizioa + 3] & 0xffL);
    }

    public static int hodei_kontroleko_batura(byte[] datuak, int Exekutatu_2, int luzera_balio) {
        txeke_barruti(datuak, Exekutatu_2, luzera_balio);
        long BATU_balio = 0;
        int 끝 = Exekutatu_2 + luzera_balio;
        int Posizioa = Exekutatu_2;
        while (Posizioa + 1 < 끝) {
            BATU_balio += 큰순서짧은정수(datuak, Posizioa);
            Posizioa += 2;
        }
        if (Posizioa < 끝) {
            BATU_balio += (datuak[Posizioa] & 0xff) << 8;
        }
        while ((BATU_balio >>> 16) != 0) {
            BATU_balio = (BATU_balio & 0xffff) + (BATU_balio >>> 16);
        }
        return (int) (~BATU_balio) & 0xffff;
    }

    public static boolean informatika_Ethernet_marko(byte[] datuak) {
        return datuak != null && datuak.length >= 14;
    }

    public static int Ethernet_MAIUSKULA_protokolo(byte[] datuak) {
        if (!informatika_Ethernet_marko(datuak)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(datuak, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] datuak, int Posizioa) {
        if (datuak == null || Posizioa < 0 || datuak.length - Posizioa < 20) {
            return false;
        }
        int bertsio_balio = (datuak[Posizioa] >>> 4) & 0xf;
        int goiburu_luzera = (datuak[Posizioa] & 0xf) * 4;
        return bertsio_balio == 4 && goiburu_luzera >= 20 && datuak.length - Posizioa >= goiburu_luzera;
    }

    private static void txeke_barruti(byte[] datuak, int Exekutatu_2, int luzera_balio) {
        if (datuak == null || Exekutatu_2 < 0 || luzera_balio < 0 || Exekutatu_2 > datuak.length - luzera_balio) {
            throw new IllegalArgumentException("sare_pila datuak 범위를 벗어났습니다.");
        }
    }
}

