// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int VALUE(); }
class poster_VALUE { static int Pripremiti = 7; int 수; String Naziv; poster_VALUE(int 수) { this.수 = 수; Naziv = "poster_VALUE"; } int VALUE() { return 수; } }
class ogranak_VALUE extends poster_VALUE implements 계산가능 { ogranak_VALUE(int 수) { super(수); Naziv = "ogranak_VALUE"; } public int VALUE() { return 수 * Pripremiti; } }
public class 객체시험 {
    static int 초기 = poster_VALUE.Pripremiti + 2;
    static int ogranak(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] Argumenti) {
        ogranak_VALUE SECOND_operand = new ogranak_VALUE(6); poster_VALUE 다 = SECOND_operand; 계산가능 라 = SECOND_operand;
        System.out.println(초기 + ":" + SECOND_operand.Naziv + ":" + 다.VALUE() + ":" + 라.VALUE());
        System.out.println((다 instanceof ogranak_VALUE) + ":" + (다 instanceof 계산가능) + ":" + ogranak(2) + ":" + 띄엄(100));
        Object[] niz_VALUE = new Object[3]; niz_VALUE[0] = SECOND_operand; niz_VALUE[1] = "한글😀"; System.gc();
        System.out.println(((ogranak_VALUE)niz_VALUE[0]).VALUE()); System.out.println((String)niz_VALUE[1]);
        int[] COUNT_spisak = {1, 2, 3, 4}; System.arraycopy(COUNT_spisak, 0, COUNT_spisak, 1, 3); System.out.println(COUNT_spisak[3]);
        byte[] bajt_VALUE = new byte[1]; bajt_VALUE[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(bajt_VALUE[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
