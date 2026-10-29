// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int WARTOŚĆ(); }
class Tło_WARTOŚĆ { static int Przygotuj = 7; int identyfikator; String Nazwa; Tło_WARTOŚĆ(int identyfikator) { this.identyfikator = identyfikator; Nazwa = "Tło_WARTOŚĆ"; } int WARTOŚĆ() { return identyfikator; } }
class gałąź_WARTOŚĆ extends Tło_WARTOŚĆ implements 계산가능 { gałąź_WARTOŚĆ(int identyfikator) { super(identyfikator); Nazwa = "gałąź_WARTOŚĆ"; } public int WARTOŚĆ() { return identyfikator * Przygotuj; } }
public class 객체시험 {
    static int stan_początkowy = Tło_WARTOŚĆ.Przygotuj + 2;
    static int gałąź_22e01337(int identyfikator) { switch (identyfikator) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int identyfikator) { switch (identyfikator) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] argumenty) {
        gałąź_WARTOŚĆ SEKUNDA_operand = new gałąź_WARTOŚĆ(6); Tło_WARTOŚĆ 다 = SEKUNDA_operand; 계산가능 라 = SEKUNDA_operand;
        System.out.println(stan_początkowy + ":" + SEKUNDA_operand.Nazwa + ":" + 다.WARTOŚĆ() + ":" + 라.WARTOŚĆ());
        System.out.println((다 instanceof gałąź_WARTOŚĆ) + ":" + (다 instanceof 계산가능) + ":" + gałąź_22e01337(2) + ":" + 띄엄(100));
        Object[] TABLICA_WARTOŚĆ = new Object[3]; TABLICA_WARTOŚĆ[0] = SEKUNDA_operand; TABLICA_WARTOŚĆ[1] = "한글😀"; System.gc();
        System.out.println(((gałąź_WARTOŚĆ)TABLICA_WARTOŚĆ[0]).WARTOŚĆ()); System.out.println((String)TABLICA_WARTOŚĆ[1]);
        int[] ILE_LICZB_Lista = {1, 2, 3, 4}; System.arraycopy(ILE_LICZB_Lista, 0, ILE_LICZB_Lista, 1, 3); System.out.println(ILE_LICZB_Lista[3]);
        byte[] bajt_WARTOŚĆ = new byte[1]; bajt_WARTOŚĆ[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] logiczny_WARTOŚĆ = {true};
        System.out.println(bajt_WARTOŚĆ[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + logiczny_WARTOŚĆ[0]);
    }
}
