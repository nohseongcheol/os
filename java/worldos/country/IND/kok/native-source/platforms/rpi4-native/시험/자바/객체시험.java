// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int मोल(); }
class फाटभूंय_मोल { static int तयार_करचें_9ce364fc = 7; int 수; String नांव; फाटभूंय_मोल(int 수) { this.수 = 수; नांव = "फाटभूंय_मोल"; } int मोल() { return 수; } }
class शाखा_मोल extends फाटभूंय_मोल implements 계산가능 { शाखा_मोल(int 수) { super(수); नांव = "शाखा_मोल"; } public int मोल() { return 수 * तयार_करचें_9ce364fc; } }
public class 객체시험 {
    static int 초기 = फाटभूंय_मोल.तयार_करचें_9ce364fc + 2;
    static int शाखा(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] 인수) {
        शाखा_मोल 나 = new शाखा_मोल(6); फाटभूंय_मोल 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.नांव + ":" + 다.मोल() + ":" + 라.मोल());
        System.out.println((다 instanceof शाखा_मोल) + ":" + (다 instanceof 계산가능) + ":" + शाखा(2) + ":" + 띄엄(100));
        Object[] क्रम_मोल_ed437109 = new Object[3]; क्रम_मोल_ed437109[0] = 나; क्रम_मोल_ed437109[1] = "한글😀"; System.gc();
        System.out.println(((शाखा_मोल)क्रम_मोल_ed437109[0]).मोल()); System.out.println((String)क्रम_मोल_ed437109[1]);
        int[] COUNT_सुची = {1, 2, 3, 4}; System.arraycopy(COUNT_सुची, 0, COUNT_सुची, 1, 3); System.out.println(COUNT_सुची[3]);
        byte[] बायट_मोल = new byte[1]; बायट_मोल[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(बायट_मोल[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
