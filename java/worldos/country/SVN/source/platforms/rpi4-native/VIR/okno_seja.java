// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 lupina stanje_VALUE. Datoteka 저장소는 공유하고 POT/변수/LOG_zapis/입력은 분리한다. */
public final class okno_seja {
    static int[] 보관 = new int[4 * 30000], Pripravi = new int[4];
    static int sprotno_element, Položaj;
    static boolean 이어읽기;
    static void ARRAY_VALUE(int[] podatki, boolean Store_VALUE) {
        for (int Loop_INDEX = 0; Loop_INDEX < podatki.length; Loop_INDEX++) { if (Store_VALUE) 보관[Položaj++] = podatki[Loop_INDEX]; else podatki[Loop_INDEX] = 보관[Položaj++]; }
    }
    static int VALUE(int podatki_VALUE, boolean 저장여부) { if (저장여부) { 보관[Položaj++] = podatki_VALUE; return podatki_VALUE; } return 보관[Položaj++]; }
    static void iskati_položaj(int 보관칸, boolean 저장여부) {
        Položaj = 보관칸 * 30000;
        ARRAY_VALUE(pomnilnik_Datoteke.sprotno_element, 저장여부); pomnilnik_Datoteke.현재길이 = VALUE(pomnilnik_Datoteke.현재길이, 저장여부);
        ARRAY_VALUE(lupina_sintaksa.변수이름, 저장여부); ARRAY_VALUE(lupina_sintaksa.변수값, 저장여부); ARRAY_VALUE(lupina_sintaksa.이름길이, 저장여부); ARRAY_VALUE(lupina_sintaksa.값길이, 저장여부);
        lupina_sintaksa.stanje_VALUE = VALUE(lupina_sintaksa.stanje_VALUE, 저장여부);
        ARRAY_VALUE(linija_Urejevalnik.LOG_zapis, 저장여부); ARRAY_VALUE(linija_Urejevalnik.기록길이, 저장여부); ARRAY_VALUE(linija_Urejevalnik.Store_VALUE, 저장여부); ARRAY_VALUE(명령해석기.Črtni, 저장여부);
        linija_Urejevalnik.LOG_COUNT = VALUE(linija_Urejevalnik.LOG_COUNT, 저장여부); linija_Urejevalnik.LOG_zapis_končati_klic = VALUE(linija_Urejevalnik.LOG_zapis_končati_klic, 저장여부);
        linija_Urejevalnik.Išči_VALUE = VALUE(linija_Urejevalnik.Išči_VALUE, 저장여부); linija_Urejevalnik.저장길이 = VALUE(linija_Urejevalnik.저장길이, 저장여부);
        linija_Urejevalnik.Velikost = VALUE(linija_Urejevalnik.Velikost, 저장여부); linija_Urejevalnik.kazalec_VALUE = VALUE(linija_Urejevalnik.kazalec_VALUE, 저장여부); linija_Urejevalnik.Start_okno = VALUE(linija_Urejevalnik.Start_okno, 저장여부);
        Pripravi[보관칸] = 1;
    }
    static void Proces_VALUE_vnos() {
        int 사건번호 = Tabla.Terminal(12); if (사건번호 == 0) return;
        iskati_položaj(sprotno_element, true);
        for (int Loop_INDEX = 0; Loop_INDEX < 4; Loop_INDEX++) {
            if ((사건번호 & (1 << (8 + Loop_INDEX))) != 0) { Tabla.nadzor_uporabnik_aplikacija(32 + Loop_INDEX); Pripravi[Loop_INDEX] = 0; }
            if ((사건번호 & (1 << (4 + Loop_INDEX))) != 0 && Loop_INDEX != sprotno_element) Pripravi[Loop_INDEX] = 0;
        }
        int Naprej_položaj = (사건번호 & 15) - 1; if (Naprej_položaj < 0) Naprej_položaj = 0;
        if (Pripravi[Naprej_položaj] == 0) for (int Loop_INDEX = 0; Loop_INDEX < 30000; Loop_INDEX++) 보관[Naprej_položaj * 30000 + Loop_INDEX] = 0;
        sprotno_element = Naprej_položaj; iskati_položaj(sprotno_element, false); Tabla.Terminal(100 + sprotno_element); 이어읽기 = true;
        단말.Pisanje("\nTERMINAL FOCUS "); 단말.수(sprotno_element + 1); 단말.문자(10);
    }
    static boolean 재개() {
        if (Tabla.nadzor_uporabnik_aplikacija(16 + sprotno_element) == 0) return false;
        셸입출력.Dovoli_interaktiven = true; 셸입출력.Zaženi(false, false); Tabla.입출력전환(1);
        int 처리값 = Tabla.nadzor_uporabnik_aplikacija(sprotno_element); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; lupina_sintaksa.stanje_VALUE = 처리값 < 0 ? 126 : 처리값; 단말.Pisanje("exit "); 단말.수(처리값); 단말.문자(10); Tabla.Terminal(3); }
        return true;
    }
}
