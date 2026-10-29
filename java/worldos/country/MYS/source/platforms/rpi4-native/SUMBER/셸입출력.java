// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 파이프는 16 KiB씩 순서대로 실행한다. 프로세스/동시 파이프를 흉내 내지 않는다. */
public final class 셸입출력 {
    static int[] 입력자료 = new int[16384], 출력자료 = new int[16384];
    static int 입력길이, 입력위치, 출력길이, fail_input = -1, 출력파일 = -1;
    static boolean 파이프입력, 파이프출력;
    static int kegagalan_VALUE;
    static boolean Izin_interaktif = true;
    public static int teknologi_maklumat_interaktif() { return Izin_interaktif && fail_input < 3 && 출력파일 < 3 && !파이프입력 && !파이프출력 ? 1 : 0; }
    public static int 출력(int Saluran_VALUE, int VALUE) {
        if (Saluran_VALUE != 1) return 0;
        if (출력파일 >= 3) { int 처리값 = Memori_Fail.Tulis(출력파일, VALUE); if (처리값 < 0) kegagalan_VALUE = 처리값; return 1; }
        if (!파이프출력) return 0;
        if (출력길이 == 출력자료.length) kegagalan_VALUE = -28;
        else 출력자료[출력길이++] = VALUE;
        return 1;
    }
    public static int 입력() {
        if (fail_input >= 3) { int 처리값 = Memori_Fail.Baca(fail_input); return 처리값 == 256 ? -2 : 처리값; }
        if (파이프입력) return 입력위치 < 입력길이 ? 입력자료[입력위치++] : -2;
        return -3; // UART로 Mara_VALUE
    }
    static void Jalan(boolean jarak_baris_paip, boolean 뒤파이프) {
        파이프입력 = jarak_baris_paip; 파이프출력 = 뒤파이프;
        입력위치 = 0; 출력길이 = 0; fail_input = -1; 출력파일 = -1; kegagalan_VALUE = 0;
    }
    static void 끝() {
        Papan.입출력전환(0);
        if (fail_input >= 3) Memori_Fail.Tutup(fail_input);
        if (출력파일 >= 3) Memori_Fail.Tutup(출력파일);
        if (파이프출력) { 입력길이 = 출력길이; for (int Loop_INDEX = 0; Loop_INDEX < 출력길이; Loop_INDEX++) 입력자료[Loop_INDEX] = 출력자료[Loop_INDEX]; }
        fail_input = -1; 출력파일 = -1; 파이프입력 = false; 파이프출력 = false;
    }
}
