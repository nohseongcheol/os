// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 shell 내장 alat. */
public final class shell_Alat {
    static int[] data = new int[16384];
    static int file_input = -1;
    static int buat_file(int argumen_INDEX, int Proses_MODE) {
        int 처리값 = PenafsirPerintah.jalur(argumen_INDEX); return 처리값 < 0 ? 처리값 : BerkasMemori.Buka(Proses_MODE);
    }
    static boolean 입력준비(int argumen_INDEX) {
        file_input = -1;
        if (argumen_INDEX < PenafsirPerintah.token_COUNT) {
            file_input = buat_file(argumen_INDEX, 0);
            if (file_input < 0) { PenafsirPerintah.galat(file_input); return false; }
        }
        return true;
    }
    static int Baca() {
        if (file_input >= 3) return BerkasMemori.Baca(file_input);
        while (true) {
            int byte_data = Papan.직렬읽기(); if (byte_data == -2 || byte_data == 4) return 256;
            if (byte_data == 3) { PenafsirPerintah.hasil = 130; return 256; }
            if (byte_data >= 0) return byte_data; Papan.YIELD_CPU();
        }
    }
    static void Tutup() { if (file_input >= 3) BerkasMemori.Tutup(file_input); file_input = -1; }
    static void Tampilan_VALUE() {
        int 마지막자리 = PenafsirPerintah.token_COUNT == 1 ? 2 : PenafsirPerintah.token_COUNT;
        for (int argumen_INDEX = 1; argumen_INDEX < 마지막자리; argumen_INDEX++) {
            if (!입력준비(argumen_INDEX)) continue;
            int byte_data; while ((byte_data = Baca()) != 256 && byte_data >= 0) Papan.직렬쓰기(byte_data);
            if (byte_data < 0) PenafsirPerintah.galat(byte_data); Tutup();
        }
    }
    static void file_Tugas(String 동작번호) {
        if (PenafsirPerintah.token_COUNT != 2) { PenafsirPerintah.hasil = 2; 단말.Tulis("사용법: mkdir/rmdir/touch berkas\n"); return; }
        int 처리값 = PenafsirPerintah.jalur(1);
        if (처리값 >= 0) {
            if (동작번호.charAt(0) == 'm') 처리값 = BerkasMemori.Buat_Direktori();
            else if (동작번호.charAt(0) == 'r') 처리값 = BerkasMemori.hapus_Direktori();
            else { 처리값 = BerkasMemori.Buka(65); if (처리값 >= 3) 처리값 = BerkasMemori.Tutup(처리값); }
        }
        if (처리값 < 0) PenafsirPerintah.galat(처리값);
    }
    static void salin_VALUE(boolean 이동여부) {
        if (PenafsirPerintah.token_COUNT != 3) { PenafsirPerintah.hasil = 2; 단말.Tulis("사용법: cp/mv 원본 tujuan_peserta (berkas)\n"); return; }
        int 처리값 = PenafsirPerintah.jalur(1); if (처리값 >= 0) 처리값 = BerkasMemori.normalkan_VALUE();
        if (처리값 < 0) { PenafsirPerintah.galat(처리값); return; }
        int 원본번호 = BerkasMemori.FIND_entri(); if (원본번호 < 0) { PenafsirPerintah.galat(-2); return; }
        int entri_COUNT = BerkasMemori.panjang_VALUE[원본번호]; for (int Loop_INDEX = 0; Loop_INDEX < entri_COUNT; Loop_INDEX++) data[Loop_INDEX] = BerkasMemori.자료읽기(원본번호, Loop_INDEX);
        처리값 = PenafsirPerintah.jalur(2); if (처리값 >= 0) 처리값 = BerkasMemori.normalkan_VALUE();
        if (처리값 < 0) { PenafsirPerintah.galat(처리값); return; }
        if (BerkasMemori.FIND_entri() == 원본번호) { if (!이동여부) PenafsirPerintah.galat(-22); return; }
        if (이동여부) { 처리값 = BerkasMemori.이름바꾸기(원본번호); if (처리값 < 0) PenafsirPerintah.galat(처리값); return; }
        int 열린파일번호 = BerkasMemori.Buka(577); if (열린파일번호 < 0) { PenafsirPerintah.galat(열린파일번호); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < entri_COUNT; Loop_INDEX++) { 처리값 = BerkasMemori.Tulis(열린파일번호, data[Loop_INDEX]); if (처리값 < 0) { PenafsirPerintah.galat(처리값); break; } }
        BerkasMemori.Tutup(열린파일번호);
    }
    static int angka_VALUE(int argumen_INDEX) {
        if (argumen_INDEX >= PenafsirPerintah.token_COUNT) return -1;
        int entri_COUNT = 0; for (int Loop_INDEX = 0; Loop_INDEX < PenafsirPerintah.panjang_VALUE[argumen_INDEX]; Loop_INDEX++) { int kode_karakter = PenafsirPerintah.token_VALUE[PenafsirPerintah.시작점[argumen_INDEX] + Loop_INDEX]; if (kode_karakter < '0' || kode_karakter > '9' || entri_COUNT > 10000) return -1; entri_COUNT = entri_COUNT * 10 + kode_karakter - '0'; } return entri_COUNT;
    }
    static void 세기() {
        int argumen_INDEX = 1, 선택번호 = 0;
        if (PenafsirPerintah.같음(1, "-c") || PenafsirPerintah.같음(1, "-l") || PenafsirPerintah.같음(1, "-w")) { 선택번호 = PenafsirPerintah.같음(1, "-c") ? 1 : PenafsirPerintah.같음(1, "-l") ? 2 : 3; argumen_INDEX++; }
        if (PenafsirPerintah.token_COUNT > argumen_INDEX + 1) { PenafsirPerintah.hasil = 2; 단말.Tulis("사용법: wc [-c|-l|-w] [berkas]\n"); return; }
        if (!입력준비(argumen_INDEX)) return;
        int byte_COUNT = 0, 줄수 = 0, 낱말수 = 0, byte_data; boolean 낱말 = false;
        while ((byte_data = Baca()) >= 0 && byte_data != 256) { byte_COUNT++; if (byte_data == 10) 줄수++; boolean SPACE = byte_data == 32 || byte_data >= 9 && byte_data <= 13; if (!SPACE && !낱말) 낱말수++; 낱말 = !SPACE; }
        Tutup(); if (byte_data < 0) { PenafsirPerintah.galat(byte_data); return; }
        if (선택번호 != 0) 단말.수(선택번호 == 1 ? byte_COUNT : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.수(줄수); 단말.문자(' '); 단말.수(낱말수); 단말.문자(' '); 단말.수(byte_COUNT); } 단말.문자(10);
    }
    static void FIND_entri() {
        if (PenafsirPerintah.token_COUNT < 2 || PenafsirPerintah.token_COUNT > 3) { PenafsirPerintah.hasil = 2; 단말.Tulis("사용법: grep 찾을문구 [berkas]\n"); return; }
        if (!입력준비(2)) return;
        int entri_COUNT = 0, byte_data, 일치수 = 0;
        while (true) {
            byte_data = Baca();
            if (byte_data == 10 || byte_data == 256 || byte_data < 0) {
                boolean 찾은여부 = false;
                for (int Loop_INDEX = 0; Loop_INDEX <= entri_COUNT - PenafsirPerintah.panjang_VALUE[1]; Loop_INDEX++) {
                    boolean 같은여부 = true; for (int dalam_posisi = 0; dalam_posisi < PenafsirPerintah.panjang_VALUE[1]; dalam_posisi++) if (data[Loop_INDEX + dalam_posisi] != PenafsirPerintah.token_VALUE[PenafsirPerintah.시작점[1] + dalam_posisi]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (entri_COUNT > 0 || byte_data == 10)) { for (int Loop_INDEX = 0; Loop_INDEX < entri_COUNT; Loop_INDEX++) Papan.직렬쓰기(data[Loop_INDEX]); 단말.문자(10); 일치수++; }
                entri_COUNT = 0; if (byte_data != 10) break;
            } else if (entri_COUNT < data.length) data[entri_COUNT++] = byte_data;
            else { PenafsirPerintah.galat(-28); Tutup(); return; }
        }
        Tutup(); if (byte_data < 0) PenafsirPerintah.galat(byte_data); else if (PenafsirPerintah.hasil == 0) PenafsirPerintah.hasil = 일치수 == 0 ? 1 : 0;
    }
    static void kepala_VALUE(boolean 뒤쪽자리) {
        int argumen_INDEX = 1, 줄수 = 10;
        if (PenafsirPerintah.같음(1, "-n")) { 줄수 = angka_VALUE(2); argumen_INDEX = 3; }
        if (줄수 < 0 || PenafsirPerintah.token_COUNT > argumen_INDEX + 1) { PenafsirPerintah.hasil = 2; 단말.Tulis("사용법: head/tail [-n 줄수] [berkas]\n"); return; }
        if (!입력준비(argumen_INDEX)) return;
        int entri_COUNT = 0, byte_data;
        while ((byte_data = Baca()) != 256 && byte_data >= 0) { if (entri_COUNT == data.length) { PenafsirPerintah.galat(-28); Tutup(); return; } data[entri_COUNT++] = byte_data; }
        Tutup(); if (byte_data < 0) { PenafsirPerintah.galat(byte_data); return; }
        int lokal_Mulai = 0, mengakhiri_posisi = entri_COUNT;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int total_COUNT = 0; for (int Loop_INDEX = entri_COUNT - 2; Loop_INDEX >= 0; Loop_INDEX--) if (data[Loop_INDEX] == 10 && ++total_COUNT == 줄수) { lokal_Mulai = Loop_INDEX + 1; break; } }
        else { int total_COUNT = 0; for (int Loop_INDEX = 0; Loop_INDEX < entri_COUNT; Loop_INDEX++) if (data[Loop_INDEX] == 10 && ++total_COUNT == 줄수) { mengakhiri_posisi = Loop_INDEX + 1; break; } }
        for (int Loop_INDEX = lokal_Mulai; Loop_INDEX < mengakhiri_posisi; Loop_INDEX++) Papan.직렬쓰기(data[Loop_INDEX]);
    }
    static void tulis_Kebersamaan() {
        boolean tambah = PenafsirPerintah.같음(1, "-a"); int argumen_INDEX = tambah ? 2 : 1;
        if (PenafsirPerintah.token_COUNT != argumen_INDEX + 1) { PenafsirPerintah.hasil = 2; 단말.Tulis("사용법: tee [-a] berkas\n"); return; }
        int 열린파일번호 = buat_file(argumen_INDEX, tambah ? 1089 : 577); if (열린파일번호 < 0) { PenafsirPerintah.galat(열린파일번호); return; }
        file_input = -1; int byte_data;
        while ((byte_data = Baca()) != 256 && byte_data >= 0) { int 처리값 = BerkasMemori.Tulis(열린파일번호, byte_data); if (처리값 < 0) { PenafsirPerintah.galat(처리값); break; } Papan.직렬쓰기(byte_data); }
        BerkasMemori.Tutup(열린파일번호);
    }
}
