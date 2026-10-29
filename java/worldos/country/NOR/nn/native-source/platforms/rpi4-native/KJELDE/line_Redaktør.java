// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 byte_VALUE 경계를 지키는 삽입/삭제, 방향키, Kommando LOG_rad, Tab 완성. */
public final class line_Redaktør {
    static boolean kommandoline;
    static int[] LOG_rad = new int[16 * 1024], LOG_lengd = new int[16], Store_VALUE = new int[4096], 후보 = new int[64];
    static int LOG_COUNT, LOG_rad_avslutte, Søk_VALUE, 저장길이, Storleik, markør_VALUE, 후보수, 후보길이, START_vindauge;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd sikker_grensesnitt fjern_vise run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String oppføring_Liste, int START_plassere, int avslutte_plassere, int 입력길이) {
        int byte_COUNT=0;
        for(int plassere_INDEX=START_plassere;plassere_INDEX<avslutte_plassere;plassere_INDEX++) {
            int teiknkode=oppføring_Liste.charAt(plassere_INDEX);
            if(teiknkode>=0xd800 && teiknkode<=0xdbff && plassere_INDEX+1<avslutte_plassere)teiknkode=0x10000+((teiknkode-0xd800)<<10)+oppføring_Liste.charAt(++plassere_INDEX)-0xdc00;
            int 수=teiknkode<128?1:teiknkode<2048?2:teiknkode<65536?3:4;
            if(byte_COUNT+수>62)return;
            for(int SEQUENCE_VALUE=수-1;SEQUENCE_VALUE>=0;SEQUENCE_VALUE--)명령후보[byte_COUNT++]=수==1?teiknkode:SEQUENCE_VALUE==수-1?(수==2?0xc0:수==3?0xe0:0xf0)|(teiknkode>>(6*SEQUENCE_VALUE)):0x80|((teiknkode>>(6*SEQUENCE_VALUE))&63);
        }
        if(byte_COUNT<입력길이)return;
        for(int plassere_INDEX=0;plassere_INDEX<입력길이;plassere_INDEX++)if(명령후보[plassere_INDEX]!=명령해석기.linje[plassere_INDEX])return;
        후보수++;후보길이=byte_COUNT+1;
        for(int plassere_INDEX=0;plassere_INDEX<byte_COUNT;plassere_INDEX++)후보[plassere_INDEX]=명령후보[plassere_INDEX];후보[byte_COUNT]=' ';
    }
    static int 앞(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (명령해석기.linje[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int TILBAKE_VALUE(int 읽는자리) { if (읽는자리 < Storleik) { 읽는자리++; while (읽는자리 < Storleik && (명령해석기.linje[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int START_plassere, int mål_VALUE_INDEX) {
        int 글칸수 = 0;
        for (int Loop_INDEX = START_plassere; Loop_INDEX < mål_VALUE_INDEX; Loop_INDEX++) { int byte_data = 명령해석기.linje[Loop_INDEX]; if ((byte_data & 192) == 128) continue; 글칸수 += byte_data >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void 다시() {
        단말.Skriv("\r\u001b[2K");
        단말.Skriv(kommandoline ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 linje 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int COLUMNS = Tavle.Terminal(13) & 65535; return COLUMNS - (kommandoline ? 18 : 9); }
    static void 보이는줄() {
        if (markør_VALUE < START_vindauge) START_vindauge = markør_VALUE;
        while (폭(START_vindauge, markør_VALUE) > 보이는폭()) START_vindauge = TILBAKE_VALUE(START_vindauge);
        int avslutte_plassere = START_vindauge;
        while (avslutte_plassere < Storleik && 폭(START_vindauge, TILBAKE_VALUE(avslutte_plassere)) <= 보이는폭()) avslutte_plassere = TILBAKE_VALUE(avslutte_plassere);
        단말.Skriv("\r\u001b["); 단말.수(kommandoline ? 16 : 7); 단말.Skriv("G\u001b[K");
        if (START_vindauge > 0) 단말.문자('<');
        for (int Loop_INDEX = START_vindauge; Loop_INDEX < avslutte_plassere; Loop_INDEX++) Tavle.직렬쓰기(명령해석기.linje[Loop_INDEX]);
        단말.문자(avslutte_plassere < Storleik ? '>' : ' ');
        단말.Skriv("\u001b["); 단말.수(폭(markør_VALUE, avslutte_plassere) + 1); 단말.문자('D');
        가로보기 = START_vindauge > 0 || avslutte_plassere < Storleik || 폭(0, Storleik) > 보이는폭();
    }
    static void 기록넣기() {
        if (!kommandoline || Storleik == 0 || Storleik > 1024) return;
        if (LOG_COUNT > 0) {
            int 마지막자리 = (LOG_rad_avslutte + 15) % 16; boolean 같은여부 = LOG_lengd[마지막자리] == Storleik;
            for (int Loop_INDEX = 0; 같은여부 && Loop_INDEX < Storleik; Loop_INDEX++) if (LOG_rad[마지막자리 * 1024 + Loop_INDEX] != 명령해석기.linje[Loop_INDEX]) 같은여부 = false;
            if (같은여부) return;
        }
        LOG_lengd[LOG_rad_avslutte] = Storleik; for (int Loop_INDEX = 0; Loop_INDEX < Storleik; Loop_INDEX++) LOG_rad[LOG_rad_avslutte * 1024 + Loop_INDEX] = 명령해석기.linje[Loop_INDEX];
        LOG_rad_avslutte = (LOG_rad_avslutte + 1) % 16; if (LOG_COUNT < 16) LOG_COUNT++;
    }
    static void 기록이동(int DELTA_VALUE) {
        if (!kommandoline) return;
        if (Søk_VALUE == 0 && DELTA_VALUE > 0) { 저장길이 = Storleik; for (int Loop_INDEX = 0; Loop_INDEX < Storleik; Loop_INDEX++) Store_VALUE[Loop_INDEX] = 명령해석기.linje[Loop_INDEX]; }
        int Neste_plassere = Søk_VALUE + DELTA_VALUE; if (Neste_plassere < 0 || Neste_plassere > LOG_COUNT) return; Søk_VALUE = Neste_plassere;
        if (Søk_VALUE == 0) { Storleik = 저장길이; for (int Loop_INDEX = 0; Loop_INDEX < Storleik; Loop_INDEX++) 명령해석기.linje[Loop_INDEX] = Store_VALUE[Loop_INDEX]; }
        else { int 보관칸 = (LOG_rad_avslutte + 16 - Søk_VALUE) % 16; Storleik = LOG_lengd[보관칸]; for (int Loop_INDEX = 0; Loop_INDEX < Storleik; Loop_INDEX++) 명령해석기.linje[Loop_INDEX] = LOG_rad[보관칸 * 1024 + Loop_INDEX]; }
        markør_VALUE = Storleik; 다시();
    }
    static void vise_LOG() {
        for (int oppføring_COUNT = 0; oppføring_COUNT < LOG_COUNT; oppføring_COUNT++) {
            int 보관칸 = (LOG_rad_avslutte + 16 - LOG_COUNT + oppføring_COUNT) % 16; 단말.수(oppføring_COUNT + 1); 단말.Skriv("  ");
            for (int Loop_INDEX = 0; Loop_INDEX < LOG_lengd[보관칸]; Loop_INDEX++) Tavle.직렬쓰기(LOG_rad[보관칸 * 1024 + Loop_INDEX]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] data_ARRAY, int START_plassere, int oppføring_COUNT, int 접두말, int 총수, boolean 폴더번호) {
        if (oppføring_COUNT < 총수 || oppføring_COUNT > 62) return;
        for (int Loop_INDEX = 0; Loop_INDEX < 총수; Loop_INDEX++) if (data_ARRAY[START_plassere + Loop_INDEX] != 명령해석기.linje[접두말 + Loop_INDEX]) return;
        후보수++; 후보길이 = oppføring_COUNT + 1;
        for (int Loop_INDEX = 0; Loop_INDEX < oppføring_COUNT; Loop_INDEX++) 후보[Loop_INDEX] = data_ARRAY[START_plassere + Loop_INDEX]; 후보[oppføring_COUNT] = 폴더번호 ? '/' : ' ';
    }
    static void 완성() {
        if (!kommandoline || markør_VALUE != Storleik) return;
        int 시작점 = Storleik; while (시작점 > 0 && 명령해석기.linje[시작점 - 1] != ' ') 시작점--;
        for (int Loop_INDEX = 시작점; Loop_INDEX < Storleik; Loop_INDEX++) if (명령해석기.linje[Loop_INDEX] == '/' || 명령해석기.linje[Loop_INDEX] == '"' || 명령해석기.linje[Loop_INDEX] == 39 || 명령해석기.linje[Loop_INDEX] == '\\') return;
        후보수 = 0; int oppføring_COUNT = Storleik - 시작점;
        if (시작점 == 0) {
            for(int Liste_INDEX=0;Liste_INDEX<2;Liste_INDEX++) {
                String oppføring_Liste=Liste_INDEX==0?명령들:관리명령.완성어();
                int 읽는자리=0;
                while(읽는자리<oppføring_Liste.length()) {
                    int avslutte_plassere=읽는자리;while(avslutte_plassere<oppføring_Liste.length() && oppføring_Liste.charAt(avslutte_plassere)!=' ')avslutte_plassere++;
                    명령후보넣기(oppføring_Liste,읽는자리,avslutte_plassere,oppføring_COUNT);읽는자리=avslutte_plassere+1;
                }
            }
        } else {
            Minne_Filer.bane_START(1); Minne_Filer.bane_byte(0, '.'); Minne_Filer.normalisere_VALUE();
            for (int Loop_INDEX = 0; Loop_INDEX < Minne_Filer.fil_COUNT; Loop_INDEX++) {
                int START_plassere = Minne_Filer.oppføring_START(Minne_Filer.Namn, Loop_INDEX * 64, Minne_Filer.이름길이[Loop_INDEX]);
                if (START_plassere >= 0) 후보넣기(Minne_Filer.Namn, Loop_INDEX * 64 + START_plassere, Minne_Filer.이름길이[Loop_INDEX] - START_plassere, 시작점, oppføring_COUNT, false);
            }
            for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
                int START_plassere = Minne_Filer.oppføring_START(Minne_Filer.katalog_namn, Loop_INDEX * 64, Minne_Filer.katalog_lengd[Loop_INDEX]);
                if (START_plassere >= 0) 후보넣기(Minne_Filer.katalog_namn, Loop_INDEX * 64 + START_plassere, Minne_Filer.katalog_lengd[Loop_INDEX] - START_plassere, 시작점, oppføring_COUNT, true);
            }
        }
        if (후보수 != 1) { Tavle.직렬쓰기(7); return; }
        for (int Loop_INDEX = oppføring_COUNT; Loop_INDEX < 후보길이 && Storleik < 명령해석기.linje.length - 1; Loop_INDEX++) {
            if (후보[Loop_INDEX] == ' ' && Loop_INDEX != 후보길이 - 1) 명령해석기.linje[Storleik++] = '\\';
            명령해석기.linje[Storleik++] = 후보[Loop_INDEX];
        }
        markør_VALUE = Storleik; 다시();
    }
    static int 탈출읽기() {
        int 시작점 = Tavle.밀리초();
        while (Tavle.밀리초() - 시작점 < 80) { int byte_data = Tavle.직렬읽기(); if (byte_data >= 0) return byte_data; Tavle.YIELD_CPU(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int oppføring_COUNT = 0, avslutte_plassere = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 12; Loop_INDEX++) { int byte_data = 탈출읽기(); if (byte_data < 0) return; if (byte_data >= '0' && byte_data <= '9') oppføring_COUNT = oppføring_COUNT * 10 + byte_data - '0'; else { avslutte_plassere = byte_data; break; } }
        if (avslutte_plassere == 'A') 기록이동(1);
        else if (avslutte_plassere == 'B') 기록이동(-1);
        else if (avslutte_plassere == 'C') { markør_VALUE = TILBAKE_VALUE(markør_VALUE); 다시(); }
        else if (avslutte_plassere == 'D') { markør_VALUE = 앞(markør_VALUE); 다시(); }
        else if (avslutte_plassere == 'H' || avslutte_plassere == '~' && (oppføring_COUNT == 1 || oppføring_COUNT == 7)) { markør_VALUE = 0; 다시(); }
        else if (avslutte_plassere == 'F' || avslutte_plassere == '~' && (oppføring_COUNT == 4 || oppføring_COUNT == 8)) { markør_VALUE = Storleik; 다시(); }
        else if (avslutte_plassere == '~' && oppføring_COUNT == 3 && markør_VALUE < Storleik) {
            int Neste_plassere = TILBAKE_VALUE(markør_VALUE); for (int Loop_INDEX = Neste_plassere; Loop_INDEX < Storleik; Loop_INDEX++) 명령해석기.linje[Loop_INDEX - Neste_plassere + markør_VALUE] = 명령해석기.linje[Loop_INDEX]; Storleik -= Neste_plassere - markør_VALUE; 다시();
        }
        else if (avslutte_plassere == '~' && (oppføring_COUNT == 5 || oppføring_COUNT == 6)) Tavle.Terminal(oppføring_COUNT == 5 ? 5 : 6);
        else if (avslutte_plassere == '~' && oppføring_COUNT == 24 && kommandoline) { 명령해석기.Terminal(true); }
    }
    static int Les() {
        if (!vindauge_økt.이어읽기) { Storleik = markør_VALUE = Søk_VALUE = START_vindauge = 0; 가로보기 = false; }
        else { vindauge_økt.이어읽기 = false; 다시(); } boolean overflyt = false;
        while (true) {
            int byte_data = Tavle.직렬읽기(); if (byte_data == -4096) return -3;
            if (Tavle.Terminal(14) != 0) 다시(); if (byte_data < 0) { Tavle.YIELD_CPU(); continue; }
            if (byte_data == 10 && 명령해석기.앞줄) { 명령해석기.앞줄 = false; continue; } 명령해석기.앞줄 = byte_data == 13;
            if (byte_data == 27) { 탈출(); continue; }
            if (byte_data == 3) { 단말.Skriv("^C\n"); return -1; }
            if (byte_data == 4 && Storleik == 0 && kommandoline) { if (Tavle.Terminal(2) != 0) 명령해석기.Terminal(true); return -1; }
            if (byte_data == 13 || byte_data == 10) { 단말.문자(10); if (!overflyt) 기록넣기(); return overflyt ? -2 : Storleik; }
            if (byte_data == 9 && kommandoline) { 완성(); continue; }
            if (byte_data == 1 || byte_data == 5) { markør_VALUE = byte_data == 1 ? 0 : Storleik; 다시(); continue; }
            if (byte_data == 8 || byte_data == 127 || byte_data == 21) {
                if (byte_data == 21) { for (int Loop_INDEX = markør_VALUE; Loop_INDEX < Storleik; Loop_INDEX++) 명령해석기.linje[Loop_INDEX - markør_VALUE] = 명령해석기.linje[Loop_INDEX]; Storleik -= markør_VALUE; markør_VALUE = 0; }
                else if (markør_VALUE > 0) { int 변경전 = 앞(markør_VALUE); for (int Loop_INDEX = markør_VALUE; Loop_INDEX < Storleik; Loop_INDEX++) 명령해석기.linje[Loop_INDEX - markør_VALUE + 변경전] = 명령해석기.linje[Loop_INDEX]; Storleik -= markør_VALUE - 변경전; markør_VALUE = 변경전; }
                다시(); continue;
            }
            if (byte_data == 11) { Storleik = markør_VALUE; 다시(); continue; }
            if (byte_data < 32 && byte_data != 9) continue;
            if (Storleik == 명령해석기.linje.length) { overflyt = true; continue; }
            for (int Loop_INDEX = Storleik; Loop_INDEX > markør_VALUE; Loop_INDEX--) 명령해석기.linje[Loop_INDEX] = 명령해석기.linje[Loop_INDEX - 1];
            명령해석기.linje[markør_VALUE++] = byte_data; Storleik++;
            if (markør_VALUE == Storleik && !가로보기 && 폭(0, Storleik) <= 보이는폭()) Tavle.직렬쓰기(byte_data);
            else if (markør_VALUE == Storleik) 보이는줄(); else 다시();
        }
    }
}
