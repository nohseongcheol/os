// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int අගය(); }
class පසුබිම_අගය { static int පිළියෙල_කරන්න = 7; int 수; String නම; පසුබිම_අගය(int 수) { this.수 = 수; නම = "පසුබිම_අගය"; } int අගය() { return 수; } }
class ශාඛාව_අගය extends පසුබිම_අගය implements 계산가능 { ශාඛාව_අගය(int 수) { super(수); නම = "ශාඛාව_අගය"; } public int අගය() { return 수 * පිළියෙල_කරන්න; } }
public class 객체시험 {
    static int 초기 = පසුබිම_අගය.පිළියෙල_කරන්න + 2;
    static int ශාඛාව(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] විස්තාරක) {
        ශාඛාව_අගය 나 = new ශාඛාව_අගය(6); පසුබිම_අගය 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.නම + ":" + 다.අගය() + ":" + 라.අගය());
        System.out.println((다 instanceof ශාඛාව_අගය) + ":" + (다 instanceof 계산가능) + ":" + ශාඛාව(2) + ":" + 띄엄(100));
        Object[] ආරා_ව_අගය = new Object[3]; ආරා_ව_අගය[0] = 나; ආරා_ව_අගය[1] = "한글😀"; System.gc();
        System.out.println(((ශාඛාව_අගය)ආරා_ව_අගය[0]).අගය()); System.out.println((String)ආරා_ව_අගය[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] බයිටය_අගය = new byte[1]; බයිටය_අගය[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(බයිටය_අගය[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
