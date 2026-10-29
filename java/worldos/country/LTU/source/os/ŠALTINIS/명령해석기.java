// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 Rašymas 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] 입력 = new int[128];
    static int 길이 = 0;
    static boolean 앞줄복귀 = false;
    static boolean eilutė_perpilda = false;

    static boolean Komanda(String Pavadinimas_2) {
        if (길이 < Pavadinimas_2.length()) return false;
        for (int INDEX = 0; INDEX < Pavadinimas_2.length(); INDEX++)
            if (입력[INDEX] != Pavadinimas_2.charAt(INDEX)) return false;
        return 길이 == Pavadinimas_2.length() || 입력[Pavadinimas_2.length()] == ' ';
    }

    static void laida_žinynas() {
        SMS_Terminalas.Rašymas("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        SMS_Terminalas.Rašymas("apps | run NAME [ARGS] | net\n");
        SMS_Terminalas.Rašymas("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        SMS_Terminalas.Rašymas("sync (연결된 JKSTORE1 Store_VALUE 장치에 Failas 보존)\n");
    }

    static void Procesas_VALUE_įrašas() {
        if (길이 == 0) return;
        if (Komanda("help")) laida_žinynas();
        else if (Komanda("sync")) {
            int REZULTATAS = 파일보존.sinchronizuoti();
            SMS_Terminalas.Rašymas("Sync: "); SMS_Terminalas.rašymas_numeris(REZULTATAS); SMS_Terminalas.문자(10);
        }
        else if (Komanda("ls")) atmintis_failų_sistema.įrašas_Sąrašas();
        else if (Komanda("edit")) atmintis_failų_sistema.Komanda(입력, 4, 길이, 0);
        else if (Komanda("cat")) atmintis_failų_sistema.Komanda(입력, 3, 길이, 1);
        else if (Komanda("rm")) atmintis_failų_sistema.Komanda(입력, 2, 길이, 2);
        else if (Komanda("java") || Komanda("javac")) {
            int REZULTATAS = 실행관리.Vykdyti_komanda(입력, 0, 길이);
            SMS_Terminalas.Rašymas("Exit: "); SMS_Terminalas.rašymas_numeris(REZULTATAS); SMS_Terminalas.문자(10);
        }
        else if (Komanda("apps")) 실행관리.įrašas_Sąrašas();
        else if (Komanda("net")) tinklas_eilė.Būsena_VALUE();
        else if (Komanda("run")) {
            int REZULTATAS = 실행관리.Vykdyti_komanda(입력, 3, 길이);
            SMS_Terminalas.Rašymas("Exit: "); SMS_Terminalas.rašymas_numeris(REZULTATAS); SMS_Terminalas.Rašymas("\n");
        } else if (Komanda("info")) {
            SMS_Terminalas.Rašymas("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (Komanda("mem")) {
            SMS_Terminalas.Rašymas("위쪽 atmintis_VALUE ADDRESS_sritis(KiB): "); SMS_Terminalas.rašymas_numeris(atmintis_sritis.UPPER_atmintis_dydis());
            SMS_Terminalas.Rašymas("\n배열 동적 atmintis_VALUE ADDRESS_sritis(baitas_VALUE): "); SMS_Terminalas.rašymas_numeris(įrenginys_VALUE.ARRAY_naudojimas());
            SMS_Terminalas.Rašymas(" / 262144\n작업 ADDRESS_sritis sekcija_VALUE: "); SMS_Terminalas.rašymas_numeris(atmintis_sritis.사용개수());
            SMS_Terminalas.Rašymas(" / 8 (각 4096바이트)\n");
        } else if (Komanda("alloc")) {
            int INDEX = atmintis_sritis.priskirti_Saugykla();
            SMS_Terminalas.Rašymas("sekcija_VALUE INDEX: "); SMS_Terminalas.rašymas_numeris(INDEX); SMS_Terminalas.Rašymas("\n");
        } else if (Komanda("free")) {
            if (길이 == 6 && 입력[4] == ' ' && 입력[5] >= '0' && 입력[5] <= '7') {
                SMS_Terminalas.Rašymas(atmintis_sritis.grąžinti_KR(입력[5] - '0') ? "반환됨\n" : "할당되지 않은 sekcija_VALUE\n");
            } else SMS_Terminalas.Rašymas("사용법: free 0..7\n");
        } else if (Komanda("echo")) {
            for (int INDEX = 5; INDEX < 길이; INDEX++) SMS_Terminalas.문자(입력[INDEX]);
            SMS_Terminalas.문자(10);
        } else if (Komanda("clear")) SMS_Terminalas.ištrinti_įrašas();
        else if (Komanda("test")) branduolys.시험();
        else if (Komanda("halt")) {
            SMS_Terminalas.Rašymas("HALTED\n");
            įrenginys_VALUE.정지();
        } else SMS_Terminalas.Rašymas("알 numeris 없는 명령입니다. help를 입력하세요.\n");
    }

    static void priimti_AND_rašymas(int VALUE) {
        if (VALUE == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = VALUE == 13;
        if (VALUE == 10 || VALUE == 13) {
            SMS_Terminalas.문자(10);
            if (atmintis_failų_sistema.편집중) atmintis_failų_sistema.Redaguotos_eilutė(입력, 길이, eilutė_perpilda);
            else Procesas_VALUE_įrašas();
            길이 = 0;
            eilutė_perpilda = false;
            SMS_Terminalas.Rašymas(atmintis_failų_sistema.편집중 ? "...> " : "jkoros> ");
        } else if (VALUE == 8 || VALUE == 127) {
            if (길이 > 0) {
                길이--;
                SMS_Terminalas.직렬바이트(8); SMS_Terminalas.직렬바이트(32); SMS_Terminalas.직렬바이트(8);
                SMS_Terminalas.화면문자(8);
            }
        } else if (VALUE >= 32 && VALUE < 127 && 길이 < 입력.length) {
            입력[길이++] = VALUE;
            SMS_Terminalas.문자(VALUE);
        } else if (VALUE >= 32 && VALUE < 127) eilutė_perpilda = true;
    }

    static void Paleisti() {
        laida_žinynas();
        SMS_Terminalas.Rašymas("READY\njkoros> ");
        while (true) {
            int VALUE = SMS_Terminalas.직렬읽기();
            if (VALUE < 0) VALUE = klaviatūra.Skaitymas();
            if (VALUE >= 0) priimti_AND_rašymas(VALUE);
            else { tinklas_eilė.patvirtinti(); įrenginys_VALUE.잠시양보(); }
        }
    }
}
