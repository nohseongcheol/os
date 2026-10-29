// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 apvalkalas 내장 Įrankiai. */
public final class apvalkalas_Įrankiai {
    static int[] duomenys = new int[16384];
    static int įvesties_failas = -1;
    static int kurti_Failas(int argumentas_INDEX, int Procesas_MODE) {
        int 처리값 = 명령해석기.KELIAS(argumentas_INDEX); return 처리값 < 0 ? 처리값 : atmintis_Failai.Atverti(Procesas_MODE);
    }
    static boolean 입력준비(int argumentas_INDEX) {
        įvesties_failas = -1;
        if (argumentas_INDEX < 명령해석기.žetonas_COUNT) {
            įvesties_failas = kurti_Failas(argumentas_INDEX, 0);
            if (įvesties_failas < 0) { 명령해석기.KLAIDA(įvesties_failas); return false; }
        }
        return true;
    }
    static int Skaitymas() {
        if (įvesties_failas >= 3) return atmintis_Failai.Skaitymas(įvesties_failas);
        while (true) {
            int baitas_duomenys = Lenta.직렬읽기(); if (baitas_duomenys == -2 || baitas_duomenys == 4) return 256;
            if (baitas_duomenys == 3) { 명령해석기.REZULTATAS = 130; return 256; }
            if (baitas_duomenys >= 0) return baitas_duomenys; Lenta.YIELD_CPU();
        }
    }
    static void Užverti() { if (įvesties_failas >= 3) atmintis_Failai.Užverti(įvesties_failas); įvesties_failas = -1; }
    static void rodyti_VALUE() {
        int 마지막자리 = 명령해석기.žetonas_COUNT == 1 ? 2 : 명령해석기.žetonas_COUNT;
        for (int argumentas_INDEX = 1; argumentas_INDEX < 마지막자리; argumentas_INDEX++) {
            if (!입력준비(argumentas_INDEX)) continue;
            int baitas_duomenys; while ((baitas_duomenys = Skaitymas()) != 256 && baitas_duomenys >= 0) Lenta.직렬쓰기(baitas_duomenys);
            if (baitas_duomenys < 0) 명령해석기.KLAIDA(baitas_duomenys); Užverti();
        }
    }
    static void Failas_Darbas(String gavinys_numeris) {
        if (명령해석기.žetonas_COUNT != 2) { 명령해석기.REZULTATAS = 2; 단말.Rašymas("사용법: mkdir/rmdir/touch Failas\n"); return; }
        int 처리값 = 명령해석기.KELIAS(1);
        if (처리값 >= 0) {
            if (gavinys_numeris.charAt(0) == 'm') 처리값 = atmintis_Failai.kurti_Katalogas();
            else if (gavinys_numeris.charAt(0) == 'r') 처리값 = atmintis_Failai.pašalinti_Katalogas();
            else { 처리값 = atmintis_Failai.Atverti(65); if (처리값 >= 3) 처리값 = atmintis_Failai.Užverti(처리값); }
        }
        if (처리값 < 0) 명령해석기.KLAIDA(처리값);
    }
    static void kopijuoti_VALUE(boolean 이동여부) {
        if (명령해석기.žetonas_COUNT != 3) { 명령해석기.REZULTATAS = 2; 단말.Rašymas("사용법: cp/mv 원본 vieta_dalyvis (Failas)\n"); return; }
        int 처리값 = 명령해석기.KELIAS(1); if (처리값 >= 0) 처리값 = atmintis_Failai.normalizuoti_VALUE();
        if (처리값 < 0) { 명령해석기.KLAIDA(처리값); return; }
        int 원본번호 = atmintis_Failai.FIND_įrašas(); if (원본번호 < 0) { 명령해석기.KLAIDA(-2); return; }
        int įrašas_COUNT = atmintis_Failai.길이[원본번호]; for (int Loop_INDEX = 0; Loop_INDEX < įrašas_COUNT; Loop_INDEX++) duomenys[Loop_INDEX] = atmintis_Failai.자료읽기(원본번호, Loop_INDEX);
        처리값 = 명령해석기.KELIAS(2); if (처리값 >= 0) 처리값 = atmintis_Failai.normalizuoti_VALUE();
        if (처리값 < 0) { 명령해석기.KLAIDA(처리값); return; }
        if (atmintis_Failai.FIND_įrašas() == 원본번호) { if (!이동여부) 명령해석기.KLAIDA(-22); return; }
        if (이동여부) { 처리값 = atmintis_Failai.Pervardyti_įrašas(원본번호); if (처리값 < 0) 명령해석기.KLAIDA(처리값); return; }
        int 열린파일번호 = atmintis_Failai.Atverti(577); if (열린파일번호 < 0) { 명령해석기.KLAIDA(열린파일번호); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < įrašas_COUNT; Loop_INDEX++) { 처리값 = atmintis_Failai.Rašymas(열린파일번호, duomenys[Loop_INDEX]); if (처리값 < 0) { 명령해석기.KLAIDA(처리값); break; } }
        atmintis_Failai.Užverti(열린파일번호);
    }
    static int skaitmuo_VALUE(int argumentas_INDEX) {
        if (argumentas_INDEX >= 명령해석기.žetonas_COUNT) return -1;
        int įrašas_COUNT = 0; for (int Loop_INDEX = 0; Loop_INDEX < 명령해석기.길이[argumentas_INDEX]; Loop_INDEX++) { int simbolio_kodas = 명령해석기.žetonas_VALUE[명령해석기.시작점[argumentas_INDEX] + Loop_INDEX]; if (simbolio_kodas < '0' || simbolio_kodas > '9' || įrašas_COUNT > 10000) return -1; įrašas_COUNT = įrašas_COUNT * 10 + simbolio_kodas - '0'; } return įrašas_COUNT;
    }
    static void 세기() {
        int argumentas_INDEX = 1, parinktis = 0;
        if (명령해석기.같음(1, "-c") || 명령해석기.같음(1, "-l") || 명령해석기.같음(1, "-w")) { parinktis = 명령해석기.같음(1, "-c") ? 1 : 명령해석기.같음(1, "-l") ? 2 : 3; argumentas_INDEX++; }
        if (명령해석기.žetonas_COUNT > argumentas_INDEX + 1) { 명령해석기.REZULTATAS = 2; 단말.Rašymas("사용법: wc [-c|-l|-w] [Failas]\n"); return; }
        if (!입력준비(argumentas_INDEX)) return;
        int baitas_COUNT = 0, 줄수 = 0, 낱말수 = 0, baitas_duomenys; boolean 낱말 = false;
        while ((baitas_duomenys = Skaitymas()) >= 0 && baitas_duomenys != 256) { baitas_COUNT++; if (baitas_duomenys == 10) 줄수++; boolean erdvė = baitas_duomenys == 32 || baitas_duomenys >= 9 && baitas_duomenys <= 13; if (!erdvė && !낱말) 낱말수++; 낱말 = !erdvė; }
        Užverti(); if (baitas_duomenys < 0) { 명령해석기.KLAIDA(baitas_duomenys); return; }
        if (parinktis != 0) 단말.numeris(parinktis == 1 ? baitas_COUNT : parinktis == 2 ? 줄수 : 낱말수);
        else { 단말.numeris(줄수); 단말.문자(' '); 단말.numeris(낱말수); 단말.문자(' '); 단말.numeris(baitas_COUNT); } 단말.문자(10);
    }
    static void FIND_įrašas() {
        if (명령해석기.žetonas_COUNT < 2 || 명령해석기.žetonas_COUNT > 3) { 명령해석기.REZULTATAS = 2; 단말.Rašymas("사용법: grep 찾을문구 [Failas]\n"); return; }
        if (!입력준비(2)) return;
        int įrašas_COUNT = 0, baitas_duomenys, 일치수 = 0;
        while (true) {
            baitas_duomenys = Skaitymas();
            if (baitas_duomenys == 10 || baitas_duomenys == 256 || baitas_duomenys < 0) {
                boolean 찾은여부 = false;
                for (int Loop_INDEX = 0; Loop_INDEX <= įrašas_COUNT - 명령해석기.길이[1]; Loop_INDEX++) {
                    boolean 같은여부 = true; for (int vidinis_padėtis = 0; vidinis_padėtis < 명령해석기.길이[1]; vidinis_padėtis++) if (duomenys[Loop_INDEX + vidinis_padėtis] != 명령해석기.žetonas_VALUE[명령해석기.시작점[1] + vidinis_padėtis]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (įrašas_COUNT > 0 || baitas_duomenys == 10)) { for (int Loop_INDEX = 0; Loop_INDEX < įrašas_COUNT; Loop_INDEX++) Lenta.직렬쓰기(duomenys[Loop_INDEX]); 단말.문자(10); 일치수++; }
                įrašas_COUNT = 0; if (baitas_duomenys != 10) break;
            } else if (įrašas_COUNT < duomenys.length) duomenys[įrašas_COUNT++] = baitas_duomenys;
            else { 명령해석기.KLAIDA(-28); Užverti(); return; }
        }
        Užverti(); if (baitas_duomenys < 0) 명령해석기.KLAIDA(baitas_duomenys); else if (명령해석기.REZULTATAS == 0) 명령해석기.REZULTATAS = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int argumentas_INDEX = 1, 줄수 = 10;
        if (명령해석기.같음(1, "-n")) { 줄수 = skaitmuo_VALUE(2); argumentas_INDEX = 3; }
        if (줄수 < 0 || 명령해석기.žetonas_COUNT > argumentas_INDEX + 1) { 명령해석기.REZULTATAS = 2; 단말.Rašymas("사용법: head/tail [-n 줄수] [Failas]\n"); return; }
        if (!입력준비(argumentas_INDEX)) return;
        int įrašas_COUNT = 0, baitas_duomenys;
        while ((baitas_duomenys = Skaitymas()) != 256 && baitas_duomenys >= 0) { if (įrašas_COUNT == duomenys.length) { 명령해석기.KLAIDA(-28); Užverti(); return; } duomenys[įrašas_COUNT++] = baitas_duomenys; }
        Užverti(); if (baitas_duomenys < 0) { 명령해석기.KLAIDA(baitas_duomenys); return; }
        int vietinis_Start = 0, baigti_pokalbį_padėtis = įrašas_COUNT;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int bendras_COUNT = 0; for (int Loop_INDEX = įrašas_COUNT - 2; Loop_INDEX >= 0; Loop_INDEX--) if (duomenys[Loop_INDEX] == 10 && ++bendras_COUNT == 줄수) { vietinis_Start = Loop_INDEX + 1; break; } }
        else { int bendras_COUNT = 0; for (int Loop_INDEX = 0; Loop_INDEX < įrašas_COUNT; Loop_INDEX++) if (duomenys[Loop_INDEX] == 10 && ++bendras_COUNT == 줄수) { baigti_pokalbį_padėtis = Loop_INDEX + 1; break; } }
        for (int Loop_INDEX = vietinis_Start; Loop_INDEX < baigti_pokalbį_padėtis; Loop_INDEX++) Lenta.직렬쓰기(duomenys[Loop_INDEX]);
    }
    static void rašymas_Dviese() {
        boolean sujungti = 명령해석기.같음(1, "-a"); int argumentas_INDEX = sujungti ? 2 : 1;
        if (명령해석기.žetonas_COUNT != argumentas_INDEX + 1) { 명령해석기.REZULTATAS = 2; 단말.Rašymas("사용법: tee [-a] Failas\n"); return; }
        int 열린파일번호 = kurti_Failas(argumentas_INDEX, sujungti ? 1089 : 577); if (열린파일번호 < 0) { 명령해석기.KLAIDA(열린파일번호); return; }
        įvesties_failas = -1; int baitas_duomenys;
        while ((baitas_duomenys = Skaitymas()) != 256 && baitas_duomenys >= 0) { int 처리값 = atmintis_Failai.Rašymas(열린파일번호, baitas_duomenys); if (처리값 < 0) { 명령해석기.KLAIDA(처리값); break; } Lenta.직렬쓰기(baitas_duomenys); }
        atmintis_Failai.Užverti(열린파일번호);
    }
}
