// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int மதிப்பு(); }
class பின்புல_மதிப்பு { static int தயார்படுத்த = 7; int 수; String பெயர்; பின்புல_மதிப்பு(int 수) { this.수 = 수; பெயர் = "பின்புல_மதிப்பு"; } int மதிப்பு() { return 수; } }
class கிளை_மதிப்பு extends பின்புல_மதிப்பு implements 계산가능 { கிளை_மதிப்பு(int 수) { super(수); பெயர் = "கிளை_மதிப்பு"; } public int மதிப்பு() { return 수 * தயார்படுத்த; } }
public class 객체시험 {
    static int 초기 = பின்புல_மதிப்பு.தயார்படுத்த + 2;
    static int கிளை(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] செயலுருபுகள்) {
        கிளை_மதிப்பு 나 = new கிளை_மதிப்பு(6); பின்புல_மதிப்பு 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.பெயர் + ":" + 다.மதிப்பு() + ":" + 라.மதிப்பு());
        System.out.println((다 instanceof கிளை_மதிப்பு) + ":" + (다 instanceof 계산가능) + ":" + கிளை(2) + ":" + 띄엄(100));
        Object[] கோவை_மதிப்பு_ed437109 = new Object[3]; கோவை_மதிப்பு_ed437109[0] = 나; கோவை_மதிப்பு_ed437109[1] = "한글😀"; System.gc();
        System.out.println(((கிளை_மதிப்பு)கோவை_மதிப்பு_ed437109[0]).மதிப்பு()); System.out.println((String)கோவை_மதிப்பு_ed437109[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] பைட்_மதிப்பு = new byte[1]; பைட்_மதிப்பு[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(பைட்_மதிப்பு[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
