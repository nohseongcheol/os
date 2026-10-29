// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package isiXhosa.자체;
/** 문자(文字), ujiko_nkcukacha_zibe_ziikhowudi_ixabiso(符號): UTF-8 바이트와 UTF-16 문자열의 변환. qhelekisa_ixabiso/조합 입력기는 별개다. */
public final class 문자 {
    public static int 바이트수(byte[] iingcombolo) { return iingcombolo.length; }
    private 문자() {}
    public static int ubude_ixabiso(String Umbhalo) { return Umbhalo.length(); }
    public static boolean 같음(String 앞, String Emva_ixabiso) { return 앞 == null ? Emva_ixabiso == null : 앞.equals(Emva_ixabiso); }
    public static String beka_I_SMS(String 앞, String Emva_ixabiso) { return 앞.concat(Emva_ixabiso); }
    public static String sika_ixabiso(String Umbhalo, int Phumeza, int 끝) { return Umbhalo.substring(Phumeza, 끝); }
    public static int ingcaciso_yegama_inani_elipheleleyo(String Umbhalo) { try { return Integer.parseInt(Umbhalo); } catch (NumberFormatException Impazamo) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String bhala_inani_elipheleleyo_ixabiso(int 수) { return Integer.toString(수); }
    public static int 코드포인트수(String Umbhalo) {
        int 수 = 0;
        for (int iluphu_indeksa = 0; iluphu_indeksa < Umbhalo.length(); iluphu_indeksa++, 수++) {
            int ikhowudi_yekharakhtha = Umbhalo.charAt(iluphu_indeksa);
            if (ikhowudi_yekharakhtha >= 0xd800 && ikhowudi_yekharakhtha <= 0xdbff && iluphu_indeksa + 1 < Umbhalo.length() && Umbhalo.charAt(iluphu_indeksa + 1) >= 0xdc00 && Umbhalo.charAt(iluphu_indeksa + 1) <= 0xdfff) iluphu_indeksa++;
        }
        return 수;
    }
    public static byte[] 부호화(String Umbhalo) {
        byte[] 임시 = new byte[Umbhalo.length() * 3]; int 쓴수 = 0;
        for (int iluphu_indeksa = 0; iluphu_indeksa < Umbhalo.length(); iluphu_indeksa++) {
            int ikhowudi_yekharakhtha = Umbhalo.charAt(iluphu_indeksa);
            if (ikhowudi_yekharakhtha >= 0xd800 && ikhowudi_yekharakhtha <= 0xdbff && iluphu_indeksa + 1 < Umbhalo.length() && Umbhalo.charAt(iluphu_indeksa + 1) >= 0xdc00 && Umbhalo.charAt(iluphu_indeksa + 1) <= 0xdfff) ikhowudi_yekharakhtha = 0x10000 + ((ikhowudi_yekharakhtha - 0xd800) << 10) + Umbhalo.charAt(++iluphu_indeksa) - 0xdc00;
            else if (ikhowudi_yekharakhtha >= 0xd800 && ikhowudi_yekharakhtha <= 0xdfff) ikhowudi_yekharakhtha = '?';
            if (ikhowudi_yekharakhtha < 128) 임시[쓴수++] = (byte)ikhowudi_yekharakhtha;
            else if (ikhowudi_yekharakhtha < 2048) { 임시[쓴수++] = (byte)(192 | ikhowudi_yekharakhtha >> 6); 임시[쓴수++] = (byte)(128 | ikhowudi_yekharakhtha & 63); }
            else if (ikhowudi_yekharakhtha < 65536) { 임시[쓴수++] = (byte)(224 | ikhowudi_yekharakhtha >> 12); 임시[쓴수++] = (byte)(128 | ikhowudi_yekharakhtha >> 6 & 63); 임시[쓴수++] = (byte)(128 | ikhowudi_yekharakhtha & 63); }
            else { 임시[쓴수++] = (byte)(240 | ikhowudi_yekharakhtha >> 18); 임시[쓴수++] = (byte)(128 | ikhowudi_yekharakhtha >> 12 & 63); 임시[쓴수++] = (byte)(128 | ikhowudi_yekharakhtha >> 6 & 63); 임시[쓴수++] = (byte)(128 | ikhowudi_yekharakhtha & 63); }
        }
        byte[] 결과 = new byte[쓴수]; System.arraycopy(임시, 0, 결과, 0, 쓴수); return 결과;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String buyisela_ubhalo_oluqhelekileyo_iingcombolo(byte[] ibhayithi_ixabiso) {
        StringBuilder 결과 = new StringBuilder();
        for (int iluphu_indeksa = 0; iluphu_indeksa < ibhayithi_ixabiso.length;) {
            int ikhowudi_yekharakhtha = ibhayithi_ixabiso[iluphu_indeksa++] & 255, 수 = ikhowudi_yekharakhtha < 128 ? 0 : ikhowudi_yekharakhtha >= 194 && ikhowudi_yekharakhtha < 224 ? 1 : ikhowudi_yekharakhtha >= 224 && ikhowudi_yekharakhtha < 240 ? 2 : ikhowudi_yekharakhtha >= 240 && ikhowudi_yekharakhtha <= 244 ? 3 : -1;
            if (수 < 0 || ibhayithi_ixabiso.length - iluphu_indeksa < 수) throw new 잘못된인수예외("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) ikhowudi_yekharakhtha &= (1 << (6 - 수)) - 1;
            for (int 안쪽자리 = 0; 안쪽자리 < 수; 안쪽자리++) { int Emva_ixabiso = ibhayithi_ixabiso[iluphu_indeksa++] & 255; if ((Emva_ixabiso & 192) != 128) throw new 잘못된인수예외("잘못된 UTF-8"); ikhowudi_yekharakhtha = ikhowudi_yekharakhtha << 6 | Emva_ixabiso & 63; }
            if (ikhowudi_yekharakhtha < 최소 || ikhowudi_yekharakhtha > 0x10ffff || ikhowudi_yekharakhtha >= 0xd800 && ikhowudi_yekharakhtha <= 0xdfff) throw new 잘못된인수예외("잘못된 UTF-8");
            if (ikhowudi_yekharakhtha < 65536) 결과.append((char)ikhowudi_yekharakhtha);
            else { ikhowudi_yekharakhtha -= 65536; 결과.append((char)(0xd800 | ikhowudi_yekharakhtha >> 10)); 결과.append((char)(0xdc00 | ikhowudi_yekharakhtha & 1023)); }
        }
        return 결과.toString();
    }
}
