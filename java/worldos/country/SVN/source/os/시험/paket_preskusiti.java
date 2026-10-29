// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** dejanski_podatki Java primer_VALUE 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class paket_preskusiti {
    static int 횟수 = 0;
    static void 확인(boolean VALUE) { if (!VALUE) throw new AssertionError("case " + 횟수); 횟수++; }
    static int kontrolna_vsota(int[] VALUE, int Zaženi, int 길이, int začetno_stanje) {
        int SUM_VALUE = začetno_stanje;
        for (int INDEX = 0; INDEX < 길이; INDEX++) SUM_VALUE += VALUE[Zaženi + INDEX] << ((INDEX & 1) == 0 ? 8 : 0);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        return ~SUM_VALUE & 65535;
    }
    static void Pripravi(int 길이) {
        mreža_Sklad.CLEAN_Proces();
        확인(mreža_Sklad.Odpri(5000) == 3);
        int[] okvir_INDEX = mreža_Sklad.입력틀;
        Arrays.fill(okvir_INDEX, 0);
        for (int INDEX = 0; INDEX < 6; INDEX++) okvir_INDEX[INDEX] = mreža_gonilnik.naprava_naslov[INDEX];
        mreža_Sklad.넣기16(okvir_INDEX, 12, 0x0800);
        okvir_INDEX[14] = 0x45; okvir_INDEX[22] = 64; okvir_INDEX[23] = 17;
        mreža_Sklad.넣기16(okvir_INDEX, 16, 28 + 길이);
        mreža_Sklad.넣기32(okvir_INDEX, 26, 0x0a000202); mreža_Sklad.넣기32(okvir_INDEX, 30, mreža_Sklad.내주소);
        mreža_Sklad.넣기16(okvir_INDEX, 34, 4321); mreža_Sklad.넣기16(okvir_INDEX, 36, 5000); mreža_Sklad.넣기16(okvir_INDEX, 38, 길이 + 8);
        for (int INDEX = 0; INDEX < 길이; INDEX++) okvir_INDEX[42 + INDEX] = INDEX & 255;
        nabor_kontrolna_vsota(길이);
    }
    static void nabor_kontrolna_vsota(int 길이) {
        int[] okvir_INDEX = mreža_Sklad.입력틀;
        mreža_Sklad.넣기16(okvir_INDEX, 24, 0); mreža_Sklad.넣기16(okvir_INDEX, 40, 0);
        mreža_Sklad.넣기16(okvir_INDEX, 24, kontrolna_vsota(okvir_INDEX, 14, 20, 0));
        int začetno_stanje = mreža_Sklad.가상머리합(mreža_Sklad.celo_število_32(okvir_INDEX, 26), mreža_Sklad.내주소, 길이 + 8);
        int SUM_VALUE = kontrolna_vsota(okvir_INDEX, 34, 길이 + 8, začetno_stanje);
        mreža_Sklad.넣기16(okvir_INDEX, 40, SUM_VALUE == 0 ? 65535 : SUM_VALUE);
    }
    static void zavrniti_VALUE(int 길이) { mreža_Sklad.Proces_okvir(길이); 확인(mreža_Sklad.받은길이[0] == -1); }
    public static void main(String[] Argumenti) {
        for (int 길이 : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Pripravi(길이); mreža_Sklad.Proces_okvir(길이 + 42);
            확인(mreža_Sklad.받은길이[0] == 길이);
            확인(mreža_Sklad.RECEIVED_naslov[0] == 0x0a000202 && mreža_Sklad.RECEIVED_številka_vrat[0] == 4321);
            for (int INDEX = 0; INDEX < 길이; INDEX++) 확인(mreža_Sklad.RECEIVED_podatki[INDEX] == (INDEX & 255));
        }
        for (int 길이 = 0; 길이 < 42; 길이++) { Pripravi(0); zavrniti_VALUE(길이); }
        Pripravi(1025); zavrniti_VALUE(1067);
        Pripravi(2); mreža_Sklad.입력틀[24] ^= 1; zavrniti_VALUE(44);
        Pripravi(2); mreža_Sklad.입력틀[42] ^= 1; zavrniti_VALUE(44);
        Pripravi(2); mreža_Sklad.넣기16(mreža_Sklad.입력틀, 38, 7); zavrniti_VALUE(44);
        Pripravi(2); mreža_Sklad.넣기16(mreža_Sklad.입력틀, 38, 65535); zavrniti_VALUE(44);
        Pripravi(2); mreža_Sklad.입력틀[14] = 0x4f; zavrniti_VALUE(44);
        Pripravi(2); mreža_Sklad.입력틀[14] = 0x44; zavrniti_VALUE(44);
        Pripravi(2); mreža_Sklad.입력틀[20] = 0x20; nabor_kontrolna_vsota(2); zavrniti_VALUE(44);
        Pripravi(2); mreža_Sklad.입력틀[21] = 1; nabor_kontrolna_vsota(2); zavrniti_VALUE(44);
        Pripravi(2); mreža_Sklad.입력틀[33] = 99; nabor_kontrolna_vsota(2); zavrniti_VALUE(44);
        Pripravi(2); mreža_Sklad.입력틀[0] ^= 1; zavrniti_VALUE(44);
        Pripravi(2); mreža_Sklad.입력틀[23] = 6; nabor_kontrolna_vsota(2); zavrniti_VALUE(44);
        Pripravi(2); mreža_Sklad.넣기16(mreža_Sklad.입력틀, 40, 0); mreža_Sklad.Proces_okvir(44); 확인(mreža_Sklad.받은길이[0] == 2);
        int[] REZULTAT = new int[4];
        확인(mreža_Sklad.sprejeti_sprejemati_prejeti_prejemati(3, REZULTAT, 1, 0) == -90);
        확인(mreža_Sklad.sprejeti_sprejemati_prejeti_prejemati(3, REZULTAT, 4, 0) == -11);
        Pripravi(2); mreža_Sklad.Proces_okvir(44); int zavreči_VALUE = mreža_Sklad.폐기수;
        mreža_Sklad.Proces_okvir(44); 확인(mreža_Sklad.폐기수 == zavreči_VALUE + 1);
        mreža_Sklad.CLEAN_Proces(); 확인(mreža_Sklad.Odpri(5000) == 3);
        확인(mreža_Sklad.Odpri(5000) == -98); 확인(mreža_Sklad.Odpri(0) == 4);
        확인(mreža_Sklad.Odpri(0) == 5); 확인(mreža_Sklad.Odpri(0) == 6); 확인(mreža_Sklad.Odpri(0) == -24);
        확인(mreža_Sklad.Zapri(4) == 0); 확인(mreža_Sklad.Zapri(4) == -9);
        mreža_Sklad.찾은주소 = mreža_Sklad.prehod_VALUE;
        확인(mreža_Sklad.poslati(3, mreža_Sklad.prehod_VALUE, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = mreža_gonilnik.Nedavno_VALUE;
        확인(kontrolna_vsota(보냄, 14, 20, 0) == 0);
        확인(kontrolna_vsota(보냄, 34, 11, mreža_Sklad.가상머리합(mreža_Sklad.내주소, mreža_Sklad.prehod_VALUE, 11)) == 0);
        확인(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + 횟수 + " assertions");
    }
}
