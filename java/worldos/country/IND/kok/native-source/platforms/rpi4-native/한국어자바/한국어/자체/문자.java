// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 문자(文字), एनकोडिंग_मोल(符號): UTF-8 바이트와 UTF-16 문자열의 CONVERT_मोल. सामान्य_स्थितीर_येवचें_मोल/조합 입력기는 별개다. */
public final class 문자 {
    public static int बायट_COUNT(byte[] डेटा) { return डेटा.length; }
    private 문자() {}
    public static int लांबाय_मोल(String SMS) { return SMS.length(); }
    public static boolean 같음(String 앞, String फाटीं_मोल) { return 앞 == null ? फाटीं_मोल == null : 앞.equals(फाटीं_मोल); }
    public static String दसोवचें_SMS(String 앞, String फाटीं_मोल) { return 앞.concat(फाटीं_मोल); }
    public static String कातरप_मोल(String SMS, int चलोवप, int 끝) { return SMS.substring(चलोवप, 끝); }
    public static int व्याकरणी_फोडणिशी_पुर्णांक(String SMS) { try { return Integer.parseInt(SMS); } catch (NumberFormatException चूक) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String बरोवचें_पुर्णांक_मोल(int 수) { return Integer.toString(수); }
    public static int वर्ण_कोड_COUNT(String SMS) {
        int 수 = 0;
        for (int लूप_INDEX = 0; लूप_INDEX < SMS.length(); लूप_INDEX++, 수++) {
            int वर्ण_कोड = SMS.charAt(लूप_INDEX);
            if (वर्ण_कोड >= 0xd800 && वर्ण_कोड <= 0xdbff && लूप_INDEX + 1 < SMS.length() && SMS.charAt(लूप_INDEX + 1) >= 0xdc00 && SMS.charAt(लूप_INDEX + 1) <= 0xdfff) लूप_INDEX++;
        }
        return 수;
    }
    public static byte[] 부호화(String SMS) {
        byte[] 임시 = new byte[SMS.length() * 3]; int 쓴수 = 0;
        for (int लूप_INDEX = 0; लूप_INDEX < SMS.length(); लूप_INDEX++) {
            int वर्ण_कोड = SMS.charAt(लूप_INDEX);
            if (वर्ण_कोड >= 0xd800 && वर्ण_कोड <= 0xdbff && लूप_INDEX + 1 < SMS.length() && SMS.charAt(लूप_INDEX + 1) >= 0xdc00 && SMS.charAt(लूप_INDEX + 1) <= 0xdfff) वर्ण_कोड = 0x10000 + ((वर्ण_कोड - 0xd800) << 10) + SMS.charAt(++लूप_INDEX) - 0xdc00;
            else if (वर्ण_कोड >= 0xd800 && वर्ण_कोड <= 0xdfff) वर्ण_कोड = '?';
            if (वर्ण_कोड < 128) 임시[쓴수++] = (byte)वर्ण_कोड;
            else if (वर्ण_कोड < 2048) { 임시[쓴수++] = (byte)(192 | वर्ण_कोड >> 6); 임시[쓴수++] = (byte)(128 | वर्ण_कोड & 63); }
            else if (वर्ण_कोड < 65536) { 임시[쓴수++] = (byte)(224 | वर्ण_कोड >> 12); 임시[쓴수++] = (byte)(128 | वर्ण_कोड >> 6 & 63); 임시[쓴수++] = (byte)(128 | वर्ण_कोड & 63); }
            else { 임시[쓴수++] = (byte)(240 | वर्ण_कोड >> 18); 임시[쓴수++] = (byte)(128 | वर्ण_कोड >> 12 & 63); 임시[쓴수++] = (byte)(128 | वर्ण_कोड >> 6 & 63); 임시[쓴수++] = (byte)(128 | वर्ण_कोड & 63); }
        }
        byte[] मेजप = new byte[쓴수]; System.arraycopy(임시, 0, मेजप, 0, 쓴수); return मेजप;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String डिक्रिप्ट_डेटा(byte[] बायट_मोल) {
        StringBuilder मेजप = new StringBuilder();
        for (int लूप_INDEX = 0; लूप_INDEX < बायट_मोल.length;) {
            int वर्ण_कोड = बायट_मोल[लूप_INDEX++] & 255, 수 = वर्ण_कोड < 128 ? 0 : वर्ण_कोड >= 194 && वर्ण_कोड < 224 ? 1 : वर्ण_कोड >= 224 && वर्ण_कोड < 240 ? 2 : वर्ण_कोड >= 240 && वर्ण_कोड <= 244 ? 3 : -1;
            if (수 < 0 || बायट_मोल.length - लूप_INDEX < 수) throw new 잘못된인수예외("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) वर्ण_कोड &= (1 << (6 - 수)) - 1;
            for (int भीतरलो_संयोग_स्थिती = 0; भीतरलो_संयोग_स्थिती < 수; भीतरलो_संयोग_स्थिती++) { int फाटीं_मोल = बायट_मोल[लूप_INDEX++] & 255; if ((फाटीं_मोल & 192) != 128) throw new 잘못된인수예외("잘못된 UTF-8"); वर्ण_कोड = वर्ण_कोड << 6 | फाटीं_मोल & 63; }
            if (वर्ण_कोड < 최소 || वर्ण_कोड > 0x10ffff || वर्ण_कोड >= 0xd800 && वर्ण_कोड <= 0xdfff) throw new 잘못된인수예외("잘못된 UTF-8");
            if (वर्ण_कोड < 65536) मेजप.append((char)वर्ण_कोड);
            else { वर्ण_कोड -= 65536; मेजप.append((char)(0xd800 | वर्ण_कोड >> 10)); मेजप.append((char)(0xdc00 | वर्ण_कोड & 1023)); }
        }
        return मेजप.toString();
    }
}
