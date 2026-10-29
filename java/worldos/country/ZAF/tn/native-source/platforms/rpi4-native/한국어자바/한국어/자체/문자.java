// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 문자(文字), khoutufatso_Boleng(符號): UTF-8 바이트와 UTF-16 문자열의 변환. fokotsa_ntsifatso_Boleng/조합 입력기는 별개다. */
public final class 문자 {
    public static int 바이트수(byte[] tshedimosetso) { return tshedimosetso.length; }
    private 문자() {}
    public static int boleele_Boleng(String SMS) { return SMS.length(); }
    public static boolean 같음(String 앞, String Morago_Boleng) { return 앞 == null ? Morago_Boleng == null : 앞.equals(Morago_Boleng); }
    public static String kgomaretsa_SMS(String 앞, String Morago_Boleng) { return 앞.concat(Morago_Boleng); }
    public static String sega_Boleng(String SMS, int dirisa, int 끝) { return SMS.substring(dirisa, 끝); }
    public static int go_lokolola_Palotlalo(String SMS) { try { return Integer.parseInt(SMS); } catch (NumberFormatException phoso) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String kwala_Palotlalo_Boleng(int 수) { return Integer.toString(수); }
    public static int 코드포인트수(String SMS) {
        int 수 = 0;
        for (int lupu_tshupane = 0; lupu_tshupane < SMS.length(); lupu_tshupane++, 수++) {
            int khoutuletshwao = SMS.charAt(lupu_tshupane);
            if (khoutuletshwao >= 0xd800 && khoutuletshwao <= 0xdbff && lupu_tshupane + 1 < SMS.length() && SMS.charAt(lupu_tshupane + 1) >= 0xdc00 && SMS.charAt(lupu_tshupane + 1) <= 0xdfff) lupu_tshupane++;
        }
        return 수;
    }
    public static byte[] 부호화(String SMS) {
        byte[] 임시 = new byte[SMS.length() * 3]; int 쓴수 = 0;
        for (int lupu_tshupane = 0; lupu_tshupane < SMS.length(); lupu_tshupane++) {
            int khoutuletshwao = SMS.charAt(lupu_tshupane);
            if (khoutuletshwao >= 0xd800 && khoutuletshwao <= 0xdbff && lupu_tshupane + 1 < SMS.length() && SMS.charAt(lupu_tshupane + 1) >= 0xdc00 && SMS.charAt(lupu_tshupane + 1) <= 0xdfff) khoutuletshwao = 0x10000 + ((khoutuletshwao - 0xd800) << 10) + SMS.charAt(++lupu_tshupane) - 0xdc00;
            else if (khoutuletshwao >= 0xd800 && khoutuletshwao <= 0xdfff) khoutuletshwao = '?';
            if (khoutuletshwao < 128) 임시[쓴수++] = (byte)khoutuletshwao;
            else if (khoutuletshwao < 2048) { 임시[쓴수++] = (byte)(192 | khoutuletshwao >> 6); 임시[쓴수++] = (byte)(128 | khoutuletshwao & 63); }
            else if (khoutuletshwao < 65536) { 임시[쓴수++] = (byte)(224 | khoutuletshwao >> 12); 임시[쓴수++] = (byte)(128 | khoutuletshwao >> 6 & 63); 임시[쓴수++] = (byte)(128 | khoutuletshwao & 63); }
            else { 임시[쓴수++] = (byte)(240 | khoutuletshwao >> 18); 임시[쓴수++] = (byte)(128 | khoutuletshwao >> 12 & 63); 임시[쓴수++] = (byte)(128 | khoutuletshwao >> 6 & 63); 임시[쓴수++] = (byte)(128 | khoutuletshwao & 63); }
        }
        byte[] 결과 = new byte[쓴수]; System.arraycopy(임시, 0, 결과, 0, 쓴수); return 결과;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String Sirolola_tshedimosetso(byte[] baete_Boleng) {
        StringBuilder 결과 = new StringBuilder();
        for (int lupu_tshupane = 0; lupu_tshupane < baete_Boleng.length;) {
            int khoutuletshwao = baete_Boleng[lupu_tshupane++] & 255, 수 = khoutuletshwao < 128 ? 0 : khoutuletshwao >= 194 && khoutuletshwao < 224 ? 1 : khoutuletshwao >= 224 && khoutuletshwao < 240 ? 2 : khoutuletshwao >= 240 && khoutuletshwao <= 244 ? 3 : -1;
            if (수 < 0 || baete_Boleng.length - lupu_tshupane < 수) throw new 잘못된인수예외("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) khoutuletshwao &= (1 << (6 - 수)) - 1;
            for (int 안쪽자리 = 0; 안쪽자리 < 수; 안쪽자리++) { int Morago_Boleng = baete_Boleng[lupu_tshupane++] & 255; if ((Morago_Boleng & 192) != 128) throw new 잘못된인수예외("잘못된 UTF-8"); khoutuletshwao = khoutuletshwao << 6 | Morago_Boleng & 63; }
            if (khoutuletshwao < 최소 || khoutuletshwao > 0x10ffff || khoutuletshwao >= 0xd800 && khoutuletshwao <= 0xdfff) throw new 잘못된인수예외("잘못된 UTF-8");
            if (khoutuletshwao < 65536) 결과.append((char)khoutuletshwao);
            else { khoutuletshwao -= 65536; 결과.append((char)(0xd800 | khoutuletshwao >> 10)); 결과.append((char)(0xdc00 | khoutuletshwao & 1023)); }
        }
        return 결과.toString();
    }
}
