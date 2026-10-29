// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 Tulis 없이 동작하는 작은 직렬/PS2 PenafsirPerintah. */
public final class PenafsirPerintah {
    static int[] 입력 = new int[128];
    static int panjang_VALUE = 0;
    static boolean 앞줄복귀 = false;
    static boolean baris_luapan = false;

    static boolean perintah(String Nama_2) {
        if (panjang_VALUE < Nama_2.length()) return false;
        for (int INDEX = 0; INDEX < Nama_2.length(); INDEX++)
            if (입력[INDEX] != Nama_2.charAt(INDEX)) return false;
        return panjang_VALUE == Nama_2.length() || 입력[Nama_2.length()] == ' ';
    }

    static void tampilkan_bantuan() {
        SMS_Terminal.Tulis("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        SMS_Terminal.Tulis("apps | run NAME [ARGS] | net\n");
        SMS_Terminal.Tulis("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        SMS_Terminal.Tulis("sync (연결된 JKSTORE1 Store_VALUE 장치에 berkas 보존)\n");
    }

    static void Proses_VALUE_entri() {
        if (panjang_VALUE == 0) return;
        if (perintah("help")) tampilkan_bantuan();
        else if (perintah("sync")) {
            int hasil = 파일보존.sinkro();
            SMS_Terminal.Tulis("Sync: "); SMS_Terminal.수쓰기(hasil); SMS_Terminal.문자(10);
        }
        else if (perintah("ls")) Memori_sistem_berkas.entri_Daftar();
        else if (perintah("edit")) Memori_sistem_berkas.perintah(입력, 4, panjang_VALUE, 0);
        else if (perintah("cat")) Memori_sistem_berkas.perintah(입력, 3, panjang_VALUE, 1);
        else if (perintah("rm")) Memori_sistem_berkas.perintah(입력, 2, panjang_VALUE, 2);
        else if (perintah("java") || perintah("javac")) {
            int hasil = 실행관리.Jalankan_perintah(입력, 0, panjang_VALUE);
            SMS_Terminal.Tulis("Exit: "); SMS_Terminal.수쓰기(hasil); SMS_Terminal.문자(10);
        }
        else if (perintah("apps")) 실행관리.entri_Daftar();
        else if (perintah("net")) jaringan_tumpuk.Status_VALUE();
        else if (perintah("run")) {
            int hasil = 실행관리.Jalankan_perintah(입력, 3, panjang_VALUE);
            SMS_Terminal.Tulis("Exit: "); SMS_Terminal.수쓰기(hasil); SMS_Terminal.Tulis("\n");
        } else if (perintah("info")) {
            SMS_Terminal.Tulis("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (perintah("mem")) {
            SMS_Terminal.Tulis("위쪽 Memori_VALUE surel_wilayah(KiB): "); SMS_Terminal.수쓰기(Memori_wilayah.UPPER_Memori_ukuran());
            SMS_Terminal.Tulis("\n배열 동적 Memori_VALUE surel_wilayah(byte_VALUE): "); SMS_Terminal.수쓰기(Ponsel_VALUE.배열사용량());
            SMS_Terminal.Tulis(" / 262144\n작업 surel_wilayah seksi_VALUE: "); SMS_Terminal.수쓰기(Memori_wilayah.사용개수());
            SMS_Terminal.Tulis(" / 8 (각 4096바이트)\n");
        } else if (perintah("alloc")) {
            int INDEX = Memori_wilayah.alokasi_Storage();
            SMS_Terminal.Tulis("seksi_VALUE INDEX: "); SMS_Terminal.수쓰기(INDEX); SMS_Terminal.Tulis("\n");
        } else if (perintah("free")) {
            if (panjang_VALUE == 6 && 입력[4] == ' ' && 입력[5] >= '0' && 입력[5] <= '7') {
                SMS_Terminal.Tulis(Memori_wilayah.kembalikan_KR(입력[5] - '0') ? "반환됨\n" : "할당되지 않은 seksi_VALUE\n");
            } else SMS_Terminal.Tulis("사용법: free 0..7\n");
        } else if (perintah("echo")) {
            for (int INDEX = 5; INDEX < panjang_VALUE; INDEX++) SMS_Terminal.문자(입력[INDEX]);
            SMS_Terminal.문자(10);
        } else if (perintah("clear")) SMS_Terminal.hapus_entri_c8dbc399();
        else if (perintah("test")) Inti.pengujian();
        else if (perintah("halt")) {
            SMS_Terminal.Tulis("HALTED\n");
            Ponsel_VALUE.정지();
        } else SMS_Terminal.Tulis("알 수 없는 명령입니다. help를 입력하세요.\n");
    }

    static void terima_AND_tulis(int VALUE) {
        if (VALUE == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = VALUE == 13;
        if (VALUE == 10 || VALUE == 13) {
            SMS_Terminal.문자(10);
            if (Memori_sistem_berkas.편집중) Memori_sistem_berkas.Diedit_baris(입력, panjang_VALUE, baris_luapan);
            else Proses_VALUE_entri();
            panjang_VALUE = 0;
            baris_luapan = false;
            SMS_Terminal.Tulis(Memori_sistem_berkas.편집중 ? "...> " : "jkoros> ");
        } else if (VALUE == 8 || VALUE == 127) {
            if (panjang_VALUE > 0) {
                panjang_VALUE--;
                SMS_Terminal.직렬바이트(8); SMS_Terminal.직렬바이트(32); SMS_Terminal.직렬바이트(8);
                SMS_Terminal.화면문자(8);
            }
        } else if (VALUE >= 32 && VALUE < 127 && panjang_VALUE < 입력.length) {
            입력[panjang_VALUE++] = VALUE;
            SMS_Terminal.문자(VALUE);
        } else if (VALUE >= 32 && VALUE < 127) baris_luapan = true;
    }

    static void jalankan() {
        tampilkan_bantuan();
        SMS_Terminal.Tulis("READY\njkoros> ");
        while (true) {
            int VALUE = SMS_Terminal.직렬읽기();
            if (VALUE < 0) VALUE = keyboard.Baca();
            if (VALUE >= 0) terima_AND_tulis(VALUE);
            else { jaringan_tumpuk.periksa(); Ponsel_VALUE.잠시양보(); }
        }
    }
}
