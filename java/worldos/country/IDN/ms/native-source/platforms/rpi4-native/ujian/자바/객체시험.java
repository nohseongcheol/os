// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int VALUE(); }
class latar_VALUE { static int Sediakan = 7; int 수; String Nama; latar_VALUE(int 수) { this.수 = 수; Nama = "latar_VALUE"; } int VALUE() { return 수; } }
class cabang_VALUE extends latar_VALUE implements 계산가능 { cabang_VALUE(int 수) { super(수); Nama = "cabang_VALUE"; } public int VALUE() { return 수 * Sediakan; } }
public class 객체시험 {
    static int 초기 = latar_VALUE.Sediakan + 2;
    static int cabang(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] 인수) {
        cabang_VALUE 나 = new cabang_VALUE(6); latar_VALUE 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.Nama + ":" + 다.VALUE() + ":" + 라.VALUE());
        System.out.println((다 instanceof cabang_VALUE) + ":" + (다 instanceof 계산가능) + ":" + cabang(2) + ":" + 띄엄(100));
        Object[] ARRAY_VALUE = new Object[3]; ARRAY_VALUE[0] = 나; ARRAY_VALUE[1] = "한글😀"; System.gc();
        System.out.println(((cabang_VALUE)ARRAY_VALUE[0]).VALUE()); System.out.println((String)ARRAY_VALUE[1]);
        int[] COUNT_Senarai = {1, 2, 3, 4}; System.arraycopy(COUNT_Senarai, 0, COUNT_Senarai, 1, 3); System.out.println(COUNT_Senarai[3]);
        byte[] bait_VALUE = new byte[1]; bait_VALUE[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] Boolean_VALUE = {true};
        System.out.println(bait_VALUE[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + Boolean_VALUE[0]);
    }
}
