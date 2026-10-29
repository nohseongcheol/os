// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** stvarni_podaci Java ugovor_VALUE 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class 패킷시험 {
    static int 횟수 = 0;
    static void verifikovati(boolean VALUE) { if (!VALUE) throw new AssertionError("case " + 횟수); 횟수++; }
    static int kontrolni_zbir(int[] VALUE, int koristiti, int 길이, int početno_stanje) {
        int SUM_VALUE = početno_stanje;
        for (int INDEX = 0; INDEX < 길이; INDEX++) SUM_VALUE += VALUE[koristiti + INDEX] << ((INDEX & 1) == 0 ? 8 : 0);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        return ~SUM_VALUE & 65535;
    }
    static void Pripremi(int 길이) {
        Mreža_stek.CLEAN_Proces();
        verifikovati(Mreža_stek.otvoren(5000) == 3);
        int[] kadar_INDEX = Mreža_stek.입력틀;
        Arrays.fill(kadar_INDEX, 0);
        for (int INDEX = 0; INDEX < 6; INDEX++) kadar_INDEX[INDEX] = Mreža_Upravljački_program.uređaj_adresa[INDEX];
        Mreža_stek.넣기16(kadar_INDEX, 12, 0x0800);
        kadar_INDEX[14] = 0x45; kadar_INDEX[22] = 64; kadar_INDEX[23] = 17;
        Mreža_stek.넣기16(kadar_INDEX, 16, 28 + 길이);
        Mreža_stek.넣기32(kadar_INDEX, 26, 0x0a000202); Mreža_stek.넣기32(kadar_INDEX, 30, Mreža_stek.내주소);
        Mreža_stek.넣기16(kadar_INDEX, 34, 4321); Mreža_stek.넣기16(kadar_INDEX, 36, 5000); Mreža_stek.넣기16(kadar_INDEX, 38, 길이 + 8);
        for (int INDEX = 0; INDEX < 길이; INDEX++) kadar_INDEX[42 + INDEX] = INDEX & 255;
        skup_kontrolni_zbir(길이);
    }
    static void skup_kontrolni_zbir(int 길이) {
        int[] kadar_INDEX = Mreža_stek.입력틀;
        Mreža_stek.넣기16(kadar_INDEX, 24, 0); Mreža_stek.넣기16(kadar_INDEX, 40, 0);
        Mreža_stek.넣기16(kadar_INDEX, 24, kontrolni_zbir(kadar_INDEX, 14, 20, 0));
        int početno_stanje = Mreža_stek.가상머리합(Mreža_stek.ceo_broj_32(kadar_INDEX, 26), Mreža_stek.내주소, 길이 + 8);
        int SUM_VALUE = kontrolni_zbir(kadar_INDEX, 34, 길이 + 8, početno_stanje);
        Mreža_stek.넣기16(kadar_INDEX, 40, SUM_VALUE == 0 ? 65535 : SUM_VALUE);
    }
    static void odbaciti_VALUE_e3ecc00b(int 길이) { Mreža_stek.Proces_kadar(길이); verifikovati(Mreža_stek.받은길이[0] == -1); }
    public static void main(String[] 인수) {
        for (int 길이 : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Pripremi(길이); Mreža_stek.Proces_kadar(길이 + 42);
            verifikovati(Mreža_stek.받은길이[0] == 길이);
            verifikovati(Mreža_stek.RECEIVED_adresa[0] == 0x0a000202 && Mreža_stek.RECEIVED_broj_porta[0] == 4321);
            for (int INDEX = 0; INDEX < 길이; INDEX++) verifikovati(Mreža_stek.RECEIVED_podaci[INDEX] == (INDEX & 255));
        }
        for (int 길이 = 0; 길이 < 42; 길이++) { Pripremi(0); odbaciti_VALUE_e3ecc00b(길이); }
        Pripremi(1025); odbaciti_VALUE_e3ecc00b(1067);
        Pripremi(2); Mreža_stek.입력틀[24] ^= 1; odbaciti_VALUE_e3ecc00b(44);
        Pripremi(2); Mreža_stek.입력틀[42] ^= 1; odbaciti_VALUE_e3ecc00b(44);
        Pripremi(2); Mreža_stek.넣기16(Mreža_stek.입력틀, 38, 7); odbaciti_VALUE_e3ecc00b(44);
        Pripremi(2); Mreža_stek.넣기16(Mreža_stek.입력틀, 38, 65535); odbaciti_VALUE_e3ecc00b(44);
        Pripremi(2); Mreža_stek.입력틀[14] = 0x4f; odbaciti_VALUE_e3ecc00b(44);
        Pripremi(2); Mreža_stek.입력틀[14] = 0x44; odbaciti_VALUE_e3ecc00b(44);
        Pripremi(2); Mreža_stek.입력틀[20] = 0x20; skup_kontrolni_zbir(2); odbaciti_VALUE_e3ecc00b(44);
        Pripremi(2); Mreža_stek.입력틀[21] = 1; skup_kontrolni_zbir(2); odbaciti_VALUE_e3ecc00b(44);
        Pripremi(2); Mreža_stek.입력틀[33] = 99; skup_kontrolni_zbir(2); odbaciti_VALUE_e3ecc00b(44);
        Pripremi(2); Mreža_stek.입력틀[0] ^= 1; odbaciti_VALUE_e3ecc00b(44);
        Pripremi(2); Mreža_stek.입력틀[23] = 6; skup_kontrolni_zbir(2); odbaciti_VALUE_e3ecc00b(44);
        Pripremi(2); Mreža_stek.넣기16(Mreža_stek.입력틀, 40, 0); Mreža_stek.Proces_kadar(44); verifikovati(Mreža_stek.받은길이[0] == 2);
        int[] KR = new int[4];
        verifikovati(Mreža_stek.primiti(3, KR, 1, 0) == -90);
        verifikovati(Mreža_stek.primiti(3, KR, 4, 0) == -11);
        Pripremi(2); Mreža_stek.Proces_kadar(44); int odbaciti_VALUE = Mreža_stek.폐기수;
        Mreža_stek.Proces_kadar(44); verifikovati(Mreža_stek.폐기수 == odbaciti_VALUE + 1);
        Mreža_stek.CLEAN_Proces(); verifikovati(Mreža_stek.otvoren(5000) == 3);
        verifikovati(Mreža_stek.otvoren(5000) == -98); verifikovati(Mreža_stek.otvoren(0) == 4);
        verifikovati(Mreža_stek.otvoren(0) == 5); verifikovati(Mreža_stek.otvoren(0) == 6); verifikovati(Mreža_stek.otvoren(0) == -24);
        verifikovati(Mreža_stek.Zatvori(4) == 0); verifikovati(Mreža_stek.Zatvori(4) == -9);
        Mreža_stek.찾은주소 = Mreža_stek.mrežni_prolaz_VALUE;
        verifikovati(Mreža_stek.poslati(3, Mreža_stek.mrežni_prolaz_VALUE, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = Mreža_Upravljački_program.nedavno_VALUE;
        verifikovati(kontrolni_zbir(보냄, 14, 20, 0) == 0);
        verifikovati(kontrolni_zbir(보냄, 34, 11, Mreža_stek.가상머리합(Mreža_stek.내주소, Mreža_stek.mrežni_prolaz_VALUE, 11)) == 0);
        verifikovati(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + 횟수 + " assertions");
    }
}
