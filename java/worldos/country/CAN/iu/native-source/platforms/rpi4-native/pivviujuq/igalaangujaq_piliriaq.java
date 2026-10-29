// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 piqujijjutiliriji qanuilinganiq_atuutilik. ini 저장소는 공유하고 aqqut/변수/papattivik_sanimukutaak/입력은 분리한다. */
public final class igalaangujaq_piliriaq {
    static int[] 보관 = new int[4 * 30000], Parnalli = new int[4];
    static int 현재, 위치;
    static boolean 이어읽기;
    static void array_atuutilik(int[] titiqqat, boolean tuqqurli_atuutilik) {
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < titiqqat.length; piliqqittaajuq_nalunaiqsimavik++) { if (tuqqurli_atuutilik) 보관[위치++] = titiqqat[piliqqittaajuq_nalunaiqsimavik]; else titiqqat[piliqqittaajuq_nalunaiqsimavik] = 보관[위치++]; }
    }
    static int atuutilik(int titiqqat_atuutilik, boolean 저장여부) { if (저장여부) { 보관[위치++] = titiqqat_atuutilik; return titiqqat_atuutilik; } return 보관[위치++]; }
    static void 옮기기(int 보관칸, boolean 저장여부) {
        위치 = 보관칸 * 30000;
        array_atuutilik(기억파일.현재, 저장여부); 기억파일.현재길이 = atuutilik(기억파일.현재길이, 저장여부);
        array_atuutilik(piqujijjutiliriji_syntax.변수이름, 저장여부); array_atuutilik(piqujijjutiliriji_syntax.변수값, 저장여부); array_atuutilik(piqujijjutiliriji_syntax.이름길이, 저장여부); array_atuutilik(piqujijjutiliriji_syntax.atuutilik_takininga, 저장여부);
        piqujijjutiliriji_syntax.qanuilinganiq_atuutilik = atuutilik(piqujijjutiliriji_syntax.qanuilinganiq_atuutilik, 저장여부);
        array_atuutilik(titikutaak_aaqqigiariji.papattivik_sanimukutaak, 저장여부); array_atuutilik(titikutaak_aaqqigiariji.papattivik_takininga, 저장여부); array_atuutilik(titikutaak_aaqqigiariji.tuqqurli_atuutilik, 저장여부); array_atuutilik(명령해석기.titikutaak, 저장여부);
        titikutaak_aaqqigiariji.기록수 = atuutilik(titikutaak_aaqqigiariji.기록수, 저장여부); titikutaak_aaqqigiariji.papattivik_sanimukutaak_isulittuq = atuutilik(titikutaak_aaqqigiariji.papattivik_sanimukutaak_isulittuq, 저장여부);
        titikutaak_aaqqigiariji.Qinirli_atuutilik = atuutilik(titikutaak_aaqqigiariji.Qinirli_atuutilik, 저장여부); titikutaak_aaqqigiariji.저장길이 = atuutilik(titikutaak_aaqqigiariji.저장길이, 저장여부);
        titikutaak_aaqqigiariji.anininga = atuutilik(titikutaak_aaqqigiariji.anininga, 저장여부); titikutaak_aaqqigiariji.pigiarut_atuutilik = atuutilik(titikutaak_aaqqigiariji.pigiarut_atuutilik, 저장여부); titikutaak_aaqqigiariji.pigiarli_igalaangujaq = atuutilik(titikutaak_aaqqigiariji.pigiarli_igalaangujaq, 저장여부);
        Parnalli[보관칸] = 1;
    }
    static void Pivallianiq_atuutilik_Iliniku() {
        int 사건번호 = 보드.터미널(12); if (사건번호 == 0) return;
        옮기기(현재, true);
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 4; piliqqittaajuq_nalunaiqsimavik++) {
            if ((사건번호 & (1 << (8 + piliqqittaajuq_nalunaiqsimavik))) != 0) { 보드.aulattivik_atuqtuq_pilirijjut(32 + piliqqittaajuq_nalunaiqsimavik); Parnalli[piliqqittaajuq_nalunaiqsimavik] = 0; }
            if ((사건번호 & (1 << (4 + piliqqittaajuq_nalunaiqsimavik))) != 0 && piliqqittaajuq_nalunaiqsimavik != 현재) Parnalli[piliqqittaajuq_nalunaiqsimavik] = 0;
        }
        int 다음자리 = (사건번호 & 15) - 1; if (다음자리 < 0) 다음자리 = 0;
        if (Parnalli[다음자리] == 0) for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 30000; piliqqittaajuq_nalunaiqsimavik++) 보관[다음자리 * 30000 + piliqqittaajuq_nalunaiqsimavik] = 0;
        현재 = 다음자리; 옮기기(현재, false); 보드.터미널(100 + 현재); 이어읽기 = true;
        단말.titiraq("\nTERMINAL FOCUS "); 단말.수(현재 + 1); 단말.문자(10);
    }
    static boolean 재개() {
        if (보드.aulattivik_atuqtuq_pilirijjut(16 + 현재) == 0) return false;
        셸입출력.Pijunnaqtilli_ilaliujjarvilik = true; 셸입출력.시작(false, false); 보드.입출력전환(1);
        int 처리값 = 보드.aulattivik_atuqtuq_pilirijjut(현재); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; piqujijjutiliriji_syntax.qanuilinganiq_atuutilik = 처리값 < 0 ? 126 : 처리값; 단말.titiraq("exit "); 단말.수(처리값); 단말.문자(10); 보드.터미널(3); }
        return true;
    }
}
