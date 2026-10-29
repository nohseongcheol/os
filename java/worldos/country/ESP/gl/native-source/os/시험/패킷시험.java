// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** real_datos Java caso_VALOR 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class 패킷시험 {
    static int 횟수 = 0;
    static void verificar(boolean VALOR) { if (!VALOR) throw new AssertionError("case " + 횟수); 횟수++; }
    static int suma_de_comprobación(int[] VALOR, int Executar_2, int duración_VALOR, int 초기) {
        int SUMA_VALOR = 초기;
        for (int ÍNDICE = 0; ÍNDICE < duración_VALOR; ÍNDICE++) SUMA_VALOR += VALOR[Executar_2 + ÍNDICE] << ((ÍNDICE & 1) == 0 ? 8 : 0);
        SUMA_VALOR = (SUMA_VALOR & 65535) + (SUMA_VALOR >>> 16);
        SUMA_VALOR = (SUMA_VALOR & 65535) + (SUMA_VALOR >>> 16);
        return ~SUMA_VALOR & 65535;
    }
    static void 준비(int duración_VALOR) {
        Rede_Montón.Limpo_Proceso();
        verificar(Rede_Montón.Abrir(5000) == 3);
        int[] marco_ÍNDICE = Rede_Montón.입력틀;
        Arrays.fill(marco_ÍNDICE, 0);
        for (int ÍNDICE = 0; ÍNDICE < 6; ÍNDICE++) marco_ÍNDICE[ÍNDICE] = Rede_controlador.dispositivo_ENDEREZO[ÍNDICE];
        Rede_Montón.넣기16(marco_ÍNDICE, 12, 0x0800);
        marco_ÍNDICE[14] = 0x45; marco_ÍNDICE[22] = 64; marco_ÍNDICE[23] = 17;
        Rede_Montón.넣기16(marco_ÍNDICE, 16, 28 + duración_VALOR);
        Rede_Montón.넣기32(marco_ÍNDICE, 26, 0x0a000202); Rede_Montón.넣기32(marco_ÍNDICE, 30, Rede_Montón.내주소);
        Rede_Montón.넣기16(marco_ÍNDICE, 34, 4321); Rede_Montón.넣기16(marco_ÍNDICE, 36, 5000); Rede_Montón.넣기16(marco_ÍNDICE, 38, duración_VALOR + 8);
        for (int ÍNDICE = 0; ÍNDICE < duración_VALOR; ÍNDICE++) marco_ÍNDICE[42 + ÍNDICE] = ÍNDICE & 255;
        conxunto_suma_de_comprobación(duración_VALOR);
    }
    static void conxunto_suma_de_comprobación(int duración_VALOR) {
        int[] marco_ÍNDICE = Rede_Montón.입력틀;
        Rede_Montón.넣기16(marco_ÍNDICE, 24, 0); Rede_Montón.넣기16(marco_ÍNDICE, 40, 0);
        Rede_Montón.넣기16(marco_ÍNDICE, 24, suma_de_comprobación(marco_ÍNDICE, 14, 20, 0));
        int 초기 = Rede_Montón.가상머리합(Rede_Montón.número_enteiro_32(marco_ÍNDICE, 26), Rede_Montón.내주소, duración_VALOR + 8);
        int SUMA_VALOR = suma_de_comprobación(marco_ÍNDICE, 34, duración_VALOR + 8, 초기);
        Rede_Montón.넣기16(marco_ÍNDICE, 40, SUMA_VALOR == 0 ? 65535 : SUMA_VALOR);
    }
    static void rexeitar_VALOR_e3ecc00b(int duración_VALOR) { Rede_Montón.Proceso_marco(duración_VALOR); verificar(Rede_Montón.RECIBIDO_duración[0] == -1); }
    public static void main(String[] Argumentos) {
        for (int duración_VALOR : new int[]{0, 1, 2, 7, 1023, 1024}) {
            준비(duración_VALOR); Rede_Montón.Proceso_marco(duración_VALOR + 42);
            verificar(Rede_Montón.RECIBIDO_duración[0] == duración_VALOR);
            verificar(Rede_Montón.RECIBIDO_ENDEREZO[0] == 0x0a000202 && Rede_Montón.RECIBIDO_número_do_porto[0] == 4321);
            for (int ÍNDICE = 0; ÍNDICE < duración_VALOR; ÍNDICE++) verificar(Rede_Montón.RECIBIDO_datos[ÍNDICE] == (ÍNDICE & 255));
        }
        for (int duración_VALOR = 0; duración_VALOR < 42; duración_VALOR++) { 준비(0); rexeitar_VALOR_e3ecc00b(duración_VALOR); }
        준비(1025); rexeitar_VALOR_e3ecc00b(1067);
        준비(2); Rede_Montón.입력틀[24] ^= 1; rexeitar_VALOR_e3ecc00b(44);
        준비(2); Rede_Montón.입력틀[42] ^= 1; rexeitar_VALOR_e3ecc00b(44);
        준비(2); Rede_Montón.넣기16(Rede_Montón.입력틀, 38, 7); rexeitar_VALOR_e3ecc00b(44);
        준비(2); Rede_Montón.넣기16(Rede_Montón.입력틀, 38, 65535); rexeitar_VALOR_e3ecc00b(44);
        준비(2); Rede_Montón.입력틀[14] = 0x4f; rexeitar_VALOR_e3ecc00b(44);
        준비(2); Rede_Montón.입력틀[14] = 0x44; rexeitar_VALOR_e3ecc00b(44);
        준비(2); Rede_Montón.입력틀[20] = 0x20; conxunto_suma_de_comprobación(2); rexeitar_VALOR_e3ecc00b(44);
        준비(2); Rede_Montón.입력틀[21] = 1; conxunto_suma_de_comprobación(2); rexeitar_VALOR_e3ecc00b(44);
        준비(2); Rede_Montón.입력틀[33] = 99; conxunto_suma_de_comprobación(2); rexeitar_VALOR_e3ecc00b(44);
        준비(2); Rede_Montón.입력틀[0] ^= 1; rexeitar_VALOR_e3ecc00b(44);
        준비(2); Rede_Montón.입력틀[23] = 6; conxunto_suma_de_comprobación(2); rexeitar_VALOR_e3ecc00b(44);
        준비(2); Rede_Montón.넣기16(Rede_Montón.입력틀, 40, 0); Rede_Montón.Proceso_marco(44); verificar(Rede_Montón.RECIBIDO_duración[0] == 2);
        int[] RESULTANTE = new int[4];
        verificar(Rede_Montón.받기(3, RESULTANTE, 1, 0) == -90);
        verificar(Rede_Montón.받기(3, RESULTANTE, 4, 0) == -11);
        준비(2); Rede_Montón.Proceso_marco(44); int rexeitar_VALOR = Rede_Montón.폐기수;
        Rede_Montón.Proceso_marco(44); verificar(Rede_Montón.폐기수 == rexeitar_VALOR + 1);
        Rede_Montón.Limpo_Proceso(); verificar(Rede_Montón.Abrir(5000) == 3);
        verificar(Rede_Montón.Abrir(5000) == -98); verificar(Rede_Montón.Abrir(0) == 4);
        verificar(Rede_Montón.Abrir(0) == 5); verificar(Rede_Montón.Abrir(0) == 6); verificar(Rede_Montón.Abrir(0) == -24);
        verificar(Rede_Montón.Pechar(4) == 0); verificar(Rede_Montón.Pechar(4) == -9);
        Rede_Montón.찾은주소 = Rede_Montón.pasarela_VALOR;
        verificar(Rede_Montón.enviar(3, Rede_Montón.pasarela_VALOR, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = Rede_controlador.recente_VALOR;
        verificar(suma_de_comprobación(보냄, 14, 20, 0) == 0);
        verificar(suma_de_comprobación(보냄, 34, 11, Rede_Montón.가상머리합(Rede_Montón.내주소, Rede_Montón.pasarela_VALOR, 11)) == 0);
        verificar(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + 횟수 + " assertions");
    }
}
