// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 Ýaz 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] 입력 = new int[128];
    static int dowamlylyk_baha = 0;
    static boolean 앞줄복귀 = false;
    static boolean setir_gyrmalanma = false;

    static boolean buýruk(String Ad) {
        if (dowamlylyk_baha < Ad.length()) return false;
        for (int indeks = 0; indeks < Ad.length(); indeks++)
            if (입력[indeks] != Ad.charAt(indeks)) return false;
        return dowamlylyk_baha == Ad.length() || 입력[Ad.length()] == ' ';
    }

    static void görkez_kömek() {
        문자단말.Ýaz("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        문자단말.Ýaz("apps | run NAME [ARGS] | net\n");
        문자단말.Ýaz("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        문자단말.Ýaz("sync (연결된 JKSTORE1 Store_baha 장치에 Faýl 보존)\n");
    }

    static void Proses_baha_girizmeklik() {
        if (dowamlylyk_baha == 0) return;
        if (buýruk("help")) görkez_kömek();
        else if (buýruk("sync")) {
            int 결과 = 파일보존.sinhronlaşdyr();
            문자단말.Ýaz("Sync: "); 문자단말.수쓰기(결과); 문자단말.문자(10);
        }
        else if (buýruk("ls")) ýat_faýl_ulgamy.girizmeklik_Sanaw();
        else if (buýruk("edit")) ýat_faýl_ulgamy.buýruk(입력, 4, dowamlylyk_baha, 0);
        else if (buýruk("cat")) ýat_faýl_ulgamy.buýruk(입력, 3, dowamlylyk_baha, 1);
        else if (buýruk("rm")) ýat_faýl_ulgamy.buýruk(입력, 2, dowamlylyk_baha, 2);
        else if (buýruk("java") || buýruk("javac")) {
            int 결과 = 실행관리.ýerine_ýetir_buýruk(입력, 0, dowamlylyk_baha);
            문자단말.Ýaz("Exit: "); 문자단말.수쓰기(결과); 문자단말.문자(10);
        }
        else if (buýruk("apps")) 실행관리.girizmeklik_Sanaw();
        else if (buýruk("net")) Tor_Desse.ýagdaý_baha();
        else if (buýruk("run")) {
            int 결과 = 실행관리.ýerine_ýetir_buýruk(입력, 3, dowamlylyk_baha);
            문자단말.Ýaz("Exit: "); 문자단말.수쓰기(결과); 문자단말.Ýaz("\n");
        } else if (buýruk("info")) {
            문자단말.Ýaz("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (buýruk("mem")) {
            문자단말.Ýaz("위쪽 ýat_baha 공간(KiB): "); 문자단말.수쓰기(기억공간.위쪽기억크기());
            문자단말.Ýaz("\n배열 동적 ýat_baha 공간(baýt_baha): "); 문자단말.수쓰기(enjam_baha.ARRAY_ulanylyş());
            문자단말.Ýaz(" / 262144\n작업 공간 bölüm_baha_366e0bfa: "); 문자단말.수쓰기(기억공간.사용개수());
            문자단말.Ýaz(" / 8 (각 4096바이트)\n");
        } else if (buýruk("alloc")) {
            int indeks = 기억공간.bölüp_aýyr_Ammar();
            문자단말.Ýaz("bölüm_baha_366e0bfa indeks: "); 문자단말.수쓰기(indeks); 문자단말.Ýaz("\n");
        } else if (buýruk("free")) {
            if (dowamlylyk_baha == 6 && 입력[4] == ' ' && 입력[5] >= '0' && 입력[5] <= '7') {
                문자단말.Ýaz(기억공간.반환(입력[5] - '0') ? "반환됨\n" : "할당되지 않은 bölüm_baha_366e0bfa\n");
            } else 문자단말.Ýaz("사용법: free 0..7\n");
        } else if (buýruk("echo")) {
            for (int indeks = 5; indeks < dowamlylyk_baha; indeks++) 문자단말.문자(입력[indeks]);
            문자단말.문자(10);
        } else if (buýruk("clear")) 문자단말.지우기();
        else if (buýruk("test")) ýadro.시험();
        else if (buýruk("halt")) {
            문자단말.Ýaz("HALTED\n");
            enjam_baha.정지();
        } else 문자단말.Ýaz("알 수 없는 명령입니다. help를 입력하세요.\n");
    }

    static void 받아쓰기(int baha) {
        if (baha == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = baha == 13;
        if (baha == 10 || baha == 13) {
            문자단말.문자(10);
            if (ýat_faýl_ulgamy.편집중) ýat_faýl_ulgamy.편집줄(입력, dowamlylyk_baha, setir_gyrmalanma);
            else Proses_baha_girizmeklik();
            dowamlylyk_baha = 0;
            setir_gyrmalanma = false;
            문자단말.Ýaz(ýat_faýl_ulgamy.편집중 ? "...> " : "jkoros> ");
        } else if (baha == 8 || baha == 127) {
            if (dowamlylyk_baha > 0) {
                dowamlylyk_baha--;
                문자단말.직렬바이트(8); 문자단말.직렬바이트(32); 문자단말.직렬바이트(8);
                문자단말.화면문자(8);
            }
        } else if (baha >= 32 && baha < 127 && dowamlylyk_baha < 입력.length) {
            입력[dowamlylyk_baha++] = baha;
            문자단말.문자(baha);
        } else if (baha >= 32 && baha < 127) setir_gyrmalanma = true;
    }

    static void Bitir() {
        görkez_kömek();
        문자단말.Ýaz("READY\njkoros> ");
        while (true) {
            int baha = 문자단말.직렬읽기();
            if (baha < 0) baha = klawiatura.Oka();
            if (baha >= 0) 받아쓰기(baha);
            else { Tor_Desse.barla(); enjam_baha.잠시양보(); }
        }
    }
}
