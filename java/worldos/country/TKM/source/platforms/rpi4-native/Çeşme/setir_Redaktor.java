// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 baýt_baha 경계를 지키는 삽입/삭제, 방향키, buýruk hasaba_alyş_setir, Tab 완성. */
public final class setir_Redaktor {
    static boolean buýruk_setiri;
    static int[] hasaba_alyş_setir = new int[16 * 1024], hasaba_alyş_dowamlylyk = new int[16], Store_baha = new int[4096], 후보 = new int[64];
    static int 기록수, hasaba_alyş_setir_tamamla, gözle_baha, 저장길이, Ululyk, kursor_baha, 후보수, 후보길이, başlat_penjire;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd goragly_gabyjak uzakdan_ekran run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String girizmeklik_Sanaw, int 시작자리, int 끝자리, int 입력길이) {
        int 바이트수=0;
        for(int 자리=시작자리;자리<끝자리;자리++) {
            int nyşanyň_kody=girizmeklik_Sanaw.charAt(자리);
            if(nyşanyň_kody>=0xd800 && nyşanyň_kody<=0xdbff && 자리+1<끝자리)nyşanyň_kody=0x10000+((nyşanyň_kody-0xd800)<<10)+girizmeklik_Sanaw.charAt(++자리)-0xdc00;
            int 수=nyşanyň_kody<128?1:nyşanyň_kody<2048?2:nyşanyň_kody<65536?3:4;
            if(바이트수+수>62)return;
            for(int SEQUENCE_baha=수-1;SEQUENCE_baha>=0;SEQUENCE_baha--)명령후보[바이트수++]=수==1?nyşanyň_kody:SEQUENCE_baha==수-1?(수==2?0xc0:수==3?0xe0:0xf0)|(nyşanyň_kody>>(6*SEQUENCE_baha)):0x80|((nyşanyň_kody>>(6*SEQUENCE_baha))&63);
        }
        if(바이트수<입력길이)return;
        for(int 자리=0;자리<입력길이;자리++)if(명령후보[자리]!=명령해석기.setir[자리])return;
        후보수++;후보길이=바이트수+1;
        for(int 자리=0;자리<바이트수;자리++)후보[자리]=명령후보[자리];후보[바이트수]=' ';
    }
    static int 앞(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (명령해석기.setir[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int Yza_baha(int 읽는자리) { if (읽는자리 < Ululyk) { 읽는자리++; while (읽는자리 < Ululyk && (명령해석기.setir[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int 시작자리, int barylmaly_ýer_baha_indeks) {
        int 글칸수 = 0;
        for (int sikl_indeks = 시작자리; sikl_indeks < barylmaly_ýer_baha_indeks; sikl_indeks++) { int baýt_maglumat = 명령해석기.setir[sikl_indeks]; if ((baýt_maglumat & 192) == 128) continue; 글칸수 += baýt_maglumat >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void 다시() {
        단말.Ýaz("\r\u001b[2K");
        단말.Ýaz(buýruk_setiri ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 setir 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int 열수 = 보드.터미널(13) & 65535; return 열수 - (buýruk_setiri ? 18 : 9); }
    static void 보이는줄() {
        if (kursor_baha < başlat_penjire) başlat_penjire = kursor_baha;
        while (폭(başlat_penjire, kursor_baha) > 보이는폭()) başlat_penjire = Yza_baha(başlat_penjire);
        int 끝자리 = başlat_penjire;
        while (끝자리 < Ululyk && 폭(başlat_penjire, Yza_baha(끝자리)) <= 보이는폭()) 끝자리 = Yza_baha(끝자리);
        단말.Ýaz("\r\u001b["); 단말.수(buýruk_setiri ? 16 : 7); 단말.Ýaz("G\u001b[K");
        if (başlat_penjire > 0) 단말.문자('<');
        for (int sikl_indeks = başlat_penjire; sikl_indeks < 끝자리; sikl_indeks++) 보드.직렬쓰기(명령해석기.setir[sikl_indeks]);
        단말.문자(끝자리 < Ululyk ? '>' : ' ');
        단말.Ýaz("\u001b["); 단말.수(폭(kursor_baha, 끝자리) + 1); 단말.문자('D');
        가로보기 = başlat_penjire > 0 || 끝자리 < Ululyk || 폭(0, Ululyk) > 보이는폭();
    }
    static void 기록넣기() {
        if (!buýruk_setiri || Ululyk == 0 || Ululyk > 1024) return;
        if (기록수 > 0) {
            int 마지막자리 = (hasaba_alyş_setir_tamamla + 15) % 16; boolean 같은여부 = hasaba_alyş_dowamlylyk[마지막자리] == Ululyk;
            for (int sikl_indeks = 0; 같은여부 && sikl_indeks < Ululyk; sikl_indeks++) if (hasaba_alyş_setir[마지막자리 * 1024 + sikl_indeks] != 명령해석기.setir[sikl_indeks]) 같은여부 = false;
            if (같은여부) return;
        }
        hasaba_alyş_dowamlylyk[hasaba_alyş_setir_tamamla] = Ululyk; for (int sikl_indeks = 0; sikl_indeks < Ululyk; sikl_indeks++) hasaba_alyş_setir[hasaba_alyş_setir_tamamla * 1024 + sikl_indeks] = 명령해석기.setir[sikl_indeks];
        hasaba_alyş_setir_tamamla = (hasaba_alyş_setir_tamamla + 1) % 16; if (기록수 < 16) 기록수++;
    }
    static void 기록이동(int 변화량) {
        if (!buýruk_setiri) return;
        if (gözle_baha == 0 && 변화량 > 0) { 저장길이 = Ululyk; for (int sikl_indeks = 0; sikl_indeks < Ululyk; sikl_indeks++) Store_baha[sikl_indeks] = 명령해석기.setir[sikl_indeks]; }
        int 다음자리 = gözle_baha + 변화량; if (다음자리 < 0 || 다음자리 > 기록수) return; gözle_baha = 다음자리;
        if (gözle_baha == 0) { Ululyk = 저장길이; for (int sikl_indeks = 0; sikl_indeks < Ululyk; sikl_indeks++) 명령해석기.setir[sikl_indeks] = Store_baha[sikl_indeks]; }
        else { int 보관칸 = (hasaba_alyş_setir_tamamla + 16 - gözle_baha) % 16; Ululyk = hasaba_alyş_dowamlylyk[보관칸]; for (int sikl_indeks = 0; sikl_indeks < Ululyk; sikl_indeks++) 명령해석기.setir[sikl_indeks] = hasaba_alyş_setir[보관칸 * 1024 + sikl_indeks]; }
        kursor_baha = Ululyk; 다시();
    }
    static void görkez_hasaba_alyş() {
        for (int 항목수 = 0; 항목수 < 기록수; 항목수++) {
            int 보관칸 = (hasaba_alyş_setir_tamamla + 16 - 기록수 + 항목수) % 16; 단말.수(항목수 + 1); 단말.Ýaz("  ");
            for (int sikl_indeks = 0; sikl_indeks < hasaba_alyş_dowamlylyk[보관칸]; sikl_indeks++) 보드.직렬쓰기(hasaba_alyş_setir[보관칸 * 1024 + sikl_indeks]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] maglumat_ARRAY, int 시작자리, int 항목수, int 접두말, int 총수, boolean 폴더번호) {
        if (항목수 < 총수 || 항목수 > 62) return;
        for (int sikl_indeks = 0; sikl_indeks < 총수; sikl_indeks++) if (maglumat_ARRAY[시작자리 + sikl_indeks] != 명령해석기.setir[접두말 + sikl_indeks]) return;
        후보수++; 후보길이 = 항목수 + 1;
        for (int sikl_indeks = 0; sikl_indeks < 항목수; sikl_indeks++) 후보[sikl_indeks] = maglumat_ARRAY[시작자리 + sikl_indeks]; 후보[항목수] = 폴더번호 ? '/' : ' ';
    }
    static void 완성() {
        if (!buýruk_setiri || kursor_baha != Ululyk) return;
        int 시작점 = Ululyk; while (시작점 > 0 && 명령해석기.setir[시작점 - 1] != ' ') 시작점--;
        for (int sikl_indeks = 시작점; sikl_indeks < Ululyk; sikl_indeks++) if (명령해석기.setir[sikl_indeks] == '/' || 명령해석기.setir[sikl_indeks] == '"' || 명령해석기.setir[sikl_indeks] == 39 || 명령해석기.setir[sikl_indeks] == '\\') return;
        후보수 = 0; int 항목수 = Ululyk - 시작점;
        if (시작점 == 0) {
            for(int Sanaw_indeks=0;Sanaw_indeks<2;Sanaw_indeks++) {
                String girizmeklik_Sanaw=Sanaw_indeks==0?명령들:관리명령.완성어();
                int 읽는자리=0;
                while(읽는자리<girizmeklik_Sanaw.length()) {
                    int 끝자리=읽는자리;while(끝자리<girizmeklik_Sanaw.length() && girizmeklik_Sanaw.charAt(끝자리)!=' ')끝자리++;
                    명령후보넣기(girizmeklik_Sanaw,읽는자리,끝자리,항목수);읽는자리=끝자리+1;
                }
            }
        } else {
            ýat_Faýllar.ýol_başlat(1); ýat_Faýllar.ýol_baýt(0, '.'); ýat_Faýllar.adaty_ýagdaýa_getir_baha();
            for (int sikl_indeks = 0; sikl_indeks < ýat_Faýllar.파일수; sikl_indeks++) {
                int 시작자리 = ýat_Faýllar.girizmeklik_başlat(ýat_Faýllar.Ad, sikl_indeks * 64, ýat_Faýllar.이름길이[sikl_indeks]);
                if (시작자리 >= 0) 후보넣기(ýat_Faýllar.Ad, sikl_indeks * 64 + 시작자리, ýat_Faýllar.이름길이[sikl_indeks] - 시작자리, 시작점, 항목수, false);
            }
            for (int sikl_indeks = 0; sikl_indeks < 16; sikl_indeks++) {
                int 시작자리 = ýat_Faýllar.girizmeklik_başlat(ýat_Faýllar.katalog_at, sikl_indeks * 64, ýat_Faýllar.katalog_dowamlylyk[sikl_indeks]);
                if (시작자리 >= 0) 후보넣기(ýat_Faýllar.katalog_at, sikl_indeks * 64 + 시작자리, ýat_Faýllar.katalog_dowamlylyk[sikl_indeks] - 시작자리, 시작점, 항목수, true);
            }
        }
        if (후보수 != 1) { 보드.직렬쓰기(7); return; }
        for (int sikl_indeks = 항목수; sikl_indeks < 후보길이 && Ululyk < 명령해석기.setir.length - 1; sikl_indeks++) {
            if (후보[sikl_indeks] == ' ' && sikl_indeks != 후보길이 - 1) 명령해석기.setir[Ululyk++] = '\\';
            명령해석기.setir[Ululyk++] = 후보[sikl_indeks];
        }
        kursor_baha = Ululyk; 다시();
    }
    static int 탈출읽기() {
        int 시작점 = 보드.밀리초();
        while (보드.밀리초() - 시작점 < 80) { int baýt_maglumat = 보드.직렬읽기(); if (baýt_maglumat >= 0) return baýt_maglumat; 보드.togtatmak_CPU(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int 항목수 = 0, 끝자리 = -1;
        for (int sikl_indeks = 0; sikl_indeks < 12; sikl_indeks++) { int baýt_maglumat = 탈출읽기(); if (baýt_maglumat < 0) return; if (baýt_maglumat >= '0' && baýt_maglumat <= '9') 항목수 = 항목수 * 10 + baýt_maglumat - '0'; else { 끝자리 = baýt_maglumat; break; } }
        if (끝자리 == 'A') 기록이동(1);
        else if (끝자리 == 'B') 기록이동(-1);
        else if (끝자리 == 'C') { kursor_baha = Yza_baha(kursor_baha); 다시(); }
        else if (끝자리 == 'D') { kursor_baha = 앞(kursor_baha); 다시(); }
        else if (끝자리 == 'H' || 끝자리 == '~' && (항목수 == 1 || 항목수 == 7)) { kursor_baha = 0; 다시(); }
        else if (끝자리 == 'F' || 끝자리 == '~' && (항목수 == 4 || 항목수 == 8)) { kursor_baha = Ululyk; 다시(); }
        else if (끝자리 == '~' && 항목수 == 3 && kursor_baha < Ululyk) {
            int 다음자리 = Yza_baha(kursor_baha); for (int sikl_indeks = 다음자리; sikl_indeks < Ululyk; sikl_indeks++) 명령해석기.setir[sikl_indeks - 다음자리 + kursor_baha] = 명령해석기.setir[sikl_indeks]; Ululyk -= 다음자리 - kursor_baha; 다시();
        }
        else if (끝자리 == '~' && (항목수 == 5 || 항목수 == 6)) 보드.터미널(항목수 == 5 ? 5 : 6);
        else if (끝자리 == '~' && 항목수 == 24 && buýruk_setiri) { 명령해석기.터미널(true); }
    }
    static int Oka() {
        if (!penjire_seans.이어읽기) { Ululyk = kursor_baha = gözle_baha = başlat_penjire = 0; 가로보기 = false; }
        else { penjire_seans.이어읽기 = false; 다시(); } boolean gyrmalanma = false;
        while (true) {
            int baýt_maglumat = 보드.직렬읽기(); if (baýt_maglumat == -4096) return -3;
            if (보드.터미널(14) != 0) 다시(); if (baýt_maglumat < 0) { 보드.togtatmak_CPU(); continue; }
            if (baýt_maglumat == 10 && 명령해석기.앞줄) { 명령해석기.앞줄 = false; continue; } 명령해석기.앞줄 = baýt_maglumat == 13;
            if (baýt_maglumat == 27) { 탈출(); continue; }
            if (baýt_maglumat == 3) { 단말.Ýaz("^C\n"); return -1; }
            if (baýt_maglumat == 4 && Ululyk == 0 && buýruk_setiri) { if (보드.터미널(2) != 0) 명령해석기.터미널(true); return -1; }
            if (baýt_maglumat == 13 || baýt_maglumat == 10) { 단말.문자(10); if (!gyrmalanma) 기록넣기(); return gyrmalanma ? -2 : Ululyk; }
            if (baýt_maglumat == 9 && buýruk_setiri) { 완성(); continue; }
            if (baýt_maglumat == 1 || baýt_maglumat == 5) { kursor_baha = baýt_maglumat == 1 ? 0 : Ululyk; 다시(); continue; }
            if (baýt_maglumat == 8 || baýt_maglumat == 127 || baýt_maglumat == 21) {
                if (baýt_maglumat == 21) { for (int sikl_indeks = kursor_baha; sikl_indeks < Ululyk; sikl_indeks++) 명령해석기.setir[sikl_indeks - kursor_baha] = 명령해석기.setir[sikl_indeks]; Ululyk -= kursor_baha; kursor_baha = 0; }
                else if (kursor_baha > 0) { int 변경전 = 앞(kursor_baha); for (int sikl_indeks = kursor_baha; sikl_indeks < Ululyk; sikl_indeks++) 명령해석기.setir[sikl_indeks - kursor_baha + 변경전] = 명령해석기.setir[sikl_indeks]; Ululyk -= kursor_baha - 변경전; kursor_baha = 변경전; }
                다시(); continue;
            }
            if (baýt_maglumat == 11) { Ululyk = kursor_baha; 다시(); continue; }
            if (baýt_maglumat < 32 && baýt_maglumat != 9) continue;
            if (Ululyk == 명령해석기.setir.length) { gyrmalanma = true; continue; }
            for (int sikl_indeks = Ululyk; sikl_indeks > kursor_baha; sikl_indeks--) 명령해석기.setir[sikl_indeks] = 명령해석기.setir[sikl_indeks - 1];
            명령해석기.setir[kursor_baha++] = baýt_maglumat; Ululyk++;
            if (kursor_baha == Ululyk && !가로보기 && 폭(0, Ululyk) <= 보이는폭()) 보드.직렬쓰기(baýt_maglumat);
            else if (kursor_baha == Ululyk) 보이는줄(); else 다시();
        }
    }
}
