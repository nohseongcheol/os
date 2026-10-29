// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int мән(); }
class Фон_мән { static int Дайындау = 7; int 수; String Аты; Фон_мән(int 수) { this.수 = 수; Аты = "Фон_мән"; } int мән() { return 수; } }
class тармақ_мән extends Фон_мән implements 계산가능 { тармақ_мән(int 수) { super(수); Аты = "тармақ_мән"; } public int мән() { return 수 * Дайындау; } }
public class 객체시험 {
    static int бастапқы_күй = Фон_мән.Дайындау + 2;
    static int тармақ(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] Аргументтер) {
        тармақ_мән 나 = new тармақ_мән(6); Фон_мән 다 = 나; 계산가능 라 = 나;
        System.out.println(бастапқы_күй + ":" + 나.Аты + ":" + 다.мән() + ":" + 라.мән());
        System.out.println((다 instanceof тармақ_мән) + ":" + (다 instanceof 계산가능) + ":" + тармақ(2) + ":" + 띄엄(100));
        Object[] массив_мән = new Object[3]; массив_мән[0] = 나; массив_мән[1] = "한글😀"; System.gc();
        System.out.println(((тармақ_мән)массив_мән[0]).мән()); System.out.println((String)массив_мән[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] байт_мән = new byte[1]; байт_мән[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] Логикалық_мән = {true};
        System.out.println(байт_мән[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + Логикалық_мән[0]);
    }
}
