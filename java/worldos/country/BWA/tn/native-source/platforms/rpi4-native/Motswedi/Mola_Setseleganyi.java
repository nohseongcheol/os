// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 baete_Boleng 경계를 지키는 삽입/삭제, 방향키, Taelo rekota_mola, Tab 완성. */
public final class Mola_Setseleganyi {
    static boolean mokwalotaelo;
    static int[] rekota_mola = new int[16 * 1024], rekota_boleele = new int[16], Store_Boleng = new int[4096], 후보 = new int[64];
    static int 기록수, rekota_mola_kgaola, batla_Boleng, 저장길이, lekanya, khesara_Boleng, 후보수, 후보길이, simolola_fensetere;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd sireletsegile_setlhalosataelo kgakala_bontsha run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String tsenyo_lenaane, int 시작자리, int 끝자리, int 입력길이) {
        int 바이트수=0;
        for(int 자리=시작자리;자리<끝자리;자리++) {
            int khoutuletshwao=tsenyo_lenaane.charAt(자리);
            if(khoutuletshwao>=0xd800 && khoutuletshwao<=0xdbff && 자리+1<끝자리)khoutuletshwao=0x10000+((khoutuletshwao-0xd800)<<10)+tsenyo_lenaane.charAt(++자리)-0xdc00;
            int 수=khoutuletshwao<128?1:khoutuletshwao<2048?2:khoutuletshwao<65536?3:4;
            if(바이트수+수>62)return;
            for(int TATELANO_Boleng=수-1;TATELANO_Boleng>=0;TATELANO_Boleng--)명령후보[바이트수++]=수==1?khoutuletshwao:TATELANO_Boleng==수-1?(수==2?0xc0:수==3?0xe0:0xf0)|(khoutuletshwao>>(6*TATELANO_Boleng)):0x80|((khoutuletshwao>>(6*TATELANO_Boleng))&63);
        }
        if(바이트수<입력길이)return;
        for(int 자리=0;자리<입력길이;자리++)if(명령후보[자리]!=명령해석기.Mola[자리])return;
        후보수++;후보길이=바이트수+1;
        for(int 자리=0;자리<바이트수;자리++)후보[자리]=명령후보[자리];후보[바이트수]=' ';
    }
    static int 앞(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (명령해석기.Mola[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int Morago_Boleng(int 읽는자리) { if (읽는자리 < lekanya) { 읽는자리++; while (읽는자리 < lekanya && (명령해석기.Mola[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int 시작자리, int bogorogelo_Boleng_tshupane) {
        int 글칸수 = 0;
        for (int lupu_tshupane = 시작자리; lupu_tshupane < bogorogelo_Boleng_tshupane; lupu_tshupane++) { int baete_tshedimosetso = 명령해석기.Mola[lupu_tshupane]; if ((baete_tshedimosetso & 192) == 128) continue; 글칸수 += baete_tshedimosetso >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void 다시() {
        단말.kwala("\r\u001b[2K");
        단말.kwala(mokwalotaelo ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 Mola 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int 열수 = 보드.터미널(13) & 65535; return 열수 - (mokwalotaelo ? 18 : 9); }
    static void 보이는줄() {
        if (khesara_Boleng < simolola_fensetere) simolola_fensetere = khesara_Boleng;
        while (폭(simolola_fensetere, khesara_Boleng) > 보이는폭()) simolola_fensetere = Morago_Boleng(simolola_fensetere);
        int 끝자리 = simolola_fensetere;
        while (끝자리 < lekanya && 폭(simolola_fensetere, Morago_Boleng(끝자리)) <= 보이는폭()) 끝자리 = Morago_Boleng(끝자리);
        단말.kwala("\r\u001b["); 단말.수(mokwalotaelo ? 16 : 7); 단말.kwala("G\u001b[K");
        if (simolola_fensetere > 0) 단말.문자('<');
        for (int lupu_tshupane = simolola_fensetere; lupu_tshupane < 끝자리; lupu_tshupane++) 보드.직렬쓰기(명령해석기.Mola[lupu_tshupane]);
        단말.문자(끝자리 < lekanya ? '>' : ' ');
        단말.kwala("\u001b["); 단말.수(폭(khesara_Boleng, 끝자리) + 1); 단말.문자('D');
        가로보기 = simolola_fensetere > 0 || 끝자리 < lekanya || 폭(0, lekanya) > 보이는폭();
    }
    static void 기록넣기() {
        if (!mokwalotaelo || lekanya == 0 || lekanya > 1024) return;
        if (기록수 > 0) {
            int 마지막자리 = (rekota_mola_kgaola + 15) % 16; boolean 같은여부 = rekota_boleele[마지막자리] == lekanya;
            for (int lupu_tshupane = 0; 같은여부 && lupu_tshupane < lekanya; lupu_tshupane++) if (rekota_mola[마지막자리 * 1024 + lupu_tshupane] != 명령해석기.Mola[lupu_tshupane]) 같은여부 = false;
            if (같은여부) return;
        }
        rekota_boleele[rekota_mola_kgaola] = lekanya; for (int lupu_tshupane = 0; lupu_tshupane < lekanya; lupu_tshupane++) rekota_mola[rekota_mola_kgaola * 1024 + lupu_tshupane] = 명령해석기.Mola[lupu_tshupane];
        rekota_mola_kgaola = (rekota_mola_kgaola + 1) % 16; if (기록수 < 16) 기록수++;
    }
    static void 기록이동(int 변화량) {
        if (!mokwalotaelo) return;
        if (batla_Boleng == 0 && 변화량 > 0) { 저장길이 = lekanya; for (int lupu_tshupane = 0; lupu_tshupane < lekanya; lupu_tshupane++) Store_Boleng[lupu_tshupane] = 명령해석기.Mola[lupu_tshupane]; }
        int 다음자리 = batla_Boleng + 변화량; if (다음자리 < 0 || 다음자리 > 기록수) return; batla_Boleng = 다음자리;
        if (batla_Boleng == 0) { lekanya = 저장길이; for (int lupu_tshupane = 0; lupu_tshupane < lekanya; lupu_tshupane++) 명령해석기.Mola[lupu_tshupane] = Store_Boleng[lupu_tshupane]; }
        else { int 보관칸 = (rekota_mola_kgaola + 16 - batla_Boleng) % 16; lekanya = rekota_boleele[보관칸]; for (int lupu_tshupane = 0; lupu_tshupane < lekanya; lupu_tshupane++) 명령해석기.Mola[lupu_tshupane] = rekota_mola[보관칸 * 1024 + lupu_tshupane]; }
        khesara_Boleng = lekanya; 다시();
    }
    static void bontsha_rekota() {
        for (int 항목수 = 0; 항목수 < 기록수; 항목수++) {
            int 보관칸 = (rekota_mola_kgaola + 16 - 기록수 + 항목수) % 16; 단말.수(항목수 + 1); 단말.kwala("  ");
            for (int lupu_tshupane = 0; lupu_tshupane < rekota_boleele[보관칸]; lupu_tshupane++) 보드.직렬쓰기(rekota_mola[보관칸 * 1024 + lupu_tshupane]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] tshedimosetso_setlhopha, int 시작자리, int 항목수, int 접두말, int 총수, boolean 폴더번호) {
        if (항목수 < 총수 || 항목수 > 62) return;
        for (int lupu_tshupane = 0; lupu_tshupane < 총수; lupu_tshupane++) if (tshedimosetso_setlhopha[시작자리 + lupu_tshupane] != 명령해석기.Mola[접두말 + lupu_tshupane]) return;
        후보수++; 후보길이 = 항목수 + 1;
        for (int lupu_tshupane = 0; lupu_tshupane < 항목수; lupu_tshupane++) 후보[lupu_tshupane] = tshedimosetso_setlhopha[시작자리 + lupu_tshupane]; 후보[항목수] = 폴더번호 ? '/' : ' ';
    }
    static void 완성() {
        if (!mokwalotaelo || khesara_Boleng != lekanya) return;
        int 시작점 = lekanya; while (시작점 > 0 && 명령해석기.Mola[시작점 - 1] != ' ') 시작점--;
        for (int lupu_tshupane = 시작점; lupu_tshupane < lekanya; lupu_tshupane++) if (명령해석기.Mola[lupu_tshupane] == '/' || 명령해석기.Mola[lupu_tshupane] == '"' || 명령해석기.Mola[lupu_tshupane] == 39 || 명령해석기.Mola[lupu_tshupane] == '\\') return;
        후보수 = 0; int 항목수 = lekanya - 시작점;
        if (시작점 == 0) {
            for(int lenaane_tshupane=0;lenaane_tshupane<2;lenaane_tshupane++) {
                String tsenyo_lenaane=lenaane_tshupane==0?명령들:관리명령.완성어();
                int 읽는자리=0;
                while(읽는자리<tsenyo_lenaane.length()) {
                    int 끝자리=읽는자리;while(끝자리<tsenyo_lenaane.length() && tsenyo_lenaane.charAt(끝자리)!=' ')끝자리++;
                    명령후보넣기(tsenyo_lenaane,읽는자리,끝자리,항목수);읽는자리=끝자리+1;
                }
            }
        } else {
            memori_Difaele.tsela_simolola(1); memori_Difaele.tsela_baete(0, '.'); memori_Difaele.fokotsa_ntsifatso_Boleng();
            for (int lupu_tshupane = 0; lupu_tshupane < memori_Difaele.파일수; lupu_tshupane++) {
                int 시작자리 = memori_Difaele.tsenyo_simolola(memori_Difaele.leina, lupu_tshupane * 64, memori_Difaele.이름길이[lupu_tshupane]);
                if (시작자리 >= 0) 후보넣기(memori_Difaele.leina, lupu_tshupane * 64 + 시작자리, memori_Difaele.이름길이[lupu_tshupane] - 시작자리, 시작점, 항목수, false);
            }
            for (int lupu_tshupane = 0; lupu_tshupane < 16; lupu_tshupane++) {
                int 시작자리 = memori_Difaele.tsenyo_simolola(memori_Difaele.Lenaneofaele_leina, lupu_tshupane * 64, memori_Difaele.Lenaneofaele_boleele[lupu_tshupane]);
                if (시작자리 >= 0) 후보넣기(memori_Difaele.Lenaneofaele_leina, lupu_tshupane * 64 + 시작자리, memori_Difaele.Lenaneofaele_boleele[lupu_tshupane] - 시작자리, 시작점, 항목수, true);
            }
        }
        if (후보수 != 1) { 보드.직렬쓰기(7); return; }
        for (int lupu_tshupane = 항목수; lupu_tshupane < 후보길이 && lekanya < 명령해석기.Mola.length - 1; lupu_tshupane++) {
            if (후보[lupu_tshupane] == ' ' && lupu_tshupane != 후보길이 - 1) 명령해석기.Mola[lekanya++] = '\\';
            명령해석기.Mola[lekanya++] = 후보[lupu_tshupane];
        }
        khesara_Boleng = lekanya; 다시();
    }
    static int 탈출읽기() {
        int 시작점 = 보드.밀리초();
        while (보드.밀리초() - 시작점 < 80) { int baete_tshedimosetso = 보드.직렬읽기(); if (baete_tshedimosetso >= 0) return baete_tshedimosetso; 보드.emisa_ka_nakwana_CPU(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int 항목수 = 0, 끝자리 = -1;
        for (int lupu_tshupane = 0; lupu_tshupane < 12; lupu_tshupane++) { int baete_tshedimosetso = 탈출읽기(); if (baete_tshedimosetso < 0) return; if (baete_tshedimosetso >= '0' && baete_tshedimosetso <= '9') 항목수 = 항목수 * 10 + baete_tshedimosetso - '0'; else { 끝자리 = baete_tshedimosetso; break; } }
        if (끝자리 == 'A') 기록이동(1);
        else if (끝자리 == 'B') 기록이동(-1);
        else if (끝자리 == 'C') { khesara_Boleng = Morago_Boleng(khesara_Boleng); 다시(); }
        else if (끝자리 == 'D') { khesara_Boleng = 앞(khesara_Boleng); 다시(); }
        else if (끝자리 == 'H' || 끝자리 == '~' && (항목수 == 1 || 항목수 == 7)) { khesara_Boleng = 0; 다시(); }
        else if (끝자리 == 'F' || 끝자리 == '~' && (항목수 == 4 || 항목수 == 8)) { khesara_Boleng = lekanya; 다시(); }
        else if (끝자리 == '~' && 항목수 == 3 && khesara_Boleng < lekanya) {
            int 다음자리 = Morago_Boleng(khesara_Boleng); for (int lupu_tshupane = 다음자리; lupu_tshupane < lekanya; lupu_tshupane++) 명령해석기.Mola[lupu_tshupane - 다음자리 + khesara_Boleng] = 명령해석기.Mola[lupu_tshupane]; lekanya -= 다음자리 - khesara_Boleng; 다시();
        }
        else if (끝자리 == '~' && (항목수 == 5 || 항목수 == 6)) 보드.터미널(항목수 == 5 ? 5 : 6);
        else if (끝자리 == '~' && 항목수 == 24 && mokwalotaelo) { 명령해석기.터미널(true); }
    }
    static int 읽기() {
        if (!fensetere_nakotiriso.이어읽기) { lekanya = khesara_Boleng = batla_Boleng = simolola_fensetere = 0; 가로보기 = false; }
        else { fensetere_nakotiriso.이어읽기 = false; 다시(); } boolean penologo = false;
        while (true) {
            int baete_tshedimosetso = 보드.직렬읽기(); if (baete_tshedimosetso == -4096) return -3;
            if (보드.터미널(14) != 0) 다시(); if (baete_tshedimosetso < 0) { 보드.emisa_ka_nakwana_CPU(); continue; }
            if (baete_tshedimosetso == 10 && 명령해석기.앞줄) { 명령해석기.앞줄 = false; continue; } 명령해석기.앞줄 = baete_tshedimosetso == 13;
            if (baete_tshedimosetso == 27) { 탈출(); continue; }
            if (baete_tshedimosetso == 3) { 단말.kwala("^C\n"); return -1; }
            if (baete_tshedimosetso == 4 && lekanya == 0 && mokwalotaelo) { if (보드.터미널(2) != 0) 명령해석기.터미널(true); return -1; }
            if (baete_tshedimosetso == 13 || baete_tshedimosetso == 10) { 단말.문자(10); if (!penologo) 기록넣기(); return penologo ? -2 : lekanya; }
            if (baete_tshedimosetso == 9 && mokwalotaelo) { 완성(); continue; }
            if (baete_tshedimosetso == 1 || baete_tshedimosetso == 5) { khesara_Boleng = baete_tshedimosetso == 1 ? 0 : lekanya; 다시(); continue; }
            if (baete_tshedimosetso == 8 || baete_tshedimosetso == 127 || baete_tshedimosetso == 21) {
                if (baete_tshedimosetso == 21) { for (int lupu_tshupane = khesara_Boleng; lupu_tshupane < lekanya; lupu_tshupane++) 명령해석기.Mola[lupu_tshupane - khesara_Boleng] = 명령해석기.Mola[lupu_tshupane]; lekanya -= khesara_Boleng; khesara_Boleng = 0; }
                else if (khesara_Boleng > 0) { int 변경전 = 앞(khesara_Boleng); for (int lupu_tshupane = khesara_Boleng; lupu_tshupane < lekanya; lupu_tshupane++) 명령해석기.Mola[lupu_tshupane - khesara_Boleng + 변경전] = 명령해석기.Mola[lupu_tshupane]; lekanya -= khesara_Boleng - 변경전; khesara_Boleng = 변경전; }
                다시(); continue;
            }
            if (baete_tshedimosetso == 11) { lekanya = khesara_Boleng; 다시(); continue; }
            if (baete_tshedimosetso < 32 && baete_tshedimosetso != 9) continue;
            if (lekanya == 명령해석기.Mola.length) { penologo = true; continue; }
            for (int lupu_tshupane = lekanya; lupu_tshupane > khesara_Boleng; lupu_tshupane--) 명령해석기.Mola[lupu_tshupane] = 명령해석기.Mola[lupu_tshupane - 1];
            명령해석기.Mola[khesara_Boleng++] = baete_tshedimosetso; lekanya++;
            if (khesara_Boleng == lekanya && !가로보기 && 폭(0, lekanya) <= 보이는폭()) 보드.직렬쓰기(baete_tshedimosetso);
            else if (khesara_Boleng == lekanya) 보이는줄(); else 다시();
        }
    }
}
