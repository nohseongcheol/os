// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 셸 Stav_VALUE. Súbor 저장소는 공유하고 Cesta/변수/LOG_RECORD/입력은 분리한다. */
public final class okno_relácia {
    static int[] 보관 = new int[4 * 30000], Pripraviť = new int[4];
    static int v_termíne_splatnosti_položka, Pozícia;
    static boolean 이어읽기;
    static void pole_VALUE(int[] údaje, boolean Store_VALUE) {
        for (int Loop_INDEX = 0; Loop_INDEX < údaje.length; Loop_INDEX++) { if (Store_VALUE) 보관[Pozícia++] = údaje[Loop_INDEX]; else údaje[Loop_INDEX] = 보관[Pozícia++]; }
    }
    static int VALUE(int údaje_VALUE, boolean 저장여부) { if (저장여부) { 보관[Pozícia++] = údaje_VALUE; return údaje_VALUE; } return 보관[Pozícia++]; }
    static void hľadať_pozícia(int 보관칸, boolean 저장여부) {
        Pozícia = 보관칸 * 30000;
        pole_VALUE(Pamäť_Súbory.v_termíne_splatnosti_položka, 저장여부); Pamäť_Súbory.v_termíne_splatnosti_dĺžka = VALUE(Pamäť_Súbory.v_termíne_splatnosti_dĺžka, 저장여부);
        pole_VALUE(셸문법.변수이름, 저장여부); pole_VALUE(셸문법.변수값, 저장여부); pole_VALUE(셸문법.이름길이, 저장여부); pole_VALUE(셸문법.VALUE_dĺžka, 저장여부);
        셸문법.Stav_VALUE = VALUE(셸문법.Stav_VALUE, 저장여부);
        pole_VALUE(riadkový_editor.LOG_RECORD, 저장여부); pole_VALUE(riadkový_editor.LOG_dĺžka, 저장여부); pole_VALUE(riadkový_editor.Store_VALUE, 저장여부); pole_VALUE(명령해석기.riadok, 저장여부);
        riadkový_editor.LOG_COUNT = VALUE(riadkový_editor.LOG_COUNT, 저장여부); riadkový_editor.LOG_RECORD_ukončiť_hovor = VALUE(riadkový_editor.LOG_RECORD_ukončiť_hovor, 저장여부);
        riadkový_editor.Hľadať_VALUE = VALUE(riadkový_editor.Hľadať_VALUE, 저장여부); riadkový_editor.저장길이 = VALUE(riadkový_editor.저장길이, 저장여부);
        riadkový_editor.Veľkosť = VALUE(riadkový_editor.Veľkosť, 저장여부); riadkový_editor.kurzor_VALUE = VALUE(riadkový_editor.kurzor_VALUE, 저장여부); riadkový_editor.START_okno = VALUE(riadkový_editor.START_okno, 저장여부);
        Pripraviť[보관칸] = 1;
    }
    static void Proces_VALUE_položka() {
        int 사건번호 = Panel.Terminál(12); if (사건번호 == 0) return;
        hľadať_pozícia(v_termíne_splatnosti_položka, true);
        for (int Loop_INDEX = 0; Loop_INDEX < 4; Loop_INDEX++) {
            if ((사건번호 & (1 << (8 + Loop_INDEX))) != 0) { Panel.riadenie_používateľ_program(32 + Loop_INDEX); Pripraviť[Loop_INDEX] = 0; }
            if ((사건번호 & (1 << (4 + Loop_INDEX))) != 0 && Loop_INDEX != v_termíne_splatnosti_položka) Pripraviť[Loop_INDEX] = 0;
        }
        int Ďalej_pozícia = (사건번호 & 15) - 1; if (Ďalej_pozícia < 0) Ďalej_pozícia = 0;
        if (Pripraviť[Ďalej_pozícia] == 0) for (int Loop_INDEX = 0; Loop_INDEX < 30000; Loop_INDEX++) 보관[Ďalej_pozícia * 30000 + Loop_INDEX] = 0;
        v_termíne_splatnosti_položka = Ďalej_pozícia; hľadať_pozícia(v_termíne_splatnosti_položka, false); Panel.Terminál(100 + v_termíne_splatnosti_položka); 이어읽기 = true;
        단말.Zápis("\nTERMINAL FOCUS "); 단말.수(v_termíne_splatnosti_položka + 1); 단말.문자(10);
    }
    static boolean 재개() {
        if (Panel.riadenie_používateľ_program(16 + v_termíne_splatnosti_položka) == 0) return false;
        셸입출력.Povoliť_interaktívny = true; 셸입출력.Spustiť_2(false, false); Panel.입출력전환(1);
        int 처리값 = Panel.riadenie_používateľ_program(v_termíne_splatnosti_položka); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; 셸문법.Stav_VALUE = 처리값 < 0 ? 126 : 처리값; 단말.Zápis("exit "); 단말.수(처리값); 단말.문자(10); Panel.Terminál(3); }
        return true;
    }
}
