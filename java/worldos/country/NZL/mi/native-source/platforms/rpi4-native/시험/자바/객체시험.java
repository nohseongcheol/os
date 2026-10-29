// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int uara(); }
class Papamuri_uara { static int Whakarite = 7; int 수; String Ingoa; Papamuri_uara(int 수) { this.수 = 수; Ingoa = "Papamuri_uara"; } int uara() { return 수; } }
class peka_uara extends Papamuri_uara implements 계산가능 { peka_uara(int 수) { super(수); Ingoa = "peka_uara"; } public int uara() { return 수 * Whakarite; } }
public class 객체시험 {
    static int 초기 = Papamuri_uara.Whakarite + 2;
    static int peka(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] 인수) {
        peka_uara 나 = new peka_uara(6); Papamuri_uara 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.Ingoa + ":" + 다.uara() + ":" + 라.uara());
        System.out.println((다 instanceof peka_uara) + ":" + (다 instanceof 계산가능) + ":" + peka(2) + ":" + 띄엄(100));
        Object[] HUĀNGA_uara = new Object[3]; HUĀNGA_uara[0] = 나; HUĀNGA_uara[1] = "한글😀"; System.gc();
        System.out.println(((peka_uara)HUĀNGA_uara[0]).uara()); System.out.println((String)HUĀNGA_uara[1]);
        int[] COUNT_Rārangi = {1, 2, 3, 4}; System.arraycopy(COUNT_Rārangi, 0, COUNT_Rārangi, 1, 3); System.out.println(COUNT_Rārangi[3]);
        byte[] paita_uara = new byte[1]; paita_uara[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(paita_uara[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
