// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int VALUE(); }
class Фон_VALUE { static int Әзерләү = 7; int 수; String исем; Фон_VALUE(int 수) { this.수 = 수; исем = "Фон_VALUE"; } int VALUE() { return 수; } }
class тармак_VALUE extends Фон_VALUE implements 계산가능 { тармак_VALUE(int 수) { super(수); исем = "тармак_VALUE"; } public int VALUE() { return 수 * Әзерләү; } }
public class 객체시험 {
    static int 초기 = Фон_VALUE.Әзерләү + 2;
    static int тармак(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] 인수) {
        тармак_VALUE 나 = new тармак_VALUE(6); Фон_VALUE 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.исем + ":" + 다.VALUE() + ":" + 라.VALUE());
        System.out.println((다 instanceof тармак_VALUE) + ":" + (다 instanceof 계산가능) + ":" + тармак(2) + ":" + 띄엄(100));
        Object[] МАССИВ_VALUE = new Object[3]; МАССИВ_VALUE[0] = 나; МАССИВ_VALUE[1] = "한글😀"; System.gc();
        System.out.println(((тармак_VALUE)МАССИВ_VALUE[0]).VALUE()); System.out.println((String)МАССИВ_VALUE[1]);
        int[] COUNT_Исемлек = {1, 2, 3, 4}; System.arraycopy(COUNT_Исемлек, 0, COUNT_Исемлек, 1, 3); System.out.println(COUNT_Исемлек[3]);
        byte[] байт_VALUE = new byte[1]; байт_VALUE[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(байт_VALUE[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
