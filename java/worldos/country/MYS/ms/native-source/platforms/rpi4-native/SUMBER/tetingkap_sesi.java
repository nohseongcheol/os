// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 cangkerang status_VALUE. Fail 저장소는 공유하고 LALUAN/pemboleh_ubah_VALUE/LOG_baris/입력은 분리한다. */
public final class tetingkap_sesi {
    static int[] 보관 = new int[4 * 30000], Sediakan = new int[4];
    static int 현재, Kedudukan;
    static boolean 이어읽기;
    static void ARRAY_VALUE(int[] data, boolean stor_VALUE) {
        for (int Loop_INDEX = 0; Loop_INDEX < data.length; Loop_INDEX++) { if (stor_VALUE) 보관[Kedudukan++] = data[Loop_INDEX]; else data[Loop_INDEX] = 보관[Kedudukan++]; }
    }
    static int VALUE(int data_VALUE, boolean 저장여부) { if (저장여부) { 보관[Kedudukan++] = data_VALUE; return data_VALUE; } return 보관[Kedudukan++]; }
    static void cari_jawatan(int 보관칸, boolean 저장여부) {
        Kedudukan = 보관칸 * 30000;
        ARRAY_VALUE(Memori_Fail.현재, 저장여부); Memori_Fail.현재길이 = VALUE(Memori_Fail.현재길이, 저장여부);
        ARRAY_VALUE(cangkerang_sintaks.pemboleh_ubah_nama, 저장여부); ARRAY_VALUE(cangkerang_sintaks.pemboleh_ubah_data, 저장여부); ARRAY_VALUE(cangkerang_sintaks.이름길이, 저장여부); ARRAY_VALUE(cangkerang_sintaks.VALUE_kepanjangan, 저장여부);
        cangkerang_sintaks.status_VALUE = VALUE(cangkerang_sintaks.status_VALUE, 저장여부);
        ARRAY_VALUE(editor_baris.LOG_baris, 저장여부); ARRAY_VALUE(editor_baris.LOG_kepanjangan, 저장여부); ARRAY_VALUE(editor_baris.stor_VALUE, 저장여부); ARRAY_VALUE(pentafsir_perintah.baris, 저장여부);
        editor_baris.LOG_COUNT = VALUE(editor_baris.LOG_COUNT, 저장여부); editor_baris.LOG_baris_tamat = VALUE(editor_baris.LOG_baris_tamat, 저장여부);
        editor_baris.Cari_VALUE = VALUE(editor_baris.Cari_VALUE, 저장여부); editor_baris.저장길이 = VALUE(editor_baris.저장길이, 저장여부);
        editor_baris.Saiz = VALUE(editor_baris.Saiz, 저장여부); editor_baris.kursor_VALUE = VALUE(editor_baris.kursor_VALUE, 저장여부); editor_baris.Mula_tetingkap = VALUE(editor_baris.Mula_tetingkap, 저장여부);
        Sediakan[보관칸] = 1;
    }
    static void Proses_VALUE_pemasukan() {
        int 사건번호 = Papan.Terminal(12); if (사건번호 == 0) return;
        cari_jawatan(현재, true);
        for (int Loop_INDEX = 0; Loop_INDEX < 4; Loop_INDEX++) {
            if ((사건번호 & (1 << (8 + Loop_INDEX))) != 0) { Papan.kawalan_pengguna_aplikasi(32 + Loop_INDEX); Sediakan[Loop_INDEX] = 0; }
            if ((사건번호 & (1 << (4 + Loop_INDEX))) != 0 && Loop_INDEX != 현재) Sediakan[Loop_INDEX] = 0;
        }
        int Seterusnya_jawatan = (사건번호 & 15) - 1; if (Seterusnya_jawatan < 0) Seterusnya_jawatan = 0;
        if (Sediakan[Seterusnya_jawatan] == 0) for (int Loop_INDEX = 0; Loop_INDEX < 30000; Loop_INDEX++) 보관[Seterusnya_jawatan * 30000 + Loop_INDEX] = 0;
        현재 = Seterusnya_jawatan; cari_jawatan(현재, false); Papan.Terminal(100 + 현재); 이어읽기 = true;
        단말.Tulis("\nTERMINAL FOCUS "); 단말.수(현재 + 1); 단말.문자(10);
    }
    static boolean 재개() {
        if (Papan.kawalan_pengguna_aplikasi(16 + 현재) == 0) return false;
        셸입출력.Izin_interaktif = true; 셸입출력.Jalan(false, false); Papan.입출력전환(1);
        int 처리값 = Papan.kawalan_pengguna_aplikasi(현재); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; cangkerang_sintaks.status_VALUE = 처리값 < 0 ? 126 : 처리값; 단말.Tulis("exit "); 단말.수(처리값); 단말.문자(10); Papan.Terminal(3); }
        return true;
    }
}
