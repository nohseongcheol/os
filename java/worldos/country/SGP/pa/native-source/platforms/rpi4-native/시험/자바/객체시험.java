// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int ਕੀਮਤ(); }
class ਪਿਛੋਕੜ_ਕੀਮਤ { static int ਤਿਆਰ_ਕਰੋ = 7; int 수; String ਨਾਂ; ਪਿਛੋਕੜ_ਕੀਮਤ(int 수) { this.수 = 수; ਨਾਂ = "ਪਿਛੋਕੜ_ਕੀਮਤ"; } int ਕੀਮਤ() { return 수; } }
class ਸ਼ਾਖਾ_ਕੀਮਤ extends ਪਿਛੋਕੜ_ਕੀਮਤ implements 계산가능 { ਸ਼ਾਖਾ_ਕੀਮਤ(int 수) { super(수); ਨਾਂ = "ਸ਼ਾਖਾ_ਕੀਮਤ"; } public int ਕੀਮਤ() { return 수 * ਤਿਆਰ_ਕਰੋ; } }
public class 객체시험 {
    static int 초기 = ਪਿਛੋਕੜ_ਕੀਮਤ.ਤਿਆਰ_ਕਰੋ + 2;
    static int ਸ਼ਾਖਾ(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] ਆਰਗੂਮੈਂਟ) {
        ਸ਼ਾਖਾ_ਕੀਮਤ 나 = new ਸ਼ਾਖਾ_ਕੀਮਤ(6); ਪਿਛੋਕੜ_ਕੀਮਤ 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.ਨਾਂ + ":" + 다.ਕੀਮਤ() + ":" + 라.ਕੀਮਤ());
        System.out.println((다 instanceof ਸ਼ਾਖਾ_ਕੀਮਤ) + ":" + (다 instanceof 계산가능) + ":" + ਸ਼ਾਖਾ(2) + ":" + 띄엄(100));
        Object[] ਤਰਤੀਬ_ਦੇਣਾ_ਕੀਮਤ = new Object[3]; ਤਰਤੀਬ_ਦੇਣਾ_ਕੀਮਤ[0] = 나; ਤਰਤੀਬ_ਦੇਣਾ_ਕੀਮਤ[1] = "한글😀"; System.gc();
        System.out.println(((ਸ਼ਾਖਾ_ਕੀਮਤ)ਤਰਤੀਬ_ਦੇਣਾ_ਕੀਮਤ[0]).ਕੀਮਤ()); System.out.println((String)ਤਰਤੀਬ_ਦੇਣਾ_ਕੀਮਤ[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] ਬਾਈਟ_ਕੀਮਤ = new byte[1]; ਬਾਈਟ_ਕੀਮਤ[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(ਬਾਈਟ_ਕੀਮਤ[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
