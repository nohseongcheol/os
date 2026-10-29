// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int baha(); }
class Fon_baha { static int Taýýarla = 7; int 수; String Ad; Fon_baha(int 수) { this.수 = 수; Ad = "Fon_baha"; } int baha() { return 수; } }
class şahalanma_baha extends Fon_baha implements 계산가능 { şahalanma_baha(int 수) { super(수); Ad = "şahalanma_baha"; } public int baha() { return 수 * Taýýarla; } }
public class 객체시험 {
    static int 초기 = Fon_baha.Taýýarla + 2;
    static int şahalanma(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] 인수) {
        şahalanma_baha 나 = new şahalanma_baha(6); Fon_baha 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.Ad + ":" + 다.baha() + ":" + 라.baha());
        System.out.println((다 instanceof şahalanma_baha) + ":" + (다 instanceof 계산가능) + ":" + şahalanma(2) + ":" + 띄엄(100));
        Object[] ARRAY_baha = new Object[3]; ARRAY_baha[0] = 나; ARRAY_baha[1] = "한글😀"; System.gc();
        System.out.println(((şahalanma_baha)ARRAY_baha[0]).baha()); System.out.println((String)ARRAY_baha[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] baýt_baha = new byte[1]; baýt_baha[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(baýt_baha[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
