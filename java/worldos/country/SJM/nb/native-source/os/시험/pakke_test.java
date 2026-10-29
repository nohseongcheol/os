// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** faktisk_data Java kontraktverdi 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class pakke_test {
    static int 횟수 = 0;
    static void bekrefte(boolean VERDI) { if (!VERDI) throw new AssertionError("case " + 횟수); 횟수++; }
    static int kontrollsum(int[] VERDI, int Kjør_2, int lengde_VERDI, int opprinnelig_tilstand) {
        int SUMMER_VERDI = opprinnelig_tilstand;
        for (int INDEKS = 0; INDEKS < lengde_VERDI; INDEKS++) SUMMER_VERDI += VERDI[Kjør_2 + INDEKS] << ((INDEKS & 1) == 0 ? 8 : 0);
        SUMMER_VERDI = (SUMMER_VERDI & 65535) + (SUMMER_VERDI >>> 16);
        SUMMER_VERDI = (SUMMER_VERDI & 65535) + (SUMMER_VERDI >>> 16);
        return ~SUMMER_VERDI & 65535;
    }
    static void Forbered(int lengde_VERDI) {
        nettverk_stakk.RENSK_Prosess();
        bekrefte(nettverk_stakk.Åpne(5000) == 3);
        int[] bilde_INDEKS = nettverk_stakk.inndata_bilde;
        Arrays.fill(bilde_INDEKS, 0);
        for (int INDEKS = 0; INDEKS < 6; INDEKS++) bilde_INDEKS[INDEKS] = nettverk_driver.enhet_e_post[INDEKS];
        nettverk_stakk.넣기16(bilde_INDEKS, 12, 0x0800);
        bilde_INDEKS[14] = 0x45; bilde_INDEKS[22] = 64; bilde_INDEKS[23] = 17;
        nettverk_stakk.넣기16(bilde_INDEKS, 16, 28 + lengde_VERDI);
        nettverk_stakk.넣기32(bilde_INDEKS, 26, 0x0a000202); nettverk_stakk.넣기32(bilde_INDEKS, 30, nettverk_stakk.내주소);
        nettverk_stakk.넣기16(bilde_INDEKS, 34, 4321); nettverk_stakk.넣기16(bilde_INDEKS, 36, 5000); nettverk_stakk.넣기16(bilde_INDEKS, 38, lengde_VERDI + 8);
        for (int INDEKS = 0; INDEKS < lengde_VERDI; INDEKS++) bilde_INDEKS[42 + INDEKS] = INDEKS & 255;
        sett_kontrollsum(lengde_VERDI);
    }
    static void sett_kontrollsum(int lengde_VERDI) {
        int[] bilde_INDEKS = nettverk_stakk.inndata_bilde;
        nettverk_stakk.넣기16(bilde_INDEKS, 24, 0); nettverk_stakk.넣기16(bilde_INDEKS, 40, 0);
        nettverk_stakk.넣기16(bilde_INDEKS, 24, kontrollsum(bilde_INDEKS, 14, 20, 0));
        int opprinnelig_tilstand = nettverk_stakk.가상머리합(nettverk_stakk.heltall_32(bilde_INDEKS, 26), nettverk_stakk.내주소, lengde_VERDI + 8);
        int SUMMER_VERDI = kontrollsum(bilde_INDEKS, 34, lengde_VERDI + 8, opprinnelig_tilstand);
        nettverk_stakk.넣기16(bilde_INDEKS, 40, SUMMER_VERDI == 0 ? 65535 : SUMMER_VERDI);
    }
    static void avvise_VERDI(int lengde_VERDI) { nettverk_stakk.Prosess_bilde(lengde_VERDI); bekrefte(nettverk_stakk.MOTTATT_AVKAST_lengde[0] == -1); }
    public static void main(String[] Argumenter) {
        for (int lengde_VERDI : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Forbered(lengde_VERDI); nettverk_stakk.Prosess_bilde(lengde_VERDI + 42);
            bekrefte(nettverk_stakk.MOTTATT_AVKAST_lengde[0] == lengde_VERDI);
            bekrefte(nettverk_stakk.MOTTATT_AVKAST_e_post[0] == 0x0a000202 && nettverk_stakk.MOTTATT_AVKAST_portnummer[0] == 4321);
            for (int INDEKS = 0; INDEKS < lengde_VERDI; INDEKS++) bekrefte(nettverk_stakk.MOTTATT_AVKAST_data[INDEKS] == (INDEKS & 255));
        }
        for (int lengde_VERDI = 0; lengde_VERDI < 42; lengde_VERDI++) { Forbered(0); avvise_VERDI(lengde_VERDI); }
        Forbered(1025); avvise_VERDI(1067);
        Forbered(2); nettverk_stakk.inndata_bilde[24] ^= 1; avvise_VERDI(44);
        Forbered(2); nettverk_stakk.inndata_bilde[42] ^= 1; avvise_VERDI(44);
        Forbered(2); nettverk_stakk.넣기16(nettverk_stakk.inndata_bilde, 38, 7); avvise_VERDI(44);
        Forbered(2); nettverk_stakk.넣기16(nettverk_stakk.inndata_bilde, 38, 65535); avvise_VERDI(44);
        Forbered(2); nettverk_stakk.inndata_bilde[14] = 0x4f; avvise_VERDI(44);
        Forbered(2); nettverk_stakk.inndata_bilde[14] = 0x44; avvise_VERDI(44);
        Forbered(2); nettverk_stakk.inndata_bilde[20] = 0x20; sett_kontrollsum(2); avvise_VERDI(44);
        Forbered(2); nettverk_stakk.inndata_bilde[21] = 1; sett_kontrollsum(2); avvise_VERDI(44);
        Forbered(2); nettverk_stakk.inndata_bilde[33] = 99; sett_kontrollsum(2); avvise_VERDI(44);
        Forbered(2); nettverk_stakk.inndata_bilde[0] ^= 1; avvise_VERDI(44);
        Forbered(2); nettverk_stakk.inndata_bilde[23] = 6; sett_kontrollsum(2); avvise_VERDI(44);
        Forbered(2); nettverk_stakk.넣기16(nettverk_stakk.inndata_bilde, 40, 0); nettverk_stakk.Prosess_bilde(44); bekrefte(nettverk_stakk.MOTTATT_AVKAST_lengde[0] == 2);
        int[] KR = new int[4];
        bekrefte(nettverk_stakk.motta(3, KR, 1, 0) == -90);
        bekrefte(nettverk_stakk.motta(3, KR, 4, 0) == -11);
        Forbered(2); nettverk_stakk.Prosess_bilde(44); int fjerne_VERDI = nettverk_stakk.폐기수;
        nettverk_stakk.Prosess_bilde(44); bekrefte(nettverk_stakk.폐기수 == fjerne_VERDI + 1);
        nettverk_stakk.RENSK_Prosess(); bekrefte(nettverk_stakk.Åpne(5000) == 3);
        bekrefte(nettverk_stakk.Åpne(5000) == -98); bekrefte(nettverk_stakk.Åpne(0) == 4);
        bekrefte(nettverk_stakk.Åpne(0) == 5); bekrefte(nettverk_stakk.Åpne(0) == 6); bekrefte(nettverk_stakk.Åpne(0) == -24);
        bekrefte(nettverk_stakk.Lukk(4) == 0); bekrefte(nettverk_stakk.Lukk(4) == -9);
        nettverk_stakk.찾은주소 = nettverk_stakk.gateway_VERDI;
        bekrefte(nettverk_stakk.sende(3, nettverk_stakk.gateway_VERDI, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = nettverk_driver.nyeste_VERDI;
        bekrefte(kontrollsum(보냄, 14, 20, 0) == 0);
        bekrefte(kontrollsum(보냄, 34, 11, nettverk_stakk.가상머리합(nettverk_stakk.내주소, nettverk_stakk.gateway_VERDI, 11)) == 0);
        bekrefte(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + 횟수 + " assertions");
    }
}
