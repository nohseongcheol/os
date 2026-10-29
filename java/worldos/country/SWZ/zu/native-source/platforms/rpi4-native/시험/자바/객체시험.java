// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int inani(); }
class ngemuva_inani { static int Hlela = 7; int 수; String Igama; ngemuva_inani(int 수) { this.수 = 수; Igama = "ngemuva_inani"; } int inani() { return 수; } }
class igatsha_inani extends ngemuva_inani implements 계산가능 { igatsha_inani(int 수) { super(수); Igama = "igatsha_inani"; } public int inani() { return 수 * Hlela; } }
public class 객체시험 {
    static int 초기 = ngemuva_inani.Hlela + 2;
    static int igatsha(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] 인수) {
        igatsha_inani 나 = new igatsha_inani(6); ngemuva_inani 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.Igama + ":" + 다.inani() + ":" + 라.inani());
        System.out.println((다 instanceof igatsha_inani) + ":" + (다 instanceof 계산가능) + ":" + igatsha(2) + ":" + 띄엄(100));
        Object[] AMALUNGU_AFANAYO_inani = new Object[3]; AMALUNGU_AFANAYO_inani[0] = 나; AMALUNGU_AFANAYO_inani[1] = "한글😀"; System.gc();
        System.out.println(((igatsha_inani)AMALUNGU_AFANAYO_inani[0]).inani()); System.out.println((String)AMALUNGU_AFANAYO_inani[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] ibhayithi_inani = new byte[1]; ibhayithi_inani[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(ibhayithi_inani[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
