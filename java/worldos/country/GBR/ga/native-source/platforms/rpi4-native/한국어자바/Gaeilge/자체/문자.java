// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Gaeilge.자체;
/** 문자(文字), ionchódú_VALUE(符號): UTF-8 바이트와 UTF-16 문자열의 CONVERT_VALUE. normalaigh_VALUE/조합 입력기는 별개다. */
public final class 문자 {
    public static int beart_COUNT(byte[] sonraí) { return sonraí.length; }
    private 문자() {}
    public static int fad_VALUE(String Téacs) { return Téacs.length(); }
    public static boolean 같음(String 앞, String Siar_VALUE) { return 앞 == null ? Siar_VALUE == null : 앞.equals(Siar_VALUE); }
    public static String greamaigh_SMS(String 앞, String Siar_VALUE) { return 앞.concat(Siar_VALUE); }
    public static String gearr_VALUE(String Téacs, int Rith_2, int 끝) { return Téacs.substring(Rith_2, 끝); }
    public static int parsáil_slánuimhir(String Téacs) { try { return Integer.parseInt(Téacs); } catch (NumberFormatException ERREÁID) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String scríobh_slánuimhir_VALUE(int 수) { return Integer.toString(수); }
    public static int pointe_cóid_COUNT(String Téacs) {
        int 수 = 0;
        for (int lúb_INDEX = 0; lúb_INDEX < Téacs.length(); lúb_INDEX++, 수++) {
            int pointe_cóid = Téacs.charAt(lúb_INDEX);
            if (pointe_cóid >= 0xd800 && pointe_cóid <= 0xdbff && lúb_INDEX + 1 < Téacs.length() && Téacs.charAt(lúb_INDEX + 1) >= 0xdc00 && Téacs.charAt(lúb_INDEX + 1) <= 0xdfff) lúb_INDEX++;
        }
        return 수;
    }
    public static byte[] 부호화(String Téacs) {
        byte[] 임시 = new byte[Téacs.length() * 3]; int 쓴수 = 0;
        for (int lúb_INDEX = 0; lúb_INDEX < Téacs.length(); lúb_INDEX++) {
            int pointe_cóid = Téacs.charAt(lúb_INDEX);
            if (pointe_cóid >= 0xd800 && pointe_cóid <= 0xdbff && lúb_INDEX + 1 < Téacs.length() && Téacs.charAt(lúb_INDEX + 1) >= 0xdc00 && Téacs.charAt(lúb_INDEX + 1) <= 0xdfff) pointe_cóid = 0x10000 + ((pointe_cóid - 0xd800) << 10) + Téacs.charAt(++lúb_INDEX) - 0xdc00;
            else if (pointe_cóid >= 0xd800 && pointe_cóid <= 0xdfff) pointe_cóid = '?';
            if (pointe_cóid < 128) 임시[쓴수++] = (byte)pointe_cóid;
            else if (pointe_cóid < 2048) { 임시[쓴수++] = (byte)(192 | pointe_cóid >> 6); 임시[쓴수++] = (byte)(128 | pointe_cóid & 63); }
            else if (pointe_cóid < 65536) { 임시[쓴수++] = (byte)(224 | pointe_cóid >> 12); 임시[쓴수++] = (byte)(128 | pointe_cóid >> 6 & 63); 임시[쓴수++] = (byte)(128 | pointe_cóid & 63); }
            else { 임시[쓴수++] = (byte)(240 | pointe_cóid >> 18); 임시[쓴수++] = (byte)(128 | pointe_cóid >> 12 & 63); 임시[쓴수++] = (byte)(128 | pointe_cóid >> 6 & 63); 임시[쓴수++] = (byte)(128 | pointe_cóid & 63); }
        }
        byte[] tomhas = new byte[쓴수]; System.arraycopy(임시, 0, tomhas, 0, 쓴수); return tomhas;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String díchriptigh_sonraí(byte[] beart_VALUE) {
        StringBuilder tomhas = new StringBuilder();
        for (int lúb_INDEX = 0; lúb_INDEX < beart_VALUE.length;) {
            int pointe_cóid = beart_VALUE[lúb_INDEX++] & 255, 수 = pointe_cóid < 128 ? 0 : pointe_cóid >= 194 && pointe_cóid < 224 ? 1 : pointe_cóid >= 224 && pointe_cóid < 240 ? 2 : pointe_cóid >= 240 && pointe_cóid <= 244 ? 3 : -1;
            if (수 < 0 || beart_VALUE.length - lúb_INDEX < 수) throw new neamhbhailí_argóint_eisceacht("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) pointe_cóid &= (1 << (6 - 수)) - 1;
            for (int comhcheangal_istigh_suíomh = 0; comhcheangal_istigh_suíomh < 수; comhcheangal_istigh_suíomh++) { int Siar_VALUE = beart_VALUE[lúb_INDEX++] & 255; if ((Siar_VALUE & 192) != 128) throw new neamhbhailí_argóint_eisceacht("잘못된 UTF-8"); pointe_cóid = pointe_cóid << 6 | Siar_VALUE & 63; }
            if (pointe_cóid < 최소 || pointe_cóid > 0x10ffff || pointe_cóid >= 0xd800 && pointe_cóid <= 0xdfff) throw new neamhbhailí_argóint_eisceacht("잘못된 UTF-8");
            if (pointe_cóid < 65536) tomhas.append((char)pointe_cóid);
            else { pointe_cóid -= 65536; tomhas.append((char)(0xd800 | pointe_cóid >> 10)); tomhas.append((char)(0xdc00 | pointe_cóid & 1023)); }
        }
        return tomhas.toString();
    }
}
