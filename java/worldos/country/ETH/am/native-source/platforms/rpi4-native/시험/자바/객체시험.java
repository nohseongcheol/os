// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int እሴት(); }
class ልጣፍ_እሴት { static int አዘጋጅ_9ce364fc = 7; int 수; String ስም; ልጣፍ_እሴት(int 수) { this.수 = 수; ስም = "ልጣፍ_እሴት"; } int እሴት() { return 수; } }
class ቅርንጫፍ_እሴት extends ልጣፍ_እሴት implements 계산가능 { ቅርንጫፍ_እሴት(int 수) { super(수); ስም = "ቅርንጫፍ_እሴት"; } public int እሴት() { return 수 * አዘጋጅ_9ce364fc; } }
public class 객체시험 {
    static int 초기 = ልጣፍ_እሴት.አዘጋጅ_9ce364fc + 2;
    static int ቅርንጫፍ(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] 인수) {
        ቅርንጫፍ_እሴት 나 = new ቅርንጫፍ_እሴት(6); ልጣፍ_እሴት 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.ስም + ":" + 다.እሴት() + ":" + 라.እሴት());
        System.out.println((다 instanceof ቅርንጫፍ_እሴት) + ":" + (다 instanceof 계산가능) + ":" + ቅርንጫፍ(2) + ":" + 띄엄(100));
        Object[] ድርድር_እሴት = new Object[3]; ድርድር_እሴት[0] = 나; ድርድር_እሴት[1] = "한글😀"; System.gc();
        System.out.println(((ቅርንጫፍ_እሴት)ድርድር_እሴት[0]).እሴት()); System.out.println((String)ድርድር_እሴት[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] ባይት_እሴት = new byte[1]; ባይት_እሴት[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(ባይት_እሴት[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
