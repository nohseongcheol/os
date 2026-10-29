// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int نرخ(); }
class بن_زمینه_نرخ { static int ئامادە_کردن_9ce364fc = 7; int 수; String ناو; بن_زمینه_نرخ(int 수) { this.수 = 수; ناو = "بن_زمینه_نرخ"; } int نرخ() { return 수; } }
class لق_نرخ extends بن_زمینه_نرخ implements 계산가능 { لق_نرخ(int 수) { super(수); ناو = "لق_نرخ"; } public int نرخ() { return 수 * ئامادە_کردن_9ce364fc; } }
public class 객체시험 {
    static int 초기 = بن_زمینه_نرخ.ئامادە_کردن_9ce364fc + 2;
    static int لق(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] 인수) {
        لق_نرخ 나 = new لق_نرخ(6); بن_زمینه_نرخ 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.ناو + ":" + 다.نرخ() + ":" + 라.نرخ());
        System.out.println((다 instanceof لق_نرخ) + ":" + (다 instanceof 계산가능) + ":" + لق(2) + ":" + 띄엄(100));
        Object[] ڕیزی_داتا_نرخ = new Object[3]; ڕیزی_داتا_نرخ[0] = 나; ڕیزی_داتا_نرخ[1] = "한글😀"; System.gc();
        System.out.println(((لق_نرخ)ڕیزی_داتا_نرخ[0]).نرخ()); System.out.println((String)ڕیزی_داتا_نرخ[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] بایت_نرخ = new byte[1]; بایت_نرخ[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(بایت_نرخ[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
