// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 파이프는 16 KiB씩 순서대로 실행한다. 프로세스/동시 파이프를 흉내 내지 않는다. */
public final class 셸입출력 {
    static int[] 입력자료 = new int[16384], 출력자료 = new int[16384];
    static int 입력길이, 입력위치, 출력길이, file_input = -1, file_output = -1;
    static boolean 파이프입력, 파이프출력;
    static int kegagalan_VALUE;
    static boolean Perbolehkan_interaktif = true;
    public static int teknologi_informasi_interaktif() { return Perbolehkan_interaktif && file_input < 3 && file_output < 3 && !파이프입력 && !파이프출력 ? 1 : 0; }
    public static int keluaranTeks(int Saluran_VALUE, int VALUE) {
        if (Saluran_VALUE != 1) return 0;
        if (file_output >= 3) { int 처리값 = BerkasMemori.Tulis(file_output, VALUE); if (처리값 < 0) kegagalan_VALUE = 처리값; return 1; }
        if (!파이프출력) return 0;
        if (출력길이 == 출력자료.length) kegagalan_VALUE = -28;
        else 출력자료[출력길이++] = VALUE;
        return 1;
    }
    public static int 입력() {
        if (file_input >= 3) { int 처리값 = BerkasMemori.Baca(file_input); return 처리값 == 256 ? -2 : 처리값; }
        if (파이프입력) return 입력위치 < 입력길이 ? 입력자료[입력위치++] : -2;
        return -3; // UART로 Maju_VALUE
    }
    static void jalankan(boolean spasi_baris_pipa, boolean berikutnya_pipa) {
        파이프입력 = spasi_baris_pipa; 파이프출력 = berikutnya_pipa;
        입력위치 = 0; 출력길이 = 0; file_input = -1; file_output = -1; kegagalan_VALUE = 0;
    }
    static void 끝() {
        Papan.입출력전환(0);
        if (file_input >= 3) BerkasMemori.Tutup(file_input);
        if (file_output >= 3) BerkasMemori.Tutup(file_output);
        if (파이프출력) { 입력길이 = 출력길이; for (int Loop_INDEX = 0; Loop_INDEX < 출력길이; Loop_INDEX++) 입력자료[Loop_INDEX] = 출력자료[Loop_INDEX]; }
        file_input = -1; file_output = -1; 파이프입력 = false; 파이프출력 = false;
    }
}
