// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int маани(); }
class Фон_маани { static int Даярдоо = 7; int 수; String Аты; Фон_маани(int 수) { this.수 = 수; Аты = "Фон_маани"; } int маани() { return 수; } }
class бутак_маани extends Фон_маани implements 계산가능 { бутак_маани(int 수) { super(수); Аты = "бутак_маани"; } public int маани() { return 수 * Даярдоо; } }
public class 객체시험 {
    static int 초기 = Фон_маани.Даярдоо + 2;
    static int бутак(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] 인수) {
        бутак_маани 나 = new бутак_маани(6); Фон_маани 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.Аты + ":" + 다.маани() + ":" + 라.маани());
        System.out.println((다 instanceof бутак_маани) + ":" + (다 instanceof 계산가능) + ":" + бутак(2) + ":" + 띄엄(100));
        Object[] МАССИВ_маани = new Object[3]; МАССИВ_маани[0] = 나; МАССИВ_маани[1] = "한글😀"; System.gc();
        System.out.println(((бутак_маани)МАССИВ_маани[0]).маани()); System.out.println((String)МАССИВ_маани[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] байт_маани = new byte[1]; байт_маани[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(байт_маани[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
