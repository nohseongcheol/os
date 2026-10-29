// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package हिंदी.निज;
/** 문자(文字), एन्कोडिंग_मान(符號): UTF-8 바이트와 UTF-16 문자열의 रूपांतरित_करें_मान. सामान्य_करें_मान/조합 입력기는 별개다. */
public final class 문자 {
    public static int 바이트수(byte[] आँकड़े) { return आँकड़े.length; }
    private 문자() {}
    public static int 길이(String पाठ) { return पाठ.length(); }
    public static boolean 같음(String सामने_मान, String वापस_मान) { return सामने_मान == null ? वापस_मान == null : सामने_मान.equals(वापस_मान); }
    public static String चिपकाएँ_पाठ(String सामने_मान, String वापस_मान) { return सामने_मान.concat(वापस_मान); }
    public static String काटें_मान(String पाठ, int चलाएँ, int 끝) { return पाठ.substring(चलाएँ, 끝); }
    public static int पार्स_करें_पूर्णांक(String पाठ) { try { return Integer.parseInt(पाठ); } catch (NumberFormatException त्रुटि) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String लिखना_पूर्णांक_मान(int 수) { return Integer.toString(수); }
    public static int 코드포인트수(String पाठ) {
        int 수 = 0;
        for (int लूप_इंडेक्स = 0; लूप_इंडेक्स < पाठ.length(); लूप_इंडेक्स++, 수++) {
            int वर्ण_कोड = पाठ.charAt(लूप_इंडेक्स);
            if (वर्ण_कोड >= 0xd800 && वर्ण_कोड <= 0xdbff && लूप_इंडेक्स + 1 < पाठ.length() && पाठ.charAt(लूप_इंडेक्स + 1) >= 0xdc00 && पाठ.charAt(लूप_इंडेक्स + 1) <= 0xdfff) लूप_इंडेक्स++;
        }
        return 수;
    }
    public static byte[] 부호화(String पाठ) {
        byte[] 임시 = new byte[पाठ.length() * 3]; int 쓴수 = 0;
        for (int लूप_इंडेक्स = 0; लूप_इंडेक्स < पाठ.length(); लूप_इंडेक्स++) {
            int वर्ण_कोड = पाठ.charAt(लूप_इंडेक्स);
            if (वर्ण_कोड >= 0xd800 && वर्ण_कोड <= 0xdbff && लूप_इंडेक्स + 1 < पाठ.length() && पाठ.charAt(लूप_इंडेक्स + 1) >= 0xdc00 && पाठ.charAt(लूप_इंडेक्स + 1) <= 0xdfff) वर्ण_कोड = 0x10000 + ((वर्ण_कोड - 0xd800) << 10) + पाठ.charAt(++लूप_इंडेक्स) - 0xdc00;
            else if (वर्ण_कोड >= 0xd800 && वर्ण_कोड <= 0xdfff) वर्ण_कोड = '?';
            if (वर्ण_कोड < 128) 임시[쓴수++] = (byte)वर्ण_कोड;
            else if (वर्ण_कोड < 2048) { 임시[쓴수++] = (byte)(192 | वर्ण_कोड >> 6); 임시[쓴수++] = (byte)(128 | वर्ण_कोड & 63); }
            else if (वर्ण_कोड < 65536) { 임시[쓴수++] = (byte)(224 | वर्ण_कोड >> 12); 임시[쓴수++] = (byte)(128 | वर्ण_कोड >> 6 & 63); 임시[쓴수++] = (byte)(128 | वर्ण_कोड & 63); }
            else { 임시[쓴수++] = (byte)(240 | वर्ण_कोड >> 18); 임시[쓴수++] = (byte)(128 | वर्ण_कोड >> 12 & 63); 임시[쓴수++] = (byte)(128 | वर्ण_कोड >> 6 & 63); 임시[쓴수++] = (byte)(128 | वर्ण_कोड & 63); }
        }
        byte[] परिणाम = new byte[쓴수]; System.arraycopy(임시, 0, परिणाम, 0, 쓴수); return परिणाम;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String डिक्रिप्ट_करें_डेटा(byte[] बाइट_मान) {
        StringBuilder परिणाम = new StringBuilder();
        for (int लूप_इंडेक्स = 0; लूप_इंडेक्स < बाइट_मान.length;) {
            int वर्ण_कोड = बाइट_मान[लूप_इंडेक्स++] & 255, 수 = वर्ण_कोड < 128 ? 0 : वर्ण_कोड >= 194 && वर्ण_कोड < 224 ? 1 : वर्ण_कोड >= 224 && वर्ण_कोड < 240 ? 2 : वर्ण_कोड >= 240 && वर्ण_कोड <= 244 ? 3 : -1;
            if (수 < 0 || बाइट_मान.length - लूप_इंडेक्स < 수) throw new अमान्य_तर्क_अपवाद("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) वर्ण_कोड &= (1 << (6 - 수)) - 1;
            for (int इनर_पद = 0; इनर_पद < 수; इनर_पद++) { int वापस_मान = बाइट_मान[लूप_इंडेक्स++] & 255; if ((वापस_मान & 192) != 128) throw new अमान्य_तर्क_अपवाद("잘못된 UTF-8"); वर्ण_कोड = वर्ण_कोड << 6 | वापस_मान & 63; }
            if (वर्ण_कोड < 최소 || वर्ण_कोड > 0x10ffff || वर्ण_कोड >= 0xd800 && वर्ण_कोड <= 0xdfff) throw new अमान्य_तर्क_अपवाद("잘못된 UTF-8");
            if (वर्ण_कोड < 65536) परिणाम.append((char)वर्ण_कोड);
            else { वर्ण_कोड -= 65536; परिणाम.append((char)(0xd800 | वर्ण_कोड >> 10)); परिणाम.append((char)(0xdc00 | वर्ण_कोड & 1023)); }
        }
        return परिणाम.toString();
    }
}
