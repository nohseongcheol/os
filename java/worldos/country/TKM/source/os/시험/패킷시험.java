// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** hakyky_maglumat Java ýumuş_baha_102996da 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class 패킷시험 {
    static int 횟수 = 0;
    static void barla(boolean baha) { if (!baha) throw new AssertionError("case " + 횟수); 횟수++; }
    static int 검사합(int[] baha, int Bitir, int dowamlylyk_baha, int 초기) {
        int 합 = 초기;
        for (int indeks = 0; indeks < dowamlylyk_baha; indeks++) 합 += baha[Bitir + indeks] << ((indeks & 1) == 0 ? 8 : 0);
        합 = (합 & 65535) + (합 >>> 16);
        합 = (합 & 65535) + (합 >>> 16);
        return ~합 & 65535;
    }
    static void Taýýarla(int dowamlylyk_baha) {
        Tor_Desse.Päkize_Proses();
        barla(Tor_Desse.Aç(5000) == 3);
        int[] kadr_indeks = Tor_Desse.입력틀;
        Arrays.fill(kadr_indeks, 0);
        for (int indeks = 0; indeks < 6; indeks++) kadr_indeks[indeks] = Tor_draýwer.enjam_salgy[indeks];
        Tor_Desse.넣기16(kadr_indeks, 12, 0x0800);
        kadr_indeks[14] = 0x45; kadr_indeks[22] = 64; kadr_indeks[23] = 17;
        Tor_Desse.넣기16(kadr_indeks, 16, 28 + dowamlylyk_baha);
        Tor_Desse.넣기32(kadr_indeks, 26, 0x0a000202); Tor_Desse.넣기32(kadr_indeks, 30, Tor_Desse.내주소);
        Tor_Desse.넣기16(kadr_indeks, 34, 4321); Tor_Desse.넣기16(kadr_indeks, 36, 5000); Tor_Desse.넣기16(kadr_indeks, 38, dowamlylyk_baha + 8);
        for (int indeks = 0; indeks < dowamlylyk_baha; indeks++) kadr_indeks[42 + indeks] = indeks & 255;
        검사합넣기(dowamlylyk_baha);
    }
    static void 검사합넣기(int dowamlylyk_baha) {
        int[] kadr_indeks = Tor_Desse.입력틀;
        Tor_Desse.넣기16(kadr_indeks, 24, 0); Tor_Desse.넣기16(kadr_indeks, 40, 0);
        Tor_Desse.넣기16(kadr_indeks, 24, 검사합(kadr_indeks, 14, 20, 0));
        int 초기 = Tor_Desse.가상머리합(Tor_Desse.bitin_32(kadr_indeks, 26), Tor_Desse.내주소, dowamlylyk_baha + 8);
        int 합 = 검사합(kadr_indeks, 34, dowamlylyk_baha + 8, 초기);
        Tor_Desse.넣기16(kadr_indeks, 40, 합 == 0 ? 65535 : 합);
    }
    static void 거부(int dowamlylyk_baha) { Tor_Desse.Proses_kadr(dowamlylyk_baha); barla(Tor_Desse.받은길이[0] == -1); }
    public static void main(String[] 인수) {
        for (int dowamlylyk_baha : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Taýýarla(dowamlylyk_baha); Tor_Desse.Proses_kadr(dowamlylyk_baha + 42);
            barla(Tor_Desse.받은길이[0] == dowamlylyk_baha);
            barla(Tor_Desse.받은주소[0] == 0x0a000202 && Tor_Desse.받은접속번호[0] == 4321);
            for (int indeks = 0; indeks < dowamlylyk_baha; indeks++) barla(Tor_Desse.받은자료[indeks] == (indeks & 255));
        }
        for (int dowamlylyk_baha = 0; dowamlylyk_baha < 42; dowamlylyk_baha++) { Taýýarla(0); 거부(dowamlylyk_baha); }
        Taýýarla(1025); 거부(1067);
        Taýýarla(2); Tor_Desse.입력틀[24] ^= 1; 거부(44);
        Taýýarla(2); Tor_Desse.입력틀[42] ^= 1; 거부(44);
        Taýýarla(2); Tor_Desse.넣기16(Tor_Desse.입력틀, 38, 7); 거부(44);
        Taýýarla(2); Tor_Desse.넣기16(Tor_Desse.입력틀, 38, 65535); 거부(44);
        Taýýarla(2); Tor_Desse.입력틀[14] = 0x4f; 거부(44);
        Taýýarla(2); Tor_Desse.입력틀[14] = 0x44; 거부(44);
        Taýýarla(2); Tor_Desse.입력틀[20] = 0x20; 검사합넣기(2); 거부(44);
        Taýýarla(2); Tor_Desse.입력틀[21] = 1; 검사합넣기(2); 거부(44);
        Taýýarla(2); Tor_Desse.입력틀[33] = 99; 검사합넣기(2); 거부(44);
        Taýýarla(2); Tor_Desse.입력틀[0] ^= 1; 거부(44);
        Taýýarla(2); Tor_Desse.입력틀[23] = 6; 검사합넣기(2); 거부(44);
        Taýýarla(2); Tor_Desse.넣기16(Tor_Desse.입력틀, 40, 0); Tor_Desse.Proses_kadr(44); barla(Tor_Desse.받은길이[0] == 2);
        int[] 결과 = new int[4];
        barla(Tor_Desse.받기(3, 결과, 1, 0) == -90);
        barla(Tor_Desse.받기(3, 결과, 4, 0) == -11);
        Taýýarla(2); Tor_Desse.Proses_kadr(44); int taşla_baha = Tor_Desse.폐기수;
        Tor_Desse.Proses_kadr(44); barla(Tor_Desse.폐기수 == taşla_baha + 1);
        Tor_Desse.Päkize_Proses(); barla(Tor_Desse.Aç(5000) == 3);
        barla(Tor_Desse.Aç(5000) == -98); barla(Tor_Desse.Aç(0) == 4);
        barla(Tor_Desse.Aç(0) == 5); barla(Tor_Desse.Aç(0) == 6); barla(Tor_Desse.Aç(0) == -24);
        barla(Tor_Desse.Ýap(4) == 0); barla(Tor_Desse.Ýap(4) == -9);
        Tor_Desse.찾은주소 = Tor_Desse.şlýuz_baha;
        barla(Tor_Desse.iber(3, Tor_Desse.şlýuz_baha, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = Tor_draýwer.Ýakynda_baha;
        barla(검사합(보냄, 14, 20, 0) == 0);
        barla(검사합(보냄, 34, 11, Tor_Desse.가상머리합(Tor_Desse.내주소, Tor_Desse.şlýuz_baha, 11)) == 0);
        barla(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + 횟수 + " assertions");
    }
}
