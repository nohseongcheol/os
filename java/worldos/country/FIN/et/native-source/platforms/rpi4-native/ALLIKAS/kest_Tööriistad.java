// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 kest 내장 Tööriistad. */
public final class kest_Tööriistad {
    static int[] andmed = new int[16384];
    static int sisendfail = -1;
    static int avama_Fail(int argument_INDEX, int Joonis_MODE) {
        int 처리값 = 명령해석기.RADA(argument_INDEX); return 처리값 < 0 ? 처리값 : Mälu_Failid.Ava(Joonis_MODE);
    }
    static boolean 입력준비(int argument_INDEX) {
        sisendfail = -1;
        if (argument_INDEX < 명령해석기.luba_COUNT) {
            sisendfail = avama_Fail(argument_INDEX, 0);
            if (sisendfail < 0) { 명령해석기.VIGA(sisendfail); return false; }
        }
        return true;
    }
    static int Lugemine() {
        if (sisendfail >= 3) return Mälu_Failid.Lugemine(sisendfail);
        while (true) {
            int bait_andmed = Tahvel.직렬읽기(); if (bait_andmed == -2 || bait_andmed == 4) return 256;
            if (bait_andmed == 3) { 명령해석기.TULEMUS = 130; return 256; }
            if (bait_andmed >= 0) return bait_andmed; Tahvel.YIELD_CPU();
        }
    }
    static void Suletud() { if (sisendfail >= 3) Mälu_Failid.Suletud(sisendfail); sisendfail = -1; }
    static void Kuva_VALUE() {
        int 마지막자리 = 명령해석기.luba_COUNT == 1 ? 2 : 명령해석기.luba_COUNT;
        for (int argument_INDEX = 1; argument_INDEX < 마지막자리; argument_INDEX++) {
            if (!입력준비(argument_INDEX)) continue;
            int bait_andmed; while ((bait_andmed = Lugemine()) != 256 && bait_andmed >= 0) Tahvel.직렬쓰기(bait_andmed);
            if (bait_andmed < 0) 명령해석기.VIGA(bait_andmed); Suletud();
        }
    }
    static void Fail_Töö(String Toiming_number) {
        if (명령해석기.luba_COUNT != 2) { 명령해석기.TULEMUS = 2; 단말.Kirjutamine("사용법: mkdir/rmdir/touch Fail\n"); return; }
        int 처리값 = 명령해석기.RADA(1);
        if (처리값 >= 0) {
            if (Toiming_number.charAt(0) == 'm') 처리값 = Mälu_Failid.avama_kaust();
            else if (Toiming_number.charAt(0) == 'r') 처리값 = Mälu_Failid.eemaldama_kaust();
            else { 처리값 = Mälu_Failid.Ava(65); if (처리값 >= 3) 처리값 = Mälu_Failid.Suletud(처리값); }
        }
        if (처리값 < 0) 명령해석기.VIGA(처리값);
    }
    static void eksemplar_VALUE(boolean 이동여부) {
        if (명령해석기.luba_COUNT != 3) { 명령해석기.TULEMUS = 2; 단말.Kirjutamine("사용법: cp/mv 원본 sihtkoht_osaleja (Fail)\n"); return; }
        int 처리값 = 명령해석기.RADA(1); if (처리값 >= 0) 처리값 = Mälu_Failid.normaliseerima_VALUE();
        if (처리값 < 0) { 명령해석기.VIGA(처리값); return; }
        int 원본번호 = Mälu_Failid.FIND_kirje(); if (원본번호 < 0) { 명령해석기.VIGA(-2); return; }
        int kirje_COUNT = Mälu_Failid.길이[원본번호]; for (int Loop_INDEX = 0; Loop_INDEX < kirje_COUNT; Loop_INDEX++) andmed[Loop_INDEX] = Mälu_Failid.자료읽기(원본번호, Loop_INDEX);
        처리값 = 명령해석기.RADA(2); if (처리값 >= 0) 처리값 = Mälu_Failid.normaliseerima_VALUE();
        if (처리값 < 0) { 명령해석기.VIGA(처리값); return; }
        if (Mälu_Failid.FIND_kirje() == 원본번호) { if (!이동여부) 명령해석기.VIGA(-22); return; }
        if (이동여부) { 처리값 = Mälu_Failid.Nimeta_ümber_kirje(원본번호); if (처리값 < 0) 명령해석기.VIGA(처리값); return; }
        int 열린파일번호 = Mälu_Failid.Ava(577); if (열린파일번호 < 0) { 명령해석기.VIGA(열린파일번호); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < kirje_COUNT; Loop_INDEX++) { 처리값 = Mälu_Failid.Kirjutamine(열린파일번호, andmed[Loop_INDEX]); if (처리값 < 0) { 명령해석기.VIGA(처리값); break; } }
        Mälu_Failid.Suletud(열린파일번호);
    }
    static int number_VALUE(int argument_INDEX) {
        if (argument_INDEX >= 명령해석기.luba_COUNT) return -1;
        int kirje_COUNT = 0; for (int Loop_INDEX = 0; Loop_INDEX < 명령해석기.길이[argument_INDEX]; Loop_INDEX++) { int koodipunkt = 명령해석기.luba_VALUE_eb540501[명령해석기.시작점[argument_INDEX] + Loop_INDEX]; if (koodipunkt < '0' || koodipunkt > '9' || kirje_COUNT > 10000) return -1; kirje_COUNT = kirje_COUNT * 10 + koodipunkt - '0'; } return kirje_COUNT;
    }
    static void 세기() {
        int argument_INDEX = 1, 선택번호 = 0;
        if (명령해석기.같음(1, "-c") || 명령해석기.같음(1, "-l") || 명령해석기.같음(1, "-w")) { 선택번호 = 명령해석기.같음(1, "-c") ? 1 : 명령해석기.같음(1, "-l") ? 2 : 3; argument_INDEX++; }
        if (명령해석기.luba_COUNT > argument_INDEX + 1) { 명령해석기.TULEMUS = 2; 단말.Kirjutamine("사용법: wc [-c|-l|-w] [Fail]\n"); return; }
        if (!입력준비(argument_INDEX)) return;
        int bait_COUNT = 0, 줄수 = 0, 낱말수 = 0, bait_andmed; boolean 낱말 = false;
        while ((bait_andmed = Lugemine()) >= 0 && bait_andmed != 256) { bait_COUNT++; if (bait_andmed == 10) 줄수++; boolean ruum = bait_andmed == 32 || bait_andmed >= 9 && bait_andmed <= 13; if (!ruum && !낱말) 낱말수++; 낱말 = !ruum; }
        Suletud(); if (bait_andmed < 0) { 명령해석기.VIGA(bait_andmed); return; }
        if (선택번호 != 0) 단말.number(선택번호 == 1 ? bait_COUNT : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.number(줄수); 단말.문자(' '); 단말.number(낱말수); 단말.문자(' '); 단말.number(bait_COUNT); } 단말.문자(10);
    }
    static void FIND_kirje() {
        if (명령해석기.luba_COUNT < 2 || 명령해석기.luba_COUNT > 3) { 명령해석기.TULEMUS = 2; 단말.Kirjutamine("사용법: grep 찾을문구 [Fail]\n"); return; }
        if (!입력준비(2)) return;
        int kirje_COUNT = 0, bait_andmed, 일치수 = 0;
        while (true) {
            bait_andmed = Lugemine();
            if (bait_andmed == 10 || bait_andmed == 256 || bait_andmed < 0) {
                boolean 찾은여부 = false;
                for (int Loop_INDEX = 0; Loop_INDEX <= kirje_COUNT - 명령해석기.길이[1]; Loop_INDEX++) {
                    boolean 같은여부 = true; for (int sisemine_ametikoht = 0; sisemine_ametikoht < 명령해석기.길이[1]; sisemine_ametikoht++) if (andmed[Loop_INDEX + sisemine_ametikoht] != 명령해석기.luba_VALUE_eb540501[명령해석기.시작점[1] + sisemine_ametikoht]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (kirje_COUNT > 0 || bait_andmed == 10)) { for (int Loop_INDEX = 0; Loop_INDEX < kirje_COUNT; Loop_INDEX++) Tahvel.직렬쓰기(andmed[Loop_INDEX]); 단말.문자(10); 일치수++; }
                kirje_COUNT = 0; if (bait_andmed != 10) break;
            } else if (kirje_COUNT < andmed.length) andmed[kirje_COUNT++] = bait_andmed;
            else { 명령해석기.VIGA(-28); Suletud(); return; }
        }
        Suletud(); if (bait_andmed < 0) 명령해석기.VIGA(bait_andmed); else if (명령해석기.TULEMUS == 0) 명령해석기.TULEMUS = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int argument_INDEX = 1, 줄수 = 10;
        if (명령해석기.같음(1, "-n")) { 줄수 = number_VALUE(2); argument_INDEX = 3; }
        if (줄수 < 0 || 명령해석기.luba_COUNT > argument_INDEX + 1) { 명령해석기.TULEMUS = 2; 단말.Kirjutamine("사용법: head/tail [-n 줄수] [Fail]\n"); return; }
        if (!입력준비(argument_INDEX)) return;
        int kirje_COUNT = 0, bait_andmed;
        while ((bait_andmed = Lugemine()) != 256 && bait_andmed >= 0) { if (kirje_COUNT == andmed.length) { 명령해석기.VIGA(-28); Suletud(); return; } andmed[kirje_COUNT++] = bait_andmed; }
        Suletud(); if (bait_andmed < 0) { 명령해석기.VIGA(bait_andmed); return; }
        int kohalik_START = 0, lõpeta_kõne_ametikoht = kirje_COUNT;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int kokku_COUNT = 0; for (int Loop_INDEX = kirje_COUNT - 2; Loop_INDEX >= 0; Loop_INDEX--) if (andmed[Loop_INDEX] == 10 && ++kokku_COUNT == 줄수) { kohalik_START = Loop_INDEX + 1; break; } }
        else { int kokku_COUNT = 0; for (int Loop_INDEX = 0; Loop_INDEX < kirje_COUNT; Loop_INDEX++) if (andmed[Loop_INDEX] == 10 && ++kokku_COUNT == 줄수) { lõpeta_kõne_ametikoht = Loop_INDEX + 1; break; } }
        for (int Loop_INDEX = kohalik_START; Loop_INDEX < lõpeta_kõne_ametikoht; Loop_INDEX++) Tahvel.직렬쓰기(andmed[Loop_INDEX]);
    }
    static void 함께쓰기() {
        boolean Lisa = 명령해석기.같음(1, "-a"); int argument_INDEX = Lisa ? 2 : 1;
        if (명령해석기.luba_COUNT != argument_INDEX + 1) { 명령해석기.TULEMUS = 2; 단말.Kirjutamine("사용법: tee [-a] Fail\n"); return; }
        int 열린파일번호 = avama_Fail(argument_INDEX, Lisa ? 1089 : 577); if (열린파일번호 < 0) { 명령해석기.VIGA(열린파일번호); return; }
        sisendfail = -1; int bait_andmed;
        while ((bait_andmed = Lugemine()) != 256 && bait_andmed >= 0) { int 처리값 = Mälu_Failid.Kirjutamine(열린파일번호, bait_andmed); if (처리값 < 0) { 명령해석기.VIGA(처리값); break; } Tahvel.직렬쓰기(bait_andmed); }
        Mälu_Failid.Suletud(열린파일번호);
    }
}
