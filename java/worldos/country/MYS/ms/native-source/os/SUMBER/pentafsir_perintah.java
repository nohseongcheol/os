// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 Tulis 없이 동작하는 작은 직렬/PS2 pentafsir_perintah. */
public final class pentafsir_perintah {
    static int[] 입력 = new int[128];
    static int kepanjangan_VALUE = 0;
    static boolean 앞줄복귀 = false;
    static boolean baris_limpahan = false;

    static boolean Perintah(String Nama) {
        if (kepanjangan_VALUE < Nama.length()) return false;
        for (int INDEX = 0; INDEX < Nama.length(); INDEX++)
            if (입력[INDEX] != Nama.charAt(INDEX)) return false;
        return kepanjangan_VALUE == Nama.length() || 입력[Nama.length()] == ' ';
    }

    static void paparkan_bantuan() {
        SMS_Terminal.Tulis("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        SMS_Terminal.Tulis("apps | run NAME [ARGS] | net\n");
        SMS_Terminal.Tulis("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        SMS_Terminal.Tulis("sync (연결된 JKSTORE1 stor_VALUE 장치에 Fail 보존)\n");
    }

    static void Proses_VALUE_pemasukan() {
        if (kepanjangan_VALUE == 0) return;
        if (Perintah("help")) paparkan_bantuan();
        else if (Perintah("sync")) {
            int ukuran = 파일보존.segerak();
            SMS_Terminal.Tulis("Sync: "); SMS_Terminal.수쓰기(ukuran); SMS_Terminal.문자(10);
        }
        else if (Perintah("ls")) Memori_sistem_fail.pemasukan_Senarai();
        else if (Perintah("edit")) Memori_sistem_fail.Perintah(입력, 4, kepanjangan_VALUE, 0);
        else if (Perintah("cat")) Memori_sistem_fail.Perintah(입력, 3, kepanjangan_VALUE, 1);
        else if (Perintah("rm")) Memori_sistem_fail.Perintah(입력, 2, kepanjangan_VALUE, 2);
        else if (Perintah("java") || Perintah("javac")) {
            int ukuran = 실행관리.laksanakan_perintah(입력, 0, kepanjangan_VALUE);
            SMS_Terminal.Tulis("Exit: "); SMS_Terminal.수쓰기(ukuran); SMS_Terminal.문자(10);
        }
        else if (Perintah("apps")) 실행관리.pemasukan_Senarai();
        else if (Perintah("net")) rangkaian_tindan.status_VALUE();
        else if (Perintah("run")) {
            int ukuran = 실행관리.laksanakan_perintah(입력, 3, kepanjangan_VALUE);
            SMS_Terminal.Tulis("Exit: "); SMS_Terminal.수쓰기(ukuran); SMS_Terminal.Tulis("\n");
        } else if (Perintah("info")) {
            SMS_Terminal.Tulis("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (Perintah("mem")) {
            SMS_Terminal.Tulis("위쪽 Memori_VALUE e_mel_rantau(KiB): "); SMS_Terminal.수쓰기(Memori_rantau.UPPER_Memori_saiz());
            SMS_Terminal.Tulis("\n배열 동적 Memori_VALUE e_mel_rantau(bait_VALUE): "); SMS_Terminal.수쓰기(peranti_VALUE.배열사용량());
            SMS_Terminal.Tulis(" / 262144\n작업 e_mel_rantau seksyen_VALUE: "); SMS_Terminal.수쓰기(Memori_rantau.사용개수());
            SMS_Terminal.Tulis(" / 8 (각 4096바이트)\n");
        } else if (Perintah("alloc")) {
            int INDEX = Memori_rantau.peruntuk_Storan();
            SMS_Terminal.Tulis("seksyen_VALUE INDEX: "); SMS_Terminal.수쓰기(INDEX); SMS_Terminal.Tulis("\n");
        } else if (Perintah("free")) {
            if (kepanjangan_VALUE == 6 && 입력[4] == ' ' && 입력[5] >= '0' && 입력[5] <= '7') {
                SMS_Terminal.Tulis(Memori_rantau.kembalikan_ukuran(입력[5] - '0') ? "반환됨\n" : "할당되지 않은 seksyen_VALUE\n");
            } else SMS_Terminal.Tulis("사용법: free 0..7\n");
        } else if (Perintah("echo")) {
            for (int INDEX = 5; INDEX < kepanjangan_VALUE; INDEX++) SMS_Terminal.문자(입력[INDEX]);
            SMS_Terminal.문자(10);
        } else if (Perintah("clear")) SMS_Terminal.padam_pemasukan();
        else if (Perintah("test")) kernel.ujian();
        else if (Perintah("halt")) {
            SMS_Terminal.Tulis("HALTED\n");
            peranti_VALUE.정지();
        } else SMS_Terminal.Tulis("알 수 없는 명령입니다. help를 입력하세요.\n");
    }

    static void terima_AND_tulis(int VALUE) {
        if (VALUE == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = VALUE == 13;
        if (VALUE == 10 || VALUE == 13) {
            SMS_Terminal.문자(10);
            if (Memori_sistem_fail.편집중) Memori_sistem_fail.Diedit_baris(입력, kepanjangan_VALUE, baris_limpahan);
            else Proses_VALUE_pemasukan();
            kepanjangan_VALUE = 0;
            baris_limpahan = false;
            SMS_Terminal.Tulis(Memori_sistem_fail.편집중 ? "...> " : "jkoros> ");
        } else if (VALUE == 8 || VALUE == 127) {
            if (kepanjangan_VALUE > 0) {
                kepanjangan_VALUE--;
                SMS_Terminal.직렬바이트(8); SMS_Terminal.직렬바이트(32); SMS_Terminal.직렬바이트(8);
                SMS_Terminal.화면문자(8);
            }
        } else if (VALUE >= 32 && VALUE < 127 && kepanjangan_VALUE < 입력.length) {
            입력[kepanjangan_VALUE++] = VALUE;
            SMS_Terminal.문자(VALUE);
        } else if (VALUE >= 32 && VALUE < 127) baris_limpahan = true;
    }

    static void Jalan() {
        paparkan_bantuan();
        SMS_Terminal.Tulis("READY\njkoros> ");
        while (true) {
            int VALUE = SMS_Terminal.직렬읽기();
            if (VALUE < 0) VALUE = papan_kekunci.Baca();
            if (VALUE >= 0) terima_AND_tulis(VALUE);
            else { rangkaian_tindan.tentu_sahkan(); peranti_VALUE.잠시양보(); }
        }
    }
}
