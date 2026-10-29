// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 ashajaa 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] 입력 = new int[128];
    static int akaliaa_ajutuu = 0;
    static boolean 앞줄복귀 = false;
    static boolean 줄넘침 = false;

    static boolean aluwataaya(String 이름) {
        if (akaliaa_ajutuu < 이름.length()) return false;
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < 이름.length(); ee_iyatialujuna++)
            if (입력[ee_iyatialujuna] != 이름.charAt(ee_iyatialujuna)) return false;
        return akaliaa_ajutuu == 이름.length() || 입력[이름.length()] == ' ';
    }

    static void 도움말() {
        문자단말.ashajaa("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        문자단말.ashajaa("apps | run NAME [ARGS] | net\n");
        문자단말.ashajaa("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        문자단말.ashajaa("sync (연결된 JKSTORE1 저장 장치에 anaajaalaa 보존)\n");
    }

    static void 처리() {
        if (akaliaa_ajutuu == 0) return;
        if (aluwataaya("help")) 도움말();
        else if (aluwataaya("sync")) {
            int 결과 = 파일보존.awanaawajaa();
            문자단말.ashajaa("Sync: "); 문자단말.수쓰기(결과); 문자단말.문자(10);
        }
        else if (aluwataaya("ls")) 주기억파일체계.목록();
        else if (aluwataaya("edit")) 주기억파일체계.aluwataaya(입력, 4, akaliaa_ajutuu, 0);
        else if (aluwataaya("cat")) 주기억파일체계.aluwataaya(입력, 3, akaliaa_ajutuu, 1);
        else if (aluwataaya("rm")) 주기억파일체계.aluwataaya(입력, 2, akaliaa_ajutuu, 2);
        else if (aluwataaya("java") || aluwataaya("javac")) {
            int 결과 = 실행관리.실행(입력, 0, akaliaa_ajutuu);
            문자단말.ashajaa("Exit: "); 문자단말.수쓰기(결과); 문자단말.문자(10);
        }
        else if (aluwataaya("apps")) 실행관리.목록();
        else if (aluwataaya("net")) 통신망.jamakua_iparülein_ajutuu();
        else if (aluwataaya("run")) {
            int 결과 = 실행관리.실행(입력, 3, akaliaa_ajutuu);
            문자단말.ashajaa("Exit: "); 문자단말.수쓰기(결과); 문자단말.ashajaa("\n");
        } else if (aluwataaya("info")) {
            문자단말.ashajaa("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (aluwataaya("mem")) {
            문자단말.ashajaa("위쪽 기억 공간(KiB): "); 문자단말.수쓰기(기억공간.위쪽기억크기());
            문자단말.ashajaa("\n배열 동적 기억 공간(waai_ajutuu): "); 문자단말.수쓰기(serulaalü_ajutuu.배열사용량());
            문자단말.ashajaa(" / 262144\n작업 공간 alüjalee_ajutuu: "); 문자단말.수쓰기(기억공간.사용개수());
            문자단말.ashajaa(" / 8 (각 4096바이트)\n");
        } else if (aluwataaya("alloc")) {
            int ee_iyatialujuna = 기억공간.할당();
            문자단말.ashajaa("alüjalee_ajutuu ee_iyatialujuna: "); 문자단말.수쓰기(ee_iyatialujuna); 문자단말.ashajaa("\n");
        } else if (aluwataaya("free")) {
            if (akaliaa_ajutuu == 6 && 입력[4] == ' ' && 입력[5] >= '0' && 입력[5] <= '7') {
                문자단말.ashajaa(기억공간.반환(입력[5] - '0') ? "반환됨\n" : "할당되지 않은 alüjalee_ajutuu\n");
            } else 문자단말.ashajaa("사용법: free 0..7\n");
        } else if (aluwataaya("echo")) {
            for (int ee_iyatialujuna = 5; ee_iyatialujuna < akaliaa_ajutuu; ee_iyatialujuna++) 문자단말.문자(입력[ee_iyatialujuna]);
            문자단말.문자(10);
        } else if (aluwataaya("clear")) 문자단말.지우기();
        else if (aluwataaya("test")) keetnerü.시험();
        else if (aluwataaya("halt")) {
            문자단말.ashajaa("HALTED\n");
            serulaalü_ajutuu.정지();
        } else 문자단말.ashajaa("알 수 없는 명령입니다. help를 입력하세요.\n");
    }

    static void 받아쓰기(int ajutuu) {
        if (ajutuu == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = ajutuu == 13;
        if (ajutuu == 10 || ajutuu == 13) {
            문자단말.문자(10);
            if (주기억파일체계.편집중) 주기억파일체계.편집줄(입력, akaliaa_ajutuu, 줄넘침);
            else 처리();
            akaliaa_ajutuu = 0;
            줄넘침 = false;
            문자단말.ashajaa(주기억파일체계.편집중 ? "...> " : "jkoros> ");
        } else if (ajutuu == 8 || ajutuu == 127) {
            if (akaliaa_ajutuu > 0) {
                akaliaa_ajutuu--;
                문자단말.직렬바이트(8); 문자단말.직렬바이트(32); 문자단말.직렬바이트(8);
                문자단말.화면문자(8);
            }
        } else if (ajutuu >= 32 && ajutuu < 127 && akaliaa_ajutuu < 입력.length) {
            입력[akaliaa_ajutuu++] = ajutuu;
            문자단말.문자(ajutuu);
        } else if (ajutuu >= 32 && ajutuu < 127) 줄넘침 = true;
    }

    static void 시작() {
        도움말();
        문자단말.ashajaa("READY\njkoros> ");
        while (true) {
            int ajutuu = 문자단말.직렬읽기();
            if (ajutuu < 0) ajutuu = ajüttiaapala.읽기();
            if (ajutuu >= 0) 받아쓰기(ajutuu);
            else { 통신망.확인(); serulaalü_ajutuu.잠시양보(); }
        }
    }
}
