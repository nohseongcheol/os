// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** real_date Java caz_VALUE 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class 패킷시험 {
    static int 횟수 = 0;
    static void verifica(boolean VALUE) { if (!VALUE) throw new AssertionError("case " + 횟수); 횟수++; }
    static int sumă_de_verificare(int[] VALUE, int Pornește, int lungime_VALUE, int stare_inițială) {
        int SUM_VALUE = stare_inițială;
        for (int INDEX = 0; INDEX < lungime_VALUE; INDEX++) SUM_VALUE += VALUE[Pornește + INDEX] << ((INDEX & 1) == 0 ? 8 : 0);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        return ~SUM_VALUE & 65535;
    }
    static void Pregătiți(int lungime_VALUE) {
        rețea_Teanc.CLEAN_Proces();
        verifica(rețea_Teanc.Deschide(5000) == 3);
        int[] cadru_INDEX = rețea_Teanc.입력틀;
        Arrays.fill(cadru_INDEX, 0);
        for (int INDEX = 0; INDEX < 6; INDEX++) cadru_INDEX[INDEX] = rețea_driver.mobil_adresa[INDEX];
        rețea_Teanc.넣기16(cadru_INDEX, 12, 0x0800);
        cadru_INDEX[14] = 0x45; cadru_INDEX[22] = 64; cadru_INDEX[23] = 17;
        rețea_Teanc.넣기16(cadru_INDEX, 16, 28 + lungime_VALUE);
        rețea_Teanc.넣기32(cadru_INDEX, 26, 0x0a000202); rețea_Teanc.넣기32(cadru_INDEX, 30, rețea_Teanc.내주소);
        rețea_Teanc.넣기16(cadru_INDEX, 34, 4321); rețea_Teanc.넣기16(cadru_INDEX, 36, 5000); rețea_Teanc.넣기16(cadru_INDEX, 38, lungime_VALUE + 8);
        for (int INDEX = 0; INDEX < lungime_VALUE; INDEX++) cadru_INDEX[42 + INDEX] = INDEX & 255;
        set_sumă_de_verificare(lungime_VALUE);
    }
    static void set_sumă_de_verificare(int lungime_VALUE) {
        int[] cadru_INDEX = rețea_Teanc.입력틀;
        rețea_Teanc.넣기16(cadru_INDEX, 24, 0); rețea_Teanc.넣기16(cadru_INDEX, 40, 0);
        rețea_Teanc.넣기16(cadru_INDEX, 24, sumă_de_verificare(cadru_INDEX, 14, 20, 0));
        int stare_inițială = rețea_Teanc.가상머리합(rețea_Teanc.întreg_32(cadru_INDEX, 26), rețea_Teanc.내주소, lungime_VALUE + 8);
        int SUM_VALUE = sumă_de_verificare(cadru_INDEX, 34, lungime_VALUE + 8, stare_inițială);
        rețea_Teanc.넣기16(cadru_INDEX, 40, SUM_VALUE == 0 ? 65535 : SUM_VALUE);
    }
    static void respinge_VALUE(int lungime_VALUE) { rețea_Teanc.Proces_cadru(lungime_VALUE); verifica(rețea_Teanc.RECEIVED_lungime[0] == -1); }
    public static void main(String[] Argumente) {
        for (int lungime_VALUE : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Pregătiți(lungime_VALUE); rețea_Teanc.Proces_cadru(lungime_VALUE + 42);
            verifica(rețea_Teanc.RECEIVED_lungime[0] == lungime_VALUE);
            verifica(rețea_Teanc.RECEIVED_adresa[0] == 0x0a000202 && rețea_Teanc.RECEIVED_număr_port[0] == 4321);
            for (int INDEX = 0; INDEX < lungime_VALUE; INDEX++) verifica(rețea_Teanc.RECEIVED_date[INDEX] == (INDEX & 255));
        }
        for (int lungime_VALUE = 0; lungime_VALUE < 42; lungime_VALUE++) { Pregătiți(0); respinge_VALUE(lungime_VALUE); }
        Pregătiți(1025); respinge_VALUE(1067);
        Pregătiți(2); rețea_Teanc.입력틀[24] ^= 1; respinge_VALUE(44);
        Pregătiți(2); rețea_Teanc.입력틀[42] ^= 1; respinge_VALUE(44);
        Pregătiți(2); rețea_Teanc.넣기16(rețea_Teanc.입력틀, 38, 7); respinge_VALUE(44);
        Pregătiți(2); rețea_Teanc.넣기16(rețea_Teanc.입력틀, 38, 65535); respinge_VALUE(44);
        Pregătiți(2); rețea_Teanc.입력틀[14] = 0x4f; respinge_VALUE(44);
        Pregătiți(2); rețea_Teanc.입력틀[14] = 0x44; respinge_VALUE(44);
        Pregătiți(2); rețea_Teanc.입력틀[20] = 0x20; set_sumă_de_verificare(2); respinge_VALUE(44);
        Pregătiți(2); rețea_Teanc.입력틀[21] = 1; set_sumă_de_verificare(2); respinge_VALUE(44);
        Pregătiți(2); rețea_Teanc.입력틀[33] = 99; set_sumă_de_verificare(2); respinge_VALUE(44);
        Pregătiți(2); rețea_Teanc.입력틀[0] ^= 1; respinge_VALUE(44);
        Pregătiți(2); rețea_Teanc.입력틀[23] = 6; set_sumă_de_verificare(2); respinge_VALUE(44);
        Pregătiți(2); rețea_Teanc.넣기16(rețea_Teanc.입력틀, 40, 0); rețea_Teanc.Proces_cadru(44); verifica(rețea_Teanc.RECEIVED_lungime[0] == 2);
        int[] KR = new int[4];
        verifica(rețea_Teanc.primi(3, KR, 1, 0) == -90);
        verifica(rețea_Teanc.primi(3, KR, 4, 0) == -11);
        Pregătiți(2); rețea_Teanc.Proces_cadru(44); int renunța_VALUE = rețea_Teanc.폐기수;
        rețea_Teanc.Proces_cadru(44); verifica(rețea_Teanc.폐기수 == renunța_VALUE + 1);
        rețea_Teanc.CLEAN_Proces(); verifica(rețea_Teanc.Deschide(5000) == 3);
        verifica(rețea_Teanc.Deschide(5000) == -98); verifica(rețea_Teanc.Deschide(0) == 4);
        verifica(rețea_Teanc.Deschide(0) == 5); verifica(rețea_Teanc.Deschide(0) == 6); verifica(rețea_Teanc.Deschide(0) == -24);
        verifica(rețea_Teanc.Închide(4) == 0); verifica(rețea_Teanc.Închide(4) == -9);
        rețea_Teanc.찾은주소 = rețea_Teanc.gateway_VALUE;
        verifica(rețea_Teanc.trimite(3, rețea_Teanc.gateway_VALUE, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = rețea_driver.recent_VALUE;
        verifica(sumă_de_verificare(보냄, 14, 20, 0) == 0);
        verifica(sumă_de_verificare(보냄, 34, 11, rețea_Teanc.가상머리합(rețea_Teanc.내주소, rețea_Teanc.gateway_VALUE, 11)) == 0);
        verifica(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + 횟수 + " assertions");
    }
}
