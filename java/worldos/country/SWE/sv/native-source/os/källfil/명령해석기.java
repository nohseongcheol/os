// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 Skriv 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] indata_värde = new int[128];
    static int längd_värde = 0;
    static boolean 앞줄복귀 = false;
    static boolean rad_spill = false;

    static boolean kommando(String Namn) {
        if (längd_värde < Namn.length()) return false;
        for (int INDEX = 0; INDEX < Namn.length(); INDEX++)
            if (indata_värde[INDEX] != Namn.charAt(INDEX)) return false;
        return längd_värde == Namn.length() || indata_värde[Namn.length()] == ' ';
    }

    static void visa_hjälp() {
        SMS_Terminal.Skriv("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        SMS_Terminal.Skriv("apps | run NAME [ARGS] | net\n");
        SMS_Terminal.Skriv("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        SMS_Terminal.Skriv("sync (연결된 JKSTORE1 Store_värde 장치에 filnamn 보존)\n");
    }

    static void Process_värde_post() {
        if (längd_värde == 0) return;
        if (kommando("help")) visa_hjälp();
        else if (kommando("sync")) {
            int RESULTAT = 파일보존.synka();
            SMS_Terminal.Skriv("Sync: "); SMS_Terminal.skriva_nummer(RESULTAT); SMS_Terminal.문자(10);
        }
        else if (kommando("ls")) Minne_filsystem.post_ange();
        else if (kommando("edit")) Minne_filsystem.kommando(indata_värde, 4, längd_värde, 0);
        else if (kommando("cat")) Minne_filsystem.kommando(indata_värde, 3, längd_värde, 1);
        else if (kommando("rm")) Minne_filsystem.kommando(indata_värde, 2, längd_värde, 2);
        else if (kommando("java") || kommando("javac")) {
            int RESULTAT = körning_Ansvarig.köra_kommando(indata_värde, 0, längd_värde);
            SMS_Terminal.Skriv("Exit: "); SMS_Terminal.skriva_nummer(RESULTAT); SMS_Terminal.문자(10);
        }
        else if (kommando("apps")) körning_Ansvarig.post_ange();
        else if (kommando("net")) nätverk_Stack.status_värde();
        else if (kommando("run")) {
            int RESULTAT = körning_Ansvarig.köra_kommando(indata_värde, 3, längd_värde);
            SMS_Terminal.Skriv("Exit: "); SMS_Terminal.skriva_nummer(RESULTAT); SMS_Terminal.Skriv("\n");
        } else if (kommando("info")) {
            SMS_Terminal.Skriv("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (kommando("mem")) {
            SMS_Terminal.Skriv("위쪽 Minne_värde ADRESS_område(KiB): "); SMS_Terminal.skriva_nummer(Minne_område.VERSALER_Minne_storlek());
            SMS_Terminal.Skriv("\n배열 동적 Minne_värde ADRESS_område(byte_värde): "); SMS_Terminal.skriva_nummer(enhet_värde.MATRIS_användning());
            SMS_Terminal.Skriv(" / 262144\n작업 ADRESS_område avsnitt_värde: "); SMS_Terminal.skriva_nummer(Minne_område.사용개수());
            SMS_Terminal.Skriv(" / 8 (각 4096바이트)\n");
        } else if (kommando("alloc")) {
            int INDEX = Minne_område.allokera_minne();
            SMS_Terminal.Skriv("avsnitt_värde INDEX: "); SMS_Terminal.skriva_nummer(INDEX); SMS_Terminal.Skriv("\n");
        } else if (kommando("free")) {
            if (längd_värde == 6 && indata_värde[4] == ' ' && indata_värde[5] >= '0' && indata_värde[5] <= '7') {
                SMS_Terminal.Skriv(Minne_område.Retur_KR(indata_värde[5] - '0') ? "반환됨\n" : "할당되지 않은 avsnitt_värde\n");
            } else SMS_Terminal.Skriv("사용법: free 0..7\n");
        } else if (kommando("echo")) {
            for (int INDEX = 5; INDEX < längd_värde; INDEX++) SMS_Terminal.문자(indata_värde[INDEX]);
            SMS_Terminal.문자(10);
        } else if (kommando("clear")) SMS_Terminal.radera_post();
        else if (kommando("test")) kärna.tester();
        else if (kommando("halt")) {
            SMS_Terminal.Skriv("HALTED\n");
            enhet_värde.정지();
        } else SMS_Terminal.Skriv("알 nummer 없는 명령입니다. help를 입력하세요.\n");
    }

    static void acceptera_AND_skriva(int värde) {
        if (värde == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = värde == 13;
        if (värde == 10 || värde == 13) {
            SMS_Terminal.문자(10);
            if (Minne_filsystem.편집중) Minne_filsystem.Redigerat_rad(indata_värde, längd_värde, rad_spill);
            else Process_värde_post();
            längd_värde = 0;
            rad_spill = false;
            SMS_Terminal.Skriv(Minne_filsystem.편집중 ? "...> " : "jkoros> ");
        } else if (värde == 8 || värde == 127) {
            if (längd_värde > 0) {
                längd_värde--;
                SMS_Terminal.직렬바이트(8); SMS_Terminal.직렬바이트(32); SMS_Terminal.직렬바이트(8);
                SMS_Terminal.skärmbild_tecken(8);
            }
        } else if (värde >= 32 && värde < 127 && längd_värde < indata_värde.length) {
            indata_värde[längd_värde++] = värde;
            SMS_Terminal.문자(värde);
        } else if (värde >= 32 && värde < 127) rad_spill = true;
    }

    static void Kör() {
        visa_hjälp();
        SMS_Terminal.Skriv("READY\njkoros> ");
        while (true) {
            int värde = SMS_Terminal.직렬읽기();
            if (värde < 0) värde = tangentbord.Läs();
            if (värde >= 0) acceptera_AND_skriva(värde);
            else { nätverk_Stack.verifiera(); enhet_värde.잠시양보(); }
        }
    }
}
