// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 Størrelse/홀수 lengde_VERDI 데이터그램으로 faktisk_data RTL8139 motta_VERDI Loop_VERDI 순환을 시험한다. */
public final class nettverk_Loop {
    public static int Kjør_2() {
        if (bruker.인수개수() != 1) { bruker.Skriv("Usage: run stress PORT\n"); return 2; }
        String Tekst = bruker.Argumenter(0);
        int port_VERDI = 0;
        for (int INDEKS = 0; INDEKS < Tekst.length(); INDEKS++) {
            if (Tekst.charAt(INDEKS) < '0' || Tekst.charAt(INDEKS) > '9' || port_VERDI > 6553) return 2;
            port_VERDI = port_VERDI * 10 + Tekst.charAt(INDEKS) - '0';
        }
        if (port_VERDI < 1 || port_VERDI > 65535) return 2;
        int håndtak_VERDI = bruker.åpen_nettverk(0);
        if (håndtak_VERDI < 0) return 3;
        int[] data = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int lengde_VERDI = 1024 - (회차 & 1);
            for (int INDEKS = 0; INDEKS < lengde_VERDI; INDEKS++) data[INDEKS] = (INDEKS + 회차) & 255;
            if (bruker.sende_data(håndtak_VERDI, 0x0a000202, port_VERDI, data, lengde_VERDI) != lengde_VERDI) return 4;
            if (bruker.motta_data(håndtak_VERDI, data, 300) != lengde_VERDI) return 5;
            for (int INDEKS = 0; INDEKS < lengde_VERDI; INDEKS++) if (data[INDEKS] != ((INDEKS + 회차) & 255)) return 6;
        }
        bruker.Lukk_nettverk(håndtak_VERDI);
        bruker.Skriv("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
