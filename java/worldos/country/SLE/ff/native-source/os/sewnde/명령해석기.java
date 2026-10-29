// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 winndude 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] 입력 = new int[128];
    static int njuuteendi_njaru = 0;
    static boolean 앞줄복귀 = false;
    static boolean diidol_binndi_ɓurtuɗi = false;

    static boolean ginol(String innde) {
        if (njuuteendi_njaru < innde.length()) return false;
        for (int joopirdu = 0; joopirdu < innde.length(); joopirdu++)
            if (입력[joopirdu] != innde.charAt(joopirdu)) return false;
        return njuuteendi_njaru == innde.length() || 입력[innde.length()] == ' ';
    }

    static void hollirde_ballal() {
        문자단말.winndude("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        문자단말.winndude("apps | run NAME [ARGS] | net\n");
        문자단말.winndude("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        문자단말.winndude("sync (연결된 JKSTORE1 resde_njaru 장치에 fiilde 보존)\n");
    }

    static void Yuɓɓo_golle_njaru_naatnugol() {
        if (njuuteendi_njaru == 0) return;
        if (ginol("help")) hollirde_ballal();
        else if (ginol("sync")) {
            int 결과 = 파일보존.sanngoɗinde();
            문자단말.winndude("Sync: "); 문자단말.수쓰기(결과); 문자단말.문자(10);
        }
        else if (ginol("ls")) teskordu_yuɓɓo_piille.naatnugol_Doggol();
        else if (ginol("edit")) teskordu_yuɓɓo_piille.ginol(입력, 4, njuuteendi_njaru, 0);
        else if (ginol("cat")) teskordu_yuɓɓo_piille.ginol(입력, 3, njuuteendi_njaru, 1);
        else if (ginol("rm")) teskordu_yuɓɓo_piille.ginol(입력, 2, njuuteendi_njaru, 2);
        else if (ginol("java") || ginol("javac")) {
            int 결과 = 실행관리.실행(입력, 0, njuuteendi_njaru);
            문자단말.winndude("Exit: "); 문자단말.수쓰기(결과); 문자단말.문자(10);
        }
        else if (ginol("apps")) 실행관리.naatnugol_Doggol();
        else if (ginol("net")) 통신망.ngonka_njaru();
        else if (ginol("run")) {
            int 결과 = 실행관리.실행(입력, 3, njuuteendi_njaru);
            문자단말.winndude("Exit: "); 문자단말.수쓰기(결과); 문자단말.winndude("\n");
        } else if (ginol("info")) {
            문자단말.winndude("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (ginol("mem")) {
            문자단말.winndude("위쪽 teskordu_njaru 공간(KiB): "); 문자단말.수쓰기(기억공간.위쪽기억크기());
            문자단말.winndude("\n배열 동적 teskordu_njaru 공간(oktee_njaru): "); 문자단말.수쓰기(kaɓirgal_njaru.배열사용량());
            문자단말.winndude(" / 262144\n작업 공간 taƴre_njaru: "); 문자단말.수쓰기(기억공간.사용개수());
            문자단말.winndude(" / 8 (각 4096바이트)\n");
        } else if (ginol("alloc")) {
            int joopirdu = 기억공간.할당();
            문자단말.winndude("taƴre_njaru joopirdu: "); 문자단말.수쓰기(joopirdu); 문자단말.winndude("\n");
        } else if (ginol("free")) {
            if (njuuteendi_njaru == 6 && 입력[4] == ' ' && 입력[5] >= '0' && 입력[5] <= '7') {
                문자단말.winndude(기억공간.반환(입력[5] - '0') ? "반환됨\n" : "할당되지 않은 taƴre_njaru\n");
            } else 문자단말.winndude("사용법: free 0..7\n");
        } else if (ginol("echo")) {
            for (int joopirdu = 5; joopirdu < njuuteendi_njaru; joopirdu++) 문자단말.문자(입력[joopirdu]);
            문자단말.문자(10);
        } else if (ginol("clear")) 문자단말.지우기();
        else if (ginol("test")) aaluude.시험();
        else if (ginol("halt")) {
            문자단말.winndude("HALTED\n");
            kaɓirgal_njaru.정지();
        } else 문자단말.winndude("알 수 없는 명령입니다. help를 입력하세요.\n");
    }

    static void 받아쓰기(int njaru) {
        if (njaru == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = njaru == 13;
        if (njaru == 10 || njaru == 13) {
            문자단말.문자(10);
            if (teskordu_yuɓɓo_piille.편집중) teskordu_yuɓɓo_piille.편집줄(입력, njuuteendi_njaru, diidol_binndi_ɓurtuɗi);
            else Yuɓɓo_golle_njaru_naatnugol();
            njuuteendi_njaru = 0;
            diidol_binndi_ɓurtuɗi = false;
            문자단말.winndude(teskordu_yuɓɓo_piille.편집중 ? "...> " : "jkoros> ");
        } else if (njaru == 8 || njaru == 127) {
            if (njuuteendi_njaru > 0) {
                njuuteendi_njaru--;
                문자단말.직렬바이트(8); 문자단말.직렬바이트(32); 문자단말.직렬바이트(8);
                문자단말.화면문자(8);
            }
        } else if (njaru >= 32 && njaru < 127 && njuuteendi_njaru < 입력.length) {
            입력[njuuteendi_njaru++] = njaru;
            문자단말.문자(njaru);
        } else if (njaru >= 32 && njaru < 127) diidol_binndi_ɓurtuɗi = true;
    }

    static void huutoraade() {
        hollirde_ballal();
        문자단말.winndude("READY\njkoros> ");
        while (true) {
            int njaru = 문자단말.직렬읽기();
            if (njaru < 0) njaru = tappirde.읽기();
            if (njaru >= 0) 받아쓰기(njaru);
            else { 통신망.ƴeewtaade(); kaɓirgal_njaru.잠시양보(); }
        }
    }
}
