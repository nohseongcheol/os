// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 Yi_Rubutu 없이 동작하는 작은 직렬/PS2 명령해석기. */
public final class 명령해석기 {
    static int[] 입력 = new int[128];
    static int Tsawo_Daraja = 0;
    static boolean 앞줄복귀 = false;
    static boolean Layi_Mamayar_bayanai = false;

    static boolean Umarni(String Suna) {
        if (Tsawo_Daraja < Suna.length()) return false;
        for (int Indes = 0; Indes < Suna.length(); Indes++)
            if (입력[Indes] != Suna.charAt(Indes)) return false;
        return Tsawo_Daraja == Suna.length() || 입력[Suna.length()] == ' ';
    }

    static void Nuna_Taimako() {
        문자단말.Yi_Rubutu("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        문자단말.Yi_Rubutu("apps | run NAME [ARGS] | net\n");
        문자단말.Yi_Rubutu("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        문자단말.Yi_Rubutu("sync (연결된 JKSTORE1 Ajiye_Daraja 장치에 Fayil 보존)\n");
    }

    static void haryar_aikin_na_ura_Daraja_Mashigar_bayanai() {
        if (Tsawo_Daraja == 0) return;
        if (Umarni("help")) Nuna_Taimako();
        else if (Umarni("sync")) {
            int 결과 = 파일보존.daidaita();
            문자단말.Yi_Rubutu("Sync: "); 문자단말.수쓰기(결과); 문자단말.문자(10);
        }
        else if (Umarni("ls")) Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.Mashigar_bayanai_Jeri();
        else if (Umarni("edit")) Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.Umarni(입력, 4, Tsawo_Daraja, 0);
        else if (Umarni("cat")) Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.Umarni(입력, 3, Tsawo_Daraja, 1);
        else if (Umarni("rm")) Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.Umarni(입력, 2, Tsawo_Daraja, 2);
        else if (Umarni("java") || Umarni("javac")) {
            int 결과 = 실행관리.gudanar_Umarni(입력, 0, Tsawo_Daraja);
            문자단말.Yi_Rubutu("Exit: "); 문자단말.수쓰기(결과); 문자단말.문자(10);
        }
        else if (Umarni("apps")) 실행관리.Mashigar_bayanai_Jeri();
        else if (Umarni("net")) Hanyar_sadarwa_tara.Matsayi_Daraja();
        else if (Umarni("run")) {
            int 결과 = 실행관리.gudanar_Umarni(입력, 3, Tsawo_Daraja);
            문자단말.Yi_Rubutu("Exit: "); 문자단말.수쓰기(결과); 문자단말.Yi_Rubutu("\n");
        } else if (Umarni("info")) {
            문자단말.Yi_Rubutu("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (Umarni("mem")) {
            문자단말.Yi_Rubutu("위쪽 Mahardatar_kwamfuta_Daraja 공간(KiB): "); 문자단말.수쓰기(기억공간.위쪽기억크기());
            문자단말.Yi_Rubutu("\n배열 동적 Mahardatar_kwamfuta_Daraja 공간(bayit_Daraja): "); 문자단말.수쓰기(na_ura_Daraja.TSARI_amfani());
            문자단말.Yi_Rubutu(" / 262144\n작업 공간 Sashi_Daraja: "); 문자단말.수쓰기(기억공간.사용개수());
            문자단말.Yi_Rubutu(" / 8 (각 4096바이트)\n");
        } else if (Umarni("alloc")) {
            int Indes = 기억공간.kasafta_Wurin_adana();
            문자단말.Yi_Rubutu("Sashi_Daraja Indes: "); 문자단말.수쓰기(Indes); 문자단말.Yi_Rubutu("\n");
        } else if (Umarni("free")) {
            if (Tsawo_Daraja == 6 && 입력[4] == ' ' && 입력[5] >= '0' && 입력[5] <= '7') {
                문자단말.Yi_Rubutu(기억공간.반환(입력[5] - '0') ? "반환됨\n" : "할당되지 않은 Sashi_Daraja\n");
            } else 문자단말.Yi_Rubutu("사용법: free 0..7\n");
        } else if (Umarni("echo")) {
            for (int Indes = 5; Indes < Tsawo_Daraja; Indes++) 문자단말.문자(입력[Indes]);
            문자단말.문자(10);
        } else if (Umarni("clear")) 문자단말.share_Mashigar_bayanai();
        else if (Umarni("test")) Kwara.시험();
        else if (Umarni("halt")) {
            문자단말.Yi_Rubutu("HALTED\n");
            na_ura_Daraja.정지();
        } else 문자단말.Yi_Rubutu("알 수 없는 명령입니다. help를 입력하세요.\n");
    }

    static void 받아쓰기(int Daraja) {
        if (Daraja == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = Daraja == 13;
        if (Daraja == 10 || Daraja == 13) {
            문자단말.문자(10);
            if (Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.편집중) Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.편집줄(입력, Tsawo_Daraja, Layi_Mamayar_bayanai);
            else haryar_aikin_na_ura_Daraja_Mashigar_bayanai();
            Tsawo_Daraja = 0;
            Layi_Mamayar_bayanai = false;
            문자단말.Yi_Rubutu(Mahardatar_kwamfuta_tsarin_fayil_a_kwamfuta.편집중 ? "...> " : "jkoros> ");
        } else if (Daraja == 8 || Daraja == 127) {
            if (Tsawo_Daraja > 0) {
                Tsawo_Daraja--;
                문자단말.직렬바이트(8); 문자단말.직렬바이트(32); 문자단말.직렬바이트(8);
                문자단말.화면문자(8);
            }
        } else if (Daraja >= 32 && Daraja < 127 && Tsawo_Daraja < 입력.length) {
            입력[Tsawo_Daraja++] = Daraja;
            문자단말.문자(Daraja);
        } else if (Daraja >= 32 && Daraja < 127) Layi_Mamayar_bayanai = true;
    }

    static void Tafiyar_da() {
        Nuna_Taimako();
        문자단말.Yi_Rubutu("READY\njkoros> ");
        while (true) {
            int Daraja = 문자단말.직렬읽기();
            if (Daraja < 0) Daraja = kibod.Yi_Karatu();
            if (Daraja >= 0) 받아쓰기(Daraja);
            else { Hanyar_sadarwa_tara.Tabbatar_da(); na_ura_Daraja.잠시양보(); }
        }
    }
}
