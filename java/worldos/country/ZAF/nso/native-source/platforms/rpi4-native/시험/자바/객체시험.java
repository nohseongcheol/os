// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int boleng(); }
class Bokamorago_boleng { static int Lokišetša = 7; int 수; String Leina; Bokamorago_boleng(int 수) { this.수 = 수; Leina = "Bokamorago_boleng"; } int boleng() { return 수; } }
class lekala_boleng extends Bokamorago_boleng implements 계산가능 { lekala_boleng(int 수) { super(수); Leina = "lekala_boleng"; } public int boleng() { return 수 * Lokišetša; } }
public class 객체시험 {
    static int 초기 = Bokamorago_boleng.Lokišetša + 2;
    static int lekala(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] 인수) {
        lekala_boleng 나 = new lekala_boleng(6); Bokamorago_boleng 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.Leina + ":" + 다.boleng() + ":" + 라.boleng());
        System.out.println((다 instanceof lekala_boleng) + ":" + (다 instanceof 계산가능) + ":" + lekala(2) + ":" + 띄엄(100));
        Object[] arei_boleng = new Object[3]; arei_boleng[0] = 나; arei_boleng[1] = "한글😀"; System.gc();
        System.out.println(((lekala_boleng)arei_boleng[0]).boleng()); System.out.println((String)arei_boleng[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] paete_boleng = new byte[1]; paete_boleng[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(paete_boleng[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
