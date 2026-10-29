// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 문자(文字), ntinye_koòdù_valuu(符號): UTF-8 바이트와 UTF-16 문자열의 변환. mèzima_valuu/조합 입력기는 별개다. */
public final class 문자 {
    public static int 바이트수(byte[] datà) { return datà.length; }
    private 문자() {}
    public static int ogologo_valuu(String SMS) { return SMS.length(); }
    public static boolean 같음(String 앞, String Àzụ_valuu) { return 앞 == null ? Àzụ_valuu == null : 앞.equals(Àzụ_valuu); }
    public static String nyàpanye_SMS(String 앞, String Àzụ_valuu) { return 앞.concat(Àzụ_valuu); }
    public static String gbubìte_valuu(String SMS, int Bido, int 끝) { return SMS.substring(Bido, 끝); }
    public static int kerìsịa_ọnụọgụ_nzùrùòkè(String SMS) { try { return Integer.parseInt(SMS); } catch (NumberFormatException mmejọ) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String dee_ọnụọgụ_nzùrùòkè_valuu(int 수) { return Integer.toString(수); }
    public static int 코드포인트수(String SMS) {
        int 수 = 0;
        for (int memmenwè_indèks = 0; memmenwè_indèks < SMS.length(); memmenwè_indèks++, 수++) {
            int koòdù_nkeakàrà = SMS.charAt(memmenwè_indèks);
            if (koòdù_nkeakàrà >= 0xd800 && koòdù_nkeakàrà <= 0xdbff && memmenwè_indèks + 1 < SMS.length() && SMS.charAt(memmenwè_indèks + 1) >= 0xdc00 && SMS.charAt(memmenwè_indèks + 1) <= 0xdfff) memmenwè_indèks++;
        }
        return 수;
    }
    public static byte[] 부호화(String SMS) {
        byte[] 임시 = new byte[SMS.length() * 3]; int 쓴수 = 0;
        for (int memmenwè_indèks = 0; memmenwè_indèks < SMS.length(); memmenwè_indèks++) {
            int koòdù_nkeakàrà = SMS.charAt(memmenwè_indèks);
            if (koòdù_nkeakàrà >= 0xd800 && koòdù_nkeakàrà <= 0xdbff && memmenwè_indèks + 1 < SMS.length() && SMS.charAt(memmenwè_indèks + 1) >= 0xdc00 && SMS.charAt(memmenwè_indèks + 1) <= 0xdfff) koòdù_nkeakàrà = 0x10000 + ((koòdù_nkeakàrà - 0xd800) << 10) + SMS.charAt(++memmenwè_indèks) - 0xdc00;
            else if (koòdù_nkeakàrà >= 0xd800 && koòdù_nkeakàrà <= 0xdfff) koòdù_nkeakàrà = '?';
            if (koòdù_nkeakàrà < 128) 임시[쓴수++] = (byte)koòdù_nkeakàrà;
            else if (koòdù_nkeakàrà < 2048) { 임시[쓴수++] = (byte)(192 | koòdù_nkeakàrà >> 6); 임시[쓴수++] = (byte)(128 | koòdù_nkeakàrà & 63); }
            else if (koòdù_nkeakàrà < 65536) { 임시[쓴수++] = (byte)(224 | koòdù_nkeakàrà >> 12); 임시[쓴수++] = (byte)(128 | koòdù_nkeakàrà >> 6 & 63); 임시[쓴수++] = (byte)(128 | koòdù_nkeakàrà & 63); }
            else { 임시[쓴수++] = (byte)(240 | koòdù_nkeakàrà >> 18); 임시[쓴수++] = (byte)(128 | koòdù_nkeakàrà >> 12 & 63); 임시[쓴수++] = (byte)(128 | koòdù_nkeakàrà >> 6 & 63); 임시[쓴수++] = (byte)(128 | koòdù_nkeakàrà & 63); }
        }
        byte[] 결과 = new byte[쓴수]; System.arraycopy(임시, 0, 결과, 0, 쓴수); return 결과;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String tụghee_edenzizo_datà(byte[] baịtị_valuu) {
        StringBuilder 결과 = new StringBuilder();
        for (int memmenwè_indèks = 0; memmenwè_indèks < baịtị_valuu.length;) {
            int koòdù_nkeakàrà = baịtị_valuu[memmenwè_indèks++] & 255, 수 = koòdù_nkeakàrà < 128 ? 0 : koòdù_nkeakàrà >= 194 && koòdù_nkeakàrà < 224 ? 1 : koòdù_nkeakàrà >= 224 && koòdù_nkeakàrà < 240 ? 2 : koòdù_nkeakàrà >= 240 && koòdù_nkeakàrà <= 244 ? 3 : -1;
            if (수 < 0 || baịtị_valuu.length - memmenwè_indèks < 수) throw new 잘못된인수예외("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) koòdù_nkeakàrà &= (1 << (6 - 수)) - 1;
            for (int 안쪽자리 = 0; 안쪽자리 < 수; 안쪽자리++) { int Àzụ_valuu = baịtị_valuu[memmenwè_indèks++] & 255; if ((Àzụ_valuu & 192) != 128) throw new 잘못된인수예외("잘못된 UTF-8"); koòdù_nkeakàrà = koòdù_nkeakàrà << 6 | Àzụ_valuu & 63; }
            if (koòdù_nkeakàrà < 최소 || koòdù_nkeakàrà > 0x10ffff || koòdù_nkeakàrà >= 0xd800 && koòdù_nkeakàrà <= 0xdfff) throw new 잘못된인수예외("잘못된 UTF-8");
            if (koòdù_nkeakàrà < 65536) 결과.append((char)koòdù_nkeakàrà);
            else { koòdù_nkeakàrà -= 65536; 결과.append((char)(0xd800 | koòdù_nkeakàrà >> 10)); 결과.append((char)(0xdc00 | koòdù_nkeakàrà & 1023)); }
        }
        return 결과.toString();
    }
}
