// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Македонски.자체;
/** 문자(文字), кодирање_VALUE(符號): UTF-8 바이트와 UTF-16 문자열의 CONVERT_VALUE. нормализирање_VALUE/조합 입력기는 별개다. */
public final class 문자 {
    public static int бајт_COUNT(byte[] податоци) { return податоци.length; }
    private 문자() {}
    public static int должина_VALUE(String Текст) { return Текст.length(); }
    public static boolean 같음(String предна_VALUE, String Назад_VALUE) { return предна_VALUE == null ? Назад_VALUE == null : предна_VALUE.equals(Назад_VALUE); }
    public static String залепи_СМС(String предна_VALUE, String Назад_VALUE) { return предна_VALUE.concat(Назад_VALUE); }
    public static String отсечи_VALUE(String Текст, int Изврши_2, int 끝) { return Текст.substring(Изврши_2, 끝); }
    public static int разложи_цел_број(String Текст) { try { return Integer.parseInt(Текст); } catch (NumberFormatException ГРЕШКА) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String запиши_цел_број_VALUE(int 수) { return Integer.toString(수); }
    public static int кодна_точка_COUNT(String Текст) {
        int 수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Текст.length(); Loop_INDEX++, 수++) {
            int кодна_точка = Текст.charAt(Loop_INDEX);
            if (кодна_точка >= 0xd800 && кодна_точка <= 0xdbff && Loop_INDEX + 1 < Текст.length() && Текст.charAt(Loop_INDEX + 1) >= 0xdc00 && Текст.charAt(Loop_INDEX + 1) <= 0xdfff) Loop_INDEX++;
        }
        return 수;
    }
    public static byte[] 부호화(String Текст) {
        byte[] 임시 = new byte[Текст.length() * 3]; int 쓴수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Текст.length(); Loop_INDEX++) {
            int кодна_точка = Текст.charAt(Loop_INDEX);
            if (кодна_точка >= 0xd800 && кодна_точка <= 0xdbff && Loop_INDEX + 1 < Текст.length() && Текст.charAt(Loop_INDEX + 1) >= 0xdc00 && Текст.charAt(Loop_INDEX + 1) <= 0xdfff) кодна_точка = 0x10000 + ((кодна_точка - 0xd800) << 10) + Текст.charAt(++Loop_INDEX) - 0xdc00;
            else if (кодна_точка >= 0xd800 && кодна_точка <= 0xdfff) кодна_точка = '?';
            if (кодна_точка < 128) 임시[쓴수++] = (byte)кодна_точка;
            else if (кодна_точка < 2048) { 임시[쓴수++] = (byte)(192 | кодна_точка >> 6); 임시[쓴수++] = (byte)(128 | кодна_точка & 63); }
            else if (кодна_точка < 65536) { 임시[쓴수++] = (byte)(224 | кодна_точка >> 12); 임시[쓴수++] = (byte)(128 | кодна_точка >> 6 & 63); 임시[쓴수++] = (byte)(128 | кодна_точка & 63); }
            else { 임시[쓴수++] = (byte)(240 | кодна_точка >> 18); 임시[쓴수++] = (byte)(128 | кодна_точка >> 12 & 63); 임시[쓴수++] = (byte)(128 | кодна_точка >> 6 & 63); 임시[쓴수++] = (byte)(128 | кодна_точка & 63); }
        }
        byte[] мерка = new byte[쓴수]; System.arraycopy(임시, 0, мерка, 0, 쓴수); return мерка;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String дешифрирај_податоци(byte[] бајт_VALUE) {
        StringBuilder мерка = new StringBuilder();
        for (int Loop_INDEX = 0; Loop_INDEX < бајт_VALUE.length;) {
            int кодна_точка = бајт_VALUE[Loop_INDEX++] & 255, 수 = кодна_точка < 128 ? 0 : кодна_точка >= 194 && кодна_точка < 224 ? 1 : кодна_точка >= 224 && кодна_точка < 240 ? 2 : кодна_точка >= 240 && кодна_точка <= 244 ? 3 : -1;
            if (수 < 0 || бајт_VALUE.length - Loop_INDEX < 수) throw new неважечки_аргумент_исклучок("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) кодна_точка &= (1 << (6 - 수)) - 1;
            for (int внатрешно_поврзување_позиционирање = 0; внатрешно_поврзување_позиционирање < 수; внатрешно_поврзување_позиционирање++) { int Назад_VALUE = бајт_VALUE[Loop_INDEX++] & 255; if ((Назад_VALUE & 192) != 128) throw new неважечки_аргумент_исклучок("잘못된 UTF-8"); кодна_точка = кодна_точка << 6 | Назад_VALUE & 63; }
            if (кодна_точка < 최소 || кодна_точка > 0x10ffff || кодна_точка >= 0xd800 && кодна_точка <= 0xdfff) throw new неважечки_аргумент_исклучок("잘못된 UTF-8");
            if (кодна_точка < 65536) мерка.append((char)кодна_точка);
            else { кодна_точка -= 65536; мерка.append((char)(0xd800 | кодна_точка >> 10)); мерка.append((char)(0xdc00 | кодна_точка & 1023)); }
        }
        return мерка.toString();
    }
}
