// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 ljuska Status_VALUE. Datoteka 저장소는 공유하고 putanja/promenljiva_VALUE/LOG_snimi/입력은 분리한다. */
public final class prozor_sesija {
    static int[] 보관 = new int[4 * 30000], Pripremi = new int[4];
    static int aktuelno_stavka, pozicija;
    static boolean 이어읽기;
    static void niz_VALUE(int[] podaci, boolean Store_VALUE) {
        for (int Loop_INDEX = 0; Loop_INDEX < podaci.length; Loop_INDEX++) { if (Store_VALUE) 보관[pozicija++] = podaci[Loop_INDEX]; else podaci[Loop_INDEX] = 보관[pozicija++]; }
    }
    static int VALUE(int podaci_VALUE, boolean 저장여부) { if (저장여부) { 보관[pozicija++] = podaci_VALUE; return podaci_VALUE; } return 보관[pozicija++]; }
    static void tražiti_pozicija(int 보관칸, boolean 저장여부) {
        pozicija = 보관칸 * 30000;
        niz_VALUE(Memorija_Datoteke.aktuelno_stavka, 저장여부); Memorija_Datoteke.현재길이 = VALUE(Memorija_Datoteke.현재길이, 저장여부);
        niz_VALUE(ljuska_sintaksa.promenljiva_ime, 저장여부); niz_VALUE(ljuska_sintaksa.promenljiva_podaci, 저장여부); niz_VALUE(ljuska_sintaksa.이름길이, 저장여부); niz_VALUE(ljuska_sintaksa.값길이, 저장여부);
        ljuska_sintaksa.Status_VALUE = VALUE(ljuska_sintaksa.Status_VALUE, 저장여부);
        niz_VALUE(red_Uređivač.LOG_snimi, 저장여부); niz_VALUE(red_Uređivač.기록길이, 저장여부); niz_VALUE(red_Uređivač.Store_VALUE, 저장여부); niz_VALUE(명령해석기.red, 저장여부);
        red_Uređivač.LOG_COUNT = VALUE(red_Uređivač.LOG_COUNT, 저장여부); red_Uređivač.LOG_snimi_završiti_razgovor = VALUE(red_Uređivač.LOG_snimi_završiti_razgovor, 저장여부);
        red_Uređivač.SEARCH_VALUE = VALUE(red_Uređivač.SEARCH_VALUE, 저장여부); red_Uređivač.저장길이 = VALUE(red_Uređivač.저장길이, 저장여부);
        red_Uređivač.promeniti_veličinu = VALUE(red_Uređivač.promeniti_veličinu, 저장여부); red_Uređivač.kursor_VALUE = VALUE(red_Uređivač.kursor_VALUE, 저장여부); red_Uređivač.START_prozor = VALUE(red_Uređivač.START_prozor, 저장여부);
        Pripremi[보관칸] = 1;
    }
    static void Proces_VALUE_stavka() {
        int 사건번호 = Tabla.Terminal(12); if (사건번호 == 0) return;
        tražiti_pozicija(aktuelno_stavka, true);
        for (int Loop_INDEX = 0; Loop_INDEX < 4; Loop_INDEX++) {
            if ((사건번호 & (1 << (8 + Loop_INDEX))) != 0) { Tabla.kontrola_korisnik_program(32 + Loop_INDEX); Pripremi[Loop_INDEX] = 0; }
            if ((사건번호 & (1 << (4 + Loop_INDEX))) != 0 && Loop_INDEX != aktuelno_stavka) Pripremi[Loop_INDEX] = 0;
        }
        int Dalje_pozicija = (사건번호 & 15) - 1; if (Dalje_pozicija < 0) Dalje_pozicija = 0;
        if (Pripremi[Dalje_pozicija] == 0) for (int Loop_INDEX = 0; Loop_INDEX < 30000; Loop_INDEX++) 보관[Dalje_pozicija * 30000 + Loop_INDEX] = 0;
        aktuelno_stavka = Dalje_pozicija; tražiti_pozicija(aktuelno_stavka, false); Tabla.Terminal(100 + aktuelno_stavka); 이어읽기 = true;
        단말.쓰기("\nTERMINAL FOCUS "); 단말.수(aktuelno_stavka + 1); 단말.문자(10);
    }
    static boolean 재개() {
        if (Tabla.kontrola_korisnik_program(16 + aktuelno_stavka) == 0) return false;
        셸입출력.대화허용 = true; 셸입출력.koristiti(false, false); Tabla.입출력전환(1);
        int 처리값 = Tabla.kontrola_korisnik_program(aktuelno_stavka); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; ljuska_sintaksa.Status_VALUE = 처리값 < 0 ? 126 : 처리값; 단말.쓰기("exit "); 단말.수(처리값); 단말.문자(10); Tabla.Terminal(3); }
        return true;
    }
}
