// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int atuutilik(); }
class ungataa_atuutilik { static int Parnalli = 7; int 수; String atiq; ungataa_atuutilik(int 수) { this.수 = 수; atiq = "ungataa_atuutilik"; } int atuutilik() { return 수; } }
class avalangajuq_atuutilik extends ungataa_atuutilik implements 계산가능 { avalangajuq_atuutilik(int 수) { super(수); atiq = "avalangajuq_atuutilik"; } public int atuutilik() { return 수 * Parnalli; } }
public class 객체시험 {
    static int 초기 = ungataa_atuutilik.Parnalli + 2;
    static int avalangajuq(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] 인수) {
        avalangajuq_atuutilik 나 = new avalangajuq_atuutilik(6); ungataa_atuutilik 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.atiq + ":" + 다.atuutilik() + ":" + 라.atuutilik());
        System.out.println((다 instanceof avalangajuq_atuutilik) + ":" + (다 instanceof 계산가능) + ":" + avalangajuq(2) + ":" + 띄엄(100));
        Object[] array_atuutilik = new Object[3]; array_atuutilik[0] = 나; array_atuutilik[1] = "한글😀"; System.gc();
        System.out.println(((avalangajuq_atuutilik)array_atuutilik[0]).atuutilik()); System.out.println((String)array_atuutilik[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] byte_atuutilik = new byte[1]; byte_atuutilik[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(byte_atuutilik[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
