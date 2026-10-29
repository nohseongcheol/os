// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 문자(文字), enkodim_VALUE(符號): UTF-8 바이트와 UTF-16 문자열의 CONVERT_VALUE. normalizoj_VALUE/조합 입력기는 별개다. */
public final class 문자 {
    public static int bajt_COUNT(byte[] të_dhëna) { return të_dhëna.length; }
    private 문자() {}
    public static int gjatësi_VALUE(String Teksti) { return Teksti.length(); }
    public static boolean 같음(String e_përparme_VALUE, String PAS_VALUE) { return e_përparme_VALUE == null ? PAS_VALUE == null : e_përparme_VALUE.equals(PAS_VALUE); }
    public static String ngjit_SMS(String e_përparme_VALUE, String PAS_VALUE) { return e_përparme_VALUE.concat(PAS_VALUE); }
    public static String pres_VALUE(String Teksti, int Ekzekuto, int 끝) { return Teksti.substring(Ekzekuto, 끝); }
    public static int analizoj_numër_i_plotë(String Teksti) { try { return Integer.parseInt(Teksti); } catch (NumberFormatException GABIM) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String shkruaj_numër_i_plotë_VALUE(int 수) { return Integer.toString(수); }
    public static int kodi_i_karakterit_COUNT(String Teksti) {
        int 수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Teksti.length(); Loop_INDEX++, 수++) {
            int kodi_i_karakterit = Teksti.charAt(Loop_INDEX);
            if (kodi_i_karakterit >= 0xd800 && kodi_i_karakterit <= 0xdbff && Loop_INDEX + 1 < Teksti.length() && Teksti.charAt(Loop_INDEX + 1) >= 0xdc00 && Teksti.charAt(Loop_INDEX + 1) <= 0xdfff) Loop_INDEX++;
        }
        return 수;
    }
    public static byte[] 부호화(String Teksti) {
        byte[] 임시 = new byte[Teksti.length() * 3]; int 쓴수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Teksti.length(); Loop_INDEX++) {
            int kodi_i_karakterit = Teksti.charAt(Loop_INDEX);
            if (kodi_i_karakterit >= 0xd800 && kodi_i_karakterit <= 0xdbff && Loop_INDEX + 1 < Teksti.length() && Teksti.charAt(Loop_INDEX + 1) >= 0xdc00 && Teksti.charAt(Loop_INDEX + 1) <= 0xdfff) kodi_i_karakterit = 0x10000 + ((kodi_i_karakterit - 0xd800) << 10) + Teksti.charAt(++Loop_INDEX) - 0xdc00;
            else if (kodi_i_karakterit >= 0xd800 && kodi_i_karakterit <= 0xdfff) kodi_i_karakterit = '?';
            if (kodi_i_karakterit < 128) 임시[쓴수++] = (byte)kodi_i_karakterit;
            else if (kodi_i_karakterit < 2048) { 임시[쓴수++] = (byte)(192 | kodi_i_karakterit >> 6); 임시[쓴수++] = (byte)(128 | kodi_i_karakterit & 63); }
            else if (kodi_i_karakterit < 65536) { 임시[쓴수++] = (byte)(224 | kodi_i_karakterit >> 12); 임시[쓴수++] = (byte)(128 | kodi_i_karakterit >> 6 & 63); 임시[쓴수++] = (byte)(128 | kodi_i_karakterit & 63); }
            else { 임시[쓴수++] = (byte)(240 | kodi_i_karakterit >> 18); 임시[쓴수++] = (byte)(128 | kodi_i_karakterit >> 12 & 63); 임시[쓴수++] = (byte)(128 | kodi_i_karakterit >> 6 & 63); 임시[쓴수++] = (byte)(128 | kodi_i_karakterit & 63); }
        }
        byte[] llogaritje = new byte[쓴수]; System.arraycopy(임시, 0, llogaritje, 0, 쓴수); return llogaritje;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String dekriptoj_të_dhëna(byte[] bajt_VALUE) {
        StringBuilder llogaritje = new StringBuilder();
        for (int Loop_INDEX = 0; Loop_INDEX < bajt_VALUE.length;) {
            int kodi_i_karakterit = bajt_VALUE[Loop_INDEX++] & 255, 수 = kodi_i_karakterit < 128 ? 0 : kodi_i_karakterit >= 194 && kodi_i_karakterit < 224 ? 1 : kodi_i_karakterit >= 224 && kodi_i_karakterit < 240 ? 2 : kodi_i_karakterit >= 240 && kodi_i_karakterit <= 244 ? 3 : -1;
            if (수 < 0 || bajt_VALUE.length - Loop_INDEX < 수) throw new i_pavlefshëm_argument_përjashtim("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) kodi_i_karakterit &= (1 << (6 - 수)) - 1;
            for (int bashkim_i_brendshëm_pozicioni = 0; bashkim_i_brendshëm_pozicioni < 수; bashkim_i_brendshëm_pozicioni++) { int PAS_VALUE = bajt_VALUE[Loop_INDEX++] & 255; if ((PAS_VALUE & 192) != 128) throw new i_pavlefshëm_argument_përjashtim("잘못된 UTF-8"); kodi_i_karakterit = kodi_i_karakterit << 6 | PAS_VALUE & 63; }
            if (kodi_i_karakterit < 최소 || kodi_i_karakterit > 0x10ffff || kodi_i_karakterit >= 0xd800 && kodi_i_karakterit <= 0xdfff) throw new i_pavlefshëm_argument_përjashtim("잘못된 UTF-8");
            if (kodi_i_karakterit < 65536) llogaritje.append((char)kodi_i_karakterit);
            else { kodi_i_karakterit -= 65536; llogaritje.append((char)(0xd800 | kodi_i_karakterit >> 10)); llogaritje.append((char)(0xdc00 | kodi_i_karakterit & 1023)); }
        }
        return llogaritje.toString();
    }
}
