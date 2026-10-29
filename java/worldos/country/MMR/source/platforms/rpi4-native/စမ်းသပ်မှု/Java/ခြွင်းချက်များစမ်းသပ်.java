// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class ခြွင်းချက်များစမ်းသပ် {
    static int စားတန်ဖိုးများ(int n) { return 8 / n; }
    static int အပြီးသတ်() { try { return စားတန်ဖိုးများ(0); } finally { System.out.println("အပြီးသတ်"); } }
    public static void main(String[] a) {
        try { အပြီးသတ်(); } catch (ArithmeticException e) { System.out.println("ဂဏန်းသင်္ချာတန်ဖိုး ခြွင်းချက်"); }
        try { throw new IllegalArgumentException("잘못된 အချက်များ 한글😀"); } catch (RuntimeException e) { System.out.println(e.getMessage()); }
        try { String s = null; s.length(); } catch (NullPointerException e) { System.out.println("빈 ကိုးကားချက်"); }
        try { int[] n = new int[1]; System.out.println(n[2]); } catch (IndexOutOfBoundsException e) { System.out.println("အခင်းအကျင်းတန်ဖိုး ဖြတ်နယ်ပယ်"); }
        try { Integer.parseInt("2147483648"); } catch (NumberFormatException e) { System.out.println("ကိန်းပြည့် ဖြတ်နယ်ပယ်"); }
        try { Object x = "글"; Integer n = (Integer)x; } catch (ClassCastException e) { System.out.println("အမျိုးပုံစံတန်ဖိုး တန်ဖိုးပြောင်းလဲ"); }
        try { java.io.FileInputStream f = new java.io.FileInputStream("없는파일"); } catch (java.io.IOException e) { System.out.println("ဖိုင် ခြွင်းချက်"); }
        System.out.println("ခြွင်းချက် လုပ်ငန်းစဉ်တန်ဖိုးအချက် ဖြစ်သောအပြည့်အစုံ");
    }
}
