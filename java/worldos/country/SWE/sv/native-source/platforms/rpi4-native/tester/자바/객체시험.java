// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int värde(); }
class Bakgrund_värde { static int Förbereda = 7; int nummer; String Namn; Bakgrund_värde(int nummer) { this.nummer = nummer; Namn = "Bakgrund_värde"; } int värde() { return nummer; } }
class gren_värde extends Bakgrund_värde implements 계산가능 { gren_värde(int nummer) { super(nummer); Namn = "gren_värde"; } public int värde() { return nummer * Förbereda; } }
public class 객체시험 {
    static int starttillstånd = Bakgrund_värde.Förbereda + 2;
    static int gren(int nummer) { switch (nummer) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int nummer) { switch (nummer) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] argument) {
        gren_värde SEKUND_operand = new gren_värde(6); Bakgrund_värde 다 = SEKUND_operand; 계산가능 라 = SEKUND_operand;
        System.out.println(starttillstånd + ":" + SEKUND_operand.Namn + ":" + 다.värde() + ":" + 라.värde());
        System.out.println((다 instanceof gren_värde) + ":" + (다 instanceof 계산가능) + ":" + gren(2) + ":" + 띄엄(100));
        Object[] MATRIS_värde = new Object[3]; MATRIS_värde[0] = SEKUND_operand; MATRIS_värde[1] = "한글😀"; System.gc();
        System.out.println(((gren_värde)MATRIS_värde[0]).värde()); System.out.println((String)MATRIS_värde[1]);
        int[] ANTAL_ange = {1, 2, 3, 4}; System.arraycopy(ANTAL_ange, 0, ANTAL_ange, 1, 3); System.out.println(ANTAL_ange[3]);
        byte[] byte_värde = new byte[1]; byte_värde[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] boolesk_värde = {true};
        System.out.println(byte_värde[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + boolesk_värde[0]);
    }
}
