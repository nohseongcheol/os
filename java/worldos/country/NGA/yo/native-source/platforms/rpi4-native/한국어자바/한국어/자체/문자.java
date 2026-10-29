// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 문자(文字), pípàrokò_iye(符號): UTF-8 바이트와 UTF-16 문자열의 변환. ṣe_níwọ̀n_iye/조합 입력기는 별개다. */
public final class 문자 {
    public static int 바이트수(byte[] détà) { return détà.length; }
    private 문자() {}
    public static int gígùn_iye(String SMS) { return SMS.length(); }
    public static boolean 같음(String 앞, String Padà_sẹ́yìn_iye) { return 앞 == null ? Padà_sẹ́yìn_iye == null : 앞.equals(Padà_sẹ́yìn_iye); }
    public static String lẹ_SMS(String 앞, String Padà_sẹ́yìn_iye) { return 앞.concat(Padà_sẹ́yìn_iye); }
    public static String gé_kúrò_iye(String SMS, int Rọ́ọ̀nù, int 끝) { return SMS.substring(Rọ́ọ̀nù, 끝); }
    public static int ìpínsíwẹ́wẹ́_nọ́ńbà_odindi(String SMS) { try { return Integer.parseInt(SMS); } catch (NumberFormatException àṣìṣe) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String kọ_nọ́ńbà_odindi_iye(int 수) { return Integer.toString(수); }
    public static int 코드포인트수(String SMS) {
        int 수 = 0;
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < SMS.length(); ṣetúnṣe_wá_atọ̀ka_àkóónú++, 수++) {
            int kóòdù_ẹyọ_ọ̀rọ̀ = SMS.charAt(ṣetúnṣe_wá_atọ̀ka_àkóónú);
            if (kóòdù_ẹyọ_ọ̀rọ̀ >= 0xd800 && kóòdù_ẹyọ_ọ̀rọ̀ <= 0xdbff && ṣetúnṣe_wá_atọ̀ka_àkóónú + 1 < SMS.length() && SMS.charAt(ṣetúnṣe_wá_atọ̀ka_àkóónú + 1) >= 0xdc00 && SMS.charAt(ṣetúnṣe_wá_atọ̀ka_àkóónú + 1) <= 0xdfff) ṣetúnṣe_wá_atọ̀ka_àkóónú++;
        }
        return 수;
    }
    public static byte[] 부호화(String SMS) {
        byte[] 임시 = new byte[SMS.length() * 3]; int 쓴수 = 0;
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < SMS.length(); ṣetúnṣe_wá_atọ̀ka_àkóónú++) {
            int kóòdù_ẹyọ_ọ̀rọ̀ = SMS.charAt(ṣetúnṣe_wá_atọ̀ka_àkóónú);
            if (kóòdù_ẹyọ_ọ̀rọ̀ >= 0xd800 && kóòdù_ẹyọ_ọ̀rọ̀ <= 0xdbff && ṣetúnṣe_wá_atọ̀ka_àkóónú + 1 < SMS.length() && SMS.charAt(ṣetúnṣe_wá_atọ̀ka_àkóónú + 1) >= 0xdc00 && SMS.charAt(ṣetúnṣe_wá_atọ̀ka_àkóónú + 1) <= 0xdfff) kóòdù_ẹyọ_ọ̀rọ̀ = 0x10000 + ((kóòdù_ẹyọ_ọ̀rọ̀ - 0xd800) << 10) + SMS.charAt(++ṣetúnṣe_wá_atọ̀ka_àkóónú) - 0xdc00;
            else if (kóòdù_ẹyọ_ọ̀rọ̀ >= 0xd800 && kóòdù_ẹyọ_ọ̀rọ̀ <= 0xdfff) kóòdù_ẹyọ_ọ̀rọ̀ = '?';
            if (kóòdù_ẹyọ_ọ̀rọ̀ < 128) 임시[쓴수++] = (byte)kóòdù_ẹyọ_ọ̀rọ̀;
            else if (kóòdù_ẹyọ_ọ̀rọ̀ < 2048) { 임시[쓴수++] = (byte)(192 | kóòdù_ẹyọ_ọ̀rọ̀ >> 6); 임시[쓴수++] = (byte)(128 | kóòdù_ẹyọ_ọ̀rọ̀ & 63); }
            else if (kóòdù_ẹyọ_ọ̀rọ̀ < 65536) { 임시[쓴수++] = (byte)(224 | kóòdù_ẹyọ_ọ̀rọ̀ >> 12); 임시[쓴수++] = (byte)(128 | kóòdù_ẹyọ_ọ̀rọ̀ >> 6 & 63); 임시[쓴수++] = (byte)(128 | kóòdù_ẹyọ_ọ̀rọ̀ & 63); }
            else { 임시[쓴수++] = (byte)(240 | kóòdù_ẹyọ_ọ̀rọ̀ >> 18); 임시[쓴수++] = (byte)(128 | kóòdù_ẹyọ_ọ̀rọ̀ >> 12 & 63); 임시[쓴수++] = (byte)(128 | kóòdù_ẹyọ_ọ̀rọ̀ >> 6 & 63); 임시[쓴수++] = (byte)(128 | kóòdù_ẹyọ_ọ̀rọ̀ & 63); }
        }
        byte[] 결과 = new byte[쓴수]; System.arraycopy(임시, 0, 결과, 0, 쓴수); return 결과;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String ṣàtúpalẹ̀_àrokò_détà(byte[] báìtì_iye) {
        StringBuilder 결과 = new StringBuilder();
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < báìtì_iye.length;) {
            int kóòdù_ẹyọ_ọ̀rọ̀ = báìtì_iye[ṣetúnṣe_wá_atọ̀ka_àkóónú++] & 255, 수 = kóòdù_ẹyọ_ọ̀rọ̀ < 128 ? 0 : kóòdù_ẹyọ_ọ̀rọ̀ >= 194 && kóòdù_ẹyọ_ọ̀rọ̀ < 224 ? 1 : kóòdù_ẹyọ_ọ̀rọ̀ >= 224 && kóòdù_ẹyọ_ọ̀rọ̀ < 240 ? 2 : kóòdù_ẹyọ_ọ̀rọ̀ >= 240 && kóòdù_ẹyọ_ọ̀rọ̀ <= 244 ? 3 : -1;
            if (수 < 0 || báìtì_iye.length - ṣetúnṣe_wá_atọ̀ka_àkóónú < 수) throw new 잘못된인수예외("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) kóòdù_ẹyọ_ọ̀rọ̀ &= (1 << (6 - 수)) - 1;
            for (int 안쪽자리 = 0; 안쪽자리 < 수; 안쪽자리++) { int Padà_sẹ́yìn_iye = báìtì_iye[ṣetúnṣe_wá_atọ̀ka_àkóónú++] & 255; if ((Padà_sẹ́yìn_iye & 192) != 128) throw new 잘못된인수예외("잘못된 UTF-8"); kóòdù_ẹyọ_ọ̀rọ̀ = kóòdù_ẹyọ_ọ̀rọ̀ << 6 | Padà_sẹ́yìn_iye & 63; }
            if (kóòdù_ẹyọ_ọ̀rọ̀ < 최소 || kóòdù_ẹyọ_ọ̀rọ̀ > 0x10ffff || kóòdù_ẹyọ_ọ̀rọ̀ >= 0xd800 && kóòdù_ẹyọ_ọ̀rọ̀ <= 0xdfff) throw new 잘못된인수예외("잘못된 UTF-8");
            if (kóòdù_ẹyọ_ọ̀rọ̀ < 65536) 결과.append((char)kóòdù_ẹyọ_ọ̀rọ̀);
            else { kóòdù_ẹyọ_ọ̀rọ̀ -= 65536; 결과.append((char)(0xd800 | kóòdù_ẹyọ_ọ̀rọ̀ >> 10)); 결과.append((char)(0xdc00 | kóòdù_ẹyọ_ọ̀rọ̀ & 1023)); }
        }
        return 결과.toString();
    }
}
