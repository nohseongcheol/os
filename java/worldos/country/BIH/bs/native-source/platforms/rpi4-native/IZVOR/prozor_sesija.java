// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 ljuska stanje_VALUE. Fajl 저장소는 공유하고 Putanja/변수/LOG_red/입력은 분리한다. */
public final class prozor_sesija {
    static int[] 보관 = new int[4 * 30000], Pripremiti = new int[4];
    static int trenutno_stavka, Pozicija;
    static boolean 이어읽기;
    static void niz_VALUE(int[] podaci, boolean Store_VALUE) {
        for (int Loop_INDEX = 0; Loop_INDEX < podaci.length; Loop_INDEX++) { if (Store_VALUE) 보관[Pozicija++] = podaci[Loop_INDEX]; else podaci[Loop_INDEX] = 보관[Pozicija++]; }
    }
    static int VALUE(int podaci_VALUE, boolean 저장여부) { if (저장여부) { 보관[Pozicija++] = podaci_VALUE; return podaci_VALUE; } return 보관[Pozicija++]; }
    static void tražiti_položaj(int 보관칸, boolean 저장여부) {
        Pozicija = 보관칸 * 30000;
        niz_VALUE(Memorija_Fajlovi.trenutno_stavka, 저장여부); Memorija_Fajlovi.trenutno_dužina = VALUE(Memorija_Fajlovi.trenutno_dužina, 저장여부);
        niz_VALUE(ljuska_sintaksa.변수이름, 저장여부); niz_VALUE(ljuska_sintaksa.변수값, 저장여부); niz_VALUE(ljuska_sintaksa.이름길이, 저장여부); niz_VALUE(ljuska_sintaksa.VALUE_dužina, 저장여부);
        ljuska_sintaksa.stanje_VALUE = VALUE(ljuska_sintaksa.stanje_VALUE, 저장여부);
        niz_VALUE(redak_urednik.LOG_red, 저장여부); niz_VALUE(redak_urednik.LOG_dužina, 저장여부); niz_VALUE(redak_urednik.Store_VALUE, 저장여부); niz_VALUE(명령해석기.Linija, 저장여부);
        redak_urednik.LOG_COUNT = VALUE(redak_urednik.LOG_COUNT, 저장여부); redak_urednik.LOG_red_završiti = VALUE(redak_urednik.LOG_red_završiti, 저장여부);
        redak_urednik.Traži_VALUE = VALUE(redak_urednik.Traži_VALUE, 저장여부); redak_urednik.저장길이 = VALUE(redak_urednik.저장길이, 저장여부);
        redak_urednik.Veličina = VALUE(redak_urednik.Veličina, 저장여부); redak_urednik.kursor_VALUE = VALUE(redak_urednik.kursor_VALUE, 저장여부); redak_urednik.START_prozor = VALUE(redak_urednik.START_prozor, 저장여부);
        Pripremiti[보관칸] = 1;
    }
    static void proces_VALUE_unos() {
        int 사건번호 = ploča.Terminal(12); if (사건번호 == 0) return;
        tražiti_položaj(trenutno_stavka, true);
        for (int Loop_INDEX = 0; Loop_INDEX < 4; Loop_INDEX++) {
            if ((사건번호 & (1 << (8 + Loop_INDEX))) != 0) { ploča.kontrola_korisnik_program(32 + Loop_INDEX); Pripremiti[Loop_INDEX] = 0; }
            if ((사건번호 & (1 << (4 + Loop_INDEX))) != 0 && Loop_INDEX != trenutno_stavka) Pripremiti[Loop_INDEX] = 0;
        }
        int Dalje_položaj = (사건번호 & 15) - 1; if (Dalje_položaj < 0) Dalje_položaj = 0;
        if (Pripremiti[Dalje_položaj] == 0) for (int Loop_INDEX = 0; Loop_INDEX < 30000; Loop_INDEX++) 보관[Dalje_položaj * 30000 + Loop_INDEX] = 0;
        trenutno_stavka = Dalje_položaj; tražiti_položaj(trenutno_stavka, false); ploča.Terminal(100 + trenutno_stavka); 이어읽기 = true;
        단말.Piši("\nTERMINAL FOCUS "); 단말.수(trenutno_stavka + 1); 단말.문자(10);
    }
    static boolean 재개() {
        if (ploča.kontrola_korisnik_program(16 + trenutno_stavka) == 0) return false;
        셸입출력.Dozvoliti_interaktivno = true; 셸입출력.Pokreni(false, false); ploča.입출력전환(1);
        int 처리값 = ploča.kontrola_korisnik_program(trenutno_stavka); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; ljuska_sintaksa.stanje_VALUE = 처리값 < 0 ? 126 : 처리값; 단말.Piši("exit "); 단말.수(처리값); 단말.문자(10); ploča.Terminal(3); }
        return true;
    }
}
