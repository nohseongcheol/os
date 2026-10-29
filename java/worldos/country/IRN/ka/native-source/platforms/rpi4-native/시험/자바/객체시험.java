// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int მნიშვნელობა(); }
class ფონი_მნიშვნელობა { static int მომზადება = 7; int 수; String სახელი; ფონი_მნიშვნელობა(int 수) { this.수 = 수; სახელი = "ფონი_მნიშვნელობა"; } int მნიშვნელობა() { return 수; } }
class განშტოება_მნიშვნელობა extends ფონი_მნიშვნელობა implements 계산가능 { განშტოება_მნიშვნელობა(int 수) { super(수); სახელი = "განშტოება_მნიშვნელობა"; } public int მნიშვნელობა() { return 수 * მომზადება; } }
public class 객체시험 {
    static int 초기 = ფონი_მნიშვნელობა.მომზადება + 2;
    static int განშტოება(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] 인수) {
        განშტოება_მნიშვნელობა 나 = new განშტოება_მნიშვნელობა(6); ფონი_მნიშვნელობა 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.სახელი + ":" + 다.მნიშვნელობა() + ":" + 라.მნიშვნელობა());
        System.out.println((다 instanceof განშტოება_მნიშვნელობა) + ":" + (다 instanceof 계산가능) + ":" + განშტოება(2) + ":" + 띄엄(100));
        Object[] მასივი_მნიშვნელობა = new Object[3]; მასივი_მნიშვნელობა[0] = 나; მასივი_მნიშვნელობა[1] = "한글😀"; System.gc();
        System.out.println(((განშტოება_მნიშვნელობა)მასივი_მნიშვნელობა[0]).მნიშვნელობა()); System.out.println((String)მასივი_მნიშვნელობა[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] ბაიტი_მნიშვნელობა = new byte[1]; ბაიტი_მნიშვნელობა[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(ბაიტი_მნიშვნელობა[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
