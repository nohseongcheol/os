// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** real_dados Java valor_do_contrato 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class pacote_teste {
    static int repetição_CONT_NÚM = 0;
    static void verificar(boolean VALOR) { if (!VALOR) throw new AssertionError("case " + repetição_CONT_NÚM); repetição_CONT_NÚM++; }
    static int soma_de_verificação(int[] VALOR, int iniciar, int duração_VALOR, int estado_inicial) {
        int SUM_VALOR = estado_inicial;
        for (int ÍNDICE = 0; ÍNDICE < duração_VALOR; ÍNDICE++) SUM_VALOR += VALOR[iniciar + ÍNDICE] << ((ÍNDICE & 1) == 0 ? 8 : 0);
        SUM_VALOR = (SUM_VALOR & 65535) + (SUM_VALOR >>> 16);
        SUM_VALOR = (SUM_VALOR & 65535) + (SUM_VALOR >>> 16);
        return ~SUM_VALOR & 65535;
    }
    static void Preparar(int duração_VALOR) {
        rede_pilha.TIRAR_Processo();
        verificar(rede_pilha.Abrir(5000) == 3);
        int[] quadro_ÍNDICE = rede_pilha.entrada_quadro;
        Arrays.fill(quadro_ÍNDICE, 0);
        for (int ÍNDICE = 0; ÍNDICE < 6; ÍNDICE++) quadro_ÍNDICE[ÍNDICE] = rede_driver.celular_email[ÍNDICE];
        rede_pilha.넣기16(quadro_ÍNDICE, 12, 0x0800);
        quadro_ÍNDICE[14] = 0x45; quadro_ÍNDICE[22] = 64; quadro_ÍNDICE[23] = 17;
        rede_pilha.넣기16(quadro_ÍNDICE, 16, 28 + duração_VALOR);
        rede_pilha.넣기32(quadro_ÍNDICE, 26, 0x0a000202); rede_pilha.넣기32(quadro_ÍNDICE, 30, rede_pilha.내주소);
        rede_pilha.넣기16(quadro_ÍNDICE, 34, 4321); rede_pilha.넣기16(quadro_ÍNDICE, 36, 5000); rede_pilha.넣기16(quadro_ÍNDICE, 38, duração_VALOR + 8);
        for (int ÍNDICE = 0; ÍNDICE < duração_VALOR; ÍNDICE++) quadro_ÍNDICE[42 + ÍNDICE] = ÍNDICE & 255;
        set_soma_de_verificação(duração_VALOR);
    }
    static void set_soma_de_verificação(int duração_VALOR) {
        int[] quadro_ÍNDICE = rede_pilha.entrada_quadro;
        rede_pilha.넣기16(quadro_ÍNDICE, 24, 0); rede_pilha.넣기16(quadro_ÍNDICE, 40, 0);
        rede_pilha.넣기16(quadro_ÍNDICE, 24, soma_de_verificação(quadro_ÍNDICE, 14, 20, 0));
        int estado_inicial = rede_pilha.가상머리합(rede_pilha.inteiro_32(quadro_ÍNDICE, 26), rede_pilha.내주소, duração_VALOR + 8);
        int SUM_VALOR = soma_de_verificação(quadro_ÍNDICE, 34, duração_VALOR + 8, estado_inicial);
        rede_pilha.넣기16(quadro_ÍNDICE, 40, SUM_VALOR == 0 ? 65535 : SUM_VALOR);
    }
    static void rejeitar_VALOR(int duração_VALOR) { rede_pilha.Processo_quadro(duração_VALOR); verificar(rede_pilha.RECEBER_duração[0] == -1); }
    public static void main(String[] argumentos) {
        for (int duração_VALOR : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Preparar(duração_VALOR); rede_pilha.Processo_quadro(duração_VALOR + 42);
            verificar(rede_pilha.RECEBER_duração[0] == duração_VALOR);
            verificar(rede_pilha.RECEBER_email[0] == 0x0a000202 && rede_pilha.RECEBER_número_da_porta[0] == 4321);
            for (int ÍNDICE = 0; ÍNDICE < duração_VALOR; ÍNDICE++) verificar(rede_pilha.RECEBER_dados[ÍNDICE] == (ÍNDICE & 255));
        }
        for (int duração_VALOR = 0; duração_VALOR < 42; duração_VALOR++) { Preparar(0); rejeitar_VALOR(duração_VALOR); }
        Preparar(1025); rejeitar_VALOR(1067);
        Preparar(2); rede_pilha.entrada_quadro[24] ^= 1; rejeitar_VALOR(44);
        Preparar(2); rede_pilha.entrada_quadro[42] ^= 1; rejeitar_VALOR(44);
        Preparar(2); rede_pilha.넣기16(rede_pilha.entrada_quadro, 38, 7); rejeitar_VALOR(44);
        Preparar(2); rede_pilha.넣기16(rede_pilha.entrada_quadro, 38, 65535); rejeitar_VALOR(44);
        Preparar(2); rede_pilha.entrada_quadro[14] = 0x4f; rejeitar_VALOR(44);
        Preparar(2); rede_pilha.entrada_quadro[14] = 0x44; rejeitar_VALOR(44);
        Preparar(2); rede_pilha.entrada_quadro[20] = 0x20; set_soma_de_verificação(2); rejeitar_VALOR(44);
        Preparar(2); rede_pilha.entrada_quadro[21] = 1; set_soma_de_verificação(2); rejeitar_VALOR(44);
        Preparar(2); rede_pilha.entrada_quadro[33] = 99; set_soma_de_verificação(2); rejeitar_VALOR(44);
        Preparar(2); rede_pilha.entrada_quadro[0] ^= 1; rejeitar_VALOR(44);
        Preparar(2); rede_pilha.entrada_quadro[23] = 6; set_soma_de_verificação(2); rejeitar_VALOR(44);
        Preparar(2); rede_pilha.넣기16(rede_pilha.entrada_quadro, 40, 0); rede_pilha.Processo_quadro(44); verificar(rede_pilha.RECEBER_duração[0] == 2);
        int[] resultado = new int[4];
        verificar(rede_pilha.receber(3, resultado, 1, 0) == -90);
        verificar(rede_pilha.receber(3, resultado, 4, 0) == -11);
        Preparar(2); rede_pilha.Processo_quadro(44); int discard_VALOR = rede_pilha.폐기수;
        rede_pilha.Processo_quadro(44); verificar(rede_pilha.폐기수 == discard_VALOR + 1);
        rede_pilha.TIRAR_Processo(); verificar(rede_pilha.Abrir(5000) == 3);
        verificar(rede_pilha.Abrir(5000) == -98); verificar(rede_pilha.Abrir(0) == 4);
        verificar(rede_pilha.Abrir(0) == 5); verificar(rede_pilha.Abrir(0) == 6); verificar(rede_pilha.Abrir(0) == -24);
        verificar(rede_pilha.Fechar(4) == 0); verificar(rede_pilha.Fechar(4) == -9);
        rede_pilha.찾은주소 = rede_pilha.gateway_VALOR;
        verificar(rede_pilha.enviar(3, rede_pilha.gateway_VALOR, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = rede_driver.recente_VALOR;
        verificar(soma_de_verificação(보냄, 14, 20, 0) == 0);
        verificar(soma_de_verificação(보냄, 34, 11, rede_pilha.가상머리합(rede_pilha.내주소, rede_pilha.gateway_VALOR, 11)) == 0);
        verificar(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + repetição_CONT_NÚM + " assertions");
    }
}
