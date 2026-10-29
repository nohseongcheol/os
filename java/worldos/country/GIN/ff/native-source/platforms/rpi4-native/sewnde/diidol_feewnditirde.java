// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 oktee_njaru 경계를 지키는 삽입/삭제, 방향키, ginol suurnal_winndande, Tab 완성. */
public final class diidol_feewnditirde {
    static boolean ɓoggol_ginorde;
    static int[] suurnal_winndande = new int[16 * 1024], suurnal_njuuteendi = new int[16], resde_njaru = new int[4096], 후보 = new int[64];
    static int 기록수, suurnal_winndande_taƴde, njiilawu_njaru, 저장길이, waylude_etannde, kirseer_njaru, 후보수, 후보길이, huɓɓude_falanteere;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd 보안셸 원격화면 run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String naatnugol_Doggol, int 시작자리, int 끝자리, int 입력길이) {
        int 바이트수=0;
        for(int 자리=시작자리;자리<끝자리;자리++) {
            int 문자값=naatnugol_Doggol.charAt(자리);
            if(문자값>=0xd800 && 문자값<=0xdbff && 자리+1<끝자리)문자값=0x10000+((문자값-0xd800)<<10)+naatnugol_Doggol.charAt(++자리)-0xdc00;
            int 수=문자값<128?1:문자값<2048?2:문자값<65536?3:4;
            if(바이트수+수>62)return;
            for(int 차례=수-1;차례>=0;차례--)명령후보[바이트수++]=수==1?문자값:차례==수-1?(수==2?0xc0:수==3?0xe0:0xf0)|(문자값>>(6*차례)):0x80|((문자값>>(6*차례))&63);
        }
        if(바이트수<입력길이)return;
        for(int 자리=0;자리<입력길이;자리++)if(명령후보[자리]!=명령해석기.diidol[자리])return;
        후보수++;후보길이=바이트수+1;
        for(int 자리=0;자리<바이트수;자리++)후보[자리]=명령후보[자리];후보[바이트수]=' ';
    }
    static int 앞(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (명령해석기.diidol[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int Caggal_njaru(int 읽는자리) { if (읽는자리 < waylude_etannde) { 읽는자리++; while (읽는자리 < waylude_etannde && (명령해석기.diidol[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int 시작자리, int tiindaare_njaru_joopirdu) {
        int 글칸수 = 0;
        for (int kowal_joopirdu = 시작자리; kowal_joopirdu < tiindaare_njaru_joopirdu; kowal_joopirdu++) { int oktee_keɓe = 명령해석기.diidol[kowal_joopirdu]; if ((oktee_keɓe & 192) == 128) continue; 글칸수 += oktee_keɓe >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void 다시() {
        단말.winndude("\r\u001b[2K");
        단말.winndude(ɓoggol_ginorde ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 diidol 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int 열수 = 보드.터미널(13) & 65535; return 열수 - (ɓoggol_ginorde ? 18 : 9); }
    static void 보이는줄() {
        if (kirseer_njaru < huɓɓude_falanteere) huɓɓude_falanteere = kirseer_njaru;
        while (폭(huɓɓude_falanteere, kirseer_njaru) > 보이는폭()) huɓɓude_falanteere = Caggal_njaru(huɓɓude_falanteere);
        int 끝자리 = huɓɓude_falanteere;
        while (끝자리 < waylude_etannde && 폭(huɓɓude_falanteere, Caggal_njaru(끝자리)) <= 보이는폭()) 끝자리 = Caggal_njaru(끝자리);
        단말.winndude("\r\u001b["); 단말.수(ɓoggol_ginorde ? 16 : 7); 단말.winndude("G\u001b[K");
        if (huɓɓude_falanteere > 0) 단말.문자('<');
        for (int kowal_joopirdu = huɓɓude_falanteere; kowal_joopirdu < 끝자리; kowal_joopirdu++) 보드.직렬쓰기(명령해석기.diidol[kowal_joopirdu]);
        단말.문자(끝자리 < waylude_etannde ? '>' : ' ');
        단말.winndude("\u001b["); 단말.수(폭(kirseer_njaru, 끝자리) + 1); 단말.문자('D');
        가로보기 = huɓɓude_falanteere > 0 || 끝자리 < waylude_etannde || 폭(0, waylude_etannde) > 보이는폭();
    }
    static void 기록넣기() {
        if (!ɓoggol_ginorde || waylude_etannde == 0 || waylude_etannde > 1024) return;
        if (기록수 > 0) {
            int 마지막자리 = (suurnal_winndande_taƴde + 15) % 16; boolean 같은여부 = suurnal_njuuteendi[마지막자리] == waylude_etannde;
            for (int kowal_joopirdu = 0; 같은여부 && kowal_joopirdu < waylude_etannde; kowal_joopirdu++) if (suurnal_winndande[마지막자리 * 1024 + kowal_joopirdu] != 명령해석기.diidol[kowal_joopirdu]) 같은여부 = false;
            if (같은여부) return;
        }
        suurnal_njuuteendi[suurnal_winndande_taƴde] = waylude_etannde; for (int kowal_joopirdu = 0; kowal_joopirdu < waylude_etannde; kowal_joopirdu++) suurnal_winndande[suurnal_winndande_taƴde * 1024 + kowal_joopirdu] = 명령해석기.diidol[kowal_joopirdu];
        suurnal_winndande_taƴde = (suurnal_winndande_taƴde + 1) % 16; if (기록수 < 16) 기록수++;
    }
    static void 기록이동(int 변화량) {
        if (!ɓoggol_ginorde) return;
        if (njiilawu_njaru == 0 && 변화량 > 0) { 저장길이 = waylude_etannde; for (int kowal_joopirdu = 0; kowal_joopirdu < waylude_etannde; kowal_joopirdu++) resde_njaru[kowal_joopirdu] = 명령해석기.diidol[kowal_joopirdu]; }
        int 다음자리 = njiilawu_njaru + 변화량; if (다음자리 < 0 || 다음자리 > 기록수) return; njiilawu_njaru = 다음자리;
        if (njiilawu_njaru == 0) { waylude_etannde = 저장길이; for (int kowal_joopirdu = 0; kowal_joopirdu < waylude_etannde; kowal_joopirdu++) 명령해석기.diidol[kowal_joopirdu] = resde_njaru[kowal_joopirdu]; }
        else { int 보관칸 = (suurnal_winndande_taƴde + 16 - njiilawu_njaru) % 16; waylude_etannde = suurnal_njuuteendi[보관칸]; for (int kowal_joopirdu = 0; kowal_joopirdu < waylude_etannde; kowal_joopirdu++) 명령해석기.diidol[kowal_joopirdu] = suurnal_winndande[보관칸 * 1024 + kowal_joopirdu]; }
        kirseer_njaru = waylude_etannde; 다시();
    }
    static void hollirde_suurnal() {
        for (int 항목수 = 0; 항목수 < 기록수; 항목수++) {
            int 보관칸 = (suurnal_winndande_taƴde + 16 - 기록수 + 항목수) % 16; 단말.수(항목수 + 1); 단말.winndude("  ");
            for (int kowal_joopirdu = 0; kowal_joopirdu < suurnal_njuuteendi[보관칸]; kowal_joopirdu++) 보드.직렬쓰기(suurnal_winndande[보관칸 * 1024 + kowal_joopirdu]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] 자료배열, int 시작자리, int 항목수, int 접두말, int 총수, boolean 폴더번호) {
        if (항목수 < 총수 || 항목수 > 62) return;
        for (int kowal_joopirdu = 0; kowal_joopirdu < 총수; kowal_joopirdu++) if (자료배열[시작자리 + kowal_joopirdu] != 명령해석기.diidol[접두말 + kowal_joopirdu]) return;
        후보수++; 후보길이 = 항목수 + 1;
        for (int kowal_joopirdu = 0; kowal_joopirdu < 항목수; kowal_joopirdu++) 후보[kowal_joopirdu] = 자료배열[시작자리 + kowal_joopirdu]; 후보[항목수] = 폴더번호 ? '/' : ' ';
    }
    static void 완성() {
        if (!ɓoggol_ginorde || kirseer_njaru != waylude_etannde) return;
        int 시작점 = waylude_etannde; while (시작점 > 0 && 명령해석기.diidol[시작점 - 1] != ' ') 시작점--;
        for (int kowal_joopirdu = 시작점; kowal_joopirdu < waylude_etannde; kowal_joopirdu++) if (명령해석기.diidol[kowal_joopirdu] == '/' || 명령해석기.diidol[kowal_joopirdu] == '"' || 명령해석기.diidol[kowal_joopirdu] == 39 || 명령해석기.diidol[kowal_joopirdu] == '\\') return;
        후보수 = 0; int 항목수 = waylude_etannde - 시작점;
        if (시작점 == 0) {
            for(int Doggol_joopirdu=0;Doggol_joopirdu<2;Doggol_joopirdu++) {
                String naatnugol_Doggol=Doggol_joopirdu==0?명령들:관리명령.완성어();
                int 읽는자리=0;
                while(읽는자리<naatnugol_Doggol.length()) {
                    int 끝자리=읽는자리;while(끝자리<naatnugol_Doggol.length() && naatnugol_Doggol.charAt(끝자리)!=' ')끝자리++;
                    명령후보넣기(naatnugol_Doggol,읽는자리,끝자리,항목수);읽는자리=끝자리+1;
                }
            }
        } else {
            기억파일.laawol_huɓɓude(1); 기억파일.laawol_oktee(0, '.'); 기억파일.정규화();
            for (int kowal_joopirdu = 0; kowal_joopirdu < 기억파일.파일수; kowal_joopirdu++) {
                int 시작자리 = 기억파일.naatnugol_huɓɓude(기억파일.innde, kowal_joopirdu * 64, 기억파일.이름길이[kowal_joopirdu]);
                if (시작자리 >= 0) 후보넣기(기억파일.innde, kowal_joopirdu * 64 + 시작자리, 기억파일.이름길이[kowal_joopirdu] - 시작자리, 시작점, 항목수, false);
            }
            for (int kowal_joopirdu = 0; kowal_joopirdu < 16; kowal_joopirdu++) {
                int 시작자리 = 기억파일.naatnugol_huɓɓude(기억파일.mooftordu_innde, kowal_joopirdu * 64, 기억파일.mooftordu_njuuteendi[kowal_joopirdu]);
                if (시작자리 >= 0) 후보넣기(기억파일.mooftordu_innde, kowal_joopirdu * 64 + 시작자리, 기억파일.mooftordu_njuuteendi[kowal_joopirdu] - 시작자리, 시작점, 항목수, true);
            }
        }
        if (후보수 != 1) { 보드.직렬쓰기(7); return; }
        for (int kowal_joopirdu = 항목수; kowal_joopirdu < 후보길이 && waylude_etannde < 명령해석기.diidol.length - 1; kowal_joopirdu++) {
            if (후보[kowal_joopirdu] == ' ' && kowal_joopirdu != 후보길이 - 1) 명령해석기.diidol[waylude_etannde++] = '\\';
            명령해석기.diidol[waylude_etannde++] = 후보[kowal_joopirdu];
        }
        kirseer_njaru = waylude_etannde; 다시();
    }
    static int 탈출읽기() {
        int 시작점 = 보드.밀리초();
        while (보드.밀리초() - 시작점 < 80) { int oktee_keɓe = 보드.직렬읽기(); if (oktee_keɓe >= 0) return oktee_keɓe; 보드.양보(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int 항목수 = 0, 끝자리 = -1;
        for (int kowal_joopirdu = 0; kowal_joopirdu < 12; kowal_joopirdu++) { int oktee_keɓe = 탈출읽기(); if (oktee_keɓe < 0) return; if (oktee_keɓe >= '0' && oktee_keɓe <= '9') 항목수 = 항목수 * 10 + oktee_keɓe - '0'; else { 끝자리 = oktee_keɓe; break; } }
        if (끝자리 == 'A') 기록이동(1);
        else if (끝자리 == 'B') 기록이동(-1);
        else if (끝자리 == 'C') { kirseer_njaru = Caggal_njaru(kirseer_njaru); 다시(); }
        else if (끝자리 == 'D') { kirseer_njaru = 앞(kirseer_njaru); 다시(); }
        else if (끝자리 == 'H' || 끝자리 == '~' && (항목수 == 1 || 항목수 == 7)) { kirseer_njaru = 0; 다시(); }
        else if (끝자리 == 'F' || 끝자리 == '~' && (항목수 == 4 || 항목수 == 8)) { kirseer_njaru = waylude_etannde; 다시(); }
        else if (끝자리 == '~' && 항목수 == 3 && kirseer_njaru < waylude_etannde) {
            int 다음자리 = Caggal_njaru(kirseer_njaru); for (int kowal_joopirdu = 다음자리; kowal_joopirdu < waylude_etannde; kowal_joopirdu++) 명령해석기.diidol[kowal_joopirdu - 다음자리 + kirseer_njaru] = 명령해석기.diidol[kowal_joopirdu]; waylude_etannde -= 다음자리 - kirseer_njaru; 다시();
        }
        else if (끝자리 == '~' && (항목수 == 5 || 항목수 == 6)) 보드.터미널(항목수 == 5 ? 5 : 6);
        else if (끝자리 == '~' && 항목수 == 24 && ɓoggol_ginorde) { 명령해석기.터미널(true); }
    }
    static int 읽기() {
        if (!falanteere_jokkondiral.이어읽기) { waylude_etannde = kirseer_njaru = njiilawu_njaru = huɓɓude_falanteere = 0; 가로보기 = false; }
        else { falanteere_jokkondiral.이어읽기 = false; 다시(); } boolean binndi_ɓurtuɗi = false;
        while (true) {
            int oktee_keɓe = 보드.직렬읽기(); if (oktee_keɓe == -4096) return -3;
            if (보드.터미널(14) != 0) 다시(); if (oktee_keɓe < 0) { 보드.양보(); continue; }
            if (oktee_keɓe == 10 && 명령해석기.앞줄) { 명령해석기.앞줄 = false; continue; } 명령해석기.앞줄 = oktee_keɓe == 13;
            if (oktee_keɓe == 27) { 탈출(); continue; }
            if (oktee_keɓe == 3) { 단말.winndude("^C\n"); return -1; }
            if (oktee_keɓe == 4 && waylude_etannde == 0 && ɓoggol_ginorde) { if (보드.터미널(2) != 0) 명령해석기.터미널(true); return -1; }
            if (oktee_keɓe == 13 || oktee_keɓe == 10) { 단말.문자(10); if (!binndi_ɓurtuɗi) 기록넣기(); return binndi_ɓurtuɗi ? -2 : waylude_etannde; }
            if (oktee_keɓe == 9 && ɓoggol_ginorde) { 완성(); continue; }
            if (oktee_keɓe == 1 || oktee_keɓe == 5) { kirseer_njaru = oktee_keɓe == 1 ? 0 : waylude_etannde; 다시(); continue; }
            if (oktee_keɓe == 8 || oktee_keɓe == 127 || oktee_keɓe == 21) {
                if (oktee_keɓe == 21) { for (int kowal_joopirdu = kirseer_njaru; kowal_joopirdu < waylude_etannde; kowal_joopirdu++) 명령해석기.diidol[kowal_joopirdu - kirseer_njaru] = 명령해석기.diidol[kowal_joopirdu]; waylude_etannde -= kirseer_njaru; kirseer_njaru = 0; }
                else if (kirseer_njaru > 0) { int 변경전 = 앞(kirseer_njaru); for (int kowal_joopirdu = kirseer_njaru; kowal_joopirdu < waylude_etannde; kowal_joopirdu++) 명령해석기.diidol[kowal_joopirdu - kirseer_njaru + 변경전] = 명령해석기.diidol[kowal_joopirdu]; waylude_etannde -= kirseer_njaru - 변경전; kirseer_njaru = 변경전; }
                다시(); continue;
            }
            if (oktee_keɓe == 11) { waylude_etannde = kirseer_njaru; 다시(); continue; }
            if (oktee_keɓe < 32 && oktee_keɓe != 9) continue;
            if (waylude_etannde == 명령해석기.diidol.length) { binndi_ɓurtuɗi = true; continue; }
            for (int kowal_joopirdu = waylude_etannde; kowal_joopirdu > kirseer_njaru; kowal_joopirdu--) 명령해석기.diidol[kowal_joopirdu] = 명령해석기.diidol[kowal_joopirdu - 1];
            명령해석기.diidol[kirseer_njaru++] = oktee_keɓe; waylude_etannde++;
            if (kirseer_njaru == waylude_etannde && !가로보기 && 폭(0, waylude_etannde) <= 보이는폭()) 보드.직렬쓰기(oktee_keɓe);
            else if (kirseer_njaru == waylude_etannde) 보이는줄(); else 다시();
        }
    }
}
