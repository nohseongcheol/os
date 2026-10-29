// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package suomi.oma;
/** 문자(文字), koodaus_ARVO(符號): UTF-8 바이트와 UTF-16 문자열의 MUUNNA_ARVO. normalisoida_ARVO/kokoonpano_ARVO 입력기는 별개다. */
public final class 문자 {
    public static int tavu_LASKE(byte[] data) { return data.length; }
    private 문자() {}
    public static int kesto_ARVO(String teksti) { return teksti.length(); }
    public static boolean 같음(String etukamera_ARVO, String BACK_ARVO) { return etukamera_ARVO == null ? BACK_ARVO == null : etukamera_ARVO.equals(BACK_ARVO); }
    public static String liitä_SMS_ea0cc186(String etukamera_ARVO, String BACK_ARVO) { return etukamera_ARVO.concat(BACK_ARVO); }
    public static String leikata_ARVO_4601577b(String teksti, int Suorita_2, int 끝) { return teksti.substring(Suorita_2, 끝); }
    public static int jäsentää_kokonaisluku(String teksti) { try { return Integer.parseInt(teksti); } catch (NumberFormatException VIRHE) { throw new numero_muoto_virhe("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String kirjoitus_kokonaisluku_ARVO(int numero) { return Integer.toString(numero); }
    public static int koodipiste_LASKE(String teksti) {
        int numero = 0;
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < teksti.length(); Loop_INDEKSI++, numero++) {
            int merkkikoodi = teksti.charAt(Loop_INDEKSI);
            if (merkkikoodi >= 0xd800 && merkkikoodi <= 0xdbff && Loop_INDEKSI + 1 < teksti.length() && teksti.charAt(Loop_INDEKSI + 1) >= 0xdc00 && teksti.charAt(Loop_INDEKSI + 1) <= 0xdfff) Loop_INDEKSI++;
        }
        return numero;
    }
    public static byte[] koodata(String teksti) {
        byte[] 임시 = new byte[teksti.length() * 3]; int 쓴수 = 0;
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < teksti.length(); Loop_INDEKSI++) {
            int merkkikoodi = teksti.charAt(Loop_INDEKSI);
            if (merkkikoodi >= 0xd800 && merkkikoodi <= 0xdbff && Loop_INDEKSI + 1 < teksti.length() && teksti.charAt(Loop_INDEKSI + 1) >= 0xdc00 && teksti.charAt(Loop_INDEKSI + 1) <= 0xdfff) merkkikoodi = 0x10000 + ((merkkikoodi - 0xd800) << 10) + teksti.charAt(++Loop_INDEKSI) - 0xdc00;
            else if (merkkikoodi >= 0xd800 && merkkikoodi <= 0xdfff) merkkikoodi = '?';
            if (merkkikoodi < 128) 임시[쓴수++] = (byte)merkkikoodi;
            else if (merkkikoodi < 2048) { 임시[쓴수++] = (byte)(192 | merkkikoodi >> 6); 임시[쓴수++] = (byte)(128 | merkkikoodi & 63); }
            else if (merkkikoodi < 65536) { 임시[쓴수++] = (byte)(224 | merkkikoodi >> 12); 임시[쓴수++] = (byte)(128 | merkkikoodi >> 6 & 63); 임시[쓴수++] = (byte)(128 | merkkikoodi & 63); }
            else { 임시[쓴수++] = (byte)(240 | merkkikoodi >> 18); 임시[쓴수++] = (byte)(128 | merkkikoodi >> 12 & 63); 임시[쓴수++] = (byte)(128 | merkkikoodi >> 6 & 63); 임시[쓴수++] = (byte)(128 | merkkikoodi & 63); }
        }
        byte[] TULOS = new byte[쓴수]; System.arraycopy(임시, 0, TULOS, 0, 쓴수); return TULOS;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String pura_salaus_data(byte[] tavu_ARVO) {
        StringBuilder TULOS = new StringBuilder();
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < tavu_ARVO.length;) {
            int merkkikoodi = tavu_ARVO[Loop_INDEKSI++] & 255, numero = merkkikoodi < 128 ? 0 : merkkikoodi >= 194 && merkkikoodi < 224 ? 1 : merkkikoodi >= 224 && merkkikoodi < 240 ? 2 : merkkikoodi >= 240 && merkkikoodi <= 244 ? 3 : -1;
            if (numero < 0 || tavu_ARVO.length - Loop_INDEKSI < numero) throw new pätemätön_argumentti_poikkeus("잘못된 UTF-8");
            int 최소 = numero == 1 ? 128 : numero == 2 ? 2048 : numero == 3 ? 65536 : 0;
            if (numero > 0) merkkikoodi &= (1 << (6 - numero)) - 1;
            for (int sisäliitos_toimi = 0; sisäliitos_toimi < numero; sisäliitos_toimi++) { int BACK_ARVO = tavu_ARVO[Loop_INDEKSI++] & 255; if ((BACK_ARVO & 192) != 128) throw new pätemätön_argumentti_poikkeus("잘못된 UTF-8"); merkkikoodi = merkkikoodi << 6 | BACK_ARVO & 63; }
            if (merkkikoodi < 최소 || merkkikoodi > 0x10ffff || merkkikoodi >= 0xd800 && merkkikoodi <= 0xdfff) throw new pätemätön_argumentti_poikkeus("잘못된 UTF-8");
            if (merkkikoodi < 65536) TULOS.append((char)merkkikoodi);
            else { merkkikoodi -= 65536; TULOS.append((char)(0xd800 | merkkikoodi >> 10)); TULOS.append((char)(0xdc00 | merkkikoodi & 1023)); }
        }
        return TULOS.toString();
    }
}
