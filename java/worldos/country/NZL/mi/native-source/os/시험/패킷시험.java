// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** tūturu_raraunga Java kēhi_uara 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class 패킷시험 {
    static int 횟수 = 0;
    static void manatoko(boolean uara) { if (!uara) throw new AssertionError("case " + 횟수); 횟수++; }
    static int 검사합(int[] uara, int whakahaere, int roa_uara, int 초기) {
        int SUM_uara = 초기;
        for (int INDEX = 0; INDEX < roa_uara; INDEX++) SUM_uara += uara[whakahaere + INDEX] << ((INDEX & 1) == 0 ? 8 : 0);
        SUM_uara = (SUM_uara & 65535) + (SUM_uara >>> 16);
        SUM_uara = (SUM_uara & 65535) + (SUM_uara >>> 16);
        return ~SUM_uara & 65535;
    }
    static void Whakarite(int roa_uara) {
        whatunga_Huinga.CLEAN_Hātepe();
        manatoko(whatunga_Huinga.Huaki(5000) == 3);
        int[] tāpare_INDEX = whatunga_Huinga.입력틀;
        Arrays.fill(tāpare_INDEX, 0);
        for (int INDEX = 0; INDEX < 6; INDEX++) tāpare_INDEX[INDEX] = whatunga_atekōkiri.pūkoro_ADDRESS[INDEX];
        whatunga_Huinga.넣기16(tāpare_INDEX, 12, 0x0800);
        tāpare_INDEX[14] = 0x45; tāpare_INDEX[22] = 64; tāpare_INDEX[23] = 17;
        whatunga_Huinga.넣기16(tāpare_INDEX, 16, 28 + roa_uara);
        whatunga_Huinga.넣기32(tāpare_INDEX, 26, 0x0a000202); whatunga_Huinga.넣기32(tāpare_INDEX, 30, whatunga_Huinga.내주소);
        whatunga_Huinga.넣기16(tāpare_INDEX, 34, 4321); whatunga_Huinga.넣기16(tāpare_INDEX, 36, 5000); whatunga_Huinga.넣기16(tāpare_INDEX, 38, roa_uara + 8);
        for (int INDEX = 0; INDEX < roa_uara; INDEX++) tāpare_INDEX[42 + INDEX] = INDEX & 255;
        검사합넣기(roa_uara);
    }
    static void 검사합넣기(int roa_uara) {
        int[] tāpare_INDEX = whatunga_Huinga.입력틀;
        whatunga_Huinga.넣기16(tāpare_INDEX, 24, 0); whatunga_Huinga.넣기16(tāpare_INDEX, 40, 0);
        whatunga_Huinga.넣기16(tāpare_INDEX, 24, 검사합(tāpare_INDEX, 14, 20, 0));
        int 초기 = whatunga_Huinga.가상머리합(whatunga_Huinga.tau_tōpū_32(tāpare_INDEX, 26), whatunga_Huinga.내주소, roa_uara + 8);
        int SUM_uara = 검사합(tāpare_INDEX, 34, roa_uara + 8, 초기);
        whatunga_Huinga.넣기16(tāpare_INDEX, 40, SUM_uara == 0 ? 65535 : SUM_uara);
    }
    static void 거부(int roa_uara) { whatunga_Huinga.Hātepe_tāpare(roa_uara); manatoko(whatunga_Huinga.RECEIVED_roa[0] == -1); }
    public static void main(String[] 인수) {
        for (int roa_uara : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Whakarite(roa_uara); whatunga_Huinga.Hātepe_tāpare(roa_uara + 42);
            manatoko(whatunga_Huinga.RECEIVED_roa[0] == roa_uara);
            manatoko(whatunga_Huinga.RECEIVED_ADDRESS[0] == 0x0a000202 && whatunga_Huinga.받은접속번호[0] == 4321);
            for (int INDEX = 0; INDEX < roa_uara; INDEX++) manatoko(whatunga_Huinga.RECEIVED_raraunga[INDEX] == (INDEX & 255));
        }
        for (int roa_uara = 0; roa_uara < 42; roa_uara++) { Whakarite(0); 거부(roa_uara); }
        Whakarite(1025); 거부(1067);
        Whakarite(2); whatunga_Huinga.입력틀[24] ^= 1; 거부(44);
        Whakarite(2); whatunga_Huinga.입력틀[42] ^= 1; 거부(44);
        Whakarite(2); whatunga_Huinga.넣기16(whatunga_Huinga.입력틀, 38, 7); 거부(44);
        Whakarite(2); whatunga_Huinga.넣기16(whatunga_Huinga.입력틀, 38, 65535); 거부(44);
        Whakarite(2); whatunga_Huinga.입력틀[14] = 0x4f; 거부(44);
        Whakarite(2); whatunga_Huinga.입력틀[14] = 0x44; 거부(44);
        Whakarite(2); whatunga_Huinga.입력틀[20] = 0x20; 검사합넣기(2); 거부(44);
        Whakarite(2); whatunga_Huinga.입력틀[21] = 1; 검사합넣기(2); 거부(44);
        Whakarite(2); whatunga_Huinga.입력틀[33] = 99; 검사합넣기(2); 거부(44);
        Whakarite(2); whatunga_Huinga.입력틀[0] ^= 1; 거부(44);
        Whakarite(2); whatunga_Huinga.입력틀[23] = 6; 검사합넣기(2); 거부(44);
        Whakarite(2); whatunga_Huinga.넣기16(whatunga_Huinga.입력틀, 40, 0); whatunga_Huinga.Hātepe_tāpare(44); manatoko(whatunga_Huinga.RECEIVED_roa[0] == 2);
        int[] mēhua = new int[4];
        manatoko(whatunga_Huinga.받기(3, mēhua, 1, 0) == -90);
        manatoko(whatunga_Huinga.받기(3, mēhua, 4, 0) == -11);
        Whakarite(2); whatunga_Huinga.Hātepe_tāpare(44); int turaki_uara = whatunga_Huinga.폐기수;
        whatunga_Huinga.Hātepe_tāpare(44); manatoko(whatunga_Huinga.폐기수 == turaki_uara + 1);
        whatunga_Huinga.CLEAN_Hātepe(); manatoko(whatunga_Huinga.Huaki(5000) == 3);
        manatoko(whatunga_Huinga.Huaki(5000) == -98); manatoko(whatunga_Huinga.Huaki(0) == 4);
        manatoko(whatunga_Huinga.Huaki(0) == 5); manatoko(whatunga_Huinga.Huaki(0) == 6); manatoko(whatunga_Huinga.Huaki(0) == -24);
        manatoko(whatunga_Huinga.Kati(4) == 0); manatoko(whatunga_Huinga.Kati(4) == -9);
        whatunga_Huinga.찾은주소 = whatunga_Huinga.waharoa_uara;
        manatoko(whatunga_Huinga.tuku(3, whatunga_Huinga.waharoa_uara, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = whatunga_atekōkiri.nōnākuanei_uara;
        manatoko(검사합(보냄, 14, 20, 0) == 0);
        manatoko(검사합(보냄, 34, 11, whatunga_Huinga.가상머리합(whatunga_Huinga.내주소, whatunga_Huinga.waharoa_uara, 11)) == 0);
        manatoko(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + 횟수 + " assertions");
    }
}
