// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 kwandika 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] 입력 = new int[128];
    static int uburebure_agaciro = 0;
    static boolean 앞줄복귀 = false;
    static boolean umurongo_umusago = false;

    static boolean Icyo_wifuza(String Izina) {
        if (uburebure_agaciro < Izina.length()) return false;
        for (int umugerekashakiro = 0; umugerekashakiro < Izina.length(); umugerekashakiro++)
            if (입력[umugerekashakiro] != Izina.charAt(umugerekashakiro)) return false;
        return uburebure_agaciro == Izina.length() || 입력[Izina.length()] == ' ';
    }

    static void kugaragaza_ifashayoboro() {
        문자단말.kwandika("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        문자단말.kwandika("apps | run NAME [ARGS] | net\n");
        문자단말.kwandika("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        문자단말.kwandika("sync (연결된 JKSTORE1 Store_agaciro 장치에 Idosiye 보존)\n");
    }

    static void Inzira_agaciro_icyinjizwa() {
        if (uburebure_agaciro == 0) return;
        if (Icyo_wifuza("help")) kugaragaza_ifashayoboro();
        else if (Icyo_wifuza("sync")) {
            int 결과 = 파일보존.guhuza();
            문자단말.kwandika("Sync: "); 문자단말.수쓰기(결과); 문자단말.문자(10);
        }
        else if (Icyo_wifuza("ls")) ububiko_sisitemu_ya_dosiye.icyinjizwa_Urutonde();
        else if (Icyo_wifuza("edit")) ububiko_sisitemu_ya_dosiye.Icyo_wifuza(입력, 4, uburebure_agaciro, 0);
        else if (Icyo_wifuza("cat")) ububiko_sisitemu_ya_dosiye.Icyo_wifuza(입력, 3, uburebure_agaciro, 1);
        else if (Icyo_wifuza("rm")) ububiko_sisitemu_ya_dosiye.Icyo_wifuza(입력, 2, uburebure_agaciro, 2);
        else if (Icyo_wifuza("java") || Icyo_wifuza("javac")) {
            int 결과 = 실행관리.gukora_ibwiriza(입력, 0, uburebure_agaciro);
            문자단말.kwandika("Exit: "); 문자단말.수쓰기(결과); 문자단말.문자(10);
        }
        else if (Icyo_wifuza("apps")) 실행관리.icyinjizwa_Urutonde();
        else if (Icyo_wifuza("net")) Urusobemiyoboro_Ikirundo.imimerere_agaciro();
        else if (Icyo_wifuza("run")) {
            int 결과 = 실행관리.gukora_ibwiriza(입력, 3, uburebure_agaciro);
            문자단말.kwandika("Exit: "); 문자단말.수쓰기(결과); 문자단말.kwandika("\n");
        } else if (Icyo_wifuza("info")) {
            문자단말.kwandika("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (Icyo_wifuza("mem")) {
            문자단말.kwandika("위쪽 ububiko_agaciro 공간(KiB): "); 문자단말.수쓰기(기억공간.위쪽기억크기());
            문자단말.kwandika("\n배열 동적 ububiko_agaciro 공간(bayiti_agaciro): "); 문자단말.수쓰기(igendanwa_agaciro.배열사용량());
            문자단말.kwandika(" / 262144\n작업 공간 igice_agaciro: "); 문자단말.수쓰기(기억공간.사용개수());
            문자단말.kwandika(" / 8 (각 4096바이트)\n");
        } else if (Icyo_wifuza("alloc")) {
            int umugerekashakiro = 기억공간.kugenera_Ububiko();
            문자단말.kwandika("igice_agaciro umugerekashakiro: "); 문자단말.수쓰기(umugerekashakiro); 문자단말.kwandika("\n");
        } else if (Icyo_wifuza("free")) {
            if (uburebure_agaciro == 6 && 입력[4] == ' ' && 입력[5] >= '0' && 입력[5] <= '7') {
                문자단말.kwandika(기억공간.반환(입력[5] - '0') ? "반환됨\n" : "할당되지 않은 igice_agaciro\n");
            } else 문자단말.kwandika("사용법: free 0..7\n");
        } else if (Icyo_wifuza("echo")) {
            for (int umugerekashakiro = 5; umugerekashakiro < uburebure_agaciro; umugerekashakiro++) 문자단말.문자(입력[umugerekashakiro]);
            문자단말.문자(10);
        } else if (Icyo_wifuza("clear")) 문자단말.지우기();
        else if (Icyo_wifuza("test")) intima.시험();
        else if (Icyo_wifuza("halt")) {
            문자단말.kwandika("HALTED\n");
            igendanwa_agaciro.정지();
        } else 문자단말.kwandika("알 수 없는 명령입니다. help를 입력하세요.\n");
    }

    static void 받아쓰기(int agaciro) {
        if (agaciro == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = agaciro == 13;
        if (agaciro == 10 || agaciro == 13) {
            문자단말.문자(10);
            if (ububiko_sisitemu_ya_dosiye.편집중) ububiko_sisitemu_ya_dosiye.편집줄(입력, uburebure_agaciro, umurongo_umusago);
            else Inzira_agaciro_icyinjizwa();
            uburebure_agaciro = 0;
            umurongo_umusago = false;
            문자단말.kwandika(ububiko_sisitemu_ya_dosiye.편집중 ? "...> " : "jkoros> ");
        } else if (agaciro == 8 || agaciro == 127) {
            if (uburebure_agaciro > 0) {
                uburebure_agaciro--;
                문자단말.직렬바이트(8); 문자단말.직렬바이트(32); 문자단말.직렬바이트(8);
                문자단말.화면문자(8);
            }
        } else if (agaciro >= 32 && agaciro < 127 && uburebure_agaciro < 입력.length) {
            입력[uburebure_agaciro++] = agaciro;
            문자단말.문자(agaciro);
        } else if (agaciro >= 32 && agaciro < 127) umurongo_umusago = true;
    }

    static void ihuriro() {
        kugaragaza_ifashayoboro();
        문자단말.kwandika("READY\njkoros> ");
        while (true) {
            int agaciro = 문자단말.직렬읽기();
            if (agaciro < 0) agaciro = mwandikisho.읽기();
            if (agaciro >= 0) 받아쓰기(agaciro);
            else { Urusobemiyoboro_Ikirundo.gusuzuma(); igendanwa_agaciro.잠시양보(); }
        }
    }
}
