// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 Írás 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] bevitel_ÉRTÉK = new int[128];
    static int hossz_ÉRTÉK = 0;
    static boolean 앞줄복귀 = false;
    static boolean sor_túlfolyás = false;

    static boolean Parancs(String Név) {
        if (hossz_ÉRTÉK < Név.length()) return false;
        for (int INDEX = 0; INDEX < Név.length(); INDEX++)
            if (bevitel_ÉRTÉK[INDEX] != Név.charAt(INDEX)) return false;
        return hossz_ÉRTÉK == Név.length() || bevitel_ÉRTÉK[Név.length()] == ' ';
    }

    static void bemutató_súgó() {
        SMS_Terminál.Írás("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        SMS_Terminál.Írás("apps | run NAME [ARGS] | net\n");
        SMS_Terminál.Írás("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        SMS_Terminál.Írás("sync (연결된 JKSTORE1 tár_ÉRTÉK 장치에 Fájl 보존)\n");
    }

    static void folyamat_ÉRTÉK_bejegyzés() {
        if (hossz_ÉRTÉK == 0) return;
        if (Parancs("help")) bemutató_súgó();
        else if (Parancs("sync")) {
            int KR = 파일보존.szinkronizál();
            SMS_Terminál.Írás("Sync: "); SMS_Terminál.ír_szám(KR); SMS_Terminál.문자(10);
        }
        else if (Parancs("ls")) Memória_fájlrendszer.bejegyzés_Lista();
        else if (Parancs("edit")) Memória_fájlrendszer.Parancs(bevitel_ÉRTÉK, 4, hossz_ÉRTÉK, 0);
        else if (Parancs("cat")) Memória_fájlrendszer.Parancs(bevitel_ÉRTÉK, 3, hossz_ÉRTÉK, 1);
        else if (Parancs("rm")) Memória_fájlrendszer.Parancs(bevitel_ÉRTÉK, 2, hossz_ÉRTÉK, 2);
        else if (Parancs("java") || Parancs("javac")) {
            int KR = végrehajtás_kezelő.végrehajt_parancs(bevitel_ÉRTÉK, 0, hossz_ÉRTÉK);
            SMS_Terminál.Írás("Exit: "); SMS_Terminál.ír_szám(KR); SMS_Terminál.문자(10);
        }
        else if (Parancs("apps")) végrehajtás_kezelő.bejegyzés_Lista();
        else if (Parancs("net")) hálózat_Sor.Állapot_ÉRTÉK();
        else if (Parancs("run")) {
            int KR = végrehajtás_kezelő.végrehajt_parancs(bevitel_ÉRTÉK, 3, hossz_ÉRTÉK);
            SMS_Terminál.Írás("Exit: "); SMS_Terminál.ír_szám(KR); SMS_Terminál.Írás("\n");
        } else if (Parancs("info")) {
            SMS_Terminál.Írás("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (Parancs("mem")) {
            SMS_Terminál.Írás("위쪽 Memória_ÉRTÉK CÍM_régió(KiB): "); SMS_Terminál.ír_szám(Memória_régió.NAGYBETŰS_Memória_méretez());
            SMS_Terminál.Írás("\n배열 동적 Memória_ÉRTÉK CÍM_régió(bájt_ÉRTÉK): "); SMS_Terminál.ír_szám(mobil_ÉRTÉK.TÖMB_felhasználás());
            SMS_Terminál.Írás(" / 262144\n작업 CÍM_régió szakasz_ÉRTÉK: "); SMS_Terminál.ír_szám(Memória_régió.사용개수());
            SMS_Terminál.Írás(" / 8 (각 4096바이트)\n");
        } else if (Parancs("alloc")) {
            int INDEX = Memória_régió.kioszt_tár();
            SMS_Terminál.Írás("szakasz_ÉRTÉK INDEX: "); SMS_Terminál.ír_szám(INDEX); SMS_Terminál.Írás("\n");
        } else if (Parancs("free")) {
            if (hossz_ÉRTÉK == 6 && bevitel_ÉRTÉK[4] == ' ' && bevitel_ÉRTÉK[5] >= '0' && bevitel_ÉRTÉK[5] <= '7') {
                SMS_Terminál.Írás(Memória_régió.visszaküld_KR(bevitel_ÉRTÉK[5] - '0') ? "반환됨\n" : "할당되지 않은 szakasz_ÉRTÉK\n");
            } else SMS_Terminál.Írás("사용법: free 0..7\n");
        } else if (Parancs("echo")) {
            for (int INDEX = 5; INDEX < hossz_ÉRTÉK; INDEX++) SMS_Terminál.문자(bevitel_ÉRTÉK[INDEX]);
            SMS_Terminál.문자(10);
        } else if (Parancs("clear")) SMS_Terminál.töröl_bejegyzés();
        else if (Parancs("test")) kernel.시험();
        else if (Parancs("halt")) {
            SMS_Terminál.Írás("HALTED\n");
            mobil_ÉRTÉK.정지();
        } else SMS_Terminál.Írás("알 szám 없는 명령입니다. help를 입력하세요.\n");
    }

    static void elfogad_ÉS_ír(int ÉRTÉK) {
        if (ÉRTÉK == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = ÉRTÉK == 13;
        if (ÉRTÉK == 10 || ÉRTÉK == 13) {
            SMS_Terminál.문자(10);
            if (Memória_fájlrendszer.편집중) Memória_fájlrendszer.Szerkesztett_sor(bevitel_ÉRTÉK, hossz_ÉRTÉK, sor_túlfolyás);
            else folyamat_ÉRTÉK_bejegyzés();
            hossz_ÉRTÉK = 0;
            sor_túlfolyás = false;
            SMS_Terminál.Írás(Memória_fájlrendszer.편집중 ? "...> " : "jkoros> ");
        } else if (ÉRTÉK == 8 || ÉRTÉK == 127) {
            if (hossz_ÉRTÉK > 0) {
                hossz_ÉRTÉK--;
                SMS_Terminál.직렬바이트(8); SMS_Terminál.직렬바이트(32); SMS_Terminál.직렬바이트(8);
                SMS_Terminál.화면문자(8);
            }
        } else if (ÉRTÉK >= 32 && ÉRTÉK < 127 && hossz_ÉRTÉK < bevitel_ÉRTÉK.length) {
            bevitel_ÉRTÉK[hossz_ÉRTÉK++] = ÉRTÉK;
            SMS_Terminál.문자(ÉRTÉK);
        } else if (ÉRTÉK >= 32 && ÉRTÉK < 127) sor_túlfolyás = true;
    }

    static void Futtatás() {
        bemutató_súgó();
        SMS_Terminál.Írás("READY\njkoros> ");
        while (true) {
            int ÉRTÉK = SMS_Terminál.직렬읽기();
            if (ÉRTÉK < 0) ÉRTÉK = billentyűzet.Olvasás();
            if (ÉRTÉK >= 0) elfogad_ÉS_ír(ÉRTÉK);
            else { hálózat_Sor.igazol(); mobil_ÉRTÉK.잠시양보(); }
        }
    }
}
