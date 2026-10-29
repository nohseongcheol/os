// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int តំលៃ(); }
class គំរូដែសថប_តំលៃ { static int រៀបចំ = 7; int 수; String ឈ្មោះ; គំរូដែសថប_តំលៃ(int 수) { this.수 = 수; ឈ្មោះ = "គំរូដែសថប_តំលៃ"; } int តំលៃ() { return 수; } }
class មែក_តំលៃ extends គំរូដែសថប_តំលៃ implements 계산가능 { មែក_តំលៃ(int 수) { super(수); ឈ្មោះ = "មែក_តំលៃ"; } public int តំលៃ() { return 수 * រៀបចំ; } }
public class 객체시험 {
    static int 초기 = គំរូដែសថប_តំលៃ.រៀបចំ + 2;
    static int មែក(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] អាគុយម៉ង់) {
        មែក_តំលៃ 나 = new មែក_តំលៃ(6); គំរូដែសថប_តំលៃ 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.ឈ្មោះ + ":" + 다.តំលៃ() + ":" + 라.តំលៃ());
        System.out.println((다 instanceof មែក_តំលៃ) + ":" + (다 instanceof 계산가능) + ":" + មែក(2) + ":" + 띄엄(100));
        Object[] អារេ_តំលៃ = new Object[3]; អារេ_តំលៃ[0] = 나; អារេ_តំលៃ[1] = "한글😀"; System.gc();
        System.out.println(((មែក_តំលៃ)អារេ_តំលៃ[0]).តំលៃ()); System.out.println((String)អារេ_តំលៃ[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] បៃ_តំលៃ = new byte[1]; បៃ_តំលៃ[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(បៃ_តំលៃ[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
