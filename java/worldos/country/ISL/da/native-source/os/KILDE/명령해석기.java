// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 Skrive 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] input_VÆRDI = new int[128];
    static int varighed_VÆRDI = 0;
    static boolean 앞줄복귀 = false;
    static boolean linje_overløb = false;

    static boolean Kommando(String Navn) {
        if (varighed_VÆRDI < Navn.length()) return false;
        for (int INDEKS = 0; INDEKS < Navn.length(); INDEKS++)
            if (input_VÆRDI[INDEKS] != Navn.charAt(INDEKS)) return false;
        return varighed_VÆRDI == Navn.length() || input_VÆRDI[Navn.length()] == ' ';
    }

    static void vise_hjælp() {
        sms_Terminal.Skrive("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        sms_Terminal.Skrive("apps | run NAME [ARGS] | net\n");
        sms_Terminal.Skrive("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        sms_Terminal.Skrive("sync (연결된 JKSTORE1 Store_VÆRDI 장치에 Fil 보존)\n");
    }

    static void Proces_VÆRDI_post() {
        if (varighed_VÆRDI == 0) return;
        if (Kommando("help")) vise_hjælp();
        else if (Kommando("sync")) {
            int KR = 파일보존.synkronisere();
            sms_Terminal.Skrive("Sync: "); sms_Terminal.skrive_tal(KR); sms_Terminal.문자(10);
        }
        else if (Kommando("ls")) Hukommelse_filsystem.post_Liste();
        else if (Kommando("edit")) Hukommelse_filsystem.Kommando(input_VÆRDI, 4, varighed_VÆRDI, 0);
        else if (Kommando("cat")) Hukommelse_filsystem.Kommando(input_VÆRDI, 3, varighed_VÆRDI, 1);
        else if (Kommando("rm")) Hukommelse_filsystem.Kommando(input_VÆRDI, 2, varighed_VÆRDI, 2);
        else if (Kommando("java") || Kommando("javac")) {
            int KR = udførelse_Leder.Udfør_kommando(input_VÆRDI, 0, varighed_VÆRDI);
            sms_Terminal.Skrive("Exit: "); sms_Terminal.skrive_tal(KR); sms_Terminal.문자(10);
        }
        else if (Kommando("apps")) udførelse_Leder.post_Liste();
        else if (Kommando("net")) netværk_Stak.status_VÆRDI();
        else if (Kommando("run")) {
            int KR = udførelse_Leder.Udfør_kommando(input_VÆRDI, 3, varighed_VÆRDI);
            sms_Terminal.Skrive("Exit: "); sms_Terminal.skrive_tal(KR); sms_Terminal.Skrive("\n");
        } else if (Kommando("info")) {
            sms_Terminal.Skrive("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (Kommando("mem")) {
            sms_Terminal.Skrive("위쪽 Hukommelse_VÆRDI mail_område(KiB): "); sms_Terminal.skrive_tal(Hukommelse_område.STORE_BOGSTAVER_Hukommelse_tilpasse_størrelse());
            sms_Terminal.Skrive("\n배열 동적 Hukommelse_VÆRDI mail_område(byte_VÆRDI): "); sms_Terminal.skrive_tal(enhed_VÆRDI.MATRIX_brug());
            sms_Terminal.Skrive(" / 262144\n작업 mail_område sektion_VÆRDI: "); sms_Terminal.skrive_tal(Hukommelse_område.사용개수());
            sms_Terminal.Skrive(" / 8 (각 4096바이트)\n");
        } else if (Kommando("alloc")) {
            int INDEKS = Hukommelse_område.tildel_Lager();
            sms_Terminal.Skrive("sektion_VÆRDI INDEKS: "); sms_Terminal.skrive_tal(INDEKS); sms_Terminal.Skrive("\n");
        } else if (Kommando("free")) {
            if (varighed_VÆRDI == 6 && input_VÆRDI[4] == ' ' && input_VÆRDI[5] >= '0' && input_VÆRDI[5] <= '7') {
                sms_Terminal.Skrive(Hukommelse_område.returnere_KR(input_VÆRDI[5] - '0') ? "반환됨\n" : "할당되지 않은 sektion_VÆRDI\n");
            } else sms_Terminal.Skrive("사용법: free 0..7\n");
        } else if (Kommando("echo")) {
            for (int INDEKS = 5; INDEKS < varighed_VÆRDI; INDEKS++) sms_Terminal.문자(input_VÆRDI[INDEKS]);
            sms_Terminal.문자(10);
        } else if (Kommando("clear")) sms_Terminal.slette_post();
        else if (Kommando("test")) kerne.시험();
        else if (Kommando("halt")) {
            sms_Terminal.Skrive("HALTED\n");
            enhed_VÆRDI.정지();
        } else sms_Terminal.Skrive("알 tal 없는 명령입니다. help를 입력하세요.\n");
    }

    static void acceptere_OG_skrive(int VÆRDI) {
        if (VÆRDI == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = VÆRDI == 13;
        if (VÆRDI == 10 || VÆRDI == 13) {
            sms_Terminal.문자(10);
            if (Hukommelse_filsystem.편집중) Hukommelse_filsystem.Redigeret_linje(input_VÆRDI, varighed_VÆRDI, linje_overløb);
            else Proces_VÆRDI_post();
            varighed_VÆRDI = 0;
            linje_overløb = false;
            sms_Terminal.Skrive(Hukommelse_filsystem.편집중 ? "...> " : "jkoros> ");
        } else if (VÆRDI == 8 || VÆRDI == 127) {
            if (varighed_VÆRDI > 0) {
                varighed_VÆRDI--;
                sms_Terminal.직렬바이트(8); sms_Terminal.직렬바이트(32); sms_Terminal.직렬바이트(8);
                sms_Terminal.skærmbillede_tegn(8);
            }
        } else if (VÆRDI >= 32 && VÆRDI < 127 && varighed_VÆRDI < input_VÆRDI.length) {
            input_VÆRDI[varighed_VÆRDI++] = VÆRDI;
            sms_Terminal.문자(VÆRDI);
        } else if (VÆRDI >= 32 && VÆRDI < 127) linje_overløb = true;
    }

    static void Kør_2() {
        vise_hjælp();
        sms_Terminal.Skrive("READY\njkoros> ");
        while (true) {
            int VÆRDI = sms_Terminal.직렬읽기();
            if (VÆRDI < 0) VÆRDI = tastatur.Læse();
            if (VÆRDI >= 0) acceptere_OG_skrive(VÆRDI);
            else { netværk_Stak.bekræfte(); enhed_VÆRDI.잠시양보(); }
        }
    }
}
