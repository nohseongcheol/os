// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int قىممىتى(); }
class تەگلىك_قىممىتى { static int تەييارلىماق = 7; int 수; String ئاتى; تەگلىك_قىممىتى(int 수) { this.수 = 수; ئاتى = "تەگلىك_قىممىتى"; } int قىممىتى() { return 수; } }
class شاخ_قىممىتى extends تەگلىك_قىممىتى implements 계산가능 { شاخ_قىممىتى(int 수) { super(수); ئاتى = "شاخ_قىممىتى"; } public int قىممىتى() { return 수 * تەييارلىماق; } }
public class 객체시험 {
    static int 초기 = تەگلىك_قىممىتى.تەييارلىماق + 2;
    static int شاخ(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] ئۆزگەرگۈچىلەر) {
        شاخ_قىممىتى 나 = new شاخ_قىممىتى(6); تەگلىك_قىممىتى 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.ئاتى + ":" + 다.قىممىتى() + ":" + 라.قىممىتى());
        System.out.println((다 instanceof شاخ_قىممىتى) + ":" + (다 instanceof 계산가능) + ":" + شاخ(2) + ":" + 띄엄(100));
        Object[] رەت_قىممىتى = new Object[3]; رەت_قىممىتى[0] = 나; رەت_قىممىتى[1] = "한글😀"; System.gc();
        System.out.println(((شاخ_قىممىتى)رەت_قىممىتى[0]).قىممىتى()); System.out.println((String)رەت_قىممىتى[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] بايت_قىممىتى = new byte[1]; بايت_قىممىتى[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(بايت_قىممىتى[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
