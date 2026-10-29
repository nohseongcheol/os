// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 paete_boleng 경계를 지키는 삽입/삭제, 방향키, Taelo pego_rei, Tab 완성. */
public final class mothaladi_Morulaganyi {
    static boolean mothalotlhako_wa_tirišo;
    static int[] pego_rei = new int[16 * 1024], pego_botelele = new int[16], lota_boleng = new int[4096], 후보 = new int[64];
    static int 기록수, pego_rei_fetša, Nyaka_boleng, 저장길이, Bogolo, kheusa_boleng, 후보수, 후보길이, Thomišo_lefastere;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd šireletšegile_šele ya_kgole_bontšha run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String go_tsenya_tshedimošo_Lenaneo, int 시작자리, int 끝자리, int 입력길이) {
        int 바이트수=0;
        for(int 자리=시작자리;자리<끝자리;자리++) {
            int khouto_ya_tlhaka=go_tsenya_tshedimošo_Lenaneo.charAt(자리);
            if(khouto_ya_tlhaka>=0xd800 && khouto_ya_tlhaka<=0xdbff && 자리+1<끝자리)khouto_ya_tlhaka=0x10000+((khouto_ya_tlhaka-0xd800)<<10)+go_tsenya_tshedimošo_Lenaneo.charAt(++자리)-0xdc00;
            int 수=khouto_ya_tlhaka<128?1:khouto_ya_tlhaka<2048?2:khouto_ya_tlhaka<65536?3:4;
            if(바이트수+수>62)return;
            for(int TATELANO_boleng=수-1;TATELANO_boleng>=0;TATELANO_boleng--)명령후보[바이트수++]=수==1?khouto_ya_tlhaka:TATELANO_boleng==수-1?(수==2?0xc0:수==3?0xe0:0xf0)|(khouto_ya_tlhaka>>(6*TATELANO_boleng)):0x80|((khouto_ya_tlhaka>>(6*TATELANO_boleng))&63);
        }
        if(바이트수<입력길이)return;
        for(int 자리=0;자리<입력길이;자리++)if(명령후보[자리]!=명령해석기.mothaladi[자리])return;
        후보수++;후보길이=바이트수+1;
        for(int 자리=0;자리<바이트수;자리++)후보[자리]=명령후보[자리];후보[바이트수]=' ';
    }
    static int 앞(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (명령해석기.mothaladi[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int Morago_boleng(int 읽는자리) { if (읽는자리 < Bogolo) { 읽는자리++; while (읽는자리 < Bogolo && (명령해석기.mothaladi[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int 시작자리, int boyo_boleng_lokela) {
        int 글칸수 = 0;
        for (int ditaelopoeletšwa_lokela = 시작자리; ditaelopoeletšwa_lokela < boyo_boleng_lokela; ditaelopoeletšwa_lokela++) { int paete_data = 명령해석기.mothaladi[ditaelopoeletšwa_lokela]; if ((paete_data & 192) == 128) continue; 글칸수 += paete_data >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void 다시() {
        단말.Ngwala("\r\u001b[2K");
        단말.Ngwala(mothalotlhako_wa_tirišo ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 mothaladi 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int 열수 = 보드.터미널(13) & 65535; return 열수 - (mothalotlhako_wa_tirišo ? 18 : 9); }
    static void 보이는줄() {
        if (kheusa_boleng < Thomišo_lefastere) Thomišo_lefastere = kheusa_boleng;
        while (폭(Thomišo_lefastere, kheusa_boleng) > 보이는폭()) Thomišo_lefastere = Morago_boleng(Thomišo_lefastere);
        int 끝자리 = Thomišo_lefastere;
        while (끝자리 < Bogolo && 폭(Thomišo_lefastere, Morago_boleng(끝자리)) <= 보이는폭()) 끝자리 = Morago_boleng(끝자리);
        단말.Ngwala("\r\u001b["); 단말.수(mothalotlhako_wa_tirišo ? 16 : 7); 단말.Ngwala("G\u001b[K");
        if (Thomišo_lefastere > 0) 단말.문자('<');
        for (int ditaelopoeletšwa_lokela = Thomišo_lefastere; ditaelopoeletšwa_lokela < 끝자리; ditaelopoeletšwa_lokela++) 보드.직렬쓰기(명령해석기.mothaladi[ditaelopoeletšwa_lokela]);
        단말.문자(끝자리 < Bogolo ? '>' : ' ');
        단말.Ngwala("\u001b["); 단말.수(폭(kheusa_boleng, 끝자리) + 1); 단말.문자('D');
        가로보기 = Thomišo_lefastere > 0 || 끝자리 < Bogolo || 폭(0, Bogolo) > 보이는폭();
    }
    static void 기록넣기() {
        if (!mothalotlhako_wa_tirišo || Bogolo == 0 || Bogolo > 1024) return;
        if (기록수 > 0) {
            int 마지막자리 = (pego_rei_fetša + 15) % 16; boolean 같은여부 = pego_botelele[마지막자리] == Bogolo;
            for (int ditaelopoeletšwa_lokela = 0; 같은여부 && ditaelopoeletšwa_lokela < Bogolo; ditaelopoeletšwa_lokela++) if (pego_rei[마지막자리 * 1024 + ditaelopoeletšwa_lokela] != 명령해석기.mothaladi[ditaelopoeletšwa_lokela]) 같은여부 = false;
            if (같은여부) return;
        }
        pego_botelele[pego_rei_fetša] = Bogolo; for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < Bogolo; ditaelopoeletšwa_lokela++) pego_rei[pego_rei_fetša * 1024 + ditaelopoeletšwa_lokela] = 명령해석기.mothaladi[ditaelopoeletšwa_lokela];
        pego_rei_fetša = (pego_rei_fetša + 1) % 16; if (기록수 < 16) 기록수++;
    }
    static void 기록이동(int 변화량) {
        if (!mothalotlhako_wa_tirišo) return;
        if (Nyaka_boleng == 0 && 변화량 > 0) { 저장길이 = Bogolo; for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < Bogolo; ditaelopoeletšwa_lokela++) lota_boleng[ditaelopoeletšwa_lokela] = 명령해석기.mothaladi[ditaelopoeletšwa_lokela]; }
        int 다음자리 = Nyaka_boleng + 변화량; if (다음자리 < 0 || 다음자리 > 기록수) return; Nyaka_boleng = 다음자리;
        if (Nyaka_boleng == 0) { Bogolo = 저장길이; for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < Bogolo; ditaelopoeletšwa_lokela++) 명령해석기.mothaladi[ditaelopoeletšwa_lokela] = lota_boleng[ditaelopoeletšwa_lokela]; }
        else { int 보관칸 = (pego_rei_fetša + 16 - Nyaka_boleng) % 16; Bogolo = pego_botelele[보관칸]; for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < Bogolo; ditaelopoeletšwa_lokela++) 명령해석기.mothaladi[ditaelopoeletšwa_lokela] = pego_rei[보관칸 * 1024 + ditaelopoeletšwa_lokela]; }
        kheusa_boleng = Bogolo; 다시();
    }
    static void bontšha_pego() {
        for (int 항목수 = 0; 항목수 < 기록수; 항목수++) {
            int 보관칸 = (pego_rei_fetša + 16 - 기록수 + 항목수) % 16; 단말.수(항목수 + 1); 단말.Ngwala("  ");
            for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < pego_botelele[보관칸]; ditaelopoeletšwa_lokela++) 보드.직렬쓰기(pego_rei[보관칸 * 1024 + ditaelopoeletšwa_lokela]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] data_arei, int 시작자리, int 항목수, int 접두말, int 총수, boolean 폴더번호) {
        if (항목수 < 총수 || 항목수 > 62) return;
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 총수; ditaelopoeletšwa_lokela++) if (data_arei[시작자리 + ditaelopoeletšwa_lokela] != 명령해석기.mothaladi[접두말 + ditaelopoeletšwa_lokela]) return;
        후보수++; 후보길이 = 항목수 + 1;
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 항목수; ditaelopoeletšwa_lokela++) 후보[ditaelopoeletšwa_lokela] = data_arei[시작자리 + ditaelopoeletšwa_lokela]; 후보[항목수] = 폴더번호 ? '/' : ' ';
    }
    static void 완성() {
        if (!mothalotlhako_wa_tirišo || kheusa_boleng != Bogolo) return;
        int 시작점 = Bogolo; while (시작점 > 0 && 명령해석기.mothaladi[시작점 - 1] != ' ') 시작점--;
        for (int ditaelopoeletšwa_lokela = 시작점; ditaelopoeletšwa_lokela < Bogolo; ditaelopoeletšwa_lokela++) if (명령해석기.mothaladi[ditaelopoeletšwa_lokela] == '/' || 명령해석기.mothaladi[ditaelopoeletšwa_lokela] == '"' || 명령해석기.mothaladi[ditaelopoeletšwa_lokela] == 39 || 명령해석기.mothaladi[ditaelopoeletšwa_lokela] == '\\') return;
        후보수 = 0; int 항목수 = Bogolo - 시작점;
        if (시작점 == 0) {
            for(int Lenaneo_lokela=0;Lenaneo_lokela<2;Lenaneo_lokela++) {
                String go_tsenya_tshedimošo_Lenaneo=Lenaneo_lokela==0?명령들:관리명령.완성어();
                int 읽는자리=0;
                while(읽는자리<go_tsenya_tshedimošo_Lenaneo.length()) {
                    int 끝자리=읽는자리;while(끝자리<go_tsenya_tshedimošo_Lenaneo.length() && go_tsenya_tshedimošo_Lenaneo.charAt(끝자리)!=' ')끝자리++;
                    명령후보넣기(go_tsenya_tshedimošo_Lenaneo,읽는자리,끝자리,항목수);읽는자리=끝자리+1;
                }
            }
        } else {
            memori_Difaele.tsela_Thomišo(1); memori_Difaele.tsela_paete(0, '.'); memori_Difaele.fokotša_kopišo_boleng();
            for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < memori_Difaele.파일수; ditaelopoeletšwa_lokela++) {
                int 시작자리 = memori_Difaele.go_tsenya_tshedimošo_Thomišo(memori_Difaele.Leina, ditaelopoeletšwa_lokela * 64, memori_Difaele.이름길이[ditaelopoeletšwa_lokela]);
                if (시작자리 >= 0) 후보넣기(memori_Difaele.Leina, ditaelopoeletšwa_lokela * 64 + 시작자리, memori_Difaele.이름길이[ditaelopoeletšwa_lokela] - 시작자리, 시작점, 항목수, false);
            }
            for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 16; ditaelopoeletšwa_lokela++) {
                int 시작자리 = memori_Difaele.go_tsenya_tshedimošo_Thomišo(memori_Difaele.lelokelelo_leina, ditaelopoeletšwa_lokela * 64, memori_Difaele.lelokelelo_botelele[ditaelopoeletšwa_lokela]);
                if (시작자리 >= 0) 후보넣기(memori_Difaele.lelokelelo_leina, ditaelopoeletšwa_lokela * 64 + 시작자리, memori_Difaele.lelokelelo_botelele[ditaelopoeletšwa_lokela] - 시작자리, 시작점, 항목수, true);
            }
        }
        if (후보수 != 1) { 보드.직렬쓰기(7); return; }
        for (int ditaelopoeletšwa_lokela = 항목수; ditaelopoeletšwa_lokela < 후보길이 && Bogolo < 명령해석기.mothaladi.length - 1; ditaelopoeletšwa_lokela++) {
            if (후보[ditaelopoeletšwa_lokela] == ' ' && ditaelopoeletšwa_lokela != 후보길이 - 1) 명령해석기.mothaladi[Bogolo++] = '\\';
            명령해석기.mothaladi[Bogolo++] = 후보[ditaelopoeletšwa_lokela];
        }
        kheusa_boleng = Bogolo; 다시();
    }
    static int 탈출읽기() {
        int 시작점 = 보드.밀리초();
        while (보드.밀리초() - 시작점 < 80) { int paete_data = 보드.직렬읽기(); if (paete_data >= 0) return paete_data; 보드.e_thibetšwe_CPU(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int 항목수 = 0, 끝자리 = -1;
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 12; ditaelopoeletšwa_lokela++) { int paete_data = 탈출읽기(); if (paete_data < 0) return; if (paete_data >= '0' && paete_data <= '9') 항목수 = 항목수 * 10 + paete_data - '0'; else { 끝자리 = paete_data; break; } }
        if (끝자리 == 'A') 기록이동(1);
        else if (끝자리 == 'B') 기록이동(-1);
        else if (끝자리 == 'C') { kheusa_boleng = Morago_boleng(kheusa_boleng); 다시(); }
        else if (끝자리 == 'D') { kheusa_boleng = 앞(kheusa_boleng); 다시(); }
        else if (끝자리 == 'H' || 끝자리 == '~' && (항목수 == 1 || 항목수 == 7)) { kheusa_boleng = 0; 다시(); }
        else if (끝자리 == 'F' || 끝자리 == '~' && (항목수 == 4 || 항목수 == 8)) { kheusa_boleng = Bogolo; 다시(); }
        else if (끝자리 == '~' && 항목수 == 3 && kheusa_boleng < Bogolo) {
            int 다음자리 = Morago_boleng(kheusa_boleng); for (int ditaelopoeletšwa_lokela = 다음자리; ditaelopoeletšwa_lokela < Bogolo; ditaelopoeletšwa_lokela++) 명령해석기.mothaladi[ditaelopoeletšwa_lokela - 다음자리 + kheusa_boleng] = 명령해석기.mothaladi[ditaelopoeletšwa_lokela]; Bogolo -= 다음자리 - kheusa_boleng; 다시();
        }
        else if (끝자리 == '~' && (항목수 == 5 || 항목수 == 6)) 보드.터미널(항목수 == 5 ? 5 : 6);
        else if (끝자리 == '~' && 항목수 == 24 && mothalotlhako_wa_tirišo) { 명령해석기.터미널(true); }
    }
    static int Bala() {
        if (!lefastere_nakotiragalo.이어읽기) { Bogolo = kheusa_boleng = Nyaka_boleng = Thomišo_lefastere = 0; 가로보기 = false; }
        else { lefastere_nakotiragalo.이어읽기 = false; 다시(); } boolean mongwaloutama = false;
        while (true) {
            int paete_data = 보드.직렬읽기(); if (paete_data == -4096) return -3;
            if (보드.터미널(14) != 0) 다시(); if (paete_data < 0) { 보드.e_thibetšwe_CPU(); continue; }
            if (paete_data == 10 && 명령해석기.앞줄) { 명령해석기.앞줄 = false; continue; } 명령해석기.앞줄 = paete_data == 13;
            if (paete_data == 27) { 탈출(); continue; }
            if (paete_data == 3) { 단말.Ngwala("^C\n"); return -1; }
            if (paete_data == 4 && Bogolo == 0 && mothalotlhako_wa_tirišo) { if (보드.터미널(2) != 0) 명령해석기.터미널(true); return -1; }
            if (paete_data == 13 || paete_data == 10) { 단말.문자(10); if (!mongwaloutama) 기록넣기(); return mongwaloutama ? -2 : Bogolo; }
            if (paete_data == 9 && mothalotlhako_wa_tirišo) { 완성(); continue; }
            if (paete_data == 1 || paete_data == 5) { kheusa_boleng = paete_data == 1 ? 0 : Bogolo; 다시(); continue; }
            if (paete_data == 8 || paete_data == 127 || paete_data == 21) {
                if (paete_data == 21) { for (int ditaelopoeletšwa_lokela = kheusa_boleng; ditaelopoeletšwa_lokela < Bogolo; ditaelopoeletšwa_lokela++) 명령해석기.mothaladi[ditaelopoeletšwa_lokela - kheusa_boleng] = 명령해석기.mothaladi[ditaelopoeletšwa_lokela]; Bogolo -= kheusa_boleng; kheusa_boleng = 0; }
                else if (kheusa_boleng > 0) { int 변경전 = 앞(kheusa_boleng); for (int ditaelopoeletšwa_lokela = kheusa_boleng; ditaelopoeletšwa_lokela < Bogolo; ditaelopoeletšwa_lokela++) 명령해석기.mothaladi[ditaelopoeletšwa_lokela - kheusa_boleng + 변경전] = 명령해석기.mothaladi[ditaelopoeletšwa_lokela]; Bogolo -= kheusa_boleng - 변경전; kheusa_boleng = 변경전; }
                다시(); continue;
            }
            if (paete_data == 11) { Bogolo = kheusa_boleng; 다시(); continue; }
            if (paete_data < 32 && paete_data != 9) continue;
            if (Bogolo == 명령해석기.mothaladi.length) { mongwaloutama = true; continue; }
            for (int ditaelopoeletšwa_lokela = Bogolo; ditaelopoeletšwa_lokela > kheusa_boleng; ditaelopoeletšwa_lokela--) 명령해석기.mothaladi[ditaelopoeletšwa_lokela] = 명령해석기.mothaladi[ditaelopoeletšwa_lokela - 1];
            명령해석기.mothaladi[kheusa_boleng++] = paete_data; Bogolo++;
            if (kheusa_boleng == Bogolo && !가로보기 && 폭(0, Bogolo) <= 보이는폭()) 보드.직렬쓰기(paete_data);
            else if (kheusa_boleng == Bogolo) 보이는줄(); else 다시();
        }
    }
}
