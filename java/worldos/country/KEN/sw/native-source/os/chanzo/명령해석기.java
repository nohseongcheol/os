// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 andika 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] 입력 = new int[128];
    static int urefu_thamani = 0;
    static boolean 앞줄복귀 = false;
    static boolean laini_ziada = false;

    static boolean amri(String Jina) {
        if (urefu_thamani < Jina.length()) return false;
        for (int kielezo = 0; kielezo < Jina.length(); kielezo++)
            if (입력[kielezo] != Jina.charAt(kielezo)) return false;
        return urefu_thamani == Jina.length() || 입력[Jina.length()] == ' ';
    }

    static void onyesha_msaada() {
        문자단말.andika("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        문자단말.andika("apps | run NAME [ARGS] | net\n");
        문자단말.andika("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        문자단말.andika("sync (연결된 JKSTORE1 Store_thamani 장치에 faili 보존)\n");
    }

    static void Mchakato_thamani_ingizo() {
        if (urefu_thamani == 0) return;
        if (amri("help")) onyesha_msaada();
        else if (amri("sync")) {
            int 결과 = 파일보존.landanisha();
            문자단말.andika("Sync: "); 문자단말.수쓰기(결과); 문자단말.문자(10);
        }
        else if (amri("ls")) kumbukumbu_mfumo_ya_mafaili.ingizo_Orodha();
        else if (amri("edit")) kumbukumbu_mfumo_ya_mafaili.amri(입력, 4, urefu_thamani, 0);
        else if (amri("cat")) kumbukumbu_mfumo_ya_mafaili.amri(입력, 3, urefu_thamani, 1);
        else if (amri("rm")) kumbukumbu_mfumo_ya_mafaili.amri(입력, 2, urefu_thamani, 2);
        else if (amri("java") || amri("javac")) {
            int 결과 = 실행관리.tekeleza_amri(입력, 0, urefu_thamani);
            문자단말.andika("Exit: "); 문자단말.수쓰기(결과); 문자단말.문자(10);
        }
        else if (amri("apps")) 실행관리.ingizo_Orodha();
        else if (amri("net")) Mtandao_Mpororo.hali_thamani();
        else if (amri("run")) {
            int 결과 = 실행관리.tekeleza_amri(입력, 3, urefu_thamani);
            문자단말.andika("Exit: "); 문자단말.수쓰기(결과); 문자단말.andika("\n");
        } else if (amri("info")) {
            문자단말.andika("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (amri("mem")) {
            문자단말.andika("위쪽 kumbukumbu_thamani_603669bd 공간(KiB): "); 문자단말.수쓰기(기억공간.위쪽기억크기());
            문자단말.andika("\n배열 동적 kumbukumbu_thamani_603669bd 공간(baiti_thamani): "); 문자단말.수쓰기(kifaa_thamani.ARRAY_utumizi());
            문자단말.andika(" / 262144\n작업 공간 sehemu_thamani: "); 문자단말.수쓰기(기억공간.사용개수());
            문자단말.andika(" / 8 (각 4096바이트)\n");
        } else if (amri("alloc")) {
            int kielezo = 기억공간.tengea_Hifadhi();
            문자단말.andika("sehemu_thamani kielezo: "); 문자단말.수쓰기(kielezo); 문자단말.andika("\n");
        } else if (amri("free")) {
            if (urefu_thamani == 6 && 입력[4] == ' ' && 입력[5] >= '0' && 입력[5] <= '7') {
                문자단말.andika(기억공간.반환(입력[5] - '0') ? "반환됨\n" : "할당되지 않은 sehemu_thamani\n");
            } else 문자단말.andika("사용법: free 0..7\n");
        } else if (amri("echo")) {
            for (int kielezo = 5; kielezo < urefu_thamani; kielezo++) 문자단말.문자(입력[kielezo]);
            문자단말.문자(10);
        } else if (amri("clear")) 문자단말.futa_ingizo();
        else if (amri("test")) kiini.시험();
        else if (amri("halt")) {
            문자단말.andika("HALTED\n");
            kifaa_thamani.정지();
        } else 문자단말.andika("알 수 없는 명령입니다. help를 입력하세요.\n");
    }

    static void 받아쓰기(int thamani) {
        if (thamani == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = thamani == 13;
        if (thamani == 10 || thamani == 13) {
            문자단말.문자(10);
            if (kumbukumbu_mfumo_ya_mafaili.편집중) kumbukumbu_mfumo_ya_mafaili.편집줄(입력, urefu_thamani, laini_ziada);
            else Mchakato_thamani_ingizo();
            urefu_thamani = 0;
            laini_ziada = false;
            문자단말.andika(kumbukumbu_mfumo_ya_mafaili.편집중 ? "...> " : "jkoros> ");
        } else if (thamani == 8 || thamani == 127) {
            if (urefu_thamani > 0) {
                urefu_thamani--;
                문자단말.직렬바이트(8); 문자단말.직렬바이트(32); 문자단말.직렬바이트(8);
                문자단말.화면문자(8);
            }
        } else if (thamani >= 32 && thamani < 127 && urefu_thamani < 입력.length) {
            입력[urefu_thamani++] = thamani;
            문자단말.문자(thamani);
        } else if (thamani >= 32 && thamani < 127) laini_ziada = true;
    }

    static void endesha() {
        onyesha_msaada();
        문자단말.andika("READY\njkoros> ");
        while (true) {
            int thamani = 문자단말.직렬읽기();
            if (thamani < 0) thamani = kibodi.읽기();
            if (thamani >= 0) 받아쓰기(thamani);
            else { Mtandao_Mpororo.thibitisha(); kifaa_thamani.잠시양보(); }
        }
    }
}
