// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int τιμή(); }
class φόντο_τιμή { static int Προετοίμασε = 7; int 수; String Όνομα; φόντο_τιμή(int 수) { this.수 = 수; Όνομα = "φόντο_τιμή"; } int τιμή() { return 수; } }
class κλάδος_τιμή extends φόντο_τιμή implements 계산가능 { κλάδος_τιμή(int 수) { super(수); Όνομα = "κλάδος_τιμή"; } public int τιμή() { return 수 * Προετοίμασε; } }
public class 객체시험 {
    static int αρχική_κατάσταση = φόντο_τιμή.Προετοίμασε + 2;
    static int κλάδος(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] Παράμετροι) {
        κλάδος_τιμή 나 = new κλάδος_τιμή(6); φόντο_τιμή 다 = 나; 계산가능 라 = 나;
        System.out.println(αρχική_κατάσταση + ":" + 나.Όνομα + ":" + 다.τιμή() + ":" + 라.τιμή());
        System.out.println((다 instanceof κλάδος_τιμή) + ":" + (다 instanceof 계산가능) + ":" + κλάδος(2) + ":" + 띄엄(100));
        Object[] πίνακας_τιμή = new Object[3]; πίνακας_τιμή[0] = 나; πίνακας_τιμή[1] = "한글😀"; System.gc();
        System.out.println(((κλάδος_τιμή)πίνακας_τιμή[0]).τιμή()); System.out.println((String)πίνακας_τιμή[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] 바이트 = new byte[1]; 바이트[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] δυαδική_τιμή_τιμή = {true};
        System.out.println(바이트[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + δυαδική_τιμή_τιμή[0]);
    }
}
