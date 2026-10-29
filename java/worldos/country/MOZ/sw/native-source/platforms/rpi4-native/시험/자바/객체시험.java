// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int thamani(); }
class nyuma_thamani { static int Andaa = 7; int 수; String Jina; nyuma_thamani(int 수) { this.수 = 수; Jina = "nyuma_thamani"; } int thamani() { return 수; } }
class tawi_thamani extends nyuma_thamani implements 계산가능 { tawi_thamani(int 수) { super(수); Jina = "tawi_thamani"; } public int thamani() { return 수 * Andaa; } }
public class 객체시험 {
    static int 초기 = nyuma_thamani.Andaa + 2;
    static int tawi(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] 인수) {
        tawi_thamani 나 = new tawi_thamani(6); nyuma_thamani 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.Jina + ":" + 다.thamani() + ":" + 라.thamani());
        System.out.println((다 instanceof tawi_thamani) + ":" + (다 instanceof 계산가능) + ":" + tawi(2) + ":" + 띄엄(100));
        Object[] ARRAY_thamani = new Object[3]; ARRAY_thamani[0] = 나; ARRAY_thamani[1] = "한글😀"; System.gc();
        System.out.println(((tawi_thamani)ARRAY_thamani[0]).thamani()); System.out.println((String)ARRAY_thamani[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] baiti_thamani = new byte[1]; baiti_thamani[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(baiti_thamani[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
