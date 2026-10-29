// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int VALUE(); }
class Cefndir_VALUE { static int Paratoi = 7; int 수; String Enw; Cefndir_VALUE(int 수) { this.수 = 수; Enw = "Cefndir_VALUE"; } int VALUE() { return 수; } }
class cangen_VALUE extends Cefndir_VALUE implements 계산가능 { cangen_VALUE(int 수) { super(수); Enw = "cangen_VALUE"; } public int VALUE() { return 수 * Paratoi; } }
public class 객체시험 {
    static int 초기 = Cefndir_VALUE.Paratoi + 2;
    static int cangen(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] 인수) {
        cangen_VALUE 나 = new cangen_VALUE(6); Cefndir_VALUE 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.Enw + ":" + 다.VALUE() + ":" + 라.VALUE());
        System.out.println((다 instanceof cangen_VALUE) + ":" + (다 instanceof 계산가능) + ":" + cangen(2) + ":" + 띄엄(100));
        Object[] ARAE_VALUE = new Object[3]; ARAE_VALUE[0] = 나; ARAE_VALUE[1] = "한글😀"; System.gc();
        System.out.println(((cangen_VALUE)ARAE_VALUE[0]).VALUE()); System.out.println((String)ARAE_VALUE[1]);
        int[] COUNT_Rhestr = {1, 2, 3, 4}; System.arraycopy(COUNT_Rhestr, 0, COUNT_Rhestr, 1, 3); System.out.println(COUNT_Rhestr[3]);
        byte[] beit_VALUE = new byte[1]; beit_VALUE[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(beit_VALUE[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
