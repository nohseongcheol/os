// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int balio(); }
class horma_paper_balio { static int 준비 = 7; int 수; String Izena; horma_paper_balio(int 수) { this.수 = 수; Izena = "horma_paper_balio"; } int balio() { return 수; } }
class adar_balio extends horma_paper_balio implements 계산가능 { adar_balio(int 수) { super(수); Izena = "adar_balio"; } public int balio() { return 수 * 준비; } }
public class 객체시험 {
    static int 초기 = horma_paper_balio.준비 + 2;
    static int adar(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] Argumentuak) {
        adar_balio 나 = new adar_balio(6); horma_paper_balio 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.Izena + ":" + 다.balio() + ":" + 라.balio());
        System.out.println((다 instanceof adar_balio) + ":" + (다 instanceof 계산가능) + ":" + adar(2) + ":" + 띄엄(100));
        Object[] matrize_balio = new Object[3]; matrize_balio[0] = 나; matrize_balio[1] = "한글😀"; System.gc();
        System.out.println(((adar_balio)matrize_balio[0]).balio()); System.out.println((String)matrize_balio[1]);
        int[] ZENBATU_Zerrenda = {1, 2, 3, 4}; System.arraycopy(ZENBATU_Zerrenda, 0, ZENBATU_Zerrenda, 1, 3); System.out.println(ZENBATU_Zerrenda[3]);
        byte[] byte_balio = new byte[1]; byte_balio[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] Boolear_balio = {true};
        System.out.println(byte_balio[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + Boolear_balio[0]);
    }
}
