// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int iye(); }
class Àgbétẹ́lẹ̀_iye { static int gbaradì = 7; int 수; String Orúkọ; Àgbétẹ́lẹ̀_iye(int 수) { this.수 = 수; Orúkọ = "Àgbétẹ́lẹ̀_iye"; } int iye() { return 수; } }
class ẹ̀ka_iye extends Àgbétẹ́lẹ̀_iye implements 계산가능 { ẹ̀ka_iye(int 수) { super(수); Orúkọ = "ẹ̀ka_iye"; } public int iye() { return 수 * gbaradì; } }
public class 객체시험 {
    static int 초기 = Àgbétẹ́lẹ̀_iye.gbaradì + 2;
    static int ẹ̀ka(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] 인수) {
        ẹ̀ka_iye 나 = new ẹ̀ka_iye(6); Àgbétẹ́lẹ̀_iye 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.Orúkọ + ":" + 다.iye() + ":" + 라.iye());
        System.out.println((다 instanceof ẹ̀ka_iye) + ":" + (다 instanceof 계산가능) + ":" + ẹ̀ka(2) + ":" + 띄엄(100));
        Object[] ÀRÉÈ_iye = new Object[3]; ÀRÉÈ_iye[0] = 나; ÀRÉÈ_iye[1] = "한글😀"; System.gc();
        System.out.println(((ẹ̀ka_iye)ÀRÉÈ_iye[0]).iye()); System.out.println((String)ÀRÉÈ_iye[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] báìtì_iye = new byte[1]; báìtì_iye[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(báìtì_iye[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
