// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 ibhayithi_inani 경계를 지키는 삽입/삭제, 방향키, Umlayelo loga_umugqa, Tab 완성. */
public final class umugqa_Umhleli {
    static boolean umugqa_wemiyalo;
    static int[] loga_umugqa = new int[16 * 1024], loga_ubude = new int[16], Store_inani = new int[4096], 후보 = new int[64];
    static int 기록수, loga_umugqa_yekisa, Bheka_inani, 저장길이, Ubungako, isikhombisi_inani, 후보수, 후보길이, qala_ifasitela;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd ivikelekile_isihumushi_miyalelo kude_bonisa run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String okufakwayo_Uhlu, int 시작자리, int 끝자리, int 입력길이) {
        int 바이트수=0;
        for(int 자리=시작자리;자리<끝자리;자리++) {
            int ikhodi_yohlamvu=okufakwayo_Uhlu.charAt(자리);
            if(ikhodi_yohlamvu>=0xd800 && ikhodi_yohlamvu<=0xdbff && 자리+1<끝자리)ikhodi_yohlamvu=0x10000+((ikhodi_yohlamvu-0xd800)<<10)+okufakwayo_Uhlu.charAt(++자리)-0xdc00;
            int 수=ikhodi_yohlamvu<128?1:ikhodi_yohlamvu<2048?2:ikhodi_yohlamvu<65536?3:4;
            if(바이트수+수>62)return;
            for(int UKULANDELANA_inani=수-1;UKULANDELANA_inani>=0;UKULANDELANA_inani--)명령후보[바이트수++]=수==1?ikhodi_yohlamvu:UKULANDELANA_inani==수-1?(수==2?0xc0:수==3?0xe0:0xf0)|(ikhodi_yohlamvu>>(6*UKULANDELANA_inani)):0x80|((ikhodi_yohlamvu>>(6*UKULANDELANA_inani))&63);
        }
        if(바이트수<입력길이)return;
        for(int 자리=0;자리<입력길이;자리++)if(명령후보[자리]!=명령해석기.umugqa[자리])return;
        후보수++;후보길이=바이트수+1;
        for(int 자리=0;자리<바이트수;자리++)후보[자리]=명령후보[자리];후보[바이트수]=' ';
    }
    static int 앞(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (명령해석기.umugqa[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int Impindamuva_inani(int 읽는자리) { if (읽는자리 < Ubungako) { 읽는자리++; while (읽는자리 < Ubungako && (명령해석기.umugqa[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int 시작자리, int isikhumulo_inani_thola_inkomba) {
        int 글칸수 = 0;
        for (int iluphu_thola_inkomba = 시작자리; iluphu_thola_inkomba < isikhumulo_inani_thola_inkomba; iluphu_thola_inkomba++) { int ibhayithi_imininingwane = 명령해석기.umugqa[iluphu_thola_inkomba]; if ((ibhayithi_imininingwane & 192) == 128) continue; 글칸수 += ibhayithi_imininingwane >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void 다시() {
        단말.Bhala("\r\u001b[2K");
        단말.Bhala(umugqa_wemiyalo ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 umugqa 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int 열수 = 보드.터미널(13) & 65535; return 열수 - (umugqa_wemiyalo ? 18 : 9); }
    static void 보이는줄() {
        if (isikhombisi_inani < qala_ifasitela) qala_ifasitela = isikhombisi_inani;
        while (폭(qala_ifasitela, isikhombisi_inani) > 보이는폭()) qala_ifasitela = Impindamuva_inani(qala_ifasitela);
        int 끝자리 = qala_ifasitela;
        while (끝자리 < Ubungako && 폭(qala_ifasitela, Impindamuva_inani(끝자리)) <= 보이는폭()) 끝자리 = Impindamuva_inani(끝자리);
        단말.Bhala("\r\u001b["); 단말.수(umugqa_wemiyalo ? 16 : 7); 단말.Bhala("G\u001b[K");
        if (qala_ifasitela > 0) 단말.문자('<');
        for (int iluphu_thola_inkomba = qala_ifasitela; iluphu_thola_inkomba < 끝자리; iluphu_thola_inkomba++) 보드.직렬쓰기(명령해석기.umugqa[iluphu_thola_inkomba]);
        단말.문자(끝자리 < Ubungako ? '>' : ' ');
        단말.Bhala("\u001b["); 단말.수(폭(isikhombisi_inani, 끝자리) + 1); 단말.문자('D');
        가로보기 = qala_ifasitela > 0 || 끝자리 < Ubungako || 폭(0, Ubungako) > 보이는폭();
    }
    static void 기록넣기() {
        if (!umugqa_wemiyalo || Ubungako == 0 || Ubungako > 1024) return;
        if (기록수 > 0) {
            int 마지막자리 = (loga_umugqa_yekisa + 15) % 16; boolean 같은여부 = loga_ubude[마지막자리] == Ubungako;
            for (int iluphu_thola_inkomba = 0; 같은여부 && iluphu_thola_inkomba < Ubungako; iluphu_thola_inkomba++) if (loga_umugqa[마지막자리 * 1024 + iluphu_thola_inkomba] != 명령해석기.umugqa[iluphu_thola_inkomba]) 같은여부 = false;
            if (같은여부) return;
        }
        loga_ubude[loga_umugqa_yekisa] = Ubungako; for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < Ubungako; iluphu_thola_inkomba++) loga_umugqa[loga_umugqa_yekisa * 1024 + iluphu_thola_inkomba] = 명령해석기.umugqa[iluphu_thola_inkomba];
        loga_umugqa_yekisa = (loga_umugqa_yekisa + 1) % 16; if (기록수 < 16) 기록수++;
    }
    static void 기록이동(int 변화량) {
        if (!umugqa_wemiyalo) return;
        if (Bheka_inani == 0 && 변화량 > 0) { 저장길이 = Ubungako; for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < Ubungako; iluphu_thola_inkomba++) Store_inani[iluphu_thola_inkomba] = 명령해석기.umugqa[iluphu_thola_inkomba]; }
        int 다음자리 = Bheka_inani + 변화량; if (다음자리 < 0 || 다음자리 > 기록수) return; Bheka_inani = 다음자리;
        if (Bheka_inani == 0) { Ubungako = 저장길이; for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < Ubungako; iluphu_thola_inkomba++) 명령해석기.umugqa[iluphu_thola_inkomba] = Store_inani[iluphu_thola_inkomba]; }
        else { int 보관칸 = (loga_umugqa_yekisa + 16 - Bheka_inani) % 16; Ubungako = loga_ubude[보관칸]; for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < Ubungako; iluphu_thola_inkomba++) 명령해석기.umugqa[iluphu_thola_inkomba] = loga_umugqa[보관칸 * 1024 + iluphu_thola_inkomba]; }
        isikhombisi_inani = Ubungako; 다시();
    }
    static void khombisa_loga() {
        for (int 항목수 = 0; 항목수 < 기록수; 항목수++) {
            int 보관칸 = (loga_umugqa_yekisa + 16 - 기록수 + 항목수) % 16; 단말.수(항목수 + 1); 단말.Bhala("  ");
            for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < loga_ubude[보관칸]; iluphu_thola_inkomba++) 보드.직렬쓰기(loga_umugqa[보관칸 * 1024 + iluphu_thola_inkomba]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] imininingwane_AMALUNGU_AFANAYO, int 시작자리, int 항목수, int 접두말, int 총수, boolean 폴더번호) {
        if (항목수 < 총수 || 항목수 > 62) return;
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 총수; iluphu_thola_inkomba++) if (imininingwane_AMALUNGU_AFANAYO[시작자리 + iluphu_thola_inkomba] != 명령해석기.umugqa[접두말 + iluphu_thola_inkomba]) return;
        후보수++; 후보길이 = 항목수 + 1;
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 항목수; iluphu_thola_inkomba++) 후보[iluphu_thola_inkomba] = imininingwane_AMALUNGU_AFANAYO[시작자리 + iluphu_thola_inkomba]; 후보[항목수] = 폴더번호 ? '/' : ' ';
    }
    static void 완성() {
        if (!umugqa_wemiyalo || isikhombisi_inani != Ubungako) return;
        int 시작점 = Ubungako; while (시작점 > 0 && 명령해석기.umugqa[시작점 - 1] != ' ') 시작점--;
        for (int iluphu_thola_inkomba = 시작점; iluphu_thola_inkomba < Ubungako; iluphu_thola_inkomba++) if (명령해석기.umugqa[iluphu_thola_inkomba] == '/' || 명령해석기.umugqa[iluphu_thola_inkomba] == '"' || 명령해석기.umugqa[iluphu_thola_inkomba] == 39 || 명령해석기.umugqa[iluphu_thola_inkomba] == '\\') return;
        후보수 = 0; int 항목수 = Ubungako - 시작점;
        if (시작점 == 0) {
            for(int Uhlu_thola_inkomba=0;Uhlu_thola_inkomba<2;Uhlu_thola_inkomba++) {
                String okufakwayo_Uhlu=Uhlu_thola_inkomba==0?명령들:관리명령.완성어();
                int 읽는자리=0;
                while(읽는자리<okufakwayo_Uhlu.length()) {
                    int 끝자리=읽는자리;while(끝자리<okufakwayo_Uhlu.length() && okufakwayo_Uhlu.charAt(끝자리)!=' ')끝자리++;
                    명령후보넣기(okufakwayo_Uhlu,읽는자리,끝자리,항목수);읽는자리=끝자리+1;
                }
            }
        } else {
            inkumbulo_Amafayela.umzila_qala(1); inkumbulo_Amafayela.umzila_ibhayithi(0, '.'); inkumbulo_Amafayela.beka_kujwayeleke_inani();
            for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < inkumbulo_Amafayela.파일수; iluphu_thola_inkomba++) {
                int 시작자리 = inkumbulo_Amafayela.okufakwayo_qala(inkumbulo_Amafayela.Igama, iluphu_thola_inkomba * 64, inkumbulo_Amafayela.이름길이[iluphu_thola_inkomba]);
                if (시작자리 >= 0) 후보넣기(inkumbulo_Amafayela.Igama, iluphu_thola_inkomba * 64 + 시작자리, inkumbulo_Amafayela.이름길이[iluphu_thola_inkomba] - 시작자리, 시작점, 항목수, false);
            }
            for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 16; iluphu_thola_inkomba++) {
                int 시작자리 = inkumbulo_Amafayela.okufakwayo_qala(inkumbulo_Amafayela.umkhombandlela_igama, iluphu_thola_inkomba * 64, inkumbulo_Amafayela.umkhombandlela_ubude[iluphu_thola_inkomba]);
                if (시작자리 >= 0) 후보넣기(inkumbulo_Amafayela.umkhombandlela_igama, iluphu_thola_inkomba * 64 + 시작자리, inkumbulo_Amafayela.umkhombandlela_ubude[iluphu_thola_inkomba] - 시작자리, 시작점, 항목수, true);
            }
        }
        if (후보수 != 1) { 보드.직렬쓰기(7); return; }
        for (int iluphu_thola_inkomba = 항목수; iluphu_thola_inkomba < 후보길이 && Ubungako < 명령해석기.umugqa.length - 1; iluphu_thola_inkomba++) {
            if (후보[iluphu_thola_inkomba] == ' ' && iluphu_thola_inkomba != 후보길이 - 1) 명령해석기.umugqa[Ubungako++] = '\\';
            명령해석기.umugqa[Ubungako++] = 후보[iluphu_thola_inkomba];
        }
        isikhombisi_inani = Ubungako; 다시();
    }
    static int 탈출읽기() {
        int 시작점 = 보드.밀리초();
        while (보드.밀리초() - 시작점 < 80) { int ibhayithi_imininingwane = 보드.직렬읽기(); if (ibhayithi_imininingwane >= 0) return ibhayithi_imininingwane; 보드.misa_okwesikhashana_i_CPU(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int 항목수 = 0, 끝자리 = -1;
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 12; iluphu_thola_inkomba++) { int ibhayithi_imininingwane = 탈출읽기(); if (ibhayithi_imininingwane < 0) return; if (ibhayithi_imininingwane >= '0' && ibhayithi_imininingwane <= '9') 항목수 = 항목수 * 10 + ibhayithi_imininingwane - '0'; else { 끝자리 = ibhayithi_imininingwane; break; } }
        if (끝자리 == 'A') 기록이동(1);
        else if (끝자리 == 'B') 기록이동(-1);
        else if (끝자리 == 'C') { isikhombisi_inani = Impindamuva_inani(isikhombisi_inani); 다시(); }
        else if (끝자리 == 'D') { isikhombisi_inani = 앞(isikhombisi_inani); 다시(); }
        else if (끝자리 == 'H' || 끝자리 == '~' && (항목수 == 1 || 항목수 == 7)) { isikhombisi_inani = 0; 다시(); }
        else if (끝자리 == 'F' || 끝자리 == '~' && (항목수 == 4 || 항목수 == 8)) { isikhombisi_inani = Ubungako; 다시(); }
        else if (끝자리 == '~' && 항목수 == 3 && isikhombisi_inani < Ubungako) {
            int 다음자리 = Impindamuva_inani(isikhombisi_inani); for (int iluphu_thola_inkomba = 다음자리; iluphu_thola_inkomba < Ubungako; iluphu_thola_inkomba++) 명령해석기.umugqa[iluphu_thola_inkomba - 다음자리 + isikhombisi_inani] = 명령해석기.umugqa[iluphu_thola_inkomba]; Ubungako -= 다음자리 - isikhombisi_inani; 다시();
        }
        else if (끝자리 == '~' && (항목수 == 5 || 항목수 == 6)) 보드.터미널(항목수 == 5 ? 5 : 6);
        else if (끝자리 == '~' && 항목수 == 24 && umugqa_wemiyalo) { 명령해석기.터미널(true); }
    }
    static int Funda() {
        if (!ifasitela_isikhathi_sokwenza.이어읽기) { Ubungako = isikhombisi_inani = Bheka_inani = qala_ifasitela = 0; 가로보기 = false; }
        else { ifasitela_isikhathi_sokwenza.이어읽기 = false; 다시(); } boolean ukukapaka = false;
        while (true) {
            int ibhayithi_imininingwane = 보드.직렬읽기(); if (ibhayithi_imininingwane == -4096) return -3;
            if (보드.터미널(14) != 0) 다시(); if (ibhayithi_imininingwane < 0) { 보드.misa_okwesikhashana_i_CPU(); continue; }
            if (ibhayithi_imininingwane == 10 && 명령해석기.앞줄) { 명령해석기.앞줄 = false; continue; } 명령해석기.앞줄 = ibhayithi_imininingwane == 13;
            if (ibhayithi_imininingwane == 27) { 탈출(); continue; }
            if (ibhayithi_imininingwane == 3) { 단말.Bhala("^C\n"); return -1; }
            if (ibhayithi_imininingwane == 4 && Ubungako == 0 && umugqa_wemiyalo) { if (보드.터미널(2) != 0) 명령해석기.터미널(true); return -1; }
            if (ibhayithi_imininingwane == 13 || ibhayithi_imininingwane == 10) { 단말.문자(10); if (!ukukapaka) 기록넣기(); return ukukapaka ? -2 : Ubungako; }
            if (ibhayithi_imininingwane == 9 && umugqa_wemiyalo) { 완성(); continue; }
            if (ibhayithi_imininingwane == 1 || ibhayithi_imininingwane == 5) { isikhombisi_inani = ibhayithi_imininingwane == 1 ? 0 : Ubungako; 다시(); continue; }
            if (ibhayithi_imininingwane == 8 || ibhayithi_imininingwane == 127 || ibhayithi_imininingwane == 21) {
                if (ibhayithi_imininingwane == 21) { for (int iluphu_thola_inkomba = isikhombisi_inani; iluphu_thola_inkomba < Ubungako; iluphu_thola_inkomba++) 명령해석기.umugqa[iluphu_thola_inkomba - isikhombisi_inani] = 명령해석기.umugqa[iluphu_thola_inkomba]; Ubungako -= isikhombisi_inani; isikhombisi_inani = 0; }
                else if (isikhombisi_inani > 0) { int 변경전 = 앞(isikhombisi_inani); for (int iluphu_thola_inkomba = isikhombisi_inani; iluphu_thola_inkomba < Ubungako; iluphu_thola_inkomba++) 명령해석기.umugqa[iluphu_thola_inkomba - isikhombisi_inani + 변경전] = 명령해석기.umugqa[iluphu_thola_inkomba]; Ubungako -= isikhombisi_inani - 변경전; isikhombisi_inani = 변경전; }
                다시(); continue;
            }
            if (ibhayithi_imininingwane == 11) { Ubungako = isikhombisi_inani; 다시(); continue; }
            if (ibhayithi_imininingwane < 32 && ibhayithi_imininingwane != 9) continue;
            if (Ubungako == 명령해석기.umugqa.length) { ukukapaka = true; continue; }
            for (int iluphu_thola_inkomba = Ubungako; iluphu_thola_inkomba > isikhombisi_inani; iluphu_thola_inkomba--) 명령해석기.umugqa[iluphu_thola_inkomba] = 명령해석기.umugqa[iluphu_thola_inkomba - 1];
            명령해석기.umugqa[isikhombisi_inani++] = ibhayithi_imininingwane; Ubungako++;
            if (isikhombisi_inani == Ubungako && !가로보기 && 폭(0, Ubungako) <= 보이는폭()) 보드.직렬쓰기(ibhayithi_imininingwane);
            else if (isikhombisi_inani == Ubungako) 보이는줄(); else 다시();
        }
    }
}
