// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Angola.JAgoOS.rede_pilha;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 byte_VALOR 순서와 soma_de_verificação 도구다. */
public final class rede_Ferramentas {
    private rede_Ferramentas() {
    }

    public static int 큰순서짧은정수(byte[] dados, int posição) {
        cheque_alcance(dados, posição, 2);
        return ((dados[posição] & 0xff) << 8) | (dados[posição + 1] & 0xff);
    }

    public static long big_endian_inteiro(byte[] dados, int posição) {
        cheque_alcance(dados, posição, 4);
        return ((long) (dados[posição] & 0xff) << 24)
                | ((long) (dados[posição + 1] & 0xff) << 16)
                | ((long) (dados[posição + 2] & 0xff) << 8)
                | (dados[posição + 3] & 0xffL);
    }

    public static int malha_soma_de_verificação(byte[] dados, int iniciar, int duração_VALOR) {
        cheque_alcance(dados, iniciar, duração_VALOR);
        long SUM_VALOR = 0;
        int 끝 = iniciar + duração_VALOR;
        int posição = iniciar;
        while (posição + 1 < 끝) {
            SUM_VALOR += 큰순서짧은정수(dados, posição);
            posição += 2;
        }
        if (posição < 끝) {
            SUM_VALOR += (dados[posição] & 0xff) << 8;
        }
        while ((SUM_VALOR >>> 16) != 0) {
            SUM_VALOR = (SUM_VALOR & 0xffff) + (SUM_VALOR >>> 16);
        }
        return (int) (~SUM_VALOR) & 0xffff;
    }

    public static boolean TI_Ethernet_quadro(byte[] dados) {
        return dados != null && dados.length >= 14;
    }

    public static int Ethernet_MAIÚSCULA_protocolo(byte[] dados) {
        if (!TI_Ethernet_quadro(dados)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(dados, 12);
    }

    public static boolean TI_IPV_4_protocolo(byte[] dados, int posição) {
        if (dados == null || posição < 0 || dados.length - posição < 20) {
            return false;
        }
        int versão_VALOR = (dados[posição] >>> 4) & 0xf;
        int Cabeçalho_duração = (dados[posição] & 0xf) * 4;
        return versão_VALOR == 4 && Cabeçalho_duração >= 20 && dados.length - posição >= Cabeçalho_duração;
    }

    private static void cheque_alcance(byte[] dados, int iniciar, int duração_VALOR) {
        if (dados == null || iniciar < 0 || duração_VALOR < 0 || iniciar > dados.length - duração_VALOR) {
            throw new IllegalArgumentException("rede_pilha dados 범위를 벗어났습니다.");
        }
    }
}

