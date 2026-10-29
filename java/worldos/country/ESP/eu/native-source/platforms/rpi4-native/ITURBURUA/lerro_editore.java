// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 byte_balio 경계를 지키는 삽입/삭제, 방향키, Komandoa LOG_marka, Tab Osatutakoak_balio. */
public final class lerro_editore {
    static boolean komando_lerro;
    static int[] LOG_marka = new int[16 * 1024], LOG_luzera = new int[16], Store_balio = new int[4096], 후보 = new int[64];
    static int LOG_ZENBATU, LOG_marka_amaitu, BILATU_balio, 저장길이, Tamaina, kurtsore_balio, 후보수, 후보길이, HASI_leiho;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd seguru_shell urruneko_pantaila run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String sarrera_Zerrenda, int HASI_kargu, int amaitu_kargu, int 입력길이) {
        int byte_ZENBATU=0;
        for(int kargu_INDIZE=HASI_kargu;kargu_INDIZE<amaitu_kargu;kargu_INDIZE++) {
            int karaktere_kode=sarrera_Zerrenda.charAt(kargu_INDIZE);
            if(karaktere_kode>=0xd800 && karaktere_kode<=0xdbff && kargu_INDIZE+1<amaitu_kargu)karaktere_kode=0x10000+((karaktere_kode-0xd800)<<10)+sarrera_Zerrenda.charAt(++kargu_INDIZE)-0xdc00;
            int 수=karaktere_kode<128?1:karaktere_kode<2048?2:karaktere_kode<65536?3:4;
            if(byte_ZENBATU+수>62)return;
            for(int SEKUENTZIA_balio=수-1;SEKUENTZIA_balio>=0;SEKUENTZIA_balio--)명령후보[byte_ZENBATU++]=수==1?karaktere_kode:SEKUENTZIA_balio==수-1?(수==2?0xc0:수==3?0xe0:0xf0)|(karaktere_kode>>(6*SEKUENTZIA_balio)):0x80|((karaktere_kode>>(6*SEKUENTZIA_balio))&63);
        }
        if(byte_ZENBATU<입력길이)return;
        for(int kargu_INDIZE=0;kargu_INDIZE<입력길이;kargu_INDIZE++)if(명령후보[kargu_INDIZE]!=명령해석기.Marra[kargu_INDIZE])return;
        후보수++;후보길이=byte_ZENBATU+1;
        for(int kargu_INDIZE=0;kargu_INDIZE<byte_ZENBATU;kargu_INDIZE++)후보[kargu_INDIZE]=명령후보[kargu_INDIZE];후보[byte_ZENBATU]=' ';
    }
    static int aurrekoa_balio(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (명령해석기.Marra[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int ATZERA_balio(int 읽는자리) { if (읽는자리 < Tamaina) { 읽는자리++; while (읽는자리 < Tamaina && (명령해석기.Marra[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int HASI_kargu, int helburu_balio_INDIZE) {
        int 글칸수 = 0;
        for (int Loop_INDIZE = HASI_kargu; Loop_INDIZE < helburu_balio_INDIZE; Loop_INDIZE++) { int byte_datuak = 명령해석기.Marra[Loop_INDIZE]; if ((byte_datuak & 192) == 128) continue; 글칸수 += byte_datuak >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void 다시() {
        단말.Idatzi("\r\u001b[2K");
        단말.Idatzi(komando_lerro ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 Marra 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int ZUTABEAK = arbel.Terminala(13) & 65535; return ZUTABEAK - (komando_lerro ? 18 : 9); }
    static void 보이는줄() {
        if (kurtsore_balio < HASI_leiho) HASI_leiho = kurtsore_balio;
        while (폭(HASI_leiho, kurtsore_balio) > 보이는폭()) HASI_leiho = ATZERA_balio(HASI_leiho);
        int amaitu_kargu = HASI_leiho;
        while (amaitu_kargu < Tamaina && 폭(HASI_leiho, ATZERA_balio(amaitu_kargu)) <= 보이는폭()) amaitu_kargu = ATZERA_balio(amaitu_kargu);
        단말.Idatzi("\r\u001b["); 단말.수(komando_lerro ? 16 : 7); 단말.Idatzi("G\u001b[K");
        if (HASI_leiho > 0) 단말.문자('<');
        for (int Loop_INDIZE = HASI_leiho; Loop_INDIZE < amaitu_kargu; Loop_INDIZE++) arbel.직렬쓰기(명령해석기.Marra[Loop_INDIZE]);
        단말.문자(amaitu_kargu < Tamaina ? '>' : ' ');
        단말.Idatzi("\u001b["); 단말.수(폭(kurtsore_balio, amaitu_kargu) + 1); 단말.문자('D');
        가로보기 = HASI_leiho > 0 || amaitu_kargu < Tamaina || 폭(0, Tamaina) > 보이는폭();
    }
    static void Erantsi_LOG() {
        if (!komando_lerro || Tamaina == 0 || Tamaina > 1024) return;
        if (LOG_ZENBATU > 0) {
            int 마지막자리 = (LOG_marka_amaitu + 15) % 16; boolean 같은여부 = LOG_luzera[마지막자리] == Tamaina;
            for (int Loop_INDIZE = 0; 같은여부 && Loop_INDIZE < Tamaina; Loop_INDIZE++) if (LOG_marka[마지막자리 * 1024 + Loop_INDIZE] != 명령해석기.Marra[Loop_INDIZE]) 같은여부 = false;
            if (같은여부) return;
        }
        LOG_luzera[LOG_marka_amaitu] = Tamaina; for (int Loop_INDIZE = 0; Loop_INDIZE < Tamaina; Loop_INDIZE++) LOG_marka[LOG_marka_amaitu * 1024 + Loop_INDIZE] = 명령해석기.Marra[Loop_INDIZE];
        LOG_marka_amaitu = (LOG_marka_amaitu + 1) % 16; if (LOG_ZENBATU < 16) LOG_ZENBATU++;
    }
    static void 기록이동(int DELTA_balio) {
        if (!komando_lerro) return;
        if (BILATU_balio == 0 && DELTA_balio > 0) { 저장길이 = Tamaina; for (int Loop_INDIZE = 0; Loop_INDIZE < Tamaina; Loop_INDIZE++) Store_balio[Loop_INDIZE] = 명령해석기.Marra[Loop_INDIZE]; }
        int Hurrengoa_kargu = BILATU_balio + DELTA_balio; if (Hurrengoa_kargu < 0 || Hurrengoa_kargu > LOG_ZENBATU) return; BILATU_balio = Hurrengoa_kargu;
        if (BILATU_balio == 0) { Tamaina = 저장길이; for (int Loop_INDIZE = 0; Loop_INDIZE < Tamaina; Loop_INDIZE++) 명령해석기.Marra[Loop_INDIZE] = Store_balio[Loop_INDIZE]; }
        else { int 보관칸 = (LOG_marka_amaitu + 16 - BILATU_balio) % 16; Tamaina = LOG_luzera[보관칸]; for (int Loop_INDIZE = 0; Loop_INDIZE < Tamaina; Loop_INDIZE++) 명령해석기.Marra[Loop_INDIZE] = LOG_marka[보관칸 * 1024 + Loop_INDIZE]; }
        kurtsore_balio = Tamaina; 다시();
    }
    static void erakutsi_LOG() {
        for (int sarrera_ZENBATU = 0; sarrera_ZENBATU < LOG_ZENBATU; sarrera_ZENBATU++) {
            int 보관칸 = (LOG_marka_amaitu + 16 - LOG_ZENBATU + sarrera_ZENBATU) % 16; 단말.수(sarrera_ZENBATU + 1); 단말.Idatzi("  ");
            for (int Loop_INDIZE = 0; Loop_INDIZE < LOG_luzera[보관칸]; Loop_INDIZE++) arbel.직렬쓰기(LOG_marka[보관칸 * 1024 + Loop_INDIZE]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] datuak_matrize, int HASI_kargu, int sarrera_ZENBATU, int 접두말, int 총수, boolean 폴더번호) {
        if (sarrera_ZENBATU < 총수 || sarrera_ZENBATU > 62) return;
        for (int Loop_INDIZE = 0; Loop_INDIZE < 총수; Loop_INDIZE++) if (datuak_matrize[HASI_kargu + Loop_INDIZE] != 명령해석기.Marra[접두말 + Loop_INDIZE]) return;
        후보수++; 후보길이 = sarrera_ZENBATU + 1;
        for (int Loop_INDIZE = 0; Loop_INDIZE < sarrera_ZENBATU; Loop_INDIZE++) 후보[Loop_INDIZE] = datuak_matrize[HASI_kargu + Loop_INDIZE]; 후보[sarrera_ZENBATU] = 폴더번호 ? '/' : ' ';
    }
    static void Osatutakoak_balio() {
        if (!komando_lerro || kurtsore_balio != Tamaina) return;
        int 시작점 = Tamaina; while (시작점 > 0 && 명령해석기.Marra[시작점 - 1] != ' ') 시작점--;
        for (int Loop_INDIZE = 시작점; Loop_INDIZE < Tamaina; Loop_INDIZE++) if (명령해석기.Marra[Loop_INDIZE] == '/' || 명령해석기.Marra[Loop_INDIZE] == '"' || 명령해석기.Marra[Loop_INDIZE] == 39 || 명령해석기.Marra[Loop_INDIZE] == '\\') return;
        후보수 = 0; int sarrera_ZENBATU = Tamaina - 시작점;
        if (시작점 == 0) {
            for(int zerrendaren_indize=0;zerrendaren_indize<2;zerrendaren_indize++) {
                String sarrera_Zerrenda=zerrendaren_indize==0?명령들:관리명령.Osatutakoak_Word();
                int 읽는자리=0;
                while(읽는자리<sarrera_Zerrenda.length()) {
                    int amaitu_kargu=읽는자리;while(amaitu_kargu<sarrera_Zerrenda.length() && sarrera_Zerrenda.charAt(amaitu_kargu)!=' ')amaitu_kargu++;
                    명령후보넣기(sarrera_Zerrenda,읽는자리,amaitu_kargu,sarrera_ZENBATU);읽는자리=amaitu_kargu+1;
                }
            }
        } else {
            Memoria_Fitxategiak.bide_izen_HASI(1); Memoria_Fitxategiak.bide_izen_byte(0, '.'); Memoria_Fitxategiak.normalizatu_balio();
            for (int Loop_INDIZE = 0; Loop_INDIZE < Memoria_Fitxategiak.fitxategi_ZENBATU; Loop_INDIZE++) {
                int HASI_kargu = Memoria_Fitxategiak.sarrera_HASI(Memoria_Fitxategiak.Izena, Loop_INDIZE * 64, Memoria_Fitxategiak.이름길이[Loop_INDIZE]);
                if (HASI_kargu >= 0) 후보넣기(Memoria_Fitxategiak.Izena, Loop_INDIZE * 64 + HASI_kargu, Memoria_Fitxategiak.이름길이[Loop_INDIZE] - HASI_kargu, 시작점, sarrera_ZENBATU, false);
            }
            for (int Loop_INDIZE = 0; Loop_INDIZE < 16; Loop_INDIZE++) {
                int HASI_kargu = Memoria_Fitxategiak.sarrera_HASI(Memoria_Fitxategiak.direktorio_izen, Loop_INDIZE * 64, Memoria_Fitxategiak.direktorio_luzera[Loop_INDIZE]);
                if (HASI_kargu >= 0) 후보넣기(Memoria_Fitxategiak.direktorio_izen, Loop_INDIZE * 64 + HASI_kargu, Memoria_Fitxategiak.direktorio_luzera[Loop_INDIZE] - HASI_kargu, 시작점, sarrera_ZENBATU, true);
            }
        }
        if (후보수 != 1) { arbel.직렬쓰기(7); return; }
        for (int Loop_INDIZE = sarrera_ZENBATU; Loop_INDIZE < 후보길이 && Tamaina < 명령해석기.Marra.length - 1; Loop_INDIZE++) {
            if (후보[Loop_INDIZE] == ' ' && Loop_INDIZE != 후보길이 - 1) 명령해석기.Marra[Tamaina++] = '\\';
            명령해석기.Marra[Tamaina++] = 후보[Loop_INDIZE];
        }
        kurtsore_balio = Tamaina; 다시();
    }
    static int 탈출읽기() {
        int 시작점 = arbel.밀리초();
        while (arbel.밀리초() - 시작점 < 80) { int byte_datuak = arbel.직렬읽기(); if (byte_datuak >= 0) return byte_datuak; arbel.YIELD_PUZ(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int sarrera_ZENBATU = 0, amaitu_kargu = -1;
        for (int Loop_INDIZE = 0; Loop_INDIZE < 12; Loop_INDIZE++) { int byte_datuak = 탈출읽기(); if (byte_datuak < 0) return; if (byte_datuak >= '0' && byte_datuak <= '9') sarrera_ZENBATU = sarrera_ZENBATU * 10 + byte_datuak - '0'; else { amaitu_kargu = byte_datuak; break; } }
        if (amaitu_kargu == 'A') 기록이동(1);
        else if (amaitu_kargu == 'B') 기록이동(-1);
        else if (amaitu_kargu == 'C') { kurtsore_balio = ATZERA_balio(kurtsore_balio); 다시(); }
        else if (amaitu_kargu == 'D') { kurtsore_balio = aurrekoa_balio(kurtsore_balio); 다시(); }
        else if (amaitu_kargu == 'H' || amaitu_kargu == '~' && (sarrera_ZENBATU == 1 || sarrera_ZENBATU == 7)) { kurtsore_balio = 0; 다시(); }
        else if (amaitu_kargu == 'F' || amaitu_kargu == '~' && (sarrera_ZENBATU == 4 || sarrera_ZENBATU == 8)) { kurtsore_balio = Tamaina; 다시(); }
        else if (amaitu_kargu == '~' && sarrera_ZENBATU == 3 && kurtsore_balio < Tamaina) {
            int Hurrengoa_kargu = ATZERA_balio(kurtsore_balio); for (int Loop_INDIZE = Hurrengoa_kargu; Loop_INDIZE < Tamaina; Loop_INDIZE++) 명령해석기.Marra[Loop_INDIZE - Hurrengoa_kargu + kurtsore_balio] = 명령해석기.Marra[Loop_INDIZE]; Tamaina -= Hurrengoa_kargu - kurtsore_balio; 다시();
        }
        else if (amaitu_kargu == '~' && (sarrera_ZENBATU == 5 || sarrera_ZENBATU == 6)) arbel.Terminala(sarrera_ZENBATU == 5 ? 5 : 6);
        else if (amaitu_kargu == '~' && sarrera_ZENBATU == 24 && komando_lerro) { 명령해석기.Terminala(true); }
    }
    static int Irakurri() {
        if (!leiho_saio.이어읽기) { Tamaina = kurtsore_balio = BILATU_balio = HASI_leiho = 0; 가로보기 = false; }
        else { leiho_saio.이어읽기 = false; 다시(); } boolean 넘침여부 = false;
        while (true) {
            int byte_datuak = arbel.직렬읽기(); if (byte_datuak == -4096) return -3;
            if (arbel.Terminala(14) != 0) 다시(); if (byte_datuak < 0) { arbel.YIELD_PUZ(); continue; }
            if (byte_datuak == 10 && 명령해석기.앞줄) { 명령해석기.앞줄 = false; continue; } 명령해석기.앞줄 = byte_datuak == 13;
            if (byte_datuak == 27) { 탈출(); continue; }
            if (byte_datuak == 3) { 단말.Idatzi("^C\n"); return -1; }
            if (byte_datuak == 4 && Tamaina == 0 && komando_lerro) { if (arbel.Terminala(2) != 0) 명령해석기.Terminala(true); return -1; }
            if (byte_datuak == 13 || byte_datuak == 10) { 단말.문자(10); if (!넘침여부) Erantsi_LOG(); return 넘침여부 ? -2 : Tamaina; }
            if (byte_datuak == 9 && komando_lerro) { Osatutakoak_balio(); continue; }
            if (byte_datuak == 1 || byte_datuak == 5) { kurtsore_balio = byte_datuak == 1 ? 0 : Tamaina; 다시(); continue; }
            if (byte_datuak == 8 || byte_datuak == 127 || byte_datuak == 21) {
                if (byte_datuak == 21) { for (int Loop_INDIZE = kurtsore_balio; Loop_INDIZE < Tamaina; Loop_INDIZE++) 명령해석기.Marra[Loop_INDIZE - kurtsore_balio] = 명령해석기.Marra[Loop_INDIZE]; Tamaina -= kurtsore_balio; kurtsore_balio = 0; }
                else if (kurtsore_balio > 0) { int 변경전 = aurrekoa_balio(kurtsore_balio); for (int Loop_INDIZE = kurtsore_balio; Loop_INDIZE < Tamaina; Loop_INDIZE++) 명령해석기.Marra[Loop_INDIZE - kurtsore_balio + 변경전] = 명령해석기.Marra[Loop_INDIZE]; Tamaina -= kurtsore_balio - 변경전; kurtsore_balio = 변경전; }
                다시(); continue;
            }
            if (byte_datuak == 11) { Tamaina = kurtsore_balio; 다시(); continue; }
            if (byte_datuak < 32 && byte_datuak != 9) continue;
            if (Tamaina == 명령해석기.Marra.length) { 넘침여부 = true; continue; }
            for (int Loop_INDIZE = Tamaina; Loop_INDIZE > kurtsore_balio; Loop_INDIZE--) 명령해석기.Marra[Loop_INDIZE] = 명령해석기.Marra[Loop_INDIZE - 1];
            명령해석기.Marra[kurtsore_balio++] = byte_datuak; Tamaina++;
            if (kurtsore_balio == Tamaina && !가로보기 && 폭(0, Tamaina) <= 보이는폭()) arbel.직렬쓰기(byte_datuak);
            else if (kurtsore_balio == Tamaina) 보이는줄(); else 다시();
        }
    }
}
