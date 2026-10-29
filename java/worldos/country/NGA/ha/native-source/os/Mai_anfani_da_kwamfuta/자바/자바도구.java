// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 Kaya 공통 출력 및 ASCII Fayil Suna haryar_aikin_na_ura_Daraja_Mashigar_bayanai. */
public final class 자바도구 {
    /** UTF-8 bayit_Daraja 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 kore_Daraja. */
    static int 원문해독(int[] Tarin_bayani, int Tsawo_Daraja) {
        int Yi_Karatu = 0, Yi_Rubutu = 0;
        if (Tsawo_Daraja >= 3 && Tarin_bayani[0] == 239 && Tarin_bayani[1] == 187 && Tarin_bayani[2] == 191) Yi_Karatu = 3;
        while (Yi_Karatu < Tsawo_Daraja) {
            int Daraja = Tarin_bayani[Yi_Karatu++], 수 = 0, 최소 = 0;
            if (Daraja >= 194 && Daraja <= 223) { 수 = 1; 최소 = 128; Daraja &= 31; }
            else if (Daraja >= 224 && Daraja <= 239) { 수 = 2; 최소 = 2048; Daraja &= 15; }
            else if (Daraja >= 240 && Daraja <= 244) { 수 = 3; 최소 = 65536; Daraja &= 7; }
            else if (Daraja >= 128 || Daraja < 0) return -1;
            if (수 > Tsawo_Daraja - Yi_Karatu) return -1;
            for (int i = 0; i < 수; i++) {
                int 다음 = Tarin_bayani[Yi_Karatu++]; if ((다음 & 192) != 128) return -1;
                Daraja = (Daraja << 6) | (다음 & 63);
            }
            if (Daraja < 최소 || Daraja > 0x10ffff || (Daraja >= 0xd800 && Daraja <= 0xdfff)) return -1;
            if (Daraja >= 65536) { Daraja -= 65536; Tarin_bayani[Yi_Rubutu++] = 0xd800 | (Daraja >> 10); Tarin_bayani[Yi_Rubutu++] = 0xdc00 | (Daraja & 1023); }
            else Tarin_bayani[Yi_Rubutu++] = Daraja;
        }
        return Yi_Rubutu;
    }
    static void 수쓰기(int Daraja) {
        if (Daraja < 0) Mai_anfani_da_kwamfuta.Rubuta_Harafi_Daraja('-'); else Daraja = -Daraja;
        int 자리 = 1000000000;
        boolean Tafiyar_da = false;
        while (자리 != 0) {
            int 수 = -(Daraja / 자리);
            if (수 != 0 || Tafiyar_da || 자리 == 1) { Mai_anfani_da_kwamfuta.Rubuta_Harafi_Daraja('0' + 수); Tafiyar_da = true; }
            Daraja %= 자리; 자리 /= 10;
        }
    }
    static int Suna(int[] Zangon_ƙarshe_Daraja, String 원본) {
        if (원본.length() >= Zangon_ƙarshe_Daraja.length) return -1;
        for (int 수 = 0; 수 < Zangon_ƙarshe_Daraja.length; 수++) Zangon_ƙarshe_Daraja[수] = 수 < 원본.length() ? 원본.charAt(수) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String 나) {
        if (가.length() != 나.length()) return false;
        for (int 수 = 0; 수 < 가.length(); 수++) if (가.charAt(수) != 나.charAt(수)) return false;
        return true;
    }
}
