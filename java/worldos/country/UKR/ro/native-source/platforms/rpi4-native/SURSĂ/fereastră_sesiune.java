// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 shell Stare_VALUE. Fișier 저장소는 공유하고 Cale/variabilă_VALUE/LOG_RECORD/입력은 분리한다. */
public final class fereastră_sesiune {
    static int[] 보관 = new int[4 * 30000], Pregătiți = new int[4];
    static int curent_element, Poziție;
    static boolean 이어읽기;
    static void ARRAY_VALUE(int[] date, boolean Store_VALUE) {
        for (int Loop_INDEX = 0; Loop_INDEX < date.length; Loop_INDEX++) { if (Store_VALUE) 보관[Poziție++] = date[Loop_INDEX]; else date[Loop_INDEX] = 보관[Poziție++]; }
    }
    static int VALUE(int date_VALUE, boolean 저장여부) { if (저장여부) { 보관[Poziție++] = date_VALUE; return date_VALUE; } return 보관[Poziție++]; }
    static void căuta_poziție(int 보관칸, boolean 저장여부) {
        Poziție = 보관칸 * 30000;
        ARRAY_VALUE(Memorie_Fișiere.curent_element, 저장여부); Memorie_Fișiere.curent_lungime = VALUE(Memorie_Fișiere.curent_lungime, 저장여부);
        ARRAY_VALUE(shell_sintaxă.variabilă_nume, 저장여부); ARRAY_VALUE(shell_sintaxă.variabilă_date, 저장여부); ARRAY_VALUE(shell_sintaxă.이름길이, 저장여부); ARRAY_VALUE(shell_sintaxă.VALUE_lungime, 저장여부);
        shell_sintaxă.Stare_VALUE = VALUE(shell_sintaxă.Stare_VALUE, 저장여부);
        ARRAY_VALUE(editor_de_linii.LOG_RECORD, 저장여부); ARRAY_VALUE(editor_de_linii.LOG_lungime, 저장여부); ARRAY_VALUE(editor_de_linii.Store_VALUE, 저장여부); ARRAY_VALUE(명령해석기.Linie, 저장여부);
        editor_de_linii.LOG_COUNT = VALUE(editor_de_linii.LOG_COUNT, 저장여부); editor_de_linii.LOG_RECORD_termina_un_apel = VALUE(editor_de_linii.LOG_RECORD_termina_un_apel, 저장여부);
        editor_de_linii.căuta_VALUE = VALUE(editor_de_linii.căuta_VALUE, 저장여부); editor_de_linii.저장길이 = VALUE(editor_de_linii.저장길이, 저장여부);
        editor_de_linii.Mărime = VALUE(editor_de_linii.Mărime, 저장여부); editor_de_linii.cursor_VALUE = VALUE(editor_de_linii.cursor_VALUE, 저장여부); editor_de_linii.buta_fereastră = VALUE(editor_de_linii.buta_fereastră, 저장여부);
        Pregătiți[보관칸] = 1;
    }
    static void Proces_VALUE_intrare() {
        int 사건번호 = Avizier.Terminal(12); if (사건번호 == 0) return;
        căuta_poziție(curent_element, true);
        for (int Loop_INDEX = 0; Loop_INDEX < 4; Loop_INDEX++) {
            if ((사건번호 & (1 << (8 + Loop_INDEX))) != 0) { Avizier.control_utilizator_program(32 + Loop_INDEX); Pregătiți[Loop_INDEX] = 0; }
            if ((사건번호 & (1 << (4 + Loop_INDEX))) != 0 && Loop_INDEX != curent_element) Pregătiți[Loop_INDEX] = 0;
        }
        int Următorul_poziție = (사건번호 & 15) - 1; if (Următorul_poziție < 0) Următorul_poziție = 0;
        if (Pregătiți[Următorul_poziție] == 0) for (int Loop_INDEX = 0; Loop_INDEX < 30000; Loop_INDEX++) 보관[Următorul_poziție * 30000 + Loop_INDEX] = 0;
        curent_element = Următorul_poziție; căuta_poziție(curent_element, false); Avizier.Terminal(100 + curent_element); 이어읽기 = true;
        단말.Scriere("\nTERMINAL FOCUS "); 단말.수(curent_element + 1); 단말.문자(10);
    }
    static boolean CV_executare() {
        if (Avizier.control_utilizator_program(16 + curent_element) == 0) return false;
        셸입출력.대화허용 = true; 셸입출력.Pornește(false, false); Avizier.입출력전환(1);
        int 처리값 = Avizier.control_utilizator_program(curent_element); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; shell_sintaxă.Stare_VALUE = 처리값 < 0 ? 126 : 처리값; 단말.Scriere("exit "); 단말.수(처리값); 단말.문자(10); Avizier.Terminal(3); }
        return true;
    }
}
