// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int Daraja(); }
class Bi_bango_Daraja { static int Shirya = 7; int 수; String Suna; Bi_bango_Daraja(int 수) { this.수 = 수; Suna = "Bi_bango_Daraja"; } int Daraja() { return 수; } }
class Reshe_Daraja extends Bi_bango_Daraja implements 계산가능 { Reshe_Daraja(int 수) { super(수); Suna = "Reshe_Daraja"; } public int Daraja() { return 수 * Shirya; } }
public class 객체시험 {
    static int 초기 = Bi_bango_Daraja.Shirya + 2;
    static int Reshe(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] 인수) {
        Reshe_Daraja 나 = new Reshe_Daraja(6); Bi_bango_Daraja 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.Suna + ":" + 다.Daraja() + ":" + 라.Daraja());
        System.out.println((다 instanceof Reshe_Daraja) + ":" + (다 instanceof 계산가능) + ":" + Reshe(2) + ":" + 띄엄(100));
        Object[] TSARI_Daraja = new Object[3]; TSARI_Daraja[0] = 나; TSARI_Daraja[1] = "한글😀"; System.gc();
        System.out.println(((Reshe_Daraja)TSARI_Daraja[0]).Daraja()); System.out.println((String)TSARI_Daraja[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] bayit_Daraja = new byte[1]; bayit_Daraja[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(bayit_Daraja[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
