// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int VALUE(); }
class Cúlra_VALUE { static int Ullmhaigh = 7; int 수; String Ainm; Cúlra_VALUE(int 수) { this.수 = 수; Ainm = "Cúlra_VALUE"; } int VALUE() { return 수; } }
class craobh_VALUE extends Cúlra_VALUE implements 계산가능 { craobh_VALUE(int 수) { super(수); Ainm = "craobh_VALUE"; } public int VALUE() { return 수 * Ullmhaigh; } }
public class 객체시험 {
    static int 초기 = Cúlra_VALUE.Ullmhaigh + 2;
    static int craobh(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] Argóintí) {
        craobh_VALUE 나 = new craobh_VALUE(6); Cúlra_VALUE 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.Ainm + ":" + 다.VALUE() + ":" + 라.VALUE());
        System.out.println((다 instanceof craobh_VALUE) + ":" + (다 instanceof 계산가능) + ":" + craobh(2) + ":" + 띄엄(100));
        Object[] ARRAY_VALUE = new Object[3]; ARRAY_VALUE[0] = 나; ARRAY_VALUE[1] = "한글😀"; System.gc();
        System.out.println(((craobh_VALUE)ARRAY_VALUE[0]).VALUE()); System.out.println((String)ARRAY_VALUE[1]);
        int[] COUNT_Liosta = {1, 2, 3, 4}; System.arraycopy(COUNT_Liosta, 0, COUNT_Liosta, 1, 3); System.out.println(COUNT_Liosta[3]);
        byte[] beart_VALUE = new byte[1]; beart_VALUE[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(beart_VALUE[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
