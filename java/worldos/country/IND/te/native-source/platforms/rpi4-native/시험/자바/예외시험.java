// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 예외시험 {
    static int 나누기(int n) { return 8 / n; }
    static int 마무리() { try { return 나누기(0); } finally { System.out.println("마무리"); } }
    public static void main(String[] a) {
        try { 마무리(); } catch (ArithmeticException e) { System.out.println("산술 మినహాయింపు"); }
        try { throw new IllegalArgumentException("잘못된 인수 한글😀"); } catch (RuntimeException e) { System.out.println(e.getMessage()); }
        try { String s = null; s.length(); } catch (NullPointerException e) { System.out.println("빈 సూచన"); }
        try { int[] n = new int[1]; System.out.println(n[2]); } catch (IndexOutOfBoundsException e) { System.out.println("శ్రేణి_మూల్యం క్లిప్"); }
        try { Integer.parseInt("2147483648"); } catch (NumberFormatException e) { System.out.println("పూర్ణాంకం క్లిప్"); }
        try { Object x = "పాఠ్యము"; Integer n = (Integer)x; } catch (ClassCastException e) { System.out.println("టైప్_చేయండి_మూల్యం 변환"); }
        try { java.io.FileInputStream f = new java.io.FileInputStream("없는파일"); } catch (java.io.IOException e) { System.out.println("దస్త్రం మినహాయింపు"); }
        System.out.println("మినహాయింపు విధానం_మూల్యం_ప్రవేశం 완료");
    }
}
