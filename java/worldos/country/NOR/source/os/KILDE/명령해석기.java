// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 Skriv 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] inndata_VERDI = new int[128];
    static int lengde_VERDI = 0;
    static boolean 앞줄복귀 = false;
    static boolean linje_overløp = false;

    static boolean Kommando(String Navn) {
        if (lengde_VERDI < Navn.length()) return false;
        for (int INDEKS = 0; INDEKS < Navn.length(); INDEKS++)
            if (inndata_VERDI[INDEKS] != Navn.charAt(INDEKS)) return false;
        return lengde_VERDI == Navn.length() || inndata_VERDI[Navn.length()] == ' ';
    }

    static void vise_hjelp() {
        SMS_Terminal.Skriv("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        SMS_Terminal.Skriv("apps | run NAME [ARGS] | net\n");
        SMS_Terminal.Skriv("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        SMS_Terminal.Skriv("sync (연결된 JKSTORE1 Store_VERDI 장치에 Fil 보존)\n");
    }

    static void Prosess_VERDI_oppføring() {
        if (lengde_VERDI == 0) return;
        if (Kommando("help")) vise_hjelp();
        else if (Kommando("sync")) {
            int KR = 파일보존.synkronisere();
            SMS_Terminal.Skriv("Sync: "); SMS_Terminal.skrive_nummer(KR); SMS_Terminal.문자(10);
        }
        else if (Kommando("ls")) Minne_filsystem.oppføring_Liste();
        else if (Kommando("edit")) Minne_filsystem.Kommando(inndata_VERDI, 4, lengde_VERDI, 0);
        else if (Kommando("cat")) Minne_filsystem.Kommando(inndata_VERDI, 3, lengde_VERDI, 1);
        else if (Kommando("rm")) Minne_filsystem.Kommando(inndata_VERDI, 2, lengde_VERDI, 2);
        else if (Kommando("java") || Kommando("javac")) {
            int KR = kjøring_overordnet.Utfør_kommando(inndata_VERDI, 0, lengde_VERDI);
            SMS_Terminal.Skriv("Exit: "); SMS_Terminal.skrive_nummer(KR); SMS_Terminal.문자(10);
        }
        else if (Kommando("apps")) kjøring_overordnet.oppføring_Liste();
        else if (Kommando("net")) nettverk_stakk.status_VERDI();
        else if (Kommando("run")) {
            int KR = kjøring_overordnet.Utfør_kommando(inndata_VERDI, 3, lengde_VERDI);
            SMS_Terminal.Skriv("Exit: "); SMS_Terminal.skrive_nummer(KR); SMS_Terminal.Skriv("\n");
        } else if (Kommando("info")) {
            SMS_Terminal.Skriv("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (Kommando("mem")) {
            SMS_Terminal.Skriv("위쪽 Minne_VERDI e_post_område(KiB): "); SMS_Terminal.skrive_nummer(Minne_område.STORE_Minne_skalere());
            SMS_Terminal.Skriv("\n배열 동적 Minne_VERDI e_post_område(byte_VERDI): "); SMS_Terminal.skrive_nummer(enhet_VERDI.MATRISE_bruk());
            SMS_Terminal.Skriv(" / 262144\n작업 e_post_område inndeling_VERDI: "); SMS_Terminal.skrive_nummer(Minne_område.사용개수());
            SMS_Terminal.Skriv(" / 8 (각 4096바이트)\n");
        } else if (Kommando("alloc")) {
            int INDEKS = Minne_område.tildele_lager();
            SMS_Terminal.Skriv("inndeling_VERDI INDEKS: "); SMS_Terminal.skrive_nummer(INDEKS); SMS_Terminal.Skriv("\n");
        } else if (Kommando("free")) {
            if (lengde_VERDI == 6 && inndata_VERDI[4] == ' ' && inndata_VERDI[5] >= '0' && inndata_VERDI[5] <= '7') {
                SMS_Terminal.Skriv(Minne_område.return_KR(inndata_VERDI[5] - '0') ? "반환됨\n" : "할당되지 않은 inndeling_VERDI\n");
            } else SMS_Terminal.Skriv("사용법: free 0..7\n");
        } else if (Kommando("echo")) {
            for (int INDEKS = 5; INDEKS < lengde_VERDI; INDEKS++) SMS_Terminal.문자(inndata_VERDI[INDEKS]);
            SMS_Terminal.문자(10);
        } else if (Kommando("clear")) SMS_Terminal.slette_oppføring();
        else if (Kommando("test")) kjerne.시험();
        else if (Kommando("halt")) {
            SMS_Terminal.Skriv("HALTED\n");
            enhet_VERDI.정지();
        } else SMS_Terminal.Skriv("알 nummer 없는 명령입니다. help를 입력하세요.\n");
    }

    static void godta_OG_skrive(int VERDI) {
        if (VERDI == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = VERDI == 13;
        if (VERDI == 10 || VERDI == 13) {
            SMS_Terminal.문자(10);
            if (Minne_filsystem.편집중) Minne_filsystem.Redigert_linje(inndata_VERDI, lengde_VERDI, linje_overløp);
            else Prosess_VERDI_oppføring();
            lengde_VERDI = 0;
            linje_overløp = false;
            SMS_Terminal.Skriv(Minne_filsystem.편집중 ? "...> " : "jkoros> ");
        } else if (VERDI == 8 || VERDI == 127) {
            if (lengde_VERDI > 0) {
                lengde_VERDI--;
                SMS_Terminal.직렬바이트(8); SMS_Terminal.직렬바이트(32); SMS_Terminal.직렬바이트(8);
                SMS_Terminal.skjermbilde_tegn(8);
            }
        } else if (VERDI >= 32 && VERDI < 127 && lengde_VERDI < inndata_VERDI.length) {
            inndata_VERDI[lengde_VERDI++] = VERDI;
            SMS_Terminal.문자(VERDI);
        } else if (VERDI >= 32 && VERDI < 127) linje_overløp = true;
    }

    static void Kjør_2() {
        vise_hjelp();
        SMS_Terminal.Skriv("READY\njkoros> ");
        while (true) {
            int VERDI = SMS_Terminal.직렬읽기();
            if (VERDI < 0) VERDI = tastatur.Les();
            if (VERDI >= 0) godta_OG_skrive(VERDI);
            else { nettverk_stakk.bekrefte(); enhet_VERDI.잠시양보(); }
        }
    }
}
