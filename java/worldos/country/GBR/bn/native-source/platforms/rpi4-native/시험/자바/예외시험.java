// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 예외시험 {
    static int 나누기(int n) { return 8 / n; }
    static int 마무리() { try { return 나누기(0); } finally { System.out.println("마무리"); } }
    public static void main(String[] a) {
        try { 마무리(); } catch (ArithmeticException e) { System.out.println("산술 ব্যতিক্রম"); }
        try { throw new IllegalArgumentException("잘못된 আর্গুমেন্ট_তালিকা 한글😀"); } catch (RuntimeException e) { System.out.println(e.getMessage()); }
        try { String s = null; s.length(); } catch (NullPointerException e) { System.out.println("빈 প্রসঙ্গ"); }
        try { int[] n = new int[1]; System.out.println(n[2]); } catch (IndexOutOfBoundsException e) { System.out.println("অ্যারে_মান ক্লিপ"); }
        try { Integer.parseInt("2147483648"); } catch (NumberFormatException e) { System.out.println("পূর্ণসংখ্যা ক্লিপ"); }
        try { Object x = "পাঠ"; Integer n = (Integer)x; } catch (ClassCastException e) { System.out.println("টাইপ_করুন_মান 변환"); }
        try { java.io.FileInputStream f = new java.io.FileInputStream("없는파일"); } catch (java.io.IOException e) { System.out.println("নথির_নাম ব্যতিক্রম"); }
        System.out.println("ব্যতিক্রম প্রসেসর_মান_ভুক্তি 완료");
    }
}
