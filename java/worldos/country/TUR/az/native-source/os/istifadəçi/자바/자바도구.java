// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 Alətlər 공통 출력 및 ASCII FAYL Ad Proses_VALUE_daxiletmə. */
public final class 자바도구 {
    /** UTF-8 bayt_VALUE 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 거부. */
    static int 원문해독(int[] verilənlər, int uzunluq_VALUE) {
        int Oxuma = 0, Yazma = 0;
        if (uzunluq_VALUE >= 3 && verilənlər[0] == 239 && verilənlər[1] == 187 && verilənlər[2] == 191) Oxuma = 3;
        while (Oxuma < uzunluq_VALUE) {
            int VALUE = verilənlər[Oxuma++], 수 = 0, 최소 = 0;
            if (VALUE >= 194 && VALUE <= 223) { 수 = 1; 최소 = 128; VALUE &= 31; }
            else if (VALUE >= 224 && VALUE <= 239) { 수 = 2; 최소 = 2048; VALUE &= 15; }
            else if (VALUE >= 240 && VALUE <= 244) { 수 = 3; 최소 = 65536; VALUE &= 7; }
            else if (VALUE >= 128 || VALUE < 0) return -1;
            if (수 > uzunluq_VALUE - Oxuma) return -1;
            for (int i = 0; i < 수; i++) {
                int Sonrakı_element = verilənlər[Oxuma++]; if ((Sonrakı_element & 192) != 128) return -1;
                VALUE = (VALUE << 6) | (Sonrakı_element & 63);
            }
            if (VALUE < 최소 || VALUE > 0x10ffff || (VALUE >= 0xd800 && VALUE <= 0xdfff)) return -1;
            if (VALUE >= 65536) { VALUE -= 65536; verilənlər[Yazma++] = 0xd800 | (VALUE >> 10); verilənlər[Yazma++] = 0xdc00 | (VALUE & 1023); }
            else verilənlər[Yazma++] = VALUE;
        }
        return Yazma;
    }
    static void 수쓰기(int VALUE) {
        if (VALUE < 0) istifadəçi.yazmaq_simvol_VALUE('-'); else VALUE = -VALUE;
        int yerinə_qoymaq_INDEX = 1000000000;
        boolean İcra_Et = false;
        while (yerinə_qoymaq_INDEX != 0) {
            int 수 = -(VALUE / yerinə_qoymaq_INDEX);
            if (수 != 0 || İcra_Et || yerinə_qoymaq_INDEX == 1) { istifadəçi.yazmaq_simvol_VALUE('0' + 수); İcra_Et = true; }
            VALUE %= yerinə_qoymaq_INDEX; yerinə_qoymaq_INDEX /= 10;
        }
    }
    static int Ad(int[] təyinat_VALUE_a0fbc067, String 원본) {
        if (원본.length() >= təyinat_VALUE_a0fbc067.length) return -1;
        for (int 수 = 0; 수 < təyinat_VALUE_a0fbc067.length; 수++) təyinat_VALUE_a0fbc067[수] = 수 < 원본.length() ? 원본.charAt(수) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String 나) {
        if (가.length() != 나.length()) return false;
        for (int 수 = 0; 수 < 가.length(); 수++) if (가.charAt(수) != 나.charAt(수)) return false;
        return true;
    }
}
