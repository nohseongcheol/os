// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 문자(文字), tukiniktiri_atuutilik(符號): UTF-8 바이트와 UTF-16 문자열의 변환. naammasitilli_atuutilik/조합 입력기는 별개다. */
public final class 문자 {
    public static int 바이트수(byte[] titiqqat) { return titiqqat.length; }
    private 문자() {}
    public static int takininga_atuutilik(String titiqqaq) { return titiqqaq.length(); }
    public static boolean 같음(String 앞, String Utimut_atuutilik) { return 앞 == null ? Utimut_atuutilik == null : 앞.equals(Utimut_atuutilik); }
    public static String nipitilli_titiqqaq(String 앞, String Utimut_atuutilik) { return 앞.concat(Utimut_atuutilik); }
    public static String nakalli_atuutilik(String titiqqaq, int 시작, int 끝) { return titiqqaq.substring(시작, 끝); }
    public static int agguqtuut_naasaut(String titiqqaq) { try { return Integer.parseInt(titiqqaq); } catch (NumberFormatException tammarniq) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String titiraq_naasaut_atuutilik(int 수) { return Integer.toString(수); }
    public static int 코드포인트수(String titiqqaq) {
        int 수 = 0;
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < titiqqaq.length(); piliqqittaajuq_nalunaiqsimavik++, 수++) {
            int immikkuuqtumut_nalunaikkut = titiqqaq.charAt(piliqqittaajuq_nalunaiqsimavik);
            if (immikkuuqtumut_nalunaikkut >= 0xd800 && immikkuuqtumut_nalunaikkut <= 0xdbff && piliqqittaajuq_nalunaiqsimavik + 1 < titiqqaq.length() && titiqqaq.charAt(piliqqittaajuq_nalunaiqsimavik + 1) >= 0xdc00 && titiqqaq.charAt(piliqqittaajuq_nalunaiqsimavik + 1) <= 0xdfff) piliqqittaajuq_nalunaiqsimavik++;
        }
        return 수;
    }
    public static byte[] 부호화(String titiqqaq) {
        byte[] 임시 = new byte[titiqqaq.length() * 3]; int 쓴수 = 0;
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < titiqqaq.length(); piliqqittaajuq_nalunaiqsimavik++) {
            int immikkuuqtumut_nalunaikkut = titiqqaq.charAt(piliqqittaajuq_nalunaiqsimavik);
            if (immikkuuqtumut_nalunaikkut >= 0xd800 && immikkuuqtumut_nalunaikkut <= 0xdbff && piliqqittaajuq_nalunaiqsimavik + 1 < titiqqaq.length() && titiqqaq.charAt(piliqqittaajuq_nalunaiqsimavik + 1) >= 0xdc00 && titiqqaq.charAt(piliqqittaajuq_nalunaiqsimavik + 1) <= 0xdfff) immikkuuqtumut_nalunaikkut = 0x10000 + ((immikkuuqtumut_nalunaikkut - 0xd800) << 10) + titiqqaq.charAt(++piliqqittaajuq_nalunaiqsimavik) - 0xdc00;
            else if (immikkuuqtumut_nalunaikkut >= 0xd800 && immikkuuqtumut_nalunaikkut <= 0xdfff) immikkuuqtumut_nalunaikkut = '?';
            if (immikkuuqtumut_nalunaikkut < 128) 임시[쓴수++] = (byte)immikkuuqtumut_nalunaikkut;
            else if (immikkuuqtumut_nalunaikkut < 2048) { 임시[쓴수++] = (byte)(192 | immikkuuqtumut_nalunaikkut >> 6); 임시[쓴수++] = (byte)(128 | immikkuuqtumut_nalunaikkut & 63); }
            else if (immikkuuqtumut_nalunaikkut < 65536) { 임시[쓴수++] = (byte)(224 | immikkuuqtumut_nalunaikkut >> 12); 임시[쓴수++] = (byte)(128 | immikkuuqtumut_nalunaikkut >> 6 & 63); 임시[쓴수++] = (byte)(128 | immikkuuqtumut_nalunaikkut & 63); }
            else { 임시[쓴수++] = (byte)(240 | immikkuuqtumut_nalunaikkut >> 18); 임시[쓴수++] = (byte)(128 | immikkuuqtumut_nalunaikkut >> 12 & 63); 임시[쓴수++] = (byte)(128 | immikkuuqtumut_nalunaikkut >> 6 & 63); 임시[쓴수++] = (byte)(128 | immikkuuqtumut_nalunaikkut & 63); }
        }
        byte[] 결과 = new byte[쓴수]; System.arraycopy(임시, 0, 결과, 0, 쓴수); return 결과;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String suqquinarunniirlit_titiqqat(byte[] byte_atuutilik) {
        StringBuilder 결과 = new StringBuilder();
        for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < byte_atuutilik.length;) {
            int immikkuuqtumut_nalunaikkut = byte_atuutilik[piliqqittaajuq_nalunaiqsimavik++] & 255, 수 = immikkuuqtumut_nalunaikkut < 128 ? 0 : immikkuuqtumut_nalunaikkut >= 194 && immikkuuqtumut_nalunaikkut < 224 ? 1 : immikkuuqtumut_nalunaikkut >= 224 && immikkuuqtumut_nalunaikkut < 240 ? 2 : immikkuuqtumut_nalunaikkut >= 240 && immikkuuqtumut_nalunaikkut <= 244 ? 3 : -1;
            if (수 < 0 || byte_atuutilik.length - piliqqittaajuq_nalunaiqsimavik < 수) throw new 잘못된인수예외("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) immikkuuqtumut_nalunaikkut &= (1 << (6 - 수)) - 1;
            for (int 안쪽자리 = 0; 안쪽자리 < 수; 안쪽자리++) { int Utimut_atuutilik = byte_atuutilik[piliqqittaajuq_nalunaiqsimavik++] & 255; if ((Utimut_atuutilik & 192) != 128) throw new 잘못된인수예외("잘못된 UTF-8"); immikkuuqtumut_nalunaikkut = immikkuuqtumut_nalunaikkut << 6 | Utimut_atuutilik & 63; }
            if (immikkuuqtumut_nalunaikkut < 최소 || immikkuuqtumut_nalunaikkut > 0x10ffff || immikkuuqtumut_nalunaikkut >= 0xd800 && immikkuuqtumut_nalunaikkut <= 0xdfff) throw new 잘못된인수예외("잘못된 UTF-8");
            if (immikkuuqtumut_nalunaikkut < 65536) 결과.append((char)immikkuuqtumut_nalunaikkut);
            else { immikkuuqtumut_nalunaikkut -= 65536; 결과.append((char)(0xd800 | immikkuuqtumut_nalunaikkut >> 10)); 결과.append((char)(0xdc00 | immikkuuqtumut_nalunaikkut & 1023)); }
        }
        return 결과.toString();
    }
}
