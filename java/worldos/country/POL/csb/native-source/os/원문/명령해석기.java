// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 Zapiszë 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] 입력 = new int[128];
    static int 길이 = 0;
    static boolean 앞줄복귀 = false;
    static boolean 줄넘침 = false;

    static boolean Pòlét(String 이름) {
        if (길이 < 이름.length()) return false;
        for (int 번호 = 0; 번호 < 이름.length(); 번호++)
            if (입력[번호] != 이름.charAt(번호)) return false;
        return 길이 == 이름.length() || 입력[이름.length()] == ' ';
    }

    static void 도움말() {
        문자단말.Zapiszë("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        문자단말.Zapiszë("apps | run NAME [ARGS] | net\n");
        문자단말.Zapiszë("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        문자단말.Zapiszë("sync (연결된 JKSTORE1 저장 장치에 Lopk 보존)\n");
    }

    static void 처리() {
        if (길이 == 0) return;
        if (Pòlét("help")) 도움말();
        else if (Pòlét("sync")) {
            int 결과 = 파일보존.동기화();
            문자단말.Zapiszë("Sync: "); 문자단말.수쓰기(결과); 문자단말.문자(10);
        }
        else if (Pòlét("ls")) 주기억파일체계.목록();
        else if (Pòlét("edit")) 주기억파일체계.Pòlét(입력, 4, 길이, 0);
        else if (Pòlét("cat")) 주기억파일체계.Pòlét(입력, 3, 길이, 1);
        else if (Pòlét("rm")) 주기억파일체계.Pòlét(입력, 2, 길이, 2);
        else if (Pòlét("java") || Pòlét("javac")) {
            int 결과 = 실행관리.실행(입력, 0, 길이);
            문자단말.Zapiszë("Exit: "); 문자단말.수쓰기(결과); 문자단말.문자(10);
        }
        else if (Pòlét("apps")) 실행관리.목록();
        else if (Pòlét("net")) 통신망.상태();
        else if (Pòlét("run")) {
            int 결과 = 실행관리.실행(입력, 3, 길이);
            문자단말.Zapiszë("Exit: "); 문자단말.수쓰기(결과); 문자단말.Zapiszë("\n");
        } else if (Pòlét("info")) {
            문자단말.Zapiszë("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (Pòlét("mem")) {
            문자단말.Zapiszë("위쪽 기억 공간(KiB): "); 문자단말.수쓰기(기억공간.위쪽기억크기());
            문자단말.Zapiszë("\n배열 동적 기억 공간(바이트): "); 문자단말.수쓰기(장치.배열사용량());
            문자단말.Zapiszë(" / 262144\n작업 공간 구역: "); 문자단말.수쓰기(기억공간.사용개수());
            문자단말.Zapiszë(" / 8 (각 4096바이트)\n");
        } else if (Pòlét("alloc")) {
            int 번호 = 기억공간.할당();
            문자단말.Zapiszë("구역 번호: "); 문자단말.수쓰기(번호); 문자단말.Zapiszë("\n");
        } else if (Pòlét("free")) {
            if (길이 == 6 && 입력[4] == ' ' && 입력[5] >= '0' && 입력[5] <= '7') {
                문자단말.Zapiszë(기억공간.반환(입력[5] - '0') ? "반환됨\n" : "할당되지 않은 구역\n");
            } else 문자단말.Zapiszë("사용법: free 0..7\n");
        } else if (Pòlét("echo")) {
            for (int 번호 = 5; 번호 < 길이; 번호++) 문자단말.문자(입력[번호]);
            문자단말.문자(10);
        } else if (Pòlét("clear")) 문자단말.지우기();
        else if (Pòlét("test")) 핵심.시험();
        else if (Pòlét("halt")) {
            문자단말.Zapiszë("HALTED\n");
            장치.정지();
        } else 문자단말.Zapiszë("알 수 없는 명령입니다. help를 입력하세요.\n");
    }

    static void 받아쓰기(int 값) {
        if (값 == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = 값 == 13;
        if (값 == 10 || 값 == 13) {
            문자단말.문자(10);
            if (주기억파일체계.편집중) 주기억파일체계.편집줄(입력, 길이, 줄넘침);
            else 처리();
            길이 = 0;
            줄넘침 = false;
            문자단말.Zapiszë(주기억파일체계.편집중 ? "...> " : "jkoros> ");
        } else if (값 == 8 || 값 == 127) {
            if (길이 > 0) {
                길이--;
                문자단말.직렬바이트(8); 문자단말.직렬바이트(32); 문자단말.직렬바이트(8);
                문자단말.화면문자(8);
            }
        } else if (값 >= 32 && 값 < 127 && 길이 < 입력.length) {
            입력[길이++] = 값;
            문자단말.문자(값);
        } else if (값 >= 32 && 값 < 127) 줄넘침 = true;
    }

    static void 시작() {
        도움말();
        문자단말.Zapiszë("READY\njkoros> ");
        while (true) {
            int 값 = 문자단말.직렬읽기();
            if (값 < 0) 값 = 글쇠판.Przeczëtóné();
            if (값 >= 0) 받아쓰기(값);
            else { 통신망.확인(); 장치.잠시양보(); }
        }
    }
}
