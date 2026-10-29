// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 byte_VERDI 경계를 지키는 삽입/삭제, 방향키, Kommando LOG_POST, Tab Fullført_VERDI. */
public final class linje_Redaktør {
    static boolean kommandolinje;
    static int[] LOG_POST = new int[16 * 1024], LOG_lengde = new int[16], Store_VERDI = new int[4096], 후보 = new int[64];
    static int LOG_ANTALL, LOG_POST_avslutte_en_samtale, SØK_VERDI, 저장길이, Størrelse, markør_VERDI, 후보수, 후보길이, START_vindu;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd sikker_Shell ekstern_vise run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String oppføring_Liste, int START_plassere, int avslutte_en_samtale_plassere, int inndata_lengde) {
        int byte_ANTALL=0;
        for(int posisjonsindeks=START_plassere;posisjonsindeks<avslutte_en_samtale_plassere;posisjonsindeks++) {
            int tegnkode=oppføring_Liste.charAt(posisjonsindeks);
            if(tegnkode>=0xd800 && tegnkode<=0xdbff && posisjonsindeks+1<avslutte_en_samtale_plassere)tegnkode=0x10000+((tegnkode-0xd800)<<10)+oppføring_Liste.charAt(++posisjonsindeks)-0xdc00;
            int nummer=tegnkode<128?1:tegnkode<2048?2:tegnkode<65536?3:4;
            if(byte_ANTALL+nummer>62)return;
            for(int SEKVENS_VERDI=nummer-1;SEKVENS_VERDI>=0;SEKVENS_VERDI--)명령후보[byte_ANTALL++]=nummer==1?tegnkode:SEKVENS_VERDI==nummer-1?(nummer==2?0xc0:nummer==3?0xe0:0xf0)|(tegnkode>>(6*SEKVENS_VERDI)):0x80|((tegnkode>>(6*SEKVENS_VERDI))&63);
        }
        if(byte_ANTALL<inndata_lengde)return;
        for(int posisjonsindeks=0;posisjonsindeks<inndata_lengde;posisjonsindeks++)if(명령후보[posisjonsindeks]!=명령해석기.Linje[posisjonsindeks])return;
        후보수++;후보길이=byte_ANTALL+1;
        for(int posisjonsindeks=0;posisjonsindeks<byte_ANTALL;posisjonsindeks++)후보[posisjonsindeks]=명령후보[posisjonsindeks];후보[byte_ANTALL]=' ';
    }
    static int frontkamera_VERDI(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (명령해석기.Linje[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int TILBAKE_VERDI(int 읽는자리) { if (읽는자리 < Størrelse) { 읽는자리++; while (읽는자리 < Størrelse && (명령해석기.Linje[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int START_plassere, int mål_VERDI_INDEKS) {
        int 글칸수 = 0;
        for (int Loop_INDEKS = START_plassere; Loop_INDEKS < mål_VERDI_INDEKS; Loop_INDEKS++) { int byte_data = 명령해석기.Linje[Loop_INDEKS]; if ((byte_data & 192) == 128) continue; 글칸수 += byte_data >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void prøve_på_nytt_VERDI() {
        단말.Skriv("\r\u001b[2K");
        단말.Skriv(kommandolinje ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 Linje 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int KOLONNER = Tavle.Terminal(13) & 65535; return KOLONNER - (kommandolinje ? 18 : 9); }
    static void 보이는줄() {
        if (markør_VERDI < START_vindu) START_vindu = markør_VERDI;
        while (폭(START_vindu, markør_VERDI) > 보이는폭()) START_vindu = TILBAKE_VERDI(START_vindu);
        int avslutte_en_samtale_plassere = START_vindu;
        while (avslutte_en_samtale_plassere < Størrelse && 폭(START_vindu, TILBAKE_VERDI(avslutte_en_samtale_plassere)) <= 보이는폭()) avslutte_en_samtale_plassere = TILBAKE_VERDI(avslutte_en_samtale_plassere);
        단말.Skriv("\r\u001b["); 단말.nummer(kommandolinje ? 16 : 7); 단말.Skriv("G\u001b[K");
        if (START_vindu > 0) 단말.문자('<');
        for (int Loop_INDEKS = START_vindu; Loop_INDEKS < avslutte_en_samtale_plassere; Loop_INDEKS++) Tavle.직렬쓰기(명령해석기.Linje[Loop_INDEKS]);
        단말.문자(avslutte_en_samtale_plassere < Størrelse ? '>' : ' ');
        단말.Skriv("\u001b["); 단말.nummer(폭(markør_VERDI, avslutte_en_samtale_plassere) + 1); 단말.문자('D');
        가로보기 = START_vindu > 0 || avslutte_en_samtale_plassere < Størrelse || 폭(0, Størrelse) > 보이는폭();
    }
    static void Tilføye_LOG() {
        if (!kommandolinje || Størrelse == 0 || Størrelse > 1024) return;
        if (LOG_ANTALL > 0) {
            int 마지막자리 = (LOG_POST_avslutte_en_samtale + 15) % 16; boolean 같은여부 = LOG_lengde[마지막자리] == Størrelse;
            for (int Loop_INDEKS = 0; 같은여부 && Loop_INDEKS < Størrelse; Loop_INDEKS++) if (LOG_POST[마지막자리 * 1024 + Loop_INDEKS] != 명령해석기.Linje[Loop_INDEKS]) 같은여부 = false;
            if (같은여부) return;
        }
        LOG_lengde[LOG_POST_avslutte_en_samtale] = Størrelse; for (int Loop_INDEKS = 0; Loop_INDEKS < Størrelse; Loop_INDEKS++) LOG_POST[LOG_POST_avslutte_en_samtale * 1024 + Loop_INDEKS] = 명령해석기.Linje[Loop_INDEKS];
        LOG_POST_avslutte_en_samtale = (LOG_POST_avslutte_en_samtale + 1) % 16; if (LOG_ANTALL < 16) LOG_ANTALL++;
    }
    static void 기록이동(int DELTA_VERDI) {
        if (!kommandolinje) return;
        if (SØK_VERDI == 0 && DELTA_VERDI > 0) { 저장길이 = Størrelse; for (int Loop_INDEKS = 0; Loop_INDEKS < Størrelse; Loop_INDEKS++) Store_VERDI[Loop_INDEKS] = 명령해석기.Linje[Loop_INDEKS]; }
        int Neste_plassere = SØK_VERDI + DELTA_VERDI; if (Neste_plassere < 0 || Neste_plassere > LOG_ANTALL) return; SØK_VERDI = Neste_plassere;
        if (SØK_VERDI == 0) { Størrelse = 저장길이; for (int Loop_INDEKS = 0; Loop_INDEKS < Størrelse; Loop_INDEKS++) 명령해석기.Linje[Loop_INDEKS] = Store_VERDI[Loop_INDEKS]; }
        else { int 보관칸 = (LOG_POST_avslutte_en_samtale + 16 - SØK_VERDI) % 16; Størrelse = LOG_lengde[보관칸]; for (int Loop_INDEKS = 0; Loop_INDEKS < Størrelse; Loop_INDEKS++) 명령해석기.Linje[Loop_INDEKS] = LOG_POST[보관칸 * 1024 + Loop_INDEKS]; }
        markør_VERDI = Størrelse; prøve_på_nytt_VERDI();
    }
    static void vise_LOG() {
        for (int oppføring_ANTALL = 0; oppføring_ANTALL < LOG_ANTALL; oppføring_ANTALL++) {
            int 보관칸 = (LOG_POST_avslutte_en_samtale + 16 - LOG_ANTALL + oppføring_ANTALL) % 16; 단말.nummer(oppføring_ANTALL + 1); 단말.Skriv("  ");
            for (int Loop_INDEKS = 0; Loop_INDEKS < LOG_lengde[보관칸]; Loop_INDEKS++) Tavle.직렬쓰기(LOG_POST[보관칸 * 1024 + Loop_INDEKS]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] data_MATRISE, int START_plassere, int oppføring_ANTALL, int 접두말, int total_ANTALL, boolean katalog_nummer) {
        if (oppføring_ANTALL < total_ANTALL || oppføring_ANTALL > 62) return;
        for (int Loop_INDEKS = 0; Loop_INDEKS < total_ANTALL; Loop_INDEKS++) if (data_MATRISE[START_plassere + Loop_INDEKS] != 명령해석기.Linje[접두말 + Loop_INDEKS]) return;
        후보수++; 후보길이 = oppføring_ANTALL + 1;
        for (int Loop_INDEKS = 0; Loop_INDEKS < oppføring_ANTALL; Loop_INDEKS++) 후보[Loop_INDEKS] = data_MATRISE[START_plassere + Loop_INDEKS]; 후보[oppføring_ANTALL] = katalog_nummer ? '/' : ' ';
    }
    static void Fullført_VERDI() {
        if (!kommandolinje || markør_VERDI != Størrelse) return;
        int 시작점 = Størrelse; while (시작점 > 0 && 명령해석기.Linje[시작점 - 1] != ' ') 시작점--;
        for (int Loop_INDEKS = 시작점; Loop_INDEKS < Størrelse; Loop_INDEKS++) if (명령해석기.Linje[Loop_INDEKS] == '/' || 명령해석기.Linje[Loop_INDEKS] == '"' || 명령해석기.Linje[Loop_INDEKS] == 39 || 명령해석기.Linje[Loop_INDEKS] == '\\') return;
        후보수 = 0; int oppføring_ANTALL = Størrelse - 시작점;
        if (시작점 == 0) {
            for(int listeindeks=0;listeindeks<2;listeindeks++) {
                String oppføring_Liste=listeindeks==0?명령들:관리명령.Fullført_ord();
                int 읽는자리=0;
                while(읽는자리<oppføring_Liste.length()) {
                    int avslutte_en_samtale_plassere=읽는자리;while(avslutte_en_samtale_plassere<oppføring_Liste.length() && oppføring_Liste.charAt(avslutte_en_samtale_plassere)!=' ')avslutte_en_samtale_plassere++;
                    명령후보넣기(oppføring_Liste,읽는자리,avslutte_en_samtale_plassere,oppføring_ANTALL);읽는자리=avslutte_en_samtale_plassere+1;
                }
            }
        } else {
            Minne_Filer.bane_START(1); Minne_Filer.bane_byte(0, '.'); Minne_Filer.normalisere_VERDI();
            for (int Loop_INDEKS = 0; Loop_INDEKS < Minne_Filer.Fil_ANTALL; Loop_INDEKS++) {
                int START_plassere = Minne_Filer.oppføring_START(Minne_Filer.Navn, Loop_INDEKS * 64, Minne_Filer.이름길이[Loop_INDEKS]);
                if (START_plassere >= 0) 후보넣기(Minne_Filer.Navn, Loop_INDEKS * 64 + START_plassere, Minne_Filer.이름길이[Loop_INDEKS] - START_plassere, 시작점, oppføring_ANTALL, false);
            }
            for (int Loop_INDEKS = 0; Loop_INDEKS < 16; Loop_INDEKS++) {
                int START_plassere = Minne_Filer.oppføring_START(Minne_Filer.katalog_navn, Loop_INDEKS * 64, Minne_Filer.katalog_lengde[Loop_INDEKS]);
                if (START_plassere >= 0) 후보넣기(Minne_Filer.katalog_navn, Loop_INDEKS * 64 + START_plassere, Minne_Filer.katalog_lengde[Loop_INDEKS] - START_plassere, 시작점, oppføring_ANTALL, true);
            }
        }
        if (후보수 != 1) { Tavle.직렬쓰기(7); return; }
        for (int Loop_INDEKS = oppføring_ANTALL; Loop_INDEKS < 후보길이 && Størrelse < 명령해석기.Linje.length - 1; Loop_INDEKS++) {
            if (후보[Loop_INDEKS] == ' ' && Loop_INDEKS != 후보길이 - 1) 명령해석기.Linje[Størrelse++] = '\\';
            명령해석기.Linje[Størrelse++] = 후보[Loop_INDEKS];
        }
        markør_VERDI = Størrelse; prøve_på_nytt_VERDI();
    }
    static int 탈출읽기() {
        int 시작점 = Tavle.밀리초();
        while (Tavle.밀리초() - 시작점 < 80) { int byte_data = Tavle.직렬읽기(); if (byte_data >= 0) return byte_data; Tavle.AVKAST_CPU(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int oppføring_ANTALL = 0, avslutte_en_samtale_plassere = -1;
        for (int Loop_INDEKS = 0; Loop_INDEKS < 12; Loop_INDEKS++) { int byte_data = 탈출읽기(); if (byte_data < 0) return; if (byte_data >= '0' && byte_data <= '9') oppføring_ANTALL = oppføring_ANTALL * 10 + byte_data - '0'; else { avslutte_en_samtale_plassere = byte_data; break; } }
        if (avslutte_en_samtale_plassere == 'A') 기록이동(1);
        else if (avslutte_en_samtale_plassere == 'B') 기록이동(-1);
        else if (avslutte_en_samtale_plassere == 'C') { markør_VERDI = TILBAKE_VERDI(markør_VERDI); prøve_på_nytt_VERDI(); }
        else if (avslutte_en_samtale_plassere == 'D') { markør_VERDI = frontkamera_VERDI(markør_VERDI); prøve_på_nytt_VERDI(); }
        else if (avslutte_en_samtale_plassere == 'H' || avslutte_en_samtale_plassere == '~' && (oppføring_ANTALL == 1 || oppføring_ANTALL == 7)) { markør_VERDI = 0; prøve_på_nytt_VERDI(); }
        else if (avslutte_en_samtale_plassere == 'F' || avslutte_en_samtale_plassere == '~' && (oppføring_ANTALL == 4 || oppføring_ANTALL == 8)) { markør_VERDI = Størrelse; prøve_på_nytt_VERDI(); }
        else if (avslutte_en_samtale_plassere == '~' && oppføring_ANTALL == 3 && markør_VERDI < Størrelse) {
            int Neste_plassere = TILBAKE_VERDI(markør_VERDI); for (int Loop_INDEKS = Neste_plassere; Loop_INDEKS < Størrelse; Loop_INDEKS++) 명령해석기.Linje[Loop_INDEKS - Neste_plassere + markør_VERDI] = 명령해석기.Linje[Loop_INDEKS]; Størrelse -= Neste_plassere - markør_VERDI; prøve_på_nytt_VERDI();
        }
        else if (avslutte_en_samtale_plassere == '~' && (oppføring_ANTALL == 5 || oppføring_ANTALL == 6)) Tavle.Terminal(oppføring_ANTALL == 5 ? 5 : 6);
        else if (avslutte_en_samtale_plassere == '~' && oppføring_ANTALL == 24 && kommandolinje) { 명령해석기.Terminal(true); }
    }
    static int Les() {
        if (!vindu_økt.이어읽기) { Størrelse = markør_VERDI = SØK_VERDI = START_vindu = 0; 가로보기 = false; }
        else { vindu_økt.이어읽기 = false; prøve_på_nytt_VERDI(); } boolean overløp = false;
        while (true) {
            int byte_data = Tavle.직렬읽기(); if (byte_data == -4096) return -3;
            if (Tavle.Terminal(14) != 0) prøve_på_nytt_VERDI(); if (byte_data < 0) { Tavle.AVKAST_CPU(); continue; }
            if (byte_data == 10 && 명령해석기.Forrige_linje) { 명령해석기.Forrige_linje = false; continue; } 명령해석기.Forrige_linje = byte_data == 13;
            if (byte_data == 27) { 탈출(); continue; }
            if (byte_data == 3) { 단말.Skriv("^C\n"); return -1; }
            if (byte_data == 4 && Størrelse == 0 && kommandolinje) { if (Tavle.Terminal(2) != 0) 명령해석기.Terminal(true); return -1; }
            if (byte_data == 13 || byte_data == 10) { 단말.문자(10); if (!overløp) Tilføye_LOG(); return overløp ? -2 : Størrelse; }
            if (byte_data == 9 && kommandolinje) { Fullført_VERDI(); continue; }
            if (byte_data == 1 || byte_data == 5) { markør_VERDI = byte_data == 1 ? 0 : Størrelse; prøve_på_nytt_VERDI(); continue; }
            if (byte_data == 8 || byte_data == 127 || byte_data == 21) {
                if (byte_data == 21) { for (int Loop_INDEKS = markør_VERDI; Loop_INDEKS < Størrelse; Loop_INDEKS++) 명령해석기.Linje[Loop_INDEKS - markør_VERDI] = 명령해석기.Linje[Loop_INDEKS]; Størrelse -= markør_VERDI; markør_VERDI = 0; }
                else if (markør_VERDI > 0) { int 변경전 = frontkamera_VERDI(markør_VERDI); for (int Loop_INDEKS = markør_VERDI; Loop_INDEKS < Størrelse; Loop_INDEKS++) 명령해석기.Linje[Loop_INDEKS - markør_VERDI + 변경전] = 명령해석기.Linje[Loop_INDEKS]; Størrelse -= markør_VERDI - 변경전; markør_VERDI = 변경전; }
                prøve_på_nytt_VERDI(); continue;
            }
            if (byte_data == 11) { Størrelse = markør_VERDI; prøve_på_nytt_VERDI(); continue; }
            if (byte_data < 32 && byte_data != 9) continue;
            if (Størrelse == 명령해석기.Linje.length) { overløp = true; continue; }
            for (int Loop_INDEKS = Størrelse; Loop_INDEKS > markør_VERDI; Loop_INDEKS--) 명령해석기.Linje[Loop_INDEKS] = 명령해석기.Linje[Loop_INDEKS - 1];
            명령해석기.Linje[markør_VERDI++] = byte_data; Størrelse++;
            if (markør_VERDI == Størrelse && !가로보기 && 폭(0, Størrelse) <= 보이는폭()) Tavle.직렬쓰기(byte_data);
            else if (markør_VERDI == Størrelse) 보이는줄(); else prøve_på_nytt_VERDI();
        }
    }
}
