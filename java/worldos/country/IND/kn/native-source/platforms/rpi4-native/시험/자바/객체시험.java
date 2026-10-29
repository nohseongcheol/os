// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int ಮೌಲ್ಯ(); }
class ಹಿನ್ನೆಲೆ_ಮೌಲ್ಯ { static int ಸಿದ್ಧಪಡಿಸು = 7; int 수; String ಹೆಸರು; ಹಿನ್ನೆಲೆ_ಮೌಲ್ಯ(int 수) { this.수 = 수; ಹೆಸರು = "ಹಿನ್ನೆಲೆ_ಮೌಲ್ಯ"; } int ಮೌಲ್ಯ() { return 수; } }
class ಶಾಖೆ_ಮೌಲ್ಯ extends ಹಿನ್ನೆಲೆ_ಮೌಲ್ಯ implements 계산가능 { ಶಾಖೆ_ಮೌಲ್ಯ(int 수) { super(수); ಹೆಸರು = "ಶಾಖೆ_ಮೌಲ್ಯ"; } public int ಮೌಲ್ಯ() { return 수 * ಸಿದ್ಧಪಡಿಸು; } }
public class 객체시험 {
    static int 초기 = ಹಿನ್ನೆಲೆ_ಮೌಲ್ಯ.ಸಿದ್ಧಪಡಿಸು + 2;
    static int ಶಾಖೆ(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] 인수) {
        ಶಾಖೆ_ಮೌಲ್ಯ 나 = new ಶಾಖೆ_ಮೌಲ್ಯ(6); ಹಿನ್ನೆಲೆ_ಮೌಲ್ಯ 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.ಹೆಸರು + ":" + 다.ಮೌಲ್ಯ() + ":" + 라.ಮೌಲ್ಯ());
        System.out.println((다 instanceof ಶಾಖೆ_ಮೌಲ್ಯ) + ":" + (다 instanceof 계산가능) + ":" + ಶಾಖೆ(2) + ":" + 띄엄(100));
        Object[] ಅರೇ_ಮೌಲ್ಯ = new Object[3]; ಅರೇ_ಮೌಲ್ಯ[0] = 나; ಅರೇ_ಮೌಲ್ಯ[1] = "한글😀"; System.gc();
        System.out.println(((ಶಾಖೆ_ಮೌಲ್ಯ)ಅರೇ_ಮೌಲ್ಯ[0]).ಮೌಲ್ಯ()); System.out.println((String)ಅರೇ_ಮೌಲ್ಯ[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] ಬೈಟ್_ಮೌಲ್ಯ = new byte[1]; ಬೈಟ್_ಮೌಲ್ಯ[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(ಬೈಟ್_ಮೌಲ್ಯ[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
