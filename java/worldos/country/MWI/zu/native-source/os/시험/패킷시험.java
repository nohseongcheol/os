// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** ulwazi_ngokwenzekile_imininingwane Java udaba_inani 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class 패킷시험 {
    static int 횟수 = 0;
    static void qiniseka(boolean inani) { if (!inani) throw new AssertionError("case " + 횟수); 횟수++; }
    static int 검사합(int[] inani, int Sebenzisa, int ubude_inani, int 초기) {
        int 합 = 초기;
        for (int thola_inkomba = 0; thola_inkomba < ubude_inani; thola_inkomba++) 합 += inani[Sebenzisa + thola_inkomba] << ((thola_inkomba & 1) == 0 ? 8 : 0);
        합 = (합 & 65535) + (합 >>> 16);
        합 = (합 & 65535) + (합 >>> 16);
        return ~합 & 65535;
    }
    static void Hlela(int ubude_inani) {
        iNethiwekhi_Isitaki.과정정리();
        qiniseka(iNethiwekhi_Isitaki.Vula(5000) == 3);
        int[] uhlaka_thola_inkomba = iNethiwekhi_Isitaki.입력틀;
        Arrays.fill(uhlaka_thola_inkomba, 0);
        for (int thola_inkomba = 0; thola_inkomba < 6; thola_inkomba++) uhlaka_thola_inkomba[thola_inkomba] = iNethiwekhi_idrayiva.idivayisi_ikheli[thola_inkomba];
        iNethiwekhi_Isitaki.넣기16(uhlaka_thola_inkomba, 12, 0x0800);
        uhlaka_thola_inkomba[14] = 0x45; uhlaka_thola_inkomba[22] = 64; uhlaka_thola_inkomba[23] = 17;
        iNethiwekhi_Isitaki.넣기16(uhlaka_thola_inkomba, 16, 28 + ubude_inani);
        iNethiwekhi_Isitaki.넣기32(uhlaka_thola_inkomba, 26, 0x0a000202); iNethiwekhi_Isitaki.넣기32(uhlaka_thola_inkomba, 30, iNethiwekhi_Isitaki.내주소);
        iNethiwekhi_Isitaki.넣기16(uhlaka_thola_inkomba, 34, 4321); iNethiwekhi_Isitaki.넣기16(uhlaka_thola_inkomba, 36, 5000); iNethiwekhi_Isitaki.넣기16(uhlaka_thola_inkomba, 38, ubude_inani + 8);
        for (int thola_inkomba = 0; thola_inkomba < ubude_inani; thola_inkomba++) uhlaka_thola_inkomba[42 + thola_inkomba] = thola_inkomba & 255;
        검사합넣기(ubude_inani);
    }
    static void 검사합넣기(int ubude_inani) {
        int[] uhlaka_thola_inkomba = iNethiwekhi_Isitaki.입력틀;
        iNethiwekhi_Isitaki.넣기16(uhlaka_thola_inkomba, 24, 0); iNethiwekhi_Isitaki.넣기16(uhlaka_thola_inkomba, 40, 0);
        iNethiwekhi_Isitaki.넣기16(uhlaka_thola_inkomba, 24, 검사합(uhlaka_thola_inkomba, 14, 20, 0));
        int 초기 = iNethiwekhi_Isitaki.가상머리합(iNethiwekhi_Isitaki.inamba_32(uhlaka_thola_inkomba, 26), iNethiwekhi_Isitaki.내주소, ubude_inani + 8);
        int 합 = 검사합(uhlaka_thola_inkomba, 34, ubude_inani + 8, 초기);
        iNethiwekhi_Isitaki.넣기16(uhlaka_thola_inkomba, 40, 합 == 0 ? 65535 : 합);
    }
    static void 거부(int ubude_inani) { iNethiwekhi_Isitaki.Inqubo_uhlaka(ubude_inani); qiniseka(iNethiwekhi_Isitaki.받은길이[0] == -1); }
    public static void main(String[] 인수) {
        for (int ubude_inani : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Hlela(ubude_inani); iNethiwekhi_Isitaki.Inqubo_uhlaka(ubude_inani + 42);
            qiniseka(iNethiwekhi_Isitaki.받은길이[0] == ubude_inani);
            qiniseka(iNethiwekhi_Isitaki.받은주소[0] == 0x0a000202 && iNethiwekhi_Isitaki.받은접속번호[0] == 4321);
            for (int thola_inkomba = 0; thola_inkomba < ubude_inani; thola_inkomba++) qiniseka(iNethiwekhi_Isitaki.받은자료[thola_inkomba] == (thola_inkomba & 255));
        }
        for (int ubude_inani = 0; ubude_inani < 42; ubude_inani++) { Hlela(0); 거부(ubude_inani); }
        Hlela(1025); 거부(1067);
        Hlela(2); iNethiwekhi_Isitaki.입력틀[24] ^= 1; 거부(44);
        Hlela(2); iNethiwekhi_Isitaki.입력틀[42] ^= 1; 거부(44);
        Hlela(2); iNethiwekhi_Isitaki.넣기16(iNethiwekhi_Isitaki.입력틀, 38, 7); 거부(44);
        Hlela(2); iNethiwekhi_Isitaki.넣기16(iNethiwekhi_Isitaki.입력틀, 38, 65535); 거부(44);
        Hlela(2); iNethiwekhi_Isitaki.입력틀[14] = 0x4f; 거부(44);
        Hlela(2); iNethiwekhi_Isitaki.입력틀[14] = 0x44; 거부(44);
        Hlela(2); iNethiwekhi_Isitaki.입력틀[20] = 0x20; 검사합넣기(2); 거부(44);
        Hlela(2); iNethiwekhi_Isitaki.입력틀[21] = 1; 검사합넣기(2); 거부(44);
        Hlela(2); iNethiwekhi_Isitaki.입력틀[33] = 99; 검사합넣기(2); 거부(44);
        Hlela(2); iNethiwekhi_Isitaki.입력틀[0] ^= 1; 거부(44);
        Hlela(2); iNethiwekhi_Isitaki.입력틀[23] = 6; 검사합넣기(2); 거부(44);
        Hlela(2); iNethiwekhi_Isitaki.넣기16(iNethiwekhi_Isitaki.입력틀, 40, 0); iNethiwekhi_Isitaki.Inqubo_uhlaka(44); qiniseka(iNethiwekhi_Isitaki.받은길이[0] == 2);
        int[] 결과 = new int[4];
        qiniseka(iNethiwekhi_Isitaki.받기(3, 결과, 1, 0) == -90);
        qiniseka(iNethiwekhi_Isitaki.받기(3, 결과, 4, 0) == -11);
        Hlela(2); iNethiwekhi_Isitaki.Inqubo_uhlaka(44); int khipha_inani = iNethiwekhi_Isitaki.폐기수;
        iNethiwekhi_Isitaki.Inqubo_uhlaka(44); qiniseka(iNethiwekhi_Isitaki.폐기수 == khipha_inani + 1);
        iNethiwekhi_Isitaki.과정정리(); qiniseka(iNethiwekhi_Isitaki.Vula(5000) == 3);
        qiniseka(iNethiwekhi_Isitaki.Vula(5000) == -98); qiniseka(iNethiwekhi_Isitaki.Vula(0) == 4);
        qiniseka(iNethiwekhi_Isitaki.Vula(0) == 5); qiniseka(iNethiwekhi_Isitaki.Vula(0) == 6); qiniseka(iNethiwekhi_Isitaki.Vula(0) == -24);
        qiniseka(iNethiwekhi_Isitaki.Vala(4) == 0); qiniseka(iNethiwekhi_Isitaki.Vala(4) == -9);
        iNethiwekhi_Isitaki.찾은주소 = iNethiwekhi_Isitaki.isango_inani;
        qiniseka(iNethiwekhi_Isitaki.Thumela(3, iNethiwekhi_Isitaki.isango_inani, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = iNethiwekhi_idrayiva.okwamuva_nje_inani;
        qiniseka(검사합(보냄, 14, 20, 0) == 0);
        qiniseka(검사합(보냄, 34, 11, iNethiwekhi_Isitaki.가상머리합(iNethiwekhi_Isitaki.내주소, iNethiwekhi_Isitaki.isango_inani, 11)) == 0);
        qiniseka(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + 횟수 + " assertions");
    }
}
