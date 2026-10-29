// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int VALUE(); }
class Fon_VALUE { static int Tayyorlamoq = 7; int 수; String Nomi; Fon_VALUE(int 수) { this.수 = 수; Nomi = "Fon_VALUE"; } int VALUE() { return 수; } }
class shox_VALUE extends Fon_VALUE implements 계산가능 { shox_VALUE(int 수) { super(수); Nomi = "shox_VALUE"; } public int VALUE() { return 수 * Tayyorlamoq; } }
public class 객체시험 {
    static int 초기 = Fon_VALUE.Tayyorlamoq + 2;
    static int shox(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] 인수) {
        shox_VALUE 나 = new shox_VALUE(6); Fon_VALUE 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.Nomi + ":" + 다.VALUE() + ":" + 라.VALUE());
        System.out.println((다 instanceof shox_VALUE) + ":" + (다 instanceof 계산가능) + ":" + shox(2) + ":" + 띄엄(100));
        Object[] ARRAY_VALUE = new Object[3]; ARRAY_VALUE[0] = 나; ARRAY_VALUE[1] = "한글😀"; System.gc();
        System.out.println(((shox_VALUE)ARRAY_VALUE[0]).VALUE()); System.out.println((String)ARRAY_VALUE[1]);
        int[] COUNT_Ro_yxat = {1, 2, 3, 4}; System.arraycopy(COUNT_Ro_yxat, 0, COUNT_Ro_yxat, 1, 3); System.out.println(COUNT_Ro_yxat[3]);
        byte[] bayt_VALUE = new byte[1]; bayt_VALUE[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(bayt_VALUE[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
