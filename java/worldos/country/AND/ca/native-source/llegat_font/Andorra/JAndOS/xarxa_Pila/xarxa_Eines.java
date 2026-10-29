// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Andorra.JAndOS.xarxa_Pila;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 byte_VALOR 순서와 suma_de_comprovació 도구다. */
public final class xarxa_Eines {
    private xarxa_Eines() {
    }

    public static int 큰순서짧은정수(byte[] dades, int Posició) {
        xec_interval(dades, Posició, 2);
        return ((dades[Posició] & 0xff) << 8) | (dades[Posició + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] dades, int Posició) {
        xec_interval(dades, Posició, 4);
        return ((long) (dades[Posició] & 0xff) << 24)
                | ((long) (dades[Posició + 1] & 0xff) << 16)
                | ((long) (dades[Posició + 2] & 0xff) << 8)
                | (dades[Posició + 3] & 0xffL);
    }

    public static int núvol_suma_de_comprovació(byte[] dades, int Executa_2, int durada_VALOR) {
        xec_interval(dades, Executa_2, durada_VALOR);
        long SUMA_VALOR = 0;
        int 끝 = Executa_2 + durada_VALOR;
        int Posició = Executa_2;
        while (Posició + 1 < 끝) {
            SUMA_VALOR += 큰순서짧은정수(dades, Posició);
            Posició += 2;
        }
        if (Posició < 끝) {
            SUMA_VALOR += (dades[Posició] & 0xff) << 8;
        }
        while ((SUMA_VALOR >>> 16) != 0) {
            SUMA_VALOR = (SUMA_VALOR & 0xffff) + (SUMA_VALOR >>> 16);
        }
        return (int) (~SUMA_VALOR) & 0xffff;
    }

    public static boolean tecnologies_de_la_informació_Ethernet_marc(byte[] dades) {
        return dades != null && dades.length >= 14;
    }

    public static int Ethernet_MAJUSC_protocol(byte[] dades) {
        if (!tecnologies_de_la_informació_Ethernet_marc(dades)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(dades, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] dades, int Posició) {
        if (dades == null || Posició < 0 || dades.length - Posició < 20) {
            return false;
        }
        int versió_VALOR = (dades[Posició] >>> 4) & 0xf;
        int Capçalera_durada = (dades[Posició] & 0xf) * 4;
        return versió_VALOR == 4 && Capçalera_durada >= 20 && dades.length - Posició >= Capçalera_durada;
    }

    private static void xec_interval(byte[] dades, int Executa_2, int durada_VALOR) {
        if (dades == null || Executa_2 < 0 || durada_VALOR < 0 || Executa_2 > dades.length - durada_VALOR) {
            throw new IllegalArgumentException("xarxa_Pila dades 범위를 벗어났습니다.");
        }
    }
}

