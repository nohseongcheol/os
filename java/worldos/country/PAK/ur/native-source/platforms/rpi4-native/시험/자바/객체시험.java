// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int قدر(); }
class پس_منظر_قدر { static int تیار_کریں = 7; int 수; String نام; پس_منظر_قدر(int 수) { this.수 = 수; نام = "پس_منظر_قدر"; } int قدر() { return 수; } }
class برانچ_قدر extends پس_منظر_قدر implements 계산가능 { برانچ_قدر(int 수) { super(수); نام = "برانچ_قدر"; } public int قدر() { return 수 * تیار_کریں; } }
public class 객체시험 {
    static int 초기 = پس_منظر_قدر.تیار_کریں + 2;
    static int برانچ(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] دلائل) {
        برانچ_قدر 나 = new برانچ_قدر(6); پس_منظر_قدر 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.نام + ":" + 다.قدر() + ":" + 라.قدر());
        System.out.println((다 instanceof برانچ_قدر) + ":" + (다 instanceof 계산가능) + ":" + برانچ(2) + ":" + 띄엄(100));
        Object[] لڑی_قدر = new Object[3]; لڑی_قدر[0] = 나; لڑی_قدر[1] = "한글😀"; System.gc();
        System.out.println(((برانچ_قدر)لڑی_قدر[0]).قدر()); System.out.println((String)لڑی_قدر[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] بائٹ_قدر = new byte[1]; بائٹ_قدر[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(بائٹ_قدر[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
