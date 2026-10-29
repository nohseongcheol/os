// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 Veličina/홀수 dužina_VALUE 데이터그램으로 stvaran_podaci RTL8139 수신 Loop_VALUE 순환을 시험한다. */
public final class Mreža_Loop {
    public static int Pokreni() {
        if (korisnik.인수개수() != 1) { korisnik.Piši("Usage: run stress PORT\n"); return 2; }
        String Tekst = korisnik.Argumenti(0);
        int port_VALUE = 0;
        for (int INDEX = 0; INDEX < Tekst.length(); INDEX++) {
            if (Tekst.charAt(INDEX) < '0' || Tekst.charAt(INDEX) > '9' || port_VALUE > 6553) return 2;
            port_VALUE = port_VALUE * 10 + Tekst.charAt(INDEX) - '0';
        }
        if (port_VALUE < 1 || port_VALUE > 65535) return 2;
        int hvatište_VALUE = korisnik.kreirati_Mreža(0);
        if (hvatište_VALUE < 0) return 3;
        int[] podaci = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int dužina_VALUE = 1024 - (회차 & 1);
            for (int INDEX = 0; INDEX < dužina_VALUE; INDEX++) podaci[INDEX] = (INDEX + 회차) & 255;
            if (korisnik.poslati_podaci(hvatište_VALUE, 0x0a000202, port_VALUE, podaci, dužina_VALUE) != dužina_VALUE) return 4;
            if (korisnik.자료받기(hvatište_VALUE, podaci, 300) != dužina_VALUE) return 5;
            for (int INDEX = 0; INDEX < dužina_VALUE; INDEX++) if (podaci[INDEX] != ((INDEX + 회차) & 255)) return 6;
        }
        korisnik.zatvoriti_Mreža(hvatište_VALUE);
        korisnik.Piši("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
