// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int ᏧᎬᏩᎶᏗᏯ(); }
class ᎠᏍᏆᏚᎸ_ᎦᏯᎸᏗ_ᏧᎬᏩᎶᏗᏯ { static int ᎭᏛᏅᎢᏍᏓ = 7; int 수; String ᏚᏙᎥᎢ; ᎠᏍᏆᏚᎸ_ᎦᏯᎸᏗ_ᏧᎬᏩᎶᏗᏯ(int 수) { this.수 = 수; ᏚᏙᎥᎢ = "ᎠᏍᏆᏚᎸ_ᎦᏯᎸᏗ_ᏧᎬᏩᎶᏗᏯ"; } int ᏧᎬᏩᎶᏗᏯ() { return 수; } }
class 가지 extends ᎠᏍᏆᏚᎸ_ᎦᏯᎸᏗ_ᏧᎬᏩᎶᏗᏯ implements 계산가능 { 가지(int 수) { super(수); ᏚᏙᎥᎢ = "가지"; } public int ᏧᎬᏩᎶᏗᏯ() { return 수 * ᎭᏛᏅᎢᏍᏓ; } }
public class 객체시험 {
    static int 초기 = ᎠᏍᏆᏚᎸ_ᎦᏯᎸᏗ_ᏧᎬᏩᎶᏗᏯ.ᎭᏛᏅᎢᏍᏓ + 2;
    static int 분기(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] 인수) {
        가지 나 = new 가지(6); ᎠᏍᏆᏚᎸ_ᎦᏯᎸᏗ_ᏧᎬᏩᎶᏗᏯ 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.ᏚᏙᎥᎢ + ":" + 다.ᏧᎬᏩᎶᏗᏯ() + ":" + 라.ᏧᎬᏩᎶᏗᏯ());
        System.out.println((다 instanceof 가지) + ":" + (다 instanceof 계산가능) + ":" + 분기(2) + ":" + 띄엄(100));
        Object[] array_ᏧᎬᏩᎶᏗᏯ = new Object[3]; array_ᏧᎬᏩᎶᏗᏯ[0] = 나; array_ᏧᎬᏩᎶᏗᏯ[1] = "한글😀"; System.gc();
        System.out.println(((가지)array_ᏧᎬᏩᎶᏗᏯ[0]).ᏧᎬᏩᎶᏗᏯ()); System.out.println((String)array_ᏧᎬᏩᎶᏗᏯ[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] byte_ᏧᎬᏩᎶᏗᏯ = new byte[1]; byte_ᏧᎬᏩᎶᏗᏯ[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(byte_ᏧᎬᏩᎶᏗᏯ[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
