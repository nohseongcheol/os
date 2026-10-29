// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int VERDI(); }
class bakgrunn_VERDI { static int Forbered = 7; int nummer; String Navn; bakgrunn_VERDI(int nummer) { this.nummer = nummer; Navn = "bakgrunn_VERDI"; } int VERDI() { return nummer; } }
class gren_VERDI extends bakgrunn_VERDI implements 계산가능 { gren_VERDI(int nummer) { super(nummer); Navn = "gren_VERDI"; } public int VERDI() { return nummer * Forbered; } }
public class 객체시험 {
    static int opprinnelig_tilstand = bakgrunn_VERDI.Forbered + 2;
    static int gren(int nummer) { switch (nummer) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int nummer) { switch (nummer) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] Argumenter) {
        gren_VERDI SEKUND_operand = new gren_VERDI(6); bakgrunn_VERDI 다 = SEKUND_operand; 계산가능 라 = SEKUND_operand;
        System.out.println(opprinnelig_tilstand + ":" + SEKUND_operand.Navn + ":" + 다.VERDI() + ":" + 라.VERDI());
        System.out.println((다 instanceof gren_VERDI) + ":" + (다 instanceof 계산가능) + ":" + gren(2) + ":" + 띄엄(100));
        Object[] MATRISE_VERDI = new Object[3]; MATRISE_VERDI[0] = SEKUND_operand; MATRISE_VERDI[1] = "한글😀"; System.gc();
        System.out.println(((gren_VERDI)MATRISE_VERDI[0]).VERDI()); System.out.println((String)MATRISE_VERDI[1]);
        int[] ANTALL_Liste = {1, 2, 3, 4}; System.arraycopy(ANTALL_Liste, 0, ANTALL_Liste, 1, 3); System.out.println(ANTALL_Liste[3]);
        byte[] byte_VERDI = new byte[1]; byte_VERDI[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] boolsk_VERDI = {true};
        System.out.println(byte_VERDI[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + boolsk_VERDI[0]);
    }
}
