// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int مقدار(); }
class زمینه_مقدار_0764f371 { static int آماده_کردن = 7; int 수; String نام; زمینه_مقدار_0764f371(int 수) { this.수 = 수; نام = "زمینه_مقدار_0764f371"; } int مقدار() { return 수; } }
class شعبه_مقدار extends زمینه_مقدار_0764f371 implements 계산가능 { شعبه_مقدار(int 수) { super(수); نام = "شعبه_مقدار"; } public int مقدار() { return 수 * آماده_کردن; } }
public class 객체시험 {
    static int 초기 = زمینه_مقدار_0764f371.آماده_کردن + 2;
    static int شعبه(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] نشانوندها) {
        شعبه_مقدار 나 = new شعبه_مقدار(6); زمینه_مقدار_0764f371 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.نام + ":" + 다.مقدار() + ":" + 라.مقدار());
        System.out.println((다 instanceof شعبه_مقدار) + ":" + (다 instanceof 계산가능) + ":" + شعبه(2) + ":" + 띄엄(100));
        Object[] آرايه_مقدار = new Object[3]; آرايه_مقدار[0] = 나; آرايه_مقدار[1] = "한글😀"; System.gc();
        System.out.println(((شعبه_مقدار)آرايه_مقدار[0]).مقدار()); System.out.println((String)آرايه_مقدار[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] بایت_مقدار = new byte[1]; بایت_مقدار[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(بایت_مقدار[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
