// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int Boleng(); }
class Lemorago_Boleng { static int Baakanya = 7; int 수; String leina; Lemorago_Boleng(int 수) { this.수 = 수; leina = "Lemorago_Boleng"; } int Boleng() { return 수; } }
class lekala_Boleng extends Lemorago_Boleng implements 계산가능 { lekala_Boleng(int 수) { super(수); leina = "lekala_Boleng"; } public int Boleng() { return 수 * Baakanya; } }
public class 객체시험 {
    static int 초기 = Lemorago_Boleng.Baakanya + 2;
    static int lekala(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] 인수) {
        lekala_Boleng 나 = new lekala_Boleng(6); Lemorago_Boleng 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.leina + ":" + 다.Boleng() + ":" + 라.Boleng());
        System.out.println((다 instanceof lekala_Boleng) + ":" + (다 instanceof 계산가능) + ":" + lekala(2) + ":" + 띄엄(100));
        Object[] setlhopha_Boleng_ed437109 = new Object[3]; setlhopha_Boleng_ed437109[0] = 나; setlhopha_Boleng_ed437109[1] = "한글😀"; System.gc();
        System.out.println(((lekala_Boleng)setlhopha_Boleng_ed437109[0]).Boleng()); System.out.println((String)setlhopha_Boleng_ed437109[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] baete_Boleng = new byte[1]; baete_Boleng[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(baete_Boleng[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
