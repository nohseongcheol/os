// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 qobiq holat_VALUE_e10195a1. Fayl 저장소는 공유하고 yo_l/변수/LOG_satr/입력은 분리한다. */
public final class oyna_seans {
    static int[] 보관 = new int[4 * 30000], Tayyorlamoq = new int[4];
    static int 현재, Holati;
    static boolean 이어읽기;
    static void ARRAY_VALUE(int[] ma_lumotlar, boolean Store_VALUE) {
        for (int Loop_INDEX = 0; Loop_INDEX < ma_lumotlar.length; Loop_INDEX++) { if (Store_VALUE) 보관[Holati++] = ma_lumotlar[Loop_INDEX]; else ma_lumotlar[Loop_INDEX] = 보관[Holati++]; }
    }
    static int VALUE(int ma_lumotlar_VALUE, boolean 저장여부) { if (저장여부) { 보관[Holati++] = ma_lumotlar_VALUE; return ma_lumotlar_VALUE; } return 보관[Holati++]; }
    static void izlamoq_holat(int 보관칸, boolean 저장여부) {
        Holati = 보관칸 * 30000;
        ARRAY_VALUE(Xotira_Fayllar.현재, 저장여부); Xotira_Fayllar.현재길이 = VALUE(Xotira_Fayllar.현재길이, 저장여부);
        ARRAY_VALUE(qobiq_sintaksis.변수이름, 저장여부); ARRAY_VALUE(qobiq_sintaksis.변수값, 저장여부); ARRAY_VALUE(qobiq_sintaksis.이름길이, 저장여부); ARRAY_VALUE(qobiq_sintaksis.VALUE_uzunlik, 저장여부);
        qobiq_sintaksis.holat_VALUE_e10195a1 = VALUE(qobiq_sintaksis.holat_VALUE_e10195a1, 저장여부);
        ARRAY_VALUE(satr_Muharrir.LOG_satr, 저장여부); ARRAY_VALUE(satr_Muharrir.LOG_uzunlik, 저장여부); ARRAY_VALUE(satr_Muharrir.Store_VALUE, 저장여부); ARRAY_VALUE(명령해석기.satr, 저장여부);
        satr_Muharrir.LOG_COUNT = VALUE(satr_Muharrir.LOG_COUNT, 저장여부); satr_Muharrir.LOG_satr_to_xtatmoq = VALUE(satr_Muharrir.LOG_satr_to_xtatmoq, 저장여부);
        satr_Muharrir.Izlash_VALUE = VALUE(satr_Muharrir.Izlash_VALUE, 저장여부); satr_Muharrir.저장길이 = VALUE(satr_Muharrir.저장길이, 저장여부);
        satr_Muharrir.Hajmi = VALUE(satr_Muharrir.Hajmi, 저장여부); satr_Muharrir.kursor_VALUE = VALUE(satr_Muharrir.kursor_VALUE, 저장여부); satr_Muharrir.Start_oyna = VALUE(satr_Muharrir.Start_oyna, 저장여부);
        Tayyorlamoq[보관칸] = 1;
    }
    static void Jarayon_VALUE_kiritish() {
        int 사건번호 = yozuv_taxtasi.Terminal(12); if (사건번호 == 0) return;
        izlamoq_holat(현재, true);
        for (int Loop_INDEX = 0; Loop_INDEX < 4; Loop_INDEX++) {
            if ((사건번호 & (1 << (8 + Loop_INDEX))) != 0) { yozuv_taxtasi.boshqaruv_foydalanuvchi_ilova(32 + Loop_INDEX); Tayyorlamoq[Loop_INDEX] = 0; }
            if ((사건번호 & (1 << (4 + Loop_INDEX))) != 0 && Loop_INDEX != 현재) Tayyorlamoq[Loop_INDEX] = 0;
        }
        int Keyingi_holat = (사건번호 & 15) - 1; if (Keyingi_holat < 0) Keyingi_holat = 0;
        if (Tayyorlamoq[Keyingi_holat] == 0) for (int Loop_INDEX = 0; Loop_INDEX < 30000; Loop_INDEX++) 보관[Keyingi_holat * 30000 + Loop_INDEX] = 0;
        현재 = Keyingi_holat; izlamoq_holat(현재, false); yozuv_taxtasi.Terminal(100 + 현재); 이어읽기 = true;
        단말.Yozish("\nTERMINAL FOCUS "); 단말.수(현재 + 1); 단말.문자(10);
    }
    static boolean 재개() {
        if (yozuv_taxtasi.boshqaruv_foydalanuvchi_ilova(16 + 현재) == 0) return false;
        셸입출력.Ruxsatnoma_o_zaro_faol = true; 셸입출력.Bajarish(false, false); yozuv_taxtasi.입출력전환(1);
        int 처리값 = yozuv_taxtasi.boshqaruv_foydalanuvchi_ilova(현재); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; qobiq_sintaksis.holat_VALUE_e10195a1 = 처리값 < 0 ? 126 : 처리값; 단말.Yozish("exit "); 단말.수(처리값); 단말.문자(10); yozuv_taxtasi.Terminal(3); }
        return true;
    }
}
