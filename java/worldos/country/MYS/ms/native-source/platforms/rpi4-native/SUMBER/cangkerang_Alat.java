// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 cangkerang 내장 alat. */
public final class cangkerang_Alat {
    static int[] data = new int[16384];
    static int fail_input = -1;
    static int buka_fail(int argumen_INDEX, int Proses_mod) {
        int 처리값 = pentafsir_perintah.LALUAN(argumen_INDEX); return 처리값 < 0 ? 처리값 : Memori_Fail.Buka(Proses_mod);
    }
    static boolean 입력준비(int argumen_INDEX) {
        fail_input = -1;
        if (argumen_INDEX < pentafsir_perintah.token_COUNT) {
            fail_input = buka_fail(argumen_INDEX, 0);
            if (fail_input < 0) { pentafsir_perintah.RALAT(fail_input); return false; }
        }
        return true;
    }
    static int Baca() {
        if (fail_input >= 3) return Memori_Fail.Baca(fail_input);
        while (true) {
            int bait_data = Papan.직렬읽기(); if (bait_data == -2 || bait_data == 4) return 256;
            if (bait_data == 3) { pentafsir_perintah.ukuran = 130; return 256; }
            if (bait_data >= 0) return bait_data; Papan.YIELD_CPU();
        }
    }
    static void Tutup() { if (fail_input >= 3) Memori_Fail.Tutup(fail_input); fail_input = -1; }
    static void lihat_VALUE() {
        int 마지막자리 = pentafsir_perintah.token_COUNT == 1 ? 2 : pentafsir_perintah.token_COUNT;
        for (int argumen_INDEX = 1; argumen_INDEX < 마지막자리; argumen_INDEX++) {
            if (!입력준비(argumen_INDEX)) continue;
            int bait_data; while ((bait_data = Baca()) != 256 && bait_data >= 0) Papan.직렬쓰기(bait_data);
            if (bait_data < 0) pentafsir_perintah.RALAT(bait_data); Tutup();
        }
    }
    static void fail_kes(String 동작번호) {
        if (pentafsir_perintah.token_COUNT != 2) { pentafsir_perintah.ukuran = 2; 단말.Tulis("사용법: mkdir/rmdir/touch Fail\n"); return; }
        int 처리값 = pentafsir_perintah.LALUAN(1);
        if (처리값 >= 0) {
            if (동작번호.charAt(0) == 'm') 처리값 = Memori_Fail.cipta_direktori();
            else if (동작번호.charAt(0) == 'r') 처리값 = Memori_Fail.alih_keluar_direktori();
            else { 처리값 = Memori_Fail.Buka(65); if (처리값 >= 3) 처리값 = Memori_Fail.Tutup(처리값); }
        }
        if (처리값 < 0) pentafsir_perintah.RALAT(처리값);
    }
    static void tika_VALUE(boolean 이동여부) {
        if (pentafsir_perintah.token_COUNT != 3) { pentafsir_perintah.ukuran = 2; 단말.Tulis("사용법: cp/mv 원본 destinasi_peserta (Fail)\n"); return; }
        int 처리값 = pentafsir_perintah.LALUAN(1); if (처리값 >= 0) 처리값 = Memori_Fail.menormalkan_VALUE();
        if (처리값 < 0) { pentafsir_perintah.RALAT(처리값); return; }
        int 원본번호 = Memori_Fail.Cari_pemasukan(); if (원본번호 < 0) { pentafsir_perintah.RALAT(-2); return; }
        int pemasukan_COUNT = Memori_Fail.kepanjangan_VALUE[원본번호]; for (int Loop_INDEX = 0; Loop_INDEX < pemasukan_COUNT; Loop_INDEX++) data[Loop_INDEX] = Memori_Fail.자료읽기(원본번호, Loop_INDEX);
        처리값 = pentafsir_perintah.LALUAN(2); if (처리값 >= 0) 처리값 = Memori_Fail.menormalkan_VALUE();
        if (처리값 < 0) { pentafsir_perintah.RALAT(처리값); return; }
        if (Memori_Fail.Cari_pemasukan() == 원본번호) { if (!이동여부) pentafsir_perintah.RALAT(-22); return; }
        if (이동여부) { 처리값 = Memori_Fail.이름바꾸기(원본번호); if (처리값 < 0) pentafsir_perintah.RALAT(처리값); return; }
        int 열린파일번호 = Memori_Fail.Buka(577); if (열린파일번호 < 0) { pentafsir_perintah.RALAT(열린파일번호); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < pemasukan_COUNT; Loop_INDEX++) { 처리값 = Memori_Fail.Tulis(열린파일번호, data[Loop_INDEX]); if (처리값 < 0) { pentafsir_perintah.RALAT(처리값); break; } }
        Memori_Fail.Tutup(열린파일번호);
    }
    static int digit_VALUE(int argumen_INDEX) {
        if (argumen_INDEX >= pentafsir_perintah.token_COUNT) return -1;
        int pemasukan_COUNT = 0; for (int Loop_INDEX = 0; Loop_INDEX < pentafsir_perintah.kepanjangan_VALUE[argumen_INDEX]; Loop_INDEX++) { int titik_kod = pentafsir_perintah.token_VALUE[pentafsir_perintah.시작점[argumen_INDEX] + Loop_INDEX]; if (titik_kod < '0' || titik_kod > '9' || pemasukan_COUNT > 10000) return -1; pemasukan_COUNT = pemasukan_COUNT * 10 + titik_kod - '0'; } return pemasukan_COUNT;
    }
    static void 세기() {
        int argumen_INDEX = 1, 선택번호 = 0;
        if (pentafsir_perintah.같음(1, "-c") || pentafsir_perintah.같음(1, "-l") || pentafsir_perintah.같음(1, "-w")) { 선택번호 = pentafsir_perintah.같음(1, "-c") ? 1 : pentafsir_perintah.같음(1, "-l") ? 2 : 3; argumen_INDEX++; }
        if (pentafsir_perintah.token_COUNT > argumen_INDEX + 1) { pentafsir_perintah.ukuran = 2; 단말.Tulis("사용법: wc [-c|-l|-w] [Fail]\n"); return; }
        if (!입력준비(argumen_INDEX)) return;
        int bait_COUNT = 0, 줄수 = 0, 낱말수 = 0, bait_data; boolean 낱말 = false;
        while ((bait_data = Baca()) >= 0 && bait_data != 256) { bait_COUNT++; if (bait_data == 10) 줄수++; boolean SPACE = bait_data == 32 || bait_data >= 9 && bait_data <= 13; if (!SPACE && !낱말) 낱말수++; 낱말 = !SPACE; }
        Tutup(); if (bait_data < 0) { pentafsir_perintah.RALAT(bait_data); return; }
        if (선택번호 != 0) 단말.수(선택번호 == 1 ? bait_COUNT : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.수(줄수); 단말.문자(' '); 단말.수(낱말수); 단말.문자(' '); 단말.수(bait_COUNT); } 단말.문자(10);
    }
    static void Cari_pemasukan() {
        if (pentafsir_perintah.token_COUNT < 2 || pentafsir_perintah.token_COUNT > 3) { pentafsir_perintah.ukuran = 2; 단말.Tulis("사용법: grep 찾을문구 [Fail]\n"); return; }
        if (!입력준비(2)) return;
        int pemasukan_COUNT = 0, bait_data, 일치수 = 0;
        while (true) {
            bait_data = Baca();
            if (bait_data == 10 || bait_data == 256 || bait_data < 0) {
                boolean 찾은여부 = false;
                for (int Loop_INDEX = 0; Loop_INDEX <= pemasukan_COUNT - pentafsir_perintah.kepanjangan_VALUE[1]; Loop_INDEX++) {
                    boolean 같은여부 = true; for (int dalaman_jawatan = 0; dalaman_jawatan < pentafsir_perintah.kepanjangan_VALUE[1]; dalaman_jawatan++) if (data[Loop_INDEX + dalaman_jawatan] != pentafsir_perintah.token_VALUE[pentafsir_perintah.시작점[1] + dalaman_jawatan]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (pemasukan_COUNT > 0 || bait_data == 10)) { for (int Loop_INDEX = 0; Loop_INDEX < pemasukan_COUNT; Loop_INDEX++) Papan.직렬쓰기(data[Loop_INDEX]); 단말.문자(10); 일치수++; }
                pemasukan_COUNT = 0; if (bait_data != 10) break;
            } else if (pemasukan_COUNT < data.length) data[pemasukan_COUNT++] = bait_data;
            else { pentafsir_perintah.RALAT(-28); Tutup(); return; }
        }
        Tutup(); if (bait_data < 0) pentafsir_perintah.RALAT(bait_data); else if (pentafsir_perintah.ukuran == 0) pentafsir_perintah.ukuran = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int argumen_INDEX = 1, 줄수 = 10;
        if (pentafsir_perintah.같음(1, "-n")) { 줄수 = digit_VALUE(2); argumen_INDEX = 3; }
        if (줄수 < 0 || pentafsir_perintah.token_COUNT > argumen_INDEX + 1) { pentafsir_perintah.ukuran = 2; 단말.Tulis("사용법: head/tail [-n 줄수] [Fail]\n"); return; }
        if (!입력준비(argumen_INDEX)) return;
        int pemasukan_COUNT = 0, bait_data;
        while ((bait_data = Baca()) != 256 && bait_data >= 0) { if (pemasukan_COUNT == data.length) { pentafsir_perintah.RALAT(-28); Tutup(); return; } data[pemasukan_COUNT++] = bait_data; }
        Tutup(); if (bait_data < 0) { pentafsir_perintah.RALAT(bait_data); return; }
        int setempat_Mula = 0, tamat_jawatan = pemasukan_COUNT;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int 총수 = 0; for (int Loop_INDEX = pemasukan_COUNT - 2; Loop_INDEX >= 0; Loop_INDEX--) if (data[Loop_INDEX] == 10 && ++총수 == 줄수) { setempat_Mula = Loop_INDEX + 1; break; } }
        else { int 총수 = 0; for (int Loop_INDEX = 0; Loop_INDEX < pemasukan_COUNT; Loop_INDEX++) if (data[Loop_INDEX] == 10 && ++총수 == 줄수) { tamat_jawatan = Loop_INDEX + 1; break; } }
        for (int Loop_INDEX = setempat_Mula; Loop_INDEX < tamat_jawatan; Loop_INDEX++) Papan.직렬쓰기(data[Loop_INDEX]);
    }
    static void tulis_Bersama_sama() {
        boolean Tambah = pentafsir_perintah.같음(1, "-a"); int argumen_INDEX = Tambah ? 2 : 1;
        if (pentafsir_perintah.token_COUNT != argumen_INDEX + 1) { pentafsir_perintah.ukuran = 2; 단말.Tulis("사용법: tee [-a] Fail\n"); return; }
        int 열린파일번호 = buka_fail(argumen_INDEX, Tambah ? 1089 : 577); if (열린파일번호 < 0) { pentafsir_perintah.RALAT(열린파일번호); return; }
        fail_input = -1; int bait_data;
        while ((bait_data = Baca()) != 256 && bait_data >= 0) { int 처리값 = Memori_Fail.Tulis(열린파일번호, bait_data); if (처리값 < 0) { pentafsir_perintah.RALAT(처리값); break; } Papan.직렬쓰기(bait_data); }
        Memori_Fail.Tutup(열린파일번호);
    }
}
