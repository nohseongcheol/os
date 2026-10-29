// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int արժեք(); }
class խորք_արժեք { static int Պատրաստել = 7; int 수; String Անուն; խորք_արժեք(int 수) { this.수 = 수; Անուն = "խորք_արժեք"; } int արժեք() { return 수; } }
class ճյուղ_արժեք extends խորք_արժեք implements 계산가능 { ճյուղ_արժեք(int 수) { super(수); Անուն = "ճյուղ_արժեք"; } public int արժեք() { return 수 * Պատրաստել; } }
public class 객체시험 {
    static int 초기 = խորք_արժեք.Պատրաստել + 2;
    static int ճյուղ(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] 인수) {
        ճյուղ_արժեք 나 = new ճյուղ_արժեք(6); խորք_արժեք 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.Անուն + ":" + 다.արժեք() + ":" + 라.արժեք());
        System.out.println((다 instanceof ճյուղ_արժեք) + ":" + (다 instanceof 계산가능) + ":" + ճյուղ(2) + ":" + 띄엄(100));
        Object[] ԶԱՆԳՎԱԾ_արժեք = new Object[3]; ԶԱՆԳՎԱԾ_արժեք[0] = 나; ԶԱՆԳՎԱԾ_արժեք[1] = "한글😀"; System.gc();
        System.out.println(((ճյուղ_արժեք)ԶԱՆԳՎԱԾ_արժեք[0]).արժեք()); System.out.println((String)ԶԱՆԳՎԱԾ_արժեք[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] բայթ_արժեք = new byte[1]; բայթ_արժեք[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(բայթ_արժեք[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
