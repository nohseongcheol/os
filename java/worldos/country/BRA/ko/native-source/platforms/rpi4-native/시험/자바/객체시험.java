// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int 값(); }
class 바탕 { static int 준비 = 7; int 수; String 이름; 바탕(int 수) { this.수 = 수; 이름 = "바탕"; } int 값() { return 수; } }
class 가지 extends 바탕 implements 계산가능 { 가지(int 수) { super(수); 이름 = "가지"; } public int 값() { return 수 * 준비; } }
public class 객체시험 {
    static int 초기 = 바탕.준비 + 2;
    static int 분기(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] 인수) {
        가지 나 = new 가지(6); 바탕 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.이름 + ":" + 다.값() + ":" + 라.값());
        System.out.println((다 instanceof 가지) + ":" + (다 instanceof 계산가능) + ":" + 분기(2) + ":" + 띄엄(100));
        Object[] 배열 = new Object[3]; 배열[0] = 나; 배열[1] = "한글😀"; System.gc();
        System.out.println(((가지)배열[0]).값()); System.out.println((String)배열[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] 바이트 = new byte[1]; 바이트[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(바이트[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
