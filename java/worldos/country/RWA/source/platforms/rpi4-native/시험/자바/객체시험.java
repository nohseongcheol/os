// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int agaciro(); }
class Imbuganyuma_agaciro { static int Gutegura = 7; int 수; String Izina; Imbuganyuma_agaciro(int 수) { this.수 = 수; Izina = "Imbuganyuma_agaciro"; } int agaciro() { return 수; } }
class ishami_agaciro extends Imbuganyuma_agaciro implements 계산가능 { ishami_agaciro(int 수) { super(수); Izina = "ishami_agaciro"; } public int agaciro() { return 수 * Gutegura; } }
public class 객체시험 {
    static int 초기 = Imbuganyuma_agaciro.Gutegura + 2;
    static int ishami(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] 인수) {
        ishami_agaciro 나 = new ishami_agaciro(6); Imbuganyuma_agaciro 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.Izina + ":" + 다.agaciro() + ":" + 라.agaciro());
        System.out.println((다 instanceof ishami_agaciro) + ":" + (다 instanceof 계산가능) + ":" + ishami(2) + ":" + 띄엄(100));
        Object[] ARRAY_agaciro = new Object[3]; ARRAY_agaciro[0] = 나; ARRAY_agaciro[1] = "한글😀"; System.gc();
        System.out.println(((ishami_agaciro)ARRAY_agaciro[0]).agaciro()); System.out.println((String)ARRAY_agaciro[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] bayiti_agaciro = new byte[1]; bayiti_agaciro[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(bayiti_agaciro[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
