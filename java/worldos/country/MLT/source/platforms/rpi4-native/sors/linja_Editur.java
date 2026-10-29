// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 byte_VALUE 경계를 지키는 삽입/삭제, 방향키, kmand LOG_RECORD, Tab 완성. */
public final class linja_Editur {
    static boolean linja_ta_kmand;
    static int[] LOG_RECORD = new int[16 * 1024], LOG_tul = new int[16], Store_VALUE = new int[4096], 후보 = new int[64];
    static int LOG_COUNT, LOG_RECORD_ttermina, SEARCH_VALUE, 저장길이, daqqas, kerser_VALUE, 후보수, 후보길이, Bidu_tieqa;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd sigur_shell mill_bogħod_wera run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String entrata_Lista, int Bidu_pożizzjoni, int ttermina_pożizzjoni, int 입력길이) {
        int byte_COUNT=0;
        for(int pożizzjoni_INDEX=Bidu_pożizzjoni;pożizzjoni_INDEX<ttermina_pożizzjoni;pożizzjoni_INDEX++) {
            int kodiċi_tal_karattru=entrata_Lista.charAt(pożizzjoni_INDEX);
            if(kodiċi_tal_karattru>=0xd800 && kodiċi_tal_karattru<=0xdbff && pożizzjoni_INDEX+1<ttermina_pożizzjoni)kodiċi_tal_karattru=0x10000+((kodiċi_tal_karattru-0xd800)<<10)+entrata_Lista.charAt(++pożizzjoni_INDEX)-0xdc00;
            int 수=kodiċi_tal_karattru<128?1:kodiċi_tal_karattru<2048?2:kodiċi_tal_karattru<65536?3:4;
            if(byte_COUNT+수>62)return;
            for(int SEQUENCE_VALUE=수-1;SEQUENCE_VALUE>=0;SEQUENCE_VALUE--)명령후보[byte_COUNT++]=수==1?kodiċi_tal_karattru:SEQUENCE_VALUE==수-1?(수==2?0xc0:수==3?0xe0:0xf0)|(kodiċi_tal_karattru>>(6*SEQUENCE_VALUE)):0x80|((kodiċi_tal_karattru>>(6*SEQUENCE_VALUE))&63);
        }
        if(byte_COUNT<입력길이)return;
        for(int pożizzjoni_INDEX=0;pożizzjoni_INDEX<입력길이;pożizzjoni_INDEX++)if(명령후보[pożizzjoni_INDEX]!=명령해석기.linja[pożizzjoni_INDEX])return;
        후보수++;후보길이=byte_COUNT+1;
        for(int pożizzjoni_INDEX=0;pożizzjoni_INDEX<byte_COUNT;pożizzjoni_INDEX++)후보[pożizzjoni_INDEX]=명령후보[pożizzjoni_INDEX];후보[byte_COUNT]=' ';
    }
    static int 앞(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (명령해석기.linja[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int Lura_VALUE(int 읽는자리) { if (읽는자리 < daqqas) { 읽는자리++; while (읽는자리 < daqqas && (명령해석기.linja[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int Bidu_pożizzjoni, int destinazzjoni_VALUE_INDEX) {
        int 글칸수 = 0;
        for (int Loop_INDEX = Bidu_pożizzjoni; Loop_INDEX < destinazzjoni_VALUE_INDEX; Loop_INDEX++) { int byte_data = 명령해석기.linja[Loop_INDEX]; if ((byte_data & 192) == 128) continue; 글칸수 += byte_data >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void 다시() {
        단말.kiteb("\r\u001b[2K");
        단말.kiteb(linja_ta_kmand ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 linja 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int COLUMNS = bord.Terminal(13) & 65535; return COLUMNS - (linja_ta_kmand ? 18 : 9); }
    static void 보이는줄() {
        if (kerser_VALUE < Bidu_tieqa) Bidu_tieqa = kerser_VALUE;
        while (폭(Bidu_tieqa, kerser_VALUE) > 보이는폭()) Bidu_tieqa = Lura_VALUE(Bidu_tieqa);
        int ttermina_pożizzjoni = Bidu_tieqa;
        while (ttermina_pożizzjoni < daqqas && 폭(Bidu_tieqa, Lura_VALUE(ttermina_pożizzjoni)) <= 보이는폭()) ttermina_pożizzjoni = Lura_VALUE(ttermina_pożizzjoni);
        단말.kiteb("\r\u001b["); 단말.수(linja_ta_kmand ? 16 : 7); 단말.kiteb("G\u001b[K");
        if (Bidu_tieqa > 0) 단말.문자('<');
        for (int Loop_INDEX = Bidu_tieqa; Loop_INDEX < ttermina_pożizzjoni; Loop_INDEX++) bord.직렬쓰기(명령해석기.linja[Loop_INDEX]);
        단말.문자(ttermina_pożizzjoni < daqqas ? '>' : ' ');
        단말.kiteb("\u001b["); 단말.수(폭(kerser_VALUE, ttermina_pożizzjoni) + 1); 단말.문자('D');
        가로보기 = Bidu_tieqa > 0 || ttermina_pożizzjoni < daqqas || 폭(0, daqqas) > 보이는폭();
    }
    static void 기록넣기() {
        if (!linja_ta_kmand || daqqas == 0 || daqqas > 1024) return;
        if (LOG_COUNT > 0) {
            int 마지막자리 = (LOG_RECORD_ttermina + 15) % 16; boolean 같은여부 = LOG_tul[마지막자리] == daqqas;
            for (int Loop_INDEX = 0; 같은여부 && Loop_INDEX < daqqas; Loop_INDEX++) if (LOG_RECORD[마지막자리 * 1024 + Loop_INDEX] != 명령해석기.linja[Loop_INDEX]) 같은여부 = false;
            if (같은여부) return;
        }
        LOG_tul[LOG_RECORD_ttermina] = daqqas; for (int Loop_INDEX = 0; Loop_INDEX < daqqas; Loop_INDEX++) LOG_RECORD[LOG_RECORD_ttermina * 1024 + Loop_INDEX] = 명령해석기.linja[Loop_INDEX];
        LOG_RECORD_ttermina = (LOG_RECORD_ttermina + 1) % 16; if (LOG_COUNT < 16) LOG_COUNT++;
    }
    static void 기록이동(int DELTA_VALUE) {
        if (!linja_ta_kmand) return;
        if (SEARCH_VALUE == 0 && DELTA_VALUE > 0) { 저장길이 = daqqas; for (int Loop_INDEX = 0; Loop_INDEX < daqqas; Loop_INDEX++) Store_VALUE[Loop_INDEX] = 명령해석기.linja[Loop_INDEX]; }
        int Li_Jmiss_pożizzjoni = SEARCH_VALUE + DELTA_VALUE; if (Li_Jmiss_pożizzjoni < 0 || Li_Jmiss_pożizzjoni > LOG_COUNT) return; SEARCH_VALUE = Li_Jmiss_pożizzjoni;
        if (SEARCH_VALUE == 0) { daqqas = 저장길이; for (int Loop_INDEX = 0; Loop_INDEX < daqqas; Loop_INDEX++) 명령해석기.linja[Loop_INDEX] = Store_VALUE[Loop_INDEX]; }
        else { int 보관칸 = (LOG_RECORD_ttermina + 16 - SEARCH_VALUE) % 16; daqqas = LOG_tul[보관칸]; for (int Loop_INDEX = 0; Loop_INDEX < daqqas; Loop_INDEX++) 명령해석기.linja[Loop_INDEX] = LOG_RECORD[보관칸 * 1024 + Loop_INDEX]; }
        kerser_VALUE = daqqas; 다시();
    }
    static void wera_LOG() {
        for (int entrata_COUNT = 0; entrata_COUNT < LOG_COUNT; entrata_COUNT++) {
            int 보관칸 = (LOG_RECORD_ttermina + 16 - LOG_COUNT + entrata_COUNT) % 16; 단말.수(entrata_COUNT + 1); 단말.kiteb("  ");
            for (int Loop_INDEX = 0; Loop_INDEX < LOG_tul[보관칸]; Loop_INDEX++) bord.직렬쓰기(LOG_RECORD[보관칸 * 1024 + Loop_INDEX]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] data_ARRAY, int Bidu_pożizzjoni, int entrata_COUNT, int 접두말, int 총수, boolean 폴더번호) {
        if (entrata_COUNT < 총수 || entrata_COUNT > 62) return;
        for (int Loop_INDEX = 0; Loop_INDEX < 총수; Loop_INDEX++) if (data_ARRAY[Bidu_pożizzjoni + Loop_INDEX] != 명령해석기.linja[접두말 + Loop_INDEX]) return;
        후보수++; 후보길이 = entrata_COUNT + 1;
        for (int Loop_INDEX = 0; Loop_INDEX < entrata_COUNT; Loop_INDEX++) 후보[Loop_INDEX] = data_ARRAY[Bidu_pożizzjoni + Loop_INDEX]; 후보[entrata_COUNT] = 폴더번호 ? '/' : ' ';
    }
    static void 완성() {
        if (!linja_ta_kmand || kerser_VALUE != daqqas) return;
        int 시작점 = daqqas; while (시작점 > 0 && 명령해석기.linja[시작점 - 1] != ' ') 시작점--;
        for (int Loop_INDEX = 시작점; Loop_INDEX < daqqas; Loop_INDEX++) if (명령해석기.linja[Loop_INDEX] == '/' || 명령해석기.linja[Loop_INDEX] == '"' || 명령해석기.linja[Loop_INDEX] == 39 || 명령해석기.linja[Loop_INDEX] == '\\') return;
        후보수 = 0; int entrata_COUNT = daqqas - 시작점;
        if (시작점 == 0) {
            for(int Lista_INDEX=0;Lista_INDEX<2;Lista_INDEX++) {
                String entrata_Lista=Lista_INDEX==0?명령들:관리명령.완성어();
                int 읽는자리=0;
                while(읽는자리<entrata_Lista.length()) {
                    int ttermina_pożizzjoni=읽는자리;while(ttermina_pożizzjoni<entrata_Lista.length() && entrata_Lista.charAt(ttermina_pożizzjoni)!=' ')ttermina_pożizzjoni++;
                    명령후보넣기(entrata_Lista,읽는자리,ttermina_pożizzjoni,entrata_COUNT);읽는자리=ttermina_pożizzjoni+1;
                }
            }
        } else {
            Memorja_Fajls.mogħdija_Bidu(1); Memorja_Fajls.mogħdija_byte(0, '.'); Memorja_Fajls.nnormalizza_VALUE();
            for (int Loop_INDEX = 0; Loop_INDEX < Memorja_Fajls.fajl_COUNT; Loop_INDEX++) {
                int Bidu_pożizzjoni = Memorja_Fajls.entrata_Bidu(Memorja_Fajls.isem, Loop_INDEX * 64, Memorja_Fajls.이름길이[Loop_INDEX]);
                if (Bidu_pożizzjoni >= 0) 후보넣기(Memorja_Fajls.isem, Loop_INDEX * 64 + Bidu_pożizzjoni, Memorja_Fajls.이름길이[Loop_INDEX] - Bidu_pożizzjoni, 시작점, entrata_COUNT, false);
            }
            for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
                int Bidu_pożizzjoni = Memorja_Fajls.entrata_Bidu(Memorja_Fajls.direttorju_isem, Loop_INDEX * 64, Memorja_Fajls.direttorju_tul[Loop_INDEX]);
                if (Bidu_pożizzjoni >= 0) 후보넣기(Memorja_Fajls.direttorju_isem, Loop_INDEX * 64 + Bidu_pożizzjoni, Memorja_Fajls.direttorju_tul[Loop_INDEX] - Bidu_pożizzjoni, 시작점, entrata_COUNT, true);
            }
        }
        if (후보수 != 1) { bord.직렬쓰기(7); return; }
        for (int Loop_INDEX = entrata_COUNT; Loop_INDEX < 후보길이 && daqqas < 명령해석기.linja.length - 1; Loop_INDEX++) {
            if (후보[Loop_INDEX] == ' ' && Loop_INDEX != 후보길이 - 1) 명령해석기.linja[daqqas++] = '\\';
            명령해석기.linja[daqqas++] = 후보[Loop_INDEX];
        }
        kerser_VALUE = daqqas; 다시();
    }
    static int 탈출읽기() {
        int 시작점 = bord.밀리초();
        while (bord.밀리초() - 시작점 < 80) { int byte_data = bord.직렬읽기(); if (byte_data >= 0) return byte_data; bord.YIELD_CPU(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int entrata_COUNT = 0, ttermina_pożizzjoni = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 12; Loop_INDEX++) { int byte_data = 탈출읽기(); if (byte_data < 0) return; if (byte_data >= '0' && byte_data <= '9') entrata_COUNT = entrata_COUNT * 10 + byte_data - '0'; else { ttermina_pożizzjoni = byte_data; break; } }
        if (ttermina_pożizzjoni == 'A') 기록이동(1);
        else if (ttermina_pożizzjoni == 'B') 기록이동(-1);
        else if (ttermina_pożizzjoni == 'C') { kerser_VALUE = Lura_VALUE(kerser_VALUE); 다시(); }
        else if (ttermina_pożizzjoni == 'D') { kerser_VALUE = 앞(kerser_VALUE); 다시(); }
        else if (ttermina_pożizzjoni == 'H' || ttermina_pożizzjoni == '~' && (entrata_COUNT == 1 || entrata_COUNT == 7)) { kerser_VALUE = 0; 다시(); }
        else if (ttermina_pożizzjoni == 'F' || ttermina_pożizzjoni == '~' && (entrata_COUNT == 4 || entrata_COUNT == 8)) { kerser_VALUE = daqqas; 다시(); }
        else if (ttermina_pożizzjoni == '~' && entrata_COUNT == 3 && kerser_VALUE < daqqas) {
            int Li_Jmiss_pożizzjoni = Lura_VALUE(kerser_VALUE); for (int Loop_INDEX = Li_Jmiss_pożizzjoni; Loop_INDEX < daqqas; Loop_INDEX++) 명령해석기.linja[Loop_INDEX - Li_Jmiss_pożizzjoni + kerser_VALUE] = 명령해석기.linja[Loop_INDEX]; daqqas -= Li_Jmiss_pożizzjoni - kerser_VALUE; 다시();
        }
        else if (ttermina_pożizzjoni == '~' && (entrata_COUNT == 5 || entrata_COUNT == 6)) bord.Terminal(entrata_COUNT == 5 ? 5 : 6);
        else if (ttermina_pożizzjoni == '~' && entrata_COUNT == 24 && linja_ta_kmand) { 명령해석기.Terminal(true); }
    }
    static int 읽기() {
        if (!tieqa_sessjoni.이어읽기) { daqqas = kerser_VALUE = SEARCH_VALUE = Bidu_tieqa = 0; 가로보기 = false; }
        else { tieqa_sessjoni.이어읽기 = false; 다시(); } boolean overflow = false;
        while (true) {
            int byte_data = bord.직렬읽기(); if (byte_data == -4096) return -3;
            if (bord.Terminal(14) != 0) 다시(); if (byte_data < 0) { bord.YIELD_CPU(); continue; }
            if (byte_data == 10 && 명령해석기.앞줄) { 명령해석기.앞줄 = false; continue; } 명령해석기.앞줄 = byte_data == 13;
            if (byte_data == 27) { 탈출(); continue; }
            if (byte_data == 3) { 단말.kiteb("^C\n"); return -1; }
            if (byte_data == 4 && daqqas == 0 && linja_ta_kmand) { if (bord.Terminal(2) != 0) 명령해석기.Terminal(true); return -1; }
            if (byte_data == 13 || byte_data == 10) { 단말.문자(10); if (!overflow) 기록넣기(); return overflow ? -2 : daqqas; }
            if (byte_data == 9 && linja_ta_kmand) { 완성(); continue; }
            if (byte_data == 1 || byte_data == 5) { kerser_VALUE = byte_data == 1 ? 0 : daqqas; 다시(); continue; }
            if (byte_data == 8 || byte_data == 127 || byte_data == 21) {
                if (byte_data == 21) { for (int Loop_INDEX = kerser_VALUE; Loop_INDEX < daqqas; Loop_INDEX++) 명령해석기.linja[Loop_INDEX - kerser_VALUE] = 명령해석기.linja[Loop_INDEX]; daqqas -= kerser_VALUE; kerser_VALUE = 0; }
                else if (kerser_VALUE > 0) { int 변경전 = 앞(kerser_VALUE); for (int Loop_INDEX = kerser_VALUE; Loop_INDEX < daqqas; Loop_INDEX++) 명령해석기.linja[Loop_INDEX - kerser_VALUE + 변경전] = 명령해석기.linja[Loop_INDEX]; daqqas -= kerser_VALUE - 변경전; kerser_VALUE = 변경전; }
                다시(); continue;
            }
            if (byte_data == 11) { daqqas = kerser_VALUE; 다시(); continue; }
            if (byte_data < 32 && byte_data != 9) continue;
            if (daqqas == 명령해석기.linja.length) { overflow = true; continue; }
            for (int Loop_INDEX = daqqas; Loop_INDEX > kerser_VALUE; Loop_INDEX--) 명령해석기.linja[Loop_INDEX] = 명령해석기.linja[Loop_INDEX - 1];
            명령해석기.linja[kerser_VALUE++] = byte_data; daqqas++;
            if (kerser_VALUE == daqqas && !가로보기 && 폭(0, daqqas) <= 보이는폭()) bord.직렬쓰기(byte_data);
            else if (kerser_VALUE == daqqas) 보이는줄(); else 다시();
        }
    }
}
