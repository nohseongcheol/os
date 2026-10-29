// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Isi_Zulu.자체;
/** 문자(文字), ukubhala_ngokufihla_inani(符號): UTF-8 바이트와 UTF-16 문자열의 변환. beka_kujwayeleke_inani/조합 입력기는 별개다. */
public final class 문자 {
    public static int 바이트수(byte[] imininingwane) { return imininingwane.length; }
    private 문자() {}
    public static int ubude_inani(String Itekisi) { return Itekisi.length(); }
    public static boolean 같음(String 앞, String Impindamuva_inani) { return 앞 == null ? Impindamuva_inani == null : 앞.equals(Impindamuva_inani); }
    public static String namathisela_I_SMS(String 앞, String Impindamuva_inani) { return 앞.concat(Impindamuva_inani); }
    public static String sika_inani(String Itekisi, int Sebenzisa, int 끝) { return Itekisi.substring(Sebenzisa, 끝); }
    public static int zawula_inamba(String Itekisi) { try { return Integer.parseInt(Itekisi); } catch (NumberFormatException Iphutha) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String bhala_inamba_inani(int 수) { return Integer.toString(수); }
    public static int 코드포인트수(String Itekisi) {
        int 수 = 0;
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < Itekisi.length(); iluphu_thola_inkomba++, 수++) {
            int ikhodi_yohlamvu = Itekisi.charAt(iluphu_thola_inkomba);
            if (ikhodi_yohlamvu >= 0xd800 && ikhodi_yohlamvu <= 0xdbff && iluphu_thola_inkomba + 1 < Itekisi.length() && Itekisi.charAt(iluphu_thola_inkomba + 1) >= 0xdc00 && Itekisi.charAt(iluphu_thola_inkomba + 1) <= 0xdfff) iluphu_thola_inkomba++;
        }
        return 수;
    }
    public static byte[] 부호화(String Itekisi) {
        byte[] 임시 = new byte[Itekisi.length() * 3]; int 쓴수 = 0;
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < Itekisi.length(); iluphu_thola_inkomba++) {
            int ikhodi_yohlamvu = Itekisi.charAt(iluphu_thola_inkomba);
            if (ikhodi_yohlamvu >= 0xd800 && ikhodi_yohlamvu <= 0xdbff && iluphu_thola_inkomba + 1 < Itekisi.length() && Itekisi.charAt(iluphu_thola_inkomba + 1) >= 0xdc00 && Itekisi.charAt(iluphu_thola_inkomba + 1) <= 0xdfff) ikhodi_yohlamvu = 0x10000 + ((ikhodi_yohlamvu - 0xd800) << 10) + Itekisi.charAt(++iluphu_thola_inkomba) - 0xdc00;
            else if (ikhodi_yohlamvu >= 0xd800 && ikhodi_yohlamvu <= 0xdfff) ikhodi_yohlamvu = '?';
            if (ikhodi_yohlamvu < 128) 임시[쓴수++] = (byte)ikhodi_yohlamvu;
            else if (ikhodi_yohlamvu < 2048) { 임시[쓴수++] = (byte)(192 | ikhodi_yohlamvu >> 6); 임시[쓴수++] = (byte)(128 | ikhodi_yohlamvu & 63); }
            else if (ikhodi_yohlamvu < 65536) { 임시[쓴수++] = (byte)(224 | ikhodi_yohlamvu >> 12); 임시[쓴수++] = (byte)(128 | ikhodi_yohlamvu >> 6 & 63); 임시[쓴수++] = (byte)(128 | ikhodi_yohlamvu & 63); }
            else { 임시[쓴수++] = (byte)(240 | ikhodi_yohlamvu >> 18); 임시[쓴수++] = (byte)(128 | ikhodi_yohlamvu >> 12 & 63); 임시[쓴수++] = (byte)(128 | ikhodi_yohlamvu >> 6 & 63); 임시[쓴수++] = (byte)(128 | ikhodi_yohlamvu & 63); }
        }
        byte[] 결과 = new byte[쓴수]; System.arraycopy(임시, 0, 결과, 0, 쓴수); return 결과;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String guqulela_imininingwane(byte[] ibhayithi_inani) {
        StringBuilder 결과 = new StringBuilder();
        for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < ibhayithi_inani.length;) {
            int ikhodi_yohlamvu = ibhayithi_inani[iluphu_thola_inkomba++] & 255, 수 = ikhodi_yohlamvu < 128 ? 0 : ikhodi_yohlamvu >= 194 && ikhodi_yohlamvu < 224 ? 1 : ikhodi_yohlamvu >= 224 && ikhodi_yohlamvu < 240 ? 2 : ikhodi_yohlamvu >= 240 && ikhodi_yohlamvu <= 244 ? 3 : -1;
            if (수 < 0 || ibhayithi_inani.length - iluphu_thola_inkomba < 수) throw new 잘못된인수예외("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) ikhodi_yohlamvu &= (1 << (6 - 수)) - 1;
            for (int 안쪽자리 = 0; 안쪽자리 < 수; 안쪽자리++) { int Impindamuva_inani = ibhayithi_inani[iluphu_thola_inkomba++] & 255; if ((Impindamuva_inani & 192) != 128) throw new 잘못된인수예외("잘못된 UTF-8"); ikhodi_yohlamvu = ikhodi_yohlamvu << 6 | Impindamuva_inani & 63; }
            if (ikhodi_yohlamvu < 최소 || ikhodi_yohlamvu > 0x10ffff || ikhodi_yohlamvu >= 0xd800 && ikhodi_yohlamvu <= 0xdfff) throw new 잘못된인수예외("잘못된 UTF-8");
            if (ikhodi_yohlamvu < 65536) 결과.append((char)ikhodi_yohlamvu);
            else { ikhodi_yohlamvu -= 65536; 결과.append((char)(0xd800 | ikhodi_yohlamvu >> 10)); 결과.append((char)(0xdc00 | ikhodi_yohlamvu & 1023)); }
        }
        return 결과.toString();
    }
}
