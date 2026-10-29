// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 bayt_VALUE 경계를 지키는 삽입/삭제, 방향키, Buyruq LOG_satr, Tab 완성. */
public final class satr_Muharrir {
    static boolean buyruq_satri;
    static int[] LOG_satr = new int[16 * 1024], LOG_uzunlik = new int[16], Store_VALUE = new int[4096], 후보 = new int[64];
    static int LOG_COUNT, LOG_satr_to_xtatmoq, Izlash_VALUE, 저장길이, Hajmi, kursor_VALUE, 후보수, 후보길이, Start_oyna;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd xavfsiz_qobiq masofaviy_ekran run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String kiritish_Ro_yxat, int Start_holat, int to_xtatmoq_holat, int 입력길이) {
        int bayt_COUNT=0;
        for(int holat_INDEX=Start_holat;holat_INDEX<to_xtatmoq_holat;holat_INDEX++) {
            int belgi_kodi=kiritish_Ro_yxat.charAt(holat_INDEX);
            if(belgi_kodi>=0xd800 && belgi_kodi<=0xdbff && holat_INDEX+1<to_xtatmoq_holat)belgi_kodi=0x10000+((belgi_kodi-0xd800)<<10)+kiritish_Ro_yxat.charAt(++holat_INDEX)-0xdc00;
            int 수=belgi_kodi<128?1:belgi_kodi<2048?2:belgi_kodi<65536?3:4;
            if(bayt_COUNT+수>62)return;
            for(int SEQUENCE_VALUE=수-1;SEQUENCE_VALUE>=0;SEQUENCE_VALUE--)명령후보[bayt_COUNT++]=수==1?belgi_kodi:SEQUENCE_VALUE==수-1?(수==2?0xc0:수==3?0xe0:0xf0)|(belgi_kodi>>(6*SEQUENCE_VALUE)):0x80|((belgi_kodi>>(6*SEQUENCE_VALUE))&63);
        }
        if(bayt_COUNT<입력길이)return;
        for(int holat_INDEX=0;holat_INDEX<입력길이;holat_INDEX++)if(명령후보[holat_INDEX]!=명령해석기.satr[holat_INDEX])return;
        후보수++;후보길이=bayt_COUNT+1;
        for(int holat_INDEX=0;holat_INDEX<bayt_COUNT;holat_INDEX++)후보[holat_INDEX]=명령후보[holat_INDEX];후보[bayt_COUNT]=' ';
    }
    static int old_kamera_VALUE(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (명령해석기.satr[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int Orqaga_VALUE(int 읽는자리) { if (읽는자리 < Hajmi) { 읽는자리++; while (읽는자리 < Hajmi && (명령해석기.satr[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int Start_holat, int ko_chirish_joyi_VALUE_INDEX) {
        int 글칸수 = 0;
        for (int Loop_INDEX = Start_holat; Loop_INDEX < ko_chirish_joyi_VALUE_INDEX; Loop_INDEX++) { int bayt_ma_lumotlar = 명령해석기.satr[Loop_INDEX]; if ((bayt_ma_lumotlar & 192) == 128) continue; 글칸수 += bayt_ma_lumotlar >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void 다시() {
        단말.Yozish("\r\u001b[2K");
        단말.Yozish(buyruq_satri ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 satr 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int COLUMNS = yozuv_taxtasi.Terminal(13) & 65535; return COLUMNS - (buyruq_satri ? 18 : 9); }
    static void 보이는줄() {
        if (kursor_VALUE < Start_oyna) Start_oyna = kursor_VALUE;
        while (폭(Start_oyna, kursor_VALUE) > 보이는폭()) Start_oyna = Orqaga_VALUE(Start_oyna);
        int to_xtatmoq_holat = Start_oyna;
        while (to_xtatmoq_holat < Hajmi && 폭(Start_oyna, Orqaga_VALUE(to_xtatmoq_holat)) <= 보이는폭()) to_xtatmoq_holat = Orqaga_VALUE(to_xtatmoq_holat);
        단말.Yozish("\r\u001b["); 단말.수(buyruq_satri ? 16 : 7); 단말.Yozish("G\u001b[K");
        if (Start_oyna > 0) 단말.문자('<');
        for (int Loop_INDEX = Start_oyna; Loop_INDEX < to_xtatmoq_holat; Loop_INDEX++) yozuv_taxtasi.직렬쓰기(명령해석기.satr[Loop_INDEX]);
        단말.문자(to_xtatmoq_holat < Hajmi ? '>' : ' ');
        단말.Yozish("\u001b["); 단말.수(폭(kursor_VALUE, to_xtatmoq_holat) + 1); 단말.문자('D');
        가로보기 = Start_oyna > 0 || to_xtatmoq_holat < Hajmi || 폭(0, Hajmi) > 보이는폭();
    }
    static void 기록넣기() {
        if (!buyruq_satri || Hajmi == 0 || Hajmi > 1024) return;
        if (LOG_COUNT > 0) {
            int 마지막자리 = (LOG_satr_to_xtatmoq + 15) % 16; boolean 같은여부 = LOG_uzunlik[마지막자리] == Hajmi;
            for (int Loop_INDEX = 0; 같은여부 && Loop_INDEX < Hajmi; Loop_INDEX++) if (LOG_satr[마지막자리 * 1024 + Loop_INDEX] != 명령해석기.satr[Loop_INDEX]) 같은여부 = false;
            if (같은여부) return;
        }
        LOG_uzunlik[LOG_satr_to_xtatmoq] = Hajmi; for (int Loop_INDEX = 0; Loop_INDEX < Hajmi; Loop_INDEX++) LOG_satr[LOG_satr_to_xtatmoq * 1024 + Loop_INDEX] = 명령해석기.satr[Loop_INDEX];
        LOG_satr_to_xtatmoq = (LOG_satr_to_xtatmoq + 1) % 16; if (LOG_COUNT < 16) LOG_COUNT++;
    }
    static void 기록이동(int DELTA_VALUE) {
        if (!buyruq_satri) return;
        if (Izlash_VALUE == 0 && DELTA_VALUE > 0) { 저장길이 = Hajmi; for (int Loop_INDEX = 0; Loop_INDEX < Hajmi; Loop_INDEX++) Store_VALUE[Loop_INDEX] = 명령해석기.satr[Loop_INDEX]; }
        int Keyingi_holat = Izlash_VALUE + DELTA_VALUE; if (Keyingi_holat < 0 || Keyingi_holat > LOG_COUNT) return; Izlash_VALUE = Keyingi_holat;
        if (Izlash_VALUE == 0) { Hajmi = 저장길이; for (int Loop_INDEX = 0; Loop_INDEX < Hajmi; Loop_INDEX++) 명령해석기.satr[Loop_INDEX] = Store_VALUE[Loop_INDEX]; }
        else { int 보관칸 = (LOG_satr_to_xtatmoq + 16 - Izlash_VALUE) % 16; Hajmi = LOG_uzunlik[보관칸]; for (int Loop_INDEX = 0; Loop_INDEX < Hajmi; Loop_INDEX++) 명령해석기.satr[Loop_INDEX] = LOG_satr[보관칸 * 1024 + Loop_INDEX]; }
        kursor_VALUE = Hajmi; 다시();
    }
    static void ko_rsatmoq_LOG() {
        for (int kiritish_COUNT = 0; kiritish_COUNT < LOG_COUNT; kiritish_COUNT++) {
            int 보관칸 = (LOG_satr_to_xtatmoq + 16 - LOG_COUNT + kiritish_COUNT) % 16; 단말.수(kiritish_COUNT + 1); 단말.Yozish("  ");
            for (int Loop_INDEX = 0; Loop_INDEX < LOG_uzunlik[보관칸]; Loop_INDEX++) yozuv_taxtasi.직렬쓰기(LOG_satr[보관칸 * 1024 + Loop_INDEX]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] ma_lumotlar_ARRAY, int Start_holat, int kiritish_COUNT, int 접두말, int 총수, boolean 폴더번호) {
        if (kiritish_COUNT < 총수 || kiritish_COUNT > 62) return;
        for (int Loop_INDEX = 0; Loop_INDEX < 총수; Loop_INDEX++) if (ma_lumotlar_ARRAY[Start_holat + Loop_INDEX] != 명령해석기.satr[접두말 + Loop_INDEX]) return;
        후보수++; 후보길이 = kiritish_COUNT + 1;
        for (int Loop_INDEX = 0; Loop_INDEX < kiritish_COUNT; Loop_INDEX++) 후보[Loop_INDEX] = ma_lumotlar_ARRAY[Start_holat + Loop_INDEX]; 후보[kiritish_COUNT] = 폴더번호 ? '/' : ' ';
    }
    static void 완성() {
        if (!buyruq_satri || kursor_VALUE != Hajmi) return;
        int 시작점 = Hajmi; while (시작점 > 0 && 명령해석기.satr[시작점 - 1] != ' ') 시작점--;
        for (int Loop_INDEX = 시작점; Loop_INDEX < Hajmi; Loop_INDEX++) if (명령해석기.satr[Loop_INDEX] == '/' || 명령해석기.satr[Loop_INDEX] == '"' || 명령해석기.satr[Loop_INDEX] == 39 || 명령해석기.satr[Loop_INDEX] == '\\') return;
        후보수 = 0; int kiritish_COUNT = Hajmi - 시작점;
        if (시작점 == 0) {
            for(int Ro_yxat_INDEX=0;Ro_yxat_INDEX<2;Ro_yxat_INDEX++) {
                String kiritish_Ro_yxat=Ro_yxat_INDEX==0?명령들:관리명령.완성어();
                int 읽는자리=0;
                while(읽는자리<kiritish_Ro_yxat.length()) {
                    int to_xtatmoq_holat=읽는자리;while(to_xtatmoq_holat<kiritish_Ro_yxat.length() && kiritish_Ro_yxat.charAt(to_xtatmoq_holat)!=' ')to_xtatmoq_holat++;
                    명령후보넣기(kiritish_Ro_yxat,읽는자리,to_xtatmoq_holat,kiritish_COUNT);읽는자리=to_xtatmoq_holat+1;
                }
            }
        } else {
            Xotira_Fayllar.yo_l_Start(1); Xotira_Fayllar.yo_l_bayt(0, '.'); Xotira_Fayllar.normallashtirmoq_VALUE();
            for (int Loop_INDEX = 0; Loop_INDEX < Xotira_Fayllar.fayl_COUNT; Loop_INDEX++) {
                int Start_holat = Xotira_Fayllar.kiritish_Start(Xotira_Fayllar.Nomi, Loop_INDEX * 64, Xotira_Fayllar.이름길이[Loop_INDEX]);
                if (Start_holat >= 0) 후보넣기(Xotira_Fayllar.Nomi, Loop_INDEX * 64 + Start_holat, Xotira_Fayllar.이름길이[Loop_INDEX] - Start_holat, 시작점, kiritish_COUNT, false);
            }
            for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
                int Start_holat = Xotira_Fayllar.kiritish_Start(Xotira_Fayllar.katalog_nom, Loop_INDEX * 64, Xotira_Fayllar.katalog_uzunlik[Loop_INDEX]);
                if (Start_holat >= 0) 후보넣기(Xotira_Fayllar.katalog_nom, Loop_INDEX * 64 + Start_holat, Xotira_Fayllar.katalog_uzunlik[Loop_INDEX] - Start_holat, 시작점, kiritish_COUNT, true);
            }
        }
        if (후보수 != 1) { yozuv_taxtasi.직렬쓰기(7); return; }
        for (int Loop_INDEX = kiritish_COUNT; Loop_INDEX < 후보길이 && Hajmi < 명령해석기.satr.length - 1; Loop_INDEX++) {
            if (후보[Loop_INDEX] == ' ' && Loop_INDEX != 후보길이 - 1) 명령해석기.satr[Hajmi++] = '\\';
            명령해석기.satr[Hajmi++] = 후보[Loop_INDEX];
        }
        kursor_VALUE = Hajmi; 다시();
    }
    static int 탈출읽기() {
        int 시작점 = yozuv_taxtasi.밀리초();
        while (yozuv_taxtasi.밀리초() - 시작점 < 80) { int bayt_ma_lumotlar = yozuv_taxtasi.직렬읽기(); if (bayt_ma_lumotlar >= 0) return bayt_ma_lumotlar; yozuv_taxtasi.YIELD_CPU(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int kiritish_COUNT = 0, to_xtatmoq_holat = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 12; Loop_INDEX++) { int bayt_ma_lumotlar = 탈출읽기(); if (bayt_ma_lumotlar < 0) return; if (bayt_ma_lumotlar >= '0' && bayt_ma_lumotlar <= '9') kiritish_COUNT = kiritish_COUNT * 10 + bayt_ma_lumotlar - '0'; else { to_xtatmoq_holat = bayt_ma_lumotlar; break; } }
        if (to_xtatmoq_holat == 'A') 기록이동(1);
        else if (to_xtatmoq_holat == 'B') 기록이동(-1);
        else if (to_xtatmoq_holat == 'C') { kursor_VALUE = Orqaga_VALUE(kursor_VALUE); 다시(); }
        else if (to_xtatmoq_holat == 'D') { kursor_VALUE = old_kamera_VALUE(kursor_VALUE); 다시(); }
        else if (to_xtatmoq_holat == 'H' || to_xtatmoq_holat == '~' && (kiritish_COUNT == 1 || kiritish_COUNT == 7)) { kursor_VALUE = 0; 다시(); }
        else if (to_xtatmoq_holat == 'F' || to_xtatmoq_holat == '~' && (kiritish_COUNT == 4 || kiritish_COUNT == 8)) { kursor_VALUE = Hajmi; 다시(); }
        else if (to_xtatmoq_holat == '~' && kiritish_COUNT == 3 && kursor_VALUE < Hajmi) {
            int Keyingi_holat = Orqaga_VALUE(kursor_VALUE); for (int Loop_INDEX = Keyingi_holat; Loop_INDEX < Hajmi; Loop_INDEX++) 명령해석기.satr[Loop_INDEX - Keyingi_holat + kursor_VALUE] = 명령해석기.satr[Loop_INDEX]; Hajmi -= Keyingi_holat - kursor_VALUE; 다시();
        }
        else if (to_xtatmoq_holat == '~' && (kiritish_COUNT == 5 || kiritish_COUNT == 6)) yozuv_taxtasi.Terminal(kiritish_COUNT == 5 ? 5 : 6);
        else if (to_xtatmoq_holat == '~' && kiritish_COUNT == 24 && buyruq_satri) { 명령해석기.Terminal(true); }
    }
    static int Oʻqish() {
        if (!oyna_seans.이어읽기) { Hajmi = kursor_VALUE = Izlash_VALUE = Start_oyna = 0; 가로보기 = false; }
        else { oyna_seans.이어읽기 = false; 다시(); } boolean to_lib_ketish = false;
        while (true) {
            int bayt_ma_lumotlar = yozuv_taxtasi.직렬읽기(); if (bayt_ma_lumotlar == -4096) return -3;
            if (yozuv_taxtasi.Terminal(14) != 0) 다시(); if (bayt_ma_lumotlar < 0) { yozuv_taxtasi.YIELD_CPU(); continue; }
            if (bayt_ma_lumotlar == 10 && 명령해석기.앞줄) { 명령해석기.앞줄 = false; continue; } 명령해석기.앞줄 = bayt_ma_lumotlar == 13;
            if (bayt_ma_lumotlar == 27) { 탈출(); continue; }
            if (bayt_ma_lumotlar == 3) { 단말.Yozish("^C\n"); return -1; }
            if (bayt_ma_lumotlar == 4 && Hajmi == 0 && buyruq_satri) { if (yozuv_taxtasi.Terminal(2) != 0) 명령해석기.Terminal(true); return -1; }
            if (bayt_ma_lumotlar == 13 || bayt_ma_lumotlar == 10) { 단말.문자(10); if (!to_lib_ketish) 기록넣기(); return to_lib_ketish ? -2 : Hajmi; }
            if (bayt_ma_lumotlar == 9 && buyruq_satri) { 완성(); continue; }
            if (bayt_ma_lumotlar == 1 || bayt_ma_lumotlar == 5) { kursor_VALUE = bayt_ma_lumotlar == 1 ? 0 : Hajmi; 다시(); continue; }
            if (bayt_ma_lumotlar == 8 || bayt_ma_lumotlar == 127 || bayt_ma_lumotlar == 21) {
                if (bayt_ma_lumotlar == 21) { for (int Loop_INDEX = kursor_VALUE; Loop_INDEX < Hajmi; Loop_INDEX++) 명령해석기.satr[Loop_INDEX - kursor_VALUE] = 명령해석기.satr[Loop_INDEX]; Hajmi -= kursor_VALUE; kursor_VALUE = 0; }
                else if (kursor_VALUE > 0) { int 변경전 = old_kamera_VALUE(kursor_VALUE); for (int Loop_INDEX = kursor_VALUE; Loop_INDEX < Hajmi; Loop_INDEX++) 명령해석기.satr[Loop_INDEX - kursor_VALUE + 변경전] = 명령해석기.satr[Loop_INDEX]; Hajmi -= kursor_VALUE - 변경전; kursor_VALUE = 변경전; }
                다시(); continue;
            }
            if (bayt_ma_lumotlar == 11) { Hajmi = kursor_VALUE; 다시(); continue; }
            if (bayt_ma_lumotlar < 32 && bayt_ma_lumotlar != 9) continue;
            if (Hajmi == 명령해석기.satr.length) { to_lib_ketish = true; continue; }
            for (int Loop_INDEX = Hajmi; Loop_INDEX > kursor_VALUE; Loop_INDEX--) 명령해석기.satr[Loop_INDEX] = 명령해석기.satr[Loop_INDEX - 1];
            명령해석기.satr[kursor_VALUE++] = bayt_ma_lumotlar; Hajmi++;
            if (kursor_VALUE == Hajmi && !가로보기 && 폭(0, Hajmi) <= 보이는폭()) yozuv_taxtasi.직렬쓰기(bayt_ma_lumotlar);
            else if (kursor_VALUE == Hajmi) 보이는줄(); else 다시();
        }
    }
}
