// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 문자(文字), Juyar_da_bayanai_zuwa_lamba_Daraja(符號): UTF-8 바이트와 UTF-16 문자열의 변환. Gajarta_kimar_bayanai_Daraja/조합 입력기는 별개다. */
public final class 문자 {
    public static int 바이트수(byte[] Tarin_bayani) { return Tarin_bayani.length; }
    private 문자() {}
    public static int Tsawo_Daraja(String SMS) { return SMS.length(); }
    public static boolean 같음(String kyamarar_gaba_Daraja, String Baya_Daraja) { return kyamarar_gaba_Daraja == null ? Baya_Daraja == null : kyamarar_gaba_Daraja.equals(Baya_Daraja); }
    public static String manna_SMS(String kyamarar_gaba_Daraja, String Baya_Daraja) { return kyamarar_gaba_Daraja.concat(Baya_Daraja); }
    public static String Yanka_Daraja(String SMS, int Tafiyar_da, int 끝) { return SMS.substring(Tafiyar_da, 끝); }
    public static int Daddatse_Lamba_mara(String SMS) { try { return Integer.parseInt(SMS); } catch (NumberFormatException Kuskure) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String Rubuta_Lamba_mara_Daraja(int 수) { return Integer.toString(수); }
    public static int 코드포인트수(String SMS) {
        int 수 = 0;
        for (int Warware_Indes = 0; Warware_Indes < SMS.length(); Warware_Indes++, 수++) {
            int Lambar_sirrin_harafi = SMS.charAt(Warware_Indes);
            if (Lambar_sirrin_harafi >= 0xd800 && Lambar_sirrin_harafi <= 0xdbff && Warware_Indes + 1 < SMS.length() && SMS.charAt(Warware_Indes + 1) >= 0xdc00 && SMS.charAt(Warware_Indes + 1) <= 0xdfff) Warware_Indes++;
        }
        return 수;
    }
    public static byte[] 부호화(String SMS) {
        byte[] 임시 = new byte[SMS.length() * 3]; int 쓴수 = 0;
        for (int Warware_Indes = 0; Warware_Indes < SMS.length(); Warware_Indes++) {
            int Lambar_sirrin_harafi = SMS.charAt(Warware_Indes);
            if (Lambar_sirrin_harafi >= 0xd800 && Lambar_sirrin_harafi <= 0xdbff && Warware_Indes + 1 < SMS.length() && SMS.charAt(Warware_Indes + 1) >= 0xdc00 && SMS.charAt(Warware_Indes + 1) <= 0xdfff) Lambar_sirrin_harafi = 0x10000 + ((Lambar_sirrin_harafi - 0xd800) << 10) + SMS.charAt(++Warware_Indes) - 0xdc00;
            else if (Lambar_sirrin_harafi >= 0xd800 && Lambar_sirrin_harafi <= 0xdfff) Lambar_sirrin_harafi = '?';
            if (Lambar_sirrin_harafi < 128) 임시[쓴수++] = (byte)Lambar_sirrin_harafi;
            else if (Lambar_sirrin_harafi < 2048) { 임시[쓴수++] = (byte)(192 | Lambar_sirrin_harafi >> 6); 임시[쓴수++] = (byte)(128 | Lambar_sirrin_harafi & 63); }
            else if (Lambar_sirrin_harafi < 65536) { 임시[쓴수++] = (byte)(224 | Lambar_sirrin_harafi >> 12); 임시[쓴수++] = (byte)(128 | Lambar_sirrin_harafi >> 6 & 63); 임시[쓴수++] = (byte)(128 | Lambar_sirrin_harafi & 63); }
            else { 임시[쓴수++] = (byte)(240 | Lambar_sirrin_harafi >> 18); 임시[쓴수++] = (byte)(128 | Lambar_sirrin_harafi >> 12 & 63); 임시[쓴수++] = (byte)(128 | Lambar_sirrin_harafi >> 6 & 63); 임시[쓴수++] = (byte)(128 | Lambar_sirrin_harafi & 63); }
        }
        byte[] 결과 = new byte[쓴수]; System.arraycopy(임시, 0, 결과, 0, 쓴수); return 결과;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String Bude_Tarin_bayani(byte[] bayit_Daraja) {
        StringBuilder 결과 = new StringBuilder();
        for (int Warware_Indes = 0; Warware_Indes < bayit_Daraja.length;) {
            int Lambar_sirrin_harafi = bayit_Daraja[Warware_Indes++] & 255, 수 = Lambar_sirrin_harafi < 128 ? 0 : Lambar_sirrin_harafi >= 194 && Lambar_sirrin_harafi < 224 ? 1 : Lambar_sirrin_harafi >= 224 && Lambar_sirrin_harafi < 240 ? 2 : Lambar_sirrin_harafi >= 240 && Lambar_sirrin_harafi <= 244 ? 3 : -1;
            if (수 < 0 || bayit_Daraja.length - Warware_Indes < 수) throw new mara_ƙarfi_Tubalin_aiki_banbanchi("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) Lambar_sirrin_harafi &= (1 << (6 - 수)) - 1;
            for (int 안쪽자리 = 0; 안쪽자리 < 수; 안쪽자리++) { int Baya_Daraja = bayit_Daraja[Warware_Indes++] & 255; if ((Baya_Daraja & 192) != 128) throw new mara_ƙarfi_Tubalin_aiki_banbanchi("잘못된 UTF-8"); Lambar_sirrin_harafi = Lambar_sirrin_harafi << 6 | Baya_Daraja & 63; }
            if (Lambar_sirrin_harafi < 최소 || Lambar_sirrin_harafi > 0x10ffff || Lambar_sirrin_harafi >= 0xd800 && Lambar_sirrin_harafi <= 0xdfff) throw new mara_ƙarfi_Tubalin_aiki_banbanchi("잘못된 UTF-8");
            if (Lambar_sirrin_harafi < 65536) 결과.append((char)Lambar_sirrin_harafi);
            else { Lambar_sirrin_harafi -= 65536; 결과.append((char)(0xd800 | Lambar_sirrin_harafi >> 10)); 결과.append((char)(0xdc00 | Lambar_sirrin_harafi & 1023)); }
        }
        return 결과.toString();
    }
}
