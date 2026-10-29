// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int মান(); }
class পটভূমি_মান { static int প্রস্তুত_করুন = 7; int 수; String নাম; পটভূমি_মান(int 수) { this.수 = 수; নাম = "পটভূমি_মান"; } int মান() { return 수; } }
class শাখা_মান extends পটভূমি_মান implements 계산가능 { শাখা_মান(int 수) { super(수); নাম = "শাখা_মান"; } public int মান() { return 수 * প্রস্তুত_করুন; } }
public class 객체시험 {
    static int 초기 = পটভূমি_মান.প্রস্তুত_করুন + 2;
    static int শাখা(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] আর্গুমেন্ট_তালিকা) {
        শাখা_মান 나 = new শাখা_মান(6); পটভূমি_মান 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.নাম + ":" + 다.মান() + ":" + 라.মান());
        System.out.println((다 instanceof শাখা_মান) + ":" + (다 instanceof 계산가능) + ":" + শাখা(2) + ":" + 띄엄(100));
        Object[] অ্যারে_মান = new Object[3]; অ্যারে_মান[0] = 나; অ্যারে_মান[1] = "한글😀"; System.gc();
        System.out.println(((শাখা_মান)অ্যারে_মান[0]).মান()); System.out.println((String)অ্যারে_মান[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] বাইট_মান = new byte[1]; বাইট_মান[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(বাইট_মান[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
