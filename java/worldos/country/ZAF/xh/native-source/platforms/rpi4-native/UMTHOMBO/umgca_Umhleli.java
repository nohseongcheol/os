// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 ibhayithi_ixabiso 경계를 지키는 삽입/삭제, 방향키, Umyalelo ilog_umqolo, Tab 완성. */
public final class umgca_Umhleli {
    static boolean umgca_wemiyalelo;
    static int[] ilog_umqolo = new int[16 * 1024], ilog_ubude = new int[16], Store_ixabiso = new int[4096], 후보 = new int[64];
    static int 기록수, ilog_umqolo_phela, Khangela_ixabiso, 저장길이, Ubukhulu, ikhesa_ixabiso, 후보수, 후보길이, qala_i_window;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd ikhuselekile_isiniki_myalelo kude_bonisa run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String ufako_nkcukacha_uludwe, int 시작자리, int 끝자리, int 입력길이) {
        int 바이트수=0;
        for(int 자리=시작자리;자리<끝자리;자리++) {
            int ikhowudi_yekharakhtha=ufako_nkcukacha_uludwe.charAt(자리);
            if(ikhowudi_yekharakhtha>=0xd800 && ikhowudi_yekharakhtha<=0xdbff && 자리+1<끝자리)ikhowudi_yekharakhtha=0x10000+((ikhowudi_yekharakhtha-0xd800)<<10)+ufako_nkcukacha_uludwe.charAt(++자리)-0xdc00;
            int 수=ikhowudi_yekharakhtha<128?1:ikhowudi_yekharakhtha<2048?2:ikhowudi_yekharakhtha<65536?3:4;
            if(바이트수+수>62)return;
            for(int ULANDELELWANO_ixabiso=수-1;ULANDELELWANO_ixabiso>=0;ULANDELELWANO_ixabiso--)명령후보[바이트수++]=수==1?ikhowudi_yekharakhtha:ULANDELELWANO_ixabiso==수-1?(수==2?0xc0:수==3?0xe0:0xf0)|(ikhowudi_yekharakhtha>>(6*ULANDELELWANO_ixabiso)):0x80|((ikhowudi_yekharakhtha>>(6*ULANDELELWANO_ixabiso))&63);
        }
        if(바이트수<입력길이)return;
        for(int 자리=0;자리<입력길이;자리++)if(명령후보[자리]!=명령해석기.umgca[자리])return;
        후보수++;후보길이=바이트수+1;
        for(int 자리=0;자리<바이트수;자리++)후보[자리]=명령후보[자리];후보[바이트수]=' ';
    }
    static int 앞(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (명령해석기.umgca[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int Emva_ixabiso(int 읽는자리) { if (읽는자리 < Ubukhulu) { 읽는자리++; while (읽는자리 < Ubukhulu && (명령해석기.umgca[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int 시작자리, int indawo_ekuyiwa_kuyo_ixabiso_indeksa) {
        int 글칸수 = 0;
        for (int iluphu_indeksa = 시작자리; iluphu_indeksa < indawo_ekuyiwa_kuyo_ixabiso_indeksa; iluphu_indeksa++) { int ibhayithi_iingcombolo = 명령해석기.umgca[iluphu_indeksa]; if ((ibhayithi_iingcombolo & 192) == 128) continue; 글칸수 += ibhayithi_iingcombolo >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void 다시() {
        단말.Bhala("\r\u001b[2K");
        단말.Bhala(umgca_wemiyalelo ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 umgca 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int 열수 = 보드.i_Terminal(13) & 65535; return 열수 - (umgca_wemiyalelo ? 18 : 9); }
    static void 보이는줄() {
        if (ikhesa_ixabiso < qala_i_window) qala_i_window = ikhesa_ixabiso;
        while (폭(qala_i_window, ikhesa_ixabiso) > 보이는폭()) qala_i_window = Emva_ixabiso(qala_i_window);
        int 끝자리 = qala_i_window;
        while (끝자리 < Ubukhulu && 폭(qala_i_window, Emva_ixabiso(끝자리)) <= 보이는폭()) 끝자리 = Emva_ixabiso(끝자리);
        단말.Bhala("\r\u001b["); 단말.수(umgca_wemiyalelo ? 16 : 7); 단말.Bhala("G\u001b[K");
        if (qala_i_window > 0) 단말.문자('<');
        for (int iluphu_indeksa = qala_i_window; iluphu_indeksa < 끝자리; iluphu_indeksa++) 보드.직렬쓰기(명령해석기.umgca[iluphu_indeksa]);
        단말.문자(끝자리 < Ubukhulu ? '>' : ' ');
        단말.Bhala("\u001b["); 단말.수(폭(ikhesa_ixabiso, 끝자리) + 1); 단말.문자('D');
        가로보기 = qala_i_window > 0 || 끝자리 < Ubukhulu || 폭(0, Ubukhulu) > 보이는폭();
    }
    static void 기록넣기() {
        if (!umgca_wemiyalelo || Ubukhulu == 0 || Ubukhulu > 1024) return;
        if (기록수 > 0) {
            int 마지막자리 = (ilog_umqolo_phela + 15) % 16; boolean 같은여부 = ilog_ubude[마지막자리] == Ubukhulu;
            for (int iluphu_indeksa = 0; 같은여부 && iluphu_indeksa < Ubukhulu; iluphu_indeksa++) if (ilog_umqolo[마지막자리 * 1024 + iluphu_indeksa] != 명령해석기.umgca[iluphu_indeksa]) 같은여부 = false;
            if (같은여부) return;
        }
        ilog_ubude[ilog_umqolo_phela] = Ubukhulu; for (int iluphu_indeksa = 0; iluphu_indeksa < Ubukhulu; iluphu_indeksa++) ilog_umqolo[ilog_umqolo_phela * 1024 + iluphu_indeksa] = 명령해석기.umgca[iluphu_indeksa];
        ilog_umqolo_phela = (ilog_umqolo_phela + 1) % 16; if (기록수 < 16) 기록수++;
    }
    static void 기록이동(int 변화량) {
        if (!umgca_wemiyalelo) return;
        if (Khangela_ixabiso == 0 && 변화량 > 0) { 저장길이 = Ubukhulu; for (int iluphu_indeksa = 0; iluphu_indeksa < Ubukhulu; iluphu_indeksa++) Store_ixabiso[iluphu_indeksa] = 명령해석기.umgca[iluphu_indeksa]; }
        int 다음자리 = Khangela_ixabiso + 변화량; if (다음자리 < 0 || 다음자리 > 기록수) return; Khangela_ixabiso = 다음자리;
        if (Khangela_ixabiso == 0) { Ubukhulu = 저장길이; for (int iluphu_indeksa = 0; iluphu_indeksa < Ubukhulu; iluphu_indeksa++) 명령해석기.umgca[iluphu_indeksa] = Store_ixabiso[iluphu_indeksa]; }
        else { int 보관칸 = (ilog_umqolo_phela + 16 - Khangela_ixabiso) % 16; Ubukhulu = ilog_ubude[보관칸]; for (int iluphu_indeksa = 0; iluphu_indeksa < Ubukhulu; iluphu_indeksa++) 명령해석기.umgca[iluphu_indeksa] = ilog_umqolo[보관칸 * 1024 + iluphu_indeksa]; }
        ikhesa_ixabiso = Ubukhulu; 다시();
    }
    static void bonisa_ilog() {
        for (int 항목수 = 0; 항목수 < 기록수; 항목수++) {
            int 보관칸 = (ilog_umqolo_phela + 16 - 기록수 + 항목수) % 16; 단말.수(항목수 + 1); 단말.Bhala("  ");
            for (int iluphu_indeksa = 0; iluphu_indeksa < ilog_ubude[보관칸]; iluphu_indeksa++) 보드.직렬쓰기(ilog_umqolo[보관칸 * 1024 + iluphu_indeksa]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] iingcombolo_ULUHLU, int 시작자리, int 항목수, int 접두말, int 총수, boolean 폴더번호) {
        if (항목수 < 총수 || 항목수 > 62) return;
        for (int iluphu_indeksa = 0; iluphu_indeksa < 총수; iluphu_indeksa++) if (iingcombolo_ULUHLU[시작자리 + iluphu_indeksa] != 명령해석기.umgca[접두말 + iluphu_indeksa]) return;
        후보수++; 후보길이 = 항목수 + 1;
        for (int iluphu_indeksa = 0; iluphu_indeksa < 항목수; iluphu_indeksa++) 후보[iluphu_indeksa] = iingcombolo_ULUHLU[시작자리 + iluphu_indeksa]; 후보[항목수] = 폴더번호 ? '/' : ' ';
    }
    static void 완성() {
        if (!umgca_wemiyalelo || ikhesa_ixabiso != Ubukhulu) return;
        int 시작점 = Ubukhulu; while (시작점 > 0 && 명령해석기.umgca[시작점 - 1] != ' ') 시작점--;
        for (int iluphu_indeksa = 시작점; iluphu_indeksa < Ubukhulu; iluphu_indeksa++) if (명령해석기.umgca[iluphu_indeksa] == '/' || 명령해석기.umgca[iluphu_indeksa] == '"' || 명령해석기.umgca[iluphu_indeksa] == 39 || 명령해석기.umgca[iluphu_indeksa] == '\\') return;
        후보수 = 0; int 항목수 = Ubukhulu - 시작점;
        if (시작점 == 0) {
            for(int uludwe_indeksa=0;uludwe_indeksa<2;uludwe_indeksa++) {
                String ufako_nkcukacha_uludwe=uludwe_indeksa==0?명령들:관리명령.완성어();
                int 읽는자리=0;
                while(읽는자리<ufako_nkcukacha_uludwe.length()) {
                    int 끝자리=읽는자리;while(끝자리<ufako_nkcukacha_uludwe.length() && ufako_nkcukacha_uludwe.charAt(끝자리)!=' ')끝자리++;
                    명령후보넣기(ufako_nkcukacha_uludwe,읽는자리,끝자리,항목수);읽는자리=끝자리+1;
                }
            }
        } else {
            imemori_Iifayile.indlela_qala(1); imemori_Iifayile.indlela_ibhayithi(0, '.'); imemori_Iifayile.qhelekisa_ixabiso();
            for (int iluphu_indeksa = 0; iluphu_indeksa < imemori_Iifayile.파일수; iluphu_indeksa++) {
                int 시작자리 = imemori_Iifayile.ufako_nkcukacha_qala(imemori_Iifayile.Igama, iluphu_indeksa * 64, imemori_Iifayile.이름길이[iluphu_indeksa]);
                if (시작자리 >= 0) 후보넣기(imemori_Iifayile.Igama, iluphu_indeksa * 64 + 시작자리, imemori_Iifayile.이름길이[iluphu_indeksa] - 시작자리, 시작점, 항목수, false);
            }
            for (int iluphu_indeksa = 0; iluphu_indeksa < 16; iluphu_indeksa++) {
                int 시작자리 = imemori_Iifayile.ufako_nkcukacha_qala(imemori_Iifayile.isalathisi_igama, iluphu_indeksa * 64, imemori_Iifayile.isalathisi_ubude[iluphu_indeksa]);
                if (시작자리 >= 0) 후보넣기(imemori_Iifayile.isalathisi_igama, iluphu_indeksa * 64 + 시작자리, imemori_Iifayile.isalathisi_ubude[iluphu_indeksa] - 시작자리, 시작점, 항목수, true);
            }
        }
        if (후보수 != 1) { 보드.직렬쓰기(7); return; }
        for (int iluphu_indeksa = 항목수; iluphu_indeksa < 후보길이 && Ubukhulu < 명령해석기.umgca.length - 1; iluphu_indeksa++) {
            if (후보[iluphu_indeksa] == ' ' && iluphu_indeksa != 후보길이 - 1) 명령해석기.umgca[Ubukhulu++] = '\\';
            명령해석기.umgca[Ubukhulu++] = 후보[iluphu_indeksa];
        }
        ikhesa_ixabiso = Ubukhulu; 다시();
    }
    static int 탈출읽기() {
        int 시작점 = 보드.밀리초();
        while (보드.밀리초() - 시작점 < 80) { int ibhayithi_iingcombolo = 보드.직렬읽기(); if (ibhayithi_iingcombolo >= 0) return ibhayithi_iingcombolo; 보드.misa_okwexeshana_i_CPU(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int 항목수 = 0, 끝자리 = -1;
        for (int iluphu_indeksa = 0; iluphu_indeksa < 12; iluphu_indeksa++) { int ibhayithi_iingcombolo = 탈출읽기(); if (ibhayithi_iingcombolo < 0) return; if (ibhayithi_iingcombolo >= '0' && ibhayithi_iingcombolo <= '9') 항목수 = 항목수 * 10 + ibhayithi_iingcombolo - '0'; else { 끝자리 = ibhayithi_iingcombolo; break; } }
        if (끝자리 == 'A') 기록이동(1);
        else if (끝자리 == 'B') 기록이동(-1);
        else if (끝자리 == 'C') { ikhesa_ixabiso = Emva_ixabiso(ikhesa_ixabiso); 다시(); }
        else if (끝자리 == 'D') { ikhesa_ixabiso = 앞(ikhesa_ixabiso); 다시(); }
        else if (끝자리 == 'H' || 끝자리 == '~' && (항목수 == 1 || 항목수 == 7)) { ikhesa_ixabiso = 0; 다시(); }
        else if (끝자리 == 'F' || 끝자리 == '~' && (항목수 == 4 || 항목수 == 8)) { ikhesa_ixabiso = Ubukhulu; 다시(); }
        else if (끝자리 == '~' && 항목수 == 3 && ikhesa_ixabiso < Ubukhulu) {
            int 다음자리 = Emva_ixabiso(ikhesa_ixabiso); for (int iluphu_indeksa = 다음자리; iluphu_indeksa < Ubukhulu; iluphu_indeksa++) 명령해석기.umgca[iluphu_indeksa - 다음자리 + ikhesa_ixabiso] = 명령해석기.umgca[iluphu_indeksa]; Ubukhulu -= 다음자리 - ikhesa_ixabiso; 다시();
        }
        else if (끝자리 == '~' && (항목수 == 5 || 항목수 == 6)) 보드.i_Terminal(항목수 == 5 ? 5 : 6);
        else if (끝자리 == '~' && 항목수 == 24 && umgca_wemiyalelo) { 명령해석기.i_Terminal(true); }
    }
    static int Funda() {
        if (!i_window_iseshoni.이어읽기) { Ubukhulu = ikhesa_ixabiso = Khangela_ixabiso = qala_i_window = 0; 가로보기 = false; }
        else { i_window_iseshoni.이어읽기 = false; 다시(); } boolean ukuphuphuma = false;
        while (true) {
            int ibhayithi_iingcombolo = 보드.직렬읽기(); if (ibhayithi_iingcombolo == -4096) return -3;
            if (보드.i_Terminal(14) != 0) 다시(); if (ibhayithi_iingcombolo < 0) { 보드.misa_okwexeshana_i_CPU(); continue; }
            if (ibhayithi_iingcombolo == 10 && 명령해석기.앞줄) { 명령해석기.앞줄 = false; continue; } 명령해석기.앞줄 = ibhayithi_iingcombolo == 13;
            if (ibhayithi_iingcombolo == 27) { 탈출(); continue; }
            if (ibhayithi_iingcombolo == 3) { 단말.Bhala("^C\n"); return -1; }
            if (ibhayithi_iingcombolo == 4 && Ubukhulu == 0 && umgca_wemiyalelo) { if (보드.i_Terminal(2) != 0) 명령해석기.i_Terminal(true); return -1; }
            if (ibhayithi_iingcombolo == 13 || ibhayithi_iingcombolo == 10) { 단말.문자(10); if (!ukuphuphuma) 기록넣기(); return ukuphuphuma ? -2 : Ubukhulu; }
            if (ibhayithi_iingcombolo == 9 && umgca_wemiyalelo) { 완성(); continue; }
            if (ibhayithi_iingcombolo == 1 || ibhayithi_iingcombolo == 5) { ikhesa_ixabiso = ibhayithi_iingcombolo == 1 ? 0 : Ubukhulu; 다시(); continue; }
            if (ibhayithi_iingcombolo == 8 || ibhayithi_iingcombolo == 127 || ibhayithi_iingcombolo == 21) {
                if (ibhayithi_iingcombolo == 21) { for (int iluphu_indeksa = ikhesa_ixabiso; iluphu_indeksa < Ubukhulu; iluphu_indeksa++) 명령해석기.umgca[iluphu_indeksa - ikhesa_ixabiso] = 명령해석기.umgca[iluphu_indeksa]; Ubukhulu -= ikhesa_ixabiso; ikhesa_ixabiso = 0; }
                else if (ikhesa_ixabiso > 0) { int 변경전 = 앞(ikhesa_ixabiso); for (int iluphu_indeksa = ikhesa_ixabiso; iluphu_indeksa < Ubukhulu; iluphu_indeksa++) 명령해석기.umgca[iluphu_indeksa - ikhesa_ixabiso + 변경전] = 명령해석기.umgca[iluphu_indeksa]; Ubukhulu -= ikhesa_ixabiso - 변경전; ikhesa_ixabiso = 변경전; }
                다시(); continue;
            }
            if (ibhayithi_iingcombolo == 11) { Ubukhulu = ikhesa_ixabiso; 다시(); continue; }
            if (ibhayithi_iingcombolo < 32 && ibhayithi_iingcombolo != 9) continue;
            if (Ubukhulu == 명령해석기.umgca.length) { ukuphuphuma = true; continue; }
            for (int iluphu_indeksa = Ubukhulu; iluphu_indeksa > ikhesa_ixabiso; iluphu_indeksa--) 명령해석기.umgca[iluphu_indeksa] = 명령해석기.umgca[iluphu_indeksa - 1];
            명령해석기.umgca[ikhesa_ixabiso++] = ibhayithi_iingcombolo; Ubukhulu++;
            if (ikhesa_ixabiso == Ubukhulu && !가로보기 && 폭(0, Ubukhulu) <= 보이는폭()) 보드.직렬쓰기(ibhayithi_iingcombolo);
            else if (ikhesa_ixabiso == Ubukhulu) 보이는줄(); else 다시();
        }
    }
}
