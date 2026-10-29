// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 Bhala 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] 입력 = new int[128];
    static int ubude_ixabiso = 0;
    static boolean 앞줄복귀 = false;
    static boolean umgca_ukuphuphuma = false;

    static boolean Umyalelo(String Igama) {
        if (ubude_ixabiso < Igama.length()) return false;
        for (int indeksa = 0; indeksa < Igama.length(); indeksa++)
            if (입력[indeksa] != Igama.charAt(indeksa)) return false;
        return ubude_ixabiso == Igama.length() || 입력[Igama.length()] == ' ';
    }

    static void bonisa_uncedo() {
        문자단말.Bhala("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        문자단말.Bhala("apps | run NAME [ARGS] | net\n");
        문자단말.Bhala("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        문자단말.Bhala("sync (연결된 JKSTORE1 Store_ixabiso 장치에 iFayili 보존)\n");
    }

    static void Inkqubo_ixabiso_ufako_nkcukacha() {
        if (ubude_ixabiso == 0) return;
        if (Umyalelo("help")) bonisa_uncedo();
        else if (Umyalelo("sync")) {
            int 결과 = 파일보존.ngqamanisa();
            문자단말.Bhala("Sync: "); 문자단말.수쓰기(결과); 문자단말.문자(10);
        }
        else if (Umyalelo("ls")) imemori_uhlobo_loseto_lwefayile.ufako_nkcukacha_uludwe();
        else if (Umyalelo("edit")) imemori_uhlobo_loseto_lwefayile.Umyalelo(입력, 4, ubude_ixabiso, 0);
        else if (Umyalelo("cat")) imemori_uhlobo_loseto_lwefayile.Umyalelo(입력, 3, ubude_ixabiso, 1);
        else if (Umyalelo("rm")) imemori_uhlobo_loseto_lwefayile.Umyalelo(입력, 2, ubude_ixabiso, 2);
        else if (Umyalelo("java") || Umyalelo("javac")) {
            int 결과 = 실행관리.ukwenza_umyalelo(입력, 0, ubude_ixabiso);
            문자단말.Bhala("Exit: "); 문자단말.수쓰기(결과); 문자단말.문자(10);
        }
        else if (Umyalelo("apps")) 실행관리.ufako_nkcukacha_uludwe();
        else if (Umyalelo("net")) Inethiwekhi_fumba.imo_ixabiso();
        else if (Umyalelo("run")) {
            int 결과 = 실행관리.ukwenza_umyalelo(입력, 3, ubude_ixabiso);
            문자단말.Bhala("Exit: "); 문자단말.수쓰기(결과); 문자단말.Bhala("\n");
        } else if (Umyalelo("info")) {
            문자단말.Bhala("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (Umyalelo("mem")) {
            문자단말.Bhala("위쪽 imemori_ixabiso 공간(KiB): "); 문자단말.수쓰기(기억공간.위쪽기억크기());
            문자단말.Bhala("\n배열 동적 imemori_ixabiso 공간(ibhayithi_ixabiso): "); 문자단말.수쓰기(isixhobo_ixabiso.ULUHLU_ukusetyenziswa());
            문자단말.Bhala(" / 262144\n작업 공간 icandelo_ixabiso: "); 문자단말.수쓰기(기억공간.사용개수());
            문자단말.Bhala(" / 8 (각 4096바이트)\n");
        } else if (Umyalelo("alloc")) {
            int indeksa = 기억공간.yabela_Ugcino();
            문자단말.Bhala("icandelo_ixabiso indeksa: "); 문자단말.수쓰기(indeksa); 문자단말.Bhala("\n");
        } else if (Umyalelo("free")) {
            if (ubude_ixabiso == 6 && 입력[4] == ' ' && 입력[5] >= '0' && 입력[5] <= '7') {
                문자단말.Bhala(기억공간.반환(입력[5] - '0') ? "반환됨\n" : "할당되지 않은 icandelo_ixabiso\n");
            } else 문자단말.Bhala("사용법: free 0..7\n");
        } else if (Umyalelo("echo")) {
            for (int indeksa = 5; indeksa < ubude_ixabiso; indeksa++) 문자단말.문자(입력[indeksa]);
            문자단말.문자(10);
        } else if (Umyalelo("clear")) 문자단말.지우기();
        else if (Umyalelo("test")) ikheneli.시험();
        else if (Umyalelo("halt")) {
            문자단말.Bhala("HALTED\n");
            isixhobo_ixabiso.정지();
        } else 문자단말.Bhala("알 수 없는 명령입니다. help를 입력하세요.\n");
    }

    static void 받아쓰기(int ixabiso) {
        if (ixabiso == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = ixabiso == 13;
        if (ixabiso == 10 || ixabiso == 13) {
            문자단말.문자(10);
            if (imemori_uhlobo_loseto_lwefayile.편집중) imemori_uhlobo_loseto_lwefayile.편집줄(입력, ubude_ixabiso, umgca_ukuphuphuma);
            else Inkqubo_ixabiso_ufako_nkcukacha();
            ubude_ixabiso = 0;
            umgca_ukuphuphuma = false;
            문자단말.Bhala(imemori_uhlobo_loseto_lwefayile.편집중 ? "...> " : "jkoros> ");
        } else if (ixabiso == 8 || ixabiso == 127) {
            if (ubude_ixabiso > 0) {
                ubude_ixabiso--;
                문자단말.직렬바이트(8); 문자단말.직렬바이트(32); 문자단말.직렬바이트(8);
                문자단말.화면문자(8);
            }
        } else if (ixabiso >= 32 && ixabiso < 127 && ubude_ixabiso < 입력.length) {
            입력[ubude_ixabiso++] = ixabiso;
            문자단말.문자(ixabiso);
        } else if (ixabiso >= 32 && ixabiso < 127) umgca_ukuphuphuma = true;
    }

    static void Phumeza() {
        bonisa_uncedo();
        문자단말.Bhala("READY\njkoros> ");
        while (true) {
            int ixabiso = 문자단말.직렬읽기();
            if (ixabiso < 0) ixabiso = ikhibhodi.Funda();
            if (ixabiso >= 0) 받아쓰기(ixabiso);
            else { Inethiwekhi_fumba.ngqinisisa(); isixhobo_ixabiso.잠시양보(); }
        }
    }
}
