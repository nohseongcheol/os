// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int VALUE(); }
class тапет_VALUE { static int Подготви = 7; int 수; String Име; тапет_VALUE(int 수) { this.수 = 수; Име = "тапет_VALUE"; } int VALUE() { return 수; } }
class гранка_VALUE extends тапет_VALUE implements 계산가능 { гранка_VALUE(int 수) { super(수); Име = "гранка_VALUE"; } public int VALUE() { return 수 * Подготви; } }
public class 객체시험 {
    static int 초기 = тапет_VALUE.Подготви + 2;
    static int гранка(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] Аргументи) {
        гранка_VALUE 나 = new гранка_VALUE(6); тапет_VALUE 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.Име + ":" + 다.VALUE() + ":" + 라.VALUE());
        System.out.println((다 instanceof гранка_VALUE) + ":" + (다 instanceof 계산가능) + ":" + гранка(2) + ":" + 띄엄(100));
        Object[] низа_VALUE = new Object[3]; низа_VALUE[0] = 나; низа_VALUE[1] = "한글😀"; System.gc();
        System.out.println(((гранка_VALUE)низа_VALUE[0]).VALUE()); System.out.println((String)низа_VALUE[1]);
        int[] COUNT_Список = {1, 2, 3, 4}; System.arraycopy(COUNT_Список, 0, COUNT_Список, 1, 3); System.out.println(COUNT_Список[3]);
        byte[] бајт_VALUE = new byte[1]; бајт_VALUE[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(бајт_VALUE[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
