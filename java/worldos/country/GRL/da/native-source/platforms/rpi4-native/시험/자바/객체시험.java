// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int VÆRDI(); }
class Baggrund_VÆRDI { static int Tilrettelæg = 7; int tal; String Navn; Baggrund_VÆRDI(int tal) { this.tal = tal; Navn = "Baggrund_VÆRDI"; } int VÆRDI() { return tal; } }
class gren_VÆRDI extends Baggrund_VÆRDI implements 계산가능 { gren_VÆRDI(int tal) { super(tal); Navn = "gren_VÆRDI"; } public int VÆRDI() { return tal * Tilrettelæg; } }
public class 객체시험 {
    static int starttilstand = Baggrund_VÆRDI.Tilrettelæg + 2;
    static int gren(int tal) { switch (tal) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int tal) { switch (tal) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] Argumenter) {
        gren_VÆRDI SEKUND_operand = new gren_VÆRDI(6); Baggrund_VÆRDI 다 = SEKUND_operand; 계산가능 라 = SEKUND_operand;
        System.out.println(starttilstand + ":" + SEKUND_operand.Navn + ":" + 다.VÆRDI() + ":" + 라.VÆRDI());
        System.out.println((다 instanceof gren_VÆRDI) + ":" + (다 instanceof 계산가능) + ":" + gren(2) + ":" + 띄엄(100));
        Object[] MATRIX_VÆRDI = new Object[3]; MATRIX_VÆRDI[0] = SEKUND_operand; MATRIX_VÆRDI[1] = "한글😀"; System.gc();
        System.out.println(((gren_VÆRDI)MATRIX_VÆRDI[0]).VÆRDI()); System.out.println((String)MATRIX_VÆRDI[1]);
        int[] TÆL_Liste = {1, 2, 3, 4}; System.arraycopy(TÆL_Liste, 0, TÆL_Liste, 1, 3); System.out.println(TÆL_Liste[3]);
        byte[] byte_VÆRDI = new byte[1]; byte_VÆRDI[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] boolesk_VÆRDI = {true};
        System.out.println(byte_VÆRDI[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + boolesk_VÆRDI[0]);
    }
}
