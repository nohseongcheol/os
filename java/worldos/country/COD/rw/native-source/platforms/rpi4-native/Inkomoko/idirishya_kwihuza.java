// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 insomamabwiriza imimerere_agaciro. Idosiye 저장소는 공유하고 Inzira/변수/kubika_umurongo/입력은 분리한다. */
public final class idirishya_kwihuza {
    static int[] 보관 = new int[4 * 30000], Gutegura = new int[4];
    static int 현재, 위치;
    static boolean 이어읽기;
    static void ARRAY_agaciro(int[] amakurushingiro, boolean Store_agaciro) {
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < amakurushingiro.length; gukora_mu_matsinda_umugerekashakiro++) { if (Store_agaciro) 보관[위치++] = amakurushingiro[gukora_mu_matsinda_umugerekashakiro]; else amakurushingiro[gukora_mu_matsinda_umugerekashakiro] = 보관[위치++]; }
    }
    static int agaciro(int amakurushingiro_agaciro, boolean 저장여부) { if (저장여부) { 보관[위치++] = amakurushingiro_agaciro; return amakurushingiro_agaciro; } return 보관[위치++]; }
    static void 옮기기(int 보관칸, boolean 저장여부) {
        위치 = 보관칸 * 30000;
        ARRAY_agaciro(ububiko_Dosiye.현재, 저장여부); ububiko_Dosiye.현재길이 = agaciro(ububiko_Dosiye.현재길이, 저장여부);
        ARRAY_agaciro(insomamabwiriza_interuro.변수이름, 저장여부); ARRAY_agaciro(insomamabwiriza_interuro.변수값, 저장여부); ARRAY_agaciro(insomamabwiriza_interuro.이름길이, 저장여부); ARRAY_agaciro(insomamabwiriza_interuro.agaciro_uburebure, 저장여부);
        insomamabwiriza_interuro.imimerere_agaciro = agaciro(insomamabwiriza_interuro.imimerere_agaciro, 저장여부);
        ARRAY_agaciro(umurongo_Muhindura.kubika_umurongo, 저장여부); ARRAY_agaciro(umurongo_Muhindura.kubika_uburebure, 저장여부); ARRAY_agaciro(umurongo_Muhindura.Store_agaciro, 저장여부); ARRAY_agaciro(명령해석기.umurongo, 저장여부);
        umurongo_Muhindura.기록수 = agaciro(umurongo_Muhindura.기록수, 저장여부); umurongo_Muhindura.kubika_umurongo_kurangiza = agaciro(umurongo_Muhindura.kubika_umurongo_kurangiza, 저장여부);
        umurongo_Muhindura.Gushaka_agaciro = agaciro(umurongo_Muhindura.Gushaka_agaciro, 저장여부); umurongo_Muhindura.저장길이 = agaciro(umurongo_Muhindura.저장길이, 저장여부);
        umurongo_Muhindura.Ingano = agaciro(umurongo_Muhindura.Ingano, 저장여부); umurongo_Muhindura.inyoboranyandika_agaciro = agaciro(umurongo_Muhindura.inyoboranyandika_agaciro, 저장여부); umurongo_Muhindura.Itangira_idirishya = agaciro(umurongo_Muhindura.Itangira_idirishya, 저장여부);
        Gutegura[보관칸] = 1;
    }
    static void Inzira_agaciro_icyinjizwa() {
        int 사건번호 = 보드.터미널(12); if (사건번호 == 0) return;
        옮기기(현재, true);
        for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 4; gukora_mu_matsinda_umugerekashakiro++) {
            if ((사건번호 & (1 << (8 + gukora_mu_matsinda_umugerekashakiro))) != 0) { 보드.icunga_ukoresha_porogaramu(32 + gukora_mu_matsinda_umugerekashakiro); Gutegura[gukora_mu_matsinda_umugerekashakiro] = 0; }
            if ((사건번호 & (1 << (4 + gukora_mu_matsinda_umugerekashakiro))) != 0 && gukora_mu_matsinda_umugerekashakiro != 현재) Gutegura[gukora_mu_matsinda_umugerekashakiro] = 0;
        }
        int 다음자리 = (사건번호 & 15) - 1; if (다음자리 < 0) 다음자리 = 0;
        if (Gutegura[다음자리] == 0) for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 30000; gukora_mu_matsinda_umugerekashakiro++) 보관[다음자리 * 30000 + gukora_mu_matsinda_umugerekashakiro] = 0;
        현재 = 다음자리; 옮기기(현재, false); 보드.터미널(100 + 현재); 이어읽기 = true;
        단말.kwandika("\nTERMINAL FOCUS "); 단말.수(현재 + 1); 단말.문자(10);
    }
    static boolean 재개() {
        if (보드.icunga_ukoresha_porogaramu(16 + 현재) == 0) return false;
        셸입출력.Kwemerera_interfacebikorana = true; 셸입출력.ihuriro(false, false); 보드.입출력전환(1);
        int 처리값 = 보드.icunga_ukoresha_porogaramu(현재); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; insomamabwiriza_interuro.imimerere_agaciro = 처리값 < 0 ? 126 : 처리값; 단말.kwandika("exit "); 단말.수(처리값); 단말.문자(10); 보드.터미널(3); }
        return true;
    }
}
