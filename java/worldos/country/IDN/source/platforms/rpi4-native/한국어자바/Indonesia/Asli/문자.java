// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Indonesia.Asli;
/** 문자(文字), pengodean_VALUE(符號): UTF-8 바이트와 UTF-16 문자열의 CONVERT_VALUE. normalkan_VALUE/조합 입력기는 별개다. */
public final class 문자 {
    public static int byte_COUNT(byte[] data) { return data.length; }
    private 문자() {}
    public static int panjang_VALUE(String teks) { return teks.length(); }
    public static boolean 같음(String depan_VALUE, String BACK_VALUE) { return depan_VALUE == null ? BACK_VALUE == null : depan_VALUE.equals(BACK_VALUE); }
    public static String tempel_SMS(String depan_VALUE, String BACK_VALUE) { return depan_VALUE.concat(BACK_VALUE); }
    public static String potong_VALUE(String teks, int jalankan, int 끝) { return teks.substring(jalankan, 끝); }
    public static int urai_bilangan_bulat(String teks) { try { return Integer.parseInt(teks); } catch (NumberFormatException galat) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String tulis_bilangan_bulat_VALUE(int 수) { return Integer.toString(수); }
    public static int poin_kode_COUNT(String teks) {
        int 수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < teks.length(); Loop_INDEX++, 수++) {
            int kode_karakter = teks.charAt(Loop_INDEX);
            if (kode_karakter >= 0xd800 && kode_karakter <= 0xdbff && Loop_INDEX + 1 < teks.length() && teks.charAt(Loop_INDEX + 1) >= 0xdc00 && teks.charAt(Loop_INDEX + 1) <= 0xdfff) Loop_INDEX++;
        }
        return 수;
    }
    public static byte[] 부호화(String teks) {
        byte[] 임시 = new byte[teks.length() * 3]; int 쓴수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < teks.length(); Loop_INDEX++) {
            int kode_karakter = teks.charAt(Loop_INDEX);
            if (kode_karakter >= 0xd800 && kode_karakter <= 0xdbff && Loop_INDEX + 1 < teks.length() && teks.charAt(Loop_INDEX + 1) >= 0xdc00 && teks.charAt(Loop_INDEX + 1) <= 0xdfff) kode_karakter = 0x10000 + ((kode_karakter - 0xd800) << 10) + teks.charAt(++Loop_INDEX) - 0xdc00;
            else if (kode_karakter >= 0xd800 && kode_karakter <= 0xdfff) kode_karakter = '?';
            if (kode_karakter < 128) 임시[쓴수++] = (byte)kode_karakter;
            else if (kode_karakter < 2048) { 임시[쓴수++] = (byte)(192 | kode_karakter >> 6); 임시[쓴수++] = (byte)(128 | kode_karakter & 63); }
            else if (kode_karakter < 65536) { 임시[쓴수++] = (byte)(224 | kode_karakter >> 12); 임시[쓴수++] = (byte)(128 | kode_karakter >> 6 & 63); 임시[쓴수++] = (byte)(128 | kode_karakter & 63); }
            else { 임시[쓴수++] = (byte)(240 | kode_karakter >> 18); 임시[쓴수++] = (byte)(128 | kode_karakter >> 12 & 63); 임시[쓴수++] = (byte)(128 | kode_karakter >> 6 & 63); 임시[쓴수++] = (byte)(128 | kode_karakter & 63); }
        }
        byte[] hasil = new byte[쓴수]; System.arraycopy(임시, 0, hasil, 0, 쓴수); return hasil;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String dekripsikan_data(byte[] byte_VALUE) {
        StringBuilder hasil = new StringBuilder();
        for (int Loop_INDEX = 0; Loop_INDEX < byte_VALUE.length;) {
            int kode_karakter = byte_VALUE[Loop_INDEX++] & 255, 수 = kode_karakter < 128 ? 0 : kode_karakter >= 194 && kode_karakter < 224 ? 1 : kode_karakter >= 224 && kode_karakter < 240 ? 2 : kode_karakter >= 240 && kode_karakter <= 244 ? 3 : -1;
            if (수 < 0 || byte_VALUE.length - Loop_INDEX < 수) throw new tidak_sahih_argumen_pengecualian("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) kode_karakter &= (1 << (6 - 수)) - 1;
            for (int dalam_posisi = 0; dalam_posisi < 수; dalam_posisi++) { int BACK_VALUE = byte_VALUE[Loop_INDEX++] & 255; if ((BACK_VALUE & 192) != 128) throw new tidak_sahih_argumen_pengecualian("잘못된 UTF-8"); kode_karakter = kode_karakter << 6 | BACK_VALUE & 63; }
            if (kode_karakter < 최소 || kode_karakter > 0x10ffff || kode_karakter >= 0xd800 && kode_karakter <= 0xdfff) throw new tidak_sahih_argumen_pengecualian("잘못된 UTF-8");
            if (kode_karakter < 65536) hasil.append((char)kode_karakter);
            else { kode_karakter -= 65536; hasil.append((char)(0xd800 | kode_karakter >> 10)); hasil.append((char)(0xdc00 | kode_karakter & 1023)); }
        }
        return hasil.toString();
    }
}
