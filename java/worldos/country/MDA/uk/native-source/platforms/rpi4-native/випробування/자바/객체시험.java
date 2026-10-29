// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int значення(); }
class Фон_значення { static int Готувати = 7; int 수; String Назва; Фон_значення(int 수) { this.수 = 수; Назва = "Фон_значення"; } int значення() { return 수; } }
class гілка_значення extends Фон_значення implements 계산가능 { гілка_значення(int 수) { super(수); Назва = "гілка_значення"; } public int значення() { return 수 * Готувати; } }
public class 객체시험 {
    static int початковий_стан = Фон_значення.Готувати + 2;
    static int гілка(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] аргументи) {
        гілка_значення 나 = new гілка_значення(6); Фон_значення 다 = 나; 계산가능 라 = 나;
        System.out.println(початковий_стан + ":" + 나.Назва + ":" + 다.значення() + ":" + 라.значення());
        System.out.println((다 instanceof гілка_значення) + ":" + (다 instanceof 계산가능) + ":" + гілка(2) + ":" + 띄엄(100));
        Object[] масив_значення = new Object[3]; масив_значення[0] = 나; масив_значення[1] = "한글😀"; System.gc();
        System.out.println(((гілка_значення)масив_значення[0]).значення()); System.out.println((String)масив_значення[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] байт_значення = new byte[1]; байт_значення[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] логічний_значення = {true};
        System.out.println(байт_значення[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + логічний_значення[0]);
    }
}
