// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 Schrijven 없이 동작하는 작은 직렬/PS2 Opdrachtvertolker. */
public final class Opdrachtvertolker {
    static int[] invoer_WAARDE = new int[128];
    static int tijdsduur_WAARDE = 0;
    static boolean 앞줄복귀 = false;
    static boolean lijn_overloop = false;

    static boolean opdracht(String Naam) {
        if (tijdsduur_WAARDE < Naam.length()) return false;
        for (int INDEX = 0; INDEX < Naam.length(); INDEX++)
            if (invoer_WAARDE[INDEX] != Naam.charAt(INDEX)) return false;
        return tijdsduur_WAARDE == Naam.length() || invoer_WAARDE[Naam.length()] == ' ';
    }

    static void hulp_tonen() {
        sms_Terminal.Schrijven("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        sms_Terminal.Schrijven("apps | run NAME [ARGS] | net\n");
        sms_Terminal.Schrijven("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        sms_Terminal.Schrijven("sync (연결된 JKSTORE1 Store_WAARDE 장치에 bestand 보존)\n");
    }

    static void Proces_WAARDE_invoer() {
        if (tijdsduur_WAARDE == 0) return;
        if (opdracht("help")) hulp_tonen();
        else if (opdracht("sync")) {
            int resultaat = 파일보존.synchroniseren();
            sms_Terminal.Schrijven("Sync: "); sms_Terminal.schrijven_nummer(resultaat); sms_Terminal.문자(10);
        }
        else if (opdracht("ls")) Geheugen_bestandssysteem.invoer_Lijst_f07b3200();
        else if (opdracht("edit")) Geheugen_bestandssysteem.opdracht(invoer_WAARDE, 4, tijdsduur_WAARDE, 0);
        else if (opdracht("cat")) Geheugen_bestandssysteem.opdracht(invoer_WAARDE, 3, tijdsduur_WAARDE, 1);
        else if (opdracht("rm")) Geheugen_bestandssysteem.opdracht(invoer_WAARDE, 2, tijdsduur_WAARDE, 2);
        else if (opdracht("java") || opdracht("javac")) {
            int resultaat = uitvoerbewerking_Manager.Uitvoeren_opdracht(invoer_WAARDE, 0, tijdsduur_WAARDE);
            sms_Terminal.Schrijven("Exit: "); sms_Terminal.schrijven_nummer(resultaat); sms_Terminal.문자(10);
        }
        else if (opdracht("apps")) uitvoerbewerking_Manager.invoer_Lijst_f07b3200();
        else if (opdracht("net")) net_stack.Status_WAARDE();
        else if (opdracht("run")) {
            int resultaat = uitvoerbewerking_Manager.Uitvoeren_opdracht(invoer_WAARDE, 3, tijdsduur_WAARDE);
            sms_Terminal.Schrijven("Exit: "); sms_Terminal.schrijven_nummer(resultaat); sms_Terminal.Schrijven("\n");
        } else if (opdracht("info")) {
            sms_Terminal.Schrijven("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (opdracht("mem")) {
            sms_Terminal.Schrijven("위쪽 Geheugen_WAARDE ADRES_regio(KiB): "); sms_Terminal.schrijven_nummer(Geheugen_regio.HOOFDLETTERS_Geheugen_formaat_wijzigen());
            sms_Terminal.Schrijven("\n배열 동적 Geheugen_WAARDE ADRES_regio(byte_WAARDE): "); sms_Terminal.schrijven_nummer(mobiel_WAARDE.MATRIX_gebruik());
            sms_Terminal.Schrijven(" / 262144\n작업 ADRES_regio sectie_WAARDE: "); sms_Terminal.schrijven_nummer(Geheugen_regio.사용개수());
            sms_Terminal.Schrijven(" / 8 (각 4096바이트)\n");
        } else if (opdracht("alloc")) {
            int INDEX = Geheugen_regio.toewijzen_Opslag();
            sms_Terminal.Schrijven("sectie_WAARDE INDEX: "); sms_Terminal.schrijven_nummer(INDEX); sms_Terminal.Schrijven("\n");
        } else if (opdracht("free")) {
            if (tijdsduur_WAARDE == 6 && invoer_WAARDE[4] == ' ' && invoer_WAARDE[5] >= '0' && invoer_WAARDE[5] <= '7') {
                sms_Terminal.Schrijven(Geheugen_regio.Retour_HR(invoer_WAARDE[5] - '0') ? "반환됨\n" : "할당되지 않은 sectie_WAARDE\n");
            } else sms_Terminal.Schrijven("사용법: free 0..7\n");
        } else if (opdracht("echo")) {
            for (int INDEX = 5; INDEX < tijdsduur_WAARDE; INDEX++) sms_Terminal.문자(invoer_WAARDE[INDEX]);
            sms_Terminal.문자(10);
        } else if (opdracht("clear")) sms_Terminal.wissen_invoer();
        else if (opdracht("test")) Kern.tests();
        else if (opdracht("halt")) {
            sms_Terminal.Schrijven("HALTED\n");
            mobiel_WAARDE.정지();
        } else sms_Terminal.Schrijven("알 nummer 없는 명령입니다. help를 입력하세요.\n");
    }

    static void accepteren_EN_schrijven(int WAARDE) {
        if (WAARDE == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = WAARDE == 13;
        if (WAARDE == 10 || WAARDE == 13) {
            sms_Terminal.문자(10);
            if (Geheugen_bestandssysteem.편집중) Geheugen_bestandssysteem.Bewerkt_lijn(invoer_WAARDE, tijdsduur_WAARDE, lijn_overloop);
            else Proces_WAARDE_invoer();
            tijdsduur_WAARDE = 0;
            lijn_overloop = false;
            sms_Terminal.Schrijven(Geheugen_bestandssysteem.편집중 ? "...> " : "jkoros> ");
        } else if (WAARDE == 8 || WAARDE == 127) {
            if (tijdsduur_WAARDE > 0) {
                tijdsduur_WAARDE--;
                sms_Terminal.직렬바이트(8); sms_Terminal.직렬바이트(32); sms_Terminal.직렬바이트(8);
                sms_Terminal.scherm_teken(8);
            }
        } else if (WAARDE >= 32 && WAARDE < 127 && tijdsduur_WAARDE < invoer_WAARDE.length) {
            invoer_WAARDE[tijdsduur_WAARDE++] = WAARDE;
            sms_Terminal.문자(WAARDE);
        } else if (WAARDE >= 32 && WAARDE < 127) lijn_overloop = true;
    }

    static void starten() {
        hulp_tonen();
        sms_Terminal.Schrijven("READY\njkoros> ");
        while (true) {
            int WAARDE = sms_Terminal.직렬읽기();
            if (WAARDE < 0) WAARDE = toetsenbord.Lezen();
            if (WAARDE >= 0) accepteren_EN_schrijven(WAARDE);
            else { net_stack.bevestigen(); mobiel_WAARDE.잠시양보(); }
        }
    }
}
