// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 örtük vəziyyət_VALUE. FAYL 저장소는 공유하고 Cığır/변수/LOG_yaz/입력은 분리한다. */
public final class pəncərə_seans {
    static int[] 보관 = new int[4 * 30000], Hazırla = new int[4];
    static int 현재, yerinə_qoymaq;
    static boolean 이어읽기;
    static void ARRAY_VALUE(int[] verilənlər, boolean Store_VALUE) {
        for (int Loop_INDEX = 0; Loop_INDEX < verilənlər.length; Loop_INDEX++) { if (Store_VALUE) 보관[yerinə_qoymaq++] = verilənlər[Loop_INDEX]; else verilənlər[Loop_INDEX] = 보관[yerinə_qoymaq++]; }
    }
    static int VALUE(int verilənlər_VALUE, boolean 저장여부) { if (저장여부) { 보관[yerinə_qoymaq++] = verilənlər_VALUE; return verilənlər_VALUE; } return 보관[yerinə_qoymaq++]; }
    static void axtarmaq_yerinə_qoymaq(int 보관칸, boolean 저장여부) {
        yerinə_qoymaq = 보관칸 * 30000;
        ARRAY_VALUE(Yaddaş_Fayllar.현재, 저장여부); Yaddaş_Fayllar.현재길이 = VALUE(Yaddaş_Fayllar.현재길이, 저장여부);
        ARRAY_VALUE(örtük_sintaksis.변수이름, 저장여부); ARRAY_VALUE(örtük_sintaksis.변수값, 저장여부); ARRAY_VALUE(örtük_sintaksis.이름길이, 저장여부); ARRAY_VALUE(örtük_sintaksis.VALUE_uzunluq, 저장여부);
        örtük_sintaksis.vəziyyət_VALUE = VALUE(örtük_sintaksis.vəziyyət_VALUE, 저장여부);
        ARRAY_VALUE(xətt_Redaktor.LOG_yaz, 저장여부); ARRAY_VALUE(xətt_Redaktor.LOG_uzunluq, 저장여부); ARRAY_VALUE(xətt_Redaktor.Store_VALUE, 저장여부); ARRAY_VALUE(명령해석기.Giriş, 저장여부);
        xətt_Redaktor.LOG_COUNT = VALUE(xətt_Redaktor.LOG_COUNT, 저장여부); xətt_Redaktor.LOG_yaz_bitirmək = VALUE(xətt_Redaktor.LOG_yaz_bitirmək, 저장여부);
        xətt_Redaktor.SEARCH_VALUE = VALUE(xətt_Redaktor.SEARCH_VALUE, 저장여부); xətt_Redaktor.저장길이 = VALUE(xətt_Redaktor.저장길이, 저장여부);
        xətt_Redaktor.Böyüklük = VALUE(xətt_Redaktor.Böyüklük, 저장여부); xətt_Redaktor.kursor_VALUE = VALUE(xətt_Redaktor.kursor_VALUE, 저장여부); xətt_Redaktor.Başla_pəncərə = VALUE(xətt_Redaktor.Başla_pəncərə, 저장여부);
        Hazırla[보관칸] = 1;
    }
    static void Proses_VALUE_daxiletmə() {
        int 사건번호 = lövhə.Terminal(12); if (사건번호 == 0) return;
        axtarmaq_yerinə_qoymaq(현재, true);
        for (int Loop_INDEX = 0; Loop_INDEX < 4; Loop_INDEX++) {
            if ((사건번호 & (1 << (8 + Loop_INDEX))) != 0) { lövhə.nəzarət_istifadəçi_proqram(32 + Loop_INDEX); Hazırla[Loop_INDEX] = 0; }
            if ((사건번호 & (1 << (4 + Loop_INDEX))) != 0 && Loop_INDEX != 현재) Hazırla[Loop_INDEX] = 0;
        }
        int Sonrakı_yerinə_qoymaq = (사건번호 & 15) - 1; if (Sonrakı_yerinə_qoymaq < 0) Sonrakı_yerinə_qoymaq = 0;
        if (Hazırla[Sonrakı_yerinə_qoymaq] == 0) for (int Loop_INDEX = 0; Loop_INDEX < 30000; Loop_INDEX++) 보관[Sonrakı_yerinə_qoymaq * 30000 + Loop_INDEX] = 0;
        현재 = Sonrakı_yerinə_qoymaq; axtarmaq_yerinə_qoymaq(현재, false); lövhə.Terminal(100 + 현재); 이어읽기 = true;
        단말.Yazma("\nTERMINAL FOCUS "); 단말.수(현재 + 1); 단말.문자(10);
    }
    static boolean 재개() {
        if (lövhə.nəzarət_istifadəçi_proqram(16 + 현재) == 0) return false;
        셸입출력.İcazə_ver_interaktiv = true; 셸입출력.İcra_Et(false, false); lövhə.입출력전환(1);
        int 처리값 = lövhə.nəzarət_istifadəçi_proqram(현재); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; örtük_sintaksis.vəziyyət_VALUE = 처리값 < 0 ? 126 : 처리값; 단말.Yazma("exit "); 단말.수(처리값); 단말.문자(10); lövhə.Terminal(3); }
        return true;
    }
}
