// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 baiti_thamani 경계를 지키는 삽입/삭제, 방향키, amri batli_REKODI, Tab 완성. */
public final class laini_Kihariri {
    static boolean tungo_amri;
    static int[] batli_REKODI = new int[16 * 1024], batli_urefu = new int[16], Store_thamani = new int[4096], 후보 = new int[64];
    static int 기록수, batli_REKODI_tamatia, Duhusi_thamani, 저장길이, panga_ukubwa, kielekezi_thamani, 후보수, 후보길이, Anza_dirisha;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd salama_sheli kwa_mbali_onyesha run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String ingizo_Orodha, int 시작자리, int 끝자리, int 입력길이) {
        int 바이트수=0;
        for(int 자리=시작자리;자리<끝자리;자리++) {
            int msimbo_wa_kibambo=ingizo_Orodha.charAt(자리);
            if(msimbo_wa_kibambo>=0xd800 && msimbo_wa_kibambo<=0xdbff && 자리+1<끝자리)msimbo_wa_kibambo=0x10000+((msimbo_wa_kibambo-0xd800)<<10)+ingizo_Orodha.charAt(++자리)-0xdc00;
            int 수=msimbo_wa_kibambo<128?1:msimbo_wa_kibambo<2048?2:msimbo_wa_kibambo<65536?3:4;
            if(바이트수+수>62)return;
            for(int MFUATANO_thamani=수-1;MFUATANO_thamani>=0;MFUATANO_thamani--)명령후보[바이트수++]=수==1?msimbo_wa_kibambo:MFUATANO_thamani==수-1?(수==2?0xc0:수==3?0xe0:0xf0)|(msimbo_wa_kibambo>>(6*MFUATANO_thamani)):0x80|((msimbo_wa_kibambo>>(6*MFUATANO_thamani))&63);
        }
        if(바이트수<입력길이)return;
        for(int 자리=0;자리<입력길이;자리++)if(명령후보[자리]!=명령해석기.laini[자리])return;
        후보수++;후보길이=바이트수+1;
        for(int 자리=0;자리<바이트수;자리++)후보[자리]=명령후보[자리];후보[바이트수]=' ';
    }
    static int mbele_thamani(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (명령해석기.laini[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int Nyuma_thamani(int 읽는자리) { if (읽는자리 < panga_ukubwa) { 읽는자리++; while (읽는자리 < panga_ukubwa && (명령해석기.laini[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int 시작자리, int fikio_thamani_kielezo) {
        int 글칸수 = 0;
        for (int kitanzi_kielezo = 시작자리; kitanzi_kielezo < fikio_thamani_kielezo; kitanzi_kielezo++) { int baiti_data = 명령해석기.laini[kitanzi_kielezo]; if ((baiti_data & 192) == 128) continue; 글칸수 += baiti_data >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void 다시() {
        단말.andika("\r\u001b[2K");
        단말.andika(tungo_amri ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 laini 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int 열수 = 보드.터미널(13) & 65535; return 열수 - (tungo_amri ? 18 : 9); }
    static void 보이는줄() {
        if (kielekezi_thamani < Anza_dirisha) Anza_dirisha = kielekezi_thamani;
        while (폭(Anza_dirisha, kielekezi_thamani) > 보이는폭()) Anza_dirisha = Nyuma_thamani(Anza_dirisha);
        int 끝자리 = Anza_dirisha;
        while (끝자리 < panga_ukubwa && 폭(Anza_dirisha, Nyuma_thamani(끝자리)) <= 보이는폭()) 끝자리 = Nyuma_thamani(끝자리);
        단말.andika("\r\u001b["); 단말.수(tungo_amri ? 16 : 7); 단말.andika("G\u001b[K");
        if (Anza_dirisha > 0) 단말.문자('<');
        for (int kitanzi_kielezo = Anza_dirisha; kitanzi_kielezo < 끝자리; kitanzi_kielezo++) 보드.직렬쓰기(명령해석기.laini[kitanzi_kielezo]);
        단말.문자(끝자리 < panga_ukubwa ? '>' : ' ');
        단말.andika("\u001b["); 단말.수(폭(kielekezi_thamani, 끝자리) + 1); 단말.문자('D');
        가로보기 = Anza_dirisha > 0 || 끝자리 < panga_ukubwa || 폭(0, panga_ukubwa) > 보이는폭();
    }
    static void 기록넣기() {
        if (!tungo_amri || panga_ukubwa == 0 || panga_ukubwa > 1024) return;
        if (기록수 > 0) {
            int 마지막자리 = (batli_REKODI_tamatia + 15) % 16; boolean 같은여부 = batli_urefu[마지막자리] == panga_ukubwa;
            for (int kitanzi_kielezo = 0; 같은여부 && kitanzi_kielezo < panga_ukubwa; kitanzi_kielezo++) if (batli_REKODI[마지막자리 * 1024 + kitanzi_kielezo] != 명령해석기.laini[kitanzi_kielezo]) 같은여부 = false;
            if (같은여부) return;
        }
        batli_urefu[batli_REKODI_tamatia] = panga_ukubwa; for (int kitanzi_kielezo = 0; kitanzi_kielezo < panga_ukubwa; kitanzi_kielezo++) batli_REKODI[batli_REKODI_tamatia * 1024 + kitanzi_kielezo] = 명령해석기.laini[kitanzi_kielezo];
        batli_REKODI_tamatia = (batli_REKODI_tamatia + 1) % 16; if (기록수 < 16) 기록수++;
    }
    static void 기록이동(int 변화량) {
        if (!tungo_amri) return;
        if (Duhusi_thamani == 0 && 변화량 > 0) { 저장길이 = panga_ukubwa; for (int kitanzi_kielezo = 0; kitanzi_kielezo < panga_ukubwa; kitanzi_kielezo++) Store_thamani[kitanzi_kielezo] = 명령해석기.laini[kitanzi_kielezo]; }
        int 다음자리 = Duhusi_thamani + 변화량; if (다음자리 < 0 || 다음자리 > 기록수) return; Duhusi_thamani = 다음자리;
        if (Duhusi_thamani == 0) { panga_ukubwa = 저장길이; for (int kitanzi_kielezo = 0; kitanzi_kielezo < panga_ukubwa; kitanzi_kielezo++) 명령해석기.laini[kitanzi_kielezo] = Store_thamani[kitanzi_kielezo]; }
        else { int 보관칸 = (batli_REKODI_tamatia + 16 - Duhusi_thamani) % 16; panga_ukubwa = batli_urefu[보관칸]; for (int kitanzi_kielezo = 0; kitanzi_kielezo < panga_ukubwa; kitanzi_kielezo++) 명령해석기.laini[kitanzi_kielezo] = batli_REKODI[보관칸 * 1024 + kitanzi_kielezo]; }
        kielekezi_thamani = panga_ukubwa; 다시();
    }
    static void onyesha_batli() {
        for (int 항목수 = 0; 항목수 < 기록수; 항목수++) {
            int 보관칸 = (batli_REKODI_tamatia + 16 - 기록수 + 항목수) % 16; 단말.수(항목수 + 1); 단말.andika("  ");
            for (int kitanzi_kielezo = 0; kitanzi_kielezo < batli_urefu[보관칸]; kitanzi_kielezo++) 보드.직렬쓰기(batli_REKODI[보관칸 * 1024 + kitanzi_kielezo]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] data_ARRAY, int 시작자리, int 항목수, int 접두말, int 총수, boolean 폴더번호) {
        if (항목수 < 총수 || 항목수 > 62) return;
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < 총수; kitanzi_kielezo++) if (data_ARRAY[시작자리 + kitanzi_kielezo] != 명령해석기.laini[접두말 + kitanzi_kielezo]) return;
        후보수++; 후보길이 = 항목수 + 1;
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < 항목수; kitanzi_kielezo++) 후보[kitanzi_kielezo] = data_ARRAY[시작자리 + kitanzi_kielezo]; 후보[항목수] = 폴더번호 ? '/' : ' ';
    }
    static void 완성() {
        if (!tungo_amri || kielekezi_thamani != panga_ukubwa) return;
        int 시작점 = panga_ukubwa; while (시작점 > 0 && 명령해석기.laini[시작점 - 1] != ' ') 시작점--;
        for (int kitanzi_kielezo = 시작점; kitanzi_kielezo < panga_ukubwa; kitanzi_kielezo++) if (명령해석기.laini[kitanzi_kielezo] == '/' || 명령해석기.laini[kitanzi_kielezo] == '"' || 명령해석기.laini[kitanzi_kielezo] == 39 || 명령해석기.laini[kitanzi_kielezo] == '\\') return;
        후보수 = 0; int 항목수 = panga_ukubwa - 시작점;
        if (시작점 == 0) {
            for(int Orodha_kielezo=0;Orodha_kielezo<2;Orodha_kielezo++) {
                String ingizo_Orodha=Orodha_kielezo==0?명령들:관리명령.완성어();
                int 읽는자리=0;
                while(읽는자리<ingizo_Orodha.length()) {
                    int 끝자리=읽는자리;while(끝자리<ingizo_Orodha.length() && ingizo_Orodha.charAt(끝자리)!=' ')끝자리++;
                    명령후보넣기(ingizo_Orodha,읽는자리,끝자리,항목수);읽는자리=끝자리+1;
                }
            }
        } else {
            kumbukumbu_Faili.njia_Anza(1); kumbukumbu_Faili.njia_baiti(0, '.'); kumbukumbu_Faili.kawaidisha_thamani();
            for (int kitanzi_kielezo = 0; kitanzi_kielezo < kumbukumbu_Faili.파일수; kitanzi_kielezo++) {
                int 시작자리 = kumbukumbu_Faili.ingizo_Anza(kumbukumbu_Faili.Jina, kitanzi_kielezo * 64, kumbukumbu_Faili.이름길이[kitanzi_kielezo]);
                if (시작자리 >= 0) 후보넣기(kumbukumbu_Faili.Jina, kitanzi_kielezo * 64 + 시작자리, kumbukumbu_Faili.이름길이[kitanzi_kielezo] - 시작자리, 시작점, 항목수, false);
            }
            for (int kitanzi_kielezo = 0; kitanzi_kielezo < 16; kitanzi_kielezo++) {
                int 시작자리 = kumbukumbu_Faili.ingizo_Anza(kumbukumbu_Faili.Saraka_jina, kitanzi_kielezo * 64, kumbukumbu_Faili.Saraka_urefu[kitanzi_kielezo]);
                if (시작자리 >= 0) 후보넣기(kumbukumbu_Faili.Saraka_jina, kitanzi_kielezo * 64 + 시작자리, kumbukumbu_Faili.Saraka_urefu[kitanzi_kielezo] - 시작자리, 시작점, 항목수, true);
            }
        }
        if (후보수 != 1) { 보드.직렬쓰기(7); return; }
        for (int kitanzi_kielezo = 항목수; kitanzi_kielezo < 후보길이 && panga_ukubwa < 명령해석기.laini.length - 1; kitanzi_kielezo++) {
            if (후보[kitanzi_kielezo] == ' ' && kitanzi_kielezo != 후보길이 - 1) 명령해석기.laini[panga_ukubwa++] = '\\';
            명령해석기.laini[panga_ukubwa++] = 후보[kitanzi_kielezo];
        }
        kielekezi_thamani = panga_ukubwa; 다시();
    }
    static int 탈출읽기() {
        int 시작점 = 보드.밀리초();
        while (보드.밀리초() - 시작점 < 80) { int baiti_data = 보드.직렬읽기(); if (baiti_data >= 0) return baiti_data; 보드.ahirisha_CPU(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int 항목수 = 0, 끝자리 = -1;
        for (int kitanzi_kielezo = 0; kitanzi_kielezo < 12; kitanzi_kielezo++) { int baiti_data = 탈출읽기(); if (baiti_data < 0) return; if (baiti_data >= '0' && baiti_data <= '9') 항목수 = 항목수 * 10 + baiti_data - '0'; else { 끝자리 = baiti_data; break; } }
        if (끝자리 == 'A') 기록이동(1);
        else if (끝자리 == 'B') 기록이동(-1);
        else if (끝자리 == 'C') { kielekezi_thamani = Nyuma_thamani(kielekezi_thamani); 다시(); }
        else if (끝자리 == 'D') { kielekezi_thamani = mbele_thamani(kielekezi_thamani); 다시(); }
        else if (끝자리 == 'H' || 끝자리 == '~' && (항목수 == 1 || 항목수 == 7)) { kielekezi_thamani = 0; 다시(); }
        else if (끝자리 == 'F' || 끝자리 == '~' && (항목수 == 4 || 항목수 == 8)) { kielekezi_thamani = panga_ukubwa; 다시(); }
        else if (끝자리 == '~' && 항목수 == 3 && kielekezi_thamani < panga_ukubwa) {
            int 다음자리 = Nyuma_thamani(kielekezi_thamani); for (int kitanzi_kielezo = 다음자리; kitanzi_kielezo < panga_ukubwa; kitanzi_kielezo++) 명령해석기.laini[kitanzi_kielezo - 다음자리 + kielekezi_thamani] = 명령해석기.laini[kitanzi_kielezo]; panga_ukubwa -= 다음자리 - kielekezi_thamani; 다시();
        }
        else if (끝자리 == '~' && (항목수 == 5 || 항목수 == 6)) 보드.터미널(항목수 == 5 ? 5 : 6);
        else if (끝자리 == '~' && 항목수 == 24 && tungo_amri) { 명령해석기.터미널(true); }
    }
    static int 읽기() {
        if (!dirisha_kipindi.이어읽기) { panga_ukubwa = kielekezi_thamani = Duhusi_thamani = Anza_dirisha = 0; 가로보기 = false; }
        else { dirisha_kipindi.이어읽기 = false; 다시(); } boolean ziada = false;
        while (true) {
            int baiti_data = 보드.직렬읽기(); if (baiti_data == -4096) return -3;
            if (보드.터미널(14) != 0) 다시(); if (baiti_data < 0) { 보드.ahirisha_CPU(); continue; }
            if (baiti_data == 10 && 명령해석기.앞줄) { 명령해석기.앞줄 = false; continue; } 명령해석기.앞줄 = baiti_data == 13;
            if (baiti_data == 27) { 탈출(); continue; }
            if (baiti_data == 3) { 단말.andika("^C\n"); return -1; }
            if (baiti_data == 4 && panga_ukubwa == 0 && tungo_amri) { if (보드.터미널(2) != 0) 명령해석기.터미널(true); return -1; }
            if (baiti_data == 13 || baiti_data == 10) { 단말.문자(10); if (!ziada) 기록넣기(); return ziada ? -2 : panga_ukubwa; }
            if (baiti_data == 9 && tungo_amri) { 완성(); continue; }
            if (baiti_data == 1 || baiti_data == 5) { kielekezi_thamani = baiti_data == 1 ? 0 : panga_ukubwa; 다시(); continue; }
            if (baiti_data == 8 || baiti_data == 127 || baiti_data == 21) {
                if (baiti_data == 21) { for (int kitanzi_kielezo = kielekezi_thamani; kitanzi_kielezo < panga_ukubwa; kitanzi_kielezo++) 명령해석기.laini[kitanzi_kielezo - kielekezi_thamani] = 명령해석기.laini[kitanzi_kielezo]; panga_ukubwa -= kielekezi_thamani; kielekezi_thamani = 0; }
                else if (kielekezi_thamani > 0) { int 변경전 = mbele_thamani(kielekezi_thamani); for (int kitanzi_kielezo = kielekezi_thamani; kitanzi_kielezo < panga_ukubwa; kitanzi_kielezo++) 명령해석기.laini[kitanzi_kielezo - kielekezi_thamani + 변경전] = 명령해석기.laini[kitanzi_kielezo]; panga_ukubwa -= kielekezi_thamani - 변경전; kielekezi_thamani = 변경전; }
                다시(); continue;
            }
            if (baiti_data == 11) { panga_ukubwa = kielekezi_thamani; 다시(); continue; }
            if (baiti_data < 32 && baiti_data != 9) continue;
            if (panga_ukubwa == 명령해석기.laini.length) { ziada = true; continue; }
            for (int kitanzi_kielezo = panga_ukubwa; kitanzi_kielezo > kielekezi_thamani; kitanzi_kielezo--) 명령해석기.laini[kitanzi_kielezo] = 명령해석기.laini[kitanzi_kielezo - 1];
            명령해석기.laini[kielekezi_thamani++] = baiti_data; panga_ukubwa++;
            if (kielekezi_thamani == panga_ukubwa && !가로보기 && 폭(0, panga_ukubwa) <= 보이는폭()) 보드.직렬쓰기(baiti_data);
            else if (kielekezi_thamani == panga_ukubwa) 보이는줄(); else 다시();
        }
    }
}
