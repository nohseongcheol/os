// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int VALUE(); }
class Fonas_VALUE { static int Parengti = 7; int numeris; String Pavadinimas_2; Fonas_VALUE(int numeris) { this.numeris = numeris; Pavadinimas_2 = "Fonas_VALUE"; } int VALUE() { return numeris; } }
class šaka_VALUE extends Fonas_VALUE implements 계산가능 { šaka_VALUE(int numeris) { super(numeris); Pavadinimas_2 = "šaka_VALUE"; } public int VALUE() { return numeris * Parengti; } }
public class 객체시험 {
    static int pradinė_būsena = Fonas_VALUE.Parengti + 2;
    static int šaka(int numeris) { switch (numeris) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int numeris) { switch (numeris) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] Argumentai) {
        šaka_VALUE SECOND_operandas = new šaka_VALUE(6); Fonas_VALUE 다 = SECOND_operandas; 계산가능 라 = SECOND_operandas;
        System.out.println(pradinė_būsena + ":" + SECOND_operandas.Pavadinimas_2 + ":" + 다.VALUE() + ":" + 라.VALUE());
        System.out.println((다 instanceof šaka_VALUE) + ":" + (다 instanceof 계산가능) + ":" + šaka(2) + ":" + 띄엄(100));
        Object[] ARRAY_VALUE = new Object[3]; ARRAY_VALUE[0] = SECOND_operandas; ARRAY_VALUE[1] = "한글😀"; System.gc();
        System.out.println(((šaka_VALUE)ARRAY_VALUE[0]).VALUE()); System.out.println((String)ARRAY_VALUE[1]);
        int[] COUNT_Sąrašas = {1, 2, 3, 4}; System.arraycopy(COUNT_Sąrašas, 0, COUNT_Sąrašas, 1, 3); System.out.println(COUNT_Sąrašas[3]);
        byte[] baitas_VALUE = new byte[1]; baitas_VALUE[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] Bulio_logikos_VALUE = {true};
        System.out.println(baitas_VALUE[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + Bulio_logikos_VALUE[0]);
    }
}
