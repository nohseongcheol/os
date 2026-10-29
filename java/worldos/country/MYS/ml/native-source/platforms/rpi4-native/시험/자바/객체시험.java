// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int മൂല്യം(); }
class నేపథ్యం_മൂല്യം { static int തയ്യാറാക്കുക = 7; int 수; String പേരു്; నేపథ్యం_മൂല്യം(int 수) { this.수 = 수; പേരു് = "నేపథ్యం_മൂല്യം"; } int മൂല്യം() { return 수; } }
class ശാഖ_മൂല്യം extends నేపథ్యం_മൂല്യം implements 계산가능 { ശാഖ_മൂല്യം(int 수) { super(수); പേരു് = "ശാഖ_മൂല്യം"; } public int മൂല്യം() { return 수 * തയ്യാറാക്കുക; } }
public class 객체시험 {
    static int 초기 = నేపథ్యం_മൂല്യം.തയ്യാറാക്കുക + 2;
    static int ശാഖ(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] 인수) {
        ശാഖ_മൂല്യം 나 = new ശാഖ_മൂല്യം(6); నేపథ్యం_മൂല്യം 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.പേരു് + ":" + 다.മൂല്യം() + ":" + 라.മൂല്യം());
        System.out.println((다 instanceof ശാഖ_മൂല്യം) + ":" + (다 instanceof 계산가능) + ":" + ശാഖ(2) + ":" + 띄엄(100));
        Object[] അരേ_മൂല്യം = new Object[3]; അരേ_മൂല്യം[0] = 나; അരേ_മൂല്യം[1] = "한글😀"; System.gc();
        System.out.println(((ശാഖ_മൂല്യം)അരേ_മൂല്യം[0]).മൂല്യം()); System.out.println((String)അരേ_മൂല്യം[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] బైట్_മൂല്യം = new byte[1]; బైట్_മൂല്യം[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(బైట్_മൂല്യം[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
