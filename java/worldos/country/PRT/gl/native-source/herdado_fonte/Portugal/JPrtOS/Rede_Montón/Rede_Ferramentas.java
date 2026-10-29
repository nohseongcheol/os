// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Portugal.JPrtOS.Rede_Montón;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 byte_VALOR 순서와 suma_de_comprobación 도구다. */
public final class Rede_Ferramentas {
    private Rede_Ferramentas() {
    }

    public static int 큰순서짧은정수(byte[] datos, int Posición) {
        cheque_intervalo(datos, Posición, 2);
        return ((datos[Posición] & 0xff) << 8) | (datos[Posición + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] datos, int Posición) {
        cheque_intervalo(datos, Posición, 4);
        return ((long) (datos[Posición] & 0xff) << 24)
                | ((long) (datos[Posición + 1] & 0xff) << 16)
                | ((long) (datos[Posición + 2] & 0xff) << 8)
                | (datos[Posición + 3] & 0xffL);
    }

    public static int nube_suma_de_comprobación(byte[] datos, int Executar_2, int duración_VALOR) {
        cheque_intervalo(datos, Executar_2, duración_VALOR);
        long SUMA_VALOR = 0;
        int 끝 = Executar_2 + duración_VALOR;
        int Posición = Executar_2;
        while (Posición + 1 < 끝) {
            SUMA_VALOR += 큰순서짧은정수(datos, Posición);
            Posición += 2;
        }
        if (Posición < 끝) {
            SUMA_VALOR += (datos[Posición] & 0xff) << 8;
        }
        while ((SUMA_VALOR >>> 16) != 0) {
            SUMA_VALOR = (SUMA_VALOR & 0xffff) + (SUMA_VALOR >>> 16);
        }
        return (int) (~SUMA_VALOR) & 0xffff;
    }

    public static boolean Tecnoloxía_da_información_TI_Ethernet_marco(byte[] datos) {
        return datos != null && datos.length >= 14;
    }

    public static int Ethernet_MAIÚSCULA_protocolo(byte[] datos) {
        if (!Tecnoloxía_da_información_TI_Ethernet_marco(datos)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(datos, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] datos, int Posición) {
        if (datos == null || Posición < 0 || datos.length - Posición < 20) {
            return false;
        }
        int versión_VALOR = (datos[Posición] >>> 4) & 0xf;
        int Cabeceira_duración = (datos[Posición] & 0xf) * 4;
        return versión_VALOR == 4 && Cabeceira_duración >= 20 && datos.length - Posición >= Cabeceira_duración;
    }

    private static void cheque_intervalo(byte[] datos, int Executar_2, int duración_VALOR) {
        if (datos == null || Executar_2 < 0 || duración_VALOR < 0 || Executar_2 > datos.length - duración_VALOR) {
            throw new IllegalArgumentException("Rede_Montón datos 범위를 벗어났습니다.");
        }
    }
}

