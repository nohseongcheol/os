// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 Bhala 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] 입력 = new int[128];
    static int ubude_inani = 0;
    static boolean 앞줄복귀 = false;
    static boolean umugqa_ukukapaka = false;

    static boolean Umlayelo(String Igama) {
        if (ubude_inani < Igama.length()) return false;
        for (int thola_inkomba = 0; thola_inkomba < Igama.length(); thola_inkomba++)
            if (입력[thola_inkomba] != Igama.charAt(thola_inkomba)) return false;
        return ubude_inani == Igama.length() || 입력[Igama.length()] == ' ';
    }

    static void khombisa_usizo() {
        문자단말.Bhala("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        문자단말.Bhala("apps | run NAME [ARGS] | net\n");
        문자단말.Bhala("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        문자단말.Bhala("sync (연결된 JKSTORE1 Store_inani 장치에 Ihele 보존)\n");
    }

    static void Inqubo_inani_okufakwayo() {
        if (ubude_inani == 0) return;
        if (Umlayelo("help")) khombisa_usizo();
        else if (Umlayelo("sync")) {
            int 결과 = 파일보존.i_sync();
            문자단말.Bhala("Sync: "); 문자단말.수쓰기(결과); 문자단말.문자(10);
        }
        else if (Umlayelo("ls")) inkumbulo_isistimu_yefayela.okufakwayo_Uhlu();
        else if (Umlayelo("edit")) inkumbulo_isistimu_yefayela.Umlayelo(입력, 4, ubude_inani, 0);
        else if (Umlayelo("cat")) inkumbulo_isistimu_yefayela.Umlayelo(입력, 3, ubude_inani, 1);
        else if (Umlayelo("rm")) inkumbulo_isistimu_yefayela.Umlayelo(입력, 2, ubude_inani, 2);
        else if (Umlayelo("java") || Umlayelo("javac")) {
            int 결과 = 실행관리.yenza_umyalo(입력, 0, ubude_inani);
            문자단말.Bhala("Exit: "); 문자단말.수쓰기(결과); 문자단말.문자(10);
        }
        else if (Umlayelo("apps")) 실행관리.okufakwayo_Uhlu();
        else if (Umlayelo("net")) iNethiwekhi_Isitaki.isimo_inani();
        else if (Umlayelo("run")) {
            int 결과 = 실행관리.yenza_umyalo(입력, 3, ubude_inani);
            문자단말.Bhala("Exit: "); 문자단말.수쓰기(결과); 문자단말.Bhala("\n");
        } else if (Umlayelo("info")) {
            문자단말.Bhala("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (Umlayelo("mem")) {
            문자단말.Bhala("위쪽 inkumbulo_inani 공간(KiB): "); 문자단말.수쓰기(기억공간.위쪽기억크기());
            문자단말.Bhala("\n배열 동적 inkumbulo_inani 공간(ibhayithi_inani): "); 문자단말.수쓰기(idivayisi_inani.AMALUNGU_AFANAYO_sebenzisa());
            문자단말.Bhala(" / 262144\n작업 공간 isigaba_inani: "); 문자단말.수쓰기(기억공간.사용개수());
            문자단말.Bhala(" / 8 (각 4096바이트)\n");
        } else if (Umlayelo("alloc")) {
            int thola_inkomba = 기억공간.abela_Indawo_yokugcina();
            문자단말.Bhala("isigaba_inani thola_inkomba: "); 문자단말.수쓰기(thola_inkomba); 문자단말.Bhala("\n");
        } else if (Umlayelo("free")) {
            if (ubude_inani == 6 && 입력[4] == ' ' && 입력[5] >= '0' && 입력[5] <= '7') {
                문자단말.Bhala(기억공간.반환(입력[5] - '0') ? "반환됨\n" : "할당되지 않은 isigaba_inani\n");
            } else 문자단말.Bhala("사용법: free 0..7\n");
        } else if (Umlayelo("echo")) {
            for (int thola_inkomba = 5; thola_inkomba < ubude_inani; thola_inkomba++) 문자단말.문자(입력[thola_inkomba]);
            문자단말.문자(10);
        } else if (Umlayelo("clear")) 문자단말.지우기();
        else if (Umlayelo("test")) ikhenela.시험();
        else if (Umlayelo("halt")) {
            문자단말.Bhala("HALTED\n");
            idivayisi_inani.정지();
        } else 문자단말.Bhala("알 수 없는 명령입니다. help를 입력하세요.\n");
    }

    static void 받아쓰기(int inani) {
        if (inani == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = inani == 13;
        if (inani == 10 || inani == 13) {
            문자단말.문자(10);
            if (inkumbulo_isistimu_yefayela.편집중) inkumbulo_isistimu_yefayela.편집줄(입력, ubude_inani, umugqa_ukukapaka);
            else Inqubo_inani_okufakwayo();
            ubude_inani = 0;
            umugqa_ukukapaka = false;
            문자단말.Bhala(inkumbulo_isistimu_yefayela.편집중 ? "...> " : "jkoros> ");
        } else if (inani == 8 || inani == 127) {
            if (ubude_inani > 0) {
                ubude_inani--;
                문자단말.직렬바이트(8); 문자단말.직렬바이트(32); 문자단말.직렬바이트(8);
                문자단말.화면문자(8);
            }
        } else if (inani >= 32 && inani < 127 && ubude_inani < 입력.length) {
            입력[ubude_inani++] = inani;
            문자단말.문자(inani);
        } else if (inani >= 32 && inani < 127) umugqa_ukukapaka = true;
    }

    static void Sebenzisa() {
        khombisa_usizo();
        문자단말.Bhala("READY\njkoros> ");
        while (true) {
            int inani = 문자단말.직렬읽기();
            if (inani < 0) inani = ikhibhodi.Funda();
            if (inani >= 0) 받아쓰기(inani);
            else { iNethiwekhi_Isitaki.qiniseka(); idivayisi_inani.잠시양보(); }
        }
    }
}
