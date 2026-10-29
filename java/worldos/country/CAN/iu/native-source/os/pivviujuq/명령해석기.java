// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 titiraq 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] 입력 = new int[128];
    static int takininga_atuutilik = 0;
    static boolean 앞줄복귀 = false;
    static boolean titikutaak_tatattuq = false;

    static boolean piqujijjut(String atiq) {
        if (takininga_atuutilik < atiq.length()) return false;
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < atiq.length(); nalunaiqsimavik++)
            if (입력[nalunaiqsimavik] != atiq.charAt(nalunaiqsimavik)) return false;
        return takininga_atuutilik == atiq.length() || 입력[atiq.length()] == ' ';
    }

    static void saqqilli_Ikajuqtau() {
        문자단말.titiraq("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        문자단말.titiraq("apps | run NAME [ARGS] | net\n");
        문자단말.titiraq("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        문자단말.titiraq("sync (연결된 JKSTORE1 tuqqurli_atuutilik 장치에 ini 보존)\n");
    }

    static void Pivallianiq_atuutilik_Iliniku() {
        if (takininga_atuutilik == 0) return;
        if (piqujijjut("help")) saqqilli_Ikajuqtau();
        else if (piqujijjut("sync")) {
            int 결과 = 파일보존.asiqqunniqannginniq();
            문자단말.titiraq("Sync: "); 문자단말.수쓰기(결과); 문자단말.문자(10);
        }
        else if (piqujijjut("ls")) puigujjaikkut_inikkuvik.Iliniku_Titiqpalliagaq();
        else if (piqujijjut("edit")) puigujjaikkut_inikkuvik.piqujijjut(입력, 4, takininga_atuutilik, 0);
        else if (piqujijjut("cat")) puigujjaikkut_inikkuvik.piqujijjut(입력, 3, takininga_atuutilik, 1);
        else if (piqujijjut("rm")) puigujjaikkut_inikkuvik.piqujijjut(입력, 2, takininga_atuutilik, 2);
        else if (piqujijjut("java") || piqujijjut("javac")) {
            int 결과 = 실행관리.실행(입력, 0, takininga_atuutilik);
            문자단말.titiraq("Exit: "); 문자단말.수쓰기(결과); 문자단말.문자(10);
        }
        else if (piqujijjut("apps")) 실행관리.Iliniku_Titiqpalliagaq();
        else if (piqujijjut("net")) 통신망.qanuilinganiq_atuutilik();
        else if (piqujijjut("run")) {
            int 결과 = 실행관리.실행(입력, 3, takininga_atuutilik);
            문자단말.titiraq("Exit: "); 문자단말.수쓰기(결과); 문자단말.titiraq("\n");
        } else if (piqujijjut("info")) {
            문자단말.titiraq("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (piqujijjut("mem")) {
            문자단말.titiraq("위쪽 puigujjaikkut_atuutilik 공간(KiB): "); 문자단말.수쓰기(기억공간.위쪽기억크기());
            문자단말.titiraq("\n배열 동적 puigujjaikkut_atuutilik 공간(byte_atuutilik): "); 문자단말.수쓰기(sunakkutaaq_atuutilik.array_aturniq());
            문자단말.titiraq(" / 262144\n작업 공간 sukuttia_atuutilik: "); 문자단말.수쓰기(기억공간.사용개수());
            문자단말.titiraq(" / 8 (각 4096바이트)\n");
        } else if (piqujijjut("alloc")) {
            int nalunaiqsimavik = 기억공간.할당();
            문자단말.titiraq("sukuttia_atuutilik nalunaiqsimavik: "); 문자단말.수쓰기(nalunaiqsimavik); 문자단말.titiraq("\n");
        } else if (piqujijjut("free")) {
            if (takininga_atuutilik == 6 && 입력[4] == ' ' && 입력[5] >= '0' && 입력[5] <= '7') {
                문자단말.titiraq(기억공간.반환(입력[5] - '0') ? "반환됨\n" : "할당되지 않은 sukuttia_atuutilik\n");
            } else 문자단말.titiraq("사용법: free 0..7\n");
        } else if (piqujijjut("echo")) {
            for (int nalunaiqsimavik = 5; nalunaiqsimavik < takininga_atuutilik; nalunaiqsimavik++) 문자단말.문자(입력[nalunaiqsimavik]);
            문자단말.문자(10);
        } else if (piqujijjut("clear")) 문자단말.지우기();
        else if (piqujijjut("test")) kernel.시험();
        else if (piqujijjut("halt")) {
            문자단말.titiraq("HALTED\n");
            sunakkutaaq_atuutilik.정지();
        } else 문자단말.titiraq("알 수 없는 명령입니다. help를 입력하세요.\n");
    }

    static void 받아쓰기(int atuutilik) {
        if (atuutilik == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = atuutilik == 13;
        if (atuutilik == 10 || atuutilik == 13) {
            문자단말.문자(10);
            if (puigujjaikkut_inikkuvik.편집중) puigujjaikkut_inikkuvik.편집줄(입력, takininga_atuutilik, titikutaak_tatattuq);
            else Pivallianiq_atuutilik_Iliniku();
            takininga_atuutilik = 0;
            titikutaak_tatattuq = false;
            문자단말.titiraq(puigujjaikkut_inikkuvik.편집중 ? "...> " : "jkoros> ");
        } else if (atuutilik == 8 || atuutilik == 127) {
            if (takininga_atuutilik > 0) {
                takininga_atuutilik--;
                문자단말.직렬바이트(8); 문자단말.직렬바이트(32); 문자단말.직렬바이트(8);
                문자단말.화면문자(8);
            }
        } else if (atuutilik >= 32 && atuutilik < 127 && takininga_atuutilik < 입력.length) {
            입력[takininga_atuutilik++] = atuutilik;
            문자단말.문자(atuutilik);
        } else if (atuutilik >= 32 && atuutilik < 127) titikutaak_tatattuq = true;
    }

    static void 시작() {
        saqqilli_Ikajuqtau();
        문자단말.titiraq("READY\njkoros> ");
        while (true) {
            int atuutilik = 문자단말.직렬읽기();
            if (atuutilik < 0) atuutilik = naqittaut.읽기();
            if (atuutilik >= 0) 받아쓰기(atuutilik);
            else { 통신망.nalunairli_1aacb54c(); sunakkutaaq_atuutilik.잠시양보(); }
        }
    }
}
