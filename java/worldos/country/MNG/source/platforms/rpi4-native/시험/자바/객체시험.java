// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int утга(); }
class Дэвсгэр_утга { static int Бэлтгэх = 7; int 수; String Нэр; Дэвсгэр_утга(int 수) { this.수 = 수; Нэр = "Дэвсгэр_утга"; } int утга() { return 수; } }
class салбар_утга extends Дэвсгэр_утга implements 계산가능 { салбар_утга(int 수) { super(수); Нэр = "салбар_утга"; } public int утга() { return 수 * Бэлтгэх; } }
public class 객체시험 {
    static int 초기 = Дэвсгэр_утга.Бэлтгэх + 2;
    static int салбар(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] 인수) {
        салбар_утга 나 = new салбар_утга(6); Дэвсгэр_утга 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.Нэр + ":" + 다.утга() + ":" + 라.утга());
        System.out.println((다 instanceof салбар_утга) + ":" + (다 instanceof 계산가능) + ":" + салбар(2) + ":" + 띄엄(100));
        Object[] олонлог_утга = new Object[3]; олонлог_утга[0] = 나; олонлог_утга[1] = "한글😀"; System.gc();
        System.out.println(((салбар_утга)олонлог_утга[0]).утга()); System.out.println((String)олонлог_утга[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] байт_утга = new byte[1]; байт_утга[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(байт_утга[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
