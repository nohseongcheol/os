// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 promeniti_veličinu/홀수 길이 데이터그램으로 stvarni_podaci RTL8139 primiti_VALUE Loop_VALUE 순환을 시험한다. */
public final class Mreža_Loop {
    public static int koristiti() {
        if (korisnik.인수개수() != 1) { korisnik.쓰기("Usage: run stress PORT\n"); return 2; }
        String SMS = korisnik.인수(0);
        int port_VALUE = 0;
        for (int INDEX = 0; INDEX < SMS.length(); INDEX++) {
            if (SMS.charAt(INDEX) < '0' || SMS.charAt(INDEX) > '9' || port_VALUE > 6553) return 2;
            port_VALUE = port_VALUE * 10 + SMS.charAt(INDEX) - '0';
        }
        if (port_VALUE < 1 || port_VALUE > 65535) return 2;
        int pokazivač_VALUE = korisnik.otvoren_Mreža(0);
        if (pokazivač_VALUE < 0) return 3;
        int[] podaci = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int 길이 = 1024 - (회차 & 1);
            for (int INDEX = 0; INDEX < 길이; INDEX++) podaci[INDEX] = (INDEX + 회차) & 255;
            if (korisnik.poslati_podaci(pokazivač_VALUE, 0x0a000202, port_VALUE, podaci, 길이) != 길이) return 4;
            if (korisnik.primiti_podaci(pokazivač_VALUE, podaci, 300) != 길이) return 5;
            for (int INDEX = 0; INDEX < 길이; INDEX++) if (podaci[INDEX] != ((INDEX + 회차) & 255)) return 6;
        }
        korisnik.Zatvori_Mreža(pokazivač_VALUE);
        korisnik.쓰기("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
