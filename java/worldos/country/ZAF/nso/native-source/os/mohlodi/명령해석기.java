// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 Ngwala 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] 입력 = new int[128];
    static int botelele_boleng = 0;
    static boolean 앞줄복귀 = false;
    static boolean mothaladi_mongwaloutama = false;

    static boolean Taelo(String Leina) {
        if (botelele_boleng < Leina.length()) return false;
        for (int lokela = 0; lokela < Leina.length(); lokela++)
            if (입력[lokela] != Leina.charAt(lokela)) return false;
        return botelele_boleng == Leina.length() || 입력[Leina.length()] == ' ';
    }

    static void bontšha_thušo() {
        문자단말.Ngwala("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        문자단말.Ngwala("apps | run NAME [ARGS] | net\n");
        문자단말.Ngwala("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        문자단말.Ngwala("sync (연결된 JKSTORE1 lota_boleng 장치에 Faele 보존)\n");
    }

    static void tiragalo_boleng_go_tsenya_tshedimošo() {
        if (botelele_boleng == 0) return;
        if (Taelo("help")) bontšha_thušo();
        else if (Taelo("sync")) {
            int 결과 = 파일보존.kopanya();
            문자단말.Ngwala("Sync: "); 문자단말.수쓰기(결과); 문자단말.문자(10);
        }
        else if (Taelo("ls")) memori_tshepedišo_ya_difaele.go_tsenya_tshedimošo_Lenaneo();
        else if (Taelo("edit")) memori_tshepedišo_ya_difaele.Taelo(입력, 4, botelele_boleng, 0);
        else if (Taelo("cat")) memori_tshepedišo_ya_difaele.Taelo(입력, 3, botelele_boleng, 1);
        else if (Taelo("rm")) memori_tshepedišo_ya_difaele.Taelo(입력, 2, botelele_boleng, 2);
        else if (Taelo("java") || Taelo("javac")) {
            int 결과 = 실행관리.phethagatša_taelo(입력, 0, botelele_boleng);
            문자단말.Ngwala("Exit: "); 문자단말.수쓰기(결과); 문자단말.문자(10);
        }
        else if (Taelo("apps")) 실행관리.go_tsenya_tshedimošo_Lenaneo();
        else if (Taelo("net")) Netweke_kgoboko.boemo_boleng();
        else if (Taelo("run")) {
            int 결과 = 실행관리.phethagatša_taelo(입력, 3, botelele_boleng);
            문자단말.Ngwala("Exit: "); 문자단말.수쓰기(결과); 문자단말.Ngwala("\n");
        } else if (Taelo("info")) {
            문자단말.Ngwala("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (Taelo("mem")) {
            문자단말.Ngwala("위쪽 memori_boleng 공간(KiB): "); 문자단말.수쓰기(기억공간.위쪽기억크기());
            문자단말.Ngwala("\n배열 동적 memori_boleng 공간(paete_boleng): "); 문자단말.수쓰기(sedirišwa_boleng.arei_tirišo());
            문자단말.Ngwala(" / 262144\n작업 공간 karolo_boleng: "); 문자단말.수쓰기(기억공간.사용개수());
            문자단말.Ngwala(" / 8 (각 4096바이트)\n");
        } else if (Taelo("alloc")) {
            int lokela = 기억공간.aba_Bobolokelo();
            문자단말.Ngwala("karolo_boleng lokela: "); 문자단말.수쓰기(lokela); 문자단말.Ngwala("\n");
        } else if (Taelo("free")) {
            if (botelele_boleng == 6 && 입력[4] == ' ' && 입력[5] >= '0' && 입력[5] <= '7') {
                문자단말.Ngwala(기억공간.반환(입력[5] - '0') ? "반환됨\n" : "할당되지 않은 karolo_boleng\n");
            } else 문자단말.Ngwala("사용법: free 0..7\n");
        } else if (Taelo("echo")) {
            for (int lokela = 5; lokela < botelele_boleng; lokela++) 문자단말.문자(입력[lokela]);
            문자단말.문자(10);
        } else if (Taelo("clear")) 문자단말.지우기();
        else if (Taelo("test")) khenele.시험();
        else if (Taelo("halt")) {
            문자단말.Ngwala("HALTED\n");
            sedirišwa_boleng.정지();
        } else 문자단말.Ngwala("알 수 없는 명령입니다. help를 입력하세요.\n");
    }

    static void 받아쓰기(int boleng) {
        if (boleng == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = boleng == 13;
        if (boleng == 10 || boleng == 13) {
            문자단말.문자(10);
            if (memori_tshepedišo_ya_difaele.편집중) memori_tshepedišo_ya_difaele.편집줄(입력, botelele_boleng, mothaladi_mongwaloutama);
            else tiragalo_boleng_go_tsenya_tshedimošo();
            botelele_boleng = 0;
            mothaladi_mongwaloutama = false;
            문자단말.Ngwala(memori_tshepedišo_ya_difaele.편집중 ? "...> " : "jkoros> ");
        } else if (boleng == 8 || boleng == 127) {
            if (botelele_boleng > 0) {
                botelele_boleng--;
                문자단말.직렬바이트(8); 문자단말.직렬바이트(32); 문자단말.직렬바이트(8);
                문자단말.화면문자(8);
            }
        } else if (boleng >= 32 && boleng < 127 && botelele_boleng < 입력.length) {
            입력[botelele_boleng++] = boleng;
            문자단말.문자(boleng);
        } else if (boleng >= 32 && boleng < 127) mothaladi_mongwaloutama = true;
    }

    static void Diriša() {
        bontšha_thušo();
        문자단말.Ngwala("READY\njkoros> ");
        while (true) {
            int boleng = 문자단말.직렬읽기();
            if (boleng < 0) boleng = khiipote.Bala();
            if (boleng >= 0) 받아쓰기(boleng);
            else { Netweke_kgoboko.kgonthiša(); sedirišwa_boleng.잠시양보(); }
        }
    }
}
