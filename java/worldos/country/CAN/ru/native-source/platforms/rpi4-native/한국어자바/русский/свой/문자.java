// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package русский.свой;
/** 문자(文字), кодирование_ЗНАЧЕН(符號): UTF-8 바이트와 UTF-16 문자열의 ПРЕОБР_ЗНАЧЕН. нормализовать_ЗНАЧЕН/состав_ЗНАЧЕН 입력기는 별개다. */
public final class 문자 {
    public static int байт_СЧЁТ(byte[] данные) { return данные.length; }
    private 문자() {}
    public static int длина_ЗНАЧЕН(String текст) { return текст.length(); }
    public static boolean 같음(String лицевая_камера_ЗНАЧЕН, String BACK_ЗНАЧЕН) { return лицевая_камера_ЗНАЧЕН == null ? BACK_ЗНАЧЕН == null : лицевая_камера_ЗНАЧЕН.equals(BACK_ЗНАЧЕН); }
    public static String вставить_SMS(String лицевая_камера_ЗНАЧЕН, String BACK_ЗНАЧЕН) { return лицевая_камера_ЗНАЧЕН.concat(BACK_ЗНАЧЕН); }
    public static String вырезать_ЗНАЧЕН(String текст, int запустить, int 끝) { return текст.substring(запустить, 끝); }
    public static int анализировать_целое_число(String текст) { try { return Integer.parseInt(текст); } catch (NumberFormatException ошибка) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String запись_целое_число_ЗНАЧЕН(int 수) { return Integer.toString(수); }
    public static int код_знака_СЧЁТ(String текст) {
        int 수 = 0;
        for (int Loop_ИНДЕКС = 0; Loop_ИНДЕКС < текст.length(); Loop_ИНДЕКС++, 수++) {
            int код_знака = текст.charAt(Loop_ИНДЕКС);
            if (код_знака >= 0xd800 && код_знака <= 0xdbff && Loop_ИНДЕКС + 1 < текст.length() && текст.charAt(Loop_ИНДЕКС + 1) >= 0xdc00 && текст.charAt(Loop_ИНДЕКС + 1) <= 0xdfff) Loop_ИНДЕКС++;
        }
        return 수;
    }
    public static byte[] кодировать(String текст) {
        byte[] 임시 = new byte[текст.length() * 3]; int 쓴수 = 0;
        for (int Loop_ИНДЕКС = 0; Loop_ИНДЕКС < текст.length(); Loop_ИНДЕКС++) {
            int код_знака = текст.charAt(Loop_ИНДЕКС);
            if (код_знака >= 0xd800 && код_знака <= 0xdbff && Loop_ИНДЕКС + 1 < текст.length() && текст.charAt(Loop_ИНДЕКС + 1) >= 0xdc00 && текст.charAt(Loop_ИНДЕКС + 1) <= 0xdfff) код_знака = 0x10000 + ((код_знака - 0xd800) << 10) + текст.charAt(++Loop_ИНДЕКС) - 0xdc00;
            else if (код_знака >= 0xd800 && код_знака <= 0xdfff) код_знака = '?';
            if (код_знака < 128) 임시[쓴수++] = (byte)код_знака;
            else if (код_знака < 2048) { 임시[쓴수++] = (byte)(192 | код_знака >> 6); 임시[쓴수++] = (byte)(128 | код_знака & 63); }
            else if (код_знака < 65536) { 임시[쓴수++] = (byte)(224 | код_знака >> 12); 임시[쓴수++] = (byte)(128 | код_знака >> 6 & 63); 임시[쓴수++] = (byte)(128 | код_знака & 63); }
            else { 임시[쓴수++] = (byte)(240 | код_знака >> 18); 임시[쓴수++] = (byte)(128 | код_знака >> 12 & 63); 임시[쓴수++] = (byte)(128 | код_знака >> 6 & 63); 임시[쓴수++] = (byte)(128 | код_знака & 63); }
        }
        byte[] результат = new byte[쓴수]; System.arraycopy(임시, 0, результат, 0, 쓴수); return результат;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String расшифровать_данные(byte[] байт_ЗНАЧЕН) {
        StringBuilder результат = new StringBuilder();
        for (int Loop_ИНДЕКС = 0; Loop_ИНДЕКС < байт_ЗНАЧЕН.length;) {
            int код_знака = байт_ЗНАЧЕН[Loop_ИНДЕКС++] & 255, 수 = код_знака < 128 ? 0 : код_знака >= 194 && код_знака < 224 ? 1 : код_знака >= 224 && код_знака < 240 ? 2 : код_знака >= 240 && код_знака <= 244 ? 3 : -1;
            if (수 < 0 || байт_ЗНАЧЕН.length - Loop_ИНДЕКС < 수) throw new неверный_аргумент_исключение("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) код_знака &= (1 << (6 - 수)) - 1;
            for (int внутреннее_соединение_позиция = 0; внутреннее_соединение_позиция < 수; внутреннее_соединение_позиция++) { int BACK_ЗНАЧЕН = байт_ЗНАЧЕН[Loop_ИНДЕКС++] & 255; if ((BACK_ЗНАЧЕН & 192) != 128) throw new неверный_аргумент_исключение("잘못된 UTF-8"); код_знака = код_знака << 6 | BACK_ЗНАЧЕН & 63; }
            if (код_знака < 최소 || код_знака > 0x10ffff || код_знака >= 0xd800 && код_знака <= 0xdfff) throw new неверный_аргумент_исключение("잘못된 UTF-8");
            if (код_знака < 65536) результат.append((char)код_знака);
            else { код_знака -= 65536; результат.append((char)(0xd800 | код_знака >> 10)); результат.append((char)(0xdc00 | код_знака & 1023)); }
        }
        return результат.toString();
    }
}
