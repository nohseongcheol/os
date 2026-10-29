// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 ìlà_ìpàṣẹ. 따옴표, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] ìlà = new int[4096], kóòdù_káàdì_àsansílẹ̀_iye = new int[4096], 시작점 = new int[32], gígùn_iye = new int[32];
    static int[] 편집내용 = new int[16384], ṣàtúnṣe_orúkọ = new int[63];
    static int 토큰수, ṣàtúnṣe_orúkọ_gígùn, 결과;
    static boolean 앞줄;
    static void 원바이트(int iye) { 보드.직렬쓰기(iye); }
    static int 줄읽기() { return ìlà_aṣàtúnṣe.Kàá(); }
    static boolean 나누기(int Ìwọ̀n) {
        int 위치 = 0, 끝 = 0; 토큰수 = 0;
        while (위치 < Ìwọ̀n) {
            while (위치 < Ìwọ̀n && (ìlà[위치] == 32 || ìlà[위치] == 9)) 위치++;
            if (위치 == Ìwọ̀n) break;
            if (토큰수 == 16) { 단말.Kọ("Àṣẹ ìpínsíwẹ́wẹ́_iye: 인수가 너무 많습니다\n"); return false; }
            시작점[토큰수] = 끝; int 인용 = 0;
            while (위치 < Ìwọ̀n) {
                int iye = ìlà[위치++];
                if (인용 == 0 && (iye == 32 || iye == 9)) break;
                if (iye == 인용) { 인용 = 0; continue; }
                if (인용 == 0 && (iye == 39 || iye == 34)) { 인용 = iye; continue; }
                kóòdù_káàdì_àsansílẹ̀_iye[끝++] = iye;
            }
            if (인용 != 0) { 단말.Kọ("Àṣẹ ìpínsíwẹ́wẹ́_iye: 따옴표가 닫히지 않았습니다\n"); return false; }
            gígùn_iye[토큰수] = 끝 - 시작점[토큰수]; 토큰수++;
        }
        return true;
    }
    static boolean 같음(int wá_atọ̀ka_àkóónú, String Ọ̀rọ̀_SMS) {
        if (wá_atọ̀ka_àkóónú >= 토큰수) return false;
        int 자리=0;
        for (int 순번=0; 순번<Ọ̀rọ̀_SMS.length(); 순번++) {
            int kóòdù_ẹyọ_ọ̀rọ̀=Ọ̀rọ̀_SMS.charAt(순번);
            if (kóòdù_ẹyọ_ọ̀rọ̀>=0xd800 && kóòdù_ẹyọ_ọ̀rọ̀<=0xdbff && 순번+1<Ọ̀rọ̀_SMS.length()) kóòdù_ẹyọ_ọ̀rọ̀=0x10000+((kóòdù_ẹyọ_ọ̀rọ̀-0xd800)<<10)+Ọ̀rọ̀_SMS.charAt(++순번)-0xdc00;
            int 바이트수=kóòdù_ẹyọ_ọ̀rọ̀<128?1:kóòdù_ẹyọ_ọ̀rọ̀<2048?2:kóòdù_ẹyọ_ọ̀rọ̀<65536?3:4;
            for (int ÀTẸ̀LÉRA_iye=바이트수-1; ÀTẸ̀LÉRA_iye>=0; ÀTẸ̀LÉRA_iye--) {
                int iye=바이트수==1?kóòdù_ẹyọ_ọ̀rọ̀:ÀTẸ̀LÉRA_iye==바이트수-1?(바이트수==2?0xc0:바이트수==3?0xe0:0xf0)|(kóòdù_ẹyọ_ọ̀rọ̀>>(6*ÀTẸ̀LÉRA_iye)):0x80|((kóòdù_ẹyọ_ọ̀rọ̀>>(6*ÀTẸ̀LÉRA_iye))&63);
                if (자리>=gígùn_iye[wá_atọ̀ka_àkóónú] || kóòdù_káàdì_àsansílẹ̀_iye[시작점[wá_atọ̀ka_àkóónú]+자리++]!=iye) return false;
            }
        }
        return 자리==gígùn_iye[wá_atọ̀ka_àkóónú];
    }
    static int ọ̀nà(int wá_atọ̀ka_àkóónú) {
        if (wá_atọ̀ka_àkóónú >= 토큰수) return -22;
        int 결과 = ibi_ìpamọ́_Àwọn_fáìlì.ọ̀nà_bẹ̀rẹ̀(gígùn_iye[wá_atọ̀ka_àkóónú]); if (결과 < 0) return 결과;
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < gígùn_iye[wá_atọ̀ka_àkóónú]; ṣetúnṣe_wá_atọ̀ka_àkóónú++) {
            결과 = ibi_ìpamọ́_Àwọn_fáìlì.ọ̀nà_báìtì(ṣetúnṣe_wá_atọ̀ka_àkóónú, kóòdù_káàdì_àsansílẹ̀_iye[시작점[wá_atọ̀ka_àkóónú] + ṣetúnṣe_wá_atọ̀ka_àkóónú]); if (결과 < 0) return 결과;
        }
        return 0;
    }
    static void àṣìṣe(int wá_atọ̀ka_àkóónú) { 결과 = 1; 단말.Kọ("àṣìṣe "); 단말.수(wá_atọ̀ka_àkóónú); 단말.문자(10); }
    static void wo_iye() {
        if (토큰수 != 2) { 단말.Kọ("사용법: cat Fáìlì\n"); return; }
        int 결과 = ọ̀nà(1); if (결과 < 0) { àṣìṣe(결과); return; }
        int Fáìlì = ibi_ìpamọ́_Àwọn_fáìlì.Ṣi(0); if (Fáìlì < 0) { àṣìṣe(Fáìlì); return; }
        while (true) { int iye = ibi_ìpamọ́_Àwọn_fáìlì.Kàá(Fáìlì); if (iye == 256) break; if (iye < 0) { àṣìṣe(iye); break; } 원바이트(iye); }
        ibi_ìpamọ́_Àwọn_fáìlì.Ti(Fáìlì); 단말.문자(10);
    }
    static void ṣàtúnṣe_iye() {
        if (토큰수 != 2) { 단말.Kọ("사용법: edit Fáìlì\n"); return; }
        int 결과 = ọ̀nà(1); if (결과 < 0) { àṣìṣe(결과); return; }
        ṣàtúnṣe_orúkọ_gígùn = gígùn_iye[1];
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < ṣàtúnṣe_orúkọ_gígùn; ṣetúnṣe_wá_atọ̀ka_àkóónú++) ṣàtúnṣe_orúkọ[ṣetúnṣe_wá_atọ̀ka_àkóónú] = kóòdù_káàdì_àsansílẹ̀_iye[시작점[1] + ṣetúnṣe_wá_atọ̀ka_àkóónú];
        단말.Kọ("EDIT: Fáìlì 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int Ìwọ̀n = 0;
        while (true) {
            단말.Kọ("edit> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Kọ("EDIT CANCELLED\n"); return; }
            if (입력 == 1 && ìlà[0] == '.') break;
            if (입력 + 1 > 편집내용.length - Ìwọ̀n) { 단말.Kọ("EDIT CANCELLED: file too large\n"); return; }
            for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 입력; ṣetúnṣe_wá_atọ̀ka_àkóónú++) 편집내용[Ìwọ̀n++] = ìlà[ṣetúnṣe_wá_atọ̀ka_àkóónú];
            편집내용[Ìwọ̀n++] = 10;
        }
        ibi_ìpamọ́_Àwọn_fáìlì.ọ̀nà_bẹ̀rẹ̀(ṣàtúnṣe_orúkọ_gígùn);
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < ṣàtúnṣe_orúkọ_gígùn; ṣetúnṣe_wá_atọ̀ka_àkóónú++) ibi_ìpamọ́_Àwọn_fáìlì.ọ̀nà_báìtì(ṣetúnṣe_wá_atọ̀ka_àkóónú, ṣàtúnṣe_orúkọ[ṣetúnṣe_wá_atọ̀ka_àkóónú]);
        int Fáìlì = ibi_ìpamọ́_Àwọn_fáìlì.Ṣi(577); if (Fáìlì < 0) { àṣìṣe(Fáìlì); return; }
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < Ìwọ̀n; ṣetúnṣe_wá_atọ̀ka_àkóónú++) ibi_ìpamọ́_Àwọn_fáìlì.Kọ(Fáìlì, 편집내용[ṣetúnṣe_wá_atọ̀ka_àkóónú]);
        ibi_ìpamọ́_Àwọn_fáìlì.Ti(Fáìlì); 단말.Kọ("SAVED "); 단말.수(Ìwọ̀n); 단말.Kọ("báìtì_iye(주기억 Fáìlì)\n");
    }
    static int 십육(int iye) {
        if (iye >= '0' && iye <= '9') return iye - '0';
        if (iye >= 'a' && iye <= 'f') return iye - 'a' + 10;
        if (iye >= 'A' && iye <= 'F') return iye - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (토큰수 != 2) { 단말.Kọ("사용법: load Fáìlì | hex Fáìlì\n"); return; }
        int 결과 = ọ̀nà(1); if (결과 < 0) { àṣìṣe(결과); return; }
        if (!넣기) {
            int Fáìlì = ibi_ìpamọ́_Àwọn_fáìlì.Ṣi(0); if (Fáìlì < 0) { àṣìṣe(Fáìlì); return; }
            단말.Kọ("HEX BEGIN "); 단말.수(ibi_ìpamọ́_Àwọn_fáìlì.Ìwọ̀n(Fáìlì)); 단말.문자(10);
            int 항목수 = 0;
            while (true) {
                int iye = ibi_ìpamọ́_Àwọn_fáìlì.Kàá(Fáìlì); if (iye < 0 || iye == 256) break;
                단말.문자("0123456789abcdef".charAt(iye >> 4)); 단말.문자("0123456789abcdef".charAt(iye & 15));
                if (++항목수 % 32 == 0) 단말.문자(10);
            }
            if (항목수 % 32 != 0) 단말.문자(10);
            ibi_ìpamọ́_Àwọn_fáìlì.Ti(Fáìlì); 단말.Kọ("HEX END\n"); return;
        }
        ṣàtúnṣe_orúkọ_gígùn = gígùn_iye[1];
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < ṣàtúnṣe_orúkọ_gígùn; ṣetúnṣe_wá_atọ̀ka_àkóónú++) ṣàtúnṣe_orúkọ[ṣetúnṣe_wá_atọ̀ka_àkóónú] = kóòdù_káàdì_àsansílẹ̀_iye[시작점[1] + ṣetúnṣe_wá_atọ̀ka_àkóónú];
        단말.Kọ("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int Ìwọ̀n = 0;
        while (true) {
            단말.Kọ("hex> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Kọ("LOAD CANCELLED\n"); return; }
            if (입력 == 1 && ìlà[0] == '.') break;
            int 앞 = -1;
            for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 입력; ṣetúnṣe_wá_atọ̀ka_àkóónú++) {
                if (ìlà[ṣetúnṣe_wá_atọ̀ka_àkóónú] == 32 || ìlà[ṣetúnṣe_wá_atọ̀ka_àkóónú] == 9) continue;
                int iye = 십육(ìlà[ṣetúnṣe_wá_atọ̀ka_àkóónú]);
                if (iye < 0 || Ìwọ̀n >= 편집내용.length) { 단말.Kọ("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (앞 < 0) 앞 = iye; else { 편집내용[Ìwọ̀n++] = 앞 * 16 + iye; 앞 = -1; }
            }
            if (앞 >= 0) { 단말.Kọ("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        ibi_ìpamọ́_Àwọn_fáìlì.ọ̀nà_bẹ̀rẹ̀(ṣàtúnṣe_orúkọ_gígùn);
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < ṣàtúnṣe_orúkọ_gígùn; ṣetúnṣe_wá_atọ̀ka_àkóónú++) ibi_ìpamọ́_Àwọn_fáìlì.ọ̀nà_báìtì(ṣetúnṣe_wá_atọ̀ka_àkóónú, ṣàtúnṣe_orúkọ[ṣetúnṣe_wá_atọ̀ka_àkóónú]);
        int Fáìlì = ibi_ìpamọ́_Àwọn_fáìlì.Ṣi(577); if (Fáìlì < 0) { àṣìṣe(Fáìlì); return; }
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < Ìwọ̀n; ṣetúnṣe_wá_atọ̀ka_àkóónú++) ibi_ìpamọ́_Àwọn_fáìlì.Kọ(Fáìlì, 편집내용[ṣetúnṣe_wá_atọ̀ka_àkóónú]);
        ibi_ìpamọ́_Àwọn_fáìlì.Ti(Fáìlì); 단말.Kọ("LOADED "); 단말.수(Ìwọ̀n); 단말.Kọ("báìtì_iye(주기억 Fáìlì)\n");
    }
    static int Àwọn_irinṣẹ́(int wá_atọ̀ka_àkóónú) {
        return irinṣẹ́_ìgbéwọlé(wá_atọ̀ka_àkóónú, 1);
    }
    static int irinṣẹ́_ìgbéwọlé(int wá_atọ̀ka_àkóónú, int Rọ́ọ̀nù) {
        if (토큰수 - Rọ́ọ̀nù > 8) return -22;
        보드.인수준비(토큰수 - Rọ́ọ̀nù);
        for (int 첫값 = Rọ́ọ̀nù; 첫값 < 토큰수; 첫값++) {
            if (gígùn_iye[첫값] > 255) return -36;
            for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < gígùn_iye[첫값]; ṣetúnṣe_wá_atọ̀ka_àkóónú++) 보드.ágúmẹ́ntì_báìtì(첫값 - Rọ́ọ̀nù, ṣetúnṣe_wá_atọ̀ka_àkóónú, kóòdù_káàdì_àsansílẹ̀_iye[시작점[첫값] + ṣetúnṣe_wá_atọ̀ka_àkóónú]);
        }
        return wá_atọ̀ka_àkóónú == -2 ? 보드.리눅스파일실행() : wá_atọ̀ka_àkóónú < 0 ? 보드.ṣiṣẹ́_aṣàmúlò_fáìlì() : 보드.ṣiṣẹ́_aṣàmúlò_àtòjọ_ètò(wá_atọ̀ka_àkóónú);
    }
    static int 파이썬꾸러미() {
        if (토큰수 > 8) return -22;
        보드.인수준비(토큰수);
        String ọ̀nà = "/lib/àkópọ̀.py";
        // Java 문자열을 셸의 UTF-8 인수 버퍼에 기록한다.
        int 자리 = 0;
        for (int 순번 = 0; 순번 < ọ̀nà.length(); 순번++) {
            int ẹyọ_ọ̀rọ̀_iye = ọ̀nà.charAt(순번);
            if (ẹyọ_ọ̀rọ̀_iye < 128) 보드.ágúmẹ́ntì_báìtì(0, 자리++, ẹyọ_ọ̀rọ̀_iye);
            else { 보드.ágúmẹ́ntì_báìtì(0, 자리++, 0xe0 | (ẹyọ_ọ̀rọ̀_iye >> 12)); 보드.ágúmẹ́ntì_báìtì(0, 자리++, 0x80 | ((ẹyọ_ọ̀rọ̀_iye >> 6) & 63)); 보드.ágúmẹ́ntì_báìtì(0, 자리++, 0x80 | (ẹyọ_ọ̀rọ̀_iye & 63)); }
        }
        for (int 순번 = 1; 순번 < 토큰수; 순번++) {
            if (gígùn_iye[순번] > 255) return -36;
            for (int ẹyọ_ọ̀rọ̀_iye = 0; ẹyọ_ọ̀rọ̀_iye < gígùn_iye[순번]; ẹyọ_ọ̀rọ̀_iye++) 보드.ágúmẹ́ntì_báìtì(순번, ẹyọ_ọ̀rọ̀_iye, kóòdù_káàdì_àsansílẹ̀_iye[시작점[순번] + ẹyọ_ọ̀rọ̀_iye]);
        }
        return 보드.ṣiṣẹ́_aṣàmúlò_àtòjọ_ètò(12);
    }
    static int 실행형식() {
        int 처리값 = ọ̀nà(0); if (처리값 < 0) return 처리값;
        int Fáìlì = ibi_ìpamọ́_Àwọn_fáìlì.Ṣi(0); if (Fáìlì < 0) return Fáìlì;
        int 첫값 = ibi_ìpamọ́_Àwọn_fáìlì.Kàá(Fáìlì), báìtì_détà = ibi_ìpamọ́_Àwọn_fáìlì.Kàá(Fáìlì), kóòdù_ẹyọ_ọ̀rọ̀ = ibi_ìpamọ́_Àwọn_fáìlì.Kàá(Fáìlì), 뒷값 = ibi_ìpamọ́_Àwọn_fáìlì.Kàá(Fáìlì);
        ibi_ìpamọ́_Àwọn_fáìlì.Ti(Fáìlì);
        if (첫값 == 127 && báìtì_détà == 'E' && kóòdù_ẹyọ_ọ̀rọ̀ == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && báìtì_détà == 'K' && kóòdù_ẹyọ_ọ̀rọ̀ == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int wá_atọ̀ka_àkóónú, String 인수) {
        보드.인수준비(1);
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 인수.length(); ṣetúnṣe_wá_atọ̀ka_àkóónú++) 보드.ágúmẹ́ntì_báìtì(0, ṣetúnṣe_wá_atọ̀ka_àkóónú, 인수.charAt(ṣetúnṣe_wá_atọ̀ka_àkóónú));
        return 보드.ṣiṣẹ́_aṣàmúlò_àtòjọ_ètò(wá_atọ̀ka_àkóónú);
    }
    static void SMS_báìtì(int Fáìlì, int iye) { ibi_ìpamọ́_Àwọn_fáìlì.Kọ(Fáìlì, iye); }
    static void ìdágún_fáìlì(String Orúkọ, String Àkóónú_iye) {
        // àkópọ̀ 파일명은 ASCII. Fáìlì 내용은 UTF-8로 저장한다.
        ibi_ìpamọ́_Àwọn_fáìlì.ọ̀nà_bẹ̀rẹ̀(Orúkọ.length());
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < Orúkọ.length(); ṣetúnṣe_wá_atọ̀ka_àkóónú++) ibi_ìpamọ́_Àwọn_fáìlì.ọ̀nà_báìtì(ṣetúnṣe_wá_atọ̀ka_àkóónú, Orúkọ.charAt(ṣetúnṣe_wá_atọ̀ka_àkóónú));
        int Fáìlì = ibi_ìpamọ́_Àwọn_fáìlì.Ṣi(193); if (Fáìlì < 0) return;
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < Àkóónú_iye.length(); ṣetúnṣe_wá_atọ̀ka_àkóónú++) {
            int kóòdù_ẹyọ_ọ̀rọ̀ = Àkóónú_iye.charAt(ṣetúnṣe_wá_atọ̀ka_àkóónú);
            if (kóòdù_ẹyọ_ọ̀rọ̀ >= 0xd800 && kóòdù_ẹyọ_ọ̀rọ̀ <= 0xdbff && ṣetúnṣe_wá_atọ̀ka_àkóónú + 1 < Àkóónú_iye.length()) kóòdù_ẹyọ_ọ̀rọ̀ = 0x10000 + ((kóòdù_ẹyọ_ọ̀rọ̀ - 0xd800) << 10) + Àkóónú_iye.charAt(++ṣetúnṣe_wá_atọ̀ka_àkóónú) - 0xdc00;
            if (kóòdù_ẹyọ_ọ̀rọ̀ < 128) SMS_báìtì(Fáìlì, kóòdù_ẹyọ_ọ̀rọ̀);
            else {
                int 수 = kóòdù_ẹyọ_ọ̀rọ̀ < 2048 ? 2 : kóòdù_ẹyọ_ọ̀rọ̀ < 65536 ? 3 : 4;
                SMS_báìtì(Fáìlì, (수 == 2 ? 0xc0 : 수 == 3 ? 0xe0 : 0xf0) | (kóòdù_ẹyọ_ọ̀rọ̀ >> (6 * (수 - 1))));
                for (int 항목수 = 수 - 1; 항목수 > 0; 항목수--) SMS_báìtì(Fáìlì, 0x80 | ((kóòdù_ẹyọ_ọ̀rọ̀ >> (6 * (항목수 - 1))) & 63));
            }
        }
        ibi_ìpamọ́_Àwọn_fáìlì.Ti(Fáìlì);
    }
    static void 한글도움말() {
        단말.Kọ("F9 / Shift+Space: [EN] ↔ [yo]\n");
        단말.Kọ("  [YO] keyboard; [EN] ASCII\n");
        단말.Kọ("  a → a\n");
        단말.Kọ("  F9: EN ↔ yo | Ctrl+Shift+V: UTF-8\n");
        단말.Kọ("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.Kọ("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String Orúkọ) {
        int 바이트수 = 0;
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < Orúkọ.length(); ṣetúnṣe_wá_atọ̀ka_àkóónú++) { int kóòdù_ẹyọ_ọ̀rọ̀ = Orúkọ.charAt(ṣetúnṣe_wá_atọ̀ka_àkóónú); if (kóòdù_ẹyọ_ọ̀rọ̀ >= 0xd800 && kóòdù_ẹyọ_ọ̀rọ̀ <= 0xdfff) return -22; 바이트수 += kóòdù_ẹyọ_ọ̀rọ̀ < 128 ? 1 : kóòdù_ẹyọ_ọ̀rọ̀ < 2048 ? 2 : 3; }
        int 처리값 = ibi_ìpamọ́_Àwọn_fáìlì.ọ̀nà_bẹ̀rẹ̀(바이트수); if (처리값 < 0) return 처리값;
        int 자리 = 0;
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < Orúkọ.length(); ṣetúnṣe_wá_atọ̀ka_àkóónú++) {
            int kóòdù_ẹyọ_ọ̀rọ̀ = Orúkọ.charAt(ṣetúnṣe_wá_atọ̀ka_àkóónú);
            if (kóòdù_ẹyọ_ọ̀rọ̀ < 128) ibi_ìpamọ́_Àwọn_fáìlì.ọ̀nà_báìtì(자리++, kóòdù_ẹyọ_ọ̀rọ̀);
            else if (kóòdù_ẹyọ_ọ̀rọ̀ < 2048) { ibi_ìpamọ́_Àwọn_fáìlì.ọ̀nà_báìtì(자리++, 0xc0 | (kóòdù_ẹyọ_ọ̀rọ̀ >> 6)); ibi_ìpamọ́_Àwọn_fáìlì.ọ̀nà_báìtì(자리++, 0x80 | (kóòdù_ẹyọ_ọ̀rọ̀ & 63)); }
            else { ibi_ìpamọ́_Àwọn_fáìlì.ọ̀nà_báìtì(자리++, 0xe0 | (kóòdù_ẹyọ_ọ̀rọ̀ >> 12)); ibi_ìpamọ́_Àwọn_fáìlì.ọ̀nà_báìtì(자리++, 0x80 | ((kóòdù_ẹyọ_ọ̀rọ̀ >> 6) & 63)); ibi_ìpamọ́_Àwọn_fáìlì.ọ̀nà_báìtì(자리++, 0x80 | (kóòdù_ẹyọ_ọ̀rọ̀ & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String Orúkọ) {
        int 처리값 = 예제경로(Orúkọ); if (처리값 < 0) return 처리값;
        처리값 = ibi_ìpamọ́_Àwọn_fáìlì.Ṣẹ̀dá_àkójọpọ̀_fáìlì(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String Orúkọ, String détà) {
        int 처리값 = 예제경로(Orúkọ); if (처리값 < 0) return 처리값;
        int Fáìlì = ibi_ìpamọ́_Àwọn_fáìlì.Ṣi(193); if (Fáìlì == -17) return 0; if (Fáìlì < 0) return Fáìlì;
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < détà.length(); ṣetúnṣe_wá_atọ̀ka_àkóónú += 2) {
            처리값 = ibi_ìpamọ́_Àwọn_fáìlì.Kọ(Fáìlì, 십육(détà.charAt(ṣetúnṣe_wá_atọ̀ka_àkóónú)) * 16 + 십육(détà.charAt(ṣetúnṣe_wá_atọ̀ka_àkóónú + 1)));
            if (처리값 < 0) { ibi_ìpamọ́_Àwọn_fáìlì.Ti(Fáìlì); return 처리값; }
        }
        return ibi_ìpamọ́_Àwọn_fáìlì.Ti(Fáìlì);
    }
    static void ṣàfihàn_ìrànwọ́() {
        ètò_irinṣẹ́.ṣàfihàn_ìrànwọ́();
        단말.Kọ("sshd / Tóláàbò_ṣẹ́ẹ̀lì start|stop|status: SSH :22 (user, 장치별 ọ̀rọ̀_aṣínà_iye)\n");
        단말.Kọ("vncd / Ìjìnnà_ṣàfihàn start|stop|status: VNC :5900 (장치별 ọ̀rọ̀_aṣínà_iye)\n");
        단말.Kọ("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.Kọ("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.Kọ("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.Kọ("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.Kọ("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.Kọ("모서리 + 왼쪽 버튼 wọ́_iye: 터미널 Ìwọ̀n ṣàyípadà_iye; terminal size: ìlà_òró_iye/ìlà_ìbú_iye\n");
        단말.Kọ("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.Kọ("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.Kọ("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.Kọ("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.Kọ("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.Kọ("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.Kọ("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.Kọ("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.Kọ("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.Kọ("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.Kọ("pip: MicroPython orísun_ètò_afigijúwe ṣàgbékalẹ̀_iye; olùpèsè --network --pip 필요; /lib는 RAM\n");
        단말.Kọ("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.Kọ("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.Kọ("/example/java /example/c /example/python: examples ready at boot\n");
        단말.Kọ("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void 터미널(boolean 전환여부) {
        if (전환여부 && 보드.터미널(2) != 0) { 보드.터미널(0); 단말.Kọ("TERMINAL CLOSED\n"); }
        else if (보드.터미널(1) < 0) àṣìṣe(-19);
        else 단말.Kọ("TERMINAL READY — yo terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void Àṣẹ() {
        if (토큰수 == 0) return;
        if (ètò_irinṣẹ́.ṣiṣẹ́_àṣẹ()) return;
        if (같음(0,"sshd") || 같음(0,"Tóláàbò_ṣẹ́ẹ̀lì") || 같음(0,"vncd") || 같음(0,"Ìjìnnà_ṣàfihàn")) {
            int 종류=같음(0,"vncd")||같음(0,"Ìjìnnà_ṣàfihàn")?1:0;
            int ìṣe=같음(1,"start")||같음(1,"Rọ́ọ̀nù")?1:같음(1,"stop")||같음(1,"Dúró")?0:2;
            int ipò_iye=보드.ìṣòjìjí(종류,ìṣe);
            if(ipò_iye<0)àṣìṣe(ipò_iye);else 단말.Kọ(보드.ìṣòjìjí(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else ṣàfihàn_ìrànwọ́(); }
        else if (같음(0, "info") || 같음(0, "i")) kánẹ́ẹ̀lì.msinfo32_exe();
        else if (같음(0, "pwd")) { ibi_ìpamọ́_Àwọn_fáìlì.현재쓰기(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (토큰수 == 1) { ibi_ìpamọ́_Àwọn_fáìlì.ọ̀nà_bẹ̀rẹ̀(1); 처리값 = ibi_ìpamọ́_Àwọn_fáìlì.ọ̀nà_báìtì(0, '/'); } else 처리값 = 토큰수 == 2 ? ọ̀nà(1) : -22;
            if (처리값 >= 0) 처리값 = ibi_ìpamọ́_Àwọn_fáìlì.ṣàyípadà_àkójọpọ̀_fáìlì(); if (처리값 < 0) àṣìṣe(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int ágúmẹ́ntì_wá_atọ̀ka_àkóónú = 같음(1, "-l") ? 2 : 1, 처리값;
            if (토큰수 == ágúmẹ́ntì_wá_atọ̀ka_àkóónú) { ibi_ìpamọ́_Àwọn_fáìlì.ọ̀nà_bẹ̀rẹ̀(1); 처리값 = ibi_ìpamọ́_Àwọn_fáìlì.ọ̀nà_báìtì(0, '.'); } else 처리값 = 토큰수 == ágúmẹ́ntì_wá_atọ̀ka_àkóónú + 1 ? ọ̀nà(ágúmẹ́ntì_wá_atọ̀ka_àkóónú) : -22;
            if (처리값 >= 0) 처리값 = ibi_ìpamọ́_Àwọn_fáìlì.경로목록(); if (처리값 < 0) àṣìṣe(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) ṣẹ́ẹ̀lì_Àwọn_irinṣẹ́.fáìlì_iṣẹ́(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) ṣẹ́ẹ̀lì_Àwọn_irinṣẹ́.ṣẹ̀dà_iye(같음(0, "mv"));
        else if (같음(0, "cat")) ṣẹ́ẹ̀lì_Àwọn_irinṣẹ́.wo_iye();
        else if (같음(0, "wc")) ṣẹ́ẹ̀lì_Àwọn_irinṣẹ́.세기();
        else if (같음(0, "grep")) ṣẹ́ẹ̀lì_Àwọn_irinṣẹ́.wá_ìgbéwọlé();
        else if (같음(0, "head") || 같음(0, "tail")) ṣẹ́ẹ̀lì_Àwọn_irinṣẹ́.머리(같음(0, "tail"));
        else if (같음(0, "tee")) ṣẹ́ẹ̀lì_Àwọn_irinṣẹ́.함께쓰기();
        else if (같음(0, "env")) ṣẹ́ẹ̀lì_síntáàsì.환경보기();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (토큰수 == 1) ṣẹ́ẹ̀lì_síntáàsì.환경보기();
            for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 1; ṣetúnṣe_wá_atọ̀ka_àkóónú < 토큰수; ṣetúnṣe_wá_atọ̀ka_àkóónú++) { int 처리값 = ṣẹ́ẹ̀lì_síntáàsì.환경설정(ṣetúnṣe_wá_atọ̀ka_àkóónú, 같음(0, "unset")); if (처리값 != 0) { 결과 = 처리값; 단말.Kọ("Àṣẹ ìpínsíwẹ́wẹ́_iye: 변수 이름이 잘못되었거나 예약된 이름이거나 환경 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) ṣẹ́ẹ̀lì_síntáàsì.ṣiṣẹ́_fáìlì();
        else if (같음(0, "true")) 결과 = 0;
        else if (같음(0, "false")) 결과 = 1;
        else if (같음(0, "history")) ìlà_aṣàtúnṣe.ṣàfihàn_àkọsílẹ̀_ìṣe();
        else if (같음(0, "exit")) {
            if (ṣẹ́ẹ̀lì_síntáàsì.깊이 > 0) { 결과 = 토큰수 == 1 ? ṣẹ́ẹ̀lì_síntáàsì.ipò_iye : ṣẹ́ẹ̀lì_Àwọn_irinṣẹ́.díjììtì_iye(1); if (결과 < 0 || 결과 > 255) 결과 = 2; ṣẹ́ẹ̀lì_síntáàsì.ìlànà_ìṣe_léréfèé_parí = true; }
            else if (보드.터미널(2) != 0) 터미널(true);
            else 단말.Kọ("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) ṣàtúnṣe_iye();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (토큰수 < 2) { 결과 = 2; 단말.Kọ("사용법: rm Fáìlì...\n"); }
            for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 1; ṣetúnṣe_wá_atọ̀ka_àkóónú < 토큰수; ṣetúnṣe_wá_atọ̀ka_àkóónú++) { int 처리값 = ọ̀nà(ṣetúnṣe_wá_atọ̀ka_àkóónú); if (처리값 == 0) 처리값 = ibi_ìpamọ́_Àwọn_fáìlì.지우기(); if (처리값 < 0) àṣìṣe(처리값); }
        }
        else if (같음(0, "echo")) {
            int 시작자리 = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = 시작자리; 첫값 < 토큰수; 첫값++) { if (첫값 > 시작자리) 단말.문자(32); for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < gígùn_iye[첫값]; ṣetúnṣe_wá_atọ̀ka_àkóónú++) 보드.직렬쓰기(kóòdù_káàdì_àsansílẹ̀_iye[시작점[첫값] + ṣetúnṣe_wá_atọ̀ka_àkóónú]); }
            if (시작자리 == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.Kọ("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? 파이썬꾸러미() : Àwọn_irinṣẹ́(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !ṣẹ́ẹ̀lì_síntáàsì.연결중) { 단말.Kọ("exit "); 단말.수(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = Àwọn_irinṣẹ́(13); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = Àwọn_irinṣẹ́(15); 결과 = 처리값 < 0 ? 126 : 처리값; if (!ṣẹ́ẹ̀lì_síntáàsì.연결중) { 단말.Kọ("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = Àwọn_irinṣẹ́(16); 결과 = 처리값 < 0 ? 126 : 처리값; if (!ṣẹ́ẹ̀lì_síntáàsì.연결중) { 단말.Kọ("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int Ìwọ̀n = 보드.터미널(13); 단말.Kọ("TERMINAL SIZE "); 단말.수(Ìwọ̀n & 65535); 단말.문자('x'); 단말.수(Ìwọ̀n >>> 16); 단말.문자(10); }
            else 터미널(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { 보드.터미널(9); àtẹ_iṣẹ́.ṣiṣẹ́_àṣẹ(); }
        else if (같음(0, "c")) kánẹ́ẹ̀lì.씨시험();
        else if (같음(0, "tasks") || 같음(0, "t")) kánẹ́ẹ̀lì.작업시험();
        else if (같음(0, "g")) kánẹ́ẹ̀lì.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) kánẹ́ẹ̀lì.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = 보드.ṣiṣẹ́_aṣàmúlò_àtòjọ_ètò(0); if (처리값 == 0) 단말.Kọ("ELF DEMO PASS\n"); else àṣìṣe(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? irinṣẹ́_ìgbéwọlé(-2, 2) : Àwọn_irinṣẹ́(-1); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !ṣẹ́ẹ̀lì_síntáàsì.연결중) { 단말.Kọ("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) kánẹ́ẹ̀lì.통신시험();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = 보드.fáìlì_ṣàgbélọ_isẹ́(1); if (처리값 < 0) àṣìṣe(처리값); else { 단말.Kọ("FTP listening "); ètò_irinṣẹ́.kọ_àdírẹ́ẹ̀sì(보드.Alásopọ̀_ipò(0,0)); 단말.Kọ(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { 보드.fáìlì_ṣàgbélọ_isẹ́(0); 단말.Kọ("FTP stopped\n"); }
            else 단말.Kọ(보드.fáìlì_ṣàgbélọ_isẹ́(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { àkópọ̀.gbaradì(); 단말.Kọ("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int Èdè = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (토큰수 != 2 || Èdè < 0) 단말.Kọ("example java|c|python: 출력, Fáìlì, 네트워크, 그래픽, Java Swing wínńdò 예제\n");
            else { int 처리값 = 예제꾸러미.ṣàgbékalẹ̀_iye(Èdè); if (처리값 < 0) { àṣìṣe(처리값); if (처리값 == -28) 단말.Kọ("RAM full: remove unused files, then retry example\n"); } else 단말.Kọ("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int ìgúnrégé_iye = 실행형식();
            if (ìgúnrégé_iye == 1 || ìgúnrégé_iye == 2) {
                int 처리값 = irinṣẹ́_ìgbéwọlé(ìgúnrégé_iye == 1 ? -1 : 14, 0); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !ṣẹ́ẹ̀lì_síntáàsì.연결중) { 단말.Kọ("exit "); 단말.수(처리값); 단말.문자(10); }
            } else if (ìgúnrégé_iye == 0) { 결과 = 126; 단말.Kọ("실행할 수 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { 결과 = 127; 단말.Kọ("Unknown command. help: commands\n"); }
        }
    }
    public static void ṣiṣẹ́_àṣẹ() {
        àkópọ̀.gbaradì();
        for (int Èdè = 0; Èdè < 3; Èdè++) { int 처리값 = 예제꾸러미.ṣàgbékalẹ̀_iye(Èdè); if (처리값 < 0) àṣìṣe(처리값); }
        ṣàfihàn_ìrànwọ́();
        while (true) {
            wínńdò_sáà.Ìlànà_iye_ìgbéwọlé(); if (wínńdò_sáà.재개()) continue;
            if (!wínńdò_sáà.이어읽기) 단말.Kọ("jkoros-native> "); ìlà_aṣàtúnṣe.ìlà_ìpàṣẹ = true; 보드.원격대기(1); int Ìwọ̀n = 줄읽기(); 보드.원격대기(0); ìlà_aṣàtúnṣe.ìlà_ìpàṣẹ = false;
            if (Ìwọ̀n == -3) continue;
            if (Ìwọ̀n == -2) 단말.Kọ("Àṣẹ ìpínsíwẹ́wẹ́_iye: 명령줄이 너무 깁니다\n");
            if (Ìwọ̀n >= 0) { ṣẹ́ẹ̀lì_síntáàsì.ìlànà_ìṣe_léréfèé_parí = false; ṣẹ́ẹ̀lì_síntáàsì.ṣiṣẹ́_àṣẹ(ìlà, 0, Ìwọ̀n, 0); } else ṣẹ́ẹ̀lì_síntáàsì.ipò_iye = 130;
            보드.parí_Ìjìnnà_àṣẹ(ṣẹ́ẹ̀lì_síntáàsì.ipò_iye);
            ìlà_aṣàtúnṣe.Ìwọ̀n = ìlà_aṣàtúnṣe.kọ́sọ̀_iye = ìlà_aṣàtúnṣe.bẹ̀rẹ̀_wínńdò = 0;
        }
    }
}
