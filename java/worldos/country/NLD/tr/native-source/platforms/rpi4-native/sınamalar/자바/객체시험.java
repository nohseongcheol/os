// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int değer(); }
class Arka_Plan_değer { static int Hazırlan = 7; int 수; String İsim; Arka_Plan_değer(int 수) { this.수 = 수; İsim = "Arka_Plan_değer"; } int değer() { return 수; } }
class dal_değer extends Arka_Plan_değer implements 계산가능 { dal_değer(int 수) { super(수); İsim = "dal_değer"; } public int değer() { return 수 * Hazırlan; } }
public class 객체시험 {
    static int başlangıç_durumu = Arka_Plan_değer.Hazırlan + 2;
    static int dal(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] bağımsız_değişkenler) {
        dal_değer SANİYE_işlenen = new dal_değer(6); Arka_Plan_değer 다 = SANİYE_işlenen; 계산가능 라 = SANİYE_işlenen;
        System.out.println(başlangıç_durumu + ":" + SANİYE_işlenen.İsim + ":" + 다.değer() + ":" + 라.değer());
        System.out.println((다 instanceof dal_değer) + ":" + (다 instanceof 계산가능) + ":" + dal(2) + ":" + 띄엄(100));
        Object[] DİZİ_değer = new Object[3]; DİZİ_değer[0] = SANİYE_işlenen; DİZİ_değer[1] = "한글😀"; System.gc();
        System.out.println(((dal_değer)DİZİ_değer[0]).değer()); System.out.println((String)DİZİ_değer[1]);
        int[] BAĞ_DEĞ_SAY_Liste = {1, 2, 3, 4}; System.arraycopy(BAĞ_DEĞ_SAY_Liste, 0, BAĞ_DEĞ_SAY_Liste, 1, 3); System.out.println(BAĞ_DEĞ_SAY_Liste[3]);
        byte[] bayt_değer = new byte[1]; bayt_değer[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] Boole_değer = {true};
        System.out.println(bayt_değer[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + Boole_değer[0]);
    }
}
