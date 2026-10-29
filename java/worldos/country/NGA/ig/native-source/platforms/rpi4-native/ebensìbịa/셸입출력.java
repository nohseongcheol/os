// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 파이프는 16 KiB씩 순서대로 실행한다. 프로세스/동시 파이프를 흉내 내지 않는다. */
public final class 셸입출력 {
    static int[] 입력자료 = new int[16384], 출력자료 = new int[16384];
    static int 입력길이, 입력위치, 출력길이, 입력파일 = -1, faịlụ_kènrụpụ = -1;
    static boolean 파이프입력, 파이프출력;
    static int ọdịdà_valuu;
    static boolean Kwère_kèmmekọrịta = true;
    public static int 대화가능() { return Kwère_kèmmekọrịta && 입력파일 < 3 && faịlụ_kènrụpụ < 3 && !파이프입력 && !파이프출력 ? 1 : 0; }
    public static int 출력(int ọwa_valuu, int valuu) {
        if (ọwa_valuu != 1) return 0;
        if (faịlụ_kènrụpụ >= 3) { int 처리값 = memọrị_Ndi_ọbọakwụkwọ.Chekwaa_ozi(faịlụ_kènrụpụ, valuu); if (처리값 < 0) ọdịdà_valuu = 처리값; return 1; }
        if (!파이프출력) return 0;
        if (출력길이 == 출력자료.length) ọdịdà_valuu = -28;
        else 출력자료[출력길이++] = valuu;
        return 1;
    }
    public static int 입력() {
        if (입력파일 >= 3) { int 처리값 = memọrị_Ndi_ọbọakwụkwọ.Wepụta_ọzi(입력파일); return 처리값 == 256 ? -2 : 처리값; }
        if (파이프입력) return 입력위치 < 입력길이 ? 입력자료[입력위치++] : -2;
        return -3; // UART로 zìgaā_valuu
    }
    static void Bido(boolean N_ebuụzọ_akàra_nkwụọtọ, boolean 뒤파이프) {
        파이프입력 = N_ebuụzọ_akàra_nkwụọtọ; 파이프출력 = 뒤파이프;
        입력위치 = 0; 출력길이 = 0; 입력파일 = -1; faịlụ_kènrụpụ = -1; ọdịdà_valuu = 0;
    }
    static void 끝() {
        보드.입출력전환(0);
        if (입력파일 >= 3) memọrị_Ndi_ọbọakwụkwọ.Mechie(입력파일);
        if (faịlụ_kènrụpụ >= 3) memọrị_Ndi_ọbọakwụkwọ.Mechie(faịlụ_kènrụpụ);
        if (파이프출력) { 입력길이 = 출력길이; for (int memmenwè_indèks = 0; memmenwè_indèks < 출력길이; memmenwè_indèks++) 입력자료[memmenwè_indèks] = 출력자료[memmenwè_indèks]; }
        입력파일 = -1; faịlụ_kènrụpụ = -1; 파이프입력 = false; 파이프출력 = false;
    }
}
