// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 baidht_VALUE 경계를 지키는 삽입/삭제, 방향키, àithne LOG_ràgh, Tab 완성. */
public final class loidhne_deasaiche {
    static boolean loidhne_àithne;
    static int[] LOG_ràgh = new int[16 * 1024], LOG_faid = new int[16], Store_VALUE = new int[4096], 후보 = new int[64];
    static int LOG_COUNT, LOG_ràgh_crìochnaich, lorg_VALUE, 저장길이, atharraich_am_meud, cursair_VALUE, 후보수, 후보길이, Start_uinneag;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd tèarainte_slige cian_taisbean run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String cur_a_steach_Liosta, int Start_suidhich, int crìochnaich_suidhich, int 입력길이) {
        int baidht_COUNT=0;
        for(int suidhich_INDEX=Start_suidhich;suidhich_INDEX<crìochnaich_suidhich;suidhich_INDEX++) {
            int còd_a_charactair=cur_a_steach_Liosta.charAt(suidhich_INDEX);
            if(còd_a_charactair>=0xd800 && còd_a_charactair<=0xdbff && suidhich_INDEX+1<crìochnaich_suidhich)còd_a_charactair=0x10000+((còd_a_charactair-0xd800)<<10)+cur_a_steach_Liosta.charAt(++suidhich_INDEX)-0xdc00;
            int 수=còd_a_charactair<128?1:còd_a_charactair<2048?2:còd_a_charactair<65536?3:4;
            if(baidht_COUNT+수>62)return;
            for(int SEQUENCE_VALUE=수-1;SEQUENCE_VALUE>=0;SEQUENCE_VALUE--)명령후보[baidht_COUNT++]=수==1?còd_a_charactair:SEQUENCE_VALUE==수-1?(수==2?0xc0:수==3?0xe0:0xf0)|(còd_a_charactair>>(6*SEQUENCE_VALUE)):0x80|((còd_a_charactair>>(6*SEQUENCE_VALUE))&63);
        }
        if(baidht_COUNT<입력길이)return;
        for(int suidhich_INDEX=0;suidhich_INDEX<입력길이;suidhich_INDEX++)if(명령후보[suidhich_INDEX]!=명령해석기.loidhne[suidhich_INDEX])return;
        후보수++;후보길이=baidht_COUNT+1;
        for(int suidhich_INDEX=0;suidhich_INDEX<baidht_COUNT;suidhich_INDEX++)후보[suidhich_INDEX]=명령후보[suidhich_INDEX];후보[baidht_COUNT]=' ';
    }
    static int 앞(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (명령해석기.loidhne[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int Air_ais_VALUE(int 읽는자리) { if (읽는자리 < atharraich_am_meud) { 읽는자리++; while (읽는자리 < atharraich_am_meud && (명령해석기.loidhne[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int Start_suidhich, int ceann_uidhe_VALUE_INDEX) {
        int 글칸수 = 0;
        for (int lùb_INDEX = Start_suidhich; lùb_INDEX < ceann_uidhe_VALUE_INDEX; lùb_INDEX++) { int baidht_dàta = 명령해석기.loidhne[lùb_INDEX]; if ((baidht_dàta & 192) == 128) continue; 글칸수 += baidht_dàta >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void 다시() {
        단말.sgrìobh("\r\u001b[2K");
        단말.sgrìobh(loidhne_àithne ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 loidhne 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int COLUMNS = bòrd.tèirmineal(13) & 65535; return COLUMNS - (loidhne_àithne ? 18 : 9); }
    static void 보이는줄() {
        if (cursair_VALUE < Start_uinneag) Start_uinneag = cursair_VALUE;
        while (폭(Start_uinneag, cursair_VALUE) > 보이는폭()) Start_uinneag = Air_ais_VALUE(Start_uinneag);
        int crìochnaich_suidhich = Start_uinneag;
        while (crìochnaich_suidhich < atharraich_am_meud && 폭(Start_uinneag, Air_ais_VALUE(crìochnaich_suidhich)) <= 보이는폭()) crìochnaich_suidhich = Air_ais_VALUE(crìochnaich_suidhich);
        단말.sgrìobh("\r\u001b["); 단말.수(loidhne_àithne ? 16 : 7); 단말.sgrìobh("G\u001b[K");
        if (Start_uinneag > 0) 단말.문자('<');
        for (int lùb_INDEX = Start_uinneag; lùb_INDEX < crìochnaich_suidhich; lùb_INDEX++) bòrd.직렬쓰기(명령해석기.loidhne[lùb_INDEX]);
        단말.문자(crìochnaich_suidhich < atharraich_am_meud ? '>' : ' ');
        단말.sgrìobh("\u001b["); 단말.수(폭(cursair_VALUE, crìochnaich_suidhich) + 1); 단말.문자('D');
        가로보기 = Start_uinneag > 0 || crìochnaich_suidhich < atharraich_am_meud || 폭(0, atharraich_am_meud) > 보이는폭();
    }
    static void 기록넣기() {
        if (!loidhne_àithne || atharraich_am_meud == 0 || atharraich_am_meud > 1024) return;
        if (LOG_COUNT > 0) {
            int 마지막자리 = (LOG_ràgh_crìochnaich + 15) % 16; boolean 같은여부 = LOG_faid[마지막자리] == atharraich_am_meud;
            for (int lùb_INDEX = 0; 같은여부 && lùb_INDEX < atharraich_am_meud; lùb_INDEX++) if (LOG_ràgh[마지막자리 * 1024 + lùb_INDEX] != 명령해석기.loidhne[lùb_INDEX]) 같은여부 = false;
            if (같은여부) return;
        }
        LOG_faid[LOG_ràgh_crìochnaich] = atharraich_am_meud; for (int lùb_INDEX = 0; lùb_INDEX < atharraich_am_meud; lùb_INDEX++) LOG_ràgh[LOG_ràgh_crìochnaich * 1024 + lùb_INDEX] = 명령해석기.loidhne[lùb_INDEX];
        LOG_ràgh_crìochnaich = (LOG_ràgh_crìochnaich + 1) % 16; if (LOG_COUNT < 16) LOG_COUNT++;
    }
    static void 기록이동(int DELTA_VALUE) {
        if (!loidhne_àithne) return;
        if (lorg_VALUE == 0 && DELTA_VALUE > 0) { 저장길이 = atharraich_am_meud; for (int lùb_INDEX = 0; lùb_INDEX < atharraich_am_meud; lùb_INDEX++) Store_VALUE[lùb_INDEX] = 명령해석기.loidhne[lùb_INDEX]; }
        int air_adhart_suidhich = lorg_VALUE + DELTA_VALUE; if (air_adhart_suidhich < 0 || air_adhart_suidhich > LOG_COUNT) return; lorg_VALUE = air_adhart_suidhich;
        if (lorg_VALUE == 0) { atharraich_am_meud = 저장길이; for (int lùb_INDEX = 0; lùb_INDEX < atharraich_am_meud; lùb_INDEX++) 명령해석기.loidhne[lùb_INDEX] = Store_VALUE[lùb_INDEX]; }
        else { int 보관칸 = (LOG_ràgh_crìochnaich + 16 - lorg_VALUE) % 16; atharraich_am_meud = LOG_faid[보관칸]; for (int lùb_INDEX = 0; lùb_INDEX < atharraich_am_meud; lùb_INDEX++) 명령해석기.loidhne[lùb_INDEX] = LOG_ràgh[보관칸 * 1024 + lùb_INDEX]; }
        cursair_VALUE = atharraich_am_meud; 다시();
    }
    static void show_LOG() {
        for (int cur_a_steach_COUNT = 0; cur_a_steach_COUNT < LOG_COUNT; cur_a_steach_COUNT++) {
            int 보관칸 = (LOG_ràgh_crìochnaich + 16 - LOG_COUNT + cur_a_steach_COUNT) % 16; 단말.수(cur_a_steach_COUNT + 1); 단말.sgrìobh("  ");
            for (int lùb_INDEX = 0; lùb_INDEX < LOG_faid[보관칸]; lùb_INDEX++) bòrd.직렬쓰기(LOG_ràgh[보관칸 * 1024 + lùb_INDEX]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] dàta_ARRAY, int Start_suidhich, int cur_a_steach_COUNT, int 접두말, int 총수, boolean 폴더번호) {
        if (cur_a_steach_COUNT < 총수 || cur_a_steach_COUNT > 62) return;
        for (int lùb_INDEX = 0; lùb_INDEX < 총수; lùb_INDEX++) if (dàta_ARRAY[Start_suidhich + lùb_INDEX] != 명령해석기.loidhne[접두말 + lùb_INDEX]) return;
        후보수++; 후보길이 = cur_a_steach_COUNT + 1;
        for (int lùb_INDEX = 0; lùb_INDEX < cur_a_steach_COUNT; lùb_INDEX++) 후보[lùb_INDEX] = dàta_ARRAY[Start_suidhich + lùb_INDEX]; 후보[cur_a_steach_COUNT] = 폴더번호 ? '/' : ' ';
    }
    static void 완성() {
        if (!loidhne_àithne || cursair_VALUE != atharraich_am_meud) return;
        int 시작점 = atharraich_am_meud; while (시작점 > 0 && 명령해석기.loidhne[시작점 - 1] != ' ') 시작점--;
        for (int lùb_INDEX = 시작점; lùb_INDEX < atharraich_am_meud; lùb_INDEX++) if (명령해석기.loidhne[lùb_INDEX] == '/' || 명령해석기.loidhne[lùb_INDEX] == '"' || 명령해석기.loidhne[lùb_INDEX] == 39 || 명령해석기.loidhne[lùb_INDEX] == '\\') return;
        후보수 = 0; int cur_a_steach_COUNT = atharraich_am_meud - 시작점;
        if (시작점 == 0) {
            for(int Liosta_INDEX=0;Liosta_INDEX<2;Liosta_INDEX++) {
                String cur_a_steach_Liosta=Liosta_INDEX==0?명령들:관리명령.완성어();
                int 읽는자리=0;
                while(읽는자리<cur_a_steach_Liosta.length()) {
                    int crìochnaich_suidhich=읽는자리;while(crìochnaich_suidhich<cur_a_steach_Liosta.length() && cur_a_steach_Liosta.charAt(crìochnaich_suidhich)!=' ')crìochnaich_suidhich++;
                    명령후보넣기(cur_a_steach_Liosta,읽는자리,crìochnaich_suidhich,cur_a_steach_COUNT);읽는자리=crìochnaich_suidhich+1;
                }
            }
        } else {
            cuimhne_faidhlichean.slighe_Start(1); cuimhne_faidhlichean.slighe_baidht(0, '.'); cuimhne_faidhlichean.àbhaistich_VALUE();
            for (int lùb_INDEX = 0; lùb_INDEX < cuimhne_faidhlichean.faidhle_COUNT; lùb_INDEX++) {
                int Start_suidhich = cuimhne_faidhlichean.cur_a_steach_Start(cuimhne_faidhlichean.Ainm, lùb_INDEX * 64, cuimhne_faidhlichean.이름길이[lùb_INDEX]);
                if (Start_suidhich >= 0) 후보넣기(cuimhne_faidhlichean.Ainm, lùb_INDEX * 64 + Start_suidhich, cuimhne_faidhlichean.이름길이[lùb_INDEX] - Start_suidhich, 시작점, cur_a_steach_COUNT, false);
            }
            for (int lùb_INDEX = 0; lùb_INDEX < 16; lùb_INDEX++) {
                int Start_suidhich = cuimhne_faidhlichean.cur_a_steach_Start(cuimhne_faidhlichean.eòlaire_ainm, lùb_INDEX * 64, cuimhne_faidhlichean.eòlaire_faid[lùb_INDEX]);
                if (Start_suidhich >= 0) 후보넣기(cuimhne_faidhlichean.eòlaire_ainm, lùb_INDEX * 64 + Start_suidhich, cuimhne_faidhlichean.eòlaire_faid[lùb_INDEX] - Start_suidhich, 시작점, cur_a_steach_COUNT, true);
            }
        }
        if (후보수 != 1) { bòrd.직렬쓰기(7); return; }
        for (int lùb_INDEX = cur_a_steach_COUNT; lùb_INDEX < 후보길이 && atharraich_am_meud < 명령해석기.loidhne.length - 1; lùb_INDEX++) {
            if (후보[lùb_INDEX] == ' ' && lùb_INDEX != 후보길이 - 1) 명령해석기.loidhne[atharraich_am_meud++] = '\\';
            명령해석기.loidhne[atharraich_am_meud++] = 후보[lùb_INDEX];
        }
        cursair_VALUE = atharraich_am_meud; 다시();
    }
    static int 탈출읽기() {
        int 시작점 = bòrd.밀리초();
        while (bòrd.밀리초() - 시작점 < 80) { int baidht_dàta = bòrd.직렬읽기(); if (baidht_dàta >= 0) return baidht_dàta; bòrd.YIELD_CPU(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int cur_a_steach_COUNT = 0, crìochnaich_suidhich = -1;
        for (int lùb_INDEX = 0; lùb_INDEX < 12; lùb_INDEX++) { int baidht_dàta = 탈출읽기(); if (baidht_dàta < 0) return; if (baidht_dàta >= '0' && baidht_dàta <= '9') cur_a_steach_COUNT = cur_a_steach_COUNT * 10 + baidht_dàta - '0'; else { crìochnaich_suidhich = baidht_dàta; break; } }
        if (crìochnaich_suidhich == 'A') 기록이동(1);
        else if (crìochnaich_suidhich == 'B') 기록이동(-1);
        else if (crìochnaich_suidhich == 'C') { cursair_VALUE = Air_ais_VALUE(cursair_VALUE); 다시(); }
        else if (crìochnaich_suidhich == 'D') { cursair_VALUE = 앞(cursair_VALUE); 다시(); }
        else if (crìochnaich_suidhich == 'H' || crìochnaich_suidhich == '~' && (cur_a_steach_COUNT == 1 || cur_a_steach_COUNT == 7)) { cursair_VALUE = 0; 다시(); }
        else if (crìochnaich_suidhich == 'F' || crìochnaich_suidhich == '~' && (cur_a_steach_COUNT == 4 || cur_a_steach_COUNT == 8)) { cursair_VALUE = atharraich_am_meud; 다시(); }
        else if (crìochnaich_suidhich == '~' && cur_a_steach_COUNT == 3 && cursair_VALUE < atharraich_am_meud) {
            int air_adhart_suidhich = Air_ais_VALUE(cursair_VALUE); for (int lùb_INDEX = air_adhart_suidhich; lùb_INDEX < atharraich_am_meud; lùb_INDEX++) 명령해석기.loidhne[lùb_INDEX - air_adhart_suidhich + cursair_VALUE] = 명령해석기.loidhne[lùb_INDEX]; atharraich_am_meud -= air_adhart_suidhich - cursair_VALUE; 다시();
        }
        else if (crìochnaich_suidhich == '~' && (cur_a_steach_COUNT == 5 || cur_a_steach_COUNT == 6)) bòrd.tèirmineal(cur_a_steach_COUNT == 5 ? 5 : 6);
        else if (crìochnaich_suidhich == '~' && cur_a_steach_COUNT == 24 && loidhne_àithne) { 명령해석기.tèirmineal(true); }
    }
    static int 읽기() {
        if (!uinneag_seisean.이어읽기) { atharraich_am_meud = cursair_VALUE = lorg_VALUE = Start_uinneag = 0; 가로보기 = false; }
        else { uinneag_seisean.이어읽기 = false; 다시(); } boolean taomadh = false;
        while (true) {
            int baidht_dàta = bòrd.직렬읽기(); if (baidht_dàta == -4096) return -3;
            if (bòrd.tèirmineal(14) != 0) 다시(); if (baidht_dàta < 0) { bòrd.YIELD_CPU(); continue; }
            if (baidht_dàta == 10 && 명령해석기.앞줄) { 명령해석기.앞줄 = false; continue; } 명령해석기.앞줄 = baidht_dàta == 13;
            if (baidht_dàta == 27) { 탈출(); continue; }
            if (baidht_dàta == 3) { 단말.sgrìobh("^C\n"); return -1; }
            if (baidht_dàta == 4 && atharraich_am_meud == 0 && loidhne_àithne) { if (bòrd.tèirmineal(2) != 0) 명령해석기.tèirmineal(true); return -1; }
            if (baidht_dàta == 13 || baidht_dàta == 10) { 단말.문자(10); if (!taomadh) 기록넣기(); return taomadh ? -2 : atharraich_am_meud; }
            if (baidht_dàta == 9 && loidhne_àithne) { 완성(); continue; }
            if (baidht_dàta == 1 || baidht_dàta == 5) { cursair_VALUE = baidht_dàta == 1 ? 0 : atharraich_am_meud; 다시(); continue; }
            if (baidht_dàta == 8 || baidht_dàta == 127 || baidht_dàta == 21) {
                if (baidht_dàta == 21) { for (int lùb_INDEX = cursair_VALUE; lùb_INDEX < atharraich_am_meud; lùb_INDEX++) 명령해석기.loidhne[lùb_INDEX - cursair_VALUE] = 명령해석기.loidhne[lùb_INDEX]; atharraich_am_meud -= cursair_VALUE; cursair_VALUE = 0; }
                else if (cursair_VALUE > 0) { int 변경전 = 앞(cursair_VALUE); for (int lùb_INDEX = cursair_VALUE; lùb_INDEX < atharraich_am_meud; lùb_INDEX++) 명령해석기.loidhne[lùb_INDEX - cursair_VALUE + 변경전] = 명령해석기.loidhne[lùb_INDEX]; atharraich_am_meud -= cursair_VALUE - 변경전; cursair_VALUE = 변경전; }
                다시(); continue;
            }
            if (baidht_dàta == 11) { atharraich_am_meud = cursair_VALUE; 다시(); continue; }
            if (baidht_dàta < 32 && baidht_dàta != 9) continue;
            if (atharraich_am_meud == 명령해석기.loidhne.length) { taomadh = true; continue; }
            for (int lùb_INDEX = atharraich_am_meud; lùb_INDEX > cursair_VALUE; lùb_INDEX--) 명령해석기.loidhne[lùb_INDEX] = 명령해석기.loidhne[lùb_INDEX - 1];
            명령해석기.loidhne[cursair_VALUE++] = baidht_dàta; atharraich_am_meud++;
            if (cursair_VALUE == atharraich_am_meud && !가로보기 && 폭(0, atharraich_am_meud) <= 보이는폭()) bòrd.직렬쓰기(baidht_dàta);
            else if (cursair_VALUE == atharraich_am_meud) 보이는줄(); else 다시();
        }
    }
}
