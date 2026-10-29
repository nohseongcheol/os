// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int ዋጋ(); }
class ድሕረባይታ_ዋጋ { static int ኣዳልው = 7; int 수; String ሽም; ድሕረባይታ_ዋጋ(int 수) { this.수 = 수; ሽም = "ድሕረባይታ_ዋጋ"; } int ዋጋ() { return 수; } }
class ጨንፈር_ዋጋ extends ድሕረባይታ_ዋጋ implements 계산가능 { ጨንፈር_ዋጋ(int 수) { super(수); ሽም = "ጨንፈር_ዋጋ"; } public int ዋጋ() { return 수 * ኣዳልው; } }
public class 객체시험 {
    static int 초기 = ድሕረባይታ_ዋጋ.ኣዳልው + 2;
    static int ጨንፈር(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] 인수) {
        ጨንፈር_ዋጋ 나 = new ጨንፈር_ዋጋ(6); ድሕረባይታ_ዋጋ 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.ሽም + ":" + 다.ዋጋ() + ":" + 라.ዋጋ());
        System.out.println((다 instanceof ጨንፈር_ዋጋ) + ":" + (다 instanceof 계산가능) + ":" + ጨንፈር(2) + ":" + 띄엄(100));
        Object[] ተርታ_ዋጋ_ed437109 = new Object[3]; ተርታ_ዋጋ_ed437109[0] = 나; ተርታ_ዋጋ_ed437109[1] = "한글😀"; System.gc();
        System.out.println(((ጨንፈር_ዋጋ)ተርታ_ዋጋ_ed437109[0]).ዋጋ()); System.out.println((String)ተርታ_ዋጋ_ed437109[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] ባይት_ዋጋ = new byte[1]; ባይት_ዋጋ[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(ባይት_ዋጋ[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
