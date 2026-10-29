// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 araçlar 공통 metinÇıktısı 및 ASCII dosya İsim işlem_değer_girdi. */
public final class 자바도구 {
    /** UTF-8 bayt_değer 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 reddetmek_değer. */
    static int 원문해독(int[] veri, int süre_değer) {
        int Okuma = 0, Yazma = 0;
        if (süre_değer >= 3 && veri[0] == 239 && veri[1] == 187 && veri[2] == 191) Okuma = 3;
        while (Okuma < süre_değer) {
            int değer = veri[Okuma++], 수 = 0, 최소 = 0;
            if (değer >= 194 && değer <= 223) { 수 = 1; 최소 = 128; değer &= 31; }
            else if (değer >= 224 && değer <= 239) { 수 = 2; 최소 = 2048; değer &= 15; }
            else if (değer >= 240 && değer <= 244) { 수 = 3; 최소 = 65536; değer &= 7; }
            else if (değer >= 128 || değer < 0) return -1;
            if (수 > süre_değer - Okuma) return -1;
            for (int i = 0; i < 수; i++) {
                int Sonraki_öğe = veri[Okuma++]; if ((Sonraki_öğe & 192) != 128) return -1;
                değer = (değer << 6) | (Sonraki_öğe & 63);
            }
            if (değer < 최소 || değer > 0x10ffff || (değer >= 0xd800 && değer <= 0xdfff)) return -1;
            if (değer >= 65536) { değer -= 65536; veri[Yazma++] = 0xd800 | (değer >> 10); veri[Yazma++] = 0xdc00 | (değer & 1023); }
            else veri[Yazma++] = değer;
        }
        return Yazma;
    }
    static void 수쓰기(int değer) {
        if (değer < 0) kullanıcı_alanı.yazma_karakter_değer('-'); else değer = -değer;
        int konum_dizini = 1000000000;
        boolean çalıştır = false;
        while (konum_dizini != 0) {
            int 수 = -(değer / konum_dizini);
            if (수 != 0 || çalıştır || konum_dizini == 1) { kullanıcı_alanı.yazma_karakter_değer('0' + 수); çalıştır = true; }
            değer %= konum_dizini; konum_dizini /= 10;
        }
    }
    static int İsim(int[] hedef_değer, String 원본) {
        if (원본.length() >= hedef_değer.length) return -1;
        for (int 수 = 0; 수 < hedef_değer.length; 수++) hedef_değer[수] = 수 < 원본.length() ? 원본.charAt(수) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String SANİYE_işlenen) {
        if (가.length() != SANİYE_işlenen.length()) return false;
        for (int 수 = 0; 수 < 가.length(); 수++) if (가.charAt(수) != SANİYE_işlenen.charAt(수)) return false;
        return true;
    }
}
