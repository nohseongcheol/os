// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 bayit_Daraja 경계를 지키는 삽입/삭제, 방향키, Umarni logu_naɗa, Tab 완성. */
public final class Layi_Edita {
    static boolean Layin_umurni;
    static int[] logu_naɗa = new int[16 * 1024], logu_Tsawo = new int[16], Ajiye_Daraja = new int[4096], 후보 = new int[64];
    static int 기록수, logu_naɗa_Ƙarshe, Leko_Daraja, 저장길이, Girma, Ɗan_jagora_Daraja, 후보수, 후보길이, Fara_taga;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd kararre_Mai_fayyace_umani na_nesa_Nuna run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String Mashigar_bayanai_Jeri, int 시작자리, int 끝자리, int 입력길이) {
        int 바이트수=0;
        for(int 자리=시작자리;자리<끝자리;자리++) {
            int Lambar_sirrin_harafi=Mashigar_bayanai_Jeri.charAt(자리);
            if(Lambar_sirrin_harafi>=0xd800 && Lambar_sirrin_harafi<=0xdbff && 자리+1<끝자리)Lambar_sirrin_harafi=0x10000+((Lambar_sirrin_harafi-0xd800)<<10)+Mashigar_bayanai_Jeri.charAt(++자리)-0xdc00;
            int 수=Lambar_sirrin_harafi<128?1:Lambar_sirrin_harafi<2048?2:Lambar_sirrin_harafi<65536?3:4;
            if(바이트수+수>62)return;
            for(int JERI_Daraja=수-1;JERI_Daraja>=0;JERI_Daraja--)명령후보[바이트수++]=수==1?Lambar_sirrin_harafi:JERI_Daraja==수-1?(수==2?0xc0:수==3?0xe0:0xf0)|(Lambar_sirrin_harafi>>(6*JERI_Daraja)):0x80|((Lambar_sirrin_harafi>>(6*JERI_Daraja))&63);
        }
        if(바이트수<입력길이)return;
        for(int 자리=0;자리<입력길이;자리++)if(명령후보[자리]!=명령해석기.Layi[자리])return;
        후보수++;후보길이=바이트수+1;
        for(int 자리=0;자리<바이트수;자리++)후보[자리]=명령후보[자리];후보[바이트수]=' ';
    }
    static int kyamarar_gaba_Daraja(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (명령해석기.Layi[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int Baya_Daraja(int 읽는자리) { if (읽는자리 < Girma) { 읽는자리++; while (읽는자리 < Girma && (명령해석기.Layi[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int 시작자리, int Zangon_ƙarshe_Daraja_Indes) {
        int 글칸수 = 0;
        for (int Warware_Indes = 시작자리; Warware_Indes < Zangon_ƙarshe_Daraja_Indes; Warware_Indes++) { int bayit_Tarin_bayani = 명령해석기.Layi[Warware_Indes]; if ((bayit_Tarin_bayani & 192) == 128) continue; 글칸수 += bayit_Tarin_bayani >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void 다시() {
        단말.Yi_Rubutu("\r\u001b[2K");
        단말.Yi_Rubutu(Layin_umurni ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 Layi 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int 열수 = 보드.터미널(13) & 65535; return 열수 - (Layin_umurni ? 18 : 9); }
    static void 보이는줄() {
        if (Ɗan_jagora_Daraja < Fara_taga) Fara_taga = Ɗan_jagora_Daraja;
        while (폭(Fara_taga, Ɗan_jagora_Daraja) > 보이는폭()) Fara_taga = Baya_Daraja(Fara_taga);
        int 끝자리 = Fara_taga;
        while (끝자리 < Girma && 폭(Fara_taga, Baya_Daraja(끝자리)) <= 보이는폭()) 끝자리 = Baya_Daraja(끝자리);
        단말.Yi_Rubutu("\r\u001b["); 단말.수(Layin_umurni ? 16 : 7); 단말.Yi_Rubutu("G\u001b[K");
        if (Fara_taga > 0) 단말.문자('<');
        for (int Warware_Indes = Fara_taga; Warware_Indes < 끝자리; Warware_Indes++) 보드.직렬쓰기(명령해석기.Layi[Warware_Indes]);
        단말.문자(끝자리 < Girma ? '>' : ' ');
        단말.Yi_Rubutu("\u001b["); 단말.수(폭(Ɗan_jagora_Daraja, 끝자리) + 1); 단말.문자('D');
        가로보기 = Fara_taga > 0 || 끝자리 < Girma || 폭(0, Girma) > 보이는폭();
    }
    static void 기록넣기() {
        if (!Layin_umurni || Girma == 0 || Girma > 1024) return;
        if (기록수 > 0) {
            int 마지막자리 = (logu_naɗa_Ƙarshe + 15) % 16; boolean 같은여부 = logu_Tsawo[마지막자리] == Girma;
            for (int Warware_Indes = 0; 같은여부 && Warware_Indes < Girma; Warware_Indes++) if (logu_naɗa[마지막자리 * 1024 + Warware_Indes] != 명령해석기.Layi[Warware_Indes]) 같은여부 = false;
            if (같은여부) return;
        }
        logu_Tsawo[logu_naɗa_Ƙarshe] = Girma; for (int Warware_Indes = 0; Warware_Indes < Girma; Warware_Indes++) logu_naɗa[logu_naɗa_Ƙarshe * 1024 + Warware_Indes] = 명령해석기.Layi[Warware_Indes];
        logu_naɗa_Ƙarshe = (logu_naɗa_Ƙarshe + 1) % 16; if (기록수 < 16) 기록수++;
    }
    static void 기록이동(int 변화량) {
        if (!Layin_umurni) return;
        if (Leko_Daraja == 0 && 변화량 > 0) { 저장길이 = Girma; for (int Warware_Indes = 0; Warware_Indes < Girma; Warware_Indes++) Ajiye_Daraja[Warware_Indes] = 명령해석기.Layi[Warware_Indes]; }
        int 다음자리 = Leko_Daraja + 변화량; if (다음자리 < 0 || 다음자리 > 기록수) return; Leko_Daraja = 다음자리;
        if (Leko_Daraja == 0) { Girma = 저장길이; for (int Warware_Indes = 0; Warware_Indes < Girma; Warware_Indes++) 명령해석기.Layi[Warware_Indes] = Ajiye_Daraja[Warware_Indes]; }
        else { int 보관칸 = (logu_naɗa_Ƙarshe + 16 - Leko_Daraja) % 16; Girma = logu_Tsawo[보관칸]; for (int Warware_Indes = 0; Warware_Indes < Girma; Warware_Indes++) 명령해석기.Layi[Warware_Indes] = logu_naɗa[보관칸 * 1024 + Warware_Indes]; }
        Ɗan_jagora_Daraja = Girma; 다시();
    }
    static void Nuna_logu() {
        for (int 항목수 = 0; 항목수 < 기록수; 항목수++) {
            int 보관칸 = (logu_naɗa_Ƙarshe + 16 - 기록수 + 항목수) % 16; 단말.수(항목수 + 1); 단말.Yi_Rubutu("  ");
            for (int Warware_Indes = 0; Warware_Indes < logu_Tsawo[보관칸]; Warware_Indes++) 보드.직렬쓰기(logu_naɗa[보관칸 * 1024 + Warware_Indes]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] Tarin_bayani_TSARI, int 시작자리, int 항목수, int 접두말, int 총수, boolean 폴더번호) {
        if (항목수 < 총수 || 항목수 > 62) return;
        for (int Warware_Indes = 0; Warware_Indes < 총수; Warware_Indes++) if (Tarin_bayani_TSARI[시작자리 + Warware_Indes] != 명령해석기.Layi[접두말 + Warware_Indes]) return;
        후보수++; 후보길이 = 항목수 + 1;
        for (int Warware_Indes = 0; Warware_Indes < 항목수; Warware_Indes++) 후보[Warware_Indes] = Tarin_bayani_TSARI[시작자리 + Warware_Indes]; 후보[항목수] = 폴더번호 ? '/' : ' ';
    }
    static void 완성() {
        if (!Layin_umurni || Ɗan_jagora_Daraja != Girma) return;
        int 시작점 = Girma; while (시작점 > 0 && 명령해석기.Layi[시작점 - 1] != ' ') 시작점--;
        for (int Warware_Indes = 시작점; Warware_Indes < Girma; Warware_Indes++) if (명령해석기.Layi[Warware_Indes] == '/' || 명령해석기.Layi[Warware_Indes] == '"' || 명령해석기.Layi[Warware_Indes] == 39 || 명령해석기.Layi[Warware_Indes] == '\\') return;
        후보수 = 0; int 항목수 = Girma - 시작점;
        if (시작점 == 0) {
            for(int Jeri_Indes=0;Jeri_Indes<2;Jeri_Indes++) {
                String Mashigar_bayanai_Jeri=Jeri_Indes==0?명령들:관리명령.완성어();
                int 읽는자리=0;
                while(읽는자리<Mashigar_bayanai_Jeri.length()) {
                    int 끝자리=읽는자리;while(끝자리<Mashigar_bayanai_Jeri.length() && Mashigar_bayanai_Jeri.charAt(끝자리)!=' ')끝자리++;
                    명령후보넣기(Mashigar_bayanai_Jeri,읽는자리,끝자리,항목수);읽는자리=끝자리+1;
                }
            }
        } else {
            Mahardatar_kwamfuta_Fayiloli.Hanyar_shiga_Fara(1); Mahardatar_kwamfuta_Fayiloli.Hanyar_shiga_bayit(0, '.'); Mahardatar_kwamfuta_Fayiloli.Gajarta_kimar_bayanai_Daraja();
            for (int Warware_Indes = 0; Warware_Indes < Mahardatar_kwamfuta_Fayiloli.파일수; Warware_Indes++) {
                int 시작자리 = Mahardatar_kwamfuta_Fayiloli.Mashigar_bayanai_Fara(Mahardatar_kwamfuta_Fayiloli.Suna, Warware_Indes * 64, Mahardatar_kwamfuta_Fayiloli.이름길이[Warware_Indes]);
                if (시작자리 >= 0) 후보넣기(Mahardatar_kwamfuta_Fayiloli.Suna, Warware_Indes * 64 + 시작자리, Mahardatar_kwamfuta_Fayiloli.이름길이[Warware_Indes] - 시작자리, 시작점, 항목수, false);
            }
            for (int Warware_Indes = 0; Warware_Indes < 16; Warware_Indes++) {
                int 시작자리 = Mahardatar_kwamfuta_Fayiloli.Mashigar_bayanai_Fara(Mahardatar_kwamfuta_Fayiloli.ma_ajiya_Suna, Warware_Indes * 64, Mahardatar_kwamfuta_Fayiloli.ma_ajiya_Tsawo[Warware_Indes]);
                if (시작자리 >= 0) 후보넣기(Mahardatar_kwamfuta_Fayiloli.ma_ajiya_Suna, Warware_Indes * 64 + 시작자리, Mahardatar_kwamfuta_Fayiloli.ma_ajiya_Tsawo[Warware_Indes] - 시작자리, 시작점, 항목수, true);
            }
        }
        if (후보수 != 1) { 보드.직렬쓰기(7); return; }
        for (int Warware_Indes = 항목수; Warware_Indes < 후보길이 && Girma < 명령해석기.Layi.length - 1; Warware_Indes++) {
            if (후보[Warware_Indes] == ' ' && Warware_Indes != 후보길이 - 1) 명령해석기.Layi[Girma++] = '\\';
            명령해석기.Layi[Girma++] = 후보[Warware_Indes];
        }
        Ɗan_jagora_Daraja = Girma; 다시();
    }
    static int 탈출읽기() {
        int 시작점 = 보드.밀리초();
        while (보드.밀리초() - 시작점 < 80) { int bayit_Tarin_bayani = 보드.직렬읽기(); if (bayit_Tarin_bayani >= 0) return bayit_Tarin_bayani; 보드.ɗan_tsai_da_CPU(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int 항목수 = 0, 끝자리 = -1;
        for (int Warware_Indes = 0; Warware_Indes < 12; Warware_Indes++) { int bayit_Tarin_bayani = 탈출읽기(); if (bayit_Tarin_bayani < 0) return; if (bayit_Tarin_bayani >= '0' && bayit_Tarin_bayani <= '9') 항목수 = 항목수 * 10 + bayit_Tarin_bayani - '0'; else { 끝자리 = bayit_Tarin_bayani; break; } }
        if (끝자리 == 'A') 기록이동(1);
        else if (끝자리 == 'B') 기록이동(-1);
        else if (끝자리 == 'C') { Ɗan_jagora_Daraja = Baya_Daraja(Ɗan_jagora_Daraja); 다시(); }
        else if (끝자리 == 'D') { Ɗan_jagora_Daraja = kyamarar_gaba_Daraja(Ɗan_jagora_Daraja); 다시(); }
        else if (끝자리 == 'H' || 끝자리 == '~' && (항목수 == 1 || 항목수 == 7)) { Ɗan_jagora_Daraja = 0; 다시(); }
        else if (끝자리 == 'F' || 끝자리 == '~' && (항목수 == 4 || 항목수 == 8)) { Ɗan_jagora_Daraja = Girma; 다시(); }
        else if (끝자리 == '~' && 항목수 == 3 && Ɗan_jagora_Daraja < Girma) {
            int 다음자리 = Baya_Daraja(Ɗan_jagora_Daraja); for (int Warware_Indes = 다음자리; Warware_Indes < Girma; Warware_Indes++) 명령해석기.Layi[Warware_Indes - 다음자리 + Ɗan_jagora_Daraja] = 명령해석기.Layi[Warware_Indes]; Girma -= 다음자리 - Ɗan_jagora_Daraja; 다시();
        }
        else if (끝자리 == '~' && (항목수 == 5 || 항목수 == 6)) 보드.터미널(항목수 == 5 ? 5 : 6);
        else if (끝자리 == '~' && 항목수 == 24 && Layin_umurni) { 명령해석기.터미널(true); }
    }
    static int Yi_Karatu() {
        if (!taga_Mahadin_canjin_bayanai.이어읽기) { Girma = Ɗan_jagora_Daraja = Leko_Daraja = Fara_taga = 0; 가로보기 = false; }
        else { taga_Mahadin_canjin_bayanai.이어읽기 = false; 다시(); } boolean Mamayar_bayanai = false;
        while (true) {
            int bayit_Tarin_bayani = 보드.직렬읽기(); if (bayit_Tarin_bayani == -4096) return -3;
            if (보드.터미널(14) != 0) 다시(); if (bayit_Tarin_bayani < 0) { 보드.ɗan_tsai_da_CPU(); continue; }
            if (bayit_Tarin_bayani == 10 && 명령해석기.앞줄) { 명령해석기.앞줄 = false; continue; } 명령해석기.앞줄 = bayit_Tarin_bayani == 13;
            if (bayit_Tarin_bayani == 27) { 탈출(); continue; }
            if (bayit_Tarin_bayani == 3) { 단말.Yi_Rubutu("^C\n"); return -1; }
            if (bayit_Tarin_bayani == 4 && Girma == 0 && Layin_umurni) { if (보드.터미널(2) != 0) 명령해석기.터미널(true); return -1; }
            if (bayit_Tarin_bayani == 13 || bayit_Tarin_bayani == 10) { 단말.문자(10); if (!Mamayar_bayanai) 기록넣기(); return Mamayar_bayanai ? -2 : Girma; }
            if (bayit_Tarin_bayani == 9 && Layin_umurni) { 완성(); continue; }
            if (bayit_Tarin_bayani == 1 || bayit_Tarin_bayani == 5) { Ɗan_jagora_Daraja = bayit_Tarin_bayani == 1 ? 0 : Girma; 다시(); continue; }
            if (bayit_Tarin_bayani == 8 || bayit_Tarin_bayani == 127 || bayit_Tarin_bayani == 21) {
                if (bayit_Tarin_bayani == 21) { for (int Warware_Indes = Ɗan_jagora_Daraja; Warware_Indes < Girma; Warware_Indes++) 명령해석기.Layi[Warware_Indes - Ɗan_jagora_Daraja] = 명령해석기.Layi[Warware_Indes]; Girma -= Ɗan_jagora_Daraja; Ɗan_jagora_Daraja = 0; }
                else if (Ɗan_jagora_Daraja > 0) { int 변경전 = kyamarar_gaba_Daraja(Ɗan_jagora_Daraja); for (int Warware_Indes = Ɗan_jagora_Daraja; Warware_Indes < Girma; Warware_Indes++) 명령해석기.Layi[Warware_Indes - Ɗan_jagora_Daraja + 변경전] = 명령해석기.Layi[Warware_Indes]; Girma -= Ɗan_jagora_Daraja - 변경전; Ɗan_jagora_Daraja = 변경전; }
                다시(); continue;
            }
            if (bayit_Tarin_bayani == 11) { Girma = Ɗan_jagora_Daraja; 다시(); continue; }
            if (bayit_Tarin_bayani < 32 && bayit_Tarin_bayani != 9) continue;
            if (Girma == 명령해석기.Layi.length) { Mamayar_bayanai = true; continue; }
            for (int Warware_Indes = Girma; Warware_Indes > Ɗan_jagora_Daraja; Warware_Indes--) 명령해석기.Layi[Warware_Indes] = 명령해석기.Layi[Warware_Indes - 1];
            명령해석기.Layi[Ɗan_jagora_Daraja++] = bayit_Tarin_bayani; Girma++;
            if (Ɗan_jagora_Daraja == Girma && !가로보기 && 폭(0, Girma) <= 보이는폭()) 보드.직렬쓰기(bayit_Tarin_bayani);
            else if (Ɗan_jagora_Daraja == Girma) 보이는줄(); else 다시();
        }
    }
}
