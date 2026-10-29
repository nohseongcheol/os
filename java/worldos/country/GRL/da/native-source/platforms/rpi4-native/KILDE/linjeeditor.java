// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 byte_VÆRDI 경계를 지키는 삽입/삭제, 방향키, Kommando LOG_post, Tab fuldført_VÆRDI. */
public final class linjeeditor {
    static boolean kommandolinje;
    static int[] LOG_post = new int[16 * 1024], LOG_varighed = new int[16], Store_VÆRDI = new int[4096], 후보 = new int[64];
    static int LOG_TÆL, LOG_post_afslutte_et_opkald, SØG_VÆRDI, 저장길이, Størrelse, markør_VÆRDI, 후보수, 후보길이, START_vindue;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd sikker_Shell fjern_vise run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String post_Liste, int START_placere, int afslutte_et_opkald_placere, int input_varighed) {
        int byte_TÆL=0;
        for(int positionsindeks=START_placere;positionsindeks<afslutte_et_opkald_placere;positionsindeks++) {
            int tegnkode=post_Liste.charAt(positionsindeks);
            if(tegnkode>=0xd800 && tegnkode<=0xdbff && positionsindeks+1<afslutte_et_opkald_placere)tegnkode=0x10000+((tegnkode-0xd800)<<10)+post_Liste.charAt(++positionsindeks)-0xdc00;
            int tal=tegnkode<128?1:tegnkode<2048?2:tegnkode<65536?3:4;
            if(byte_TÆL+tal>62)return;
            for(int SEKVENS_VÆRDI=tal-1;SEKVENS_VÆRDI>=0;SEKVENS_VÆRDI--)명령후보[byte_TÆL++]=tal==1?tegnkode:SEKVENS_VÆRDI==tal-1?(tal==2?0xc0:tal==3?0xe0:0xf0)|(tegnkode>>(6*SEKVENS_VÆRDI)):0x80|((tegnkode>>(6*SEKVENS_VÆRDI))&63);
        }
        if(byte_TÆL<input_varighed)return;
        for(int positionsindeks=0;positionsindeks<input_varighed;positionsindeks++)if(명령후보[positionsindeks]!=명령해석기.Linje[positionsindeks])return;
        후보수++;후보길이=byte_TÆL+1;
        for(int positionsindeks=0;positionsindeks<byte_TÆL;positionsindeks++)후보[positionsindeks]=명령후보[positionsindeks];후보[byte_TÆL]=' ';
    }
    static int frontvendt_VÆRDI(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (명령해석기.Linje[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int BACK_VÆRDI(int 읽는자리) { if (읽는자리 < Størrelse) { 읽는자리++; while (읽는자리 < Størrelse && (명령해석기.Linje[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int START_placere, int destination_VÆRDI_INDEKS) {
        int 글칸수 = 0;
        for (int Loop_INDEKS = START_placere; Loop_INDEKS < destination_VÆRDI_INDEKS; Loop_INDEKS++) { int byte_data = 명령해석기.Linje[Loop_INDEKS]; if ((byte_data & 192) == 128) continue; 글칸수 += byte_data >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void prøve_igen_VÆRDI() {
        단말.Skrive("\r\u001b[2K");
        단말.Skrive(kommandolinje ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 Linje 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int KOLONNER = Tavle.Terminal(13) & 65535; return KOLONNER - (kommandolinje ? 18 : 9); }
    static void 보이는줄() {
        if (markør_VÆRDI < START_vindue) START_vindue = markør_VÆRDI;
        while (폭(START_vindue, markør_VÆRDI) > 보이는폭()) START_vindue = BACK_VÆRDI(START_vindue);
        int afslutte_et_opkald_placere = START_vindue;
        while (afslutte_et_opkald_placere < Størrelse && 폭(START_vindue, BACK_VÆRDI(afslutte_et_opkald_placere)) <= 보이는폭()) afslutte_et_opkald_placere = BACK_VÆRDI(afslutte_et_opkald_placere);
        단말.Skrive("\r\u001b["); 단말.tal(kommandolinje ? 16 : 7); 단말.Skrive("G\u001b[K");
        if (START_vindue > 0) 단말.문자('<');
        for (int Loop_INDEKS = START_vindue; Loop_INDEKS < afslutte_et_opkald_placere; Loop_INDEKS++) Tavle.직렬쓰기(명령해석기.Linje[Loop_INDEKS]);
        단말.문자(afslutte_et_opkald_placere < Størrelse ? '>' : ' ');
        단말.Skrive("\u001b["); 단말.tal(폭(markør_VÆRDI, afslutte_et_opkald_placere) + 1); 단말.문자('D');
        가로보기 = START_vindue > 0 || afslutte_et_opkald_placere < Størrelse || 폭(0, Størrelse) > 보이는폭();
    }
    static void tilføj_LOG() {
        if (!kommandolinje || Størrelse == 0 || Størrelse > 1024) return;
        if (LOG_TÆL > 0) {
            int 마지막자리 = (LOG_post_afslutte_et_opkald + 15) % 16; boolean 같은여부 = LOG_varighed[마지막자리] == Størrelse;
            for (int Loop_INDEKS = 0; 같은여부 && Loop_INDEKS < Størrelse; Loop_INDEKS++) if (LOG_post[마지막자리 * 1024 + Loop_INDEKS] != 명령해석기.Linje[Loop_INDEKS]) 같은여부 = false;
            if (같은여부) return;
        }
        LOG_varighed[LOG_post_afslutte_et_opkald] = Størrelse; for (int Loop_INDEKS = 0; Loop_INDEKS < Størrelse; Loop_INDEKS++) LOG_post[LOG_post_afslutte_et_opkald * 1024 + Loop_INDEKS] = 명령해석기.Linje[Loop_INDEKS];
        LOG_post_afslutte_et_opkald = (LOG_post_afslutte_et_opkald + 1) % 16; if (LOG_TÆL < 16) LOG_TÆL++;
    }
    static void 기록이동(int DELTA_VÆRDI) {
        if (!kommandolinje) return;
        if (SØG_VÆRDI == 0 && DELTA_VÆRDI > 0) { 저장길이 = Størrelse; for (int Loop_INDEKS = 0; Loop_INDEKS < Størrelse; Loop_INDEKS++) Store_VÆRDI[Loop_INDEKS] = 명령해석기.Linje[Loop_INDEKS]; }
        int Næste_placere = SØG_VÆRDI + DELTA_VÆRDI; if (Næste_placere < 0 || Næste_placere > LOG_TÆL) return; SØG_VÆRDI = Næste_placere;
        if (SØG_VÆRDI == 0) { Størrelse = 저장길이; for (int Loop_INDEKS = 0; Loop_INDEKS < Størrelse; Loop_INDEKS++) 명령해석기.Linje[Loop_INDEKS] = Store_VÆRDI[Loop_INDEKS]; }
        else { int 보관칸 = (LOG_post_afslutte_et_opkald + 16 - SØG_VÆRDI) % 16; Størrelse = LOG_varighed[보관칸]; for (int Loop_INDEKS = 0; Loop_INDEKS < Størrelse; Loop_INDEKS++) 명령해석기.Linje[Loop_INDEKS] = LOG_post[보관칸 * 1024 + Loop_INDEKS]; }
        markør_VÆRDI = Størrelse; prøve_igen_VÆRDI();
    }
    static void vise_LOG() {
        for (int post_TÆL_8f7753a1 = 0; post_TÆL_8f7753a1 < LOG_TÆL; post_TÆL_8f7753a1++) {
            int 보관칸 = (LOG_post_afslutte_et_opkald + 16 - LOG_TÆL + post_TÆL_8f7753a1) % 16; 단말.tal(post_TÆL_8f7753a1 + 1); 단말.Skrive("  ");
            for (int Loop_INDEKS = 0; Loop_INDEKS < LOG_varighed[보관칸]; Loop_INDEKS++) Tavle.직렬쓰기(LOG_post[보관칸 * 1024 + Loop_INDEKS]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] data_MATRIX, int START_placere, int post_TÆL_8f7753a1, int 접두말, int i_alt_TÆL, boolean mappe_tal) {
        if (post_TÆL_8f7753a1 < i_alt_TÆL || post_TÆL_8f7753a1 > 62) return;
        for (int Loop_INDEKS = 0; Loop_INDEKS < i_alt_TÆL; Loop_INDEKS++) if (data_MATRIX[START_placere + Loop_INDEKS] != 명령해석기.Linje[접두말 + Loop_INDEKS]) return;
        후보수++; 후보길이 = post_TÆL_8f7753a1 + 1;
        for (int Loop_INDEKS = 0; Loop_INDEKS < post_TÆL_8f7753a1; Loop_INDEKS++) 후보[Loop_INDEKS] = data_MATRIX[START_placere + Loop_INDEKS]; 후보[post_TÆL_8f7753a1] = mappe_tal ? '/' : ' ';
    }
    static void fuldført_VÆRDI() {
        if (!kommandolinje || markør_VÆRDI != Størrelse) return;
        int 시작점 = Størrelse; while (시작점 > 0 && 명령해석기.Linje[시작점 - 1] != ' ') 시작점--;
        for (int Loop_INDEKS = 시작점; Loop_INDEKS < Størrelse; Loop_INDEKS++) if (명령해석기.Linje[Loop_INDEKS] == '/' || 명령해석기.Linje[Loop_INDEKS] == '"' || 명령해석기.Linje[Loop_INDEKS] == 39 || 명령해석기.Linje[Loop_INDEKS] == '\\') return;
        후보수 = 0; int post_TÆL_8f7753a1 = Størrelse - 시작점;
        if (시작점 == 0) {
            for(int listeindeks=0;listeindeks<2;listeindeks++) {
                String post_Liste=listeindeks==0?명령들:관리명령.fuldført_Ord();
                int 읽는자리=0;
                while(읽는자리<post_Liste.length()) {
                    int afslutte_et_opkald_placere=읽는자리;while(afslutte_et_opkald_placere<post_Liste.length() && post_Liste.charAt(afslutte_et_opkald_placere)!=' ')afslutte_et_opkald_placere++;
                    명령후보넣기(post_Liste,읽는자리,afslutte_et_opkald_placere,post_TÆL_8f7753a1);읽는자리=afslutte_et_opkald_placere+1;
                }
            }
        } else {
            Hukommelse_Filer.sti_START(1); Hukommelse_Filer.sti_byte(0, '.'); Hukommelse_Filer.normalisere_VÆRDI();
            for (int Loop_INDEKS = 0; Loop_INDEKS < Hukommelse_Filer.fil_TÆL; Loop_INDEKS++) {
                int START_placere = Hukommelse_Filer.post_START(Hukommelse_Filer.Navn, Loop_INDEKS * 64, Hukommelse_Filer.이름길이[Loop_INDEKS]);
                if (START_placere >= 0) 후보넣기(Hukommelse_Filer.Navn, Loop_INDEKS * 64 + START_placere, Hukommelse_Filer.이름길이[Loop_INDEKS] - START_placere, 시작점, post_TÆL_8f7753a1, false);
            }
            for (int Loop_INDEKS = 0; Loop_INDEKS < 16; Loop_INDEKS++) {
                int START_placere = Hukommelse_Filer.post_START(Hukommelse_Filer.mappe_navn, Loop_INDEKS * 64, Hukommelse_Filer.mappe_varighed[Loop_INDEKS]);
                if (START_placere >= 0) 후보넣기(Hukommelse_Filer.mappe_navn, Loop_INDEKS * 64 + START_placere, Hukommelse_Filer.mappe_varighed[Loop_INDEKS] - START_placere, 시작점, post_TÆL_8f7753a1, true);
            }
        }
        if (후보수 != 1) { Tavle.직렬쓰기(7); return; }
        for (int Loop_INDEKS = post_TÆL_8f7753a1; Loop_INDEKS < 후보길이 && Størrelse < 명령해석기.Linje.length - 1; Loop_INDEKS++) {
            if (후보[Loop_INDEKS] == ' ' && Loop_INDEKS != 후보길이 - 1) 명령해석기.Linje[Størrelse++] = '\\';
            명령해석기.Linje[Størrelse++] = 후보[Loop_INDEKS];
        }
        markør_VÆRDI = Størrelse; prøve_igen_VÆRDI();
    }
    static int 탈출읽기() {
        int 시작점 = Tavle.밀리초();
        while (Tavle.밀리초() - 시작점 < 80) { int byte_data = Tavle.직렬읽기(); if (byte_data >= 0) return byte_data; Tavle.AFKAST_CPU(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int post_TÆL_8f7753a1 = 0, afslutte_et_opkald_placere = -1;
        for (int Loop_INDEKS = 0; Loop_INDEKS < 12; Loop_INDEKS++) { int byte_data = 탈출읽기(); if (byte_data < 0) return; if (byte_data >= '0' && byte_data <= '9') post_TÆL_8f7753a1 = post_TÆL_8f7753a1 * 10 + byte_data - '0'; else { afslutte_et_opkald_placere = byte_data; break; } }
        if (afslutte_et_opkald_placere == 'A') 기록이동(1);
        else if (afslutte_et_opkald_placere == 'B') 기록이동(-1);
        else if (afslutte_et_opkald_placere == 'C') { markør_VÆRDI = BACK_VÆRDI(markør_VÆRDI); prøve_igen_VÆRDI(); }
        else if (afslutte_et_opkald_placere == 'D') { markør_VÆRDI = frontvendt_VÆRDI(markør_VÆRDI); prøve_igen_VÆRDI(); }
        else if (afslutte_et_opkald_placere == 'H' || afslutte_et_opkald_placere == '~' && (post_TÆL_8f7753a1 == 1 || post_TÆL_8f7753a1 == 7)) { markør_VÆRDI = 0; prøve_igen_VÆRDI(); }
        else if (afslutte_et_opkald_placere == 'F' || afslutte_et_opkald_placere == '~' && (post_TÆL_8f7753a1 == 4 || post_TÆL_8f7753a1 == 8)) { markør_VÆRDI = Størrelse; prøve_igen_VÆRDI(); }
        else if (afslutte_et_opkald_placere == '~' && post_TÆL_8f7753a1 == 3 && markør_VÆRDI < Størrelse) {
            int Næste_placere = BACK_VÆRDI(markør_VÆRDI); for (int Loop_INDEKS = Næste_placere; Loop_INDEKS < Størrelse; Loop_INDEKS++) 명령해석기.Linje[Loop_INDEKS - Næste_placere + markør_VÆRDI] = 명령해석기.Linje[Loop_INDEKS]; Størrelse -= Næste_placere - markør_VÆRDI; prøve_igen_VÆRDI();
        }
        else if (afslutte_et_opkald_placere == '~' && (post_TÆL_8f7753a1 == 5 || post_TÆL_8f7753a1 == 6)) Tavle.Terminal(post_TÆL_8f7753a1 == 5 ? 5 : 6);
        else if (afslutte_et_opkald_placere == '~' && post_TÆL_8f7753a1 == 24 && kommandolinje) { 명령해석기.Terminal(true); }
    }
    static int Læse() {
        if (!vindue_session.이어읽기) { Størrelse = markør_VÆRDI = SØG_VÆRDI = START_vindue = 0; 가로보기 = false; }
        else { vindue_session.이어읽기 = false; prøve_igen_VÆRDI(); } boolean overløb = false;
        while (true) {
            int byte_data = Tavle.직렬읽기(); if (byte_data == -4096) return -3;
            if (Tavle.Terminal(14) != 0) prøve_igen_VÆRDI(); if (byte_data < 0) { Tavle.AFKAST_CPU(); continue; }
            if (byte_data == 10 && 명령해석기.Forrige_linje) { 명령해석기.Forrige_linje = false; continue; } 명령해석기.Forrige_linje = byte_data == 13;
            if (byte_data == 27) { 탈출(); continue; }
            if (byte_data == 3) { 단말.Skrive("^C\n"); return -1; }
            if (byte_data == 4 && Størrelse == 0 && kommandolinje) { if (Tavle.Terminal(2) != 0) 명령해석기.Terminal(true); return -1; }
            if (byte_data == 13 || byte_data == 10) { 단말.문자(10); if (!overløb) tilføj_LOG(); return overløb ? -2 : Størrelse; }
            if (byte_data == 9 && kommandolinje) { fuldført_VÆRDI(); continue; }
            if (byte_data == 1 || byte_data == 5) { markør_VÆRDI = byte_data == 1 ? 0 : Størrelse; prøve_igen_VÆRDI(); continue; }
            if (byte_data == 8 || byte_data == 127 || byte_data == 21) {
                if (byte_data == 21) { for (int Loop_INDEKS = markør_VÆRDI; Loop_INDEKS < Størrelse; Loop_INDEKS++) 명령해석기.Linje[Loop_INDEKS - markør_VÆRDI] = 명령해석기.Linje[Loop_INDEKS]; Størrelse -= markør_VÆRDI; markør_VÆRDI = 0; }
                else if (markør_VÆRDI > 0) { int 변경전 = frontvendt_VÆRDI(markør_VÆRDI); for (int Loop_INDEKS = markør_VÆRDI; Loop_INDEKS < Størrelse; Loop_INDEKS++) 명령해석기.Linje[Loop_INDEKS - markør_VÆRDI + 변경전] = 명령해석기.Linje[Loop_INDEKS]; Størrelse -= markør_VÆRDI - 변경전; markør_VÆRDI = 변경전; }
                prøve_igen_VÆRDI(); continue;
            }
            if (byte_data == 11) { Størrelse = markør_VÆRDI; prøve_igen_VÆRDI(); continue; }
            if (byte_data < 32 && byte_data != 9) continue;
            if (Størrelse == 명령해석기.Linje.length) { overløb = true; continue; }
            for (int Loop_INDEKS = Størrelse; Loop_INDEKS > markør_VÆRDI; Loop_INDEKS--) 명령해석기.Linje[Loop_INDEKS] = 명령해석기.Linje[Loop_INDEKS - 1];
            명령해석기.Linje[markør_VÆRDI++] = byte_data; Størrelse++;
            if (markør_VÆRDI == Størrelse && !가로보기 && 폭(0, Størrelse) <= 보이는폭()) Tavle.직렬쓰기(byte_data);
            else if (markør_VÆRDI == Størrelse) 보이는줄(); else prøve_igen_VÆRDI();
        }
    }
}
