// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int قيمة(); }
class خلفية_قيمة { static int إعداد = 7; int رقم; String اسم; خلفية_قيمة(int رقم) { this.رقم = رقم; اسم = "خلفية_قيمة"; } int قيمة() { return رقم; } }
class فرع_قيمة extends خلفية_قيمة implements 계산가능 { فرع_قيمة(int رقم) { super(رقم); اسم = "فرع_قيمة"; } public int قيمة() { return رقم * إعداد; } }
public class 객체시험 {
    static int حالة_أولية = خلفية_قيمة.إعداد + 2;
    static int فرع(int رقم) { switch (رقم) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int رقم) { switch (رقم) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] وسائط) {
        فرع_قيمة 나 = new فرع_قيمة(6); خلفية_قيمة 다 = 나; 계산가능 라 = 나;
        System.out.println(حالة_أولية + ":" + 나.اسم + ":" + 다.قيمة() + ":" + 라.قيمة());
        System.out.println((다 instanceof فرع_قيمة) + ":" + (다 instanceof 계산가능) + ":" + فرع(2) + ":" + 띄엄(100));
        Object[] صفيف_قيمة = new Object[3]; صفيف_قيمة[0] = 나; صفيف_قيمة[1] = "한글😀"; System.gc();
        System.out.println(((فرع_قيمة)صفيف_قيمة[0]).قيمة()); System.out.println((String)صفيف_قيمة[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] بايت_قيمة = new byte[1]; بايت_قيمة[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] منطقي_قيمة = {true};
        System.out.println(بايت_قيمة[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + منطقي_قيمة[0]);
    }
}
