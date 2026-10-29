// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 waai_ajutuu 경계를 지키는 삽입/삭제, 방향키, aluwataaya aa_innachikimaajatü_aparatsee, Tab 완성. */
public final class liinia_anaatülü {
    static boolean liinia_aluwataayapala;
    static int[] aa_innachikimaajatü_aparatsee = new int[16 * 1024], aa_innachikimaajatü_akaliaa = new int[16], 저장 = new int[4096], 후보 = new int[64];
    static int 기록수, aa_innachikimaajatü_aparatsee_ajattiraa, Achajaaya_ajutuu, 저장길이, 크기, ee_iyatiaa_ajutuu, 후보수, 후보길이, achuwalaa_analaaya;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd 보안셸 원격화면 run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String 목록, int 시작자리, int 끝자리, int 입력길이) {
        int 바이트수=0;
        for(int 자리=시작자리;자리<끝자리;자리++) {
            int 문자값=목록.charAt(자리);
            if(문자값>=0xd800 && 문자값<=0xdbff && 자리+1<끝자리)문자값=0x10000+((문자값-0xd800)<<10)+목록.charAt(++자리)-0xdc00;
            int 수=문자값<128?1:문자값<2048?2:문자값<65536?3:4;
            if(바이트수+수>62)return;
            for(int 차례=수-1;차례>=0;차례--)명령후보[바이트수++]=수==1?문자값:차례==수-1?(수==2?0xc0:수==3?0xe0:0xf0)|(문자값>>(6*차례)):0x80|((문자값>>(6*차례))&63);
        }
        if(바이트수<입력길이)return;
        for(int 자리=0;자리<입력길이;자리++)if(명령후보[자리]!=명령해석기.liinia[자리])return;
        후보수++;후보길이=바이트수+1;
        for(int 자리=0;자리<바이트수;자리++)후보[자리]=명령후보[자리];후보[바이트수]=' ';
    }
    static int 앞(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (명령해석기.liinia[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int 뒤(int 읽는자리) { if (읽는자리 < 크기) { 읽는자리++; while (읽는자리 < 크기 && (명령해석기.liinia[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int 시작자리, int jalamüinjatü_ajutuu_ee_iyatialujuna) {
        int 글칸수 = 0;
        for (int eitawaakualü_ee_iyatialujuna = 시작자리; eitawaakualü_ee_iyatialujuna < jalamüinjatü_ajutuu_ee_iyatialujuna; eitawaakualü_ee_iyatialujuna++) { int waai_atijaaya = 명령해석기.liinia[eitawaakualü_ee_iyatialujuna]; if ((waai_atijaaya & 192) == 128) continue; 글칸수 += waai_atijaaya >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void 다시() {
        단말.ashajaa("\r\u001b[2K");
        단말.ashajaa(liinia_aluwataayapala ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 liinia 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int 열수 = 보드.터미널(13) & 65535; return 열수 - (liinia_aluwataayapala ? 18 : 9); }
    static void 보이는줄() {
        if (ee_iyatiaa_ajutuu < achuwalaa_analaaya) achuwalaa_analaaya = ee_iyatiaa_ajutuu;
        while (폭(achuwalaa_analaaya, ee_iyatiaa_ajutuu) > 보이는폭()) achuwalaa_analaaya = 뒤(achuwalaa_analaaya);
        int 끝자리 = achuwalaa_analaaya;
        while (끝자리 < 크기 && 폭(achuwalaa_analaaya, 뒤(끝자리)) <= 보이는폭()) 끝자리 = 뒤(끝자리);
        단말.ashajaa("\r\u001b["); 단말.수(liinia_aluwataayapala ? 16 : 7); 단말.ashajaa("G\u001b[K");
        if (achuwalaa_analaaya > 0) 단말.문자('<');
        for (int eitawaakualü_ee_iyatialujuna = achuwalaa_analaaya; eitawaakualü_ee_iyatialujuna < 끝자리; eitawaakualü_ee_iyatialujuna++) 보드.직렬쓰기(명령해석기.liinia[eitawaakualü_ee_iyatialujuna]);
        단말.문자(끝자리 < 크기 ? '>' : ' ');
        단말.ashajaa("\u001b["); 단말.수(폭(ee_iyatiaa_ajutuu, 끝자리) + 1); 단말.문자('D');
        가로보기 = achuwalaa_analaaya > 0 || 끝자리 < 크기 || 폭(0, 크기) > 보이는폭();
    }
    static void 기록넣기() {
        if (!liinia_aluwataayapala || 크기 == 0 || 크기 > 1024) return;
        if (기록수 > 0) {
            int 마지막자리 = (aa_innachikimaajatü_aparatsee_ajattiraa + 15) % 16; boolean 같은여부 = aa_innachikimaajatü_akaliaa[마지막자리] == 크기;
            for (int eitawaakualü_ee_iyatialujuna = 0; 같은여부 && eitawaakualü_ee_iyatialujuna < 크기; eitawaakualü_ee_iyatialujuna++) if (aa_innachikimaajatü_aparatsee[마지막자리 * 1024 + eitawaakualü_ee_iyatialujuna] != 명령해석기.liinia[eitawaakualü_ee_iyatialujuna]) 같은여부 = false;
            if (같은여부) return;
        }
        aa_innachikimaajatü_akaliaa[aa_innachikimaajatü_aparatsee_ajattiraa] = 크기; for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 크기; eitawaakualü_ee_iyatialujuna++) aa_innachikimaajatü_aparatsee[aa_innachikimaajatü_aparatsee_ajattiraa * 1024 + eitawaakualü_ee_iyatialujuna] = 명령해석기.liinia[eitawaakualü_ee_iyatialujuna];
        aa_innachikimaajatü_aparatsee_ajattiraa = (aa_innachikimaajatü_aparatsee_ajattiraa + 1) % 16; if (기록수 < 16) 기록수++;
    }
    static void 기록이동(int 변화량) {
        if (!liinia_aluwataayapala) return;
        if (Achajaaya_ajutuu == 0 && 변화량 > 0) { 저장길이 = 크기; for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 크기; eitawaakualü_ee_iyatialujuna++) 저장[eitawaakualü_ee_iyatialujuna] = 명령해석기.liinia[eitawaakualü_ee_iyatialujuna]; }
        int 다음자리 = Achajaaya_ajutuu + 변화량; if (다음자리 < 0 || 다음자리 > 기록수) return; Achajaaya_ajutuu = 다음자리;
        if (Achajaaya_ajutuu == 0) { 크기 = 저장길이; for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 크기; eitawaakualü_ee_iyatialujuna++) 명령해석기.liinia[eitawaakualü_ee_iyatialujuna] = 저장[eitawaakualü_ee_iyatialujuna]; }
        else { int 보관칸 = (aa_innachikimaajatü_aparatsee_ajattiraa + 16 - Achajaaya_ajutuu) % 16; 크기 = aa_innachikimaajatü_akaliaa[보관칸]; for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 크기; eitawaakualü_ee_iyatialujuna++) 명령해석기.liinia[eitawaakualü_ee_iyatialujuna] = aa_innachikimaajatü_aparatsee[보관칸 * 1024 + eitawaakualü_ee_iyatialujuna]; }
        ee_iyatiaa_ajutuu = 크기; 다시();
    }
    static void 기록보기() {
        for (int 항목수 = 0; 항목수 < 기록수; 항목수++) {
            int 보관칸 = (aa_innachikimaajatü_aparatsee_ajattiraa + 16 - 기록수 + 항목수) % 16; 단말.수(항목수 + 1); 단말.ashajaa("  ");
            for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < aa_innachikimaajatü_akaliaa[보관칸]; eitawaakualü_ee_iyatialujuna++) 보드.직렬쓰기(aa_innachikimaajatü_aparatsee[보관칸 * 1024 + eitawaakualü_ee_iyatialujuna]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] atijaaya_matüriisü, int 시작자리, int 항목수, int 접두말, int 총수, boolean 폴더번호) {
        if (항목수 < 총수 || 항목수 > 62) return;
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 총수; eitawaakualü_ee_iyatialujuna++) if (atijaaya_matüriisü[시작자리 + eitawaakualü_ee_iyatialujuna] != 명령해석기.liinia[접두말 + eitawaakualü_ee_iyatialujuna]) return;
        후보수++; 후보길이 = 항목수 + 1;
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 항목수; eitawaakualü_ee_iyatialujuna++) 후보[eitawaakualü_ee_iyatialujuna] = atijaaya_matüriisü[시작자리 + eitawaakualü_ee_iyatialujuna]; 후보[항목수] = 폴더번호 ? '/' : ' ';
    }
    static void 완성() {
        if (!liinia_aluwataayapala || ee_iyatiaa_ajutuu != 크기) return;
        int 시작점 = 크기; while (시작점 > 0 && 명령해석기.liinia[시작점 - 1] != ' ') 시작점--;
        for (int eitawaakualü_ee_iyatialujuna = 시작점; eitawaakualü_ee_iyatialujuna < 크기; eitawaakualü_ee_iyatialujuna++) if (명령해석기.liinia[eitawaakualü_ee_iyatialujuna] == '/' || 명령해석기.liinia[eitawaakualü_ee_iyatialujuna] == '"' || 명령해석기.liinia[eitawaakualü_ee_iyatialujuna] == 39 || 명령해석기.liinia[eitawaakualü_ee_iyatialujuna] == '\\') return;
        후보수 = 0; int 항목수 = 크기 - 시작점;
        if (시작점 == 0) {
            for(int 목록번호=0;목록번호<2;목록번호++) {
                String 목록=목록번호==0?명령들:관리명령.완성어();
                int 읽는자리=0;
                while(읽는자리<목록.length()) {
                    int 끝자리=읽는자리;while(끝자리<목록.length() && 목록.charAt(끝자리)!=' ')끝자리++;
                    명령후보넣기(목록,읽는자리,끝자리,항목수);읽는자리=끝자리+1;
                }
            }
        } else {
            기억파일.wopu_a_ttaaleemüin_achuwalaa(1); 기억파일.wopu_a_ttaaleemüin_waai(0, '.'); 기억파일.anaajaa_ajutuu();
            for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 기억파일.파일수; eitawaakualü_ee_iyatialujuna++) {
                int 시작자리 = 기억파일.ekeroliaa_achuwalaa(기억파일.이름, eitawaakualü_ee_iyatialujuna * 64, 기억파일.이름길이[eitawaakualü_ee_iyatialujuna]);
                if (시작자리 >= 0) 후보넣기(기억파일.이름, eitawaakualü_ee_iyatialujuna * 64 + 시작자리, 기억파일.이름길이[eitawaakualü_ee_iyatialujuna] - 시작자리, 시작점, 항목수, false);
            }
            for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 16; eitawaakualü_ee_iyatialujuna++) {
                int 시작자리 = 기억파일.ekeroliaa_achuwalaa(기억파일.폴더이름, eitawaakualü_ee_iyatialujuna * 64, 기억파일.anaajaalee_akaliaa[eitawaakualü_ee_iyatialujuna]);
                if (시작자리 >= 0) 후보넣기(기억파일.폴더이름, eitawaakualü_ee_iyatialujuna * 64 + 시작자리, 기억파일.anaajaalee_akaliaa[eitawaakualü_ee_iyatialujuna] - 시작자리, 시작점, 항목수, true);
            }
        }
        if (후보수 != 1) { 보드.직렬쓰기(7); return; }
        for (int eitawaakualü_ee_iyatialujuna = 항목수; eitawaakualü_ee_iyatialujuna < 후보길이 && 크기 < 명령해석기.liinia.length - 1; eitawaakualü_ee_iyatialujuna++) {
            if (후보[eitawaakualü_ee_iyatialujuna] == ' ' && eitawaakualü_ee_iyatialujuna != 후보길이 - 1) 명령해석기.liinia[크기++] = '\\';
            명령해석기.liinia[크기++] = 후보[eitawaakualü_ee_iyatialujuna];
        }
        ee_iyatiaa_ajutuu = 크기; 다시();
    }
    static int 탈출읽기() {
        int 시작점 = 보드.밀리초();
        while (보드.밀리초() - 시작점 < 80) { int waai_atijaaya = 보드.직렬읽기(); if (waai_atijaaya >= 0) return waai_atijaaya; 보드.양보(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int 항목수 = 0, 끝자리 = -1;
        for (int eitawaakualü_ee_iyatialujuna = 0; eitawaakualü_ee_iyatialujuna < 12; eitawaakualü_ee_iyatialujuna++) { int waai_atijaaya = 탈출읽기(); if (waai_atijaaya < 0) return; if (waai_atijaaya >= '0' && waai_atijaaya <= '9') 항목수 = 항목수 * 10 + waai_atijaaya - '0'; else { 끝자리 = waai_atijaaya; break; } }
        if (끝자리 == 'A') 기록이동(1);
        else if (끝자리 == 'B') 기록이동(-1);
        else if (끝자리 == 'C') { ee_iyatiaa_ajutuu = 뒤(ee_iyatiaa_ajutuu); 다시(); }
        else if (끝자리 == 'D') { ee_iyatiaa_ajutuu = 앞(ee_iyatiaa_ajutuu); 다시(); }
        else if (끝자리 == 'H' || 끝자리 == '~' && (항목수 == 1 || 항목수 == 7)) { ee_iyatiaa_ajutuu = 0; 다시(); }
        else if (끝자리 == 'F' || 끝자리 == '~' && (항목수 == 4 || 항목수 == 8)) { ee_iyatiaa_ajutuu = 크기; 다시(); }
        else if (끝자리 == '~' && 항목수 == 3 && ee_iyatiaa_ajutuu < 크기) {
            int 다음자리 = 뒤(ee_iyatiaa_ajutuu); for (int eitawaakualü_ee_iyatialujuna = 다음자리; eitawaakualü_ee_iyatialujuna < 크기; eitawaakualü_ee_iyatialujuna++) 명령해석기.liinia[eitawaakualü_ee_iyatialujuna - 다음자리 + ee_iyatiaa_ajutuu] = 명령해석기.liinia[eitawaakualü_ee_iyatialujuna]; 크기 -= 다음자리 - ee_iyatiaa_ajutuu; 다시();
        }
        else if (끝자리 == '~' && (항목수 == 5 || 항목수 == 6)) 보드.터미널(항목수 == 5 ? 5 : 6);
        else if (끝자리 == '~' && 항목수 == 24 && liinia_aluwataayapala) { 명령해석기.터미널(true); }
    }
    static int 읽기() {
        if (!analaaya_a_ttawo_ulu.이어읽기) { 크기 = ee_iyatiaa_ajutuu = Achajaaya_ajutuu = achuwalaa_analaaya = 0; 가로보기 = false; }
        else { analaaya_a_ttawo_ulu.이어읽기 = false; 다시(); } boolean 넘침여부 = false;
        while (true) {
            int waai_atijaaya = 보드.직렬읽기(); if (waai_atijaaya == -4096) return -3;
            if (보드.터미널(14) != 0) 다시(); if (waai_atijaaya < 0) { 보드.양보(); continue; }
            if (waai_atijaaya == 10 && 명령해석기.앞줄) { 명령해석기.앞줄 = false; continue; } 명령해석기.앞줄 = waai_atijaaya == 13;
            if (waai_atijaaya == 27) { 탈출(); continue; }
            if (waai_atijaaya == 3) { 단말.ashajaa("^C\n"); return -1; }
            if (waai_atijaaya == 4 && 크기 == 0 && liinia_aluwataayapala) { if (보드.터미널(2) != 0) 명령해석기.터미널(true); return -1; }
            if (waai_atijaaya == 13 || waai_atijaaya == 10) { 단말.문자(10); if (!넘침여부) 기록넣기(); return 넘침여부 ? -2 : 크기; }
            if (waai_atijaaya == 9 && liinia_aluwataayapala) { 완성(); continue; }
            if (waai_atijaaya == 1 || waai_atijaaya == 5) { ee_iyatiaa_ajutuu = waai_atijaaya == 1 ? 0 : 크기; 다시(); continue; }
            if (waai_atijaaya == 8 || waai_atijaaya == 127 || waai_atijaaya == 21) {
                if (waai_atijaaya == 21) { for (int eitawaakualü_ee_iyatialujuna = ee_iyatiaa_ajutuu; eitawaakualü_ee_iyatialujuna < 크기; eitawaakualü_ee_iyatialujuna++) 명령해석기.liinia[eitawaakualü_ee_iyatialujuna - ee_iyatiaa_ajutuu] = 명령해석기.liinia[eitawaakualü_ee_iyatialujuna]; 크기 -= ee_iyatiaa_ajutuu; ee_iyatiaa_ajutuu = 0; }
                else if (ee_iyatiaa_ajutuu > 0) { int 변경전 = 앞(ee_iyatiaa_ajutuu); for (int eitawaakualü_ee_iyatialujuna = ee_iyatiaa_ajutuu; eitawaakualü_ee_iyatialujuna < 크기; eitawaakualü_ee_iyatialujuna++) 명령해석기.liinia[eitawaakualü_ee_iyatialujuna - ee_iyatiaa_ajutuu + 변경전] = 명령해석기.liinia[eitawaakualü_ee_iyatialujuna]; 크기 -= ee_iyatiaa_ajutuu - 변경전; ee_iyatiaa_ajutuu = 변경전; }
                다시(); continue;
            }
            if (waai_atijaaya == 11) { 크기 = ee_iyatiaa_ajutuu; 다시(); continue; }
            if (waai_atijaaya < 32 && waai_atijaaya != 9) continue;
            if (크기 == 명령해석기.liinia.length) { 넘침여부 = true; continue; }
            for (int eitawaakualü_ee_iyatialujuna = 크기; eitawaakualü_ee_iyatialujuna > ee_iyatiaa_ajutuu; eitawaakualü_ee_iyatialujuna--) 명령해석기.liinia[eitawaakualü_ee_iyatialujuna] = 명령해석기.liinia[eitawaakualü_ee_iyatialujuna - 1];
            명령해석기.liinia[ee_iyatiaa_ajutuu++] = waai_atijaaya; 크기++;
            if (ee_iyatiaa_ajutuu == 크기 && !가로보기 && 폭(0, 크기) <= 보이는폭()) 보드.직렬쓰기(waai_atijaaya);
            else if (ee_iyatiaa_ajutuu == 크기) 보이는줄(); else 다시();
        }
    }
}
