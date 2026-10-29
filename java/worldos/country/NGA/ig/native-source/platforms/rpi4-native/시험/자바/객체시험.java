// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int valuu(); }
class Bakgraụnd_valuu { static int Kwado = 7; int 수; String Aha; Bakgraụnd_valuu(int 수) { this.수 = 수; Aha = "Bakgraụnd_valuu"; } int valuu() { return 수; } }
class ogbè_valuu extends Bakgraụnd_valuu implements 계산가능 { ogbè_valuu(int 수) { super(수); Aha = "ogbè_valuu"; } public int valuu() { return 수 * Kwado; } }
public class 객체시험 {
    static int 초기 = Bakgraụnd_valuu.Kwado + 2;
    static int ogbè(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] 인수) {
        ogbè_valuu 나 = new ogbè_valuu(6); Bakgraụnd_valuu 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.Aha + ":" + 다.valuu() + ":" + 라.valuu());
        System.out.println((다 instanceof ogbè_valuu) + ":" + (다 instanceof 계산가능) + ":" + ogbè(2) + ":" + 띄엄(100));
        Object[] MKPOKỌTA_valuu = new Object[3]; MKPOKỌTA_valuu[0] = 나; MKPOKỌTA_valuu[1] = "한글😀"; System.gc();
        System.out.println(((ogbè_valuu)MKPOKỌTA_valuu[0]).valuu()); System.out.println((String)MKPOKỌTA_valuu[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] baịtị_valuu = new byte[1]; baịtị_valuu[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(baịtị_valuu[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
