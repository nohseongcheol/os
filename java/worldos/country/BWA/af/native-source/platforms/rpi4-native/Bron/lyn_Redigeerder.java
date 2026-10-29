// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 greep_VALUE 경계를 지키는 삽입/삭제, 방향키, Opdrag LOG_ry, Tab 완성. */
public final class lyn_Redigeerder {
    static boolean bevelreël;
    static int[] LOG_ry = new int[16 * 1024], LOG_lengte = new int[16], bêre_VALUE = new int[4096], 후보 = new int[64];
    static int LOG_COUNT, LOG_ry_beëindig, Soek_VALUE, 저장길이, Grootte, loper_VALUE, 후보수, 후보길이, BEGIN_venster;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd beveiligde_dop afstands_wys run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String inskrywing_Lys, int BEGIN_plaas, int beëindig_plaas, int 입력길이) {
        int greep_COUNT=0;
        for(int plaas_INDEX=BEGIN_plaas;plaas_INDEX<beëindig_plaas;plaas_INDEX++) {
            int karakterkode=inskrywing_Lys.charAt(plaas_INDEX);
            if(karakterkode>=0xd800 && karakterkode<=0xdbff && plaas_INDEX+1<beëindig_plaas)karakterkode=0x10000+((karakterkode-0xd800)<<10)+inskrywing_Lys.charAt(++plaas_INDEX)-0xdc00;
            int 수=karakterkode<128?1:karakterkode<2048?2:karakterkode<65536?3:4;
            if(greep_COUNT+수>62)return;
            for(int SEQUENCE_VALUE=수-1;SEQUENCE_VALUE>=0;SEQUENCE_VALUE--)명령후보[greep_COUNT++]=수==1?karakterkode:SEQUENCE_VALUE==수-1?(수==2?0xc0:수==3?0xe0:0xf0)|(karakterkode>>(6*SEQUENCE_VALUE)):0x80|((karakterkode>>(6*SEQUENCE_VALUE))&63);
        }
        if(greep_COUNT<입력길이)return;
        for(int plaas_INDEX=0;plaas_INDEX<입력길이;plaas_INDEX++)if(명령후보[plaas_INDEX]!=명령해석기.lyn[plaas_INDEX])return;
        후보수++;후보길이=greep_COUNT+1;
        for(int plaas_INDEX=0;plaas_INDEX<greep_COUNT;plaas_INDEX++)후보[plaas_INDEX]=명령후보[plaas_INDEX];후보[greep_COUNT]=' ';
    }
    static int voor_VALUE(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (명령해석기.lyn[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int TERUG_VALUE(int 읽는자리) { if (읽는자리 < Grootte) { 읽는자리++; while (읽는자리 < Grootte && (명령해석기.lyn[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int BEGIN_plaas, int bestemming_VALUE_INDEX) {
        int 글칸수 = 0;
        for (int lus_INDEX = BEGIN_plaas; lus_INDEX < bestemming_VALUE_INDEX; lus_INDEX++) { int greep_data = 명령해석기.lyn[lus_INDEX]; if ((greep_data & 192) == 128) continue; 글칸수 += greep_data >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void 다시() {
        단말.Skryf("\r\u001b[2K");
        단말.Skryf(bevelreël ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 lyn 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int COLUMNS = bord.Terminaal(13) & 65535; return COLUMNS - (bevelreël ? 18 : 9); }
    static void 보이는줄() {
        if (loper_VALUE < BEGIN_venster) BEGIN_venster = loper_VALUE;
        while (폭(BEGIN_venster, loper_VALUE) > 보이는폭()) BEGIN_venster = TERUG_VALUE(BEGIN_venster);
        int beëindig_plaas = BEGIN_venster;
        while (beëindig_plaas < Grootte && 폭(BEGIN_venster, TERUG_VALUE(beëindig_plaas)) <= 보이는폭()) beëindig_plaas = TERUG_VALUE(beëindig_plaas);
        단말.Skryf("\r\u001b["); 단말.수(bevelreël ? 16 : 7); 단말.Skryf("G\u001b[K");
        if (BEGIN_venster > 0) 단말.문자('<');
        for (int lus_INDEX = BEGIN_venster; lus_INDEX < beëindig_plaas; lus_INDEX++) bord.직렬쓰기(명령해석기.lyn[lus_INDEX]);
        단말.문자(beëindig_plaas < Grootte ? '>' : ' ');
        단말.Skryf("\u001b["); 단말.수(폭(loper_VALUE, beëindig_plaas) + 1); 단말.문자('D');
        가로보기 = BEGIN_venster > 0 || beëindig_plaas < Grootte || 폭(0, Grootte) > 보이는폭();
    }
    static void 기록넣기() {
        if (!bevelreël || Grootte == 0 || Grootte > 1024) return;
        if (LOG_COUNT > 0) {
            int 마지막자리 = (LOG_ry_beëindig + 15) % 16; boolean 같은여부 = LOG_lengte[마지막자리] == Grootte;
            for (int lus_INDEX = 0; 같은여부 && lus_INDEX < Grootte; lus_INDEX++) if (LOG_ry[마지막자리 * 1024 + lus_INDEX] != 명령해석기.lyn[lus_INDEX]) 같은여부 = false;
            if (같은여부) return;
        }
        LOG_lengte[LOG_ry_beëindig] = Grootte; for (int lus_INDEX = 0; lus_INDEX < Grootte; lus_INDEX++) LOG_ry[LOG_ry_beëindig * 1024 + lus_INDEX] = 명령해석기.lyn[lus_INDEX];
        LOG_ry_beëindig = (LOG_ry_beëindig + 1) % 16; if (LOG_COUNT < 16) LOG_COUNT++;
    }
    static void 기록이동(int DELTA_VALUE) {
        if (!bevelreël) return;
        if (Soek_VALUE == 0 && DELTA_VALUE > 0) { 저장길이 = Grootte; for (int lus_INDEX = 0; lus_INDEX < Grootte; lus_INDEX++) bêre_VALUE[lus_INDEX] = 명령해석기.lyn[lus_INDEX]; }
        int Volgende_plaas = Soek_VALUE + DELTA_VALUE; if (Volgende_plaas < 0 || Volgende_plaas > LOG_COUNT) return; Soek_VALUE = Volgende_plaas;
        if (Soek_VALUE == 0) { Grootte = 저장길이; for (int lus_INDEX = 0; lus_INDEX < Grootte; lus_INDEX++) 명령해석기.lyn[lus_INDEX] = bêre_VALUE[lus_INDEX]; }
        else { int 보관칸 = (LOG_ry_beëindig + 16 - Soek_VALUE) % 16; Grootte = LOG_lengte[보관칸]; for (int lus_INDEX = 0; lus_INDEX < Grootte; lus_INDEX++) 명령해석기.lyn[lus_INDEX] = LOG_ry[보관칸 * 1024 + lus_INDEX]; }
        loper_VALUE = Grootte; 다시();
    }
    static void wys_LOG() {
        for (int inskrywing_COUNT = 0; inskrywing_COUNT < LOG_COUNT; inskrywing_COUNT++) {
            int 보관칸 = (LOG_ry_beëindig + 16 - LOG_COUNT + inskrywing_COUNT) % 16; 단말.수(inskrywing_COUNT + 1); 단말.Skryf("  ");
            for (int lus_INDEX = 0; lus_INDEX < LOG_lengte[보관칸]; lus_INDEX++) bord.직렬쓰기(LOG_ry[보관칸 * 1024 + lus_INDEX]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] data_ARRAY, int BEGIN_plaas, int inskrywing_COUNT, int 접두말, int 총수, boolean 폴더번호) {
        if (inskrywing_COUNT < 총수 || inskrywing_COUNT > 62) return;
        for (int lus_INDEX = 0; lus_INDEX < 총수; lus_INDEX++) if (data_ARRAY[BEGIN_plaas + lus_INDEX] != 명령해석기.lyn[접두말 + lus_INDEX]) return;
        후보수++; 후보길이 = inskrywing_COUNT + 1;
        for (int lus_INDEX = 0; lus_INDEX < inskrywing_COUNT; lus_INDEX++) 후보[lus_INDEX] = data_ARRAY[BEGIN_plaas + lus_INDEX]; 후보[inskrywing_COUNT] = 폴더번호 ? '/' : ' ';
    }
    static void 완성() {
        if (!bevelreël || loper_VALUE != Grootte) return;
        int 시작점 = Grootte; while (시작점 > 0 && 명령해석기.lyn[시작점 - 1] != ' ') 시작점--;
        for (int lus_INDEX = 시작점; lus_INDEX < Grootte; lus_INDEX++) if (명령해석기.lyn[lus_INDEX] == '/' || 명령해석기.lyn[lus_INDEX] == '"' || 명령해석기.lyn[lus_INDEX] == 39 || 명령해석기.lyn[lus_INDEX] == '\\') return;
        후보수 = 0; int inskrywing_COUNT = Grootte - 시작점;
        if (시작점 == 0) {
            for(int Lys_INDEX=0;Lys_INDEX<2;Lys_INDEX++) {
                String inskrywing_Lys=Lys_INDEX==0?명령들:관리명령.완성어();
                int 읽는자리=0;
                while(읽는자리<inskrywing_Lys.length()) {
                    int beëindig_plaas=읽는자리;while(beëindig_plaas<inskrywing_Lys.length() && inskrywing_Lys.charAt(beëindig_plaas)!=' ')beëindig_plaas++;
                    명령후보넣기(inskrywing_Lys,읽는자리,beëindig_plaas,inskrywing_COUNT);읽는자리=beëindig_plaas+1;
                }
            }
        } else {
            Geheue_Lêers.pad_BEGIN(1); Geheue_Lêers.pad_greep(0, '.'); Geheue_Lêers.normaliseer_VALUE();
            for (int lus_INDEX = 0; lus_INDEX < Geheue_Lêers.lêer_COUNT; lus_INDEX++) {
                int BEGIN_plaas = Geheue_Lêers.inskrywing_BEGIN(Geheue_Lêers.Naam, lus_INDEX * 64, Geheue_Lêers.이름길이[lus_INDEX]);
                if (BEGIN_plaas >= 0) 후보넣기(Geheue_Lêers.Naam, lus_INDEX * 64 + BEGIN_plaas, Geheue_Lêers.이름길이[lus_INDEX] - BEGIN_plaas, 시작점, inskrywing_COUNT, false);
            }
            for (int lus_INDEX = 0; lus_INDEX < 16; lus_INDEX++) {
                int BEGIN_plaas = Geheue_Lêers.inskrywing_BEGIN(Geheue_Lêers.gids_naam, lus_INDEX * 64, Geheue_Lêers.gids_lengte[lus_INDEX]);
                if (BEGIN_plaas >= 0) 후보넣기(Geheue_Lêers.gids_naam, lus_INDEX * 64 + BEGIN_plaas, Geheue_Lêers.gids_lengte[lus_INDEX] - BEGIN_plaas, 시작점, inskrywing_COUNT, true);
            }
        }
        if (후보수 != 1) { bord.직렬쓰기(7); return; }
        for (int lus_INDEX = inskrywing_COUNT; lus_INDEX < 후보길이 && Grootte < 명령해석기.lyn.length - 1; lus_INDEX++) {
            if (후보[lus_INDEX] == ' ' && lus_INDEX != 후보길이 - 1) 명령해석기.lyn[Grootte++] = '\\';
            명령해석기.lyn[Grootte++] = 후보[lus_INDEX];
        }
        loper_VALUE = Grootte; 다시();
    }
    static int 탈출읽기() {
        int 시작점 = bord.밀리초();
        while (bord.밀리초() - 시작점 < 80) { int greep_data = bord.직렬읽기(); if (greep_data >= 0) return greep_data; bord.YIELD_SVE(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int inskrywing_COUNT = 0, beëindig_plaas = -1;
        for (int lus_INDEX = 0; lus_INDEX < 12; lus_INDEX++) { int greep_data = 탈출읽기(); if (greep_data < 0) return; if (greep_data >= '0' && greep_data <= '9') inskrywing_COUNT = inskrywing_COUNT * 10 + greep_data - '0'; else { beëindig_plaas = greep_data; break; } }
        if (beëindig_plaas == 'A') 기록이동(1);
        else if (beëindig_plaas == 'B') 기록이동(-1);
        else if (beëindig_plaas == 'C') { loper_VALUE = TERUG_VALUE(loper_VALUE); 다시(); }
        else if (beëindig_plaas == 'D') { loper_VALUE = voor_VALUE(loper_VALUE); 다시(); }
        else if (beëindig_plaas == 'H' || beëindig_plaas == '~' && (inskrywing_COUNT == 1 || inskrywing_COUNT == 7)) { loper_VALUE = 0; 다시(); }
        else if (beëindig_plaas == 'F' || beëindig_plaas == '~' && (inskrywing_COUNT == 4 || inskrywing_COUNT == 8)) { loper_VALUE = Grootte; 다시(); }
        else if (beëindig_plaas == '~' && inskrywing_COUNT == 3 && loper_VALUE < Grootte) {
            int Volgende_plaas = TERUG_VALUE(loper_VALUE); for (int lus_INDEX = Volgende_plaas; lus_INDEX < Grootte; lus_INDEX++) 명령해석기.lyn[lus_INDEX - Volgende_plaas + loper_VALUE] = 명령해석기.lyn[lus_INDEX]; Grootte -= Volgende_plaas - loper_VALUE; 다시();
        }
        else if (beëindig_plaas == '~' && (inskrywing_COUNT == 5 || inskrywing_COUNT == 6)) bord.Terminaal(inskrywing_COUNT == 5 ? 5 : 6);
        else if (beëindig_plaas == '~' && inskrywing_COUNT == 24 && bevelreël) { 명령해석기.Terminaal(true); }
    }
    static int Lees() {
        if (!venster_sessie.이어읽기) { Grootte = loper_VALUE = Soek_VALUE = BEGIN_venster = 0; 가로보기 = false; }
        else { venster_sessie.이어읽기 = false; 다시(); } boolean oorloop = false;
        while (true) {
            int greep_data = bord.직렬읽기(); if (greep_data == -4096) return -3;
            if (bord.Terminaal(14) != 0) 다시(); if (greep_data < 0) { bord.YIELD_SVE(); continue; }
            if (greep_data == 10 && 명령해석기.앞줄) { 명령해석기.앞줄 = false; continue; } 명령해석기.앞줄 = greep_data == 13;
            if (greep_data == 27) { 탈출(); continue; }
            if (greep_data == 3) { 단말.Skryf("^C\n"); return -1; }
            if (greep_data == 4 && Grootte == 0 && bevelreël) { if (bord.Terminaal(2) != 0) 명령해석기.Terminaal(true); return -1; }
            if (greep_data == 13 || greep_data == 10) { 단말.문자(10); if (!oorloop) 기록넣기(); return oorloop ? -2 : Grootte; }
            if (greep_data == 9 && bevelreël) { 완성(); continue; }
            if (greep_data == 1 || greep_data == 5) { loper_VALUE = greep_data == 1 ? 0 : Grootte; 다시(); continue; }
            if (greep_data == 8 || greep_data == 127 || greep_data == 21) {
                if (greep_data == 21) { for (int lus_INDEX = loper_VALUE; lus_INDEX < Grootte; lus_INDEX++) 명령해석기.lyn[lus_INDEX - loper_VALUE] = 명령해석기.lyn[lus_INDEX]; Grootte -= loper_VALUE; loper_VALUE = 0; }
                else if (loper_VALUE > 0) { int 변경전 = voor_VALUE(loper_VALUE); for (int lus_INDEX = loper_VALUE; lus_INDEX < Grootte; lus_INDEX++) 명령해석기.lyn[lus_INDEX - loper_VALUE + 변경전] = 명령해석기.lyn[lus_INDEX]; Grootte -= loper_VALUE - 변경전; loper_VALUE = 변경전; }
                다시(); continue;
            }
            if (greep_data == 11) { Grootte = loper_VALUE; 다시(); continue; }
            if (greep_data < 32 && greep_data != 9) continue;
            if (Grootte == 명령해석기.lyn.length) { oorloop = true; continue; }
            for (int lus_INDEX = Grootte; lus_INDEX > loper_VALUE; lus_INDEX--) 명령해석기.lyn[lus_INDEX] = 명령해석기.lyn[lus_INDEX - 1];
            명령해석기.lyn[loper_VALUE++] = greep_data; Grootte++;
            if (loper_VALUE == Grootte && !가로보기 && 폭(0, Grootte) <= 보이는폭()) bord.직렬쓰기(greep_data);
            else if (loper_VALUE == Grootte) 보이는줄(); else 다시();
        }
    }
}
