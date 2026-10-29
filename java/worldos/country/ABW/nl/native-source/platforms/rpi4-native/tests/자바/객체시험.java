// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int WAARDE(); }
class Achtergrond_WAARDE { static int Bereid_voor = 7; int nummer; String Naam; Achtergrond_WAARDE(int nummer) { this.nummer = nummer; Naam = "Achtergrond_WAARDE"; } int WAARDE() { return nummer; } }
class branch_WAARDE extends Achtergrond_WAARDE implements 계산가능 { branch_WAARDE(int nummer) { super(nummer); Naam = "branch_WAARDE"; } public int WAARDE() { return nummer * Bereid_voor; } }
public class 객체시험 {
    static int begintoestand = Achtergrond_WAARDE.Bereid_voor + 2;
    static int branch(int nummer) { switch (nummer) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int nummer) { switch (nummer) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] argumenten) {
        branch_WAARDE SECONDE_operand = new branch_WAARDE(6); Achtergrond_WAARDE 다 = SECONDE_operand; 계산가능 라 = SECONDE_operand;
        System.out.println(begintoestand + ":" + SECONDE_operand.Naam + ":" + 다.WAARDE() + ":" + 라.WAARDE());
        System.out.println((다 instanceof branch_WAARDE) + ":" + (다 instanceof 계산가능) + ":" + branch(2) + ":" + 띄엄(100));
        Object[] MATRIX_WAARDE = new Object[3]; MATRIX_WAARDE[0] = SECONDE_operand; MATRIX_WAARDE[1] = "한글😀"; System.gc();
        System.out.println(((branch_WAARDE)MATRIX_WAARDE[0]).WAARDE()); System.out.println((String)MATRIX_WAARDE[1]);
        int[] AANTAL_Lijst = {1, 2, 3, 4}; System.arraycopy(AANTAL_Lijst, 0, AANTAL_Lijst, 1, 3); System.out.println(AANTAL_Lijst[3]);
        byte[] byte_WAARDE = new byte[1]; byte_WAARDE[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] booleaans_WAARDE = {true};
        System.out.println(byte_WAARDE[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + booleaans_WAARDE[0]);
    }
}
