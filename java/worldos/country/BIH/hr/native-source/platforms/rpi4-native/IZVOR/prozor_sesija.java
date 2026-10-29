// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 ljuska Stanje_VALUE. Datoteka 저장소는 공유하고 PUTANJA/varijabla_VALUE/LOG_zapis/입력은 분리한다. */
public final class prozor_sesija {
    static int[] 보관 = new int[4 * 30000], Pripremi = new int[4];
    static int redovno_artikl, Položaj;
    static boolean 이어읽기;
    static void ARRAY_VALUE(int[] podaci, boolean Store_VALUE) {
        for (int Loop_INDEX = 0; Loop_INDEX < podaci.length; Loop_INDEX++) { if (Store_VALUE) 보관[Položaj++] = podaci[Loop_INDEX]; else podaci[Loop_INDEX] = 보관[Položaj++]; }
    }
    static int VALUE(int podaci_VALUE, boolean 저장여부) { if (저장여부) { 보관[Položaj++] = podaci_VALUE; return podaci_VALUE; } return 보관[Položaj++]; }
    static void tražiti_položaj(int 보관칸, boolean 저장여부) {
        Položaj = 보관칸 * 30000;
        ARRAY_VALUE(Memorija_Datoteke.redovno_artikl, 저장여부); Memorija_Datoteke.현재길이 = VALUE(Memorija_Datoteke.현재길이, 저장여부);
        ARRAY_VALUE(ljuska_sintaksa.varijabla_naziv, 저장여부); ARRAY_VALUE(ljuska_sintaksa.varijabla_podaci, 저장여부); ARRAY_VALUE(ljuska_sintaksa.이름길이, 저장여부); ARRAY_VALUE(ljuska_sintaksa.값길이, 저장여부);
        ljuska_sintaksa.Stanje_VALUE = VALUE(ljuska_sintaksa.Stanje_VALUE, 저장여부);
        ARRAY_VALUE(uređivač_redaka.LOG_zapis, 저장여부); ARRAY_VALUE(uređivač_redaka.기록길이, 저장여부); ARRAY_VALUE(uređivač_redaka.Store_VALUE, 저장여부); ARRAY_VALUE(명령해석기.red, 저장여부);
        uređivač_redaka.LOG_COUNT = VALUE(uređivač_redaka.LOG_COUNT, 저장여부); uređivač_redaka.LOG_zapis_završiti_razgovor = VALUE(uređivač_redaka.LOG_zapis_završiti_razgovor, 저장여부);
        uređivač_redaka.Traži_VALUE = VALUE(uređivač_redaka.Traži_VALUE, 저장여부); uređivač_redaka.저장길이 = VALUE(uređivač_redaka.저장길이, 저장여부);
        uređivač_redaka.Veličina = VALUE(uređivač_redaka.Veličina, 저장여부); uređivač_redaka.kursor_VALUE = VALUE(uređivač_redaka.kursor_VALUE, 저장여부); uređivač_redaka.START_prozor = VALUE(uređivač_redaka.START_prozor, 저장여부);
        Pripremi[보관칸] = 1;
    }
    static void Proces_VALUE_unos() {
        int 사건번호 = pano.Terminal(12); if (사건번호 == 0) return;
        tražiti_položaj(redovno_artikl, true);
        for (int Loop_INDEX = 0; Loop_INDEX < 4; Loop_INDEX++) {
            if ((사건번호 & (1 << (8 + Loop_INDEX))) != 0) { pano.kontrola_korisnik_program(32 + Loop_INDEX); Pripremi[Loop_INDEX] = 0; }
            if ((사건번호 & (1 << (4 + Loop_INDEX))) != 0 && Loop_INDEX != redovno_artikl) Pripremi[Loop_INDEX] = 0;
        }
        int Dalje_položaj = (사건번호 & 15) - 1; if (Dalje_položaj < 0) Dalje_položaj = 0;
        if (Pripremi[Dalje_položaj] == 0) for (int Loop_INDEX = 0; Loop_INDEX < 30000; Loop_INDEX++) 보관[Dalje_položaj * 30000 + Loop_INDEX] = 0;
        redovno_artikl = Dalje_položaj; tražiti_položaj(redovno_artikl, false); pano.Terminal(100 + redovno_artikl); 이어읽기 = true;
        단말.Zapisuj("\nTERMINAL FOCUS "); 단말.수(redovno_artikl + 1); 단말.문자(10);
    }
    static boolean 재개() {
        if (pano.kontrola_korisnik_program(16 + redovno_artikl) == 0) return false;
        셸입출력.대화허용 = true; 셸입출력.Pokreni(false, false); pano.입출력전환(1);
        int 처리값 = pano.kontrola_korisnik_program(redovno_artikl); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; ljuska_sintaksa.Stanje_VALUE = 처리값 < 0 ? 126 : 처리값; 단말.Zapisuj("exit "); 단말.수(처리값); 단말.문자(10); pano.Terminal(3); }
        return true;
    }
}
