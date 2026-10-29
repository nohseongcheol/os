// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 alat 공통 출력 및 ASCII Fail Nama Proses_VALUE_pemasukan. */
public final class 자바도구 {
    /** UTF-8 bait_VALUE 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 tolak_VALUE. */
    static int 원문해독(int[] data, int kepanjangan_VALUE) {
        int Baca = 0, Tulis = 0;
        if (kepanjangan_VALUE >= 3 && data[0] == 239 && data[1] == 187 && data[2] == 191) Baca = 3;
        while (Baca < kepanjangan_VALUE) {
            int VALUE = data[Baca++], 수 = 0, 최소 = 0;
            if (VALUE >= 194 && VALUE <= 223) { 수 = 1; 최소 = 128; VALUE &= 31; }
            else if (VALUE >= 224 && VALUE <= 239) { 수 = 2; 최소 = 2048; VALUE &= 15; }
            else if (VALUE >= 240 && VALUE <= 244) { 수 = 3; 최소 = 65536; VALUE &= 7; }
            else if (VALUE >= 128 || VALUE < 0) return -1;
            if (수 > kepanjangan_VALUE - Baca) return -1;
            for (int i = 0; i < 수; i++) {
                int Seterusnya_item = data[Baca++]; if ((Seterusnya_item & 192) != 128) return -1;
                VALUE = (VALUE << 6) | (Seterusnya_item & 63);
            }
            if (VALUE < 최소 || VALUE > 0x10ffff || (VALUE >= 0xd800 && VALUE <= 0xdfff)) return -1;
            if (VALUE >= 65536) { VALUE -= 65536; data[Tulis++] = 0xd800 | (VALUE >> 10); data[Tulis++] = 0xdc00 | (VALUE & 1023); }
            else data[Tulis++] = VALUE;
        }
        return Tulis;
    }
    static void 수쓰기(int VALUE) {
        if (VALUE < 0) ruang_pengguna.tulis_aksara_VALUE('-'); else VALUE = -VALUE;
        int jawatan_INDEX = 1000000000;
        boolean Jalan = false;
        while (jawatan_INDEX != 0) {
            int 수 = -(VALUE / jawatan_INDEX);
            if (수 != 0 || Jalan || jawatan_INDEX == 1) { ruang_pengguna.tulis_aksara_VALUE('0' + 수); Jalan = true; }
            VALUE %= jawatan_INDEX; jawatan_INDEX /= 10;
        }
    }
    static int Nama(int[] destinasi_VALUE, String 원본) {
        if (원본.length() >= destinasi_VALUE.length) return -1;
        for (int 수 = 0; 수 < destinasi_VALUE.length; 수++) destinasi_VALUE[수] = 수 < 원본.length() ? 원본.charAt(수) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String 나) {
        if (가.length() != 나.length()) return false;
        for (int 수 = 0; 수 < 가.length(); 수++) if (가.charAt(수) != 나.charAt(수)) return false;
        return true;
    }
}
