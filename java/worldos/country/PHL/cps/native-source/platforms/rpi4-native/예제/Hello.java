// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class Hello {
    public static int square(int n) { return n * n; }
    public static void main(String[] args) {
        System.out.println("안녕하세요 · 日本語 · العربية · 😀");
        System.out.println("square=" + square(7));
        if (args.length > 0) System.out.println(args[0]);
    }
}
