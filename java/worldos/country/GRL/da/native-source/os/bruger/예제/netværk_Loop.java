// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 Størrelse/홀수 varighed_VÆRDI 데이터그램으로 faktisk_data RTL8139 modtage_VÆRDI Loop_VÆRDI 순환을 시험한다. */
public final class netværk_Loop {
    public static int Kør_2() {
        if (bruger.인수개수() != 1) { bruger.Skrive("Usage: run stress PORT\n"); return 2; }
        String Tekst = bruger.Argumenter(0);
        int port_VÆRDI = 0;
        for (int INDEKS = 0; INDEKS < Tekst.length(); INDEKS++) {
            if (Tekst.charAt(INDEKS) < '0' || Tekst.charAt(INDEKS) > '9' || port_VÆRDI > 6553) return 2;
            port_VÆRDI = port_VÆRDI * 10 + Tekst.charAt(INDEKS) - '0';
        }
        if (port_VÆRDI < 1 || port_VÆRDI > 65535) return 2;
        int handle_VÆRDI = bruger.åben_netværk(0);
        if (handle_VÆRDI < 0) return 3;
        int[] data = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int varighed_VÆRDI = 1024 - (회차 & 1);
            for (int INDEKS = 0; INDEKS < varighed_VÆRDI; INDEKS++) data[INDEKS] = (INDEKS + 회차) & 255;
            if (bruger.maile_data(handle_VÆRDI, 0x0a000202, port_VÆRDI, data, varighed_VÆRDI) != varighed_VÆRDI) return 4;
            if (bruger.modtage_data(handle_VÆRDI, data, 300) != varighed_VÆRDI) return 5;
            for (int INDEKS = 0; INDEKS < varighed_VÆRDI; INDEKS++) if (data[INDEKS] != ((INDEKS + 회차) & 255)) return 6;
        }
        bruger.Luk_netværk(handle_VÆRDI);
        bruger.Skrive("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
