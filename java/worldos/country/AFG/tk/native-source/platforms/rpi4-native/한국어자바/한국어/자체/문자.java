// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 문자(文字), kodlaşdyrma_baha(符號): UTF-8 바이트와 UTF-16 문자열의 변환. adaty_ýagdaýa_getir_baha/조합 입력기는 별개다. */
public final class 문자 {
    public static int 바이트수(byte[] maglumat) { return maglumat.length; }
    private 문자() {}
    public static int dowamlylyk_baha(String Metin) { return Metin.length(); }
    public static boolean 같음(String 앞, String Yza_baha) { return 앞 == null ? Yza_baha == null : 앞.equals(Yza_baha); }
    public static String ýelme_SMS(String 앞, String Yza_baha) { return 앞.concat(Yza_baha); }
    public static String kes_baha(String Metin, int Bitir, int 끝) { return Metin.substring(Bitir, 끝); }
    public static int seljer_bitin(String Metin) { try { return Integer.parseInt(Metin); } catch (NumberFormatException Hata) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String ýaz_bitin_baha(int 수) { return Integer.toString(수); }
    public static int 코드포인트수(String Metin) {
        int 수 = 0;
        for (int sikl_indeks = 0; sikl_indeks < Metin.length(); sikl_indeks++, 수++) {
            int nyşanyň_kody = Metin.charAt(sikl_indeks);
            if (nyşanyň_kody >= 0xd800 && nyşanyň_kody <= 0xdbff && sikl_indeks + 1 < Metin.length() && Metin.charAt(sikl_indeks + 1) >= 0xdc00 && Metin.charAt(sikl_indeks + 1) <= 0xdfff) sikl_indeks++;
        }
        return 수;
    }
    public static byte[] 부호화(String Metin) {
        byte[] 임시 = new byte[Metin.length() * 3]; int 쓴수 = 0;
        for (int sikl_indeks = 0; sikl_indeks < Metin.length(); sikl_indeks++) {
            int nyşanyň_kody = Metin.charAt(sikl_indeks);
            if (nyşanyň_kody >= 0xd800 && nyşanyň_kody <= 0xdbff && sikl_indeks + 1 < Metin.length() && Metin.charAt(sikl_indeks + 1) >= 0xdc00 && Metin.charAt(sikl_indeks + 1) <= 0xdfff) nyşanyň_kody = 0x10000 + ((nyşanyň_kody - 0xd800) << 10) + Metin.charAt(++sikl_indeks) - 0xdc00;
            else if (nyşanyň_kody >= 0xd800 && nyşanyň_kody <= 0xdfff) nyşanyň_kody = '?';
            if (nyşanyň_kody < 128) 임시[쓴수++] = (byte)nyşanyň_kody;
            else if (nyşanyň_kody < 2048) { 임시[쓴수++] = (byte)(192 | nyşanyň_kody >> 6); 임시[쓴수++] = (byte)(128 | nyşanyň_kody & 63); }
            else if (nyşanyň_kody < 65536) { 임시[쓴수++] = (byte)(224 | nyşanyň_kody >> 12); 임시[쓴수++] = (byte)(128 | nyşanyň_kody >> 6 & 63); 임시[쓴수++] = (byte)(128 | nyşanyň_kody & 63); }
            else { 임시[쓴수++] = (byte)(240 | nyşanyň_kody >> 18); 임시[쓴수++] = (byte)(128 | nyşanyň_kody >> 12 & 63); 임시[쓴수++] = (byte)(128 | nyşanyň_kody >> 6 & 63); 임시[쓴수++] = (byte)(128 | nyşanyň_kody & 63); }
        }
        byte[] 결과 = new byte[쓴수]; System.arraycopy(임시, 0, 결과, 0, 쓴수); return 결과;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String koddan_aç_maglumat(byte[] baýt_baha) {
        StringBuilder 결과 = new StringBuilder();
        for (int sikl_indeks = 0; sikl_indeks < baýt_baha.length;) {
            int nyşanyň_kody = baýt_baha[sikl_indeks++] & 255, 수 = nyşanyň_kody < 128 ? 0 : nyşanyň_kody >= 194 && nyşanyň_kody < 224 ? 1 : nyşanyň_kody >= 224 && nyşanyň_kody < 240 ? 2 : nyşanyň_kody >= 240 && nyşanyň_kody <= 244 ? 3 : -1;
            if (수 < 0 || baýt_baha.length - sikl_indeks < 수) throw new 잘못된인수예외("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) nyşanyň_kody &= (1 << (6 - 수)) - 1;
            for (int 안쪽자리 = 0; 안쪽자리 < 수; 안쪽자리++) { int Yza_baha = baýt_baha[sikl_indeks++] & 255; if ((Yza_baha & 192) != 128) throw new 잘못된인수예외("잘못된 UTF-8"); nyşanyň_kody = nyşanyň_kody << 6 | Yza_baha & 63; }
            if (nyşanyň_kody < 최소 || nyşanyň_kody > 0x10ffff || nyşanyň_kody >= 0xd800 && nyşanyň_kody <= 0xdfff) throw new 잘못된인수예외("잘못된 UTF-8");
            if (nyşanyň_kody < 65536) 결과.append((char)nyşanyň_kody);
            else { nyşanyň_kody -= 65536; 결과.append((char)(0xd800 | nyşanyň_kody >> 10)); 결과.append((char)(0xdc00 | nyşanyň_kody & 1023)); }
        }
        return 결과.toString();
    }
}
