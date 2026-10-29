// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lietuvių.savas;
/** 문자(文字), kodavimas_VALUE(符號): UTF-8 바이트와 UTF-16 문자열의 CONVERT_VALUE. normalizuoti_VALUE/struktūra_VALUE 입력기는 별개다. */
public final class 문자 {
    public static int baitas_COUNT(byte[] duomenys) { return duomenys.length; }
    private 문자() {}
    public static int 길이(String Tekstas) { return Tekstas.length(); }
    public static boolean 같음(String priekinis_VALUE, String ATGAL_VALUE) { return priekinis_VALUE == null ? ATGAL_VALUE == null : priekinis_VALUE.equals(ATGAL_VALUE); }
    public static String Įklijuoti_SMS(String priekinis_VALUE, String ATGAL_VALUE) { return priekinis_VALUE.concat(ATGAL_VALUE); }
    public static String kirpti_VALUE(String Tekstas, int Paleisti, int 끝) { return Tekstas.substring(Paleisti, 끝); }
    public static int analizuoti_sintaksę_sveikasis_skaičius(String Tekstas) { try { return Integer.parseInt(Tekstas); } catch (NumberFormatException KLAIDA) { throw new numeris_formatas_triktis("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String rašymas_sveikasis_skaičius_VALUE(int numeris) { return Integer.toString(numeris); }
    public static int kodo_elementas_COUNT(String Tekstas) {
        int numeris = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Tekstas.length(); Loop_INDEX++, numeris++) {
            int simbolio_kodas = Tekstas.charAt(Loop_INDEX);
            if (simbolio_kodas >= 0xd800 && simbolio_kodas <= 0xdbff && Loop_INDEX + 1 < Tekstas.length() && Tekstas.charAt(Loop_INDEX + 1) >= 0xdc00 && Tekstas.charAt(Loop_INDEX + 1) <= 0xdfff) Loop_INDEX++;
        }
        return numeris;
    }
    public static byte[] koduoti(String Tekstas) {
        byte[] 임시 = new byte[Tekstas.length() * 3]; int 쓴수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Tekstas.length(); Loop_INDEX++) {
            int simbolio_kodas = Tekstas.charAt(Loop_INDEX);
            if (simbolio_kodas >= 0xd800 && simbolio_kodas <= 0xdbff && Loop_INDEX + 1 < Tekstas.length() && Tekstas.charAt(Loop_INDEX + 1) >= 0xdc00 && Tekstas.charAt(Loop_INDEX + 1) <= 0xdfff) simbolio_kodas = 0x10000 + ((simbolio_kodas - 0xd800) << 10) + Tekstas.charAt(++Loop_INDEX) - 0xdc00;
            else if (simbolio_kodas >= 0xd800 && simbolio_kodas <= 0xdfff) simbolio_kodas = '?';
            if (simbolio_kodas < 128) 임시[쓴수++] = (byte)simbolio_kodas;
            else if (simbolio_kodas < 2048) { 임시[쓴수++] = (byte)(192 | simbolio_kodas >> 6); 임시[쓴수++] = (byte)(128 | simbolio_kodas & 63); }
            else if (simbolio_kodas < 65536) { 임시[쓴수++] = (byte)(224 | simbolio_kodas >> 12); 임시[쓴수++] = (byte)(128 | simbolio_kodas >> 6 & 63); 임시[쓴수++] = (byte)(128 | simbolio_kodas & 63); }
            else { 임시[쓴수++] = (byte)(240 | simbolio_kodas >> 18); 임시[쓴수++] = (byte)(128 | simbolio_kodas >> 12 & 63); 임시[쓴수++] = (byte)(128 | simbolio_kodas >> 6 & 63); 임시[쓴수++] = (byte)(128 | simbolio_kodas & 63); }
        }
        byte[] REZULTATAS = new byte[쓴수]; System.arraycopy(임시, 0, REZULTATAS, 0, 쓴수); return REZULTATAS;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String iššifruoti_duomenys(byte[] baitas_VALUE) {
        StringBuilder REZULTATAS = new StringBuilder();
        for (int Loop_INDEX = 0; Loop_INDEX < baitas_VALUE.length;) {
            int simbolio_kodas = baitas_VALUE[Loop_INDEX++] & 255, numeris = simbolio_kodas < 128 ? 0 : simbolio_kodas >= 194 && simbolio_kodas < 224 ? 1 : simbolio_kodas >= 224 && simbolio_kodas < 240 ? 2 : simbolio_kodas >= 240 && simbolio_kodas <= 244 ? 3 : -1;
            if (numeris < 0 || baitas_VALUE.length - Loop_INDEX < numeris) throw new neleistinas_argumentas_išimtis("잘못된 UTF-8");
            int 최소 = numeris == 1 ? 128 : numeris == 2 ? 2048 : numeris == 3 ? 65536 : 0;
            if (numeris > 0) simbolio_kodas &= (1 << (6 - numeris)) - 1;
            for (int vidinis_padėtis = 0; vidinis_padėtis < numeris; vidinis_padėtis++) { int ATGAL_VALUE = baitas_VALUE[Loop_INDEX++] & 255; if ((ATGAL_VALUE & 192) != 128) throw new neleistinas_argumentas_išimtis("잘못된 UTF-8"); simbolio_kodas = simbolio_kodas << 6 | ATGAL_VALUE & 63; }
            if (simbolio_kodas < 최소 || simbolio_kodas > 0x10ffff || simbolio_kodas >= 0xd800 && simbolio_kodas <= 0xdfff) throw new neleistinas_argumentas_išimtis("잘못된 UTF-8");
            if (simbolio_kodas < 65536) REZULTATAS.append((char)simbolio_kodas);
            else { simbolio_kodas -= 65536; REZULTATAS.append((char)(0xd800 | simbolio_kodas >> 10)); REZULTATAS.append((char)(0xdc00 | simbolio_kodas & 1023)); }
        }
        return REZULTATAS.toString();
    }
}
