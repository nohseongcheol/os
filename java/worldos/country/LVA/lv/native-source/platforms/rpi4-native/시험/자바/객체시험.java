// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int VALUE(); }
class Fons_VALUE { static int Sagatavot = 7; int numurs; String Nosaukums; Fons_VALUE(int numurs) { this.numurs = numurs; Nosaukums = "Fons_VALUE"; } int VALUE() { return numurs; } }
class zars_VALUE extends Fons_VALUE implements 계산가능 { zars_VALUE(int numurs) { super(numurs); Nosaukums = "zars_VALUE"; } public int VALUE() { return numurs * Sagatavot; } }
public class 객체시험 {
    static int sākumstāvoklis = Fons_VALUE.Sagatavot + 2;
    static int zars(int numurs) { switch (numurs) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int numurs) { switch (numurs) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] Parametri) {
        zars_VALUE SECOND_operands = new zars_VALUE(6); Fons_VALUE 다 = SECOND_operands; 계산가능 라 = SECOND_operands;
        System.out.println(sākumstāvoklis + ":" + SECOND_operands.Nosaukums + ":" + 다.VALUE() + ":" + 라.VALUE());
        System.out.println((다 instanceof zars_VALUE) + ":" + (다 instanceof 계산가능) + ":" + zars(2) + ":" + 띄엄(100));
        Object[] ARRAY_VALUE = new Object[3]; ARRAY_VALUE[0] = SECOND_operands; ARRAY_VALUE[1] = "한글😀"; System.gc();
        System.out.println(((zars_VALUE)ARRAY_VALUE[0]).VALUE()); System.out.println((String)ARRAY_VALUE[1]);
        int[] COUNT_Saraksts = {1, 2, 3, 4}; System.arraycopy(COUNT_Saraksts, 0, COUNT_Saraksts, 1, 3); System.out.println(COUNT_Saraksts[3]);
        byte[] byte_VALUE = new byte[1]; byte_VALUE[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] Būla_VALUE = {true};
        System.out.println(byte_VALUE[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + Būla_VALUE[0]);
    }
}
