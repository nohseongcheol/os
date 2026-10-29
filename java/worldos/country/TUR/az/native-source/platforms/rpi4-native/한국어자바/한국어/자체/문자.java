// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 문자(文字), kodlaşdırma_VALUE(符號): UTF-8 바이트와 UTF-16 문자열의 CONVERT_VALUE. normallaşdırmaq_VALUE/조합 입력기는 별개다. */
public final class 문자 {
    public static int bayt_COUNT(byte[] verilənlər) { return verilənlər.length; }
    private 문자() {}
    public static int uzunluq_VALUE(String Mətn) { return Mətn.length(); }
    public static boolean 같음(String ön_VALUE, String GERİ_VALUE) { return ön_VALUE == null ? GERİ_VALUE == null : ön_VALUE.equals(GERİ_VALUE); }
    public static String əlavə_etmək_SMS(String ön_VALUE, String GERİ_VALUE) { return ön_VALUE.concat(GERİ_VALUE); }
    public static String bölmək_VALUE(String Mətn, int İcra_Et, int 끝) { return Mətn.substring(İcra_Et, 끝); }
    public static int parselləmək_tam_ədəd(String Mətn) { try { return Integer.parseInt(Mətn); } catch (NumberFormatException XƏTA) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String yazmaq_tam_ədəd_VALUE(int 수) { return Integer.toString(수); }
    public static int simvol_kodu_COUNT(String Mətn) {
        int 수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Mətn.length(); Loop_INDEX++, 수++) {
            int simvol_kodu = Mətn.charAt(Loop_INDEX);
            if (simvol_kodu >= 0xd800 && simvol_kodu <= 0xdbff && Loop_INDEX + 1 < Mətn.length() && Mətn.charAt(Loop_INDEX + 1) >= 0xdc00 && Mətn.charAt(Loop_INDEX + 1) <= 0xdfff) Loop_INDEX++;
        }
        return 수;
    }
    public static byte[] 부호화(String Mətn) {
        byte[] 임시 = new byte[Mətn.length() * 3]; int 쓴수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Mətn.length(); Loop_INDEX++) {
            int simvol_kodu = Mətn.charAt(Loop_INDEX);
            if (simvol_kodu >= 0xd800 && simvol_kodu <= 0xdbff && Loop_INDEX + 1 < Mətn.length() && Mətn.charAt(Loop_INDEX + 1) >= 0xdc00 && Mətn.charAt(Loop_INDEX + 1) <= 0xdfff) simvol_kodu = 0x10000 + ((simvol_kodu - 0xd800) << 10) + Mətn.charAt(++Loop_INDEX) - 0xdc00;
            else if (simvol_kodu >= 0xd800 && simvol_kodu <= 0xdfff) simvol_kodu = '?';
            if (simvol_kodu < 128) 임시[쓴수++] = (byte)simvol_kodu;
            else if (simvol_kodu < 2048) { 임시[쓴수++] = (byte)(192 | simvol_kodu >> 6); 임시[쓴수++] = (byte)(128 | simvol_kodu & 63); }
            else if (simvol_kodu < 65536) { 임시[쓴수++] = (byte)(224 | simvol_kodu >> 12); 임시[쓴수++] = (byte)(128 | simvol_kodu >> 6 & 63); 임시[쓴수++] = (byte)(128 | simvol_kodu & 63); }
            else { 임시[쓴수++] = (byte)(240 | simvol_kodu >> 18); 임시[쓴수++] = (byte)(128 | simvol_kodu >> 12 & 63); 임시[쓴수++] = (byte)(128 | simvol_kodu >> 6 & 63); 임시[쓴수++] = (byte)(128 | simvol_kodu & 63); }
        }
        byte[] ölçü = new byte[쓴수]; System.arraycopy(임시, 0, ölçü, 0, 쓴수); return ölçü;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String şifr_açmaq_verilənlər(byte[] bayt_VALUE) {
        StringBuilder ölçü = new StringBuilder();
        for (int Loop_INDEX = 0; Loop_INDEX < bayt_VALUE.length;) {
            int simvol_kodu = bayt_VALUE[Loop_INDEX++] & 255, 수 = simvol_kodu < 128 ? 0 : simvol_kodu >= 194 && simvol_kodu < 224 ? 1 : simvol_kodu >= 224 && simvol_kodu < 240 ? 2 : simvol_kodu >= 240 && simvol_kodu <= 244 ? 3 : -1;
            if (수 < 0 || bayt_VALUE.length - Loop_INDEX < 수) throw new yanlış_arqument_istisna("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) simvol_kodu &= (1 << (6 - 수)) - 1;
            for (int daxili_qoşulma_yerinə_qoymaq = 0; daxili_qoşulma_yerinə_qoymaq < 수; daxili_qoşulma_yerinə_qoymaq++) { int GERİ_VALUE = bayt_VALUE[Loop_INDEX++] & 255; if ((GERİ_VALUE & 192) != 128) throw new yanlış_arqument_istisna("잘못된 UTF-8"); simvol_kodu = simvol_kodu << 6 | GERİ_VALUE & 63; }
            if (simvol_kodu < 최소 || simvol_kodu > 0x10ffff || simvol_kodu >= 0xd800 && simvol_kodu <= 0xdfff) throw new yanlış_arqument_istisna("잘못된 UTF-8");
            if (simvol_kodu < 65536) ölçü.append((char)simvol_kodu);
            else { simvol_kodu -= 65536; ölçü.append((char)(0xd800 | simvol_kodu >> 10)); ölçü.append((char)(0xdc00 | simvol_kodu & 1023)); }
        }
        return ölçü.toString();
    }
}
