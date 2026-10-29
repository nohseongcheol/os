// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Cymraeg.자체;
/** 문자(文字), amgodio_VALUE(符號): UTF-8 바이트와 UTF-16 문자열의 CONVERT_VALUE. normaleiddio_VALUE/조합 입력기는 별개다. */
public final class 문자 {
    public static int beit_COUNT(byte[] data) { return data.length; }
    private 문자() {}
    public static int hyd_VALUE(String Testun) { return Testun.length(); }
    public static boolean 같음(String 앞, String BACK_VALUE) { return 앞 == null ? BACK_VALUE == null : 앞.equals(BACK_VALUE); }
    public static String gludo_SMS(String 앞, String BACK_VALUE) { return 앞.concat(BACK_VALUE); }
    public static String torri_VALUE(String Testun, int Gweithredu_2, int 끝) { return Testun.substring(Gweithredu_2, 끝); }
    public static int dosrannu_cyfanrif(String Testun) { try { return Integer.parseInt(Testun); } catch (NumberFormatException Gwall) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String ysgrifennu_cyfanrif_VALUE(int 수) { return Integer.toString(수); }
    public static int cod_nod_COUNT(String Testun) {
        int 수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Testun.length(); Loop_INDEX++, 수++) {
            int cod_nod = Testun.charAt(Loop_INDEX);
            if (cod_nod >= 0xd800 && cod_nod <= 0xdbff && Loop_INDEX + 1 < Testun.length() && Testun.charAt(Loop_INDEX + 1) >= 0xdc00 && Testun.charAt(Loop_INDEX + 1) <= 0xdfff) Loop_INDEX++;
        }
        return 수;
    }
    public static byte[] 부호화(String Testun) {
        byte[] 임시 = new byte[Testun.length() * 3]; int 쓴수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Testun.length(); Loop_INDEX++) {
            int cod_nod = Testun.charAt(Loop_INDEX);
            if (cod_nod >= 0xd800 && cod_nod <= 0xdbff && Loop_INDEX + 1 < Testun.length() && Testun.charAt(Loop_INDEX + 1) >= 0xdc00 && Testun.charAt(Loop_INDEX + 1) <= 0xdfff) cod_nod = 0x10000 + ((cod_nod - 0xd800) << 10) + Testun.charAt(++Loop_INDEX) - 0xdc00;
            else if (cod_nod >= 0xd800 && cod_nod <= 0xdfff) cod_nod = '?';
            if (cod_nod < 128) 임시[쓴수++] = (byte)cod_nod;
            else if (cod_nod < 2048) { 임시[쓴수++] = (byte)(192 | cod_nod >> 6); 임시[쓴수++] = (byte)(128 | cod_nod & 63); }
            else if (cod_nod < 65536) { 임시[쓴수++] = (byte)(224 | cod_nod >> 12); 임시[쓴수++] = (byte)(128 | cod_nod >> 6 & 63); 임시[쓴수++] = (byte)(128 | cod_nod & 63); }
            else { 임시[쓴수++] = (byte)(240 | cod_nod >> 18); 임시[쓴수++] = (byte)(128 | cod_nod >> 12 & 63); 임시[쓴수++] = (byte)(128 | cod_nod >> 6 & 63); 임시[쓴수++] = (byte)(128 | cod_nod & 63); }
        }
        byte[] mesur = new byte[쓴수]; System.arraycopy(임시, 0, mesur, 0, 쓴수); return mesur;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String dadgryptio_data(byte[] beit_VALUE) {
        StringBuilder mesur = new StringBuilder();
        for (int Loop_INDEX = 0; Loop_INDEX < beit_VALUE.length;) {
            int cod_nod = beit_VALUE[Loop_INDEX++] & 255, 수 = cod_nod < 128 ? 0 : cod_nod >= 194 && cod_nod < 224 ? 1 : cod_nod >= 224 && cod_nod < 240 ? 2 : cod_nod >= 240 && cod_nod <= 244 ? 3 : -1;
            if (수 < 0 || beit_VALUE.length - Loop_INDEX < 수) throw new annilys_arg_eithriad("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) cod_nod &= (1 << (6 - 수)) - 1;
            for (int uno_mewnol_safle = 0; uno_mewnol_safle < 수; uno_mewnol_safle++) { int BACK_VALUE = beit_VALUE[Loop_INDEX++] & 255; if ((BACK_VALUE & 192) != 128) throw new annilys_arg_eithriad("잘못된 UTF-8"); cod_nod = cod_nod << 6 | BACK_VALUE & 63; }
            if (cod_nod < 최소 || cod_nod > 0x10ffff || cod_nod >= 0xd800 && cod_nod <= 0xdfff) throw new annilys_arg_eithriad("잘못된 UTF-8");
            if (cod_nod < 65536) mesur.append((char)cod_nod);
            else { cod_nod -= 65536; mesur.append((char)(0xd800 | cod_nod >> 10)); mesur.append((char)(0xdc00 | cod_nod & 1023)); }
        }
        return mesur.toString();
    }
}
