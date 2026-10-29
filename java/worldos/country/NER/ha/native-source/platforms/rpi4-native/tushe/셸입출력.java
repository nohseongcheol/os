// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 파이프는 16 KiB씩 순서대로 실행한다. 프로세스/동시 파이프를 흉내 내지 않는다. */
public final class 셸입출력 {
    static int[] 입력자료 = new int[16384], 출력자료 = new int[16384];
    static int 입력길이, 입력위치, 출력길이, 입력파일 = -1, makunshin_shirye_shiryen_da_aka_kirkira = -1;
    static boolean 파이프입력, 파이프출력;
    static int Kasa_aiki_Daraja;
    static boolean Bada_izini_Shigar_da_umarni_na_kwamfuta = true;
    public static int kimiyar_bayanai_Shigar_da_umarni_na_kwamfuta() { return Bada_izini_Shigar_da_umarni_na_kwamfuta && 입력파일 < 3 && makunshin_shirye_shiryen_da_aka_kirkira < 3 && !파이프입력 && !파이프출력 ? 1 : 0; }
    public static int 출력(int tasha_Daraja, int Daraja) {
        if (tasha_Daraja != 1) return 0;
        if (makunshin_shirye_shiryen_da_aka_kirkira >= 3) { int 처리값 = Mahardatar_kwamfuta_Fayiloli.Yi_Rubutu(makunshin_shirye_shiryen_da_aka_kirkira, Daraja); if (처리값 < 0) Kasa_aiki_Daraja = 처리값; return 1; }
        if (!파이프출력) return 0;
        if (출력길이 == 출력자료.length) Kasa_aiki_Daraja = -28;
        else 출력자료[출력길이++] = Daraja;
        return 1;
    }
    public static int 입력() {
        if (입력파일 >= 3) { int 처리값 = Mahardatar_kwamfuta_Fayiloli.Yi_Karatu(입력파일); return 처리값 == 256 ? -2 : 처리값; }
        if (파이프입력) return 입력위치 < 입력길이 ? 입력자료[입력위치++] : -2;
        return -3; // UART로 Ingiza_Daraja
    }
    static void Tafiyar_da(boolean Layin_Tazara_Bututu, boolean 뒤파이프) {
        파이프입력 = Layin_Tazara_Bututu; 파이프출력 = 뒤파이프;
        입력위치 = 0; 출력길이 = 0; 입력파일 = -1; makunshin_shirye_shiryen_da_aka_kirkira = -1; Kasa_aiki_Daraja = 0;
    }
    static void 끝() {
        보드.입출력전환(0);
        if (입력파일 >= 3) Mahardatar_kwamfuta_Fayiloli.Rufe(입력파일);
        if (makunshin_shirye_shiryen_da_aka_kirkira >= 3) Mahardatar_kwamfuta_Fayiloli.Rufe(makunshin_shirye_shiryen_da_aka_kirkira);
        if (파이프출력) { 입력길이 = 출력길이; for (int Warware_Indes = 0; Warware_Indes < 출력길이; Warware_Indes++) 입력자료[Warware_Indes] = 출력자료[Warware_Indes]; }
        입력파일 = -1; makunshin_shirye_shiryen_da_aka_kirkira = -1; 파이프입력 = false; 파이프출력 = false;
    }
}
