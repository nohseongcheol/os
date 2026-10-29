// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** 실제 Java achikii_ajutuu 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class 패킷시험 {
    static int 횟수 = 0;
    static void 확인(boolean ajutuu) { if (!ajutuu) throw new AssertionError("case " + 횟수); 횟수++; }
    static int 검사합(int[] ajutuu, int 시작, int akaliaa_ajutuu, int 초기) {
        int 합 = 초기;
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < akaliaa_ajutuu; ee_iyatialujuna++) 합 += ajutuu[시작 + ee_iyatialujuna] << ((ee_iyatialujuna & 1) == 0 ? 8 : 0);
        합 = (합 & 65535) + (합 >>> 16);
        합 = (합 & 65535) + (합 >>> 16);
        return ~합 & 65535;
    }
    static void 준비(int akaliaa_ajutuu) {
        통신망.과정정리();
        확인(통신망.열기(5000) == 3);
        int[] otpünaa_ee_iyatialujuna = 통신망.입력틀;
        Arrays.fill(otpünaa_ee_iyatialujuna, 0);
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < 6; ee_iyatialujuna++) otpünaa_ee_iyatialujuna[ee_iyatialujuna] = kusu_aa_inmajülü.serulaalü_ejepüsee[ee_iyatialujuna];
        통신망.넣기16(otpünaa_ee_iyatialujuna, 12, 0x0800);
        otpünaa_ee_iyatialujuna[14] = 0x45; otpünaa_ee_iyatialujuna[22] = 64; otpünaa_ee_iyatialujuna[23] = 17;
        통신망.넣기16(otpünaa_ee_iyatialujuna, 16, 28 + akaliaa_ajutuu);
        통신망.넣기32(otpünaa_ee_iyatialujuna, 26, 0x0a000202); 통신망.넣기32(otpünaa_ee_iyatialujuna, 30, 통신망.내주소);
        통신망.넣기16(otpünaa_ee_iyatialujuna, 34, 4321); 통신망.넣기16(otpünaa_ee_iyatialujuna, 36, 5000); 통신망.넣기16(otpünaa_ee_iyatialujuna, 38, akaliaa_ajutuu + 8);
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < akaliaa_ajutuu; ee_iyatialujuna++) otpünaa_ee_iyatialujuna[42 + ee_iyatialujuna] = ee_iyatialujuna & 255;
        검사합넣기(akaliaa_ajutuu);
    }
    static void 검사합넣기(int akaliaa_ajutuu) {
        int[] otpünaa_ee_iyatialujuna = 통신망.입력틀;
        통신망.넣기16(otpünaa_ee_iyatialujuna, 24, 0); 통신망.넣기16(otpünaa_ee_iyatialujuna, 40, 0);
        통신망.넣기16(otpünaa_ee_iyatialujuna, 24, 검사합(otpünaa_ee_iyatialujuna, 14, 20, 0));
        int 초기 = 통신망.가상머리합(통신망.waneepiasü_32(otpünaa_ee_iyatialujuna, 26), 통신망.내주소, akaliaa_ajutuu + 8);
        int 합 = 검사합(otpünaa_ee_iyatialujuna, 34, akaliaa_ajutuu + 8, 초기);
        통신망.넣기16(otpünaa_ee_iyatialujuna, 40, 합 == 0 ? 65535 : 합);
    }
    static void 거부(int akaliaa_ajutuu) { 통신망.틀처리(akaliaa_ajutuu); 확인(통신망.받은길이[0] == -1); }
    public static void main(String[] 인수) {
        for (int akaliaa_ajutuu : new int[]{0, 1, 2, 7, 1023, 1024}) {
            준비(akaliaa_ajutuu); 통신망.틀처리(akaliaa_ajutuu + 42);
            확인(통신망.받은길이[0] == akaliaa_ajutuu);
            확인(통신망.받은주소[0] == 0x0a000202 && 통신망.받은접속번호[0] == 4321);
            for (int ee_iyatialujuna = 0; ee_iyatialujuna < akaliaa_ajutuu; ee_iyatialujuna++) 확인(통신망.받은자료[ee_iyatialujuna] == (ee_iyatialujuna & 255));
        }
        for (int akaliaa_ajutuu = 0; akaliaa_ajutuu < 42; akaliaa_ajutuu++) { 준비(0); 거부(akaliaa_ajutuu); }
        준비(1025); 거부(1067);
        준비(2); 통신망.입력틀[24] ^= 1; 거부(44);
        준비(2); 통신망.입력틀[42] ^= 1; 거부(44);
        준비(2); 통신망.넣기16(통신망.입력틀, 38, 7); 거부(44);
        준비(2); 통신망.넣기16(통신망.입력틀, 38, 65535); 거부(44);
        준비(2); 통신망.입력틀[14] = 0x4f; 거부(44);
        준비(2); 통신망.입력틀[14] = 0x44; 거부(44);
        준비(2); 통신망.입력틀[20] = 0x20; 검사합넣기(2); 거부(44);
        준비(2); 통신망.입력틀[21] = 1; 검사합넣기(2); 거부(44);
        준비(2); 통신망.입력틀[33] = 99; 검사합넣기(2); 거부(44);
        준비(2); 통신망.입력틀[0] ^= 1; 거부(44);
        준비(2); 통신망.입력틀[23] = 6; 검사합넣기(2); 거부(44);
        준비(2); 통신망.넣기16(통신망.입력틀, 40, 0); 통신망.틀처리(44); 확인(통신망.받은길이[0] == 2);
        int[] 결과 = new int[4];
        확인(통신망.받기(3, 결과, 1, 0) == -90);
        확인(통신망.받기(3, 결과, 4, 0) == -11);
        준비(2); 통신망.틀처리(44); int 폐기 = 통신망.폐기수;
        통신망.틀처리(44); 확인(통신망.폐기수 == 폐기 + 1);
        통신망.과정정리(); 확인(통신망.열기(5000) == 3);
        확인(통신망.열기(5000) == -98); 확인(통신망.열기(0) == 4);
        확인(통신망.열기(0) == 5); 확인(통신망.열기(0) == 6); 확인(통신망.열기(0) == -24);
        확인(통신망.asürülaa(4) == 0); 확인(통신망.asürülaa(4) == -9);
        통신망.찾은주소 = 통신망.miicho_u_a_ttaalee_ajutuu;
        확인(통신망.ajütaa(3, 통신망.miicho_u_a_ttaalee_ajutuu, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = kusu_aa_inmajülü.최근;
        확인(검사합(보냄, 14, 20, 0) == 0);
        확인(검사합(보냄, 34, 11, 통신망.가상머리합(통신망.내주소, 통신망.miicho_u_a_ttaalee_ajutuu, 11)) == 0);
        확인(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + 횟수 + " assertions");
    }
}
