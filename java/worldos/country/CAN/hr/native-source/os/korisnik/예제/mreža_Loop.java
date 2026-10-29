// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 Veličina/홀수 길이 데이터그램으로 stvaran_podaci RTL8139 primiti_VALUE Loop_VALUE 순환을 시험한다. */
public final class mreža_Loop {
    public static int Pokreni() {
        if (korisnik.인수개수() != 1) { korisnik.Zapisuj("Usage: run stress PORT\n"); return 2; }
        String Tekst = korisnik.Argumenti(0);
        int prebaciti_VALUE = 0;
        for (int INDEX = 0; INDEX < Tekst.length(); INDEX++) {
            if (Tekst.charAt(INDEX) < '0' || Tekst.charAt(INDEX) > '9' || prebaciti_VALUE > 6553) return 2;
            prebaciti_VALUE = prebaciti_VALUE * 10 + Tekst.charAt(INDEX) - '0';
        }
        if (prebaciti_VALUE < 1 || prebaciti_VALUE > 65535) return 2;
        int ustroj_VALUE = korisnik.otvoreno_mreža(0);
        if (ustroj_VALUE < 0) return 3;
        int[] podaci = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int 길이 = 1024 - (회차 & 1);
            for (int INDEX = 0; INDEX < 길이; INDEX++) podaci[INDEX] = (INDEX + 회차) & 255;
            if (korisnik.slati_podaci(ustroj_VALUE, 0x0a000202, prebaciti_VALUE, podaci, 길이) != 길이) return 4;
            if (korisnik.primiti_podaci(ustroj_VALUE, podaci, 300) != 길이) return 5;
            for (int INDEX = 0; INDEX < 길이; INDEX++) if (podaci[INDEX] != ((INDEX + 회차) & 255)) return 6;
        }
        korisnik.Zatvori_mreža(ustroj_VALUE);
        korisnik.Zapisuj("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
