// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int ערך(); }
class טפט_ערך { static int להכין = 7; int 수; String שם; טפט_ערך(int 수) { this.수 = 수; שם = "טפט_ערך"; } int ערך() { return 수; } }
class ענף_ערך extends טפט_ערך implements 계산가능 { ענף_ערך(int 수) { super(수); שם = "ענף_ערך"; } public int ערך() { return 수 * להכין; } }
public class 객체시험 {
    static int מצב_התחלתי = טפט_ערך.להכין + 2;
    static int ענף(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] ארגומנטים) {
        ענף_ערך 나 = new ענף_ערך(6); טפט_ערך 다 = 나; 계산가능 라 = 나;
        System.out.println(מצב_התחלתי + ":" + 나.שם + ":" + 다.ערך() + ":" + 라.ערך());
        System.out.println((다 instanceof ענף_ערך) + ":" + (다 instanceof 계산가능) + ":" + ענף(2) + ":" + 띄엄(100));
        Object[] מערך_ערך = new Object[3]; מערך_ערך[0] = 나; מערך_ערך[1] = "한글😀"; System.gc();
        System.out.println(((ענף_ערך)מערך_ערך[0]).ערך()); System.out.println((String)מערך_ערך[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] בית_ערך = new byte[1]; בית_ערך[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] בוליאני_ערך = {true};
        System.out.println(בית_ערך[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + בוליאני_ערך[0]);
    }
}
