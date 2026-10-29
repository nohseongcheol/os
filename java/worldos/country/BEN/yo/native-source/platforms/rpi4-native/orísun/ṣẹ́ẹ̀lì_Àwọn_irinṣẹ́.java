// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 ṣẹ́ẹ̀lì 내장 Àwọn_irinṣẹ́. */
public final class ṣẹ́ẹ̀lì_Àwọn_irinṣẹ́ {
    static int[] détà = new int[16384];
    static int 입력파일 = -1;
    static int ṣí_fáìlì(int ágúmẹ́ntì_wá_atọ̀ka_àkóónú, int Ìlànà_móòdù) {
        int 처리값 = 명령해석기.ọ̀nà(ágúmẹ́ntì_wá_atọ̀ka_àkóónú); return 처리값 < 0 ? 처리값 : ibi_ìpamọ́_Àwọn_fáìlì.Ṣi(Ìlànà_móòdù);
    }
    static boolean 입력준비(int ágúmẹ́ntì_wá_atọ̀ka_àkóónú) {
        입력파일 = -1;
        if (ágúmẹ́ntì_wá_atọ̀ka_àkóónú < 명령해석기.토큰수) {
            입력파일 = ṣí_fáìlì(ágúmẹ́ntì_wá_atọ̀ka_àkóónú, 0);
            if (입력파일 < 0) { 명령해석기.àṣìṣe(입력파일); return false; }
        }
        return true;
    }
    static int Kàá() {
        if (입력파일 >= 3) return ibi_ìpamọ́_Àwọn_fáìlì.Kàá(입력파일);
        while (true) {
            int báìtì_détà = 보드.직렬읽기(); if (báìtì_détà == -2 || báìtì_détà == 4) return 256;
            if (báìtì_détà == 3) { 명령해석기.결과 = 130; return 256; }
            if (báìtì_détà >= 0) return báìtì_détà; 보드.ti_dádúró_díẹ̀_CPU();
        }
    }
    static void Ti() { if (입력파일 >= 3) ibi_ìpamọ́_Àwọn_fáìlì.Ti(입력파일); 입력파일 = -1; }
    static void wo_iye() {
        int 마지막자리 = 명령해석기.토큰수 == 1 ? 2 : 명령해석기.토큰수;
        for (int ágúmẹ́ntì_wá_atọ̀ka_àkóónú = 1; ágúmẹ́ntì_wá_atọ̀ka_àkóónú < 마지막자리; ágúmẹ́ntì_wá_atọ̀ka_àkóónú++) {
            if (!입력준비(ágúmẹ́ntì_wá_atọ̀ka_àkóónú)) continue;
            int báìtì_détà; while ((báìtì_détà = Kàá()) != 256 && báìtì_détà >= 0) 보드.직렬쓰기(báìtì_détà);
            if (báìtì_détà < 0) 명령해석기.àṣìṣe(báìtì_détà); Ti();
        }
    }
    static void fáìlì_iṣẹ́(String 동작번호) {
        if (명령해석기.토큰수 != 2) { 명령해석기.결과 = 2; 단말.Kọ("사용법: mkdir/rmdir/touch Fáìlì\n"); return; }
        int 처리값 = 명령해석기.ọ̀nà(1);
        if (처리값 >= 0) {
            if (동작번호.charAt(0) == 'm') 처리값 = ibi_ìpamọ́_Àwọn_fáìlì.Ṣẹ̀dá_àkójọpọ̀_fáìlì();
            else if (동작번호.charAt(0) == 'r') 처리값 = ibi_ìpamọ́_Àwọn_fáìlì.ṣèmúkúro_àkójọpọ̀_fáìlì();
            else { 처리값 = ibi_ìpamọ́_Àwọn_fáìlì.Ṣi(65); if (처리값 >= 3) 처리값 = ibi_ìpamọ́_Àwọn_fáìlì.Ti(처리값); }
        }
        if (처리값 < 0) 명령해석기.àṣìṣe(처리값);
    }
    static void ṣẹ̀dà_iye(boolean 이동여부) {
        if (명령해석기.토큰수 != 3) { 명령해석기.결과 = 2; 단말.Kọ("사용법: cp/mv 원본 목적지 (Fáìlì)\n"); return; }
        int 처리값 = 명령해석기.ọ̀nà(1); if (처리값 >= 0) 처리값 = ibi_ìpamọ́_Àwọn_fáìlì.ṣe_níwọ̀n_iye();
        if (처리값 < 0) { 명령해석기.àṣìṣe(처리값); return; }
        int 원본번호 = ibi_ìpamọ́_Àwọn_fáìlì.wá_ìgbéwọlé(); if (원본번호 < 0) { 명령해석기.àṣìṣe(-2); return; }
        int 항목수 = ibi_ìpamọ́_Àwọn_fáìlì.gígùn_iye[원본번호]; for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 항목수; ṣetúnṣe_wá_atọ̀ka_àkóónú++) détà[ṣetúnṣe_wá_atọ̀ka_àkóónú] = ibi_ìpamọ́_Àwọn_fáìlì.자료읽기(원본번호, ṣetúnṣe_wá_atọ̀ka_àkóónú);
        처리값 = 명령해석기.ọ̀nà(2); if (처리값 >= 0) 처리값 = ibi_ìpamọ́_Àwọn_fáìlì.ṣe_níwọ̀n_iye();
        if (처리값 < 0) { 명령해석기.àṣìṣe(처리값); return; }
        if (ibi_ìpamọ́_Àwọn_fáìlì.wá_ìgbéwọlé() == 원본번호) { if (!이동여부) 명령해석기.àṣìṣe(-22); return; }
        if (이동여부) { 처리값 = ibi_ìpamọ́_Àwọn_fáìlì.이름바꾸기(원본번호); if (처리값 < 0) 명령해석기.àṣìṣe(처리값); return; }
        int 열린파일번호 = ibi_ìpamọ́_Àwọn_fáìlì.Ṣi(577); if (열린파일번호 < 0) { 명령해석기.àṣìṣe(열린파일번호); return; }
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 항목수; ṣetúnṣe_wá_atọ̀ka_àkóónú++) { 처리값 = ibi_ìpamọ́_Àwọn_fáìlì.Kọ(열린파일번호, détà[ṣetúnṣe_wá_atọ̀ka_àkóónú]); if (처리값 < 0) { 명령해석기.àṣìṣe(처리값); break; } }
        ibi_ìpamọ́_Àwọn_fáìlì.Ti(열린파일번호);
    }
    static int díjììtì_iye(int ágúmẹ́ntì_wá_atọ̀ka_àkóónú) {
        if (ágúmẹ́ntì_wá_atọ̀ka_àkóónú >= 명령해석기.토큰수) return -1;
        int 항목수 = 0; for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 명령해석기.gígùn_iye[ágúmẹ́ntì_wá_atọ̀ka_àkóónú]; ṣetúnṣe_wá_atọ̀ka_àkóónú++) { int kóòdù_ẹyọ_ọ̀rọ̀ = 명령해석기.kóòdù_káàdì_àsansílẹ̀_iye[명령해석기.시작점[ágúmẹ́ntì_wá_atọ̀ka_àkóónú] + ṣetúnṣe_wá_atọ̀ka_àkóónú]; if (kóòdù_ẹyọ_ọ̀rọ̀ < '0' || kóòdù_ẹyọ_ọ̀rọ̀ > '9' || 항목수 > 10000) return -1; 항목수 = 항목수 * 10 + kóòdù_ẹyọ_ọ̀rọ̀ - '0'; } return 항목수;
    }
    static void 세기() {
        int ágúmẹ́ntì_wá_atọ̀ka_àkóónú = 1, 선택번호 = 0;
        if (명령해석기.같음(1, "-c") || 명령해석기.같음(1, "-l") || 명령해석기.같음(1, "-w")) { 선택번호 = 명령해석기.같음(1, "-c") ? 1 : 명령해석기.같음(1, "-l") ? 2 : 3; ágúmẹ́ntì_wá_atọ̀ka_àkóónú++; }
        if (명령해석기.토큰수 > ágúmẹ́ntì_wá_atọ̀ka_àkóónú + 1) { 명령해석기.결과 = 2; 단말.Kọ("사용법: wc [-c|-l|-w] [Fáìlì]\n"); return; }
        if (!입력준비(ágúmẹ́ntì_wá_atọ̀ka_àkóónú)) return;
        int 바이트수 = 0, 줄수 = 0, 낱말수 = 0, báìtì_détà; boolean 낱말 = false;
        while ((báìtì_détà = Kàá()) >= 0 && báìtì_détà != 256) { 바이트수++; if (báìtì_détà == 10) 줄수++; boolean àlàfo = báìtì_détà == 32 || báìtì_détà >= 9 && báìtì_détà <= 13; if (!àlàfo && !낱말) 낱말수++; 낱말 = !àlàfo; }
        Ti(); if (báìtì_détà < 0) { 명령해석기.àṣìṣe(báìtì_détà); return; }
        if (선택번호 != 0) 단말.수(선택번호 == 1 ? 바이트수 : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.수(줄수); 단말.문자(' '); 단말.수(낱말수); 단말.문자(' '); 단말.수(바이트수); } 단말.문자(10);
    }
    static void wá_ìgbéwọlé() {
        if (명령해석기.토큰수 < 2 || 명령해석기.토큰수 > 3) { 명령해석기.결과 = 2; 단말.Kọ("사용법: grep 찾을문구 [Fáìlì]\n"); return; }
        if (!입력준비(2)) return;
        int 항목수 = 0, báìtì_détà, 일치수 = 0;
        while (true) {
            báìtì_détà = Kàá();
            if (báìtì_détà == 10 || báìtì_détà == 256 || báìtì_détà < 0) {
                boolean 찾은여부 = false;
                for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú <= 항목수 - 명령해석기.gígùn_iye[1]; ṣetúnṣe_wá_atọ̀ka_àkóónú++) {
                    boolean 같은여부 = true; for (int 안쪽자리 = 0; 안쪽자리 < 명령해석기.gígùn_iye[1]; 안쪽자리++) if (détà[ṣetúnṣe_wá_atọ̀ka_àkóónú + 안쪽자리] != 명령해석기.kóòdù_káàdì_àsansílẹ̀_iye[명령해석기.시작점[1] + 안쪽자리]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (항목수 > 0 || báìtì_détà == 10)) { for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 항목수; ṣetúnṣe_wá_atọ̀ka_àkóónú++) 보드.직렬쓰기(détà[ṣetúnṣe_wá_atọ̀ka_àkóónú]); 단말.문자(10); 일치수++; }
                항목수 = 0; if (báìtì_détà != 10) break;
            } else if (항목수 < détà.length) détà[항목수++] = báìtì_détà;
            else { 명령해석기.àṣìṣe(-28); Ti(); return; }
        }
        Ti(); if (báìtì_détà < 0) 명령해석기.àṣìṣe(báìtì_détà); else if (명령해석기.결과 == 0) 명령해석기.결과 = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int ágúmẹ́ntì_wá_atọ̀ka_àkóónú = 1, 줄수 = 10;
        if (명령해석기.같음(1, "-n")) { 줄수 = díjììtì_iye(2); ágúmẹ́ntì_wá_atọ̀ka_àkóónú = 3; }
        if (줄수 < 0 || 명령해석기.토큰수 > ágúmẹ́ntì_wá_atọ̀ka_àkóónú + 1) { 명령해석기.결과 = 2; 단말.Kọ("사용법: head/tail [-n 줄수] [Fáìlì]\n"); return; }
        if (!입력준비(ágúmẹ́ntì_wá_atọ̀ka_àkóónú)) return;
        int 항목수 = 0, báìtì_détà;
        while ((báìtì_détà = Kàá()) != 256 && báìtì_détà >= 0) { if (항목수 == détà.length) { 명령해석기.àṣìṣe(-28); Ti(); return; } détà[항목수++] = báìtì_détà; }
        Ti(); if (báìtì_détà < 0) { 명령해석기.àṣìṣe(báìtì_détà); return; }
        int agbègbè_bẹ̀rẹ̀ = 0, 끝자리 = 항목수;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int 총수 = 0; for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 항목수 - 2; ṣetúnṣe_wá_atọ̀ka_àkóónú >= 0; ṣetúnṣe_wá_atọ̀ka_àkóónú--) if (détà[ṣetúnṣe_wá_atọ̀ka_àkóónú] == 10 && ++총수 == 줄수) { agbègbè_bẹ̀rẹ̀ = ṣetúnṣe_wá_atọ̀ka_àkóónú + 1; break; } }
        else { int 총수 = 0; for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 항목수; ṣetúnṣe_wá_atọ̀ka_àkóónú++) if (détà[ṣetúnṣe_wá_atọ̀ka_àkóónú] == 10 && ++총수 == 줄수) { 끝자리 = ṣetúnṣe_wá_atọ̀ka_àkóónú + 1; break; } }
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = agbègbè_bẹ̀rẹ̀; ṣetúnṣe_wá_atọ̀ka_àkóónú < 끝자리; ṣetúnṣe_wá_atọ̀ka_àkóónú++) 보드.직렬쓰기(détà[ṣetúnṣe_wá_atọ̀ka_àkóónú]);
    }
    static void 함께쓰기() {
        boolean 덧붙임여부 = 명령해석기.같음(1, "-a"); int ágúmẹ́ntì_wá_atọ̀ka_àkóónú = 덧붙임여부 ? 2 : 1;
        if (명령해석기.토큰수 != ágúmẹ́ntì_wá_atọ̀ka_àkóónú + 1) { 명령해석기.결과 = 2; 단말.Kọ("사용법: tee [-a] Fáìlì\n"); return; }
        int 열린파일번호 = ṣí_fáìlì(ágúmẹ́ntì_wá_atọ̀ka_àkóónú, 덧붙임여부 ? 1089 : 577); if (열린파일번호 < 0) { 명령해석기.àṣìṣe(열린파일번호); return; }
        입력파일 = -1; int báìtì_détà;
        while ((báìtì_détà = Kàá()) != 256 && báìtì_détà >= 0) { int 처리값 = ibi_ìpamọ́_Àwọn_fáìlì.Kọ(열린파일번호, báìtì_détà); if (처리값 < 0) { 명령해석기.àṣìṣe(처리값); break; } 보드.직렬쓰기(báìtì_détà); }
        ibi_ìpamọ́_Àwọn_fáìlì.Ti(열린파일번호);
    }
}
