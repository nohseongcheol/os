// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 shell Egoera_balio. Fitxategia 저장소는 공유하고 Bide_izena/변수/LOG_marka/입력은 분리한다. */
public final class leiho_saio {
    static int[] 보관 = new int[4 * 30000], 준비 = new int[4];
    static int 현재, Posizioa;
    static boolean 이어읽기;
    static void matrize_balio(int[] datuak, boolean Store_balio) {
        for (int Loop_INDIZE = 0; Loop_INDIZE < datuak.length; Loop_INDIZE++) { if (Store_balio) 보관[Posizioa++] = datuak[Loop_INDIZE]; else datuak[Loop_INDIZE] = 보관[Posizioa++]; }
    }
    static int balio(int datuak_balio, boolean 저장여부) { if (저장여부) { 보관[Posizioa++] = datuak_balio; return datuak_balio; } return 보관[Posizioa++]; }
    static void bilatu_kargu(int 보관칸, boolean 저장여부) {
        Posizioa = 보관칸 * 30000;
        matrize_balio(Memoria_Fitxategiak.현재, 저장여부); Memoria_Fitxategiak.현재길이 = balio(Memoria_Fitxategiak.현재길이, 저장여부);
        matrize_balio(shell_sintaxi.변수이름, 저장여부); matrize_balio(shell_sintaxi.변수값, 저장여부); matrize_balio(shell_sintaxi.이름길이, 저장여부); matrize_balio(shell_sintaxi.balio_luzera, 저장여부);
        shell_sintaxi.Egoera_balio = balio(shell_sintaxi.Egoera_balio, 저장여부);
        matrize_balio(lerro_editore.LOG_marka, 저장여부); matrize_balio(lerro_editore.LOG_luzera, 저장여부); matrize_balio(lerro_editore.Store_balio, 저장여부); matrize_balio(명령해석기.Marra, 저장여부);
        lerro_editore.LOG_ZENBATU = balio(lerro_editore.LOG_ZENBATU, 저장여부); lerro_editore.LOG_marka_amaitu = balio(lerro_editore.LOG_marka_amaitu, 저장여부);
        lerro_editore.BILATU_balio = balio(lerro_editore.BILATU_balio, 저장여부); lerro_editore.저장길이 = balio(lerro_editore.저장길이, 저장여부);
        lerro_editore.Tamaina = balio(lerro_editore.Tamaina, 저장여부); lerro_editore.kurtsore_balio = balio(lerro_editore.kurtsore_balio, 저장여부); lerro_editore.HASI_leiho = balio(lerro_editore.HASI_leiho, 저장여부);
        준비[보관칸] = 1;
    }
    static void prozesu_balio_sarrera() {
        int 사건번호 = arbel.Terminala(12); if (사건번호 == 0) return;
        bilatu_kargu(현재, true);
        for (int Loop_INDIZE = 0; Loop_INDIZE < 4; Loop_INDIZE++) {
            if ((사건번호 & (1 << (8 + Loop_INDIZE))) != 0) { arbel.kontrol_erabiltzaile_aplik(32 + Loop_INDIZE); 준비[Loop_INDIZE] = 0; }
            if ((사건번호 & (1 << (4 + Loop_INDIZE))) != 0 && Loop_INDIZE != 현재) 준비[Loop_INDIZE] = 0;
        }
        int Hurrengoa_kargu = (사건번호 & 15) - 1; if (Hurrengoa_kargu < 0) Hurrengoa_kargu = 0;
        if (준비[Hurrengoa_kargu] == 0) for (int Loop_INDIZE = 0; Loop_INDIZE < 30000; Loop_INDIZE++) 보관[Hurrengoa_kargu * 30000 + Loop_INDIZE] = 0;
        현재 = Hurrengoa_kargu; bilatu_kargu(현재, false); arbel.Terminala(100 + 현재); 이어읽기 = true;
        단말.Idatzi("\nTERMINAL FOCUS "); 단말.수(현재 + 1); 단말.문자(10);
    }
    static boolean 재개() {
        if (arbel.kontrol_erabiltzaile_aplik(16 + 현재) == 0) return false;
        셸입출력.Onartu_interaktibo = true; 셸입출력.Exekutatu_2(false, false); arbel.입출력전환(1);
        int 처리값 = arbel.kontrol_erabiltzaile_aplik(현재); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; shell_sintaxi.Egoera_balio = 처리값 < 0 ? 126 : 처리값; 단말.Idatzi("exit "); 단말.수(처리값); 단말.문자(10); arbel.Terminala(3); }
        return true;
    }
}
