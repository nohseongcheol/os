// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int xëyma(); }
class Njiitlay_xëyma { static int jël_matuwaay = 7; int 수; String tur_253d1510; Njiitlay_xëyma(int 수) { this.수 = 수; tur_253d1510 = "Njiitlay_xëyma"; } int xëyma() { return 수; } }
class car_xëyma extends Njiitlay_xëyma implements 계산가능 { car_xëyma(int 수) { super(수); tur_253d1510 = "car_xëyma"; } public int xëyma() { return 수 * jël_matuwaay; } }
public class 객체시험 {
    static int 초기 = Njiitlay_xëyma.jël_matuwaay + 2;
    static int car(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] 인수) {
        car_xëyma 나 = new car_xëyma(6); Njiitlay_xëyma 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.tur_253d1510 + ":" + 다.xëyma() + ":" + 라.xëyma());
        System.out.println((다 instanceof car_xëyma) + ":" + (다 instanceof 계산가능) + ":" + car(2) + ":" + 띄엄(100));
        Object[] TABLO_xëyma = new Object[3]; TABLO_xëyma[0] = 나; TABLO_xëyma[1] = "한글😀"; System.gc();
        System.out.println(((car_xëyma)TABLO_xëyma[0]).xëyma()); System.out.println((String)TABLO_xëyma[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] okte_xëyma = new byte[1]; okte_xëyma[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(okte_xëyma[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
