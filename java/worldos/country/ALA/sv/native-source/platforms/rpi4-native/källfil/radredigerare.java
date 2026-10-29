// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 byte_värde 경계를 지키는 삽입/삭제, 방향키, kommando LOG_POST, Tab Slutfört_värde. */
public final class radredigerare {
    static boolean kommandorad;
    static int[] LOG_POST = new int[16 * 1024], LOG_längd = new int[16], Store_värde = new int[4096], kandidat = new int[64];
    static int LOG_ANTAL, LOG_POST_avsluta, SÖK_värde, 저장길이, Storlek, markör_värde_04ee3e20, kandidat_ANTAL, kandidat_längd, START_fönster;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd säker_Shell fjärr_visa run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] kommando_kandidat = new int[128];
    static void Lägg_till_kommando_kandidat(String post_ange, int START_placera, int avsluta_placera, int indata_längd) {
        int byte_ANTAL=0;
        for(int positionsindex=START_placera;positionsindex<avsluta_placera;positionsindex++) {
            int kodpunkt=post_ange.charAt(positionsindex);
            if(kodpunkt>=0xd800 && kodpunkt<=0xdbff && positionsindex+1<avsluta_placera)kodpunkt=0x10000+((kodpunkt-0xd800)<<10)+post_ange.charAt(++positionsindex)-0xdc00;
            int nummer=kodpunkt<128?1:kodpunkt<2048?2:kodpunkt<65536?3:4;
            if(byte_ANTAL+nummer>62)return;
            for(int SEKVENS_värde=nummer-1;SEKVENS_värde>=0;SEKVENS_värde--)kommando_kandidat[byte_ANTAL++]=nummer==1?kodpunkt:SEKVENS_värde==nummer-1?(nummer==2?0xc0:nummer==3?0xe0:0xf0)|(kodpunkt>>(6*SEKVENS_värde)):0x80|((kodpunkt>>(6*SEKVENS_värde))&63);
        }
        if(byte_ANTAL<indata_längd)return;
        for(int positionsindex=0;positionsindex<indata_längd;positionsindex++)if(kommando_kandidat[positionsindex]!=명령해석기.inmatningsrad[positionsindex])return;
        kandidat_ANTAL++;kandidat_längd=byte_ANTAL+1;
        for(int positionsindex=0;positionsindex<byte_ANTAL;positionsindex++)kandidat[positionsindex]=kommando_kandidat[positionsindex];kandidat[byte_ANTAL]=' ';
    }
    static int framåtvänd_värde(int läsa_markör) { if (läsa_markör > 0) { läsa_markör--; while (läsa_markör > 0 && (명령해석기.inmatningsrad[läsa_markör] & 192) == 128) läsa_markör--; } return läsa_markör; }
    static int BACK_värde(int läsa_markör) { if (läsa_markör < Storlek) { läsa_markör++; while (läsa_markör < Storlek && (명령해석기.inmatningsrad[läsa_markör] & 192) == 128) läsa_markör++; } return läsa_markör; }
    static int 폭(int START_placera, int mål_värde_INDEX) {
        int 글칸수 = 0;
        for (int Loop_INDEX = START_placera; Loop_INDEX < mål_värde_INDEX; Loop_INDEX++) { int byte_data = 명령해석기.inmatningsrad[Loop_INDEX]; if ((byte_data & 192) == 128) continue; 글칸수 += byte_data >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void försöka_igen_värde() {
        단말.Skriv("\r\u001b[2K");
        단말.Skriv(kommandorad ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 inmatningsrad 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int KOLUMNER = Tavla.kommandotolk(13) & 65535; return KOLUMNER - (kommandorad ? 18 : 9); }
    static void 보이는줄() {
        if (markör_värde_04ee3e20 < START_fönster) START_fönster = markör_värde_04ee3e20;
        while (폭(START_fönster, markör_värde_04ee3e20) > 보이는폭()) START_fönster = BACK_värde(START_fönster);
        int avsluta_placera = START_fönster;
        while (avsluta_placera < Storlek && 폭(START_fönster, BACK_värde(avsluta_placera)) <= 보이는폭()) avsluta_placera = BACK_värde(avsluta_placera);
        단말.Skriv("\r\u001b["); 단말.nummer(kommandorad ? 16 : 7); 단말.Skriv("G\u001b[K");
        if (START_fönster > 0) 단말.문자('<');
        for (int Loop_INDEX = START_fönster; Loop_INDEX < avsluta_placera; Loop_INDEX++) Tavla.직렬쓰기(명령해석기.inmatningsrad[Loop_INDEX]);
        단말.문자(avsluta_placera < Storlek ? '>' : ' ');
        단말.Skriv("\u001b["); 단말.nummer(폭(markör_värde_04ee3e20, avsluta_placera) + 1); 단말.문자('D');
        가로보기 = START_fönster > 0 || avsluta_placera < Storlek || 폭(0, Storlek) > 보이는폭();
    }
    static void Lägga_till_LOG() {
        if (!kommandorad || Storlek == 0 || Storlek > 1024) return;
        if (LOG_ANTAL > 0) {
            int 마지막자리 = (LOG_POST_avsluta + 15) % 16; boolean 같은여부 = LOG_längd[마지막자리] == Storlek;
            for (int Loop_INDEX = 0; 같은여부 && Loop_INDEX < Storlek; Loop_INDEX++) if (LOG_POST[마지막자리 * 1024 + Loop_INDEX] != 명령해석기.inmatningsrad[Loop_INDEX]) 같은여부 = false;
            if (같은여부) return;
        }
        LOG_längd[LOG_POST_avsluta] = Storlek; for (int Loop_INDEX = 0; Loop_INDEX < Storlek; Loop_INDEX++) LOG_POST[LOG_POST_avsluta * 1024 + Loop_INDEX] = 명령해석기.inmatningsrad[Loop_INDEX];
        LOG_POST_avsluta = (LOG_POST_avsluta + 1) % 16; if (LOG_ANTAL < 16) LOG_ANTAL++;
    }
    static void 기록이동(int DELTA_värde) {
        if (!kommandorad) return;
        if (SÖK_värde == 0 && DELTA_värde > 0) { 저장길이 = Storlek; for (int Loop_INDEX = 0; Loop_INDEX < Storlek; Loop_INDEX++) Store_värde[Loop_INDEX] = 명령해석기.inmatningsrad[Loop_INDEX]; }
        int Nästa_placera = SÖK_värde + DELTA_värde; if (Nästa_placera < 0 || Nästa_placera > LOG_ANTAL) return; SÖK_värde = Nästa_placera;
        if (SÖK_värde == 0) { Storlek = 저장길이; for (int Loop_INDEX = 0; Loop_INDEX < Storlek; Loop_INDEX++) 명령해석기.inmatningsrad[Loop_INDEX] = Store_värde[Loop_INDEX]; }
        else { int 보관칸 = (LOG_POST_avsluta + 16 - SÖK_värde) % 16; Storlek = LOG_längd[보관칸]; for (int Loop_INDEX = 0; Loop_INDEX < Storlek; Loop_INDEX++) 명령해석기.inmatningsrad[Loop_INDEX] = LOG_POST[보관칸 * 1024 + Loop_INDEX]; }
        markör_värde_04ee3e20 = Storlek; försöka_igen_värde();
    }
    static void visa_LOG() {
        for (int post_ANTAL = 0; post_ANTAL < LOG_ANTAL; post_ANTAL++) {
            int 보관칸 = (LOG_POST_avsluta + 16 - LOG_ANTAL + post_ANTAL) % 16; 단말.nummer(post_ANTAL + 1); 단말.Skriv("  ");
            for (int Loop_INDEX = 0; Loop_INDEX < LOG_längd[보관칸]; Loop_INDEX++) Tavla.직렬쓰기(LOG_POST[보관칸 * 1024 + Loop_INDEX]); 단말.문자(10);
        }
    }
    static void Lägg_till_kandidat(int[] data_MATRIS, int START_placera, int post_ANTAL, int 접두말, int summa_ANTAL, boolean Katalog_nummer) {
        if (post_ANTAL < summa_ANTAL || post_ANTAL > 62) return;
        for (int Loop_INDEX = 0; Loop_INDEX < summa_ANTAL; Loop_INDEX++) if (data_MATRIS[START_placera + Loop_INDEX] != 명령해석기.inmatningsrad[접두말 + Loop_INDEX]) return;
        kandidat_ANTAL++; kandidat_längd = post_ANTAL + 1;
        for (int Loop_INDEX = 0; Loop_INDEX < post_ANTAL; Loop_INDEX++) kandidat[Loop_INDEX] = data_MATRIS[START_placera + Loop_INDEX]; kandidat[post_ANTAL] = Katalog_nummer ? '/' : ' ';
    }
    static void Slutfört_värde() {
        if (!kommandorad || markör_värde_04ee3e20 != Storlek) return;
        int 시작점 = Storlek; while (시작점 > 0 && 명령해석기.inmatningsrad[시작점 - 1] != ' ') 시작점--;
        for (int Loop_INDEX = 시작점; Loop_INDEX < Storlek; Loop_INDEX++) if (명령해석기.inmatningsrad[Loop_INDEX] == '/' || 명령해석기.inmatningsrad[Loop_INDEX] == '"' || 명령해석기.inmatningsrad[Loop_INDEX] == 39 || 명령해석기.inmatningsrad[Loop_INDEX] == '\\') return;
        kandidat_ANTAL = 0; int post_ANTAL = Storlek - 시작점;
        if (시작점 == 0) {
            for(int listindex=0;listindex<2;listindex++) {
                String post_ange=listindex==0?명령들:관리명령.Slutfört_Ord();
                int läsa_markör=0;
                while(läsa_markör<post_ange.length()) {
                    int avsluta_placera=läsa_markör;while(avsluta_placera<post_ange.length() && post_ange.charAt(avsluta_placera)!=' ')avsluta_placera++;
                    Lägg_till_kommando_kandidat(post_ange,läsa_markör,avsluta_placera,post_ANTAL);läsa_markör=avsluta_placera+1;
                }
            }
        } else {
            Minne_Filer.väg_START(1); Minne_Filer.väg_byte(0, '.'); Minne_Filer.normalisera_värde();
            for (int Loop_INDEX = 0; Loop_INDEX < Minne_Filer.fil_ANTAL; Loop_INDEX++) {
                int START_placera = Minne_Filer.post_START(Minne_Filer.Namn, Loop_INDEX * 64, Minne_Filer.이름길이[Loop_INDEX]);
                if (START_placera >= 0) Lägg_till_kandidat(Minne_Filer.Namn, Loop_INDEX * 64 + START_placera, Minne_Filer.이름길이[Loop_INDEX] - START_placera, 시작점, post_ANTAL, false);
            }
            for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
                int START_placera = Minne_Filer.post_START(Minne_Filer.Katalog_namn, Loop_INDEX * 64, Minne_Filer.Katalog_längd[Loop_INDEX]);
                if (START_placera >= 0) Lägg_till_kandidat(Minne_Filer.Katalog_namn, Loop_INDEX * 64 + START_placera, Minne_Filer.Katalog_längd[Loop_INDEX] - START_placera, 시작점, post_ANTAL, true);
            }
        }
        if (kandidat_ANTAL != 1) { Tavla.직렬쓰기(7); return; }
        for (int Loop_INDEX = post_ANTAL; Loop_INDEX < kandidat_längd && Storlek < 명령해석기.inmatningsrad.length - 1; Loop_INDEX++) {
            if (kandidat[Loop_INDEX] == ' ' && Loop_INDEX != kandidat_längd - 1) 명령해석기.inmatningsrad[Storlek++] = '\\';
            명령해석기.inmatningsrad[Storlek++] = kandidat[Loop_INDEX];
        }
        markör_värde_04ee3e20 = Storlek; försöka_igen_värde();
    }
    static int 탈출읽기() {
        int 시작점 = Tavla.밀리초();
        while (Tavla.밀리초() - 시작점 < 80) { int byte_data = Tavla.직렬읽기(); if (byte_data >= 0) return byte_data; Tavla.NOMAVK_CPU(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int post_ANTAL = 0, avsluta_placera = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 12; Loop_INDEX++) { int byte_data = 탈출읽기(); if (byte_data < 0) return; if (byte_data >= '0' && byte_data <= '9') post_ANTAL = post_ANTAL * 10 + byte_data - '0'; else { avsluta_placera = byte_data; break; } }
        if (avsluta_placera == 'A') 기록이동(1);
        else if (avsluta_placera == 'B') 기록이동(-1);
        else if (avsluta_placera == 'C') { markör_värde_04ee3e20 = BACK_värde(markör_värde_04ee3e20); försöka_igen_värde(); }
        else if (avsluta_placera == 'D') { markör_värde_04ee3e20 = framåtvänd_värde(markör_värde_04ee3e20); försöka_igen_värde(); }
        else if (avsluta_placera == 'H' || avsluta_placera == '~' && (post_ANTAL == 1 || post_ANTAL == 7)) { markör_värde_04ee3e20 = 0; försöka_igen_värde(); }
        else if (avsluta_placera == 'F' || avsluta_placera == '~' && (post_ANTAL == 4 || post_ANTAL == 8)) { markör_värde_04ee3e20 = Storlek; försöka_igen_värde(); }
        else if (avsluta_placera == '~' && post_ANTAL == 3 && markör_värde_04ee3e20 < Storlek) {
            int Nästa_placera = BACK_värde(markör_värde_04ee3e20); for (int Loop_INDEX = Nästa_placera; Loop_INDEX < Storlek; Loop_INDEX++) 명령해석기.inmatningsrad[Loop_INDEX - Nästa_placera + markör_värde_04ee3e20] = 명령해석기.inmatningsrad[Loop_INDEX]; Storlek -= Nästa_placera - markör_värde_04ee3e20; försöka_igen_värde();
        }
        else if (avsluta_placera == '~' && (post_ANTAL == 5 || post_ANTAL == 6)) Tavla.kommandotolk(post_ANTAL == 5 ? 5 : 6);
        else if (avsluta_placera == '~' && post_ANTAL == 24 && kommandorad) { 명령해석기.kommandotolk(true); }
    }
    static int Läs() {
        if (!fönster_session.이어읽기) { Storlek = markör_värde_04ee3e20 = SÖK_värde = START_fönster = 0; 가로보기 = false; }
        else { fönster_session.이어읽기 = false; försöka_igen_värde(); } boolean spill = false;
        while (true) {
            int byte_data = Tavla.직렬읽기(); if (byte_data == -4096) return -3;
            if (Tavla.kommandotolk(14) != 0) försöka_igen_värde(); if (byte_data < 0) { Tavla.NOMAVK_CPU(); continue; }
            if (byte_data == 10 && 명령해석기.Föregående_rad) { 명령해석기.Föregående_rad = false; continue; } 명령해석기.Föregående_rad = byte_data == 13;
            if (byte_data == 27) { 탈출(); continue; }
            if (byte_data == 3) { 단말.Skriv("^C\n"); return -1; }
            if (byte_data == 4 && Storlek == 0 && kommandorad) { if (Tavla.kommandotolk(2) != 0) 명령해석기.kommandotolk(true); return -1; }
            if (byte_data == 13 || byte_data == 10) { 단말.문자(10); if (!spill) Lägga_till_LOG(); return spill ? -2 : Storlek; }
            if (byte_data == 9 && kommandorad) { Slutfört_värde(); continue; }
            if (byte_data == 1 || byte_data == 5) { markör_värde_04ee3e20 = byte_data == 1 ? 0 : Storlek; försöka_igen_värde(); continue; }
            if (byte_data == 8 || byte_data == 127 || byte_data == 21) {
                if (byte_data == 21) { for (int Loop_INDEX = markör_värde_04ee3e20; Loop_INDEX < Storlek; Loop_INDEX++) 명령해석기.inmatningsrad[Loop_INDEX - markör_värde_04ee3e20] = 명령해석기.inmatningsrad[Loop_INDEX]; Storlek -= markör_värde_04ee3e20; markör_värde_04ee3e20 = 0; }
                else if (markör_värde_04ee3e20 > 0) { int 변경전 = framåtvänd_värde(markör_värde_04ee3e20); for (int Loop_INDEX = markör_värde_04ee3e20; Loop_INDEX < Storlek; Loop_INDEX++) 명령해석기.inmatningsrad[Loop_INDEX - markör_värde_04ee3e20 + 변경전] = 명령해석기.inmatningsrad[Loop_INDEX]; Storlek -= markör_värde_04ee3e20 - 변경전; markör_värde_04ee3e20 = 변경전; }
                försöka_igen_värde(); continue;
            }
            if (byte_data == 11) { Storlek = markör_värde_04ee3e20; försöka_igen_värde(); continue; }
            if (byte_data < 32 && byte_data != 9) continue;
            if (Storlek == 명령해석기.inmatningsrad.length) { spill = true; continue; }
            for (int Loop_INDEX = Storlek; Loop_INDEX > markör_värde_04ee3e20; Loop_INDEX--) 명령해석기.inmatningsrad[Loop_INDEX] = 명령해석기.inmatningsrad[Loop_INDEX - 1];
            명령해석기.inmatningsrad[markör_värde_04ee3e20++] = byte_data; Storlek++;
            if (markör_värde_04ee3e20 == Storlek && !가로보기 && 폭(0, Storlek) <= 보이는폭()) Tavla.직렬쓰기(byte_data);
            else if (markör_värde_04ee3e20 == Storlek) 보이는줄(); else försöka_igen_värde();
        }
    }
}
