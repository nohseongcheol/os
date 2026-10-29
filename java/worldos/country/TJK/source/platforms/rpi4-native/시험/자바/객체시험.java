// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int қимат(); }
class Пасзамина_қимат { static int Омода_кардан = 7; int 수; String Ном; Пасзамина_қимат(int 수) { this.수 = 수; Ном = "Пасзамина_қимат"; } int қимат() { return 수; } }
class шоха_қимат extends Пасзамина_қимат implements 계산가능 { шоха_қимат(int 수) { super(수); Ном = "шоха_қимат"; } public int қимат() { return 수 * Омода_кардан; } }
public class 객체시험 {
    static int 초기 = Пасзамина_қимат.Омода_кардан + 2;
    static int шоха(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] 인수) {
        шоха_қимат 나 = new шоха_қимат(6); Пасзамина_қимат 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.Ном + ":" + 다.қимат() + ":" + 라.қимат());
        System.out.println((다 instanceof шоха_қимат) + ":" + (다 instanceof 계산가능) + ":" + шоха(2) + ":" + 띄엄(100));
        Object[] қатор_қимат = new Object[3]; қатор_қимат[0] = 나; қатор_қимат[1] = "한글😀"; System.gc();
        System.out.println(((шоха_қимат)қатор_қимат[0]).қимат()); System.out.println((String)қатор_қимат[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] байт_қимат = new byte[1]; байт_қимат[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(байт_қимат[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
