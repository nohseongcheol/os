// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 byte_WAARDE 경계를 지키는 삽입/삭제, 방향키, opdracht LOG_RECORD, Tab Voltooid_WAARDE. */
public final class regeleditor {
    static boolean opdrachtregel;
    static int[] LOG_RECORD = new int[16 * 1024], LOG_tijdsduur = new int[16], Store_WAARDE = new int[4096], sollicitant = new int[64];
    static int LOG_AANTAL, LOG_RECORD_beëindigen, Search_WAARDE, 저장길이, Grootte, cursor_WAARDE, sollicitant_AANTAL, sollicitant_tijdsduur, START_venster;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd veilig_Shell extern_weergeven run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] opdracht_sollicitant = new int[128];
    static void Toevoegen_opdracht_sollicitant(String invoer_Lijst_f07b3200, int START_functie, int beëindigen_functie, int invoer_tijdsduur) {
        int byte_AANTAL=0;
        for(int plaatsingsindex=START_functie;plaatsingsindex<beëindigen_functie;plaatsingsindex++) {
            int codepoint=invoer_Lijst_f07b3200.charAt(plaatsingsindex);
            if(codepoint>=0xd800 && codepoint<=0xdbff && plaatsingsindex+1<beëindigen_functie)codepoint=0x10000+((codepoint-0xd800)<<10)+invoer_Lijst_f07b3200.charAt(++plaatsingsindex)-0xdc00;
            int nummer=codepoint<128?1:codepoint<2048?2:codepoint<65536?3:4;
            if(byte_AANTAL+nummer>62)return;
            for(int REEKS_WAARDE=nummer-1;REEKS_WAARDE>=0;REEKS_WAARDE--)opdracht_sollicitant[byte_AANTAL++]=nummer==1?codepoint:REEKS_WAARDE==nummer-1?(nummer==2?0xc0:nummer==3?0xe0:0xf0)|(codepoint>>(6*REEKS_WAARDE)):0x80|((codepoint>>(6*REEKS_WAARDE))&63);
        }
        if(byte_AANTAL<invoer_tijdsduur)return;
        for(int plaatsingsindex=0;plaatsingsindex<invoer_tijdsduur;plaatsingsindex++)if(opdracht_sollicitant[plaatsingsindex]!=Opdrachtvertolker.invoerregel[plaatsingsindex])return;
        sollicitant_AANTAL++;sollicitant_tijdsduur=byte_AANTAL+1;
        for(int plaatsingsindex=0;plaatsingsindex<byte_AANTAL;plaatsingsindex++)sollicitant[plaatsingsindex]=opdracht_sollicitant[plaatsingsindex];sollicitant[byte_AANTAL]=' ';
    }
    static int voorkant_WAARDE(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (Opdrachtvertolker.invoerregel[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int BACK_WAARDE(int 읽는자리) { if (읽는자리 < Grootte) { 읽는자리++; while (읽는자리 < Grootte && (Opdrachtvertolker.invoerregel[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int START_functie, int doel_WAARDE_INDEX) {
        int 글칸수 = 0;
        for (int lus_INDEX = START_functie; lus_INDEX < doel_WAARDE_INDEX; lus_INDEX++) { int byte_gegevens = Opdrachtvertolker.invoerregel[lus_INDEX]; if ((byte_gegevens & 192) == 128) continue; 글칸수 += byte_gegevens >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void opnieuw_proberen_WAARDE() {
        단말.Schrijven("\r\u001b[2K");
        단말.Schrijven(opdrachtregel ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 invoerregel 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int KOLOMMEN = Bord.terminal(13) & 65535; return KOLOMMEN - (opdrachtregel ? 18 : 9); }
    static void 보이는줄() {
        if (cursor_WAARDE < START_venster) START_venster = cursor_WAARDE;
        while (폭(START_venster, cursor_WAARDE) > 보이는폭()) START_venster = BACK_WAARDE(START_venster);
        int beëindigen_functie = START_venster;
        while (beëindigen_functie < Grootte && 폭(START_venster, BACK_WAARDE(beëindigen_functie)) <= 보이는폭()) beëindigen_functie = BACK_WAARDE(beëindigen_functie);
        단말.Schrijven("\r\u001b["); 단말.nummer(opdrachtregel ? 16 : 7); 단말.Schrijven("G\u001b[K");
        if (START_venster > 0) 단말.문자('<');
        for (int lus_INDEX = START_venster; lus_INDEX < beëindigen_functie; lus_INDEX++) Bord.직렬쓰기(Opdrachtvertolker.invoerregel[lus_INDEX]);
        단말.문자(beëindigen_functie < Grootte ? '>' : ' ');
        단말.Schrijven("\u001b["); 단말.nummer(폭(cursor_WAARDE, beëindigen_functie) + 1); 단말.문자('D');
        가로보기 = START_venster > 0 || beëindigen_functie < Grootte || 폭(0, Grootte) > 보이는폭();
    }
    static void toevoegen_LOG() {
        if (!opdrachtregel || Grootte == 0 || Grootte > 1024) return;
        if (LOG_AANTAL > 0) {
            int 마지막자리 = (LOG_RECORD_beëindigen + 15) % 16; boolean 같은여부 = LOG_tijdsduur[마지막자리] == Grootte;
            for (int lus_INDEX = 0; 같은여부 && lus_INDEX < Grootte; lus_INDEX++) if (LOG_RECORD[마지막자리 * 1024 + lus_INDEX] != Opdrachtvertolker.invoerregel[lus_INDEX]) 같은여부 = false;
            if (같은여부) return;
        }
        LOG_tijdsduur[LOG_RECORD_beëindigen] = Grootte; for (int lus_INDEX = 0; lus_INDEX < Grootte; lus_INDEX++) LOG_RECORD[LOG_RECORD_beëindigen * 1024 + lus_INDEX] = Opdrachtvertolker.invoerregel[lus_INDEX];
        LOG_RECORD_beëindigen = (LOG_RECORD_beëindigen + 1) % 16; if (LOG_AANTAL < 16) LOG_AANTAL++;
    }
    static void 기록이동(int DELTA_WAARDE) {
        if (!opdrachtregel) return;
        if (Search_WAARDE == 0 && DELTA_WAARDE > 0) { 저장길이 = Grootte; for (int lus_INDEX = 0; lus_INDEX < Grootte; lus_INDEX++) Store_WAARDE[lus_INDEX] = Opdrachtvertolker.invoerregel[lus_INDEX]; }
        int Volgende_functie = Search_WAARDE + DELTA_WAARDE; if (Volgende_functie < 0 || Volgende_functie > LOG_AANTAL) return; Search_WAARDE = Volgende_functie;
        if (Search_WAARDE == 0) { Grootte = 저장길이; for (int lus_INDEX = 0; lus_INDEX < Grootte; lus_INDEX++) Opdrachtvertolker.invoerregel[lus_INDEX] = Store_WAARDE[lus_INDEX]; }
        else { int 보관칸 = (LOG_RECORD_beëindigen + 16 - Search_WAARDE) % 16; Grootte = LOG_tijdsduur[보관칸]; for (int lus_INDEX = 0; lus_INDEX < Grootte; lus_INDEX++) Opdrachtvertolker.invoerregel[lus_INDEX] = LOG_RECORD[보관칸 * 1024 + lus_INDEX]; }
        cursor_WAARDE = Grootte; opnieuw_proberen_WAARDE();
    }
    static void weergeven_LOG() {
        for (int invoer_AANTAL_8f7753a1 = 0; invoer_AANTAL_8f7753a1 < LOG_AANTAL; invoer_AANTAL_8f7753a1++) {
            int 보관칸 = (LOG_RECORD_beëindigen + 16 - LOG_AANTAL + invoer_AANTAL_8f7753a1) % 16; 단말.nummer(invoer_AANTAL_8f7753a1 + 1); 단말.Schrijven("  ");
            for (int lus_INDEX = 0; lus_INDEX < LOG_tijdsduur[보관칸]; lus_INDEX++) Bord.직렬쓰기(LOG_RECORD[보관칸 * 1024 + lus_INDEX]); 단말.문자(10);
        }
    }
    static void Toevoegen_sollicitant(int[] gegevens_MATRIX, int START_functie, int invoer_AANTAL_8f7753a1, int 접두말, int totaal_AANTAL, boolean map_nummer) {
        if (invoer_AANTAL_8f7753a1 < totaal_AANTAL || invoer_AANTAL_8f7753a1 > 62) return;
        for (int lus_INDEX = 0; lus_INDEX < totaal_AANTAL; lus_INDEX++) if (gegevens_MATRIX[START_functie + lus_INDEX] != Opdrachtvertolker.invoerregel[접두말 + lus_INDEX]) return;
        sollicitant_AANTAL++; sollicitant_tijdsduur = invoer_AANTAL_8f7753a1 + 1;
        for (int lus_INDEX = 0; lus_INDEX < invoer_AANTAL_8f7753a1; lus_INDEX++) sollicitant[lus_INDEX] = gegevens_MATRIX[START_functie + lus_INDEX]; sollicitant[invoer_AANTAL_8f7753a1] = map_nummer ? '/' : ' ';
    }
    static void Voltooid_WAARDE() {
        if (!opdrachtregel || cursor_WAARDE != Grootte) return;
        int 시작점 = Grootte; while (시작점 > 0 && Opdrachtvertolker.invoerregel[시작점 - 1] != ' ') 시작점--;
        for (int lus_INDEX = 시작점; lus_INDEX < Grootte; lus_INDEX++) if (Opdrachtvertolker.invoerregel[lus_INDEX] == '/' || Opdrachtvertolker.invoerregel[lus_INDEX] == '"' || Opdrachtvertolker.invoerregel[lus_INDEX] == 39 || Opdrachtvertolker.invoerregel[lus_INDEX] == '\\') return;
        sollicitant_AANTAL = 0; int invoer_AANTAL_8f7753a1 = Grootte - 시작점;
        if (시작점 == 0) {
            for(int lijstindex=0;lijstindex<2;lijstindex++) {
                String invoer_Lijst_f07b3200=lijstindex==0?명령들:관리명령.Voltooid_Word();
                int 읽는자리=0;
                while(읽는자리<invoer_Lijst_f07b3200.length()) {
                    int beëindigen_functie=읽는자리;while(beëindigen_functie<invoer_Lijst_f07b3200.length() && invoer_Lijst_f07b3200.charAt(beëindigen_functie)!=' ')beëindigen_functie++;
                    Toevoegen_opdracht_sollicitant(invoer_Lijst_f07b3200,읽는자리,beëindigen_functie,invoer_AANTAL_8f7753a1);읽는자리=beëindigen_functie+1;
                }
            }
        } else {
            GeheugenBestanden.pad_START(1); GeheugenBestanden.pad_byte(0, '.'); GeheugenBestanden.normaliseren_WAARDE();
            for (int lus_INDEX = 0; lus_INDEX < GeheugenBestanden.Bestand_AANTAL; lus_INDEX++) {
                int START_functie = GeheugenBestanden.invoer_START(GeheugenBestanden.Naam, lus_INDEX * 64, GeheugenBestanden.이름길이[lus_INDEX]);
                if (START_functie >= 0) Toevoegen_sollicitant(GeheugenBestanden.Naam, lus_INDEX * 64 + START_functie, GeheugenBestanden.이름길이[lus_INDEX] - START_functie, 시작점, invoer_AANTAL_8f7753a1, false);
            }
            for (int lus_INDEX = 0; lus_INDEX < 16; lus_INDEX++) {
                int START_functie = GeheugenBestanden.invoer_START(GeheugenBestanden.map_naam, lus_INDEX * 64, GeheugenBestanden.map_tijdsduur[lus_INDEX]);
                if (START_functie >= 0) Toevoegen_sollicitant(GeheugenBestanden.map_naam, lus_INDEX * 64 + START_functie, GeheugenBestanden.map_tijdsduur[lus_INDEX] - START_functie, 시작점, invoer_AANTAL_8f7753a1, true);
            }
        }
        if (sollicitant_AANTAL != 1) { Bord.직렬쓰기(7); return; }
        for (int lus_INDEX = invoer_AANTAL_8f7753a1; lus_INDEX < sollicitant_tijdsduur && Grootte < Opdrachtvertolker.invoerregel.length - 1; lus_INDEX++) {
            if (sollicitant[lus_INDEX] == ' ' && lus_INDEX != sollicitant_tijdsduur - 1) Opdrachtvertolker.invoerregel[Grootte++] = '\\';
            Opdrachtvertolker.invoerregel[Grootte++] = sollicitant[lus_INDEX];
        }
        cursor_WAARDE = Grootte; opnieuw_proberen_WAARDE();
    }
    static int 탈출읽기() {
        int 시작점 = Bord.밀리초();
        while (Bord.밀리초() - 시작점 < 80) { int byte_gegevens = Bord.직렬읽기(); if (byte_gegevens >= 0) return byte_gegevens; Bord.RENDEMENT_CPU(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int invoer_AANTAL_8f7753a1 = 0, beëindigen_functie = -1;
        for (int lus_INDEX = 0; lus_INDEX < 12; lus_INDEX++) { int byte_gegevens = 탈출읽기(); if (byte_gegevens < 0) return; if (byte_gegevens >= '0' && byte_gegevens <= '9') invoer_AANTAL_8f7753a1 = invoer_AANTAL_8f7753a1 * 10 + byte_gegevens - '0'; else { beëindigen_functie = byte_gegevens; break; } }
        if (beëindigen_functie == 'A') 기록이동(1);
        else if (beëindigen_functie == 'B') 기록이동(-1);
        else if (beëindigen_functie == 'C') { cursor_WAARDE = BACK_WAARDE(cursor_WAARDE); opnieuw_proberen_WAARDE(); }
        else if (beëindigen_functie == 'D') { cursor_WAARDE = voorkant_WAARDE(cursor_WAARDE); opnieuw_proberen_WAARDE(); }
        else if (beëindigen_functie == 'H' || beëindigen_functie == '~' && (invoer_AANTAL_8f7753a1 == 1 || invoer_AANTAL_8f7753a1 == 7)) { cursor_WAARDE = 0; opnieuw_proberen_WAARDE(); }
        else if (beëindigen_functie == 'F' || beëindigen_functie == '~' && (invoer_AANTAL_8f7753a1 == 4 || invoer_AANTAL_8f7753a1 == 8)) { cursor_WAARDE = Grootte; opnieuw_proberen_WAARDE(); }
        else if (beëindigen_functie == '~' && invoer_AANTAL_8f7753a1 == 3 && cursor_WAARDE < Grootte) {
            int Volgende_functie = BACK_WAARDE(cursor_WAARDE); for (int lus_INDEX = Volgende_functie; lus_INDEX < Grootte; lus_INDEX++) Opdrachtvertolker.invoerregel[lus_INDEX - Volgende_functie + cursor_WAARDE] = Opdrachtvertolker.invoerregel[lus_INDEX]; Grootte -= Volgende_functie - cursor_WAARDE; opnieuw_proberen_WAARDE();
        }
        else if (beëindigen_functie == '~' && (invoer_AANTAL_8f7753a1 == 5 || invoer_AANTAL_8f7753a1 == 6)) Bord.terminal(invoer_AANTAL_8f7753a1 == 5 ? 5 : 6);
        else if (beëindigen_functie == '~' && invoer_AANTAL_8f7753a1 == 24 && opdrachtregel) { Opdrachtvertolker.terminal(true); }
    }
    static int Lezen() {
        if (!venster_sessie.이어읽기) { Grootte = cursor_WAARDE = Search_WAARDE = START_venster = 0; 가로보기 = false; }
        else { venster_sessie.이어읽기 = false; opnieuw_proberen_WAARDE(); } boolean overloop = false;
        while (true) {
            int byte_gegevens = Bord.직렬읽기(); if (byte_gegevens == -4096) return -3;
            if (Bord.terminal(14) != 0) opnieuw_proberen_WAARDE(); if (byte_gegevens < 0) { Bord.RENDEMENT_CPU(); continue; }
            if (byte_gegevens == 10 && Opdrachtvertolker.Vorige_lijn) { Opdrachtvertolker.Vorige_lijn = false; continue; } Opdrachtvertolker.Vorige_lijn = byte_gegevens == 13;
            if (byte_gegevens == 27) { 탈출(); continue; }
            if (byte_gegevens == 3) { 단말.Schrijven("^C\n"); return -1; }
            if (byte_gegevens == 4 && Grootte == 0 && opdrachtregel) { if (Bord.terminal(2) != 0) Opdrachtvertolker.terminal(true); return -1; }
            if (byte_gegevens == 13 || byte_gegevens == 10) { 단말.문자(10); if (!overloop) toevoegen_LOG(); return overloop ? -2 : Grootte; }
            if (byte_gegevens == 9 && opdrachtregel) { Voltooid_WAARDE(); continue; }
            if (byte_gegevens == 1 || byte_gegevens == 5) { cursor_WAARDE = byte_gegevens == 1 ? 0 : Grootte; opnieuw_proberen_WAARDE(); continue; }
            if (byte_gegevens == 8 || byte_gegevens == 127 || byte_gegevens == 21) {
                if (byte_gegevens == 21) { for (int lus_INDEX = cursor_WAARDE; lus_INDEX < Grootte; lus_INDEX++) Opdrachtvertolker.invoerregel[lus_INDEX - cursor_WAARDE] = Opdrachtvertolker.invoerregel[lus_INDEX]; Grootte -= cursor_WAARDE; cursor_WAARDE = 0; }
                else if (cursor_WAARDE > 0) { int 변경전 = voorkant_WAARDE(cursor_WAARDE); for (int lus_INDEX = cursor_WAARDE; lus_INDEX < Grootte; lus_INDEX++) Opdrachtvertolker.invoerregel[lus_INDEX - cursor_WAARDE + 변경전] = Opdrachtvertolker.invoerregel[lus_INDEX]; Grootte -= cursor_WAARDE - 변경전; cursor_WAARDE = 변경전; }
                opnieuw_proberen_WAARDE(); continue;
            }
            if (byte_gegevens == 11) { Grootte = cursor_WAARDE; opnieuw_proberen_WAARDE(); continue; }
            if (byte_gegevens < 32 && byte_gegevens != 9) continue;
            if (Grootte == Opdrachtvertolker.invoerregel.length) { overloop = true; continue; }
            for (int lus_INDEX = Grootte; lus_INDEX > cursor_WAARDE; lus_INDEX--) Opdrachtvertolker.invoerregel[lus_INDEX] = Opdrachtvertolker.invoerregel[lus_INDEX - 1];
            Opdrachtvertolker.invoerregel[cursor_WAARDE++] = byte_gegevens; Grootte++;
            if (cursor_WAARDE == Grootte && !가로보기 && 폭(0, Grootte) <= 보이는폭()) Bord.직렬쓰기(byte_gegevens);
            else if (cursor_WAARDE == Grootte) 보이는줄(); else opnieuw_proberen_WAARDE();
        }
    }
}
