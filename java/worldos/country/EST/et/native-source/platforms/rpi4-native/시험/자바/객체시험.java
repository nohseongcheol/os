// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int VALUE(); }
class taust_VALUE { static int Ettevalmistamine = 7; int number; String Nimi_2; taust_VALUE(int number) { this.number = number; Nimi_2 = "taust_VALUE"; } int VALUE() { return number; } }
class haru_VALUE extends taust_VALUE implements 계산가능 { haru_VALUE(int number) { super(number); Nimi_2 = "haru_VALUE"; } public int VALUE() { return number * Ettevalmistamine; } }
public class 객체시험 {
    static int lähteolek = taust_VALUE.Ettevalmistamine + 2;
    static int haru(int number) { switch (number) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int number) { switch (number) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] Argumendid) {
        haru_VALUE SECOND_operand = new haru_VALUE(6); taust_VALUE 다 = SECOND_operand; 계산가능 라 = SECOND_operand;
        System.out.println(lähteolek + ":" + SECOND_operand.Nimi_2 + ":" + 다.VALUE() + ":" + 라.VALUE());
        System.out.println((다 instanceof haru_VALUE) + ":" + (다 instanceof 계산가능) + ":" + haru(2) + ":" + 띄엄(100));
        Object[] ARRAY_VALUE = new Object[3]; ARRAY_VALUE[0] = SECOND_operand; ARRAY_VALUE[1] = "한글😀"; System.gc();
        System.out.println(((haru_VALUE)ARRAY_VALUE[0]).VALUE()); System.out.println((String)ARRAY_VALUE[1]);
        int[] COUNT_Loend = {1, 2, 3, 4}; System.arraycopy(COUNT_Loend, 0, COUNT_Loend, 1, 3); System.out.println(COUNT_Loend[3]);
        byte[] bait_VALUE = new byte[1]; bait_VALUE[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] loogiline_VALUE = {true};
        System.out.println(bait_VALUE[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + loogiline_VALUE[0]);
    }
}
