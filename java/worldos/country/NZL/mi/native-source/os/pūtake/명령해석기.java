// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 Tuhia 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] 입력 = new int[128];
    static int roa_uara = 0;
    static boolean 앞줄복귀 = false;
    static boolean hononga_waipuke = false;

    static boolean tono(String Ingoa) {
        if (roa_uara < Ingoa.length()) return false;
        for (int INDEX = 0; INDEX < Ingoa.length(); INDEX++)
            if (입력[INDEX] != Ingoa.charAt(INDEX)) return false;
        return roa_uara == Ingoa.length() || 입력[Ingoa.length()] == ' ';
    }

    static void whakaatu_āwhina() {
        TEXT_Tauranga.Tuhia("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        TEXT_Tauranga.Tuhia("apps | run NAME [ARGS] | net\n");
        TEXT_Tauranga.Tuhia("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        TEXT_Tauranga.Tuhia("sync (연결된 JKSTORE1 Store_uara 장치에 Kōnae 보존)\n");
    }

    static void Hātepe_uara_tāurunga() {
        if (roa_uara == 0) return;
        if (tono("help")) whakaatu_āwhina();
        else if (tono("sync")) {
            int mēhua = 파일보존.tukutahi();
            TEXT_Tauranga.Tuhia("Sync: "); TEXT_Tauranga.수쓰기(mēhua); TEXT_Tauranga.문자(10);
        }
        else if (tono("ls")) Pūmahara_pūnaha_kōnae.tāurunga_Rārangi();
        else if (tono("edit")) Pūmahara_pūnaha_kōnae.tono(입력, 4, roa_uara, 0);
        else if (tono("cat")) Pūmahara_pūnaha_kōnae.tono(입력, 3, roa_uara, 1);
        else if (tono("rm")) Pūmahara_pūnaha_kōnae.tono(입력, 2, roa_uara, 2);
        else if (tono("java") || tono("javac")) {
            int mēhua = 실행관리.kawe_tono(입력, 0, roa_uara);
            TEXT_Tauranga.Tuhia("Exit: "); TEXT_Tauranga.수쓰기(mēhua); TEXT_Tauranga.문자(10);
        }
        else if (tono("apps")) 실행관리.tāurunga_Rārangi();
        else if (tono("net")) whatunga_Huinga.tūnga_uara();
        else if (tono("run")) {
            int mēhua = 실행관리.kawe_tono(입력, 3, roa_uara);
            TEXT_Tauranga.Tuhia("Exit: "); TEXT_Tauranga.수쓰기(mēhua); TEXT_Tauranga.Tuhia("\n");
        } else if (tono("info")) {
            TEXT_Tauranga.Tuhia("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (tono("mem")) {
            TEXT_Tauranga.Tuhia("위쪽 Pūmahara_uara 공간(KiB): "); TEXT_Tauranga.수쓰기(기억공간.UPPER_Pūmahara_rahi());
            TEXT_Tauranga.Tuhia("\n배열 동적 Pūmahara_uara 공간(paita_uara): "); TEXT_Tauranga.수쓰기(pūkoro_uara.HUĀNGA_paunga());
            TEXT_Tauranga.Tuhia(" / 262144\n작업 공간 wāhanga_uara: "); TEXT_Tauranga.수쓰기(기억공간.사용개수());
            TEXT_Tauranga.Tuhia(" / 8 (각 4096바이트)\n");
        } else if (tono("alloc")) {
            int INDEX = 기억공간.tiritiri_Rokiroki();
            TEXT_Tauranga.Tuhia("wāhanga_uara INDEX: "); TEXT_Tauranga.수쓰기(INDEX); TEXT_Tauranga.Tuhia("\n");
        } else if (tono("free")) {
            if (roa_uara == 6 && 입력[4] == ' ' && 입력[5] >= '0' && 입력[5] <= '7') {
                TEXT_Tauranga.Tuhia(기억공간.반환(입력[5] - '0') ? "반환됨\n" : "할당되지 않은 wāhanga_uara\n");
            } else TEXT_Tauranga.Tuhia("사용법: free 0..7\n");
        } else if (tono("echo")) {
            for (int INDEX = 5; INDEX < roa_uara; INDEX++) TEXT_Tauranga.문자(입력[INDEX]);
            TEXT_Tauranga.문자(10);
        } else if (tono("clear")) TEXT_Tauranga.지우기();
        else if (tono("test")) kākano.시험();
        else if (tono("halt")) {
            TEXT_Tauranga.Tuhia("HALTED\n");
            pūkoro_uara.정지();
        } else TEXT_Tauranga.Tuhia("알 수 없는 명령입니다. help를 입력하세요.\n");
    }

    static void whakaae_AND_tuhi(int uara) {
        if (uara == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = uara == 13;
        if (uara == 10 || uara == 13) {
            TEXT_Tauranga.문자(10);
            if (Pūmahara_pūnaha_kōnae.편집중) Pūmahara_pūnaha_kōnae.편집줄(입력, roa_uara, hononga_waipuke);
            else Hātepe_uara_tāurunga();
            roa_uara = 0;
            hononga_waipuke = false;
            TEXT_Tauranga.Tuhia(Pūmahara_pūnaha_kōnae.편집중 ? "...> " : "jkoros> ");
        } else if (uara == 8 || uara == 127) {
            if (roa_uara > 0) {
                roa_uara--;
                TEXT_Tauranga.직렬바이트(8); TEXT_Tauranga.직렬바이트(32); TEXT_Tauranga.직렬바이트(8);
                TEXT_Tauranga.화면문자(8);
            }
        } else if (uara >= 32 && uara < 127 && roa_uara < 입력.length) {
            입력[roa_uara++] = uara;
            TEXT_Tauranga.문자(uara);
        } else if (uara >= 32 && uara < 127) hononga_waipuke = true;
    }

    static void whakahaere() {
        whakaatu_āwhina();
        TEXT_Tauranga.Tuhia("READY\njkoros> ");
        while (true) {
            int uara = TEXT_Tauranga.직렬읽기();
            if (uara < 0) uara = papapātuhi.Pānuitia();
            if (uara >= 0) whakaae_AND_tuhi(uara);
            else { whatunga_Huinga.manatoko(); pūkoro_uara.잠시양보(); }
        }
    }
}
