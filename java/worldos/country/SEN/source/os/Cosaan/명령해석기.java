// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 biir 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] 입력 = new int[128];
    static int diir_xëyma = 0;
    static boolean 앞줄복귀 = false;
    static boolean buum_luëppe = false;

    static boolean ndigel(String tur_253d1510) {
        if (diir_xëyma < tur_253d1510.length()) return false;
        for (int àlluwa_tur = 0; àlluwa_tur < tur_253d1510.length(); àlluwa_tur++)
            if (입력[àlluwa_tur] != tur_253d1510.charAt(àlluwa_tur)) return false;
        return diir_xëyma == tur_253d1510.length() || 입력[tur_253d1510.length()] == ' ';
    }

    static void féeñal_ndimbal() {
        문자단말.biir("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        문자단말.biir("apps | run NAME [ARGS] | net\n");
        문자단말.biir("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        문자단말.biir("sync (연결된 JKSTORE1 Store_xëyma 장치에 bara_denc 보존)\n");
    }

    static void yokkute_xëyma_dugal_xabaar() {
        if (diir_xëyma == 0) return;
        if (ndigel("help")) féeñal_ndimbal();
        else if (ndigel("sync")) {
            int 결과 = 파일보존.lëkkale();
            문자단말.biir("Sync: "); 문자단말.수쓰기(결과); 문자단말.문자(10);
        }
        else if (ndigel("ls")) fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.dugal_xabaar_lim();
        else if (ndigel("edit")) fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.ndigel(입력, 4, diir_xëyma, 0);
        else if (ndigel("cat")) fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.ndigel(입력, 3, diir_xëyma, 1);
        else if (ndigel("rm")) fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.ndigel(입력, 2, diir_xëyma, 2);
        else if (ndigel("java") || ndigel("javac")) {
            int 결과 = 실행관리.def_ndigel(입력, 0, diir_xëyma);
            문자단말.biir("Exit: "); 문자단말.수쓰기(결과); 문자단말.문자(10);
        }
        else if (ndigel("apps")) 실행관리.dugal_xabaar_lim();
        else if (ndigel("net")) mbaal_Tegalo.nekkin_xëyma();
        else if (ndigel("run")) {
            int 결과 = 실행관리.def_ndigel(입력, 3, diir_xëyma);
            문자단말.biir("Exit: "); 문자단말.수쓰기(결과); 문자단말.biir("\n");
        } else if (ndigel("info")) {
            문자단말.biir("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (ndigel("mem")) {
            문자단말.biir("위쪽 fatlekookaay_xëyma 공간(KiB): "); 문자단말.수쓰기(기억공간.위쪽기억크기());
            문자단말.biir("\n배열 동적 fatlekookaay_xëyma 공간(okte_xëyma): "); 문자단말.수쓰기(toftal_xëyma.배열사용량());
            문자단말.biir(" / 262144\n작업 공간 dog_xëyma: "); 문자단말.수쓰기(기억공간.사용개수());
            문자단말.biir(" / 8 (각 4096바이트)\n");
        } else if (ndigel("alloc")) {
            int àlluwa_tur = 기억공간.jagleel_Dencukaay();
            문자단말.biir("dog_xëyma àlluwa_tur: "); 문자단말.수쓰기(àlluwa_tur); 문자단말.biir("\n");
        } else if (ndigel("free")) {
            if (diir_xëyma == 6 && 입력[4] == ' ' && 입력[5] >= '0' && 입력[5] <= '7') {
                문자단말.biir(기억공간.반환(입력[5] - '0') ? "반환됨\n" : "할당되지 않은 dog_xëyma\n");
            } else 문자단말.biir("사용법: free 0..7\n");
        } else if (ndigel("echo")) {
            for (int àlluwa_tur = 5; àlluwa_tur < diir_xëyma; àlluwa_tur++) 문자단말.문자(입력[àlluwa_tur]);
            문자단말.문자(10);
        } else if (ndigel("clear")) 문자단말.지우기();
        else if (ndigel("test")) xoox.시험();
        else if (ndigel("halt")) {
            문자단말.biir("HALTED\n");
            toftal_xëyma.정지();
        } else 문자단말.biir("알 수 없는 명령입니다. help를 입력하세요.\n");
    }

    static void 받아쓰기(int xëyma) {
        if (xëyma == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = xëyma == 13;
        if (xëyma == 10 || xëyma == 13) {
            문자단말.문자(10);
            if (fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.편집중) fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.편집줄(입력, diir_xëyma, buum_luëppe);
            else yokkute_xëyma_dugal_xabaar();
            diir_xëyma = 0;
            buum_luëppe = false;
            문자단말.biir(fatlekookaay_barabu_boolebdenc_yu_ñu_bennal.편집중 ? "...> " : "jkoros> ");
        } else if (xëyma == 8 || xëyma == 127) {
            if (diir_xëyma > 0) {
                diir_xëyma--;
                문자단말.직렬바이트(8); 문자단말.직렬바이트(32); 문자단말.직렬바이트(8);
                문자단말.화면문자(8);
            }
        } else if (xëyma >= 32 && xëyma < 127 && diir_xëyma < 입력.length) {
            입력[diir_xëyma++] = xëyma;
            문자단말.문자(xëyma);
        } else if (xëyma >= 32 && xëyma < 127) buum_luëppe = true;
    }

    static void daw() {
        féeñal_ndimbal();
        문자단말.biir("READY\njkoros> ");
        while (true) {
            int xëyma = 문자단말.직렬읽기();
            if (xëyma < 0) xëyma = arafukaay.읽기();
            if (xëyma >= 0) 받아쓰기(xëyma);
            else { mbaal_Tegalo.luñutu(); toftal_xëyma.잠시양보(); }
        }
    }
}
