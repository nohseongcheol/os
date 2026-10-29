// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package magyar.saját;
/** 문자(文字), kódolás_ÉRTÉK(符號): UTF-8 바이트와 UTF-16 문자열의 konvertál_ÉRTÉK. normalizál_ÉRTÉK/rész_egész_ÉRTÉK 입력기는 별개다. */
public final class 문자 {
    public static int bájt_DARAB(byte[] adat) { return adat.length; }
    private 문자() {}
    public static int hossz_ÉRTÉK(String Szöveg) { return Szöveg.length(); }
    public static boolean 같음(String elülső_kamera_ÉRTÉK, String BACK_ÉRTÉK) { return elülső_kamera_ÉRTÉK == null ? BACK_ÉRTÉK == null : elülső_kamera_ÉRTÉK.equals(BACK_ÉRTÉK); }
    public static String beilleszt_SMS(String elülső_kamera_ÉRTÉK, String BACK_ÉRTÉK) { return elülső_kamera_ÉRTÉK.concat(BACK_ÉRTÉK); }
    public static String vágás_ÉRTÉK(String Szöveg, int Futtatás, int 끝) { return Szöveg.substring(Futtatás, 끝); }
    public static int elemez_egész_szám(String Szöveg) { try { return Integer.parseInt(Szöveg); } catch (NumberFormatException HIBA) { throw new szám_formáz_hiba("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String ír_egész_szám_ÉRTÉK(int szám) { return Integer.toString(szám); }
    public static int kódpont_DARAB(String Szöveg) {
        int szám = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Szöveg.length(); Loop_INDEX++, szám++) {
            int kódpont = Szöveg.charAt(Loop_INDEX);
            if (kódpont >= 0xd800 && kódpont <= 0xdbff && Loop_INDEX + 1 < Szöveg.length() && Szöveg.charAt(Loop_INDEX + 1) >= 0xdc00 && Szöveg.charAt(Loop_INDEX + 1) <= 0xdfff) Loop_INDEX++;
        }
        return szám;
    }
    public static byte[] kódolás(String Szöveg) {
        byte[] 임시 = new byte[Szöveg.length() * 3]; int 쓴수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Szöveg.length(); Loop_INDEX++) {
            int kódpont = Szöveg.charAt(Loop_INDEX);
            if (kódpont >= 0xd800 && kódpont <= 0xdbff && Loop_INDEX + 1 < Szöveg.length() && Szöveg.charAt(Loop_INDEX + 1) >= 0xdc00 && Szöveg.charAt(Loop_INDEX + 1) <= 0xdfff) kódpont = 0x10000 + ((kódpont - 0xd800) << 10) + Szöveg.charAt(++Loop_INDEX) - 0xdc00;
            else if (kódpont >= 0xd800 && kódpont <= 0xdfff) kódpont = '?';
            if (kódpont < 128) 임시[쓴수++] = (byte)kódpont;
            else if (kódpont < 2048) { 임시[쓴수++] = (byte)(192 | kódpont >> 6); 임시[쓴수++] = (byte)(128 | kódpont & 63); }
            else if (kódpont < 65536) { 임시[쓴수++] = (byte)(224 | kódpont >> 12); 임시[쓴수++] = (byte)(128 | kódpont >> 6 & 63); 임시[쓴수++] = (byte)(128 | kódpont & 63); }
            else { 임시[쓴수++] = (byte)(240 | kódpont >> 18); 임시[쓴수++] = (byte)(128 | kódpont >> 12 & 63); 임시[쓴수++] = (byte)(128 | kódpont >> 6 & 63); 임시[쓴수++] = (byte)(128 | kódpont & 63); }
        }
        byte[] KR = new byte[쓴수]; System.arraycopy(임시, 0, KR, 0, 쓴수); return KR;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String visszafejt_adat(byte[] bájt_ÉRTÉK) {
        StringBuilder KR = new StringBuilder();
        for (int Loop_INDEX = 0; Loop_INDEX < bájt_ÉRTÉK.length;) {
            int kódpont = bájt_ÉRTÉK[Loop_INDEX++] & 255, szám = kódpont < 128 ? 0 : kódpont >= 194 && kódpont < 224 ? 1 : kódpont >= 224 && kódpont < 240 ? 2 : kódpont >= 240 && kódpont <= 244 ? 3 : -1;
            if (szám < 0 || bájt_ÉRTÉK.length - Loop_INDEX < szám) throw new alaptalan_argumentum_kivétel("잘못된 UTF-8");
            int 최소 = szám == 1 ? 128 : szám == 2 ? 2048 : szám == 3 ? 65536 : 0;
            if (szám > 0) kódpont &= (1 << (6 - szám)) - 1;
            for (int belső_pozíció = 0; belső_pozíció < szám; belső_pozíció++) { int BACK_ÉRTÉK = bájt_ÉRTÉK[Loop_INDEX++] & 255; if ((BACK_ÉRTÉK & 192) != 128) throw new alaptalan_argumentum_kivétel("잘못된 UTF-8"); kódpont = kódpont << 6 | BACK_ÉRTÉK & 63; }
            if (kódpont < 최소 || kódpont > 0x10ffff || kódpont >= 0xd800 && kódpont <= 0xdfff) throw new alaptalan_argumentum_kivétel("잘못된 UTF-8");
            if (kódpont < 65536) KR.append((char)kódpont);
            else { kódpont -= 65536; KR.append((char)(0xd800 | kódpont >> 10)); KR.append((char)(0xdc00 | kódpont & 1023)); }
        }
        return KR.toString();
    }
}
