// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 beart_VALUE 경계를 지키는 삽입/삭제, 방향키, Ordú LOG_ró, Tab 완성. */
public final class líne_Eagarthóir {
    static boolean líne_na_n_orduithe;
    static int[] LOG_ró = new int[16 * 1024], LOG_fad = new int[16], Store_VALUE = new int[4096], 후보 = new int[64];
    static int LOG_COUNT, LOG_ró_cuir_deireadh_le, SEARCH_VALUE, 저장길이, Méid, cúrsóir_VALUE, 후보수, 후보길이, Start_fuinneog;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd slán_blaosc cianda_taispeáin run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String iontráil_Liosta, int Start_suíomh, int cuir_deireadh_le_suíomh, int 입력길이) {
        int beart_COUNT=0;
        for(int suíomh_INDEX=Start_suíomh;suíomh_INDEX<cuir_deireadh_le_suíomh;suíomh_INDEX++) {
            int pointe_cóid=iontráil_Liosta.charAt(suíomh_INDEX);
            if(pointe_cóid>=0xd800 && pointe_cóid<=0xdbff && suíomh_INDEX+1<cuir_deireadh_le_suíomh)pointe_cóid=0x10000+((pointe_cóid-0xd800)<<10)+iontráil_Liosta.charAt(++suíomh_INDEX)-0xdc00;
            int 수=pointe_cóid<128?1:pointe_cóid<2048?2:pointe_cóid<65536?3:4;
            if(beart_COUNT+수>62)return;
            for(int SEQUENCE_VALUE=수-1;SEQUENCE_VALUE>=0;SEQUENCE_VALUE--)명령후보[beart_COUNT++]=수==1?pointe_cóid:SEQUENCE_VALUE==수-1?(수==2?0xc0:수==3?0xe0:0xf0)|(pointe_cóid>>(6*SEQUENCE_VALUE)):0x80|((pointe_cóid>>(6*SEQUENCE_VALUE))&63);
        }
        if(beart_COUNT<입력길이)return;
        for(int suíomh_INDEX=0;suíomh_INDEX<입력길이;suíomh_INDEX++)if(명령후보[suíomh_INDEX]!=명령해석기.Líne[suíomh_INDEX])return;
        후보수++;후보길이=beart_COUNT+1;
        for(int suíomh_INDEX=0;suíomh_INDEX<beart_COUNT;suíomh_INDEX++)후보[suíomh_INDEX]=명령후보[suíomh_INDEX];후보[beart_COUNT]=' ';
    }
    static int 앞(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (명령해석기.Líne[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int Siar_VALUE(int 읽는자리) { if (읽는자리 < Méid) { 읽는자리++; while (읽는자리 < Méid && (명령해석기.Líne[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int Start_suíomh, int sprioc_VALUE_INDEX) {
        int 글칸수 = 0;
        for (int lúb_INDEX = Start_suíomh; lúb_INDEX < sprioc_VALUE_INDEX; lúb_INDEX++) { int beart_sonraí = 명령해석기.Líne[lúb_INDEX]; if ((beart_sonraí & 192) == 128) continue; 글칸수 += beart_sonraí >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void 다시() {
        단말.Scríobh("\r\u001b[2K");
        단말.Scríobh(líne_na_n_orduithe ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 Líne 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int COLUMNS = clár.Teirminéal(13) & 65535; return COLUMNS - (líne_na_n_orduithe ? 18 : 9); }
    static void 보이는줄() {
        if (cúrsóir_VALUE < Start_fuinneog) Start_fuinneog = cúrsóir_VALUE;
        while (폭(Start_fuinneog, cúrsóir_VALUE) > 보이는폭()) Start_fuinneog = Siar_VALUE(Start_fuinneog);
        int cuir_deireadh_le_suíomh = Start_fuinneog;
        while (cuir_deireadh_le_suíomh < Méid && 폭(Start_fuinneog, Siar_VALUE(cuir_deireadh_le_suíomh)) <= 보이는폭()) cuir_deireadh_le_suíomh = Siar_VALUE(cuir_deireadh_le_suíomh);
        단말.Scríobh("\r\u001b["); 단말.수(líne_na_n_orduithe ? 16 : 7); 단말.Scríobh("G\u001b[K");
        if (Start_fuinneog > 0) 단말.문자('<');
        for (int lúb_INDEX = Start_fuinneog; lúb_INDEX < cuir_deireadh_le_suíomh; lúb_INDEX++) clár.직렬쓰기(명령해석기.Líne[lúb_INDEX]);
        단말.문자(cuir_deireadh_le_suíomh < Méid ? '>' : ' ');
        단말.Scríobh("\u001b["); 단말.수(폭(cúrsóir_VALUE, cuir_deireadh_le_suíomh) + 1); 단말.문자('D');
        가로보기 = Start_fuinneog > 0 || cuir_deireadh_le_suíomh < Méid || 폭(0, Méid) > 보이는폭();
    }
    static void 기록넣기() {
        if (!líne_na_n_orduithe || Méid == 0 || Méid > 1024) return;
        if (LOG_COUNT > 0) {
            int 마지막자리 = (LOG_ró_cuir_deireadh_le + 15) % 16; boolean 같은여부 = LOG_fad[마지막자리] == Méid;
            for (int lúb_INDEX = 0; 같은여부 && lúb_INDEX < Méid; lúb_INDEX++) if (LOG_ró[마지막자리 * 1024 + lúb_INDEX] != 명령해석기.Líne[lúb_INDEX]) 같은여부 = false;
            if (같은여부) return;
        }
        LOG_fad[LOG_ró_cuir_deireadh_le] = Méid; for (int lúb_INDEX = 0; lúb_INDEX < Méid; lúb_INDEX++) LOG_ró[LOG_ró_cuir_deireadh_le * 1024 + lúb_INDEX] = 명령해석기.Líne[lúb_INDEX];
        LOG_ró_cuir_deireadh_le = (LOG_ró_cuir_deireadh_le + 1) % 16; if (LOG_COUNT < 16) LOG_COUNT++;
    }
    static void 기록이동(int DELTA_VALUE) {
        if (!líne_na_n_orduithe) return;
        if (SEARCH_VALUE == 0 && DELTA_VALUE > 0) { 저장길이 = Méid; for (int lúb_INDEX = 0; lúb_INDEX < Méid; lúb_INDEX++) Store_VALUE[lúb_INDEX] = 명령해석기.Líne[lúb_INDEX]; }
        int Ar_aghaidh_suíomh = SEARCH_VALUE + DELTA_VALUE; if (Ar_aghaidh_suíomh < 0 || Ar_aghaidh_suíomh > LOG_COUNT) return; SEARCH_VALUE = Ar_aghaidh_suíomh;
        if (SEARCH_VALUE == 0) { Méid = 저장길이; for (int lúb_INDEX = 0; lúb_INDEX < Méid; lúb_INDEX++) 명령해석기.Líne[lúb_INDEX] = Store_VALUE[lúb_INDEX]; }
        else { int 보관칸 = (LOG_ró_cuir_deireadh_le + 16 - SEARCH_VALUE) % 16; Méid = LOG_fad[보관칸]; for (int lúb_INDEX = 0; lúb_INDEX < Méid; lúb_INDEX++) 명령해석기.Líne[lúb_INDEX] = LOG_ró[보관칸 * 1024 + lúb_INDEX]; }
        cúrsóir_VALUE = Méid; 다시();
    }
    static void seó_LOG() {
        for (int iontráil_COUNT = 0; iontráil_COUNT < LOG_COUNT; iontráil_COUNT++) {
            int 보관칸 = (LOG_ró_cuir_deireadh_le + 16 - LOG_COUNT + iontráil_COUNT) % 16; 단말.수(iontráil_COUNT + 1); 단말.Scríobh("  ");
            for (int lúb_INDEX = 0; lúb_INDEX < LOG_fad[보관칸]; lúb_INDEX++) clár.직렬쓰기(LOG_ró[보관칸 * 1024 + lúb_INDEX]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] sonraí_ARRAY, int Start_suíomh, int iontráil_COUNT, int 접두말, int 총수, boolean 폴더번호) {
        if (iontráil_COUNT < 총수 || iontráil_COUNT > 62) return;
        for (int lúb_INDEX = 0; lúb_INDEX < 총수; lúb_INDEX++) if (sonraí_ARRAY[Start_suíomh + lúb_INDEX] != 명령해석기.Líne[접두말 + lúb_INDEX]) return;
        후보수++; 후보길이 = iontráil_COUNT + 1;
        for (int lúb_INDEX = 0; lúb_INDEX < iontráil_COUNT; lúb_INDEX++) 후보[lúb_INDEX] = sonraí_ARRAY[Start_suíomh + lúb_INDEX]; 후보[iontráil_COUNT] = 폴더번호 ? '/' : ' ';
    }
    static void 완성() {
        if (!líne_na_n_orduithe || cúrsóir_VALUE != Méid) return;
        int 시작점 = Méid; while (시작점 > 0 && 명령해석기.Líne[시작점 - 1] != ' ') 시작점--;
        for (int lúb_INDEX = 시작점; lúb_INDEX < Méid; lúb_INDEX++) if (명령해석기.Líne[lúb_INDEX] == '/' || 명령해석기.Líne[lúb_INDEX] == '"' || 명령해석기.Líne[lúb_INDEX] == 39 || 명령해석기.Líne[lúb_INDEX] == '\\') return;
        후보수 = 0; int iontráil_COUNT = Méid - 시작점;
        if (시작점 == 0) {
            for(int Liosta_INDEX=0;Liosta_INDEX<2;Liosta_INDEX++) {
                String iontráil_Liosta=Liosta_INDEX==0?명령들:관리명령.완성어();
                int 읽는자리=0;
                while(읽는자리<iontráil_Liosta.length()) {
                    int cuir_deireadh_le_suíomh=읽는자리;while(cuir_deireadh_le_suíomh<iontráil_Liosta.length() && iontráil_Liosta.charAt(cuir_deireadh_le_suíomh)!=' ')cuir_deireadh_le_suíomh++;
                    명령후보넣기(iontráil_Liosta,읽는자리,cuir_deireadh_le_suíomh,iontráil_COUNT);읽는자리=cuir_deireadh_le_suíomh+1;
                }
            }
        } else {
            Cuimhne_Comhaid.cosán_Start(1); Cuimhne_Comhaid.cosán_beart(0, '.'); Cuimhne_Comhaid.normalaigh_VALUE();
            for (int lúb_INDEX = 0; lúb_INDEX < Cuimhne_Comhaid.comhad_COUNT; lúb_INDEX++) {
                int Start_suíomh = Cuimhne_Comhaid.iontráil_Start(Cuimhne_Comhaid.Ainm, lúb_INDEX * 64, Cuimhne_Comhaid.이름길이[lúb_INDEX]);
                if (Start_suíomh >= 0) 후보넣기(Cuimhne_Comhaid.Ainm, lúb_INDEX * 64 + Start_suíomh, Cuimhne_Comhaid.이름길이[lúb_INDEX] - Start_suíomh, 시작점, iontráil_COUNT, false);
            }
            for (int lúb_INDEX = 0; lúb_INDEX < 16; lúb_INDEX++) {
                int Start_suíomh = Cuimhne_Comhaid.iontráil_Start(Cuimhne_Comhaid.eolaire_ainm, lúb_INDEX * 64, Cuimhne_Comhaid.eolaire_fad[lúb_INDEX]);
                if (Start_suíomh >= 0) 후보넣기(Cuimhne_Comhaid.eolaire_ainm, lúb_INDEX * 64 + Start_suíomh, Cuimhne_Comhaid.eolaire_fad[lúb_INDEX] - Start_suíomh, 시작점, iontráil_COUNT, true);
            }
        }
        if (후보수 != 1) { clár.직렬쓰기(7); return; }
        for (int lúb_INDEX = iontráil_COUNT; lúb_INDEX < 후보길이 && Méid < 명령해석기.Líne.length - 1; lúb_INDEX++) {
            if (후보[lúb_INDEX] == ' ' && lúb_INDEX != 후보길이 - 1) 명령해석기.Líne[Méid++] = '\\';
            명령해석기.Líne[Méid++] = 후보[lúb_INDEX];
        }
        cúrsóir_VALUE = Méid; 다시();
    }
    static int 탈출읽기() {
        int 시작점 = clár.밀리초();
        while (clár.밀리초() - 시작점 < 80) { int beart_sonraí = clár.직렬읽기(); if (beart_sonraí >= 0) return beart_sonraí; clár.YIELD_CPU(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int iontráil_COUNT = 0, cuir_deireadh_le_suíomh = -1;
        for (int lúb_INDEX = 0; lúb_INDEX < 12; lúb_INDEX++) { int beart_sonraí = 탈출읽기(); if (beart_sonraí < 0) return; if (beart_sonraí >= '0' && beart_sonraí <= '9') iontráil_COUNT = iontráil_COUNT * 10 + beart_sonraí - '0'; else { cuir_deireadh_le_suíomh = beart_sonraí; break; } }
        if (cuir_deireadh_le_suíomh == 'A') 기록이동(1);
        else if (cuir_deireadh_le_suíomh == 'B') 기록이동(-1);
        else if (cuir_deireadh_le_suíomh == 'C') { cúrsóir_VALUE = Siar_VALUE(cúrsóir_VALUE); 다시(); }
        else if (cuir_deireadh_le_suíomh == 'D') { cúrsóir_VALUE = 앞(cúrsóir_VALUE); 다시(); }
        else if (cuir_deireadh_le_suíomh == 'H' || cuir_deireadh_le_suíomh == '~' && (iontráil_COUNT == 1 || iontráil_COUNT == 7)) { cúrsóir_VALUE = 0; 다시(); }
        else if (cuir_deireadh_le_suíomh == 'F' || cuir_deireadh_le_suíomh == '~' && (iontráil_COUNT == 4 || iontráil_COUNT == 8)) { cúrsóir_VALUE = Méid; 다시(); }
        else if (cuir_deireadh_le_suíomh == '~' && iontráil_COUNT == 3 && cúrsóir_VALUE < Méid) {
            int Ar_aghaidh_suíomh = Siar_VALUE(cúrsóir_VALUE); for (int lúb_INDEX = Ar_aghaidh_suíomh; lúb_INDEX < Méid; lúb_INDEX++) 명령해석기.Líne[lúb_INDEX - Ar_aghaidh_suíomh + cúrsóir_VALUE] = 명령해석기.Líne[lúb_INDEX]; Méid -= Ar_aghaidh_suíomh - cúrsóir_VALUE; 다시();
        }
        else if (cuir_deireadh_le_suíomh == '~' && (iontráil_COUNT == 5 || iontráil_COUNT == 6)) clár.Teirminéal(iontráil_COUNT == 5 ? 5 : 6);
        else if (cuir_deireadh_le_suíomh == '~' && iontráil_COUNT == 24 && líne_na_n_orduithe) { 명령해석기.Teirminéal(true); }
    }
    static int Léigh() {
        if (!fuinneog_seisiún.이어읽기) { Méid = cúrsóir_VALUE = SEARCH_VALUE = Start_fuinneog = 0; 가로보기 = false; }
        else { fuinneog_seisiún.이어읽기 = false; 다시(); } boolean róshreabhadh = false;
        while (true) {
            int beart_sonraí = clár.직렬읽기(); if (beart_sonraí == -4096) return -3;
            if (clár.Teirminéal(14) != 0) 다시(); if (beart_sonraí < 0) { clár.YIELD_CPU(); continue; }
            if (beart_sonraí == 10 && 명령해석기.앞줄) { 명령해석기.앞줄 = false; continue; } 명령해석기.앞줄 = beart_sonraí == 13;
            if (beart_sonraí == 27) { 탈출(); continue; }
            if (beart_sonraí == 3) { 단말.Scríobh("^C\n"); return -1; }
            if (beart_sonraí == 4 && Méid == 0 && líne_na_n_orduithe) { if (clár.Teirminéal(2) != 0) 명령해석기.Teirminéal(true); return -1; }
            if (beart_sonraí == 13 || beart_sonraí == 10) { 단말.문자(10); if (!róshreabhadh) 기록넣기(); return róshreabhadh ? -2 : Méid; }
            if (beart_sonraí == 9 && líne_na_n_orduithe) { 완성(); continue; }
            if (beart_sonraí == 1 || beart_sonraí == 5) { cúrsóir_VALUE = beart_sonraí == 1 ? 0 : Méid; 다시(); continue; }
            if (beart_sonraí == 8 || beart_sonraí == 127 || beart_sonraí == 21) {
                if (beart_sonraí == 21) { for (int lúb_INDEX = cúrsóir_VALUE; lúb_INDEX < Méid; lúb_INDEX++) 명령해석기.Líne[lúb_INDEX - cúrsóir_VALUE] = 명령해석기.Líne[lúb_INDEX]; Méid -= cúrsóir_VALUE; cúrsóir_VALUE = 0; }
                else if (cúrsóir_VALUE > 0) { int 변경전 = 앞(cúrsóir_VALUE); for (int lúb_INDEX = cúrsóir_VALUE; lúb_INDEX < Méid; lúb_INDEX++) 명령해석기.Líne[lúb_INDEX - cúrsóir_VALUE + 변경전] = 명령해석기.Líne[lúb_INDEX]; Méid -= cúrsóir_VALUE - 변경전; cúrsóir_VALUE = 변경전; }
                다시(); continue;
            }
            if (beart_sonraí == 11) { Méid = cúrsóir_VALUE; 다시(); continue; }
            if (beart_sonraí < 32 && beart_sonraí != 9) continue;
            if (Méid == 명령해석기.Líne.length) { róshreabhadh = true; continue; }
            for (int lúb_INDEX = Méid; lúb_INDEX > cúrsóir_VALUE; lúb_INDEX--) 명령해석기.Líne[lúb_INDEX] = 명령해석기.Líne[lúb_INDEX - 1];
            명령해석기.Líne[cúrsóir_VALUE++] = beart_sonraí; Méid++;
            if (cúrsóir_VALUE == Méid && !가로보기 && 폭(0, Méid) <= 보이는폭()) clár.직렬쓰기(beart_sonraí);
            else if (cúrsóir_VALUE == Méid) 보이는줄(); else 다시();
        }
    }
}
