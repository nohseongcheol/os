// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Melayu.Asli;
/** 문자(文字), pengekodan_VALUE(符號): UTF-8 바이트와 UTF-16 문자열의 tukar_VALUE. menormalkan_VALUE/조합 입력기는 별개다. */
public final class 문자 {
    public static int bait_COUNT(byte[] data) { return data.length; }
    private 문자() {}
    public static int kepanjangan_VALUE(String Teks) { return Teks.length(); }
    public static boolean 같음(String hadapan_VALUE, String BACK_VALUE) { return hadapan_VALUE == null ? BACK_VALUE == null : hadapan_VALUE.equals(BACK_VALUE); }
    public static String tampal_SMS(String hadapan_VALUE, String BACK_VALUE) { return hadapan_VALUE.concat(BACK_VALUE); }
    public static String potong_VALUE(String Teks, int Jalan, int 끝) { return Teks.substring(Jalan, 끝); }
    public static int hurai_integer(String Teks) { try { return Integer.parseInt(Teks); } catch (NumberFormatException RALAT) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String tulis_integer_VALUE(int 수) { return Integer.toString(수); }
    public static int titik_kod_COUNT(String Teks) {
        int 수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Teks.length(); Loop_INDEX++, 수++) {
            int titik_kod = Teks.charAt(Loop_INDEX);
            if (titik_kod >= 0xd800 && titik_kod <= 0xdbff && Loop_INDEX + 1 < Teks.length() && Teks.charAt(Loop_INDEX + 1) >= 0xdc00 && Teks.charAt(Loop_INDEX + 1) <= 0xdfff) Loop_INDEX++;
        }
        return 수;
    }
    public static byte[] 부호화(String Teks) {
        byte[] 임시 = new byte[Teks.length() * 3]; int 쓴수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Teks.length(); Loop_INDEX++) {
            int titik_kod = Teks.charAt(Loop_INDEX);
            if (titik_kod >= 0xd800 && titik_kod <= 0xdbff && Loop_INDEX + 1 < Teks.length() && Teks.charAt(Loop_INDEX + 1) >= 0xdc00 && Teks.charAt(Loop_INDEX + 1) <= 0xdfff) titik_kod = 0x10000 + ((titik_kod - 0xd800) << 10) + Teks.charAt(++Loop_INDEX) - 0xdc00;
            else if (titik_kod >= 0xd800 && titik_kod <= 0xdfff) titik_kod = '?';
            if (titik_kod < 128) 임시[쓴수++] = (byte)titik_kod;
            else if (titik_kod < 2048) { 임시[쓴수++] = (byte)(192 | titik_kod >> 6); 임시[쓴수++] = (byte)(128 | titik_kod & 63); }
            else if (titik_kod < 65536) { 임시[쓴수++] = (byte)(224 | titik_kod >> 12); 임시[쓴수++] = (byte)(128 | titik_kod >> 6 & 63); 임시[쓴수++] = (byte)(128 | titik_kod & 63); }
            else { 임시[쓴수++] = (byte)(240 | titik_kod >> 18); 임시[쓴수++] = (byte)(128 | titik_kod >> 12 & 63); 임시[쓴수++] = (byte)(128 | titik_kod >> 6 & 63); 임시[쓴수++] = (byte)(128 | titik_kod & 63); }
        }
        byte[] ukuran = new byte[쓴수]; System.arraycopy(임시, 0, ukuran, 0, 쓴수); return ukuran;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String nyahsulit_data(byte[] bait_VALUE) {
        StringBuilder ukuran = new StringBuilder();
        for (int Loop_INDEX = 0; Loop_INDEX < bait_VALUE.length;) {
            int titik_kod = bait_VALUE[Loop_INDEX++] & 255, 수 = titik_kod < 128 ? 0 : titik_kod >= 194 && titik_kod < 224 ? 1 : titik_kod >= 224 && titik_kod < 240 ? 2 : titik_kod >= 240 && titik_kod <= 244 ? 3 : -1;
            if (수 < 0 || bait_VALUE.length - Loop_INDEX < 수) throw new tak_sah_argumen_pengecualian("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) titik_kod &= (1 << (6 - 수)) - 1;
            for (int dalaman_jawatan = 0; dalaman_jawatan < 수; dalaman_jawatan++) { int BACK_VALUE = bait_VALUE[Loop_INDEX++] & 255; if ((BACK_VALUE & 192) != 128) throw new tak_sah_argumen_pengecualian("잘못된 UTF-8"); titik_kod = titik_kod << 6 | BACK_VALUE & 63; }
            if (titik_kod < 최소 || titik_kod > 0x10ffff || titik_kod >= 0xd800 && titik_kod <= 0xdfff) throw new tak_sah_argumen_pengecualian("잘못된 UTF-8");
            if (titik_kod < 65536) ukuran.append((char)titik_kod);
            else { titik_kod -= 65536; ukuran.append((char)(0xd800 | titik_kod >> 10)); ukuran.append((char)(0xdc00 | titik_kod & 1023)); }
        }
        return ukuran.toString();
    }
}
