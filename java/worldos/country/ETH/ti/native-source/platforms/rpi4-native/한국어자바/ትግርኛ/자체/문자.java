// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ትግርኛ.자체;
/** 문자(文字), ምምስጣር_ዋጋ(符號): UTF-8 바이트와 UTF-16 문자열의 변환. ኖርማላይዝ_ዋጋ/조합 입력기는 별개다. */
public final class 문자 {
    public static int 바이트수(byte[] ሓበሬታ) { return ሓበሬታ.length; }
    private 문자() {}
    public static int ንውሓት_ዋጋ(String ጽሑፍ) { return ጽሑፍ.length(); }
    public static boolean 같음(String 앞, String ድሕሪት_ዋጋ) { return 앞 == null ? ድሕሪት_ዋጋ == null : 앞.equals(ድሕሪት_ዋጋ); }
    public static String ለጥፍ_ጽሑፍ(String 앞, String ድሕሪት_ዋጋ) { return 앞.concat(ድሕሪት_ዋጋ); }
    public static String ቁረጽ_ዋጋ(String ጽሑፍ, int ኣኺድ, int 끝) { return ጽሑፍ.substring(ኣኺድ, 끝); }
    public static int 정수읽기(String ጽሑፍ) { try { return Integer.parseInt(ጽሑፍ); } catch (NumberFormatException ጌጋ) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String ጸሓፍ_ኢንቲጀር_ዋጋ(int 수) { return Integer.toString(수); }
    public static int 코드포인트수(String ጽሑፍ) {
        int 수 = 0;
        for (int ደጋግም_መሐበሪ = 0; ደጋግም_መሐበሪ < ጽሑፍ.length(); ደጋግም_መሐበሪ++, 수++) {
            int ኮድ_ፊደል = ጽሑፍ.charAt(ደጋግም_መሐበሪ);
            if (ኮድ_ፊደል >= 0xd800 && ኮድ_ፊደል <= 0xdbff && ደጋግም_መሐበሪ + 1 < ጽሑፍ.length() && ጽሑፍ.charAt(ደጋግም_መሐበሪ + 1) >= 0xdc00 && ጽሑፍ.charAt(ደጋግም_መሐበሪ + 1) <= 0xdfff) ደጋግም_መሐበሪ++;
        }
        return 수;
    }
    public static byte[] 부호화(String ጽሑፍ) {
        byte[] 임시 = new byte[ጽሑፍ.length() * 3]; int 쓴수 = 0;
        for (int ደጋግም_መሐበሪ = 0; ደጋግም_መሐበሪ < ጽሑፍ.length(); ደጋግም_መሐበሪ++) {
            int ኮድ_ፊደል = ጽሑፍ.charAt(ደጋግም_መሐበሪ);
            if (ኮድ_ፊደል >= 0xd800 && ኮድ_ፊደል <= 0xdbff && ደጋግም_መሐበሪ + 1 < ጽሑፍ.length() && ጽሑፍ.charAt(ደጋግም_መሐበሪ + 1) >= 0xdc00 && ጽሑፍ.charAt(ደጋግም_መሐበሪ + 1) <= 0xdfff) ኮድ_ፊደል = 0x10000 + ((ኮድ_ፊደል - 0xd800) << 10) + ጽሑፍ.charAt(++ደጋግም_መሐበሪ) - 0xdc00;
            else if (ኮድ_ፊደል >= 0xd800 && ኮድ_ፊደል <= 0xdfff) ኮድ_ፊደል = '?';
            if (ኮድ_ፊደል < 128) 임시[쓴수++] = (byte)ኮድ_ፊደል;
            else if (ኮድ_ፊደል < 2048) { 임시[쓴수++] = (byte)(192 | ኮድ_ፊደል >> 6); 임시[쓴수++] = (byte)(128 | ኮድ_ፊደል & 63); }
            else if (ኮድ_ፊደል < 65536) { 임시[쓴수++] = (byte)(224 | ኮድ_ፊደል >> 12); 임시[쓴수++] = (byte)(128 | ኮድ_ፊደል >> 6 & 63); 임시[쓴수++] = (byte)(128 | ኮድ_ፊደል & 63); }
            else { 임시[쓴수++] = (byte)(240 | ኮድ_ፊደል >> 18); 임시[쓴수++] = (byte)(128 | ኮድ_ፊደል >> 12 & 63); 임시[쓴수++] = (byte)(128 | ኮድ_ፊደል >> 6 & 63); 임시[쓴수++] = (byte)(128 | ኮድ_ፊደል & 63); }
        }
        byte[] 결과 = new byte[쓴수]; System.arraycopy(임시, 0, 결과, 0, 쓴수); return 결과;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String ምስጢር_ፍታሕ_ሓበሬታ(byte[] ባይት_ዋጋ) {
        StringBuilder 결과 = new StringBuilder();
        for (int ደጋግም_መሐበሪ = 0; ደጋግም_መሐበሪ < ባይት_ዋጋ.length;) {
            int ኮድ_ፊደል = ባይት_ዋጋ[ደጋግም_መሐበሪ++] & 255, 수 = ኮድ_ፊደል < 128 ? 0 : ኮድ_ፊደል >= 194 && ኮድ_ፊደል < 224 ? 1 : ኮድ_ፊደል >= 224 && ኮድ_ፊደል < 240 ? 2 : ኮድ_ፊደል >= 240 && ኮድ_ፊደል <= 244 ? 3 : -1;
            if (수 < 0 || ባይት_ዋጋ.length - ደጋግም_መሐበሪ < 수) throw new 잘못된인수예외("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) ኮድ_ፊደል &= (1 << (6 - 수)) - 1;
            for (int 안쪽자리 = 0; 안쪽자리 < 수; 안쪽자리++) { int ድሕሪት_ዋጋ = ባይት_ዋጋ[ደጋግም_መሐበሪ++] & 255; if ((ድሕሪት_ዋጋ & 192) != 128) throw new 잘못된인수예외("잘못된 UTF-8"); ኮድ_ፊደል = ኮድ_ፊደል << 6 | ድሕሪት_ዋጋ & 63; }
            if (ኮድ_ፊደል < 최소 || ኮድ_ፊደል > 0x10ffff || ኮድ_ፊደል >= 0xd800 && ኮድ_ፊደል <= 0xdfff) throw new 잘못된인수예외("잘못된 UTF-8");
            if (ኮድ_ፊደል < 65536) 결과.append((char)ኮድ_ፊደል);
            else { ኮድ_ፊደል -= 65536; 결과.append((char)(0xd800 | ኮድ_ፊደል >> 10)); 결과.append((char)(0xdc00 | ኮድ_ፊደል & 1023)); }
        }
        return 결과.toString();
    }
}
