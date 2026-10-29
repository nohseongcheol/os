// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 예외시험 {
    static int 나누기(int n) { return 8 / n; }
    static int 마무리() { try { return 나누기(0); } finally { System.out.println("마무리"); } }
    public static void main(String[] a) {
        try { 마무리(); } catch (ArithmeticException e) { System.out.println("산술 예외"); }
        try { throw new IllegalArgumentException("잘못된 විස්තාරක 한글😀"); } catch (RuntimeException e) { System.out.println(e.getMessage()); }
        try { String s = null; s.length(); } catch (NullPointerException e) { System.out.println("빈 පරිශීලනය"); }
        try { int[] n = new int[1]; System.out.println(n[2]); } catch (IndexOutOfBoundsException e) { System.out.println("ආරා_ව_අගය පසුර"); }
        try { Integer.parseInt("2147483648"); } catch (NumberFormatException e) { System.out.println("පූර්ණාංකය පසුර"); }
        try { Object x = "පෙළ"; Integer n = (Integer)x; } catch (ClassCastException e) { System.out.println("ටයිප්_කරන්න_අගය 변환"); }
        try { java.io.FileInputStream f = new java.io.FileInputStream("없는파일"); } catch (java.io.IOException e) { System.out.println("ගොනු 예외"); }
        System.out.println("예외 ක්_රියාවලිය_අගය_පිවිසුම 완료");
    }
}
