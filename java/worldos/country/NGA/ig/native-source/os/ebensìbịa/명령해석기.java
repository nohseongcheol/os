// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 Chekwaa_ozi 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] 입력 = new int[128];
    static int ogologo_valuu = 0;
    static boolean 앞줄복귀 = false;
    static boolean ahịrī_njubigaoke = false;

    static boolean Ntiiwu(String Aha) {
        if (ogologo_valuu < Aha.length()) return false;
        for (int indèks = 0; indèks < Aha.length(); indèks++)
            if (입력[indèks] != Aha.charAt(indèks)) return false;
        return ogologo_valuu == Aha.length() || 입력[Aha.length()] == ' ';
    }

    static void gòsi_ènyèmaka() {
        문자단말.Chekwaa_ozi("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        문자단말.Chekwaa_ozi("apps | run NAME [ARGS] | net\n");
        문자단말.Chekwaa_ozi("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        문자단말.Chekwaa_ozi("sync (연결된 JKSTORE1 Store_valuu 장치에 Faịlụ 보존)\n");
    }

    static void ùsòrò_valuu_ndebà() {
        if (ogologo_valuu == 0) return;
        if (Ntiiwu("help")) gòsi_ènyèmaka();
        else if (Ntiiwu("sync")) {
            int 결과 = 파일보존.hàkọọ();
            문자단말.Chekwaa_ozi("Sync: "); 문자단말.수쓰기(결과); 문자단말.문자(10);
        }
        else if (Ntiiwu("ls")) memọrị_sistèm_ọbọakwụkwo.ndebà_ndepụta();
        else if (Ntiiwu("edit")) memọrị_sistèm_ọbọakwụkwo.Ntiiwu(입력, 4, ogologo_valuu, 0);
        else if (Ntiiwu("cat")) memọrị_sistèm_ọbọakwụkwo.Ntiiwu(입력, 3, ogologo_valuu, 1);
        else if (Ntiiwu("rm")) memọrị_sistèm_ọbọakwụkwo.Ntiiwu(입력, 2, ogologo_valuu, 2);
        else if (Ntiiwu("java") || Ntiiwu("javac")) {
            int 결과 = 실행관리.mee_nnyemiwu(입력, 0, ogologo_valuu);
            문자단말.Chekwaa_ozi("Exit: "); 문자단말.수쓰기(결과); 문자단말.문자(10);
        }
        else if (Ntiiwu("apps")) 실행관리.ndebà_ndepụta();
        else if (Ntiiwu("net")) Netwọọkụ_ikpo.ọnọdụ_valuu();
        else if (Ntiiwu("run")) {
            int 결과 = 실행관리.mee_nnyemiwu(입력, 3, ogologo_valuu);
            문자단말.Chekwaa_ozi("Exit: "); 문자단말.수쓰기(결과); 문자단말.Chekwaa_ozi("\n");
        } else if (Ntiiwu("info")) {
            문자단말.Chekwaa_ozi("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (Ntiiwu("mem")) {
            문자단말.Chekwaa_ozi("위쪽 memọrị_valuu 공간(KiB): "); 문자단말.수쓰기(기억공간.위쪽기억크기());
            문자단말.Chekwaa_ozi("\n배열 동적 memọrị_valuu 공간(baịtị_valuu): "); 문자단말.수쓰기(njìarụ_valuu.MKPOKỌTA_ojiji());
            문자단말.Chekwaa_ozi(" / 262144\n작업 공간 nkebì_valuu: "); 문자단말.수쓰기(기억공간.사용개수());
            문자단말.Chekwaa_ozi(" / 8 (각 4096바이트)\n");
        } else if (Ntiiwu("alloc")) {
            int indèks = 기억공간.kepụta_Nchekwa();
            문자단말.Chekwaa_ozi("nkebì_valuu indèks: "); 문자단말.수쓰기(indèks); 문자단말.Chekwaa_ozi("\n");
        } else if (Ntiiwu("free")) {
            if (ogologo_valuu == 6 && 입력[4] == ' ' && 입력[5] >= '0' && 입력[5] <= '7') {
                문자단말.Chekwaa_ozi(기억공간.반환(입력[5] - '0') ? "반환됨\n" : "할당되지 않은 nkebì_valuu\n");
            } else 문자단말.Chekwaa_ozi("사용법: free 0..7\n");
        } else if (Ntiiwu("echo")) {
            for (int indèks = 5; indèks < ogologo_valuu; indèks++) 문자단말.문자(입력[indèks]);
            문자단말.문자(10);
        } else if (Ntiiwu("clear")) 문자단말.지우기();
        else if (Ntiiwu("test")) mkpụrụobī_kọmpùta.시험();
        else if (Ntiiwu("halt")) {
            문자단말.Chekwaa_ozi("HALTED\n");
            njìarụ_valuu.정지();
        } else 문자단말.Chekwaa_ozi("알 수 없는 명령입니다. help를 입력하세요.\n");
    }

    static void 받아쓰기(int valuu) {
        if (valuu == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = valuu == 13;
        if (valuu == 10 || valuu == 13) {
            문자단말.문자(10);
            if (memọrị_sistèm_ọbọakwụkwo.편집중) memọrị_sistèm_ọbọakwụkwo.편집줄(입력, ogologo_valuu, ahịrī_njubigaoke);
            else ùsòrò_valuu_ndebà();
            ogologo_valuu = 0;
            ahịrī_njubigaoke = false;
            문자단말.Chekwaa_ozi(memọrị_sistèm_ọbọakwụkwo.편집중 ? "...> " : "jkoros> ");
        } else if (valuu == 8 || valuu == 127) {
            if (ogologo_valuu > 0) {
                ogologo_valuu--;
                문자단말.직렬바이트(8); 문자단말.직렬바이트(32); 문자단말.직렬바이트(8);
                문자단말.화면문자(8);
            }
        } else if (valuu >= 32 && valuu < 127 && ogologo_valuu < 입력.length) {
            입력[ogologo_valuu++] = valuu;
            문자단말.문자(valuu);
        } else if (valuu >= 32 && valuu < 127) ahịrī_njubigaoke = true;
    }

    static void Bido() {
        gòsi_ènyèmaka();
        문자단말.Chekwaa_ozi("READY\njkoros> ");
        while (true) {
            int valuu = 문자단말.직렬읽기();
            if (valuu < 0) valuu = ụgbọọtụgwo.Wepụta_ọzi();
            if (valuu >= 0) 받아쓰기(valuu);
            else { Netwọọkụ_ikpo.nkwàdo_eziokwū(); njìarụ_valuu.잠시양보(); }
        }
    }
}
