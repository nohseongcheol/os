// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Türkçe.Öz;
/** 문자(文字), kodlama_değer(符號): UTF-8 바이트와 UTF-16 문자열의 ÇEVİR_değer. normalleştirmek_değer/조합 입력기는 별개다. */
public final class 문자 {
    public static int bayt_BAĞ_DEĞ_SAY(byte[] veri) { return veri.length; }
    private 문자() {}
    public static int süre_değer(String metin) { return metin.length(); }
    public static boolean 같음(String ön_kamera_değer, String BACK_değer) { return ön_kamera_değer == null ? BACK_değer == null : ön_kamera_değer.equals(BACK_değer); }
    public static String yapıştırmak_SMS(String ön_kamera_değer, String BACK_değer) { return ön_kamera_değer.concat(BACK_değer); }
    public static String kesmek_değer(String metin, int çalıştır, int 끝) { return metin.substring(çalıştır, 끝); }
    public static int ayrıştırmak_bilgi(String metin) { try { return Integer.parseInt(metin); } catch (NumberFormatException hata) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String yazma_bilgi_değer(int 수) { return Integer.toString(수); }
    public static int kod_öğesi_BAĞ_DEĞ_SAY(String metin) {
        int 수 = 0;
        for (int Loop_Dizin = 0; Loop_Dizin < metin.length(); Loop_Dizin++, 수++) {
            int kod_noktası = metin.charAt(Loop_Dizin);
            if (kod_noktası >= 0xd800 && kod_noktası <= 0xdbff && Loop_Dizin + 1 < metin.length() && metin.charAt(Loop_Dizin + 1) >= 0xdc00 && metin.charAt(Loop_Dizin + 1) <= 0xdfff) Loop_Dizin++;
        }
        return 수;
    }
    public static byte[] kodlamak(String metin) {
        byte[] 임시 = new byte[metin.length() * 3]; int 쓴수 = 0;
        for (int Loop_Dizin = 0; Loop_Dizin < metin.length(); Loop_Dizin++) {
            int kod_noktası = metin.charAt(Loop_Dizin);
            if (kod_noktası >= 0xd800 && kod_noktası <= 0xdbff && Loop_Dizin + 1 < metin.length() && metin.charAt(Loop_Dizin + 1) >= 0xdc00 && metin.charAt(Loop_Dizin + 1) <= 0xdfff) kod_noktası = 0x10000 + ((kod_noktası - 0xd800) << 10) + metin.charAt(++Loop_Dizin) - 0xdc00;
            else if (kod_noktası >= 0xd800 && kod_noktası <= 0xdfff) kod_noktası = '?';
            if (kod_noktası < 128) 임시[쓴수++] = (byte)kod_noktası;
            else if (kod_noktası < 2048) { 임시[쓴수++] = (byte)(192 | kod_noktası >> 6); 임시[쓴수++] = (byte)(128 | kod_noktası & 63); }
            else if (kod_noktası < 65536) { 임시[쓴수++] = (byte)(224 | kod_noktası >> 12); 임시[쓴수++] = (byte)(128 | kod_noktası >> 6 & 63); 임시[쓴수++] = (byte)(128 | kod_noktası & 63); }
            else { 임시[쓴수++] = (byte)(240 | kod_noktası >> 18); 임시[쓴수++] = (byte)(128 | kod_noktası >> 12 & 63); 임시[쓴수++] = (byte)(128 | kod_noktası >> 6 & 63); 임시[쓴수++] = (byte)(128 | kod_noktası & 63); }
        }
        byte[] sonuç = new byte[쓴수]; System.arraycopy(임시, 0, sonuç, 0, 쓴수); return sonuç;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String şifre_çözmek_veri(byte[] bayt_değer) {
        StringBuilder sonuç = new StringBuilder();
        for (int Loop_Dizin = 0; Loop_Dizin < bayt_değer.length;) {
            int kod_noktası = bayt_değer[Loop_Dizin++] & 255, 수 = kod_noktası < 128 ? 0 : kod_noktası >= 194 && kod_noktası < 224 ? 1 : kod_noktası >= 224 && kod_noktası < 240 ? 2 : kod_noktası >= 240 && kod_noktası <= 244 ? 3 : -1;
            if (수 < 0 || bayt_değer.length - Loop_Dizin < 수) throw new geçersiz_bağımsız_değişken_özel_durum("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) kod_noktası &= (1 << (6 - 수)) - 1;
            for (int iç_konum = 0; iç_konum < 수; iç_konum++) { int BACK_değer = bayt_değer[Loop_Dizin++] & 255; if ((BACK_değer & 192) != 128) throw new geçersiz_bağımsız_değişken_özel_durum("잘못된 UTF-8"); kod_noktası = kod_noktası << 6 | BACK_değer & 63; }
            if (kod_noktası < 최소 || kod_noktası > 0x10ffff || kod_noktası >= 0xd800 && kod_noktası <= 0xdfff) throw new geçersiz_bağımsız_değişken_özel_durum("잘못된 UTF-8");
            if (kod_noktası < 65536) sonuç.append((char)kod_noktası);
            else { kod_noktası -= 65536; sonuç.append((char)(0xd800 | kod_noktası >> 10)); sonuç.append((char)(0xdc00 | kod_noktası & 1023)); }
        }
        return sonuç.toString();
    }
}
