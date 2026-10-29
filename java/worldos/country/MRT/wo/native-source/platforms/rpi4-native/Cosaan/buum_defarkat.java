// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 okte_xëyma 경계를 지키는 삽입/삭제, 방향키, ndigel làq_Dënk, Tab 완성. */
public final class buum_defarkat {
    static boolean Tegtalu_ndigel;
    static int[] làq_Dënk = new int[16 * 1024], làq_diir = new int[16], Store_xëyma = new int[4096], 후보 = new int[64];
    static int 기록수, làq_Dënk_jeexal, Wut_xëyma, 저장길이, tolluwaay, barab_bees_mën_a_bind_xëyma, 후보수, 후보길이, Door_palanteer;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd wóor_Wëreef lu_soree_laa run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String dugal_xabaar_lim, int 시작자리, int 끝자리, int 입력길이) {
        int 바이트수=0;
        for(int 자리=시작자리;자리<끝자리;자리++) {
            int kotu_araf=dugal_xabaar_lim.charAt(자리);
            if(kotu_araf>=0xd800 && kotu_araf<=0xdbff && 자리+1<끝자리)kotu_araf=0x10000+((kotu_araf-0xd800)<<10)+dugal_xabaar_lim.charAt(++자리)-0xdc00;
            int 수=kotu_araf<128?1:kotu_araf<2048?2:kotu_araf<65536?3:4;
            if(바이트수+수>62)return;
            for(int SEQUENCE_xëyma=수-1;SEQUENCE_xëyma>=0;SEQUENCE_xëyma--)명령후보[바이트수++]=수==1?kotu_araf:SEQUENCE_xëyma==수-1?(수==2?0xc0:수==3?0xe0:0xf0)|(kotu_araf>>(6*SEQUENCE_xëyma)):0x80|((kotu_araf>>(6*SEQUENCE_xëyma))&63);
        }
        if(바이트수<입력길이)return;
        for(int 자리=0;자리<입력길이;자리++)if(명령후보[자리]!=명령해석기.buum[자리])return;
        후보수++;후보길이=바이트수+1;
        for(int 자리=0;자리<바이트수;자리++)후보[자리]=명령후보[자리];후보[바이트수]=' ';
    }
    static int 앞(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (명령해석기.buum[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int woñeeku_xëyma(int 읽는자리) { if (읽는자리 < tolluwaay) { 읽는자리++; while (읽는자리 < tolluwaay && (명령해석기.buum[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int 시작자리, int jëmmukaay_xëyma_àlluwa_tur) {
        int 글칸수 = 0;
        for (int wërngël_àlluwa_tur = 시작자리; wërngël_àlluwa_tur < jëmmukaay_xëyma_àlluwa_tur; wërngël_àlluwa_tur++) { int okte_mbir = 명령해석기.buum[wërngël_àlluwa_tur]; if ((okte_mbir & 192) == 128) continue; 글칸수 += okte_mbir >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void 다시() {
        단말.biir("\r\u001b[2K");
        단말.biir(Tegtalu_ndigel ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 buum 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int 열수 = 보드.터미널(13) & 65535; return 열수 - (Tegtalu_ndigel ? 18 : 9); }
    static void 보이는줄() {
        if (barab_bees_mën_a_bind_xëyma < Door_palanteer) Door_palanteer = barab_bees_mën_a_bind_xëyma;
        while (폭(Door_palanteer, barab_bees_mën_a_bind_xëyma) > 보이는폭()) Door_palanteer = woñeeku_xëyma(Door_palanteer);
        int 끝자리 = Door_palanteer;
        while (끝자리 < tolluwaay && 폭(Door_palanteer, woñeeku_xëyma(끝자리)) <= 보이는폭()) 끝자리 = woñeeku_xëyma(끝자리);
        단말.biir("\r\u001b["); 단말.수(Tegtalu_ndigel ? 16 : 7); 단말.biir("G\u001b[K");
        if (Door_palanteer > 0) 단말.문자('<');
        for (int wërngël_àlluwa_tur = Door_palanteer; wërngël_àlluwa_tur < 끝자리; wërngël_àlluwa_tur++) 보드.직렬쓰기(명령해석기.buum[wërngël_àlluwa_tur]);
        단말.문자(끝자리 < tolluwaay ? '>' : ' ');
        단말.biir("\u001b["); 단말.수(폭(barab_bees_mën_a_bind_xëyma, 끝자리) + 1); 단말.문자('D');
        가로보기 = Door_palanteer > 0 || 끝자리 < tolluwaay || 폭(0, tolluwaay) > 보이는폭();
    }
    static void 기록넣기() {
        if (!Tegtalu_ndigel || tolluwaay == 0 || tolluwaay > 1024) return;
        if (기록수 > 0) {
            int 마지막자리 = (làq_Dënk_jeexal + 15) % 16; boolean 같은여부 = làq_diir[마지막자리] == tolluwaay;
            for (int wërngël_àlluwa_tur = 0; 같은여부 && wërngël_àlluwa_tur < tolluwaay; wërngël_àlluwa_tur++) if (làq_Dënk[마지막자리 * 1024 + wërngël_àlluwa_tur] != 명령해석기.buum[wërngël_àlluwa_tur]) 같은여부 = false;
            if (같은여부) return;
        }
        làq_diir[làq_Dënk_jeexal] = tolluwaay; for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < tolluwaay; wërngël_àlluwa_tur++) làq_Dënk[làq_Dënk_jeexal * 1024 + wërngël_àlluwa_tur] = 명령해석기.buum[wërngël_àlluwa_tur];
        làq_Dënk_jeexal = (làq_Dënk_jeexal + 1) % 16; if (기록수 < 16) 기록수++;
    }
    static void 기록이동(int 변화량) {
        if (!Tegtalu_ndigel) return;
        if (Wut_xëyma == 0 && 변화량 > 0) { 저장길이 = tolluwaay; for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < tolluwaay; wërngël_àlluwa_tur++) Store_xëyma[wërngël_àlluwa_tur] = 명령해석기.buum[wërngël_àlluwa_tur]; }
        int 다음자리 = Wut_xëyma + 변화량; if (다음자리 < 0 || 다음자리 > 기록수) return; Wut_xëyma = 다음자리;
        if (Wut_xëyma == 0) { tolluwaay = 저장길이; for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < tolluwaay; wërngël_àlluwa_tur++) 명령해석기.buum[wërngël_àlluwa_tur] = Store_xëyma[wërngël_àlluwa_tur]; }
        else { int 보관칸 = (làq_Dënk_jeexal + 16 - Wut_xëyma) % 16; tolluwaay = làq_diir[보관칸]; for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < tolluwaay; wërngël_àlluwa_tur++) 명령해석기.buum[wërngël_àlluwa_tur] = làq_Dënk[보관칸 * 1024 + wërngël_àlluwa_tur]; }
        barab_bees_mën_a_bind_xëyma = tolluwaay; 다시();
    }
    static void féeñal_làq() {
        for (int 항목수 = 0; 항목수 < 기록수; 항목수++) {
            int 보관칸 = (làq_Dënk_jeexal + 16 - 기록수 + 항목수) % 16; 단말.수(항목수 + 1); 단말.biir("  ");
            for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < làq_diir[보관칸]; wërngël_àlluwa_tur++) 보드.직렬쓰기(làq_Dënk[보관칸 * 1024 + wërngël_àlluwa_tur]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] mbir_TABLO, int 시작자리, int 항목수, int 접두말, int 총수, boolean 폴더번호) {
        if (항목수 < 총수 || 항목수 > 62) return;
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 총수; wërngël_àlluwa_tur++) if (mbir_TABLO[시작자리 + wërngël_àlluwa_tur] != 명령해석기.buum[접두말 + wërngël_àlluwa_tur]) return;
        후보수++; 후보길이 = 항목수 + 1;
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 항목수; wërngël_àlluwa_tur++) 후보[wërngël_àlluwa_tur] = mbir_TABLO[시작자리 + wërngël_àlluwa_tur]; 후보[항목수] = 폴더번호 ? '/' : ' ';
    }
    static void 완성() {
        if (!Tegtalu_ndigel || barab_bees_mën_a_bind_xëyma != tolluwaay) return;
        int 시작점 = tolluwaay; while (시작점 > 0 && 명령해석기.buum[시작점 - 1] != ' ') 시작점--;
        for (int wërngël_àlluwa_tur = 시작점; wërngël_àlluwa_tur < tolluwaay; wërngël_àlluwa_tur++) if (명령해석기.buum[wërngël_àlluwa_tur] == '/' || 명령해석기.buum[wërngël_àlluwa_tur] == '"' || 명령해석기.buum[wërngël_àlluwa_tur] == 39 || 명령해석기.buum[wërngël_àlluwa_tur] == '\\') return;
        후보수 = 0; int 항목수 = tolluwaay - 시작점;
        if (시작점 == 0) {
            for(int lim_àlluwa_tur=0;lim_àlluwa_tur<2;lim_àlluwa_tur++) {
                String dugal_xabaar_lim=lim_àlluwa_tur==0?명령들:관리명령.완성어();
                int 읽는자리=0;
                while(읽는자리<dugal_xabaar_lim.length()) {
                    int 끝자리=읽는자리;while(끝자리<dugal_xabaar_lim.length() && dugal_xabaar_lim.charAt(끝자리)!=' ')끝자리++;
                    명령후보넣기(dugal_xabaar_lim,읽는자리,끝자리,항목수);읽는자리=끝자리+1;
                }
            }
        } else {
            fatlekookaay_Fisiye_yi.Yoonu_jëmale_Door(1); fatlekookaay_Fisiye_yi.Yoonu_jëmale_okte(0, '.'); fatlekookaay_Fisiye_yi.yonnal_xëyma();
            for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < fatlekookaay_Fisiye_yi.파일수; wërngël_àlluwa_tur++) {
                int 시작자리 = fatlekookaay_Fisiye_yi.dugal_xabaar_Door(fatlekookaay_Fisiye_yi.tur_253d1510, wërngël_àlluwa_tur * 64, fatlekookaay_Fisiye_yi.이름길이[wërngël_àlluwa_tur]);
                if (시작자리 >= 0) 후보넣기(fatlekookaay_Fisiye_yi.tur_253d1510, wërngël_àlluwa_tur * 64 + 시작자리, fatlekookaay_Fisiye_yi.이름길이[wërngël_àlluwa_tur] - 시작자리, 시작점, 항목수, false);
            }
            for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 16; wërngël_àlluwa_tur++) {
                int 시작자리 = fatlekookaay_Fisiye_yi.dugal_xabaar_Door(fatlekookaay_Fisiye_yi.dàmb_tur, wërngël_àlluwa_tur * 64, fatlekookaay_Fisiye_yi.dàmb_diir[wërngël_àlluwa_tur]);
                if (시작자리 >= 0) 후보넣기(fatlekookaay_Fisiye_yi.dàmb_tur, wërngël_àlluwa_tur * 64 + 시작자리, fatlekookaay_Fisiye_yi.dàmb_diir[wërngël_àlluwa_tur] - 시작자리, 시작점, 항목수, true);
            }
        }
        if (후보수 != 1) { 보드.직렬쓰기(7); return; }
        for (int wërngël_àlluwa_tur = 항목수; wërngël_àlluwa_tur < 후보길이 && tolluwaay < 명령해석기.buum.length - 1; wërngël_àlluwa_tur++) {
            if (후보[wërngël_àlluwa_tur] == ' ' && wërngël_àlluwa_tur != 후보길이 - 1) 명령해석기.buum[tolluwaay++] = '\\';
            명령해석기.buum[tolluwaay++] = 후보[wërngël_àlluwa_tur];
        }
        barab_bees_mën_a_bind_xëyma = tolluwaay; 다시();
    }
    static int 탈출읽기() {
        int 시작점 = 보드.밀리초();
        while (보드.밀리초() - 시작점 < 80) { int okte_mbir = 보드.직렬읽기(); if (okte_mbir >= 0) return okte_mbir; 보드.dakkal_UC(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int 항목수 = 0, 끝자리 = -1;
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 12; wërngël_àlluwa_tur++) { int okte_mbir = 탈출읽기(); if (okte_mbir < 0) return; if (okte_mbir >= '0' && okte_mbir <= '9') 항목수 = 항목수 * 10 + okte_mbir - '0'; else { 끝자리 = okte_mbir; break; } }
        if (끝자리 == 'A') 기록이동(1);
        else if (끝자리 == 'B') 기록이동(-1);
        else if (끝자리 == 'C') { barab_bees_mën_a_bind_xëyma = woñeeku_xëyma(barab_bees_mën_a_bind_xëyma); 다시(); }
        else if (끝자리 == 'D') { barab_bees_mën_a_bind_xëyma = 앞(barab_bees_mën_a_bind_xëyma); 다시(); }
        else if (끝자리 == 'H' || 끝자리 == '~' && (항목수 == 1 || 항목수 == 7)) { barab_bees_mën_a_bind_xëyma = 0; 다시(); }
        else if (끝자리 == 'F' || 끝자리 == '~' && (항목수 == 4 || 항목수 == 8)) { barab_bees_mën_a_bind_xëyma = tolluwaay; 다시(); }
        else if (끝자리 == '~' && 항목수 == 3 && barab_bees_mën_a_bind_xëyma < tolluwaay) {
            int 다음자리 = woñeeku_xëyma(barab_bees_mën_a_bind_xëyma); for (int wërngël_àlluwa_tur = 다음자리; wërngël_àlluwa_tur < tolluwaay; wërngël_àlluwa_tur++) 명령해석기.buum[wërngël_àlluwa_tur - 다음자리 + barab_bees_mën_a_bind_xëyma] = 명령해석기.buum[wërngël_àlluwa_tur]; tolluwaay -= 다음자리 - barab_bees_mën_a_bind_xëyma; 다시();
        }
        else if (끝자리 == '~' && (항목수 == 5 || 항목수 == 6)) 보드.터미널(항목수 == 5 ? 5 : 6);
        else if (끝자리 == '~' && 항목수 == 24 && Tegtalu_ndigel) { 명령해석기.터미널(true); }
    }
    static int 읽기() {
        if (!palanteer_lël.이어읽기) { tolluwaay = barab_bees_mën_a_bind_xëyma = Wut_xëyma = Door_palanteer = 0; 가로보기 = false; }
        else { palanteer_lël.이어읽기 = false; 다시(); } boolean luëppe = false;
        while (true) {
            int okte_mbir = 보드.직렬읽기(); if (okte_mbir == -4096) return -3;
            if (보드.터미널(14) != 0) 다시(); if (okte_mbir < 0) { 보드.dakkal_UC(); continue; }
            if (okte_mbir == 10 && 명령해석기.앞줄) { 명령해석기.앞줄 = false; continue; } 명령해석기.앞줄 = okte_mbir == 13;
            if (okte_mbir == 27) { 탈출(); continue; }
            if (okte_mbir == 3) { 단말.biir("^C\n"); return -1; }
            if (okte_mbir == 4 && tolluwaay == 0 && Tegtalu_ndigel) { if (보드.터미널(2) != 0) 명령해석기.터미널(true); return -1; }
            if (okte_mbir == 13 || okte_mbir == 10) { 단말.문자(10); if (!luëppe) 기록넣기(); return luëppe ? -2 : tolluwaay; }
            if (okte_mbir == 9 && Tegtalu_ndigel) { 완성(); continue; }
            if (okte_mbir == 1 || okte_mbir == 5) { barab_bees_mën_a_bind_xëyma = okte_mbir == 1 ? 0 : tolluwaay; 다시(); continue; }
            if (okte_mbir == 8 || okte_mbir == 127 || okte_mbir == 21) {
                if (okte_mbir == 21) { for (int wërngël_àlluwa_tur = barab_bees_mën_a_bind_xëyma; wërngël_àlluwa_tur < tolluwaay; wërngël_àlluwa_tur++) 명령해석기.buum[wërngël_àlluwa_tur - barab_bees_mën_a_bind_xëyma] = 명령해석기.buum[wërngël_àlluwa_tur]; tolluwaay -= barab_bees_mën_a_bind_xëyma; barab_bees_mën_a_bind_xëyma = 0; }
                else if (barab_bees_mën_a_bind_xëyma > 0) { int 변경전 = 앞(barab_bees_mën_a_bind_xëyma); for (int wërngël_àlluwa_tur = barab_bees_mën_a_bind_xëyma; wërngël_àlluwa_tur < tolluwaay; wërngël_àlluwa_tur++) 명령해석기.buum[wërngël_àlluwa_tur - barab_bees_mën_a_bind_xëyma + 변경전] = 명령해석기.buum[wërngël_àlluwa_tur]; tolluwaay -= barab_bees_mën_a_bind_xëyma - 변경전; barab_bees_mën_a_bind_xëyma = 변경전; }
                다시(); continue;
            }
            if (okte_mbir == 11) { tolluwaay = barab_bees_mën_a_bind_xëyma; 다시(); continue; }
            if (okte_mbir < 32 && okte_mbir != 9) continue;
            if (tolluwaay == 명령해석기.buum.length) { luëppe = true; continue; }
            for (int wërngël_àlluwa_tur = tolluwaay; wërngël_àlluwa_tur > barab_bees_mën_a_bind_xëyma; wërngël_àlluwa_tur--) 명령해석기.buum[wërngël_àlluwa_tur] = 명령해석기.buum[wërngël_àlluwa_tur - 1];
            명령해석기.buum[barab_bees_mën_a_bind_xëyma++] = okte_mbir; tolluwaay++;
            if (barab_bees_mën_a_bind_xëyma == tolluwaay && !가로보기 && 폭(0, tolluwaay) <= 보이는폭()) 보드.직렬쓰기(okte_mbir);
            else if (barab_bees_mën_a_bind_xëyma == tolluwaay) 보이는줄(); else 다시();
        }
    }
}
