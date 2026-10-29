// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 bajt_VALUE 경계를 지키는 삽입/삭제, 방향키, Komanda LOG_RECORD, Tab 완성. */
public final class linjë_Redaktori {
    static boolean rreshti_i_komandës;
    static int[] LOG_RECORD = new int[16 * 1024], LOG_gjatësi = new int[16], Store_VALUE = new int[4096], 후보 = new int[64];
    static int LOG_COUNT, LOG_RECORD_mbaroj, Kërkim_VALUE, 저장길이, Madhësi, kursor_VALUE, 후보수, 후보길이, nis_dritare;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd i_sigurt_pasues në_largësi_afishim run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String futje_Listë, int nis_pozicioni, int mbaroj_pozicioni, int 입력길이) {
        int bajt_COUNT=0;
        for(int pozicioni_INDEX=nis_pozicioni;pozicioni_INDEX<mbaroj_pozicioni;pozicioni_INDEX++) {
            int kodi_i_karakterit=futje_Listë.charAt(pozicioni_INDEX);
            if(kodi_i_karakterit>=0xd800 && kodi_i_karakterit<=0xdbff && pozicioni_INDEX+1<mbaroj_pozicioni)kodi_i_karakterit=0x10000+((kodi_i_karakterit-0xd800)<<10)+futje_Listë.charAt(++pozicioni_INDEX)-0xdc00;
            int 수=kodi_i_karakterit<128?1:kodi_i_karakterit<2048?2:kodi_i_karakterit<65536?3:4;
            if(bajt_COUNT+수>62)return;
            for(int SEQUENCE_VALUE=수-1;SEQUENCE_VALUE>=0;SEQUENCE_VALUE--)명령후보[bajt_COUNT++]=수==1?kodi_i_karakterit:SEQUENCE_VALUE==수-1?(수==2?0xc0:수==3?0xe0:0xf0)|(kodi_i_karakterit>>(6*SEQUENCE_VALUE)):0x80|((kodi_i_karakterit>>(6*SEQUENCE_VALUE))&63);
        }
        if(bajt_COUNT<입력길이)return;
        for(int pozicioni_INDEX=0;pozicioni_INDEX<입력길이;pozicioni_INDEX++)if(명령후보[pozicioni_INDEX]!=명령해석기.linjë[pozicioni_INDEX])return;
        후보수++;후보길이=bajt_COUNT+1;
        for(int pozicioni_INDEX=0;pozicioni_INDEX<bajt_COUNT;pozicioni_INDEX++)후보[pozicioni_INDEX]=명령후보[pozicioni_INDEX];후보[bajt_COUNT]=' ';
    }
    static int e_përparme_VALUE(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (명령해석기.linjë[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int PAS_VALUE(int 읽는자리) { if (읽는자리 < Madhësi) { 읽는자리++; while (읽는자리 < Madhësi && (명령해석기.linjë[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int nis_pozicioni, int vendmbërritje_VALUE_INDEX) {
        int 글칸수 = 0;
        for (int Loop_INDEX = nis_pozicioni; Loop_INDEX < vendmbërritje_VALUE_INDEX; Loop_INDEX++) { int bajt_të_dhëna = 명령해석기.linjë[Loop_INDEX]; if ((bajt_të_dhëna & 192) == 128) continue; 글칸수 += bajt_të_dhëna >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void 다시() {
        단말.Shkrimi("\r\u001b[2K");
        단말.Shkrimi(rreshti_i_komandës ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 linjë 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int COLUMNS = panel.Terminali(13) & 65535; return COLUMNS - (rreshti_i_komandës ? 18 : 9); }
    static void 보이는줄() {
        if (kursor_VALUE < nis_dritare) nis_dritare = kursor_VALUE;
        while (폭(nis_dritare, kursor_VALUE) > 보이는폭()) nis_dritare = PAS_VALUE(nis_dritare);
        int mbaroj_pozicioni = nis_dritare;
        while (mbaroj_pozicioni < Madhësi && 폭(nis_dritare, PAS_VALUE(mbaroj_pozicioni)) <= 보이는폭()) mbaroj_pozicioni = PAS_VALUE(mbaroj_pozicioni);
        단말.Shkrimi("\r\u001b["); 단말.수(rreshti_i_komandës ? 16 : 7); 단말.Shkrimi("G\u001b[K");
        if (nis_dritare > 0) 단말.문자('<');
        for (int Loop_INDEX = nis_dritare; Loop_INDEX < mbaroj_pozicioni; Loop_INDEX++) panel.직렬쓰기(명령해석기.linjë[Loop_INDEX]);
        단말.문자(mbaroj_pozicioni < Madhësi ? '>' : ' ');
        단말.Shkrimi("\u001b["); 단말.수(폭(kursor_VALUE, mbaroj_pozicioni) + 1); 단말.문자('D');
        가로보기 = nis_dritare > 0 || mbaroj_pozicioni < Madhësi || 폭(0, Madhësi) > 보이는폭();
    }
    static void 기록넣기() {
        if (!rreshti_i_komandës || Madhësi == 0 || Madhësi > 1024) return;
        if (LOG_COUNT > 0) {
            int 마지막자리 = (LOG_RECORD_mbaroj + 15) % 16; boolean 같은여부 = LOG_gjatësi[마지막자리] == Madhësi;
            for (int Loop_INDEX = 0; 같은여부 && Loop_INDEX < Madhësi; Loop_INDEX++) if (LOG_RECORD[마지막자리 * 1024 + Loop_INDEX] != 명령해석기.linjë[Loop_INDEX]) 같은여부 = false;
            if (같은여부) return;
        }
        LOG_gjatësi[LOG_RECORD_mbaroj] = Madhësi; for (int Loop_INDEX = 0; Loop_INDEX < Madhësi; Loop_INDEX++) LOG_RECORD[LOG_RECORD_mbaroj * 1024 + Loop_INDEX] = 명령해석기.linjë[Loop_INDEX];
        LOG_RECORD_mbaroj = (LOG_RECORD_mbaroj + 1) % 16; if (LOG_COUNT < 16) LOG_COUNT++;
    }
    static void 기록이동(int DELTA_VALUE) {
        if (!rreshti_i_komandës) return;
        if (Kërkim_VALUE == 0 && DELTA_VALUE > 0) { 저장길이 = Madhësi; for (int Loop_INDEX = 0; Loop_INDEX < Madhësi; Loop_INDEX++) Store_VALUE[Loop_INDEX] = 명령해석기.linjë[Loop_INDEX]; }
        int Tjetër_pozicioni = Kërkim_VALUE + DELTA_VALUE; if (Tjetër_pozicioni < 0 || Tjetër_pozicioni > LOG_COUNT) return; Kërkim_VALUE = Tjetër_pozicioni;
        if (Kërkim_VALUE == 0) { Madhësi = 저장길이; for (int Loop_INDEX = 0; Loop_INDEX < Madhësi; Loop_INDEX++) 명령해석기.linjë[Loop_INDEX] = Store_VALUE[Loop_INDEX]; }
        else { int 보관칸 = (LOG_RECORD_mbaroj + 16 - Kërkim_VALUE) % 16; Madhësi = LOG_gjatësi[보관칸]; for (int Loop_INDEX = 0; Loop_INDEX < Madhësi; Loop_INDEX++) 명령해석기.linjë[Loop_INDEX] = LOG_RECORD[보관칸 * 1024 + Loop_INDEX]; }
        kursor_VALUE = Madhësi; 다시();
    }
    static void shfaq_LOG() {
        for (int futje_COUNT = 0; futje_COUNT < LOG_COUNT; futje_COUNT++) {
            int 보관칸 = (LOG_RECORD_mbaroj + 16 - LOG_COUNT + futje_COUNT) % 16; 단말.수(futje_COUNT + 1); 단말.Shkrimi("  ");
            for (int Loop_INDEX = 0; Loop_INDEX < LOG_gjatësi[보관칸]; Loop_INDEX++) panel.직렬쓰기(LOG_RECORD[보관칸 * 1024 + Loop_INDEX]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] të_dhëna_ARRAY, int nis_pozicioni, int futje_COUNT, int 접두말, int 총수, boolean 폴더번호) {
        if (futje_COUNT < 총수 || futje_COUNT > 62) return;
        for (int Loop_INDEX = 0; Loop_INDEX < 총수; Loop_INDEX++) if (të_dhëna_ARRAY[nis_pozicioni + Loop_INDEX] != 명령해석기.linjë[접두말 + Loop_INDEX]) return;
        후보수++; 후보길이 = futje_COUNT + 1;
        for (int Loop_INDEX = 0; Loop_INDEX < futje_COUNT; Loop_INDEX++) 후보[Loop_INDEX] = të_dhëna_ARRAY[nis_pozicioni + Loop_INDEX]; 후보[futje_COUNT] = 폴더번호 ? '/' : ' ';
    }
    static void 완성() {
        if (!rreshti_i_komandës || kursor_VALUE != Madhësi) return;
        int 시작점 = Madhësi; while (시작점 > 0 && 명령해석기.linjë[시작점 - 1] != ' ') 시작점--;
        for (int Loop_INDEX = 시작점; Loop_INDEX < Madhësi; Loop_INDEX++) if (명령해석기.linjë[Loop_INDEX] == '/' || 명령해석기.linjë[Loop_INDEX] == '"' || 명령해석기.linjë[Loop_INDEX] == 39 || 명령해석기.linjë[Loop_INDEX] == '\\') return;
        후보수 = 0; int futje_COUNT = Madhësi - 시작점;
        if (시작점 == 0) {
            for(int Listë_INDEX=0;Listë_INDEX<2;Listë_INDEX++) {
                String futje_Listë=Listë_INDEX==0?명령들:관리명령.완성어();
                int 읽는자리=0;
                while(읽는자리<futje_Listë.length()) {
                    int mbaroj_pozicioni=읽는자리;while(mbaroj_pozicioni<futje_Listë.length() && futje_Listë.charAt(mbaroj_pozicioni)!=' ')mbaroj_pozicioni++;
                    명령후보넣기(futje_Listë,읽는자리,mbaroj_pozicioni,futje_COUNT);읽는자리=mbaroj_pozicioni+1;
                }
            }
        } else {
            Memorie_Skedarët.shteg_nis(1); Memorie_Skedarët.shteg_bajt(0, '.'); Memorie_Skedarët.normalizoj_VALUE();
            for (int Loop_INDEX = 0; Loop_INDEX < Memorie_Skedarët.skedar_COUNT; Loop_INDEX++) {
                int nis_pozicioni = Memorie_Skedarët.futje_nis(Memorie_Skedarët.Emër, Loop_INDEX * 64, Memorie_Skedarët.이름길이[Loop_INDEX]);
                if (nis_pozicioni >= 0) 후보넣기(Memorie_Skedarët.Emër, Loop_INDEX * 64 + nis_pozicioni, Memorie_Skedarët.이름길이[Loop_INDEX] - nis_pozicioni, 시작점, futje_COUNT, false);
            }
            for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
                int nis_pozicioni = Memorie_Skedarët.futje_nis(Memorie_Skedarët.direktori_emër, Loop_INDEX * 64, Memorie_Skedarët.direktori_gjatësi[Loop_INDEX]);
                if (nis_pozicioni >= 0) 후보넣기(Memorie_Skedarët.direktori_emër, Loop_INDEX * 64 + nis_pozicioni, Memorie_Skedarët.direktori_gjatësi[Loop_INDEX] - nis_pozicioni, 시작점, futje_COUNT, true);
            }
        }
        if (후보수 != 1) { panel.직렬쓰기(7); return; }
        for (int Loop_INDEX = futje_COUNT; Loop_INDEX < 후보길이 && Madhësi < 명령해석기.linjë.length - 1; Loop_INDEX++) {
            if (후보[Loop_INDEX] == ' ' && Loop_INDEX != 후보길이 - 1) 명령해석기.linjë[Madhësi++] = '\\';
            명령해석기.linjë[Madhësi++] = 후보[Loop_INDEX];
        }
        kursor_VALUE = Madhësi; 다시();
    }
    static int 탈출읽기() {
        int 시작점 = panel.밀리초();
        while (panel.밀리초() - 시작점 < 80) { int bajt_të_dhëna = panel.직렬읽기(); if (bajt_të_dhëna >= 0) return bajt_të_dhëna; panel.YIELD_CPU(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int futje_COUNT = 0, mbaroj_pozicioni = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 12; Loop_INDEX++) { int bajt_të_dhëna = 탈출읽기(); if (bajt_të_dhëna < 0) return; if (bajt_të_dhëna >= '0' && bajt_të_dhëna <= '9') futje_COUNT = futje_COUNT * 10 + bajt_të_dhëna - '0'; else { mbaroj_pozicioni = bajt_të_dhëna; break; } }
        if (mbaroj_pozicioni == 'A') 기록이동(1);
        else if (mbaroj_pozicioni == 'B') 기록이동(-1);
        else if (mbaroj_pozicioni == 'C') { kursor_VALUE = PAS_VALUE(kursor_VALUE); 다시(); }
        else if (mbaroj_pozicioni == 'D') { kursor_VALUE = e_përparme_VALUE(kursor_VALUE); 다시(); }
        else if (mbaroj_pozicioni == 'H' || mbaroj_pozicioni == '~' && (futje_COUNT == 1 || futje_COUNT == 7)) { kursor_VALUE = 0; 다시(); }
        else if (mbaroj_pozicioni == 'F' || mbaroj_pozicioni == '~' && (futje_COUNT == 4 || futje_COUNT == 8)) { kursor_VALUE = Madhësi; 다시(); }
        else if (mbaroj_pozicioni == '~' && futje_COUNT == 3 && kursor_VALUE < Madhësi) {
            int Tjetër_pozicioni = PAS_VALUE(kursor_VALUE); for (int Loop_INDEX = Tjetër_pozicioni; Loop_INDEX < Madhësi; Loop_INDEX++) 명령해석기.linjë[Loop_INDEX - Tjetër_pozicioni + kursor_VALUE] = 명령해석기.linjë[Loop_INDEX]; Madhësi -= Tjetër_pozicioni - kursor_VALUE; 다시();
        }
        else if (mbaroj_pozicioni == '~' && (futje_COUNT == 5 || futje_COUNT == 6)) panel.Terminali(futje_COUNT == 5 ? 5 : 6);
        else if (mbaroj_pozicioni == '~' && futje_COUNT == 24 && rreshti_i_komandës) { 명령해석기.Terminali(true); }
    }
    static int Leximi() {
        if (!dritare_sesion.이어읽기) { Madhësi = kursor_VALUE = Kërkim_VALUE = nis_dritare = 0; 가로보기 = false; }
        else { dritare_sesion.이어읽기 = false; 다시(); } boolean tejkalim = false;
        while (true) {
            int bajt_të_dhëna = panel.직렬읽기(); if (bajt_të_dhëna == -4096) return -3;
            if (panel.Terminali(14) != 0) 다시(); if (bajt_të_dhëna < 0) { panel.YIELD_CPU(); continue; }
            if (bajt_të_dhëna == 10 && 명령해석기.앞줄) { 명령해석기.앞줄 = false; continue; } 명령해석기.앞줄 = bajt_të_dhëna == 13;
            if (bajt_të_dhëna == 27) { 탈출(); continue; }
            if (bajt_të_dhëna == 3) { 단말.Shkrimi("^C\n"); return -1; }
            if (bajt_të_dhëna == 4 && Madhësi == 0 && rreshti_i_komandës) { if (panel.Terminali(2) != 0) 명령해석기.Terminali(true); return -1; }
            if (bajt_të_dhëna == 13 || bajt_të_dhëna == 10) { 단말.문자(10); if (!tejkalim) 기록넣기(); return tejkalim ? -2 : Madhësi; }
            if (bajt_të_dhëna == 9 && rreshti_i_komandës) { 완성(); continue; }
            if (bajt_të_dhëna == 1 || bajt_të_dhëna == 5) { kursor_VALUE = bajt_të_dhëna == 1 ? 0 : Madhësi; 다시(); continue; }
            if (bajt_të_dhëna == 8 || bajt_të_dhëna == 127 || bajt_të_dhëna == 21) {
                if (bajt_të_dhëna == 21) { for (int Loop_INDEX = kursor_VALUE; Loop_INDEX < Madhësi; Loop_INDEX++) 명령해석기.linjë[Loop_INDEX - kursor_VALUE] = 명령해석기.linjë[Loop_INDEX]; Madhësi -= kursor_VALUE; kursor_VALUE = 0; }
                else if (kursor_VALUE > 0) { int 변경전 = e_përparme_VALUE(kursor_VALUE); for (int Loop_INDEX = kursor_VALUE; Loop_INDEX < Madhësi; Loop_INDEX++) 명령해석기.linjë[Loop_INDEX - kursor_VALUE + 변경전] = 명령해석기.linjë[Loop_INDEX]; Madhësi -= kursor_VALUE - 변경전; kursor_VALUE = 변경전; }
                다시(); continue;
            }
            if (bajt_të_dhëna == 11) { Madhësi = kursor_VALUE; 다시(); continue; }
            if (bajt_të_dhëna < 32 && bajt_të_dhëna != 9) continue;
            if (Madhësi == 명령해석기.linjë.length) { tejkalim = true; continue; }
            for (int Loop_INDEX = Madhësi; Loop_INDEX > kursor_VALUE; Loop_INDEX--) 명령해석기.linjë[Loop_INDEX] = 명령해석기.linjë[Loop_INDEX - 1];
            명령해석기.linjë[kursor_VALUE++] = bajt_të_dhëna; Madhësi++;
            if (kursor_VALUE == Madhësi && !가로보기 && 폭(0, Madhësi) <= 보이는폭()) panel.직렬쓰기(bajt_të_dhëna);
            else if (kursor_VALUE == Madhësi) 보이는줄(); else 다시();
        }
    }
}
