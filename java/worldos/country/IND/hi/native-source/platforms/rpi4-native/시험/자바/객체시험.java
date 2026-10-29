// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int मान(); }
class वॉलपेपर_मान { static int 준비 = 7; int 수; String नाम; वॉलपेपर_मान(int 수) { this.수 = 수; नाम = "वॉलपेपर_मान"; } int मान() { return 수; } }
class शाखा_मान extends वॉलपेपर_मान implements 계산가능 { शाखा_मान(int 수) { super(수); नाम = "शाखा_मान"; } public int मान() { return 수 * 준비; } }
public class 객체시험 {
    static int प्रारंभिक_स्थिति = वॉलपेपर_मान.준비 + 2;
    static int शाखा(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] तर्क) {
        शाखा_मान 나 = new शाखा_मान(6); वॉलपेपर_मान 다 = 나; 계산가능 라 = 나;
        System.out.println(प्रारंभिक_स्थिति + ":" + 나.नाम + ":" + 다.मान() + ":" + 라.मान());
        System.out.println((다 instanceof शाखा_मान) + ":" + (다 instanceof 계산가능) + ":" + शाखा(2) + ":" + 띄엄(100));
        Object[] सरणी_मान = new Object[3]; सरणी_मान[0] = 나; सरणी_मान[1] = "한글😀"; System.gc();
        System.out.println(((शाखा_मान)सरणी_मान[0]).मान()); System.out.println((String)सरणी_मान[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] बाइट_मान = new byte[1]; बाइट_मान[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] बूलियन_मान = {true};
        System.out.println(बाइट_मान[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + बूलियन_मान[0]);
    }
}
