// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 beit_VALUE 경계를 지키는 삽입/삭제, 방향키, Gorchymyn LOG_rhes, Tab 완성. */
public final class llinell_Editor {
    static boolean llinell_gorchymyn;
    static int[] LOG_rhes = new int[16 * 1024], LOG_hyd = new int[16], Store_VALUE = new int[4096], 후보 = new int[64];
    static int LOG_COUNT, LOG_rhes_gorffen, SEARCH_VALUE, 저장길이, Maint, cyrchwr_VALUE, 후보수, 후보길이, START_ffenestr;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd diogel_cragen pell_dangos run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String cofnod_Rhestr, int START_safle, int gorffen_safle, int 입력길이) {
        int beit_COUNT=0;
        for(int safle_INDEX=START_safle;safle_INDEX<gorffen_safle;safle_INDEX++) {
            int cod_nod=cofnod_Rhestr.charAt(safle_INDEX);
            if(cod_nod>=0xd800 && cod_nod<=0xdbff && safle_INDEX+1<gorffen_safle)cod_nod=0x10000+((cod_nod-0xd800)<<10)+cofnod_Rhestr.charAt(++safle_INDEX)-0xdc00;
            int 수=cod_nod<128?1:cod_nod<2048?2:cod_nod<65536?3:4;
            if(beit_COUNT+수>62)return;
            for(int SEQUENCE_VALUE=수-1;SEQUENCE_VALUE>=0;SEQUENCE_VALUE--)명령후보[beit_COUNT++]=수==1?cod_nod:SEQUENCE_VALUE==수-1?(수==2?0xc0:수==3?0xe0:0xf0)|(cod_nod>>(6*SEQUENCE_VALUE)):0x80|((cod_nod>>(6*SEQUENCE_VALUE))&63);
        }
        if(beit_COUNT<입력길이)return;
        for(int safle_INDEX=0;safle_INDEX<입력길이;safle_INDEX++)if(명령후보[safle_INDEX]!=명령해석기.llinell[safle_INDEX])return;
        후보수++;후보길이=beit_COUNT+1;
        for(int safle_INDEX=0;safle_INDEX<beit_COUNT;safle_INDEX++)후보[safle_INDEX]=명령후보[safle_INDEX];후보[beit_COUNT]=' ';
    }
    static int 앞(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (명령해석기.llinell[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int BACK_VALUE(int 읽는자리) { if (읽는자리 < Maint) { 읽는자리++; while (읽는자리 < Maint && (명령해석기.llinell[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int START_safle, int cyrchfan_VALUE_INDEX) {
        int 글칸수 = 0;
        for (int Loop_INDEX = START_safle; Loop_INDEX < cyrchfan_VALUE_INDEX; Loop_INDEX++) { int beit_data = 명령해석기.llinell[Loop_INDEX]; if ((beit_data & 192) == 128) continue; 글칸수 += beit_data >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void 다시() {
        단말.Ysgrifennu("\r\u001b[2K");
        단말.Ysgrifennu(llinell_gorchymyn ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 llinell 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int COLUMNS = bwrdd.Terfynell(13) & 65535; return COLUMNS - (llinell_gorchymyn ? 18 : 9); }
    static void 보이는줄() {
        if (cyrchwr_VALUE < START_ffenestr) START_ffenestr = cyrchwr_VALUE;
        while (폭(START_ffenestr, cyrchwr_VALUE) > 보이는폭()) START_ffenestr = BACK_VALUE(START_ffenestr);
        int gorffen_safle = START_ffenestr;
        while (gorffen_safle < Maint && 폭(START_ffenestr, BACK_VALUE(gorffen_safle)) <= 보이는폭()) gorffen_safle = BACK_VALUE(gorffen_safle);
        단말.Ysgrifennu("\r\u001b["); 단말.수(llinell_gorchymyn ? 16 : 7); 단말.Ysgrifennu("G\u001b[K");
        if (START_ffenestr > 0) 단말.문자('<');
        for (int Loop_INDEX = START_ffenestr; Loop_INDEX < gorffen_safle; Loop_INDEX++) bwrdd.직렬쓰기(명령해석기.llinell[Loop_INDEX]);
        단말.문자(gorffen_safle < Maint ? '>' : ' ');
        단말.Ysgrifennu("\u001b["); 단말.수(폭(cyrchwr_VALUE, gorffen_safle) + 1); 단말.문자('D');
        가로보기 = START_ffenestr > 0 || gorffen_safle < Maint || 폭(0, Maint) > 보이는폭();
    }
    static void 기록넣기() {
        if (!llinell_gorchymyn || Maint == 0 || Maint > 1024) return;
        if (LOG_COUNT > 0) {
            int 마지막자리 = (LOG_rhes_gorffen + 15) % 16; boolean 같은여부 = LOG_hyd[마지막자리] == Maint;
            for (int Loop_INDEX = 0; 같은여부 && Loop_INDEX < Maint; Loop_INDEX++) if (LOG_rhes[마지막자리 * 1024 + Loop_INDEX] != 명령해석기.llinell[Loop_INDEX]) 같은여부 = false;
            if (같은여부) return;
        }
        LOG_hyd[LOG_rhes_gorffen] = Maint; for (int Loop_INDEX = 0; Loop_INDEX < Maint; Loop_INDEX++) LOG_rhes[LOG_rhes_gorffen * 1024 + Loop_INDEX] = 명령해석기.llinell[Loop_INDEX];
        LOG_rhes_gorffen = (LOG_rhes_gorffen + 1) % 16; if (LOG_COUNT < 16) LOG_COUNT++;
    }
    static void 기록이동(int DELTA_VALUE) {
        if (!llinell_gorchymyn) return;
        if (SEARCH_VALUE == 0 && DELTA_VALUE > 0) { 저장길이 = Maint; for (int Loop_INDEX = 0; Loop_INDEX < Maint; Loop_INDEX++) Store_VALUE[Loop_INDEX] = 명령해석기.llinell[Loop_INDEX]; }
        int Nesaf_safle = SEARCH_VALUE + DELTA_VALUE; if (Nesaf_safle < 0 || Nesaf_safle > LOG_COUNT) return; SEARCH_VALUE = Nesaf_safle;
        if (SEARCH_VALUE == 0) { Maint = 저장길이; for (int Loop_INDEX = 0; Loop_INDEX < Maint; Loop_INDEX++) 명령해석기.llinell[Loop_INDEX] = Store_VALUE[Loop_INDEX]; }
        else { int 보관칸 = (LOG_rhes_gorffen + 16 - SEARCH_VALUE) % 16; Maint = LOG_hyd[보관칸]; for (int Loop_INDEX = 0; Loop_INDEX < Maint; Loop_INDEX++) 명령해석기.llinell[Loop_INDEX] = LOG_rhes[보관칸 * 1024 + Loop_INDEX]; }
        cyrchwr_VALUE = Maint; 다시();
    }
    static void sioe_LOG() {
        for (int cofnod_COUNT = 0; cofnod_COUNT < LOG_COUNT; cofnod_COUNT++) {
            int 보관칸 = (LOG_rhes_gorffen + 16 - LOG_COUNT + cofnod_COUNT) % 16; 단말.수(cofnod_COUNT + 1); 단말.Ysgrifennu("  ");
            for (int Loop_INDEX = 0; Loop_INDEX < LOG_hyd[보관칸]; Loop_INDEX++) bwrdd.직렬쓰기(LOG_rhes[보관칸 * 1024 + Loop_INDEX]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] data_ARAE, int START_safle, int cofnod_COUNT, int 접두말, int 총수, boolean 폴더번호) {
        if (cofnod_COUNT < 총수 || cofnod_COUNT > 62) return;
        for (int Loop_INDEX = 0; Loop_INDEX < 총수; Loop_INDEX++) if (data_ARAE[START_safle + Loop_INDEX] != 명령해석기.llinell[접두말 + Loop_INDEX]) return;
        후보수++; 후보길이 = cofnod_COUNT + 1;
        for (int Loop_INDEX = 0; Loop_INDEX < cofnod_COUNT; Loop_INDEX++) 후보[Loop_INDEX] = data_ARAE[START_safle + Loop_INDEX]; 후보[cofnod_COUNT] = 폴더번호 ? '/' : ' ';
    }
    static void 완성() {
        if (!llinell_gorchymyn || cyrchwr_VALUE != Maint) return;
        int 시작점 = Maint; while (시작점 > 0 && 명령해석기.llinell[시작점 - 1] != ' ') 시작점--;
        for (int Loop_INDEX = 시작점; Loop_INDEX < Maint; Loop_INDEX++) if (명령해석기.llinell[Loop_INDEX] == '/' || 명령해석기.llinell[Loop_INDEX] == '"' || 명령해석기.llinell[Loop_INDEX] == 39 || 명령해석기.llinell[Loop_INDEX] == '\\') return;
        후보수 = 0; int cofnod_COUNT = Maint - 시작점;
        if (시작점 == 0) {
            for(int Rhestr_INDEX=0;Rhestr_INDEX<2;Rhestr_INDEX++) {
                String cofnod_Rhestr=Rhestr_INDEX==0?명령들:관리명령.완성어();
                int 읽는자리=0;
                while(읽는자리<cofnod_Rhestr.length()) {
                    int gorffen_safle=읽는자리;while(gorffen_safle<cofnod_Rhestr.length() && cofnod_Rhestr.charAt(gorffen_safle)!=' ')gorffen_safle++;
                    명령후보넣기(cofnod_Rhestr,읽는자리,gorffen_safle,cofnod_COUNT);읽는자리=gorffen_safle+1;
                }
            }
        } else {
            Cof_Ffeil.llwybr_START(1); Cof_Ffeil.llwybr_beit(0, '.'); Cof_Ffeil.normaleiddio_VALUE();
            for (int Loop_INDEX = 0; Loop_INDEX < Cof_Ffeil.ffeil_COUNT; Loop_INDEX++) {
                int START_safle = Cof_Ffeil.cofnod_START(Cof_Ffeil.Enw, Loop_INDEX * 64, Cof_Ffeil.이름길이[Loop_INDEX]);
                if (START_safle >= 0) 후보넣기(Cof_Ffeil.Enw, Loop_INDEX * 64 + START_safle, Cof_Ffeil.이름길이[Loop_INDEX] - START_safle, 시작점, cofnod_COUNT, false);
            }
            for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
                int START_safle = Cof_Ffeil.cofnod_START(Cof_Ffeil.cyfeiriadur_enw, Loop_INDEX * 64, Cof_Ffeil.cyfeiriadur_hyd[Loop_INDEX]);
                if (START_safle >= 0) 후보넣기(Cof_Ffeil.cyfeiriadur_enw, Loop_INDEX * 64 + START_safle, Cof_Ffeil.cyfeiriadur_hyd[Loop_INDEX] - START_safle, 시작점, cofnod_COUNT, true);
            }
        }
        if (후보수 != 1) { bwrdd.직렬쓰기(7); return; }
        for (int Loop_INDEX = cofnod_COUNT; Loop_INDEX < 후보길이 && Maint < 명령해석기.llinell.length - 1; Loop_INDEX++) {
            if (후보[Loop_INDEX] == ' ' && Loop_INDEX != 후보길이 - 1) 명령해석기.llinell[Maint++] = '\\';
            명령해석기.llinell[Maint++] = 후보[Loop_INDEX];
        }
        cyrchwr_VALUE = Maint; 다시();
    }
    static int 탈출읽기() {
        int 시작점 = bwrdd.밀리초();
        while (bwrdd.밀리초() - 시작점 < 80) { int beit_data = bwrdd.직렬읽기(); if (beit_data >= 0) return beit_data; bwrdd.atal_CPU(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int cofnod_COUNT = 0, gorffen_safle = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 12; Loop_INDEX++) { int beit_data = 탈출읽기(); if (beit_data < 0) return; if (beit_data >= '0' && beit_data <= '9') cofnod_COUNT = cofnod_COUNT * 10 + beit_data - '0'; else { gorffen_safle = beit_data; break; } }
        if (gorffen_safle == 'A') 기록이동(1);
        else if (gorffen_safle == 'B') 기록이동(-1);
        else if (gorffen_safle == 'C') { cyrchwr_VALUE = BACK_VALUE(cyrchwr_VALUE); 다시(); }
        else if (gorffen_safle == 'D') { cyrchwr_VALUE = 앞(cyrchwr_VALUE); 다시(); }
        else if (gorffen_safle == 'H' || gorffen_safle == '~' && (cofnod_COUNT == 1 || cofnod_COUNT == 7)) { cyrchwr_VALUE = 0; 다시(); }
        else if (gorffen_safle == 'F' || gorffen_safle == '~' && (cofnod_COUNT == 4 || cofnod_COUNT == 8)) { cyrchwr_VALUE = Maint; 다시(); }
        else if (gorffen_safle == '~' && cofnod_COUNT == 3 && cyrchwr_VALUE < Maint) {
            int Nesaf_safle = BACK_VALUE(cyrchwr_VALUE); for (int Loop_INDEX = Nesaf_safle; Loop_INDEX < Maint; Loop_INDEX++) 명령해석기.llinell[Loop_INDEX - Nesaf_safle + cyrchwr_VALUE] = 명령해석기.llinell[Loop_INDEX]; Maint -= Nesaf_safle - cyrchwr_VALUE; 다시();
        }
        else if (gorffen_safle == '~' && (cofnod_COUNT == 5 || cofnod_COUNT == 6)) bwrdd.Terfynell(cofnod_COUNT == 5 ? 5 : 6);
        else if (gorffen_safle == '~' && cofnod_COUNT == 24 && llinell_gorchymyn) { 명령해석기.Terfynell(true); }
    }
    static int Darllen() {
        if (!ffenestr_sesiwn.이어읽기) { Maint = cyrchwr_VALUE = SEARCH_VALUE = START_ffenestr = 0; 가로보기 = false; }
        else { ffenestr_sesiwn.이어읽기 = false; 다시(); } boolean gorlif = false;
        while (true) {
            int beit_data = bwrdd.직렬읽기(); if (beit_data == -4096) return -3;
            if (bwrdd.Terfynell(14) != 0) 다시(); if (beit_data < 0) { bwrdd.atal_CPU(); continue; }
            if (beit_data == 10 && 명령해석기.앞줄) { 명령해석기.앞줄 = false; continue; } 명령해석기.앞줄 = beit_data == 13;
            if (beit_data == 27) { 탈출(); continue; }
            if (beit_data == 3) { 단말.Ysgrifennu("^C\n"); return -1; }
            if (beit_data == 4 && Maint == 0 && llinell_gorchymyn) { if (bwrdd.Terfynell(2) != 0) 명령해석기.Terfynell(true); return -1; }
            if (beit_data == 13 || beit_data == 10) { 단말.문자(10); if (!gorlif) 기록넣기(); return gorlif ? -2 : Maint; }
            if (beit_data == 9 && llinell_gorchymyn) { 완성(); continue; }
            if (beit_data == 1 || beit_data == 5) { cyrchwr_VALUE = beit_data == 1 ? 0 : Maint; 다시(); continue; }
            if (beit_data == 8 || beit_data == 127 || beit_data == 21) {
                if (beit_data == 21) { for (int Loop_INDEX = cyrchwr_VALUE; Loop_INDEX < Maint; Loop_INDEX++) 명령해석기.llinell[Loop_INDEX - cyrchwr_VALUE] = 명령해석기.llinell[Loop_INDEX]; Maint -= cyrchwr_VALUE; cyrchwr_VALUE = 0; }
                else if (cyrchwr_VALUE > 0) { int 변경전 = 앞(cyrchwr_VALUE); for (int Loop_INDEX = cyrchwr_VALUE; Loop_INDEX < Maint; Loop_INDEX++) 명령해석기.llinell[Loop_INDEX - cyrchwr_VALUE + 변경전] = 명령해석기.llinell[Loop_INDEX]; Maint -= cyrchwr_VALUE - 변경전; cyrchwr_VALUE = 변경전; }
                다시(); continue;
            }
            if (beit_data == 11) { Maint = cyrchwr_VALUE; 다시(); continue; }
            if (beit_data < 32 && beit_data != 9) continue;
            if (Maint == 명령해석기.llinell.length) { gorlif = true; continue; }
            for (int Loop_INDEX = Maint; Loop_INDEX > cyrchwr_VALUE; Loop_INDEX--) 명령해석기.llinell[Loop_INDEX] = 명령해석기.llinell[Loop_INDEX - 1];
            명령해석기.llinell[cyrchwr_VALUE++] = beit_data; Maint++;
            if (cyrchwr_VALUE == Maint && !가로보기 && 폭(0, Maint) <= 보이는폭()) bwrdd.직렬쓰기(beit_data);
            else if (cyrchwr_VALUE == Maint) 보이는줄(); else 다시();
        }
    }
}
