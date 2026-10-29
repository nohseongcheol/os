// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eesti.oma;
/** 문자(文字), kodeerimine_VALUE(符號): UTF-8 바이트와 UTF-16 문자열의 CONVERT_VALUE. normaliseerima_VALUE/koosseis_VALUE 입력기는 별개다. */
public final class 문자 {
    public static int bait_COUNT(byte[] andmed) { return andmed.length; }
    private 문자() {}
    public static int 길이(String Tekst) { return Tekst.length(); }
    public static boolean 같음(String esikaamera_VALUE, String Tagasi_VALUE) { return esikaamera_VALUE == null ? Tagasi_VALUE == null : esikaamera_VALUE.equals(Tagasi_VALUE); }
    public static String kleepima_SMS(String esikaamera_VALUE, String Tagasi_VALUE) { return esikaamera_VALUE.concat(Tagasi_VALUE); }
    public static String lõikama_VALUE(String Tekst, int Käivita_2, int 끝) { return Tekst.substring(Käivita_2, 끝); }
    public static int sõeluma_täisarv(String Tekst) { try { return Integer.parseInt(Tekst); } catch (NumberFormatException VIGA) { throw new number_vorming_tõrge("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String kirjutamine_täisarv_VALUE(int number) { return Integer.toString(number); }
    public static int koodipunkt_COUNT(String Tekst) {
        int number = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Tekst.length(); Loop_INDEX++, number++) {
            int koodipunkt = Tekst.charAt(Loop_INDEX);
            if (koodipunkt >= 0xd800 && koodipunkt <= 0xdbff && Loop_INDEX + 1 < Tekst.length() && Tekst.charAt(Loop_INDEX + 1) >= 0xdc00 && Tekst.charAt(Loop_INDEX + 1) <= 0xdfff) Loop_INDEX++;
        }
        return number;
    }
    public static byte[] kodeerima(String Tekst) {
        byte[] 임시 = new byte[Tekst.length() * 3]; int 쓴수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Tekst.length(); Loop_INDEX++) {
            int koodipunkt = Tekst.charAt(Loop_INDEX);
            if (koodipunkt >= 0xd800 && koodipunkt <= 0xdbff && Loop_INDEX + 1 < Tekst.length() && Tekst.charAt(Loop_INDEX + 1) >= 0xdc00 && Tekst.charAt(Loop_INDEX + 1) <= 0xdfff) koodipunkt = 0x10000 + ((koodipunkt - 0xd800) << 10) + Tekst.charAt(++Loop_INDEX) - 0xdc00;
            else if (koodipunkt >= 0xd800 && koodipunkt <= 0xdfff) koodipunkt = '?';
            if (koodipunkt < 128) 임시[쓴수++] = (byte)koodipunkt;
            else if (koodipunkt < 2048) { 임시[쓴수++] = (byte)(192 | koodipunkt >> 6); 임시[쓴수++] = (byte)(128 | koodipunkt & 63); }
            else if (koodipunkt < 65536) { 임시[쓴수++] = (byte)(224 | koodipunkt >> 12); 임시[쓴수++] = (byte)(128 | koodipunkt >> 6 & 63); 임시[쓴수++] = (byte)(128 | koodipunkt & 63); }
            else { 임시[쓴수++] = (byte)(240 | koodipunkt >> 18); 임시[쓴수++] = (byte)(128 | koodipunkt >> 12 & 63); 임시[쓴수++] = (byte)(128 | koodipunkt >> 6 & 63); 임시[쓴수++] = (byte)(128 | koodipunkt & 63); }
        }
        byte[] TULEMUS = new byte[쓴수]; System.arraycopy(임시, 0, TULEMUS, 0, 쓴수); return TULEMUS;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String dekrüptima_andmed(byte[] bait_VALUE) {
        StringBuilder TULEMUS = new StringBuilder();
        for (int Loop_INDEX = 0; Loop_INDEX < bait_VALUE.length;) {
            int koodipunkt = bait_VALUE[Loop_INDEX++] & 255, number = koodipunkt < 128 ? 0 : koodipunkt >= 194 && koodipunkt < 224 ? 1 : koodipunkt >= 224 && koodipunkt < 240 ? 2 : koodipunkt >= 240 && koodipunkt <= 244 ? 3 : -1;
            if (number < 0 || bait_VALUE.length - Loop_INDEX < number) throw new kehtetu_argument_erand("잘못된 UTF-8");
            int 최소 = number == 1 ? 128 : number == 2 ? 2048 : number == 3 ? 65536 : 0;
            if (number > 0) koodipunkt &= (1 << (6 - number)) - 1;
            for (int sisemine_ametikoht = 0; sisemine_ametikoht < number; sisemine_ametikoht++) { int Tagasi_VALUE = bait_VALUE[Loop_INDEX++] & 255; if ((Tagasi_VALUE & 192) != 128) throw new kehtetu_argument_erand("잘못된 UTF-8"); koodipunkt = koodipunkt << 6 | Tagasi_VALUE & 63; }
            if (koodipunkt < 최소 || koodipunkt > 0x10ffff || koodipunkt >= 0xd800 && koodipunkt <= 0xdfff) throw new kehtetu_argument_erand("잘못된 UTF-8");
            if (koodipunkt < 65536) TULEMUS.append((char)koodipunkt);
            else { koodipunkt -= 65536; TULEMUS.append((char)(0xd800 | koodipunkt >> 10)); TULEMUS.append((char)(0xdc00 | koodipunkt & 1023)); }
        }
        return TULEMUS.toString();
    }
}
