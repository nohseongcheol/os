// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int ମୂଲ୍ୟ(); }
class ପୃଷ୍ଠପଟ_ମୂଲ୍ୟ { static int ପ୍ରସ୍ତୁତ = 7; int 수; String ନାମ; ପୃଷ୍ଠପଟ_ମୂଲ୍ୟ(int 수) { this.수 = 수; ନାମ = "ପୃଷ୍ଠପଟ_ମୂଲ୍ୟ"; } int ମୂଲ୍ୟ() { return 수; } }
class ଶାଖା_ମୂଲ୍ୟ extends ପୃଷ୍ଠପଟ_ମୂଲ୍ୟ implements 계산가능 { ଶାଖା_ମୂଲ୍ୟ(int 수) { super(수); ନାମ = "ଶାଖା_ମୂଲ୍ୟ"; } public int ମୂଲ୍ୟ() { return 수 * ପ୍ରସ୍ତୁତ; } }
public class 객체시험 {
    static int 초기 = ପୃଷ୍ଠପଟ_ମୂଲ୍ୟ.ପ୍ରସ୍ତୁତ + 2;
    static int ଶାଖା(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] 인수) {
        ଶାଖା_ମୂଲ୍ୟ 나 = new ଶାଖା_ମୂଲ୍ୟ(6); ପୃଷ୍ଠପଟ_ମୂଲ୍ୟ 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.ନାମ + ":" + 다.ମୂଲ୍ୟ() + ":" + 라.ମୂଲ୍ୟ());
        System.out.println((다 instanceof ଶାଖା_ମୂଲ୍ୟ) + ":" + (다 instanceof 계산가능) + ":" + ଶାଖା(2) + ":" + 띄엄(100));
        Object[] ଆରେ_ମୂଲ୍ୟ = new Object[3]; ଆରେ_ମୂଲ୍ୟ[0] = 나; ଆରେ_ମୂଲ୍ୟ[1] = "한글😀"; System.gc();
        System.out.println(((ଶାଖା_ମୂଲ୍ୟ)ଆରେ_ମୂଲ୍ୟ[0]).ମୂଲ୍ୟ()); System.out.println((String)ଆରେ_ମୂଲ୍ୟ[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] ବାଇଟ୍_ମୂଲ୍ୟ = new byte[1]; ବାଇଟ୍_ମୂଲ୍ୟ[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(ବାଇଟ୍_ମୂଲ୍ୟ[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
