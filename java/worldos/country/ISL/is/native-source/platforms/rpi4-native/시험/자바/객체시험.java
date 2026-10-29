// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int VALUE(); }
class veggfóður_VALUE { static int Undirbúa = 7; int númer; String Heiti; veggfóður_VALUE(int númer) { this.númer = númer; Heiti = "veggfóður_VALUE"; } int VALUE() { return númer; } }
class grein_VALUE extends veggfóður_VALUE implements 계산가능 { grein_VALUE(int númer) { super(númer); Heiti = "grein_VALUE"; } public int VALUE() { return númer * Undirbúa; } }
public class 객체시험 {
    static int 초기 = veggfóður_VALUE.Undirbúa + 2;
    static int grein(int númer) { switch (númer) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int númer) { switch (númer) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] Viðföng) {
        grein_VALUE 나 = new grein_VALUE(6); veggfóður_VALUE 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.Heiti + ":" + 다.VALUE() + ":" + 라.VALUE());
        System.out.println((다 instanceof grein_VALUE) + ":" + (다 instanceof 계산가능) + ":" + grein(2) + ":" + 띄엄(100));
        Object[] ARRAY_VALUE = new Object[3]; ARRAY_VALUE[0] = 나; ARRAY_VALUE[1] = "한글😀"; System.gc();
        System.out.println(((grein_VALUE)ARRAY_VALUE[0]).VALUE()); System.out.println((String)ARRAY_VALUE[1]);
        int[] COUNT_Listi = {1, 2, 3, 4}; System.arraycopy(COUNT_Listi, 0, COUNT_Listi, 1, 3); System.out.println(COUNT_Listi[3]);
        byte[] bæti_VALUE = new byte[1]; bæti_VALUE[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(bæti_VALUE[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
