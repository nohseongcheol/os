// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 nkọwannyemiwu 내장 Ngwaọrụ. */
public final class nkọwannyemiwu_Ngwaọrụ {
    static int[] datà = new int[16384];
    static int 입력파일 = -1;
    static int mepee_ọbọakwụkwọ(int agụment_indèks, int ùsòrò_moòdù) {
        int 처리값 = 명령해석기.ụzọ_ozi(agụment_indèks); return 처리값 < 0 ? 처리값 : memọrị_Ndi_ọbọakwụkwọ.Mepee(ùsòrò_moòdù);
    }
    static boolean 입력준비(int agụment_indèks) {
        입력파일 = -1;
        if (agụment_indèks < 명령해석기.토큰수) {
            입력파일 = mepee_ọbọakwụkwọ(agụment_indèks, 0);
            if (입력파일 < 0) { 명령해석기.mmejọ(입력파일); return false; }
        }
        return true;
    }
    static int Wepụta_ọzi() {
        if (입력파일 >= 3) return memọrị_Ndi_ọbọakwụkwọ.Wepụta_ọzi(입력파일);
        while (true) {
            int baịtị_datà = 보드.직렬읽기(); if (baịtị_datà == -2 || baịtị_datà == 4) return 256;
            if (baịtị_datà == 3) { 명령해석기.결과 = 130; return 256; }
            if (baịtị_datà >= 0) return baịtị_datà; 보드.kwụsịtụ_CPU();
        }
    }
    static void Mechie() { if (입력파일 >= 3) memọrị_Ndi_ọbọakwụkwọ.Mechie(입력파일); 입력파일 = -1; }
    static void lèe_valuu() {
        int 마지막자리 = 명령해석기.토큰수 == 1 ? 2 : 명령해석기.토큰수;
        for (int agụment_indèks = 1; agụment_indèks < 마지막자리; agụment_indèks++) {
            if (!입력준비(agụment_indèks)) continue;
            int baịtị_datà; while ((baịtị_datà = Wepụta_ọzi()) != 256 && baịtị_datà >= 0) 보드.직렬쓰기(baịtị_datà);
            if (baịtị_datà < 0) 명령해석기.mmejọ(baịtị_datà); Mechie();
        }
    }
    static void ọbọakwụkwọ_ọrụ(String 동작번호) {
        if (명령해석기.토큰수 != 2) { 명령해석기.결과 = 2; 단말.Chekwaa_ozi("사용법: mkdir/rmdir/touch Faịlụ\n"); return; }
        int 처리값 = 명령해석기.ụzọ_ozi(1);
        if (처리값 >= 0) {
            if (동작번호.charAt(0) == 'm') 처리값 = memọrị_Ndi_ọbọakwụkwọ.mepụta_dàịrektrị();
            else if (동작번호.charAt(0) == 'r') 처리값 = memọrị_Ndi_ọbọakwụkwọ.wepụ_dàịrektrị();
            else { 처리값 = memọrị_Ndi_ọbọakwụkwọ.Mepee(65); if (처리값 >= 3) 처리값 = memọrị_Ndi_ọbọakwụkwọ.Mechie(처리값); }
        }
        if (처리값 < 0) 명령해석기.mmejọ(처리값);
    }
    static void ṅomie_valuu(boolean 이동여부) {
        if (명령해석기.토큰수 != 3) { 명령해석기.결과 = 2; 단말.Chekwaa_ozi("사용법: cp/mv 원본 목적지 (Faịlụ)\n"); return; }
        int 처리값 = 명령해석기.ụzọ_ozi(1); if (처리값 >= 0) 처리값 = memọrị_Ndi_ọbọakwụkwọ.mèzima_valuu();
        if (처리값 < 0) { 명령해석기.mmejọ(처리값); return; }
        int 원본번호 = memọrị_Ndi_ọbọakwụkwọ.chọta_ndebà(); if (원본번호 < 0) { 명령해석기.mmejọ(-2); return; }
        int 항목수 = memọrị_Ndi_ọbọakwụkwọ.ogologo_valuu[원본번호]; for (int memmenwè_indèks = 0; memmenwè_indèks < 항목수; memmenwè_indèks++) datà[memmenwè_indèks] = memọrị_Ndi_ọbọakwụkwọ.자료읽기(원본번호, memmenwè_indèks);
        처리값 = 명령해석기.ụzọ_ozi(2); if (처리값 >= 0) 처리값 = memọrị_Ndi_ọbọakwụkwọ.mèzima_valuu();
        if (처리값 < 0) { 명령해석기.mmejọ(처리값); return; }
        if (memọrị_Ndi_ọbọakwụkwọ.chọta_ndebà() == 원본번호) { if (!이동여부) 명령해석기.mmejọ(-22); return; }
        if (이동여부) { 처리값 = memọrị_Ndi_ọbọakwụkwọ.이름바꾸기(원본번호); if (처리값 < 0) 명령해석기.mmejọ(처리값); return; }
        int 열린파일번호 = memọrị_Ndi_ọbọakwụkwọ.Mepee(577); if (열린파일번호 < 0) { 명령해석기.mmejọ(열린파일번호); return; }
        for (int memmenwè_indèks = 0; memmenwè_indèks < 항목수; memmenwè_indèks++) { 처리값 = memọrị_Ndi_ọbọakwụkwọ.Chekwaa_ozi(열린파일번호, datà[memmenwè_indèks]); if (처리값 < 0) { 명령해석기.mmejọ(처리값); break; } }
        memọrị_Ndi_ọbọakwụkwọ.Mechie(열린파일번호);
    }
    static int ọbula_valuu(int agụment_indèks) {
        if (agụment_indèks >= 명령해석기.토큰수) return -1;
        int 항목수 = 0; for (int memmenwè_indèks = 0; memmenwè_indèks < 명령해석기.ogologo_valuu[agụment_indèks]; memmenwè_indèks++) { int koòdù_nkeakàrà = 명령해석기.akara_valuu_eb540501[명령해석기.시작점[agụment_indèks] + memmenwè_indèks]; if (koòdù_nkeakàrà < '0' || koòdù_nkeakàrà > '9' || 항목수 > 10000) return -1; 항목수 = 항목수 * 10 + koòdù_nkeakàrà - '0'; } return 항목수;
    }
    static void 세기() {
        int agụment_indèks = 1, 선택번호 = 0;
        if (명령해석기.같음(1, "-c") || 명령해석기.같음(1, "-l") || 명령해석기.같음(1, "-w")) { 선택번호 = 명령해석기.같음(1, "-c") ? 1 : 명령해석기.같음(1, "-l") ? 2 : 3; agụment_indèks++; }
        if (명령해석기.토큰수 > agụment_indèks + 1) { 명령해석기.결과 = 2; 단말.Chekwaa_ozi("사용법: wc [-c|-l|-w] [Faịlụ]\n"); return; }
        if (!입력준비(agụment_indèks)) return;
        int 바이트수 = 0, 줄수 = 0, 낱말수 = 0, baịtị_datà; boolean 낱말 = false;
        while ((baịtị_datà = Wepụta_ọzi()) >= 0 && baịtị_datà != 256) { 바이트수++; if (baịtị_datà == 10) 줄수++; boolean ohere = baịtị_datà == 32 || baịtị_datà >= 9 && baịtị_datà <= 13; if (!ohere && !낱말) 낱말수++; 낱말 = !ohere; }
        Mechie(); if (baịtị_datà < 0) { 명령해석기.mmejọ(baịtị_datà); return; }
        if (선택번호 != 0) 단말.수(선택번호 == 1 ? 바이트수 : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.수(줄수); 단말.문자(' '); 단말.수(낱말수); 단말.문자(' '); 단말.수(바이트수); } 단말.문자(10);
    }
    static void chọta_ndebà() {
        if (명령해석기.토큰수 < 2 || 명령해석기.토큰수 > 3) { 명령해석기.결과 = 2; 단말.Chekwaa_ozi("사용법: grep 찾을문구 [Faịlụ]\n"); return; }
        if (!입력준비(2)) return;
        int 항목수 = 0, baịtị_datà, 일치수 = 0;
        while (true) {
            baịtị_datà = Wepụta_ọzi();
            if (baịtị_datà == 10 || baịtị_datà == 256 || baịtị_datà < 0) {
                boolean 찾은여부 = false;
                for (int memmenwè_indèks = 0; memmenwè_indèks <= 항목수 - 명령해석기.ogologo_valuu[1]; memmenwè_indèks++) {
                    boolean 같은여부 = true; for (int 안쪽자리 = 0; 안쪽자리 < 명령해석기.ogologo_valuu[1]; 안쪽자리++) if (datà[memmenwè_indèks + 안쪽자리] != 명령해석기.akara_valuu_eb540501[명령해석기.시작점[1] + 안쪽자리]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (항목수 > 0 || baịtị_datà == 10)) { for (int memmenwè_indèks = 0; memmenwè_indèks < 항목수; memmenwè_indèks++) 보드.직렬쓰기(datà[memmenwè_indèks]); 단말.문자(10); 일치수++; }
                항목수 = 0; if (baịtị_datà != 10) break;
            } else if (항목수 < datà.length) datà[항목수++] = baịtị_datà;
            else { 명령해석기.mmejọ(-28); Mechie(); return; }
        }
        Mechie(); if (baịtị_datà < 0) 명령해석기.mmejọ(baịtị_datà); else if (명령해석기.결과 == 0) 명령해석기.결과 = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int agụment_indèks = 1, 줄수 = 10;
        if (명령해석기.같음(1, "-n")) { 줄수 = ọbula_valuu(2); agụment_indèks = 3; }
        if (줄수 < 0 || 명령해석기.토큰수 > agụment_indèks + 1) { 명령해석기.결과 = 2; 단말.Chekwaa_ozi("사용법: head/tail [-n 줄수] [Faịlụ]\n"); return; }
        if (!입력준비(agụment_indèks)) return;
        int 항목수 = 0, baịtị_datà;
        while ((baịtị_datà = Wepụta_ọzi()) != 256 && baịtị_datà >= 0) { if (항목수 == datà.length) { 명령해석기.mmejọ(-28); Mechie(); return; } datà[항목수++] = baịtị_datà; }
        Mechie(); if (baịtị_datà < 0) { 명령해석기.mmejọ(baịtị_datà); return; }
        int otù_ebe_Mbido = 0, 끝자리 = 항목수;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int 총수 = 0; for (int memmenwè_indèks = 항목수 - 2; memmenwè_indèks >= 0; memmenwè_indèks--) if (datà[memmenwè_indèks] == 10 && ++총수 == 줄수) { otù_ebe_Mbido = memmenwè_indèks + 1; break; } }
        else { int 총수 = 0; for (int memmenwè_indèks = 0; memmenwè_indèks < 항목수; memmenwè_indèks++) if (datà[memmenwè_indèks] == 10 && ++총수 == 줄수) { 끝자리 = memmenwè_indèks + 1; break; } }
        for (int memmenwè_indèks = otù_ebe_Mbido; memmenwè_indèks < 끝자리; memmenwè_indèks++) 보드.직렬쓰기(datà[memmenwè_indèks]);
    }
    static void 함께쓰기() {
        boolean 덧붙임여부 = 명령해석기.같음(1, "-a"); int agụment_indèks = 덧붙임여부 ? 2 : 1;
        if (명령해석기.토큰수 != agụment_indèks + 1) { 명령해석기.결과 = 2; 단말.Chekwaa_ozi("사용법: tee [-a] Faịlụ\n"); return; }
        int 열린파일번호 = mepee_ọbọakwụkwọ(agụment_indèks, 덧붙임여부 ? 1089 : 577); if (열린파일번호 < 0) { 명령해석기.mmejọ(열린파일번호); return; }
        입력파일 = -1; int baịtị_datà;
        while ((baịtị_datà = Wepụta_ọzi()) != 256 && baịtị_datà >= 0) { int 처리값 = memọrị_Ndi_ọbọakwụkwọ.Chekwaa_ozi(열린파일번호, baịtị_datà); if (처리값 < 0) { 명령해석기.mmejọ(처리값); break; } 보드.직렬쓰기(baịtị_datà); }
        memọrị_Ndi_ọbọakwụkwọ.Mechie(열린파일번호);
    }
}
