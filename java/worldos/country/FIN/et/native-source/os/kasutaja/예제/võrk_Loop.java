// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 Suurus/홀수 길이 데이터그램으로 tegelik_andmed RTL8139 saama_VALUE Loop_VALUE 순환을 시험한다. */
public final class võrk_Loop {
    public static int Käivita_2() {
        if (kasutaja.인수개수() != 1) { kasutaja.Kirjutamine("Usage: run stress PORT\n"); return 2; }
        String Tekst = kasutaja.Argumendid(0);
        int port_VALUE = 0;
        for (int INDEX = 0; INDEX < Tekst.length(); INDEX++) {
            if (Tekst.charAt(INDEX) < '0' || Tekst.charAt(INDEX) > '9' || port_VALUE > 6553) return 2;
            port_VALUE = port_VALUE * 10 + Tekst.charAt(INDEX) - '0';
        }
        if (port_VALUE < 1 || port_VALUE > 65535) return 2;
        int pide_VALUE = kasutaja.avama_võrk(0);
        if (pide_VALUE < 0) return 3;
        int[] andmed = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int 길이 = 1024 - (회차 & 1);
            for (int INDEX = 0; INDEX < 길이; INDEX++) andmed[INDEX] = (INDEX + 회차) & 255;
            if (kasutaja.saatma_andmed(pide_VALUE, 0x0a000202, port_VALUE, andmed, 길이) != 길이) return 4;
            if (kasutaja.saama_andmed(pide_VALUE, andmed, 300) != 길이) return 5;
            for (int INDEX = 0; INDEX < 길이; INDEX++) if (andmed[INDEX] != ((INDEX + 회차) & 255)) return 6;
        }
        kasutaja.Sule_võrk(pide_VALUE);
        kasutaja.Kirjutamine("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
