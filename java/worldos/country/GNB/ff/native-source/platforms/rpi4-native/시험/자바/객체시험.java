// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int njaru(); }
class cakkital_njaru { static int Heblu = 7; int 수; String innde; cakkital_njaru(int 수) { this.수 = 수; innde = "cakkital_njaru"; } int njaru() { return 수; } }
class 가지 extends cakkital_njaru implements 계산가능 { 가지(int 수) { super(수); innde = "가지"; } public int njaru() { return 수 * Heblu; } }
public class 객체시험 {
    static int 초기 = cakkital_njaru.Heblu + 2;
    static int 분기(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] 인수) {
        가지 나 = new 가지(6); cakkital_njaru 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.innde + ":" + 다.njaru() + ":" + 라.njaru());
        System.out.println((다 instanceof 가지) + ":" + (다 instanceof 계산가능) + ":" + 분기(2) + ":" + 띄엄(100));
        Object[] 배열 = new Object[3]; 배열[0] = 나; 배열[1] = "한글😀"; System.gc();
        System.out.println(((가지)배열[0]).njaru()); System.out.println((String)배열[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] oktee_njaru = new byte[1]; oktee_njaru[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(oktee_njaru[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
