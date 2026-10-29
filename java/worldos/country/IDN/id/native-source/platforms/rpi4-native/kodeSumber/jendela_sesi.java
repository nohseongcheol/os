// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 shell Status_VALUE. berkas 저장소는 공유하고 jalur/variabel_VALUE/LOG_baris/입력은 분리한다. */
public final class jendela_sesi {
    static int[] 보관 = new int[4 * 30000], Siapkan = new int[4];
    static int saat_ini_item, posisi;
    static boolean 이어읽기;
    static void ARRAY_VALUE(int[] data, boolean Store_VALUE) {
        for (int Loop_INDEX = 0; Loop_INDEX < data.length; Loop_INDEX++) { if (Store_VALUE) 보관[posisi++] = data[Loop_INDEX]; else data[Loop_INDEX] = 보관[posisi++]; }
    }
    static int VALUE(int data_VALUE, boolean 저장여부) { if (저장여부) { 보관[posisi++] = data_VALUE; return data_VALUE; } return 보관[posisi++]; }
    static void cari_posisi(int 보관칸, boolean 저장여부) {
        posisi = 보관칸 * 30000;
        ARRAY_VALUE(BerkasMemori.saat_ini_item, 저장여부); BerkasMemori.saat_ini_panjang = VALUE(BerkasMemori.saat_ini_panjang, 저장여부);
        ARRAY_VALUE(shell_sintaksis.variabel_nama, 저장여부); ARRAY_VALUE(shell_sintaksis.variabel_data, 저장여부); ARRAY_VALUE(shell_sintaksis.이름길이, 저장여부); ARRAY_VALUE(shell_sintaksis.VALUE_panjang, 저장여부);
        shell_sintaksis.Status_VALUE = VALUE(shell_sintaksis.Status_VALUE, 저장여부);
        ARRAY_VALUE(editor_baris.LOG_baris, 저장여부); ARRAY_VALUE(editor_baris.LOG_panjang, 저장여부); ARRAY_VALUE(editor_baris.Store_VALUE, 저장여부); ARRAY_VALUE(PenafsirPerintah.baris_masukan, 저장여부);
        editor_baris.LOG_COUNT = VALUE(editor_baris.LOG_COUNT, 저장여부); editor_baris.LOG_baris_mengakhiri = VALUE(editor_baris.LOG_baris_mengakhiri, 저장여부);
        editor_baris.Cari_VALUE = VALUE(editor_baris.Cari_VALUE, 저장여부); editor_baris.저장길이 = VALUE(editor_baris.저장길이, 저장여부);
        editor_baris.Ukuran = VALUE(editor_baris.Ukuran, 저장여부); editor_baris.kursor_VALUE = VALUE(editor_baris.kursor_VALUE, 저장여부); editor_baris.Mulai_jendela = VALUE(editor_baris.Mulai_jendela, 저장여부);
        Siapkan[보관칸] = 1;
    }
    static void Proses_VALUE_entri() {
        int 사건번호 = Papan.terminal(12); if (사건번호 == 0) return;
        cari_posisi(saat_ini_item, true);
        for (int Loop_INDEX = 0; Loop_INDEX < 4; Loop_INDEX++) {
            if ((사건번호 & (1 << (8 + Loop_INDEX))) != 0) { Papan.kontrol_pengguna_apl(32 + Loop_INDEX); Siapkan[Loop_INDEX] = 0; }
            if ((사건번호 & (1 << (4 + Loop_INDEX))) != 0 && Loop_INDEX != saat_ini_item) Siapkan[Loop_INDEX] = 0;
        }
        int Berikutnya_posisi = (사건번호 & 15) - 1; if (Berikutnya_posisi < 0) Berikutnya_posisi = 0;
        if (Siapkan[Berikutnya_posisi] == 0) for (int Loop_INDEX = 0; Loop_INDEX < 30000; Loop_INDEX++) 보관[Berikutnya_posisi * 30000 + Loop_INDEX] = 0;
        saat_ini_item = Berikutnya_posisi; cari_posisi(saat_ini_item, false); Papan.terminal(100 + saat_ini_item); 이어읽기 = true;
        단말.Tulis("\nTERMINAL FOCUS "); 단말.수(saat_ini_item + 1); 단말.문자(10);
    }
    static boolean 재개() {
        if (Papan.kontrol_pengguna_apl(16 + saat_ini_item) == 0) return false;
        셸입출력.Perbolehkan_interaktif = true; 셸입출력.jalankan(false, false); Papan.입출력전환(1);
        int 처리값 = Papan.kontrol_pengguna_apl(saat_ini_item); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; shell_sintaksis.Status_VALUE = 처리값 < 0 ? 126 : 처리값; 단말.Tulis("exit "); 단말.수(처리값); 단말.문자(10); Papan.terminal(3); }
        return true;
    }
}
