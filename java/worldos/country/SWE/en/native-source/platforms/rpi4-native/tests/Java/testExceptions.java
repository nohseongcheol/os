// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class testExceptions {
    static int divideValues(int n) { return 8 / n; }
    static int finalizeValue() { try { return divideValues(0); } finally { System.out.println("finalizeValue"); } }
    public static void main(String[] a) {
        try { finalizeValue(); } catch (ArithmeticException e) { System.out.println("arithmeticValue exception"); }
        try { throw new IllegalArgumentException("잘못된 arguments 한글😀"); } catch (RuntimeException e) { System.out.println(e.getMessage()); }
        try { String s = null; s.length(); } catch (NullPointerException e) { System.out.println("빈 reference"); }
        try { int[] n = new int[1]; System.out.println(n[2]); } catch (IndexOutOfBoundsException e) { System.out.println("arrayValue clip"); }
        try { Integer.parseInt("2147483648"); } catch (NumberFormatException e) { System.out.println("Integer clip"); }
        try { Object x = "text"; Integer n = (Integer)x; } catch (ClassCastException e) { System.out.println("typeValue convertValue"); }
        try { java.io.FileInputStream f = new java.io.FileInputStream("없는파일"); } catch (java.io.IOException e) { System.out.println("file exception"); }
        System.out.println("exception processValueEntry isComplete");
    }
}
