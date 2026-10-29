// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latviešu.savs;
/** 문자(文字), kodēšana_VALUE(符號): UTF-8 바이트와 UTF-16 문자열의 CONVERT_VALUE. normalizēt_VALUE/salikums_VALUE 입력기는 별개다. */
public final class 문자 {
    public static int byte_COUNT(byte[] dati) { return dati.length; }
    private 문자() {}
    public static int 길이(String Teksts) { return Teksts.length(); }
    public static boolean 같음(String priekšējā_VALUE, String ATPAKAĻ_VALUE) { return priekšējā_VALUE == null ? ATPAKAĻ_VALUE == null : priekšējā_VALUE.equals(ATPAKAĻ_VALUE); }
    public static String ielīmēt_SMS(String priekšējā_VALUE, String ATPAKAĻ_VALUE) { return priekšējā_VALUE.concat(ATPAKAĻ_VALUE); }
    public static String izgriezt_VALUE(String Teksts, int Palaist, int 끝) { return Teksts.substring(Palaist, 끝); }
    public static int parsēt_vesels_skaitlis(String Teksts) { try { return Integer.parseInt(Teksts); } catch (NumberFormatException Kļūda) { throw new numurs_formāts_kļūme("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String rakstīšana_vesels_skaitlis_VALUE(int numurs) { return Integer.toString(numurs); }
    public static int koda_punkts_COUNT(String Teksts) {
        int numurs = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Teksts.length(); Loop_INDEX++, numurs++) {
            int koda_punkts = Teksts.charAt(Loop_INDEX);
            if (koda_punkts >= 0xd800 && koda_punkts <= 0xdbff && Loop_INDEX + 1 < Teksts.length() && Teksts.charAt(Loop_INDEX + 1) >= 0xdc00 && Teksts.charAt(Loop_INDEX + 1) <= 0xdfff) Loop_INDEX++;
        }
        return numurs;
    }
    public static byte[] kodēt(String Teksts) {
        byte[] 임시 = new byte[Teksts.length() * 3]; int 쓴수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Teksts.length(); Loop_INDEX++) {
            int koda_punkts = Teksts.charAt(Loop_INDEX);
            if (koda_punkts >= 0xd800 && koda_punkts <= 0xdbff && Loop_INDEX + 1 < Teksts.length() && Teksts.charAt(Loop_INDEX + 1) >= 0xdc00 && Teksts.charAt(Loop_INDEX + 1) <= 0xdfff) koda_punkts = 0x10000 + ((koda_punkts - 0xd800) << 10) + Teksts.charAt(++Loop_INDEX) - 0xdc00;
            else if (koda_punkts >= 0xd800 && koda_punkts <= 0xdfff) koda_punkts = '?';
            if (koda_punkts < 128) 임시[쓴수++] = (byte)koda_punkts;
            else if (koda_punkts < 2048) { 임시[쓴수++] = (byte)(192 | koda_punkts >> 6); 임시[쓴수++] = (byte)(128 | koda_punkts & 63); }
            else if (koda_punkts < 65536) { 임시[쓴수++] = (byte)(224 | koda_punkts >> 12); 임시[쓴수++] = (byte)(128 | koda_punkts >> 6 & 63); 임시[쓴수++] = (byte)(128 | koda_punkts & 63); }
            else { 임시[쓴수++] = (byte)(240 | koda_punkts >> 18); 임시[쓴수++] = (byte)(128 | koda_punkts >> 12 & 63); 임시[쓴수++] = (byte)(128 | koda_punkts >> 6 & 63); 임시[쓴수++] = (byte)(128 | koda_punkts & 63); }
        }
        byte[] mērs = new byte[쓴수]; System.arraycopy(임시, 0, mērs, 0, 쓴수); return mērs;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String atšifrēt_dati(byte[] byte_VALUE) {
        StringBuilder mērs = new StringBuilder();
        for (int Loop_INDEX = 0; Loop_INDEX < byte_VALUE.length;) {
            int koda_punkts = byte_VALUE[Loop_INDEX++] & 255, numurs = koda_punkts < 128 ? 0 : koda_punkts >= 194 && koda_punkts < 224 ? 1 : koda_punkts >= 224 && koda_punkts < 240 ? 2 : koda_punkts >= 240 && koda_punkts <= 244 ? 3 : -1;
            if (numurs < 0 || byte_VALUE.length - Loop_INDEX < numurs) throw new nederīgs_arg_izņēmums("잘못된 UTF-8");
            int 최소 = numurs == 1 ? 128 : numurs == 2 ? 2048 : numurs == 3 ? 65536 : 0;
            if (numurs > 0) koda_punkts &= (1 << (6 - numurs)) - 1;
            for (int iekšējais_amats = 0; iekšējais_amats < numurs; iekšējais_amats++) { int ATPAKAĻ_VALUE = byte_VALUE[Loop_INDEX++] & 255; if ((ATPAKAĻ_VALUE & 192) != 128) throw new nederīgs_arg_izņēmums("잘못된 UTF-8"); koda_punkts = koda_punkts << 6 | ATPAKAĻ_VALUE & 63; }
            if (koda_punkts < 최소 || koda_punkts > 0x10ffff || koda_punkts >= 0xd800 && koda_punkts <= 0xdfff) throw new nederīgs_arg_izņēmums("잘못된 UTF-8");
            if (koda_punkts < 65536) mērs.append((char)koda_punkts);
            else { koda_punkts -= 65536; mērs.append((char)(0xd800 | koda_punkts >> 10)); mērs.append((char)(0xdc00 | koda_punkts & 1023)); }
        }
        return mērs.toString();
    }
}
