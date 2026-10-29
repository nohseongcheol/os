// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 paita_uara 경계를 지키는 삽입/삭제, 방향키, tono LOG_RECORD, Tab 완성. */
public final class hononga_Pūwhakatika {
    static boolean rārangi_tono;
    static int[] LOG_RECORD = new int[16 * 1024], LOG_roa = new int[16], Store_uara = new int[4096], 후보 = new int[64];
    static int LOG_COUNT, LOG_RECORD_mutu, Rapu_uara, 저장길이, rahi, pehu_uara, 후보수, 후보길이, Start_matapihi;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd haumaru_anga mamao_whakaatu run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String tāurunga_Rārangi, int Start_tūranga, int mutu_tūranga, int 입력길이) {
        int paita_COUNT=0;
        for(int tūranga_INDEX=Start_tūranga;tūranga_INDEX<mutu_tūranga;tūranga_INDEX++) {
            int waehere_pūāhua=tāurunga_Rārangi.charAt(tūranga_INDEX);
            if(waehere_pūāhua>=0xd800 && waehere_pūāhua<=0xdbff && tūranga_INDEX+1<mutu_tūranga)waehere_pūāhua=0x10000+((waehere_pūāhua-0xd800)<<10)+tāurunga_Rārangi.charAt(++tūranga_INDEX)-0xdc00;
            int 수=waehere_pūāhua<128?1:waehere_pūāhua<2048?2:waehere_pūāhua<65536?3:4;
            if(paita_COUNT+수>62)return;
            for(int SEQUENCE_uara=수-1;SEQUENCE_uara>=0;SEQUENCE_uara--)명령후보[paita_COUNT++]=수==1?waehere_pūāhua:SEQUENCE_uara==수-1?(수==2?0xc0:수==3?0xe0:0xf0)|(waehere_pūāhua>>(6*SEQUENCE_uara)):0x80|((waehere_pūāhua>>(6*SEQUENCE_uara))&63);
        }
        if(paita_COUNT<입력길이)return;
        for(int tūranga_INDEX=0;tūranga_INDEX<입력길이;tūranga_INDEX++)if(명령후보[tūranga_INDEX]!=명령해석기.hononga[tūranga_INDEX])return;
        후보수++;후보길이=paita_COUNT+1;
        for(int tūranga_INDEX=0;tūranga_INDEX<paita_COUNT;tūranga_INDEX++)후보[tūranga_INDEX]=명령후보[tūranga_INDEX];후보[paita_COUNT]=' ';
    }
    static int 앞(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (명령해석기.hononga[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int Hoki_uara(int 읽는자리) { if (읽는자리 < rahi) { 읽는자리++; while (읽는자리 < rahi && (명령해석기.hononga[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int Start_tūranga, int ūnga_uara_INDEX) {
        int 글칸수 = 0;
        for (int Loop_INDEX = Start_tūranga; Loop_INDEX < ūnga_uara_INDEX; Loop_INDEX++) { int paita_raraunga = 명령해석기.hononga[Loop_INDEX]; if ((paita_raraunga & 192) == 128) continue; 글칸수 += paita_raraunga >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void 다시() {
        단말.Tuhia("\r\u001b[2K");
        단말.Tuhia(rārangi_tono ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 hononga 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int COLUMNS = papa.Tauranga(13) & 65535; return COLUMNS - (rārangi_tono ? 18 : 9); }
    static void 보이는줄() {
        if (pehu_uara < Start_matapihi) Start_matapihi = pehu_uara;
        while (폭(Start_matapihi, pehu_uara) > 보이는폭()) Start_matapihi = Hoki_uara(Start_matapihi);
        int mutu_tūranga = Start_matapihi;
        while (mutu_tūranga < rahi && 폭(Start_matapihi, Hoki_uara(mutu_tūranga)) <= 보이는폭()) mutu_tūranga = Hoki_uara(mutu_tūranga);
        단말.Tuhia("\r\u001b["); 단말.수(rārangi_tono ? 16 : 7); 단말.Tuhia("G\u001b[K");
        if (Start_matapihi > 0) 단말.문자('<');
        for (int Loop_INDEX = Start_matapihi; Loop_INDEX < mutu_tūranga; Loop_INDEX++) papa.직렬쓰기(명령해석기.hononga[Loop_INDEX]);
        단말.문자(mutu_tūranga < rahi ? '>' : ' ');
        단말.Tuhia("\u001b["); 단말.수(폭(pehu_uara, mutu_tūranga) + 1); 단말.문자('D');
        가로보기 = Start_matapihi > 0 || mutu_tūranga < rahi || 폭(0, rahi) > 보이는폭();
    }
    static void 기록넣기() {
        if (!rārangi_tono || rahi == 0 || rahi > 1024) return;
        if (LOG_COUNT > 0) {
            int 마지막자리 = (LOG_RECORD_mutu + 15) % 16; boolean 같은여부 = LOG_roa[마지막자리] == rahi;
            for (int Loop_INDEX = 0; 같은여부 && Loop_INDEX < rahi; Loop_INDEX++) if (LOG_RECORD[마지막자리 * 1024 + Loop_INDEX] != 명령해석기.hononga[Loop_INDEX]) 같은여부 = false;
            if (같은여부) return;
        }
        LOG_roa[LOG_RECORD_mutu] = rahi; for (int Loop_INDEX = 0; Loop_INDEX < rahi; Loop_INDEX++) LOG_RECORD[LOG_RECORD_mutu * 1024 + Loop_INDEX] = 명령해석기.hononga[Loop_INDEX];
        LOG_RECORD_mutu = (LOG_RECORD_mutu + 1) % 16; if (LOG_COUNT < 16) LOG_COUNT++;
    }
    static void 기록이동(int DELTA_uara) {
        if (!rārangi_tono) return;
        if (Rapu_uara == 0 && DELTA_uara > 0) { 저장길이 = rahi; for (int Loop_INDEX = 0; Loop_INDEX < rahi; Loop_INDEX++) Store_uara[Loop_INDEX] = 명령해석기.hononga[Loop_INDEX]; }
        int Panuku_tūranga = Rapu_uara + DELTA_uara; if (Panuku_tūranga < 0 || Panuku_tūranga > LOG_COUNT) return; Rapu_uara = Panuku_tūranga;
        if (Rapu_uara == 0) { rahi = 저장길이; for (int Loop_INDEX = 0; Loop_INDEX < rahi; Loop_INDEX++) 명령해석기.hononga[Loop_INDEX] = Store_uara[Loop_INDEX]; }
        else { int 보관칸 = (LOG_RECORD_mutu + 16 - Rapu_uara) % 16; rahi = LOG_roa[보관칸]; for (int Loop_INDEX = 0; Loop_INDEX < rahi; Loop_INDEX++) 명령해석기.hononga[Loop_INDEX] = LOG_RECORD[보관칸 * 1024 + Loop_INDEX]; }
        pehu_uara = rahi; 다시();
    }
    static void whakaatu_LOG() {
        for (int tāurunga_COUNT = 0; tāurunga_COUNT < LOG_COUNT; tāurunga_COUNT++) {
            int 보관칸 = (LOG_RECORD_mutu + 16 - LOG_COUNT + tāurunga_COUNT) % 16; 단말.수(tāurunga_COUNT + 1); 단말.Tuhia("  ");
            for (int Loop_INDEX = 0; Loop_INDEX < LOG_roa[보관칸]; Loop_INDEX++) papa.직렬쓰기(LOG_RECORD[보관칸 * 1024 + Loop_INDEX]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] raraunga_HUĀNGA, int Start_tūranga, int tāurunga_COUNT, int 접두말, int 총수, boolean 폴더번호) {
        if (tāurunga_COUNT < 총수 || tāurunga_COUNT > 62) return;
        for (int Loop_INDEX = 0; Loop_INDEX < 총수; Loop_INDEX++) if (raraunga_HUĀNGA[Start_tūranga + Loop_INDEX] != 명령해석기.hononga[접두말 + Loop_INDEX]) return;
        후보수++; 후보길이 = tāurunga_COUNT + 1;
        for (int Loop_INDEX = 0; Loop_INDEX < tāurunga_COUNT; Loop_INDEX++) 후보[Loop_INDEX] = raraunga_HUĀNGA[Start_tūranga + Loop_INDEX]; 후보[tāurunga_COUNT] = 폴더번호 ? '/' : ' ';
    }
    static void 완성() {
        if (!rārangi_tono || pehu_uara != rahi) return;
        int 시작점 = rahi; while (시작점 > 0 && 명령해석기.hononga[시작점 - 1] != ' ') 시작점--;
        for (int Loop_INDEX = 시작점; Loop_INDEX < rahi; Loop_INDEX++) if (명령해석기.hononga[Loop_INDEX] == '/' || 명령해석기.hononga[Loop_INDEX] == '"' || 명령해석기.hononga[Loop_INDEX] == 39 || 명령해석기.hononga[Loop_INDEX] == '\\') return;
        후보수 = 0; int tāurunga_COUNT = rahi - 시작점;
        if (시작점 == 0) {
            for(int Rārangi_INDEX=0;Rārangi_INDEX<2;Rārangi_INDEX++) {
                String tāurunga_Rārangi=Rārangi_INDEX==0?명령들:관리명령.완성어();
                int 읽는자리=0;
                while(읽는자리<tāurunga_Rārangi.length()) {
                    int mutu_tūranga=읽는자리;while(mutu_tūranga<tāurunga_Rārangi.length() && tāurunga_Rārangi.charAt(mutu_tūranga)!=' ')mutu_tūranga++;
                    명령후보넣기(tāurunga_Rārangi,읽는자리,mutu_tūranga,tāurunga_COUNT);읽는자리=mutu_tūranga+1;
                }
            }
        } else {
            Pūmahara_Ngā_Kōnae.ara_Start(1); Pūmahara_Ngā_Kōnae.ara_paita(0, '.'); Pūmahara_Ngā_Kōnae.whakanoa_uara();
            for (int Loop_INDEX = 0; Loop_INDEX < Pūmahara_Ngā_Kōnae.kōnae_COUNT; Loop_INDEX++) {
                int Start_tūranga = Pūmahara_Ngā_Kōnae.tāurunga_Start(Pūmahara_Ngā_Kōnae.Ingoa, Loop_INDEX * 64, Pūmahara_Ngā_Kōnae.이름길이[Loop_INDEX]);
                if (Start_tūranga >= 0) 후보넣기(Pūmahara_Ngā_Kōnae.Ingoa, Loop_INDEX * 64 + Start_tūranga, Pūmahara_Ngā_Kōnae.이름길이[Loop_INDEX] - Start_tūranga, 시작점, tāurunga_COUNT, false);
            }
            for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
                int Start_tūranga = Pūmahara_Ngā_Kōnae.tāurunga_Start(Pūmahara_Ngā_Kōnae.whaiaronga_ingoa, Loop_INDEX * 64, Pūmahara_Ngā_Kōnae.whaiaronga_roa[Loop_INDEX]);
                if (Start_tūranga >= 0) 후보넣기(Pūmahara_Ngā_Kōnae.whaiaronga_ingoa, Loop_INDEX * 64 + Start_tūranga, Pūmahara_Ngā_Kōnae.whaiaronga_roa[Loop_INDEX] - Start_tūranga, 시작점, tāurunga_COUNT, true);
            }
        }
        if (후보수 != 1) { papa.직렬쓰기(7); return; }
        for (int Loop_INDEX = tāurunga_COUNT; Loop_INDEX < 후보길이 && rahi < 명령해석기.hononga.length - 1; Loop_INDEX++) {
            if (후보[Loop_INDEX] == ' ' && Loop_INDEX != 후보길이 - 1) 명령해석기.hononga[rahi++] = '\\';
            명령해석기.hononga[rahi++] = 후보[Loop_INDEX];
        }
        pehu_uara = rahi; 다시();
    }
    static int 탈출읽기() {
        int 시작점 = papa.밀리초();
        while (papa.밀리초() - 시작점 < 80) { int paita_raraunga = papa.직렬읽기(); if (paita_raraunga >= 0) return paita_raraunga; papa.YIELD_PTM(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int tāurunga_COUNT = 0, mutu_tūranga = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 12; Loop_INDEX++) { int paita_raraunga = 탈출읽기(); if (paita_raraunga < 0) return; if (paita_raraunga >= '0' && paita_raraunga <= '9') tāurunga_COUNT = tāurunga_COUNT * 10 + paita_raraunga - '0'; else { mutu_tūranga = paita_raraunga; break; } }
        if (mutu_tūranga == 'A') 기록이동(1);
        else if (mutu_tūranga == 'B') 기록이동(-1);
        else if (mutu_tūranga == 'C') { pehu_uara = Hoki_uara(pehu_uara); 다시(); }
        else if (mutu_tūranga == 'D') { pehu_uara = 앞(pehu_uara); 다시(); }
        else if (mutu_tūranga == 'H' || mutu_tūranga == '~' && (tāurunga_COUNT == 1 || tāurunga_COUNT == 7)) { pehu_uara = 0; 다시(); }
        else if (mutu_tūranga == 'F' || mutu_tūranga == '~' && (tāurunga_COUNT == 4 || tāurunga_COUNT == 8)) { pehu_uara = rahi; 다시(); }
        else if (mutu_tūranga == '~' && tāurunga_COUNT == 3 && pehu_uara < rahi) {
            int Panuku_tūranga = Hoki_uara(pehu_uara); for (int Loop_INDEX = Panuku_tūranga; Loop_INDEX < rahi; Loop_INDEX++) 명령해석기.hononga[Loop_INDEX - Panuku_tūranga + pehu_uara] = 명령해석기.hononga[Loop_INDEX]; rahi -= Panuku_tūranga - pehu_uara; 다시();
        }
        else if (mutu_tūranga == '~' && (tāurunga_COUNT == 5 || tāurunga_COUNT == 6)) papa.Tauranga(tāurunga_COUNT == 5 ? 5 : 6);
        else if (mutu_tūranga == '~' && tāurunga_COUNT == 24 && rārangi_tono) { 명령해석기.Tauranga(true); }
    }
    static int Pānuitia() {
        if (!matapihi_wātū.이어읽기) { rahi = pehu_uara = Rapu_uara = Start_matapihi = 0; 가로보기 = false; }
        else { matapihi_wātū.이어읽기 = false; 다시(); } boolean waipuke = false;
        while (true) {
            int paita_raraunga = papa.직렬읽기(); if (paita_raraunga == -4096) return -3;
            if (papa.Tauranga(14) != 0) 다시(); if (paita_raraunga < 0) { papa.YIELD_PTM(); continue; }
            if (paita_raraunga == 10 && 명령해석기.앞줄) { 명령해석기.앞줄 = false; continue; } 명령해석기.앞줄 = paita_raraunga == 13;
            if (paita_raraunga == 27) { 탈출(); continue; }
            if (paita_raraunga == 3) { 단말.Tuhia("^C\n"); return -1; }
            if (paita_raraunga == 4 && rahi == 0 && rārangi_tono) { if (papa.Tauranga(2) != 0) 명령해석기.Tauranga(true); return -1; }
            if (paita_raraunga == 13 || paita_raraunga == 10) { 단말.문자(10); if (!waipuke) 기록넣기(); return waipuke ? -2 : rahi; }
            if (paita_raraunga == 9 && rārangi_tono) { 완성(); continue; }
            if (paita_raraunga == 1 || paita_raraunga == 5) { pehu_uara = paita_raraunga == 1 ? 0 : rahi; 다시(); continue; }
            if (paita_raraunga == 8 || paita_raraunga == 127 || paita_raraunga == 21) {
                if (paita_raraunga == 21) { for (int Loop_INDEX = pehu_uara; Loop_INDEX < rahi; Loop_INDEX++) 명령해석기.hononga[Loop_INDEX - pehu_uara] = 명령해석기.hononga[Loop_INDEX]; rahi -= pehu_uara; pehu_uara = 0; }
                else if (pehu_uara > 0) { int 변경전 = 앞(pehu_uara); for (int Loop_INDEX = pehu_uara; Loop_INDEX < rahi; Loop_INDEX++) 명령해석기.hononga[Loop_INDEX - pehu_uara + 변경전] = 명령해석기.hononga[Loop_INDEX]; rahi -= pehu_uara - 변경전; pehu_uara = 변경전; }
                다시(); continue;
            }
            if (paita_raraunga == 11) { rahi = pehu_uara; 다시(); continue; }
            if (paita_raraunga < 32 && paita_raraunga != 9) continue;
            if (rahi == 명령해석기.hononga.length) { waipuke = true; continue; }
            for (int Loop_INDEX = rahi; Loop_INDEX > pehu_uara; Loop_INDEX--) 명령해석기.hononga[Loop_INDEX] = 명령해석기.hononga[Loop_INDEX - 1];
            명령해석기.hononga[pehu_uara++] = paita_raraunga; rahi++;
            if (pehu_uara == rahi && !가로보기 && 폭(0, rahi) <= 보이는폭()) papa.직렬쓰기(paita_raraunga);
            else if (pehu_uara == rahi) 보이는줄(); else 다시();
        }
    }
}
