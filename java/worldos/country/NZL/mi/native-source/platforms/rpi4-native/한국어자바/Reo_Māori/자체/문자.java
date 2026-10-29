// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Reo_Māori.자체;
/** 문자(文字), whakawaehere_uara(符號): UTF-8 바이트와 UTF-16 문자열의 CONVERT_uara. whakanoa_uara/조합 입력기는 별개다. */
public final class 문자 {
    public static int paita_COUNT(byte[] raraunga) { return raraunga.length; }
    private 문자() {}
    public static int roa_uara(String Ngā_kupu) { return Ngā_kupu.length(); }
    public static boolean 같음(String 앞, String Hoki_uara) { return 앞 == null ? Hoki_uara == null : 앞.equals(Hoki_uara); }
    public static String whakapiri_TEXT(String 앞, String Hoki_uara) { return 앞.concat(Hoki_uara); }
    public static String tapahi_uara(String Ngā_kupu, int whakahaere, int 끝) { return Ngā_kupu.substring(whakahaere, 끝); }
    public static int poroporo_tau_tōpū(String Ngā_kupu) { try { return Integer.parseInt(Ngā_kupu); } catch (NumberFormatException Pōhēhē) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String tuhi_tau_tōpū_uara(int 수) { return Integer.toString(수); }
    public static int waehere_pūāhua_COUNT(String Ngā_kupu) {
        int 수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Ngā_kupu.length(); Loop_INDEX++, 수++) {
            int waehere_pūāhua = Ngā_kupu.charAt(Loop_INDEX);
            if (waehere_pūāhua >= 0xd800 && waehere_pūāhua <= 0xdbff && Loop_INDEX + 1 < Ngā_kupu.length() && Ngā_kupu.charAt(Loop_INDEX + 1) >= 0xdc00 && Ngā_kupu.charAt(Loop_INDEX + 1) <= 0xdfff) Loop_INDEX++;
        }
        return 수;
    }
    public static byte[] 부호화(String Ngā_kupu) {
        byte[] 임시 = new byte[Ngā_kupu.length() * 3]; int 쓴수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Ngā_kupu.length(); Loop_INDEX++) {
            int waehere_pūāhua = Ngā_kupu.charAt(Loop_INDEX);
            if (waehere_pūāhua >= 0xd800 && waehere_pūāhua <= 0xdbff && Loop_INDEX + 1 < Ngā_kupu.length() && Ngā_kupu.charAt(Loop_INDEX + 1) >= 0xdc00 && Ngā_kupu.charAt(Loop_INDEX + 1) <= 0xdfff) waehere_pūāhua = 0x10000 + ((waehere_pūāhua - 0xd800) << 10) + Ngā_kupu.charAt(++Loop_INDEX) - 0xdc00;
            else if (waehere_pūāhua >= 0xd800 && waehere_pūāhua <= 0xdfff) waehere_pūāhua = '?';
            if (waehere_pūāhua < 128) 임시[쓴수++] = (byte)waehere_pūāhua;
            else if (waehere_pūāhua < 2048) { 임시[쓴수++] = (byte)(192 | waehere_pūāhua >> 6); 임시[쓴수++] = (byte)(128 | waehere_pūāhua & 63); }
            else if (waehere_pūāhua < 65536) { 임시[쓴수++] = (byte)(224 | waehere_pūāhua >> 12); 임시[쓴수++] = (byte)(128 | waehere_pūāhua >> 6 & 63); 임시[쓴수++] = (byte)(128 | waehere_pūāhua & 63); }
            else { 임시[쓴수++] = (byte)(240 | waehere_pūāhua >> 18); 임시[쓴수++] = (byte)(128 | waehere_pūāhua >> 12 & 63); 임시[쓴수++] = (byte)(128 | waehere_pūāhua >> 6 & 63); 임시[쓴수++] = (byte)(128 | waehere_pūāhua & 63); }
        }
        byte[] mēhua = new byte[쓴수]; System.arraycopy(임시, 0, mēhua, 0, 쓴수); return mēhua;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String wetemuna_raraunga(byte[] paita_uara) {
        StringBuilder mēhua = new StringBuilder();
        for (int Loop_INDEX = 0; Loop_INDEX < paita_uara.length;) {
            int waehere_pūāhua = paita_uara[Loop_INDEX++] & 255, 수 = waehere_pūāhua < 128 ? 0 : waehere_pūāhua >= 194 && waehere_pūāhua < 224 ? 1 : waehere_pūāhua >= 224 && waehere_pūāhua < 240 ? 2 : waehere_pūāhua >= 240 && waehere_pūāhua <= 244 ? 3 : -1;
            if (수 < 0 || paita_uara.length - Loop_INDEX < 수) throw new 잘못된인수예외("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) waehere_pūāhua &= (1 << (6 - 수)) - 1;
            for (int hono_roto_tūranga = 0; hono_roto_tūranga < 수; hono_roto_tūranga++) { int Hoki_uara = paita_uara[Loop_INDEX++] & 255; if ((Hoki_uara & 192) != 128) throw new 잘못된인수예외("잘못된 UTF-8"); waehere_pūāhua = waehere_pūāhua << 6 | Hoki_uara & 63; }
            if (waehere_pūāhua < 최소 || waehere_pūāhua > 0x10ffff || waehere_pūāhua >= 0xd800 && waehere_pūāhua <= 0xdfff) throw new 잘못된인수예외("잘못된 UTF-8");
            if (waehere_pūāhua < 65536) mēhua.append((char)waehere_pūāhua);
            else { waehere_pūāhua -= 65536; mēhua.append((char)(0xd800 | waehere_pūāhua >> 10)); mēhua.append((char)(0xdc00 | waehere_pūāhua & 1023)); }
        }
        return mēhua.toString();
    }
}
