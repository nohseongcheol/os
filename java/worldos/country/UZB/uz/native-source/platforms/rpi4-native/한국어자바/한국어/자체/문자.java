// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 문자(文字), kodlash_VALUE(符號): UTF-8 바이트와 UTF-16 문자열의 CONVERT_VALUE. normallashtirmoq_VALUE/조합 입력기는 별개다. */
public final class 문자 {
    public static int bayt_COUNT(byte[] ma_lumotlar) { return ma_lumotlar.length; }
    private 문자() {}
    public static int uzunlik_VALUE(String Matn) { return Matn.length(); }
    public static boolean 같음(String old_kamera_VALUE, String Orqaga_VALUE) { return old_kamera_VALUE == null ? Orqaga_VALUE == null : old_kamera_VALUE.equals(Orqaga_VALUE); }
    public static String qo_shib_qo_ymoq_SMS(String old_kamera_VALUE, String Orqaga_VALUE) { return old_kamera_VALUE.concat(Orqaga_VALUE); }
    public static String qirqmoq_VALUE(String Matn, int Bajarish, int 끝) { return Matn.substring(Bajarish, 끝); }
    public static int tahlil_qilmoq_butun_son(String Matn) { try { return Integer.parseInt(Matn); } catch (NumberFormatException Xato) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String yozmoq_butun_son_VALUE(int 수) { return Integer.toString(수); }
    public static int belgi_kodi_COUNT(String Matn) {
        int 수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Matn.length(); Loop_INDEX++, 수++) {
            int belgi_kodi = Matn.charAt(Loop_INDEX);
            if (belgi_kodi >= 0xd800 && belgi_kodi <= 0xdbff && Loop_INDEX + 1 < Matn.length() && Matn.charAt(Loop_INDEX + 1) >= 0xdc00 && Matn.charAt(Loop_INDEX + 1) <= 0xdfff) Loop_INDEX++;
        }
        return 수;
    }
    public static byte[] 부호화(String Matn) {
        byte[] 임시 = new byte[Matn.length() * 3]; int 쓴수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Matn.length(); Loop_INDEX++) {
            int belgi_kodi = Matn.charAt(Loop_INDEX);
            if (belgi_kodi >= 0xd800 && belgi_kodi <= 0xdbff && Loop_INDEX + 1 < Matn.length() && Matn.charAt(Loop_INDEX + 1) >= 0xdc00 && Matn.charAt(Loop_INDEX + 1) <= 0xdfff) belgi_kodi = 0x10000 + ((belgi_kodi - 0xd800) << 10) + Matn.charAt(++Loop_INDEX) - 0xdc00;
            else if (belgi_kodi >= 0xd800 && belgi_kodi <= 0xdfff) belgi_kodi = '?';
            if (belgi_kodi < 128) 임시[쓴수++] = (byte)belgi_kodi;
            else if (belgi_kodi < 2048) { 임시[쓴수++] = (byte)(192 | belgi_kodi >> 6); 임시[쓴수++] = (byte)(128 | belgi_kodi & 63); }
            else if (belgi_kodi < 65536) { 임시[쓴수++] = (byte)(224 | belgi_kodi >> 12); 임시[쓴수++] = (byte)(128 | belgi_kodi >> 6 & 63); 임시[쓴수++] = (byte)(128 | belgi_kodi & 63); }
            else { 임시[쓴수++] = (byte)(240 | belgi_kodi >> 18); 임시[쓴수++] = (byte)(128 | belgi_kodi >> 12 & 63); 임시[쓴수++] = (byte)(128 | belgi_kodi >> 6 & 63); 임시[쓴수++] = (byte)(128 | belgi_kodi & 63); }
        }
        byte[] o_lchov = new byte[쓴수]; System.arraycopy(임시, 0, o_lchov, 0, 쓴수); return o_lchov;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String shifrsizlantirish_ma_lumotlar(byte[] bayt_VALUE) {
        StringBuilder o_lchov = new StringBuilder();
        for (int Loop_INDEX = 0; Loop_INDEX < bayt_VALUE.length;) {
            int belgi_kodi = bayt_VALUE[Loop_INDEX++] & 255, 수 = belgi_kodi < 128 ? 0 : belgi_kodi >= 194 && belgi_kodi < 224 ? 1 : belgi_kodi >= 224 && belgi_kodi < 240 ? 2 : belgi_kodi >= 240 && belgi_kodi <= 244 ? 3 : -1;
            if (수 < 0 || bayt_VALUE.length - Loop_INDEX < 수) throw new xato_dalil_istisno("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) belgi_kodi &= (1 << (6 - 수)) - 1;
            for (int ichki_qo_shilish_holat = 0; ichki_qo_shilish_holat < 수; ichki_qo_shilish_holat++) { int Orqaga_VALUE = bayt_VALUE[Loop_INDEX++] & 255; if ((Orqaga_VALUE & 192) != 128) throw new xato_dalil_istisno("잘못된 UTF-8"); belgi_kodi = belgi_kodi << 6 | Orqaga_VALUE & 63; }
            if (belgi_kodi < 최소 || belgi_kodi > 0x10ffff || belgi_kodi >= 0xd800 && belgi_kodi <= 0xdfff) throw new xato_dalil_istisno("잘못된 UTF-8");
            if (belgi_kodi < 65536) o_lchov.append((char)belgi_kodi);
            else { belgi_kodi -= 65536; o_lchov.append((char)(0xd800 | belgi_kodi >> 10)); o_lchov.append((char)(0xdc00 | belgi_kodi & 1023)); }
        }
        return o_lchov.toString();
    }
}
