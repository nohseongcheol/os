// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 문자(文字), go_enkhouta_boleng(符號): UTF-8 바이트와 UTF-16 문자열의 변환. fokotša_kopišo_boleng/조합 입력기는 별개다. */
public final class 문자 {
    public static int 바이트수(byte[] data) { return data.length; }
    private 문자() {}
    public static int botelele_boleng(String Sengwalwa) { return Sengwalwa.length(); }
    public static boolean 같음(String 앞, String Morago_boleng) { return 앞 == null ? Morago_boleng == null : 앞.equals(Morago_boleng); }
    public static String pheista_SMS(String 앞, String Morago_boleng) { return 앞.concat(Morago_boleng); }
    public static String sega_boleng(String Sengwalwa, int Diriša, int 끝) { return Sengwalwa.substring(Diriša, 끝); }
    public static int ripaganya_palotlalo(String Sengwalwa) { try { return Integer.parseInt(Sengwalwa); } catch (NumberFormatException Phošo) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String ngwala_palotlalo_boleng(int 수) { return Integer.toString(수); }
    public static int 코드포인트수(String Sengwalwa) {
        int 수 = 0;
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < Sengwalwa.length(); ditaelopoeletšwa_lokela++, 수++) {
            int khouto_ya_tlhaka = Sengwalwa.charAt(ditaelopoeletšwa_lokela);
            if (khouto_ya_tlhaka >= 0xd800 && khouto_ya_tlhaka <= 0xdbff && ditaelopoeletšwa_lokela + 1 < Sengwalwa.length() && Sengwalwa.charAt(ditaelopoeletšwa_lokela + 1) >= 0xdc00 && Sengwalwa.charAt(ditaelopoeletšwa_lokela + 1) <= 0xdfff) ditaelopoeletšwa_lokela++;
        }
        return 수;
    }
    public static byte[] 부호화(String Sengwalwa) {
        byte[] 임시 = new byte[Sengwalwa.length() * 3]; int 쓴수 = 0;
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < Sengwalwa.length(); ditaelopoeletšwa_lokela++) {
            int khouto_ya_tlhaka = Sengwalwa.charAt(ditaelopoeletšwa_lokela);
            if (khouto_ya_tlhaka >= 0xd800 && khouto_ya_tlhaka <= 0xdbff && ditaelopoeletšwa_lokela + 1 < Sengwalwa.length() && Sengwalwa.charAt(ditaelopoeletšwa_lokela + 1) >= 0xdc00 && Sengwalwa.charAt(ditaelopoeletšwa_lokela + 1) <= 0xdfff) khouto_ya_tlhaka = 0x10000 + ((khouto_ya_tlhaka - 0xd800) << 10) + Sengwalwa.charAt(++ditaelopoeletšwa_lokela) - 0xdc00;
            else if (khouto_ya_tlhaka >= 0xd800 && khouto_ya_tlhaka <= 0xdfff) khouto_ya_tlhaka = '?';
            if (khouto_ya_tlhaka < 128) 임시[쓴수++] = (byte)khouto_ya_tlhaka;
            else if (khouto_ya_tlhaka < 2048) { 임시[쓴수++] = (byte)(192 | khouto_ya_tlhaka >> 6); 임시[쓴수++] = (byte)(128 | khouto_ya_tlhaka & 63); }
            else if (khouto_ya_tlhaka < 65536) { 임시[쓴수++] = (byte)(224 | khouto_ya_tlhaka >> 12); 임시[쓴수++] = (byte)(128 | khouto_ya_tlhaka >> 6 & 63); 임시[쓴수++] = (byte)(128 | khouto_ya_tlhaka & 63); }
            else { 임시[쓴수++] = (byte)(240 | khouto_ya_tlhaka >> 18); 임시[쓴수++] = (byte)(128 | khouto_ya_tlhaka >> 12 & 63); 임시[쓴수++] = (byte)(128 | khouto_ya_tlhaka >> 6 & 63); 임시[쓴수++] = (byte)(128 | khouto_ya_tlhaka & 63); }
        }
        byte[] 결과 = new byte[쓴수]; System.arraycopy(임시, 0, 결과, 0, 쓴수); return 결과;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String boetša_sekeng_data(byte[] paete_boleng) {
        StringBuilder 결과 = new StringBuilder();
        for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < paete_boleng.length;) {
            int khouto_ya_tlhaka = paete_boleng[ditaelopoeletšwa_lokela++] & 255, 수 = khouto_ya_tlhaka < 128 ? 0 : khouto_ya_tlhaka >= 194 && khouto_ya_tlhaka < 224 ? 1 : khouto_ya_tlhaka >= 224 && khouto_ya_tlhaka < 240 ? 2 : khouto_ya_tlhaka >= 240 && khouto_ya_tlhaka <= 244 ? 3 : -1;
            if (수 < 0 || paete_boleng.length - ditaelopoeletšwa_lokela < 수) throw new 잘못된인수예외("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) khouto_ya_tlhaka &= (1 << (6 - 수)) - 1;
            for (int 안쪽자리 = 0; 안쪽자리 < 수; 안쪽자리++) { int Morago_boleng = paete_boleng[ditaelopoeletšwa_lokela++] & 255; if ((Morago_boleng & 192) != 128) throw new 잘못된인수예외("잘못된 UTF-8"); khouto_ya_tlhaka = khouto_ya_tlhaka << 6 | Morago_boleng & 63; }
            if (khouto_ya_tlhaka < 최소 || khouto_ya_tlhaka > 0x10ffff || khouto_ya_tlhaka >= 0xd800 && khouto_ya_tlhaka <= 0xdfff) throw new 잘못된인수예외("잘못된 UTF-8");
            if (khouto_ya_tlhaka < 65536) 결과.append((char)khouto_ya_tlhaka);
            else { khouto_ya_tlhaka -= 65536; 결과.append((char)(0xd800 | khouto_ya_tlhaka >> 10)); 결과.append((char)(0xdc00 | khouto_ya_tlhaka & 1023)); }
        }
        return 결과.toString();
    }
}
