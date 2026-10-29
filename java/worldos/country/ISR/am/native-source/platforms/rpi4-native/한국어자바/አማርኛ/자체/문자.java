// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package አማርኛ.자체;
/** 문자(文字), በኮድ_መክተት_እሴት(符號): UTF-8 바이트와 UTF-16 문자열의 변환. አጠናቅር_እሴት/조합 입력기는 별개다. */
public final class 문자 {
    public static int 바이트수(byte[] ውሂብ) { return ውሂብ.length; }
    private 문자() {}
    public static int ርዝመት_እሴት(String ጽሁፍ) { return ጽሁፍ.length(); }
    public static boolean 같음(String ፊት_እሴት, String ተመለስ_እሴት) { return ፊት_እሴት == null ? ተመለስ_እሴት == null : ፊት_እሴት.equals(ተመለስ_እሴት); }
    public static String ለጥፍ_ጽሁፍ(String ፊት_እሴት, String ተመለስ_እሴት) { return ፊት_እሴት.concat(ተመለስ_እሴት); }
    public static String ቁረጥ_እሴት(String ጽሁፍ, int ማስኬጃ, int 끝) { return ጽሁፍ.substring(ማስኬጃ, 끝); }
    public static int ተንትን_ኢንተጀር(String ጽሁፍ) { try { return Integer.parseInt(ጽሁፍ); } catch (NumberFormatException ስህተት) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String ጻፍ_ኢንተጀር_እሴት(int 수) { return Integer.toString(수); }
    public static int 코드포인트수(String ጽሁፍ) {
        int 수 = 0;
        for (int ድግግሞሽ_መረጃ_ጠቆመ = 0; ድግግሞሽ_መረጃ_ጠቆመ < ጽሁፍ.length(); ድግግሞሽ_መረጃ_ጠቆመ++, 수++) {
            int የቁምፊ_ኮድ = ጽሁፍ.charAt(ድግግሞሽ_መረጃ_ጠቆመ);
            if (የቁምፊ_ኮድ >= 0xd800 && የቁምፊ_ኮድ <= 0xdbff && ድግግሞሽ_መረጃ_ጠቆመ + 1 < ጽሁፍ.length() && ጽሁፍ.charAt(ድግግሞሽ_መረጃ_ጠቆመ + 1) >= 0xdc00 && ጽሁፍ.charAt(ድግግሞሽ_መረጃ_ጠቆመ + 1) <= 0xdfff) ድግግሞሽ_መረጃ_ጠቆመ++;
        }
        return 수;
    }
    public static byte[] 부호화(String ጽሁፍ) {
        byte[] 임시 = new byte[ጽሁፍ.length() * 3]; int 쓴수 = 0;
        for (int ድግግሞሽ_መረጃ_ጠቆመ = 0; ድግግሞሽ_መረጃ_ጠቆመ < ጽሁፍ.length(); ድግግሞሽ_መረጃ_ጠቆመ++) {
            int የቁምፊ_ኮድ = ጽሁፍ.charAt(ድግግሞሽ_መረጃ_ጠቆመ);
            if (የቁምፊ_ኮድ >= 0xd800 && የቁምፊ_ኮድ <= 0xdbff && ድግግሞሽ_መረጃ_ጠቆመ + 1 < ጽሁፍ.length() && ጽሁፍ.charAt(ድግግሞሽ_መረጃ_ጠቆመ + 1) >= 0xdc00 && ጽሁፍ.charAt(ድግግሞሽ_መረጃ_ጠቆመ + 1) <= 0xdfff) የቁምፊ_ኮድ = 0x10000 + ((የቁምፊ_ኮድ - 0xd800) << 10) + ጽሁፍ.charAt(++ድግግሞሽ_መረጃ_ጠቆመ) - 0xdc00;
            else if (የቁምፊ_ኮድ >= 0xd800 && የቁምፊ_ኮድ <= 0xdfff) የቁምፊ_ኮድ = '?';
            if (የቁምፊ_ኮድ < 128) 임시[쓴수++] = (byte)የቁምፊ_ኮድ;
            else if (የቁምፊ_ኮድ < 2048) { 임시[쓴수++] = (byte)(192 | የቁምፊ_ኮድ >> 6); 임시[쓴수++] = (byte)(128 | የቁምፊ_ኮድ & 63); }
            else if (የቁምፊ_ኮድ < 65536) { 임시[쓴수++] = (byte)(224 | የቁምፊ_ኮድ >> 12); 임시[쓴수++] = (byte)(128 | የቁምፊ_ኮድ >> 6 & 63); 임시[쓴수++] = (byte)(128 | የቁምፊ_ኮድ & 63); }
            else { 임시[쓴수++] = (byte)(240 | የቁምፊ_ኮድ >> 18); 임시[쓴수++] = (byte)(128 | የቁምፊ_ኮድ >> 12 & 63); 임시[쓴수++] = (byte)(128 | የቁምፊ_ኮድ >> 6 & 63); 임시[쓴수++] = (byte)(128 | የቁምፊ_ኮድ & 63); }
        }
        byte[] ልኬት = new byte[쓴수]; System.arraycopy(임시, 0, ልኬት, 0, 쓴수); return ልኬት;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String ምስጠራውን_ፍታ_ውሂብ(byte[] ባይት_እሴት) {
        StringBuilder ልኬት = new StringBuilder();
        for (int ድግግሞሽ_መረጃ_ጠቆመ = 0; ድግግሞሽ_መረጃ_ጠቆመ < ባይት_እሴት.length;) {
            int የቁምፊ_ኮድ = ባይት_እሴት[ድግግሞሽ_መረጃ_ጠቆመ++] & 255, 수 = የቁምፊ_ኮድ < 128 ? 0 : የቁምፊ_ኮድ >= 194 && የቁምፊ_ኮድ < 224 ? 1 : የቁምፊ_ኮድ >= 224 && የቁምፊ_ኮድ < 240 ? 2 : የቁምፊ_ኮድ >= 240 && የቁምፊ_ኮድ <= 244 ? 3 : -1;
            if (수 < 0 || ባይት_እሴት.length - ድግግሞሽ_መረጃ_ጠቆመ < 수) throw new ልክ_ያልኾነ_ነጋሪ_እሴት_ልዩነት("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) የቁምፊ_ኮድ &= (1 << (6 - 수)) - 1;
            for (int ውስጣዊ_መገናኛ_በቦታ_አስቀመጠ = 0; ውስጣዊ_መገናኛ_በቦታ_አስቀመጠ < 수; ውስጣዊ_መገናኛ_በቦታ_አስቀመጠ++) { int ተመለስ_እሴት = ባይት_እሴት[ድግግሞሽ_መረጃ_ጠቆመ++] & 255; if ((ተመለስ_እሴት & 192) != 128) throw new ልክ_ያልኾነ_ነጋሪ_እሴት_ልዩነት("잘못된 UTF-8"); የቁምፊ_ኮድ = የቁምፊ_ኮድ << 6 | ተመለስ_እሴት & 63; }
            if (የቁምፊ_ኮድ < 최소 || የቁምፊ_ኮድ > 0x10ffff || የቁምፊ_ኮድ >= 0xd800 && የቁምፊ_ኮድ <= 0xdfff) throw new ልክ_ያልኾነ_ነጋሪ_እሴት_ልዩነት("잘못된 UTF-8");
            if (የቁምፊ_ኮድ < 65536) ልኬት.append((char)የቁምፊ_ኮድ);
            else { የቁምፊ_ኮድ -= 65536; ልኬት.append((char)(0xd800 | የቁምፊ_ኮድ >> 10)); ልኬት.append((char)(0xdc00 | የቁምፊ_ኮድ & 1023)); }
        }
        return ልኬት.toString();
    }
}
