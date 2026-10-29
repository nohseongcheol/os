// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 kwala 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] 입력 = new int[128];
    static int boleele_Boleng = 0;
    static boolean 앞줄복귀 = false;
    static boolean Mola_penologo = false;

    static boolean Taelo(String leina) {
        if (boleele_Boleng < leina.length()) return false;
        for (int tshupane = 0; tshupane < leina.length(); tshupane++)
            if (입력[tshupane] != leina.charAt(tshupane)) return false;
        return boleele_Boleng == leina.length() || 입력[leina.length()] == ' ';
    }

    static void bontsha_thuso() {
        문자단말.kwala("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        문자단말.kwala("apps | run NAME [ARGS] | net\n");
        문자단말.kwala("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        문자단말.kwala("sync (연결된 JKSTORE1 Store_Boleng 장치에 faele 보존)\n");
    }

    static void Thulaganyo_Boleng_tsenyo() {
        if (boleele_Boleng == 0) return;
        if (Taelo("help")) bontsha_thuso();
        else if (Taelo("sync")) {
            int 결과 = 파일보존.tsamaisanya();
            문자단말.kwala("Sync: "); 문자단말.수쓰기(결과); 문자단말.문자(10);
        }
        else if (Taelo("ls")) memori_setsamaisadifaele.tsenyo_lenaane();
        else if (Taelo("edit")) memori_setsamaisadifaele.Taelo(입력, 4, boleele_Boleng, 0);
        else if (Taelo("cat")) memori_setsamaisadifaele.Taelo(입력, 3, boleele_Boleng, 1);
        else if (Taelo("rm")) memori_setsamaisadifaele.Taelo(입력, 2, boleele_Boleng, 2);
        else if (Taelo("java") || Taelo("javac")) {
            int 결과 = 실행관리.diragatsa_Taelo(입력, 0, boleele_Boleng);
            문자단말.kwala("Exit: "); 문자단말.수쓰기(결과); 문자단말.문자(10);
        }
        else if (Taelo("apps")) 실행관리.tsenyo_lenaane();
        else if (Taelo("net")) Neteweke_kokoanyodinepe.kemo_Boleng();
        else if (Taelo("run")) {
            int 결과 = 실행관리.diragatsa_Taelo(입력, 3, boleele_Boleng);
            문자단말.kwala("Exit: "); 문자단말.수쓰기(결과); 문자단말.kwala("\n");
        } else if (Taelo("info")) {
            문자단말.kwala("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (Taelo("mem")) {
            문자단말.kwala("위쪽 memori_Boleng 공간(KiB): "); 문자단말.수쓰기(기억공간.위쪽기억크기());
            문자단말.kwala("\n배열 동적 memori_Boleng 공간(baete_Boleng): "); 문자단말.수쓰기(mobaele_Boleng.setlhopha_tiriso());
            문자단말.kwala(" / 262144\n작업 공간 karolo_Boleng: "); 문자단말.수쓰기(기억공간.사용개수());
            문자단말.kwala(" / 8 (각 4096바이트)\n");
        } else if (Taelo("alloc")) {
            int tshupane = 기억공간.abela_Polokelo();
            문자단말.kwala("karolo_Boleng tshupane: "); 문자단말.수쓰기(tshupane); 문자단말.kwala("\n");
        } else if (Taelo("free")) {
            if (boleele_Boleng == 6 && 입력[4] == ' ' && 입력[5] >= '0' && 입력[5] <= '7') {
                문자단말.kwala(기억공간.반환(입력[5] - '0') ? "반환됨\n" : "할당되지 않은 karolo_Boleng\n");
            } else 문자단말.kwala("사용법: free 0..7\n");
        } else if (Taelo("echo")) {
            for (int tshupane = 5; tshupane < boleele_Boleng; tshupane++) 문자단말.문자(입력[tshupane]);
            문자단말.문자(10);
        } else if (Taelo("clear")) 문자단말.지우기();
        else if (Taelo("test")) Khenele.시험();
        else if (Taelo("halt")) {
            문자단말.kwala("HALTED\n");
            mobaele_Boleng.정지();
        } else 문자단말.kwala("알 수 없는 명령입니다. help를 입력하세요.\n");
    }

    static void 받아쓰기(int Boleng) {
        if (Boleng == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = Boleng == 13;
        if (Boleng == 10 || Boleng == 13) {
            문자단말.문자(10);
            if (memori_setsamaisadifaele.편집중) memori_setsamaisadifaele.편집줄(입력, boleele_Boleng, Mola_penologo);
            else Thulaganyo_Boleng_tsenyo();
            boleele_Boleng = 0;
            Mola_penologo = false;
            문자단말.kwala(memori_setsamaisadifaele.편집중 ? "...> " : "jkoros> ");
        } else if (Boleng == 8 || Boleng == 127) {
            if (boleele_Boleng > 0) {
                boleele_Boleng--;
                문자단말.직렬바이트(8); 문자단말.직렬바이트(32); 문자단말.직렬바이트(8);
                문자단말.화면문자(8);
            }
        } else if (Boleng >= 32 && Boleng < 127 && boleele_Boleng < 입력.length) {
            입력[boleele_Boleng++] = Boleng;
            문자단말.문자(Boleng);
        } else if (Boleng >= 32 && Boleng < 127) Mola_penologo = true;
    }

    static void dirisa() {
        bontsha_thuso();
        문자단말.kwala("READY\njkoros> ");
        while (true) {
            int Boleng = 문자단말.직렬읽기();
            if (Boleng < 0) Boleng = Khiiboto.읽기();
            if (Boleng >= 0) 받아쓰기(Boleng);
            else { Neteweke_kokoanyodinepe.netefatsa(); mobaele_Boleng.잠시양보(); }
        }
    }
}
