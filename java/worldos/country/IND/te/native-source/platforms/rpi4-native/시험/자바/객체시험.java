// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int మూల్యం(); }
class నేపథ్యం_మూల్యం { static int సిద్ధం_చేయు = 7; int 수; String పేరు; నేపథ్యం_మూల్యం(int 수) { this.수 = 수; పేరు = "నేపథ్యం_మూల్యం"; } int మూల్యం() { return 수; } }
class శాఖ_మూల్యం extends నేపథ్యం_మూల్యం implements 계산가능 { శాఖ_మూల్యం(int 수) { super(수); పేరు = "శాఖ_మూల్యం"; } public int మూల్యం() { return 수 * సిద్ధం_చేయు; } }
public class 객체시험 {
    static int 초기 = నేపథ్యం_మూల్యం.సిద్ధం_చేయు + 2;
    static int శాఖ(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] 인수) {
        శాఖ_మూల్యం 나 = new శాఖ_మూల్యం(6); నేపథ్యం_మూల్యం 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.పేరు + ":" + 다.మూల్యం() + ":" + 라.మూల్యం());
        System.out.println((다 instanceof శాఖ_మూల్యం) + ":" + (다 instanceof 계산가능) + ":" + శాఖ(2) + ":" + 띄엄(100));
        Object[] శ్రేణి_మూల్యం = new Object[3]; శ్రేణి_మూల్యం[0] = 나; శ్రేణి_మూల్యం[1] = "한글😀"; System.gc();
        System.out.println(((శాఖ_మూల్యం)శ్రేణి_మూల్యం[0]).మూల్యం()); System.out.println((String)శ్రేణి_మూల్యం[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] బైట్_మూల్యం = new byte[1]; బైట్_మూల్యం[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(బైట్_మూల్యం[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
