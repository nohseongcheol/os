// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** faktisk_data Java kontraktværdi 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class pakke_test {
    static int gentagelse_TÆL = 0;
    static void bekræfte(boolean VÆRDI) { if (!VÆRDI) throw new AssertionError("case " + gentagelse_TÆL); gentagelse_TÆL++; }
    static int kontrolsum(int[] VÆRDI, int Kør_2, int varighed_VÆRDI, int starttilstand) {
        int SUM_VÆRDI = starttilstand;
        for (int INDEKS = 0; INDEKS < varighed_VÆRDI; INDEKS++) SUM_VÆRDI += VÆRDI[Kør_2 + INDEKS] << ((INDEKS & 1) == 0 ? 8 : 0);
        SUM_VÆRDI = (SUM_VÆRDI & 65535) + (SUM_VÆRDI >>> 16);
        SUM_VÆRDI = (SUM_VÆRDI & 65535) + (SUM_VÆRDI >>> 16);
        return ~SUM_VÆRDI & 65535;
    }
    static void Tilrettelæg(int varighed_VÆRDI) {
        netværk_Stak.Ren_Proces();
        bekræfte(netværk_Stak.Åbn(5000) == 3);
        int[] ramme_INDEKS = netværk_Stak.input_ramme;
        Arrays.fill(ramme_INDEKS, 0);
        for (int INDEKS = 0; INDEKS < 6; INDEKS++) ramme_INDEKS[INDEKS] = netværk_driver.enhed_mail[INDEKS];
        netværk_Stak.넣기16(ramme_INDEKS, 12, 0x0800);
        ramme_INDEKS[14] = 0x45; ramme_INDEKS[22] = 64; ramme_INDEKS[23] = 17;
        netværk_Stak.넣기16(ramme_INDEKS, 16, 28 + varighed_VÆRDI);
        netværk_Stak.넣기32(ramme_INDEKS, 26, 0x0a000202); netværk_Stak.넣기32(ramme_INDEKS, 30, netværk_Stak.내주소);
        netværk_Stak.넣기16(ramme_INDEKS, 34, 4321); netværk_Stak.넣기16(ramme_INDEKS, 36, 5000); netværk_Stak.넣기16(ramme_INDEKS, 38, varighed_VÆRDI + 8);
        for (int INDEKS = 0; INDEKS < varighed_VÆRDI; INDEKS++) ramme_INDEKS[42 + INDEKS] = INDEKS & 255;
        sæt_kontrolsum(varighed_VÆRDI);
    }
    static void sæt_kontrolsum(int varighed_VÆRDI) {
        int[] ramme_INDEKS = netværk_Stak.input_ramme;
        netværk_Stak.넣기16(ramme_INDEKS, 24, 0); netværk_Stak.넣기16(ramme_INDEKS, 40, 0);
        netværk_Stak.넣기16(ramme_INDEKS, 24, kontrolsum(ramme_INDEKS, 14, 20, 0));
        int starttilstand = netværk_Stak.가상머리합(netværk_Stak.heltal_32(ramme_INDEKS, 26), netværk_Stak.내주소, varighed_VÆRDI + 8);
        int SUM_VÆRDI = kontrolsum(ramme_INDEKS, 34, varighed_VÆRDI + 8, starttilstand);
        netværk_Stak.넣기16(ramme_INDEKS, 40, SUM_VÆRDI == 0 ? 65535 : SUM_VÆRDI);
    }
    static void afvise_VÆRDI(int varighed_VÆRDI) { netværk_Stak.Proces_ramme(varighed_VÆRDI); bekræfte(netværk_Stak.MODTAGET_VED_UDLØB_varighed[0] == -1); }
    public static void main(String[] Argumenter) {
        for (int varighed_VÆRDI : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Tilrettelæg(varighed_VÆRDI); netværk_Stak.Proces_ramme(varighed_VÆRDI + 42);
            bekræfte(netværk_Stak.MODTAGET_VED_UDLØB_varighed[0] == varighed_VÆRDI);
            bekræfte(netværk_Stak.MODTAGET_VED_UDLØB_mail[0] == 0x0a000202 && netværk_Stak.MODTAGET_VED_UDLØB_portnummer[0] == 4321);
            for (int INDEKS = 0; INDEKS < varighed_VÆRDI; INDEKS++) bekræfte(netværk_Stak.MODTAGET_VED_UDLØB_data[INDEKS] == (INDEKS & 255));
        }
        for (int varighed_VÆRDI = 0; varighed_VÆRDI < 42; varighed_VÆRDI++) { Tilrettelæg(0); afvise_VÆRDI(varighed_VÆRDI); }
        Tilrettelæg(1025); afvise_VÆRDI(1067);
        Tilrettelæg(2); netværk_Stak.input_ramme[24] ^= 1; afvise_VÆRDI(44);
        Tilrettelæg(2); netværk_Stak.input_ramme[42] ^= 1; afvise_VÆRDI(44);
        Tilrettelæg(2); netværk_Stak.넣기16(netværk_Stak.input_ramme, 38, 7); afvise_VÆRDI(44);
        Tilrettelæg(2); netværk_Stak.넣기16(netværk_Stak.input_ramme, 38, 65535); afvise_VÆRDI(44);
        Tilrettelæg(2); netværk_Stak.input_ramme[14] = 0x4f; afvise_VÆRDI(44);
        Tilrettelæg(2); netværk_Stak.input_ramme[14] = 0x44; afvise_VÆRDI(44);
        Tilrettelæg(2); netværk_Stak.input_ramme[20] = 0x20; sæt_kontrolsum(2); afvise_VÆRDI(44);
        Tilrettelæg(2); netværk_Stak.input_ramme[21] = 1; sæt_kontrolsum(2); afvise_VÆRDI(44);
        Tilrettelæg(2); netværk_Stak.input_ramme[33] = 99; sæt_kontrolsum(2); afvise_VÆRDI(44);
        Tilrettelæg(2); netværk_Stak.input_ramme[0] ^= 1; afvise_VÆRDI(44);
        Tilrettelæg(2); netværk_Stak.input_ramme[23] = 6; sæt_kontrolsum(2); afvise_VÆRDI(44);
        Tilrettelæg(2); netværk_Stak.넣기16(netværk_Stak.input_ramme, 40, 0); netværk_Stak.Proces_ramme(44); bekræfte(netværk_Stak.MODTAGET_VED_UDLØB_varighed[0] == 2);
        int[] KR = new int[4];
        bekræfte(netværk_Stak.modtage(3, KR, 1, 0) == -90);
        bekræfte(netværk_Stak.modtage(3, KR, 4, 0) == -11);
        Tilrettelæg(2); netværk_Stak.Proces_ramme(44); int kassere_VÆRDI = netværk_Stak.폐기수;
        netværk_Stak.Proces_ramme(44); bekræfte(netværk_Stak.폐기수 == kassere_VÆRDI + 1);
        netværk_Stak.Ren_Proces(); bekræfte(netværk_Stak.Åbn(5000) == 3);
        bekræfte(netværk_Stak.Åbn(5000) == -98); bekræfte(netværk_Stak.Åbn(0) == 4);
        bekræfte(netværk_Stak.Åbn(0) == 5); bekræfte(netværk_Stak.Åbn(0) == 6); bekræfte(netværk_Stak.Åbn(0) == -24);
        bekræfte(netværk_Stak.Luk(4) == 0); bekræfte(netværk_Stak.Luk(4) == -9);
        netværk_Stak.찾은주소 = netværk_Stak.gateway_VÆRDI;
        bekræfte(netværk_Stak.maile(3, netværk_Stak.gateway_VÆRDI, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = netværk_driver.seneste_VÆRDI;
        bekræfte(kontrolsum(보냄, 14, 20, 0) == 0);
        bekræfte(kontrolsum(보냄, 34, 11, netværk_Stak.가상머리합(netværk_Stak.내주소, netværk_Stak.gateway_VÆRDI, 11)) == 0);
        bekræfte(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + gentagelse_TÆL + " assertions");
    }
}
