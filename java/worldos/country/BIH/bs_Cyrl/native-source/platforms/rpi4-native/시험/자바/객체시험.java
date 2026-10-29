// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int вриједност(); }
class позадина_вриједност { static int Припремити = 7; int 수; String назив; позадина_вриједност(int 수) { this.수 = 수; назив = "позадина_вриједност"; } int вриједност() { return 수; } }
class огранак_вриједност extends позадина_вриједност implements 계산가능 { огранак_вриједност(int 수) { super(수); назив = "огранак_вриједност"; } public int вриједност() { return 수 * Припремити; } }
public class 객체시험 {
    static int 초기 = позадина_вриједност.Припремити + 2;
    static int огранак(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] 인수) {
        огранак_вриједност 나 = new огранак_вриједност(6); позадина_вриједност 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.назив + ":" + 다.вриједност() + ":" + 라.вриједност());
        System.out.println((다 instanceof огранак_вриједност) + ":" + (다 instanceof 계산가능) + ":" + огранак(2) + ":" + 띄엄(100));
        Object[] низ_вриједност = new Object[3]; низ_вриједност[0] = 나; низ_вриједност[1] = "한글😀"; System.gc();
        System.out.println(((огранак_вриједност)низ_вриједност[0]).вриједност()); System.out.println((String)низ_вриједност[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] бајт_вриједност = new byte[1]; бајт_вриједност[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(бајт_вриједност[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
