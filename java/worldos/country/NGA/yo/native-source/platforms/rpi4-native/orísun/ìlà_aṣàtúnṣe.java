// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 báìtì_iye 경계를 지키는 삽입/삭제, 방향키, Àṣẹ àkọsílẹ̀_ìṣe_ìlà_ìbú, Tab 완성. */
public final class ìlà_aṣàtúnṣe {
    static boolean ìlà_ìpàṣẹ;
    static int[] àkọsílẹ̀_ìṣe_ìlà_ìbú = new int[16 * 1024], àkọsílẹ̀_ìṣe_gígùn = new int[16], Store_iye = new int[4096], 후보 = new int[64];
    static int 기록수, àkọsílẹ̀_ìṣe_ìlà_ìbú_parí, wákiri_iye, 저장길이, Ìwọ̀n, kọ́sọ̀_iye, 후보수, 후보길이, bẹ̀rẹ̀_wínńdò;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd Tóláàbò_ṣẹ́ẹ̀lì Ìjìnnà_ṣàfihàn run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String ìgbéwọlé_Àtòkọ, int 시작자리, int 끝자리, int 입력길이) {
        int 바이트수=0;
        for(int 자리=시작자리;자리<끝자리;자리++) {
            int kóòdù_ẹyọ_ọ̀rọ̀=ìgbéwọlé_Àtòkọ.charAt(자리);
            if(kóòdù_ẹyọ_ọ̀rọ̀>=0xd800 && kóòdù_ẹyọ_ọ̀rọ̀<=0xdbff && 자리+1<끝자리)kóòdù_ẹyọ_ọ̀rọ̀=0x10000+((kóòdù_ẹyọ_ọ̀rọ̀-0xd800)<<10)+ìgbéwọlé_Àtòkọ.charAt(++자리)-0xdc00;
            int 수=kóòdù_ẹyọ_ọ̀rọ̀<128?1:kóòdù_ẹyọ_ọ̀rọ̀<2048?2:kóòdù_ẹyọ_ọ̀rọ̀<65536?3:4;
            if(바이트수+수>62)return;
            for(int ÀTẸ̀LÉRA_iye=수-1;ÀTẸ̀LÉRA_iye>=0;ÀTẸ̀LÉRA_iye--)명령후보[바이트수++]=수==1?kóòdù_ẹyọ_ọ̀rọ̀:ÀTẸ̀LÉRA_iye==수-1?(수==2?0xc0:수==3?0xe0:0xf0)|(kóòdù_ẹyọ_ọ̀rọ̀>>(6*ÀTẸ̀LÉRA_iye)):0x80|((kóòdù_ẹyọ_ọ̀rọ̀>>(6*ÀTẸ̀LÉRA_iye))&63);
        }
        if(바이트수<입력길이)return;
        for(int 자리=0;자리<입력길이;자리++)if(명령후보[자리]!=명령해석기.ìlà[자리])return;
        후보수++;후보길이=바이트수+1;
        for(int 자리=0;자리<바이트수;자리++)후보[자리]=명령후보[자리];후보[바이트수]=' ';
    }
    static int 앞(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (명령해석기.ìlà[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int Padà_sẹ́yìn_iye(int 읽는자리) { if (읽는자리 < Ìwọ̀n) { 읽는자리++; while (읽는자리 < Ìwọ̀n && (명령해석기.ìlà[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int 시작자리, int èbúté_iye_wá_atọ̀ka_àkóónú) {
        int 글칸수 = 0;
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 시작자리; ṣetúnṣe_wá_atọ̀ka_àkóónú < èbúté_iye_wá_atọ̀ka_àkóónú; ṣetúnṣe_wá_atọ̀ka_àkóónú++) { int báìtì_détà = 명령해석기.ìlà[ṣetúnṣe_wá_atọ̀ka_àkóónú]; if ((báìtì_détà & 192) == 128) continue; 글칸수 += báìtì_détà >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void 다시() {
        단말.Kọ("\r\u001b[2K");
        단말.Kọ(ìlà_ìpàṣẹ ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 ìlà 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int 열수 = 보드.터미널(13) & 65535; return 열수 - (ìlà_ìpàṣẹ ? 18 : 9); }
    static void 보이는줄() {
        if (kọ́sọ̀_iye < bẹ̀rẹ̀_wínńdò) bẹ̀rẹ̀_wínńdò = kọ́sọ̀_iye;
        while (폭(bẹ̀rẹ̀_wínńdò, kọ́sọ̀_iye) > 보이는폭()) bẹ̀rẹ̀_wínńdò = Padà_sẹ́yìn_iye(bẹ̀rẹ̀_wínńdò);
        int 끝자리 = bẹ̀rẹ̀_wínńdò;
        while (끝자리 < Ìwọ̀n && 폭(bẹ̀rẹ̀_wínńdò, Padà_sẹ́yìn_iye(끝자리)) <= 보이는폭()) 끝자리 = Padà_sẹ́yìn_iye(끝자리);
        단말.Kọ("\r\u001b["); 단말.수(ìlà_ìpàṣẹ ? 16 : 7); 단말.Kọ("G\u001b[K");
        if (bẹ̀rẹ̀_wínńdò > 0) 단말.문자('<');
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = bẹ̀rẹ̀_wínńdò; ṣetúnṣe_wá_atọ̀ka_àkóónú < 끝자리; ṣetúnṣe_wá_atọ̀ka_àkóónú++) 보드.직렬쓰기(명령해석기.ìlà[ṣetúnṣe_wá_atọ̀ka_àkóónú]);
        단말.문자(끝자리 < Ìwọ̀n ? '>' : ' ');
        단말.Kọ("\u001b["); 단말.수(폭(kọ́sọ̀_iye, 끝자리) + 1); 단말.문자('D');
        가로보기 = bẹ̀rẹ̀_wínńdò > 0 || 끝자리 < Ìwọ̀n || 폭(0, Ìwọ̀n) > 보이는폭();
    }
    static void 기록넣기() {
        if (!ìlà_ìpàṣẹ || Ìwọ̀n == 0 || Ìwọ̀n > 1024) return;
        if (기록수 > 0) {
            int 마지막자리 = (àkọsílẹ̀_ìṣe_ìlà_ìbú_parí + 15) % 16; boolean 같은여부 = àkọsílẹ̀_ìṣe_gígùn[마지막자리] == Ìwọ̀n;
            for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; 같은여부 && ṣetúnṣe_wá_atọ̀ka_àkóónú < Ìwọ̀n; ṣetúnṣe_wá_atọ̀ka_àkóónú++) if (àkọsílẹ̀_ìṣe_ìlà_ìbú[마지막자리 * 1024 + ṣetúnṣe_wá_atọ̀ka_àkóónú] != 명령해석기.ìlà[ṣetúnṣe_wá_atọ̀ka_àkóónú]) 같은여부 = false;
            if (같은여부) return;
        }
        àkọsílẹ̀_ìṣe_gígùn[àkọsílẹ̀_ìṣe_ìlà_ìbú_parí] = Ìwọ̀n; for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < Ìwọ̀n; ṣetúnṣe_wá_atọ̀ka_àkóónú++) àkọsílẹ̀_ìṣe_ìlà_ìbú[àkọsílẹ̀_ìṣe_ìlà_ìbú_parí * 1024 + ṣetúnṣe_wá_atọ̀ka_àkóónú] = 명령해석기.ìlà[ṣetúnṣe_wá_atọ̀ka_àkóónú];
        àkọsílẹ̀_ìṣe_ìlà_ìbú_parí = (àkọsílẹ̀_ìṣe_ìlà_ìbú_parí + 1) % 16; if (기록수 < 16) 기록수++;
    }
    static void 기록이동(int 변화량) {
        if (!ìlà_ìpàṣẹ) return;
        if (wákiri_iye == 0 && 변화량 > 0) { 저장길이 = Ìwọ̀n; for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < Ìwọ̀n; ṣetúnṣe_wá_atọ̀ka_àkóónú++) Store_iye[ṣetúnṣe_wá_atọ̀ka_àkóónú] = 명령해석기.ìlà[ṣetúnṣe_wá_atọ̀ka_àkóónú]; }
        int 다음자리 = wákiri_iye + 변화량; if (다음자리 < 0 || 다음자리 > 기록수) return; wákiri_iye = 다음자리;
        if (wákiri_iye == 0) { Ìwọ̀n = 저장길이; for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < Ìwọ̀n; ṣetúnṣe_wá_atọ̀ka_àkóónú++) 명령해석기.ìlà[ṣetúnṣe_wá_atọ̀ka_àkóónú] = Store_iye[ṣetúnṣe_wá_atọ̀ka_àkóónú]; }
        else { int 보관칸 = (àkọsílẹ̀_ìṣe_ìlà_ìbú_parí + 16 - wákiri_iye) % 16; Ìwọ̀n = àkọsílẹ̀_ìṣe_gígùn[보관칸]; for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < Ìwọ̀n; ṣetúnṣe_wá_atọ̀ka_àkóónú++) 명령해석기.ìlà[ṣetúnṣe_wá_atọ̀ka_àkóónú] = àkọsílẹ̀_ìṣe_ìlà_ìbú[보관칸 * 1024 + ṣetúnṣe_wá_atọ̀ka_àkóónú]; }
        kọ́sọ̀_iye = Ìwọ̀n; 다시();
    }
    static void ṣàfihàn_àkọsílẹ̀_ìṣe() {
        for (int 항목수 = 0; 항목수 < 기록수; 항목수++) {
            int 보관칸 = (àkọsílẹ̀_ìṣe_ìlà_ìbú_parí + 16 - 기록수 + 항목수) % 16; 단말.수(항목수 + 1); 단말.Kọ("  ");
            for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < àkọsílẹ̀_ìṣe_gígùn[보관칸]; ṣetúnṣe_wá_atọ̀ka_àkóónú++) 보드.직렬쓰기(àkọsílẹ̀_ìṣe_ìlà_ìbú[보관칸 * 1024 + ṣetúnṣe_wá_atọ̀ka_àkóónú]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] détà_ÀRÉÈ, int 시작자리, int 항목수, int 접두말, int 총수, boolean 폴더번호) {
        if (항목수 < 총수 || 항목수 > 62) return;
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 총수; ṣetúnṣe_wá_atọ̀ka_àkóónú++) if (détà_ÀRÉÈ[시작자리 + ṣetúnṣe_wá_atọ̀ka_àkóónú] != 명령해석기.ìlà[접두말 + ṣetúnṣe_wá_atọ̀ka_àkóónú]) return;
        후보수++; 후보길이 = 항목수 + 1;
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 항목수; ṣetúnṣe_wá_atọ̀ka_àkóónú++) 후보[ṣetúnṣe_wá_atọ̀ka_àkóónú] = détà_ÀRÉÈ[시작자리 + ṣetúnṣe_wá_atọ̀ka_àkóónú]; 후보[항목수] = 폴더번호 ? '/' : ' ';
    }
    static void 완성() {
        if (!ìlà_ìpàṣẹ || kọ́sọ̀_iye != Ìwọ̀n) return;
        int 시작점 = Ìwọ̀n; while (시작점 > 0 && 명령해석기.ìlà[시작점 - 1] != ' ') 시작점--;
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 시작점; ṣetúnṣe_wá_atọ̀ka_àkóónú < Ìwọ̀n; ṣetúnṣe_wá_atọ̀ka_àkóónú++) if (명령해석기.ìlà[ṣetúnṣe_wá_atọ̀ka_àkóónú] == '/' || 명령해석기.ìlà[ṣetúnṣe_wá_atọ̀ka_àkóónú] == '"' || 명령해석기.ìlà[ṣetúnṣe_wá_atọ̀ka_àkóónú] == 39 || 명령해석기.ìlà[ṣetúnṣe_wá_atọ̀ka_àkóónú] == '\\') return;
        후보수 = 0; int 항목수 = Ìwọ̀n - 시작점;
        if (시작점 == 0) {
            for(int Àtòkọ_wá_atọ̀ka_àkóónú=0;Àtòkọ_wá_atọ̀ka_àkóónú<2;Àtòkọ_wá_atọ̀ka_àkóónú++) {
                String ìgbéwọlé_Àtòkọ=Àtòkọ_wá_atọ̀ka_àkóónú==0?명령들:관리명령.완성어();
                int 읽는자리=0;
                while(읽는자리<ìgbéwọlé_Àtòkọ.length()) {
                    int 끝자리=읽는자리;while(끝자리<ìgbéwọlé_Àtòkọ.length() && ìgbéwọlé_Àtòkọ.charAt(끝자리)!=' ')끝자리++;
                    명령후보넣기(ìgbéwọlé_Àtòkọ,읽는자리,끝자리,항목수);읽는자리=끝자리+1;
                }
            }
        } else {
            ibi_ìpamọ́_Àwọn_fáìlì.ọ̀nà_bẹ̀rẹ̀(1); ibi_ìpamọ́_Àwọn_fáìlì.ọ̀nà_báìtì(0, '.'); ibi_ìpamọ́_Àwọn_fáìlì.ṣe_níwọ̀n_iye();
            for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < ibi_ìpamọ́_Àwọn_fáìlì.파일수; ṣetúnṣe_wá_atọ̀ka_àkóónú++) {
                int 시작자리 = ibi_ìpamọ́_Àwọn_fáìlì.ìgbéwọlé_bẹ̀rẹ̀(ibi_ìpamọ́_Àwọn_fáìlì.Orúkọ, ṣetúnṣe_wá_atọ̀ka_àkóónú * 64, ibi_ìpamọ́_Àwọn_fáìlì.이름길이[ṣetúnṣe_wá_atọ̀ka_àkóónú]);
                if (시작자리 >= 0) 후보넣기(ibi_ìpamọ́_Àwọn_fáìlì.Orúkọ, ṣetúnṣe_wá_atọ̀ka_àkóónú * 64 + 시작자리, ibi_ìpamọ́_Àwọn_fáìlì.이름길이[ṣetúnṣe_wá_atọ̀ka_àkóónú] - 시작자리, 시작점, 항목수, false);
            }
            for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 16; ṣetúnṣe_wá_atọ̀ka_àkóónú++) {
                int 시작자리 = ibi_ìpamọ́_Àwọn_fáìlì.ìgbéwọlé_bẹ̀rẹ̀(ibi_ìpamọ́_Àwọn_fáìlì.àkójọpọ̀_fáìlì_orúkọ, ṣetúnṣe_wá_atọ̀ka_àkóónú * 64, ibi_ìpamọ́_Àwọn_fáìlì.àkójọpọ̀_fáìlì_gígùn[ṣetúnṣe_wá_atọ̀ka_àkóónú]);
                if (시작자리 >= 0) 후보넣기(ibi_ìpamọ́_Àwọn_fáìlì.àkójọpọ̀_fáìlì_orúkọ, ṣetúnṣe_wá_atọ̀ka_àkóónú * 64 + 시작자리, ibi_ìpamọ́_Àwọn_fáìlì.àkójọpọ̀_fáìlì_gígùn[ṣetúnṣe_wá_atọ̀ka_àkóónú] - 시작자리, 시작점, 항목수, true);
            }
        }
        if (후보수 != 1) { 보드.직렬쓰기(7); return; }
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 항목수; ṣetúnṣe_wá_atọ̀ka_àkóónú < 후보길이 && Ìwọ̀n < 명령해석기.ìlà.length - 1; ṣetúnṣe_wá_atọ̀ka_àkóónú++) {
            if (후보[ṣetúnṣe_wá_atọ̀ka_àkóónú] == ' ' && ṣetúnṣe_wá_atọ̀ka_àkóónú != 후보길이 - 1) 명령해석기.ìlà[Ìwọ̀n++] = '\\';
            명령해석기.ìlà[Ìwọ̀n++] = 후보[ṣetúnṣe_wá_atọ̀ka_àkóónú];
        }
        kọ́sọ̀_iye = Ìwọ̀n; 다시();
    }
    static int 탈출읽기() {
        int 시작점 = 보드.밀리초();
        while (보드.밀리초() - 시작점 < 80) { int báìtì_détà = 보드.직렬읽기(); if (báìtì_détà >= 0) return báìtì_détà; 보드.ti_dádúró_díẹ̀_CPU(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int 항목수 = 0, 끝자리 = -1;
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 12; ṣetúnṣe_wá_atọ̀ka_àkóónú++) { int báìtì_détà = 탈출읽기(); if (báìtì_détà < 0) return; if (báìtì_détà >= '0' && báìtì_détà <= '9') 항목수 = 항목수 * 10 + báìtì_détà - '0'; else { 끝자리 = báìtì_détà; break; } }
        if (끝자리 == 'A') 기록이동(1);
        else if (끝자리 == 'B') 기록이동(-1);
        else if (끝자리 == 'C') { kọ́sọ̀_iye = Padà_sẹ́yìn_iye(kọ́sọ̀_iye); 다시(); }
        else if (끝자리 == 'D') { kọ́sọ̀_iye = 앞(kọ́sọ̀_iye); 다시(); }
        else if (끝자리 == 'H' || 끝자리 == '~' && (항목수 == 1 || 항목수 == 7)) { kọ́sọ̀_iye = 0; 다시(); }
        else if (끝자리 == 'F' || 끝자리 == '~' && (항목수 == 4 || 항목수 == 8)) { kọ́sọ̀_iye = Ìwọ̀n; 다시(); }
        else if (끝자리 == '~' && 항목수 == 3 && kọ́sọ̀_iye < Ìwọ̀n) {
            int 다음자리 = Padà_sẹ́yìn_iye(kọ́sọ̀_iye); for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 다음자리; ṣetúnṣe_wá_atọ̀ka_àkóónú < Ìwọ̀n; ṣetúnṣe_wá_atọ̀ka_àkóónú++) 명령해석기.ìlà[ṣetúnṣe_wá_atọ̀ka_àkóónú - 다음자리 + kọ́sọ̀_iye] = 명령해석기.ìlà[ṣetúnṣe_wá_atọ̀ka_àkóónú]; Ìwọ̀n -= 다음자리 - kọ́sọ̀_iye; 다시();
        }
        else if (끝자리 == '~' && (항목수 == 5 || 항목수 == 6)) 보드.터미널(항목수 == 5 ? 5 : 6);
        else if (끝자리 == '~' && 항목수 == 24 && ìlà_ìpàṣẹ) { 명령해석기.터미널(true); }
    }
    static int Kàá() {
        if (!wínńdò_sáà.이어읽기) { Ìwọ̀n = kọ́sọ̀_iye = wákiri_iye = bẹ̀rẹ̀_wínńdò = 0; 가로보기 = false; }
        else { wínńdò_sáà.이어읽기 = false; 다시(); } boolean rékọjá = false;
        while (true) {
            int báìtì_détà = 보드.직렬읽기(); if (báìtì_détà == -4096) return -3;
            if (보드.터미널(14) != 0) 다시(); if (báìtì_détà < 0) { 보드.ti_dádúró_díẹ̀_CPU(); continue; }
            if (báìtì_détà == 10 && 명령해석기.앞줄) { 명령해석기.앞줄 = false; continue; } 명령해석기.앞줄 = báìtì_détà == 13;
            if (báìtì_détà == 27) { 탈출(); continue; }
            if (báìtì_détà == 3) { 단말.Kọ("^C\n"); return -1; }
            if (báìtì_détà == 4 && Ìwọ̀n == 0 && ìlà_ìpàṣẹ) { if (보드.터미널(2) != 0) 명령해석기.터미널(true); return -1; }
            if (báìtì_détà == 13 || báìtì_détà == 10) { 단말.문자(10); if (!rékọjá) 기록넣기(); return rékọjá ? -2 : Ìwọ̀n; }
            if (báìtì_détà == 9 && ìlà_ìpàṣẹ) { 완성(); continue; }
            if (báìtì_détà == 1 || báìtì_détà == 5) { kọ́sọ̀_iye = báìtì_détà == 1 ? 0 : Ìwọ̀n; 다시(); continue; }
            if (báìtì_détà == 8 || báìtì_détà == 127 || báìtì_détà == 21) {
                if (báìtì_détà == 21) { for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = kọ́sọ̀_iye; ṣetúnṣe_wá_atọ̀ka_àkóónú < Ìwọ̀n; ṣetúnṣe_wá_atọ̀ka_àkóónú++) 명령해석기.ìlà[ṣetúnṣe_wá_atọ̀ka_àkóónú - kọ́sọ̀_iye] = 명령해석기.ìlà[ṣetúnṣe_wá_atọ̀ka_àkóónú]; Ìwọ̀n -= kọ́sọ̀_iye; kọ́sọ̀_iye = 0; }
                else if (kọ́sọ̀_iye > 0) { int 변경전 = 앞(kọ́sọ̀_iye); for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = kọ́sọ̀_iye; ṣetúnṣe_wá_atọ̀ka_àkóónú < Ìwọ̀n; ṣetúnṣe_wá_atọ̀ka_àkóónú++) 명령해석기.ìlà[ṣetúnṣe_wá_atọ̀ka_àkóónú - kọ́sọ̀_iye + 변경전] = 명령해석기.ìlà[ṣetúnṣe_wá_atọ̀ka_àkóónú]; Ìwọ̀n -= kọ́sọ̀_iye - 변경전; kọ́sọ̀_iye = 변경전; }
                다시(); continue;
            }
            if (báìtì_détà == 11) { Ìwọ̀n = kọ́sọ̀_iye; 다시(); continue; }
            if (báìtì_détà < 32 && báìtì_détà != 9) continue;
            if (Ìwọ̀n == 명령해석기.ìlà.length) { rékọjá = true; continue; }
            for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = Ìwọ̀n; ṣetúnṣe_wá_atọ̀ka_àkóónú > kọ́sọ̀_iye; ṣetúnṣe_wá_atọ̀ka_àkóónú--) 명령해석기.ìlà[ṣetúnṣe_wá_atọ̀ka_àkóónú] = 명령해석기.ìlà[ṣetúnṣe_wá_atọ̀ka_àkóónú - 1];
            명령해석기.ìlà[kọ́sọ̀_iye++] = báìtì_détà; Ìwọ̀n++;
            if (kọ́sọ̀_iye == Ìwọ̀n && !가로보기 && 폭(0, Ìwọ̀n) <= 보이는폭()) 보드.직렬쓰기(báìtì_détà);
            else if (kọ́sọ̀_iye == Ìwọ̀n) 보이는줄(); else 다시();
        }
    }
}
