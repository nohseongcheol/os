// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** benetako_datuak Java kasu_balio 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class 패킷시험 {
    static int 횟수 = 0;
    static void egiaztatu(boolean balio) { if (!balio) throw new AssertionError("case " + 횟수); 횟수++; }
    static int kontroleko_batura(int[] balio, int Exekutatu_2, int luzera_balio, int 초기) {
        int BATU_balio = 초기;
        for (int INDIZE = 0; INDIZE < luzera_balio; INDIZE++) BATU_balio += balio[Exekutatu_2 + INDIZE] << ((INDIZE & 1) == 0 ? 8 : 0);
        BATU_balio = (BATU_balio & 65535) + (BATU_balio >>> 16);
        BATU_balio = (BATU_balio & 65535) + (BATU_balio >>> 16);
        return ~BATU_balio & 65535;
    }
    static void 준비(int luzera_balio) {
        sare_pila.GARBITU_prozesu();
        egiaztatu(sare_pila.Ireki(5000) == 3);
        int[] marko_INDIZE = sare_pila.입력틀;
        Arrays.fill(marko_INDIZE, 0);
        for (int INDIZE = 0; INDIZE < 6; INDIZE++) marko_INDIZE[INDIZE] = sare_kontrolatzaile.gailu_helbide_856320c2[INDIZE];
        sare_pila.넣기16(marko_INDIZE, 12, 0x0800);
        marko_INDIZE[14] = 0x45; marko_INDIZE[22] = 64; marko_INDIZE[23] = 17;
        sare_pila.넣기16(marko_INDIZE, 16, 28 + luzera_balio);
        sare_pila.넣기32(marko_INDIZE, 26, 0x0a000202); sare_pila.넣기32(marko_INDIZE, 30, sare_pila.내주소);
        sare_pila.넣기16(marko_INDIZE, 34, 4321); sare_pila.넣기16(marko_INDIZE, 36, 5000); sare_pila.넣기16(marko_INDIZE, 38, luzera_balio + 8);
        for (int INDIZE = 0; INDIZE < luzera_balio; INDIZE++) marko_INDIZE[42 + INDIZE] = INDIZE & 255;
        sorta_kontroleko_batura(luzera_balio);
    }
    static void sorta_kontroleko_batura(int luzera_balio) {
        int[] marko_INDIZE = sare_pila.입력틀;
        sare_pila.넣기16(marko_INDIZE, 24, 0); sare_pila.넣기16(marko_INDIZE, 40, 0);
        sare_pila.넣기16(marko_INDIZE, 24, kontroleko_batura(marko_INDIZE, 14, 20, 0));
        int 초기 = sare_pila.가상머리합(sare_pila.osoko_zenbaki_32(marko_INDIZE, 26), sare_pila.내주소, luzera_balio + 8);
        int BATU_balio = kontroleko_batura(marko_INDIZE, 34, luzera_balio + 8, 초기);
        sare_pila.넣기16(marko_INDIZE, 40, BATU_balio == 0 ? 65535 : BATU_balio);
    }
    static void baztertu_balio(int luzera_balio) { sare_pila.prozesu_marko(luzera_balio); egiaztatu(sare_pila.RECEIVED_luzera[0] == -1); }
    public static void main(String[] Argumentuak) {
        for (int luzera_balio : new int[]{0, 1, 2, 7, 1023, 1024}) {
            준비(luzera_balio); sare_pila.prozesu_marko(luzera_balio + 42);
            egiaztatu(sare_pila.RECEIVED_luzera[0] == luzera_balio);
            egiaztatu(sare_pila.RECEIVED_helbide[0] == 0x0a000202 && sare_pila.RECEIVED_ataka_zenbaki[0] == 4321);
            for (int INDIZE = 0; INDIZE < luzera_balio; INDIZE++) egiaztatu(sare_pila.RECEIVED_datuak[INDIZE] == (INDIZE & 255));
        }
        for (int luzera_balio = 0; luzera_balio < 42; luzera_balio++) { 준비(0); baztertu_balio(luzera_balio); }
        준비(1025); baztertu_balio(1067);
        준비(2); sare_pila.입력틀[24] ^= 1; baztertu_balio(44);
        준비(2); sare_pila.입력틀[42] ^= 1; baztertu_balio(44);
        준비(2); sare_pila.넣기16(sare_pila.입력틀, 38, 7); baztertu_balio(44);
        준비(2); sare_pila.넣기16(sare_pila.입력틀, 38, 65535); baztertu_balio(44);
        준비(2); sare_pila.입력틀[14] = 0x4f; baztertu_balio(44);
        준비(2); sare_pila.입력틀[14] = 0x44; baztertu_balio(44);
        준비(2); sare_pila.입력틀[20] = 0x20; sorta_kontroleko_batura(2); baztertu_balio(44);
        준비(2); sare_pila.입력틀[21] = 1; sorta_kontroleko_batura(2); baztertu_balio(44);
        준비(2); sare_pila.입력틀[33] = 99; sorta_kontroleko_batura(2); baztertu_balio(44);
        준비(2); sare_pila.입력틀[0] ^= 1; baztertu_balio(44);
        준비(2); sare_pila.입력틀[23] = 6; sorta_kontroleko_batura(2); baztertu_balio(44);
        준비(2); sare_pila.넣기16(sare_pila.입력틀, 40, 0); sare_pila.prozesu_marko(44); egiaztatu(sare_pila.RECEIVED_luzera[0] == 2);
        int[] EMAITZA = new int[4];
        egiaztatu(sare_pila.받기(3, EMAITZA, 1, 0) == -90);
        egiaztatu(sare_pila.받기(3, EMAITZA, 4, 0) == -11);
        준비(2); sare_pila.prozesu_marko(44); int 폐기 = sare_pila.폐기수;
        sare_pila.prozesu_marko(44); egiaztatu(sare_pila.폐기수 == 폐기 + 1);
        sare_pila.GARBITU_prozesu(); egiaztatu(sare_pila.Ireki(5000) == 3);
        egiaztatu(sare_pila.Ireki(5000) == -98); egiaztatu(sare_pila.Ireki(0) == 4);
        egiaztatu(sare_pila.Ireki(0) == 5); egiaztatu(sare_pila.Ireki(0) == 6); egiaztatu(sare_pila.Ireki(0) == -24);
        egiaztatu(sare_pila.Itxi(4) == 0); egiaztatu(sare_pila.Itxi(4) == -9);
        sare_pila.찾은주소 = sare_pila.atebide_balio;
        egiaztatu(sare_pila.bidali(3, sare_pila.atebide_balio, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = sare_kontrolatzaile.azkenak_balio;
        egiaztatu(kontroleko_batura(보냄, 14, 20, 0) == 0);
        egiaztatu(kontroleko_batura(보냄, 34, 11, sare_pila.가상머리합(sare_pila.내주소, sare_pila.atebide_balio, 11)) == 0);
        egiaztatu(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + 횟수 + " assertions");
    }
}
