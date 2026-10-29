// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int ixabiso(); }
class Ngasemva_ixabiso { static int lungisa = 7; int 수; String Igama; Ngasemva_ixabiso(int 수) { this.수 = 수; Igama = "Ngasemva_ixabiso"; } int ixabiso() { return 수; } }
class isebe_ixabiso extends Ngasemva_ixabiso implements 계산가능 { isebe_ixabiso(int 수) { super(수); Igama = "isebe_ixabiso"; } public int ixabiso() { return 수 * lungisa; } }
public class 객체시험 {
    static int 초기 = Ngasemva_ixabiso.lungisa + 2;
    static int isebe(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] 인수) {
        isebe_ixabiso 나 = new isebe_ixabiso(6); Ngasemva_ixabiso 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.Igama + ":" + 다.ixabiso() + ":" + 라.ixabiso());
        System.out.println((다 instanceof isebe_ixabiso) + ":" + (다 instanceof 계산가능) + ":" + isebe(2) + ":" + 띄엄(100));
        Object[] ULUHLU_ixabiso = new Object[3]; ULUHLU_ixabiso[0] = 나; ULUHLU_ixabiso[1] = "한글😀"; System.gc();
        System.out.println(((isebe_ixabiso)ULUHLU_ixabiso[0]).ixabiso()); System.out.println((String)ULUHLU_ixabiso[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] ibhayithi_ixabiso = new byte[1]; ibhayithi_ixabiso[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(ibhayithi_ixabiso[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
