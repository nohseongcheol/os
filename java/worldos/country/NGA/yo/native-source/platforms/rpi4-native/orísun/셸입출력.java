// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 파이프는 16 KiB씩 순서대로 실행한다. 프로세스/동시 파이프를 흉내 내지 않는다. */
public final class 셸입출력 {
    static int[] 입력자료 = new int[16384], 출력자료 = new int[16384];
    static int 입력길이, 입력위치, 출력길이, 입력파일 = -1, fáìlì_ìgbéjáde = -1;
    static boolean 파이프입력, 파이프출력;
    static int ìkùnà_iye;
    static boolean Fún_Lááyè_ìjọṣepọ̀ = true;
    public static int 대화가능() { return Fún_Lááyè_ìjọṣepọ̀ && 입력파일 < 3 && fáìlì_ìgbéjáde < 3 && !파이프입력 && !파이프출력 ? 1 : 0; }
    public static int 출력(int òpónà_iye, int iye) {
        if (òpónà_iye != 1) return 0;
        if (fáìlì_ìgbéjáde >= 3) { int 처리값 = ibi_ìpamọ́_Àwọn_fáìlì.Kọ(fáìlì_ìgbéjáde, iye); if (처리값 < 0) ìkùnà_iye = 처리값; return 1; }
        if (!파이프출력) return 0;
        if (출력길이 == 출력자료.length) ìkùnà_iye = -28;
        else 출력자료[출력길이++] = iye;
        return 1;
    }
    public static int 입력() {
        if (입력파일 >= 3) { int 처리값 = ibi_ìpamọ́_Àwọn_fáìlì.Kàá(입력파일); return 처리값 == 256 ? -2 : 처리값; }
        if (파이프입력) return 입력위치 < 입력길이 ? 입력자료[입력위치++] : -2;
        return -3; // UART로 tari_sí_iye
    }
    static void Rọ́ọ̀nù(boolean ìṣáájú_ÌLÀ_OLÓÒRÓ, boolean 뒤파이프) {
        파이프입력 = ìṣáájú_ÌLÀ_OLÓÒRÓ; 파이프출력 = 뒤파이프;
        입력위치 = 0; 출력길이 = 0; 입력파일 = -1; fáìlì_ìgbéjáde = -1; ìkùnà_iye = 0;
    }
    static void 끝() {
        보드.입출력전환(0);
        if (입력파일 >= 3) ibi_ìpamọ́_Àwọn_fáìlì.Ti(입력파일);
        if (fáìlì_ìgbéjáde >= 3) ibi_ìpamọ́_Àwọn_fáìlì.Ti(fáìlì_ìgbéjáde);
        if (파이프출력) { 입력길이 = 출력길이; for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 출력길이; ṣetúnṣe_wá_atọ̀ka_àkóónú++) 입력자료[ṣetúnṣe_wá_atọ̀ka_àkóónú] = 출력자료[ṣetúnṣe_wá_atọ̀ka_àkóónú]; }
        입력파일 = -1; fáìlì_ìgbéjáde = -1; 파이프입력 = false; 파이프출력 = false;
    }
}
