// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** real_dades Java cas_VALOR 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class 패킷시험 {
    static int 횟수 = 0;
    static void verificar(boolean VALOR) { if (!VALOR) throw new AssertionError("case " + 횟수); 횟수++; }
    static int suma_de_comprovació(int[] VALOR, int Executa_2, int durada_VALOR, int 초기) {
        int SUMA_VALOR = 초기;
        for (int INDEX = 0; INDEX < durada_VALOR; INDEX++) SUMA_VALOR += VALOR[Executa_2 + INDEX] << ((INDEX & 1) == 0 ? 8 : 0);
        SUMA_VALOR = (SUMA_VALOR & 65535) + (SUMA_VALOR >>> 16);
        SUMA_VALOR = (SUMA_VALOR & 65535) + (SUMA_VALOR >>> 16);
        return ~SUMA_VALOR & 65535;
    }
    static void Prepara(int durada_VALOR) {
        xarxa_Pila.NETEJA_Procés();
        verificar(xarxa_Pila.Obre(5000) == 3);
        int[] marc_INDEX = xarxa_Pila.입력틀;
        Arrays.fill(marc_INDEX, 0);
        for (int INDEX = 0; INDEX < 6; INDEX++) marc_INDEX[INDEX] = xarxa_controlador.dispositiu_ADREÇA[INDEX];
        xarxa_Pila.넣기16(marc_INDEX, 12, 0x0800);
        marc_INDEX[14] = 0x45; marc_INDEX[22] = 64; marc_INDEX[23] = 17;
        xarxa_Pila.넣기16(marc_INDEX, 16, 28 + durada_VALOR);
        xarxa_Pila.넣기32(marc_INDEX, 26, 0x0a000202); xarxa_Pila.넣기32(marc_INDEX, 30, xarxa_Pila.내주소);
        xarxa_Pila.넣기16(marc_INDEX, 34, 4321); xarxa_Pila.넣기16(marc_INDEX, 36, 5000); xarxa_Pila.넣기16(marc_INDEX, 38, durada_VALOR + 8);
        for (int INDEX = 0; INDEX < durada_VALOR; INDEX++) marc_INDEX[42 + INDEX] = INDEX & 255;
        conjunt_suma_de_comprovació(durada_VALOR);
    }
    static void conjunt_suma_de_comprovació(int durada_VALOR) {
        int[] marc_INDEX = xarxa_Pila.입력틀;
        xarxa_Pila.넣기16(marc_INDEX, 24, 0); xarxa_Pila.넣기16(marc_INDEX, 40, 0);
        xarxa_Pila.넣기16(marc_INDEX, 24, suma_de_comprovació(marc_INDEX, 14, 20, 0));
        int 초기 = xarxa_Pila.가상머리합(xarxa_Pila.수32(marc_INDEX, 26), xarxa_Pila.내주소, durada_VALOR + 8);
        int SUMA_VALOR = suma_de_comprovació(marc_INDEX, 34, durada_VALOR + 8, 초기);
        xarxa_Pila.넣기16(marc_INDEX, 40, SUMA_VALOR == 0 ? 65535 : SUMA_VALOR);
    }
    static void rebutjar_VALOR(int durada_VALOR) { xarxa_Pila.Procés_marc(durada_VALOR); verificar(xarxa_Pila.CANTIDAD_RECIBIDA_durada[0] == -1); }
    public static void main(String[] 인수) {
        for (int durada_VALOR : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Prepara(durada_VALOR); xarxa_Pila.Procés_marc(durada_VALOR + 42);
            verificar(xarxa_Pila.CANTIDAD_RECIBIDA_durada[0] == durada_VALOR);
            verificar(xarxa_Pila.CANTIDAD_RECIBIDA_ADREÇA[0] == 0x0a000202 && xarxa_Pila.CANTIDAD_RECIBIDA_número_de_port[0] == 4321);
            for (int INDEX = 0; INDEX < durada_VALOR; INDEX++) verificar(xarxa_Pila.CANTIDAD_RECIBIDA_dades[INDEX] == (INDEX & 255));
        }
        for (int durada_VALOR = 0; durada_VALOR < 42; durada_VALOR++) { Prepara(0); rebutjar_VALOR(durada_VALOR); }
        Prepara(1025); rebutjar_VALOR(1067);
        Prepara(2); xarxa_Pila.입력틀[24] ^= 1; rebutjar_VALOR(44);
        Prepara(2); xarxa_Pila.입력틀[42] ^= 1; rebutjar_VALOR(44);
        Prepara(2); xarxa_Pila.넣기16(xarxa_Pila.입력틀, 38, 7); rebutjar_VALOR(44);
        Prepara(2); xarxa_Pila.넣기16(xarxa_Pila.입력틀, 38, 65535); rebutjar_VALOR(44);
        Prepara(2); xarxa_Pila.입력틀[14] = 0x4f; rebutjar_VALOR(44);
        Prepara(2); xarxa_Pila.입력틀[14] = 0x44; rebutjar_VALOR(44);
        Prepara(2); xarxa_Pila.입력틀[20] = 0x20; conjunt_suma_de_comprovació(2); rebutjar_VALOR(44);
        Prepara(2); xarxa_Pila.입력틀[21] = 1; conjunt_suma_de_comprovació(2); rebutjar_VALOR(44);
        Prepara(2); xarxa_Pila.입력틀[33] = 99; conjunt_suma_de_comprovació(2); rebutjar_VALOR(44);
        Prepara(2); xarxa_Pila.입력틀[0] ^= 1; rebutjar_VALOR(44);
        Prepara(2); xarxa_Pila.입력틀[23] = 6; conjunt_suma_de_comprovació(2); rebutjar_VALOR(44);
        Prepara(2); xarxa_Pila.넣기16(xarxa_Pila.입력틀, 40, 0); xarxa_Pila.Procés_marc(44); verificar(xarxa_Pila.CANTIDAD_RECIBIDA_durada[0] == 2);
        int[] RESULTAT = new int[4];
        verificar(xarxa_Pila.rebre(3, RESULTAT, 1, 0) == -90);
        verificar(xarxa_Pila.rebre(3, RESULTAT, 4, 0) == -11);
        Prepara(2); xarxa_Pila.Procés_marc(44); int descartar_VALOR = xarxa_Pila.폐기수;
        xarxa_Pila.Procés_marc(44); verificar(xarxa_Pila.폐기수 == descartar_VALOR + 1);
        xarxa_Pila.NETEJA_Procés(); verificar(xarxa_Pila.Obre(5000) == 3);
        verificar(xarxa_Pila.Obre(5000) == -98); verificar(xarxa_Pila.Obre(0) == 4);
        verificar(xarxa_Pila.Obre(0) == 5); verificar(xarxa_Pila.Obre(0) == 6); verificar(xarxa_Pila.Obre(0) == -24);
        verificar(xarxa_Pila.Tanca(4) == 0); verificar(xarxa_Pila.Tanca(4) == -9);
        xarxa_Pila.찾은주소 = xarxa_Pila.passarel_la_VALOR;
        verificar(xarxa_Pila.enviar(3, xarxa_Pila.passarel_la_VALOR, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = xarxa_controlador.recent_VALOR;
        verificar(suma_de_comprovació(보냄, 14, 20, 0) == 0);
        verificar(suma_de_comprovació(보냄, 34, 11, xarxa_Pila.가상머리합(xarxa_Pila.내주소, xarxa_Pila.passarel_la_VALOR, 11)) == 0);
        verificar(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + 횟수 + " assertions");
    }
}
