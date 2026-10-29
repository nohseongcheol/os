// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** stvaran_podaci Java slučaj_VALUE 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class 패킷시험 {
    static int 횟수 = 0;
    static void potvrditi(boolean VALUE) { if (!VALUE) throw new AssertionError("case " + 횟수); 횟수++; }
    static int kontrolni_zbir(int[] VALUE, int Pokreni, int dužina_VALUE, int 초기) {
        int SUM_VALUE = 초기;
        for (int INDEX = 0; INDEX < dužina_VALUE; INDEX++) SUM_VALUE += VALUE[Pokreni + INDEX] << ((INDEX & 1) == 0 ? 8 : 0);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        return ~SUM_VALUE & 65535;
    }
    static void Pripremiti(int dužina_VALUE) {
        Mreža_snop.CLEAN_proces();
        potvrditi(Mreža_snop.Otvori(5000) == 3);
        int[] kadar_INDEX = Mreža_snop.입력틀;
        Arrays.fill(kadar_INDEX, 0);
        for (int INDEX = 0; INDEX < 6; INDEX++) kadar_INDEX[INDEX] = Mreža_drajver_uređaja.uređaj_adresa[INDEX];
        Mreža_snop.넣기16(kadar_INDEX, 12, 0x0800);
        kadar_INDEX[14] = 0x45; kadar_INDEX[22] = 64; kadar_INDEX[23] = 17;
        Mreža_snop.넣기16(kadar_INDEX, 16, 28 + dužina_VALUE);
        Mreža_snop.넣기32(kadar_INDEX, 26, 0x0a000202); Mreža_snop.넣기32(kadar_INDEX, 30, Mreža_snop.내주소);
        Mreža_snop.넣기16(kadar_INDEX, 34, 4321); Mreža_snop.넣기16(kadar_INDEX, 36, 5000); Mreža_snop.넣기16(kadar_INDEX, 38, dužina_VALUE + 8);
        for (int INDEX = 0; INDEX < dužina_VALUE; INDEX++) kadar_INDEX[42 + INDEX] = INDEX & 255;
        skup_kontrolni_zbir(dužina_VALUE);
    }
    static void skup_kontrolni_zbir(int dužina_VALUE) {
        int[] kadar_INDEX = Mreža_snop.입력틀;
        Mreža_snop.넣기16(kadar_INDEX, 24, 0); Mreža_snop.넣기16(kadar_INDEX, 40, 0);
        Mreža_snop.넣기16(kadar_INDEX, 24, kontrolni_zbir(kadar_INDEX, 14, 20, 0));
        int 초기 = Mreža_snop.가상머리합(Mreža_snop.cijeli_broj_32(kadar_INDEX, 26), Mreža_snop.내주소, dužina_VALUE + 8);
        int SUM_VALUE = kontrolni_zbir(kadar_INDEX, 34, dužina_VALUE + 8, 초기);
        Mreža_snop.넣기16(kadar_INDEX, 40, SUM_VALUE == 0 ? 65535 : SUM_VALUE);
    }
    static void odbiti_VALUE(int dužina_VALUE) { Mreža_snop.proces_kadar(dužina_VALUE); potvrditi(Mreža_snop.RECEIVED_dužina[0] == -1); }
    public static void main(String[] Argumenti) {
        for (int dužina_VALUE : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Pripremiti(dužina_VALUE); Mreža_snop.proces_kadar(dužina_VALUE + 42);
            potvrditi(Mreža_snop.RECEIVED_dužina[0] == dužina_VALUE);
            potvrditi(Mreža_snop.RECEIVED_adresa[0] == 0x0a000202 && Mreža_snop.RECEIVED_broj_priključka[0] == 4321);
            for (int INDEX = 0; INDEX < dužina_VALUE; INDEX++) potvrditi(Mreža_snop.RECEIVED_podaci[INDEX] == (INDEX & 255));
        }
        for (int dužina_VALUE = 0; dužina_VALUE < 42; dužina_VALUE++) { Pripremiti(0); odbiti_VALUE(dužina_VALUE); }
        Pripremiti(1025); odbiti_VALUE(1067);
        Pripremiti(2); Mreža_snop.입력틀[24] ^= 1; odbiti_VALUE(44);
        Pripremiti(2); Mreža_snop.입력틀[42] ^= 1; odbiti_VALUE(44);
        Pripremiti(2); Mreža_snop.넣기16(Mreža_snop.입력틀, 38, 7); odbiti_VALUE(44);
        Pripremiti(2); Mreža_snop.넣기16(Mreža_snop.입력틀, 38, 65535); odbiti_VALUE(44);
        Pripremiti(2); Mreža_snop.입력틀[14] = 0x4f; odbiti_VALUE(44);
        Pripremiti(2); Mreža_snop.입력틀[14] = 0x44; odbiti_VALUE(44);
        Pripremiti(2); Mreža_snop.입력틀[20] = 0x20; skup_kontrolni_zbir(2); odbiti_VALUE(44);
        Pripremiti(2); Mreža_snop.입력틀[21] = 1; skup_kontrolni_zbir(2); odbiti_VALUE(44);
        Pripremiti(2); Mreža_snop.입력틀[33] = 99; skup_kontrolni_zbir(2); odbiti_VALUE(44);
        Pripremiti(2); Mreža_snop.입력틀[0] ^= 1; odbiti_VALUE(44);
        Pripremiti(2); Mreža_snop.입력틀[23] = 6; skup_kontrolni_zbir(2); odbiti_VALUE(44);
        Pripremiti(2); Mreža_snop.넣기16(Mreža_snop.입력틀, 40, 0); Mreža_snop.proces_kadar(44); potvrditi(Mreža_snop.RECEIVED_dužina[0] == 2);
        int[] mjera = new int[4];
        potvrditi(Mreža_snop.받기(3, mjera, 1, 0) == -90);
        potvrditi(Mreža_snop.받기(3, mjera, 4, 0) == -11);
        Pripremiti(2); Mreža_snop.proces_kadar(44); int odbaci_VALUE = Mreža_snop.폐기수;
        Mreža_snop.proces_kadar(44); potvrditi(Mreža_snop.폐기수 == odbaci_VALUE + 1);
        Mreža_snop.CLEAN_proces(); potvrditi(Mreža_snop.Otvori(5000) == 3);
        potvrditi(Mreža_snop.Otvori(5000) == -98); potvrditi(Mreža_snop.Otvori(0) == 4);
        potvrditi(Mreža_snop.Otvori(0) == 5); potvrditi(Mreža_snop.Otvori(0) == 6); potvrditi(Mreža_snop.Otvori(0) == -24);
        potvrditi(Mreža_snop.Zatvori(4) == 0); potvrditi(Mreža_snop.Zatvori(4) == -9);
        Mreža_snop.찾은주소 = Mreža_snop.pristupni_uređaj_VALUE;
        potvrditi(Mreža_snop.poslati(3, Mreža_snop.pristupni_uređaj_VALUE, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = Mreža_drajver_uređaja.nedavno_VALUE;
        potvrditi(kontrolni_zbir(보냄, 14, 20, 0) == 0);
        potvrditi(kontrolni_zbir(보냄, 34, 11, Mreža_snop.가상머리합(Mreža_snop.내주소, Mreža_snop.pristupni_uređaj_VALUE, 11)) == 0);
        potvrditi(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + 횟수 + " assertions");
    }
}
