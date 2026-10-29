// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** liteew_mbir Java ay_xëyma 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class 패킷시험 {
    static int 횟수 = 0;
    static void luñutu(boolean xëyma) { if (!xëyma) throw new AssertionError("case " + 횟수); 횟수++; }
    static int 검사합(int[] xëyma, int daw, int diir_xëyma, int 초기) {
        int 합 = 초기;
        for (int àlluwa_tur = 0; àlluwa_tur < diir_xëyma; àlluwa_tur++) 합 += xëyma[daw + àlluwa_tur] << ((àlluwa_tur & 1) == 0 ? 8 : 0);
        합 = (합 & 65535) + (합 >>> 16);
        합 = (합 & 65535) + (합 >>> 16);
        return ~합 & 65535;
    }
    static void jël_matuwaay(int diir_xëyma) {
        mbaal_Tegalo.과정정리();
        luñutu(mbaal_Tegalo.sos(5000) == 3);
        int[] kadar_àlluwa_tur = mbaal_Tegalo.입력틀;
        Arrays.fill(kadar_àlluwa_tur, 0);
        for (int àlluwa_tur = 0; àlluwa_tur < 6; àlluwa_tur++) kadar_àlluwa_tur[àlluwa_tur] = mbaal_daraayba.toftal_dëkkuwaay[àlluwa_tur];
        mbaal_Tegalo.넣기16(kadar_àlluwa_tur, 12, 0x0800);
        kadar_àlluwa_tur[14] = 0x45; kadar_àlluwa_tur[22] = 64; kadar_àlluwa_tur[23] = 17;
        mbaal_Tegalo.넣기16(kadar_àlluwa_tur, 16, 28 + diir_xëyma);
        mbaal_Tegalo.넣기32(kadar_àlluwa_tur, 26, 0x0a000202); mbaal_Tegalo.넣기32(kadar_àlluwa_tur, 30, mbaal_Tegalo.내주소);
        mbaal_Tegalo.넣기16(kadar_àlluwa_tur, 34, 4321); mbaal_Tegalo.넣기16(kadar_àlluwa_tur, 36, 5000); mbaal_Tegalo.넣기16(kadar_àlluwa_tur, 38, diir_xëyma + 8);
        for (int àlluwa_tur = 0; àlluwa_tur < diir_xëyma; àlluwa_tur++) kadar_àlluwa_tur[42 + àlluwa_tur] = àlluwa_tur & 255;
        검사합넣기(diir_xëyma);
    }
    static void 검사합넣기(int diir_xëyma) {
        int[] kadar_àlluwa_tur = mbaal_Tegalo.입력틀;
        mbaal_Tegalo.넣기16(kadar_àlluwa_tur, 24, 0); mbaal_Tegalo.넣기16(kadar_àlluwa_tur, 40, 0);
        mbaal_Tegalo.넣기16(kadar_àlluwa_tur, 24, 검사합(kadar_àlluwa_tur, 14, 20, 0));
        int 초기 = mbaal_Tegalo.가상머리합(mbaal_Tegalo.lëmm_32(kadar_àlluwa_tur, 26), mbaal_Tegalo.내주소, diir_xëyma + 8);
        int 합 = 검사합(kadar_àlluwa_tur, 34, diir_xëyma + 8, 초기);
        mbaal_Tegalo.넣기16(kadar_àlluwa_tur, 40, 합 == 0 ? 65535 : 합);
    }
    static void 거부(int diir_xëyma) { mbaal_Tegalo.yokkute_kadar(diir_xëyma); luñutu(mbaal_Tegalo.받은길이[0] == -1); }
    public static void main(String[] 인수) {
        for (int diir_xëyma : new int[]{0, 1, 2, 7, 1023, 1024}) {
            jël_matuwaay(diir_xëyma); mbaal_Tegalo.yokkute_kadar(diir_xëyma + 42);
            luñutu(mbaal_Tegalo.받은길이[0] == diir_xëyma);
            luñutu(mbaal_Tegalo.받은주소[0] == 0x0a000202 && mbaal_Tegalo.받은접속번호[0] == 4321);
            for (int àlluwa_tur = 0; àlluwa_tur < diir_xëyma; àlluwa_tur++) luñutu(mbaal_Tegalo.받은자료[àlluwa_tur] == (àlluwa_tur & 255));
        }
        for (int diir_xëyma = 0; diir_xëyma < 42; diir_xëyma++) { jël_matuwaay(0); 거부(diir_xëyma); }
        jël_matuwaay(1025); 거부(1067);
        jël_matuwaay(2); mbaal_Tegalo.입력틀[24] ^= 1; 거부(44);
        jël_matuwaay(2); mbaal_Tegalo.입력틀[42] ^= 1; 거부(44);
        jël_matuwaay(2); mbaal_Tegalo.넣기16(mbaal_Tegalo.입력틀, 38, 7); 거부(44);
        jël_matuwaay(2); mbaal_Tegalo.넣기16(mbaal_Tegalo.입력틀, 38, 65535); 거부(44);
        jël_matuwaay(2); mbaal_Tegalo.입력틀[14] = 0x4f; 거부(44);
        jël_matuwaay(2); mbaal_Tegalo.입력틀[14] = 0x44; 거부(44);
        jël_matuwaay(2); mbaal_Tegalo.입력틀[20] = 0x20; 검사합넣기(2); 거부(44);
        jël_matuwaay(2); mbaal_Tegalo.입력틀[21] = 1; 검사합넣기(2); 거부(44);
        jël_matuwaay(2); mbaal_Tegalo.입력틀[33] = 99; 검사합넣기(2); 거부(44);
        jël_matuwaay(2); mbaal_Tegalo.입력틀[0] ^= 1; 거부(44);
        jël_matuwaay(2); mbaal_Tegalo.입력틀[23] = 6; 검사합넣기(2); 거부(44);
        jël_matuwaay(2); mbaal_Tegalo.넣기16(mbaal_Tegalo.입력틀, 40, 0); mbaal_Tegalo.yokkute_kadar(44); luñutu(mbaal_Tegalo.받은길이[0] == 2);
        int[] 결과 = new int[4];
        luñutu(mbaal_Tegalo.받기(3, 결과, 1, 0) == -90);
        luñutu(mbaal_Tegalo.받기(3, 결과, 4, 0) == -11);
        jël_matuwaay(2); mbaal_Tegalo.yokkute_kadar(44); int far_xëyma = mbaal_Tegalo.폐기수;
        mbaal_Tegalo.yokkute_kadar(44); luñutu(mbaal_Tegalo.폐기수 == far_xëyma + 1);
        mbaal_Tegalo.과정정리(); luñutu(mbaal_Tegalo.sos(5000) == 3);
        luñutu(mbaal_Tegalo.sos(5000) == -98); luñutu(mbaal_Tegalo.sos(0) == 4);
        luñutu(mbaal_Tegalo.sos(0) == 5); luñutu(mbaal_Tegalo.sos(0) == 6); luñutu(mbaal_Tegalo.sos(0) == -24);
        luñutu(mbaal_Tegalo.Tej(4) == 0); luñutu(mbaal_Tegalo.Tej(4) == -9);
        mbaal_Tegalo.찾은주소 = mbaal_Tegalo.bunt_xëyma;
        luñutu(mbaal_Tegalo.Yónnee(3, mbaal_Tegalo.bunt_xëyma, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = mbaal_daraayba.bees_xëyma;
        luñutu(검사합(보냄, 14, 20, 0) == 0);
        luñutu(검사합(보냄, 34, 11, mbaal_Tegalo.가상머리합(mbaal_Tegalo.내주소, mbaal_Tegalo.bunt_xëyma, 11)) == 0);
        luñutu(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + 횟수 + " assertions");
    }
}
