// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 문자(文字), ᎪᏗᏍᎩ_ᏧᎬᏩᎶᏗᏯ(符號): UTF-8 바이트와 UTF-16 문자열의 변환. 정규화/조합 입력기는 별개다. */
public final class 문자 {
    public static int 바이트수(byte[] ᎦᏟᏌᏅᎯ) { return ᎦᏟᏌᏅᎯ.length; }
    private 문자() {}
    public static int ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ(String ᎠᎪᎵᏰᏗ) { return ᎠᎪᎵᏰᏗ.length(); }
    public static boolean 같음(String 앞, String ᎠᎰᏂ_ᏧᎬᏩᎶᏗᏯ) { return 앞 == null ? ᎠᎰᏂ_ᏧᎬᏩᎶᏗᏯ == null : 앞.equals(ᎠᎰᏂ_ᏧᎬᏩᎶᏗᏯ); }
    public static String ᏘᎦᏣᎴᏍᏙᏓ_ᎠᎪᎵᏰᏗ(String 앞, String ᎠᎰᏂ_ᏧᎬᏩᎶᏗᏯ) { return 앞.concat(ᎠᎰᏂ_ᏧᎬᏩᎶᏗᏯ); }
    public static String ᎯᎦᎳ_ᏧᎬᏩᎶᏗᏯ(String ᎠᎪᎵᏰᏗ, int ᎠᎢᏎᏍᏗ, int 끝) { return ᎠᎪᎵᏰᏗ.substring(ᎠᎢᏎᏍᏗ, 끝); }
    public static int 정수읽기(String ᎠᎪᎵᏰᏗ) { try { return Integer.parseInt(ᎠᎪᎵᏰᏗ); } catch (NumberFormatException ᎦᎵᏓᏍᏔᏅ) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String ᎪᏪᎶᏗ_integer_ᏧᎬᏩᎶᏗᏯ(int 수) { return Integer.toString(수); }
    public static int 코드포인트수(String ᎠᎪᎵᏰᏗ) {
        int 수 = 0;
        for (int ᎬᎪᏘᎶᏓ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ = 0; ᎬᎪᏘᎶᏓ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ < ᎠᎪᎵᏰᏗ.length(); ᎬᎪᏘᎶᏓ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ++, 수++) {
            int 문자값 = ᎠᎪᎵᏰᏗ.charAt(ᎬᎪᏘᎶᏓ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ);
            if (문자값 >= 0xd800 && 문자값 <= 0xdbff && ᎬᎪᏘᎶᏓ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ + 1 < ᎠᎪᎵᏰᏗ.length() && ᎠᎪᎵᏰᏗ.charAt(ᎬᎪᏘᎶᏓ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ + 1) >= 0xdc00 && ᎠᎪᎵᏰᏗ.charAt(ᎬᎪᏘᎶᏓ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ + 1) <= 0xdfff) ᎬᎪᏘᎶᏓ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ++;
        }
        return 수;
    }
    public static byte[] 부호화(String ᎠᎪᎵᏰᏗ) {
        byte[] 임시 = new byte[ᎠᎪᎵᏰᏗ.length() * 3]; int 쓴수 = 0;
        for (int ᎬᎪᏘᎶᏓ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ = 0; ᎬᎪᏘᎶᏓ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ < ᎠᎪᎵᏰᏗ.length(); ᎬᎪᏘᎶᏓ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ++) {
            int 문자값 = ᎠᎪᎵᏰᏗ.charAt(ᎬᎪᏘᎶᏓ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ);
            if (문자값 >= 0xd800 && 문자값 <= 0xdbff && ᎬᎪᏘᎶᏓ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ + 1 < ᎠᎪᎵᏰᏗ.length() && ᎠᎪᎵᏰᏗ.charAt(ᎬᎪᏘᎶᏓ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ + 1) >= 0xdc00 && ᎠᎪᎵᏰᏗ.charAt(ᎬᎪᏘᎶᏓ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ + 1) <= 0xdfff) 문자값 = 0x10000 + ((문자값 - 0xd800) << 10) + ᎠᎪᎵᏰᏗ.charAt(++ᎬᎪᏘᎶᏓ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ) - 0xdc00;
            else if (문자값 >= 0xd800 && 문자값 <= 0xdfff) 문자값 = '?';
            if (문자값 < 128) 임시[쓴수++] = (byte)문자값;
            else if (문자값 < 2048) { 임시[쓴수++] = (byte)(192 | 문자값 >> 6); 임시[쓴수++] = (byte)(128 | 문자값 & 63); }
            else if (문자값 < 65536) { 임시[쓴수++] = (byte)(224 | 문자값 >> 12); 임시[쓴수++] = (byte)(128 | 문자값 >> 6 & 63); 임시[쓴수++] = (byte)(128 | 문자값 & 63); }
            else { 임시[쓴수++] = (byte)(240 | 문자값 >> 18); 임시[쓴수++] = (byte)(128 | 문자값 >> 12 & 63); 임시[쓴수++] = (byte)(128 | 문자값 >> 6 & 63); 임시[쓴수++] = (byte)(128 | 문자값 & 63); }
        }
        byte[] 결과 = new byte[쓴수]; System.arraycopy(임시, 0, 결과, 0, 쓴수); return 결과;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String ᎠᎭᏓᏗᎭ_ᎦᏟᏌᏅᎯ(byte[] byte_ᏧᎬᏩᎶᏗᏯ) {
        StringBuilder 결과 = new StringBuilder();
        for (int ᎬᎪᏘᎶᏓ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ = 0; ᎬᎪᏘᎶᏓ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ < byte_ᏧᎬᏩᎶᏗᏯ.length;) {
            int 문자값 = byte_ᏧᎬᏩᎶᏗᏯ[ᎬᎪᏘᎶᏓ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ++] & 255, 수 = 문자값 < 128 ? 0 : 문자값 >= 194 && 문자값 < 224 ? 1 : 문자값 >= 224 && 문자값 < 240 ? 2 : 문자값 >= 240 && 문자값 <= 244 ? 3 : -1;
            if (수 < 0 || byte_ᏧᎬᏩᎶᏗᏯ.length - ᎬᎪᏘᎶᏓ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ < 수) throw new 잘못된인수예외("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) 문자값 &= (1 << (6 - 수)) - 1;
            for (int 안쪽자리 = 0; 안쪽자리 < 수; 안쪽자리++) { int ᎠᎰᏂ_ᏧᎬᏩᎶᏗᏯ = byte_ᏧᎬᏩᎶᏗᏯ[ᎬᎪᏘᎶᏓ_ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ++] & 255; if ((ᎠᎰᏂ_ᏧᎬᏩᎶᏗᏯ & 192) != 128) throw new 잘못된인수예외("잘못된 UTF-8"); 문자값 = 문자값 << 6 | ᎠᎰᏂ_ᏧᎬᏩᎶᏗᏯ & 63; }
            if (문자값 < 최소 || 문자값 > 0x10ffff || 문자값 >= 0xd800 && 문자값 <= 0xdfff) throw new 잘못된인수예외("잘못된 UTF-8");
            if (문자값 < 65536) 결과.append((char)문자값);
            else { 문자값 -= 65536; 결과.append((char)(0xd800 | 문자값 >> 10)); 결과.append((char)(0xdc00 | 문자값 & 1023)); }
        }
        return 결과.toString();
    }
}
