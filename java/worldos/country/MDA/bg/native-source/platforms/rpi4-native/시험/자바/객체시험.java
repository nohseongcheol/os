// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int стойност(); }
class Фон_стойност { static int Подготвяне = 7; int 수; String Име; Фон_стойност(int 수) { this.수 = 수; Име = "Фон_стойност"; } int стойност() { return 수; } }
class клон_стойност extends Фон_стойност implements 계산가능 { клон_стойност(int 수) { super(수); Име = "клон_стойност"; } public int стойност() { return 수 * Подготвяне; } }
public class 객체시험 {
    static int първоначално_състояние = Фон_стойност.Подготвяне + 2;
    static int клон(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] Параметри) {
        клон_стойност 나 = new клон_стойност(6); Фон_стойност 다 = 나; 계산가능 라 = 나;
        System.out.println(първоначално_състояние + ":" + 나.Име + ":" + 다.стойност() + ":" + 라.стойност());
        System.out.println((다 instanceof клон_стойност) + ":" + (다 instanceof 계산가능) + ":" + клон(2) + ":" + 띄엄(100));
        Object[] масив_стойност = new Object[3]; масив_стойност[0] = 나; масив_стойност[1] = "한글😀"; System.gc();
        System.out.println(((клон_стойност)масив_стойност[0]).стойност()); System.out.println((String)масив_стойност[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] байт_стойност = new byte[1]; байт_стойност[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] булев_стойност = {true};
        System.out.println(байт_стойност[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + булев_стойност[0]);
    }
}
