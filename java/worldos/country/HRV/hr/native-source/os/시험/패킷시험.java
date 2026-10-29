// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** stvaran_podaci Java slučaj_VALUE 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class 패킷시험 {
    static int 횟수 = 0;
    static void provjeriti(boolean VALUE) { if (!VALUE) throw new AssertionError("case " + 횟수); 횟수++; }
    static int kontrolni_zbroj(int[] VALUE, int Pokreni, int 길이, int početno_stanje) {
        int SUM_VALUE = početno_stanje;
        for (int INDEX = 0; INDEX < 길이; INDEX++) SUM_VALUE += VALUE[Pokreni + INDEX] << ((INDEX & 1) == 0 ? 8 : 0);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        SUM_VALUE = (SUM_VALUE & 65535) + (SUM_VALUE >>> 16);
        return ~SUM_VALUE & 65535;
    }
    static void Pripremi(int 길이) {
        mreža_hrpa.CLEAN_Proces();
        provjeriti(mreža_hrpa.Otvori(5000) == 3);
        int[] kadar_INDEX = mreža_hrpa.입력틀;
        Arrays.fill(kadar_INDEX, 0);
        for (int INDEX = 0; INDEX < 6; INDEX++) kadar_INDEX[INDEX] = mreža_upravljački_program.uređaj_adresa[INDEX];
        mreža_hrpa.넣기16(kadar_INDEX, 12, 0x0800);
        kadar_INDEX[14] = 0x45; kadar_INDEX[22] = 64; kadar_INDEX[23] = 17;
        mreža_hrpa.넣기16(kadar_INDEX, 16, 28 + 길이);
        mreža_hrpa.넣기32(kadar_INDEX, 26, 0x0a000202); mreža_hrpa.넣기32(kadar_INDEX, 30, mreža_hrpa.내주소);
        mreža_hrpa.넣기16(kadar_INDEX, 34, 4321); mreža_hrpa.넣기16(kadar_INDEX, 36, 5000); mreža_hrpa.넣기16(kadar_INDEX, 38, 길이 + 8);
        for (int INDEX = 0; INDEX < 길이; INDEX++) kadar_INDEX[42 + INDEX] = INDEX & 255;
        skup_kontrolni_zbroj(길이);
    }
    static void skup_kontrolni_zbroj(int 길이) {
        int[] kadar_INDEX = mreža_hrpa.입력틀;
        mreža_hrpa.넣기16(kadar_INDEX, 24, 0); mreža_hrpa.넣기16(kadar_INDEX, 40, 0);
        mreža_hrpa.넣기16(kadar_INDEX, 24, kontrolni_zbroj(kadar_INDEX, 14, 20, 0));
        int početno_stanje = mreža_hrpa.가상머리합(mreža_hrpa.cijeli_broj_32(kadar_INDEX, 26), mreža_hrpa.내주소, 길이 + 8);
        int SUM_VALUE = kontrolni_zbroj(kadar_INDEX, 34, 길이 + 8, početno_stanje);
        mreža_hrpa.넣기16(kadar_INDEX, 40, SUM_VALUE == 0 ? 65535 : SUM_VALUE);
    }
    static void odbiti_VALUE(int 길이) { mreža_hrpa.Proces_kadar(길이); provjeriti(mreža_hrpa.받은길이[0] == -1); }
    public static void main(String[] Argumenti) {
        for (int 길이 : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Pripremi(길이); mreža_hrpa.Proces_kadar(길이 + 42);
            provjeriti(mreža_hrpa.받은길이[0] == 길이);
            provjeriti(mreža_hrpa.RECEIVED_adresa[0] == 0x0a000202 && mreža_hrpa.RECEIVED_broj_priključka[0] == 4321);
            for (int INDEX = 0; INDEX < 길이; INDEX++) provjeriti(mreža_hrpa.RECEIVED_podaci[INDEX] == (INDEX & 255));
        }
        for (int 길이 = 0; 길이 < 42; 길이++) { Pripremi(0); odbiti_VALUE(길이); }
        Pripremi(1025); odbiti_VALUE(1067);
        Pripremi(2); mreža_hrpa.입력틀[24] ^= 1; odbiti_VALUE(44);
        Pripremi(2); mreža_hrpa.입력틀[42] ^= 1; odbiti_VALUE(44);
        Pripremi(2); mreža_hrpa.넣기16(mreža_hrpa.입력틀, 38, 7); odbiti_VALUE(44);
        Pripremi(2); mreža_hrpa.넣기16(mreža_hrpa.입력틀, 38, 65535); odbiti_VALUE(44);
        Pripremi(2); mreža_hrpa.입력틀[14] = 0x4f; odbiti_VALUE(44);
        Pripremi(2); mreža_hrpa.입력틀[14] = 0x44; odbiti_VALUE(44);
        Pripremi(2); mreža_hrpa.입력틀[20] = 0x20; skup_kontrolni_zbroj(2); odbiti_VALUE(44);
        Pripremi(2); mreža_hrpa.입력틀[21] = 1; skup_kontrolni_zbroj(2); odbiti_VALUE(44);
        Pripremi(2); mreža_hrpa.입력틀[33] = 99; skup_kontrolni_zbroj(2); odbiti_VALUE(44);
        Pripremi(2); mreža_hrpa.입력틀[0] ^= 1; odbiti_VALUE(44);
        Pripremi(2); mreža_hrpa.입력틀[23] = 6; skup_kontrolni_zbroj(2); odbiti_VALUE(44);
        Pripremi(2); mreža_hrpa.넣기16(mreža_hrpa.입력틀, 40, 0); mreža_hrpa.Proces_kadar(44); provjeriti(mreža_hrpa.받은길이[0] == 2);
        int[] REZULTAT = new int[4];
        provjeriti(mreža_hrpa.primiti(3, REZULTAT, 1, 0) == -90);
        provjeriti(mreža_hrpa.primiti(3, REZULTAT, 4, 0) == -11);
        Pripremi(2); mreža_hrpa.Proces_kadar(44); int odbaciti_VALUE = mreža_hrpa.폐기수;
        mreža_hrpa.Proces_kadar(44); provjeriti(mreža_hrpa.폐기수 == odbaciti_VALUE + 1);
        mreža_hrpa.CLEAN_Proces(); provjeriti(mreža_hrpa.Otvori(5000) == 3);
        provjeriti(mreža_hrpa.Otvori(5000) == -98); provjeriti(mreža_hrpa.Otvori(0) == 4);
        provjeriti(mreža_hrpa.Otvori(0) == 5); provjeriti(mreža_hrpa.Otvori(0) == 6); provjeriti(mreža_hrpa.Otvori(0) == -24);
        provjeriti(mreža_hrpa.Zatvori(4) == 0); provjeriti(mreža_hrpa.Zatvori(4) == -9);
        mreža_hrpa.찾은주소 = mreža_hrpa.pristupnik_VALUE;
        provjeriti(mreža_hrpa.slati(3, mreža_hrpa.pristupnik_VALUE, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = mreža_upravljački_program.nedavno_VALUE;
        provjeriti(kontrolni_zbroj(보냄, 14, 20, 0) == 0);
        provjeriti(kontrolni_zbroj(보냄, 34, 11, mreža_hrpa.가상머리합(mreža_hrpa.내주소, mreža_hrpa.pristupnik_VALUE, 11)) == 0);
        provjeriti(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + 횟수 + " assertions");
    }
}
