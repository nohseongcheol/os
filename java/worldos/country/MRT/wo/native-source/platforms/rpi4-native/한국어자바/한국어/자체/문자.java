// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 문자(文字), nëbbin_ci_lim_xëyma(符號): UTF-8 바이트와 UTF-16 문자열의 변환. yonnal_xëyma/조합 입력기는 별개다. */
public final class 문자 {
    public static int 바이트수(byte[] mbir) { return mbir.length; }
    private 문자() {}
    public static int diir_xëyma(String Tekst) { return Tekst.length(); }
    public static boolean 같음(String 앞, String woñeeku_xëyma) { return 앞 == null ? woñeeku_xëyma == null : 앞.equals(woñeeku_xëyma); }
    public static String Taf_SMS(String 앞, String woñeeku_xëyma) { return 앞.concat(woñeeku_xëyma); }
    public static String dogandi_xëyma(String Tekst, int daw, int 끝) { return Tekst.substring(daw, 끝); }
    public static int Segg_lëmm(String Tekst) { try { return Integer.parseInt(Tekst); } catch (NumberFormatException njumte) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String biir_lëmm_xëyma(int 수) { return Integer.toString(수); }
    public static int 코드포인트수(String Tekst) {
        int 수 = 0;
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < Tekst.length(); wërngël_àlluwa_tur++, 수++) {
            int kotu_araf = Tekst.charAt(wërngël_àlluwa_tur);
            if (kotu_araf >= 0xd800 && kotu_araf <= 0xdbff && wërngël_àlluwa_tur + 1 < Tekst.length() && Tekst.charAt(wërngël_àlluwa_tur + 1) >= 0xdc00 && Tekst.charAt(wërngël_àlluwa_tur + 1) <= 0xdfff) wërngël_àlluwa_tur++;
        }
        return 수;
    }
    public static byte[] 부호화(String Tekst) {
        byte[] 임시 = new byte[Tekst.length() * 3]; int 쓴수 = 0;
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < Tekst.length(); wërngël_àlluwa_tur++) {
            int kotu_araf = Tekst.charAt(wërngël_àlluwa_tur);
            if (kotu_araf >= 0xd800 && kotu_araf <= 0xdbff && wërngël_àlluwa_tur + 1 < Tekst.length() && Tekst.charAt(wërngël_àlluwa_tur + 1) >= 0xdc00 && Tekst.charAt(wërngël_àlluwa_tur + 1) <= 0xdfff) kotu_araf = 0x10000 + ((kotu_araf - 0xd800) << 10) + Tekst.charAt(++wërngël_àlluwa_tur) - 0xdc00;
            else if (kotu_araf >= 0xd800 && kotu_araf <= 0xdfff) kotu_araf = '?';
            if (kotu_araf < 128) 임시[쓴수++] = (byte)kotu_araf;
            else if (kotu_araf < 2048) { 임시[쓴수++] = (byte)(192 | kotu_araf >> 6); 임시[쓴수++] = (byte)(128 | kotu_araf & 63); }
            else if (kotu_araf < 65536) { 임시[쓴수++] = (byte)(224 | kotu_araf >> 12); 임시[쓴수++] = (byte)(128 | kotu_araf >> 6 & 63); 임시[쓴수++] = (byte)(128 | kotu_araf & 63); }
            else { 임시[쓴수++] = (byte)(240 | kotu_araf >> 18); 임시[쓴수++] = (byte)(128 | kotu_araf >> 12 & 63); 임시[쓴수++] = (byte)(128 | kotu_araf >> 6 & 63); 임시[쓴수++] = (byte)(128 | kotu_araf & 63); }
        }
        byte[] 결과 = new byte[쓴수]; System.arraycopy(임시, 0, 결과, 0, 쓴수); return 결과;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String fecci_mbir(byte[] okte_xëyma) {
        StringBuilder 결과 = new StringBuilder();
        for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < okte_xëyma.length;) {
            int kotu_araf = okte_xëyma[wërngël_àlluwa_tur++] & 255, 수 = kotu_araf < 128 ? 0 : kotu_araf >= 194 && kotu_araf < 224 ? 1 : kotu_araf >= 224 && kotu_araf < 240 ? 2 : kotu_araf >= 240 && kotu_araf <= 244 ? 3 : -1;
            if (수 < 0 || okte_xëyma.length - wërngël_àlluwa_tur < 수) throw new 잘못된인수예외("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) kotu_araf &= (1 << (6 - 수)) - 1;
            for (int 안쪽자리 = 0; 안쪽자리 < 수; 안쪽자리++) { int woñeeku_xëyma = okte_xëyma[wërngël_àlluwa_tur++] & 255; if ((woñeeku_xëyma & 192) != 128) throw new 잘못된인수예외("잘못된 UTF-8"); kotu_araf = kotu_araf << 6 | woñeeku_xëyma & 63; }
            if (kotu_araf < 최소 || kotu_araf > 0x10ffff || kotu_araf >= 0xd800 && kotu_araf <= 0xdfff) throw new 잘못된인수예외("잘못된 UTF-8");
            if (kotu_araf < 65536) 결과.append((char)kotu_araf);
            else { kotu_araf -= 65536; 결과.append((char)(0xd800 | kotu_araf >> 10)); 결과.append((char)(0xdc00 | kotu_araf & 1023)); }
        }
        return 결과.toString();
    }
}
