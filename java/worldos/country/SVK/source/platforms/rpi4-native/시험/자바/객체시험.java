// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int VALUE(); }
class tapeta_VALUE { static int Pripraviť = 7; int 수; String Názov; tapeta_VALUE(int 수) { this.수 = 수; Názov = "tapeta_VALUE"; } int VALUE() { return 수; } }
class vetva_VALUE extends tapeta_VALUE implements 계산가능 { vetva_VALUE(int 수) { super(수); Názov = "vetva_VALUE"; } public int VALUE() { return 수 * Pripraviť; } }
public class 객체시험 {
    static int počiatočný_stav = tapeta_VALUE.Pripraviť + 2;
    static int vetva(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] Argumenty) {
        vetva_VALUE SECOND_operand = new vetva_VALUE(6); tapeta_VALUE 다 = SECOND_operand; 계산가능 라 = SECOND_operand;
        System.out.println(počiatočný_stav + ":" + SECOND_operand.Názov + ":" + 다.VALUE() + ":" + 라.VALUE());
        System.out.println((다 instanceof vetva_VALUE) + ":" + (다 instanceof 계산가능) + ":" + vetva(2) + ":" + 띄엄(100));
        Object[] pole_VALUE = new Object[3]; pole_VALUE[0] = SECOND_operand; pole_VALUE[1] = "한글😀"; System.gc();
        System.out.println(((vetva_VALUE)pole_VALUE[0]).VALUE()); System.out.println((String)pole_VALUE[1]);
        int[] COUNT_Zoznam = {1, 2, 3, 4}; System.arraycopy(COUNT_Zoznam, 0, COUNT_Zoznam, 1, 3); System.out.println(COUNT_Zoznam[3]);
        byte[] Byte_VALUE = new byte[1]; Byte_VALUE[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] booleovský_VALUE = {true};
        System.out.println(Byte_VALUE[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + booleovský_VALUE[0]);
    }
}
