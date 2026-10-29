// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 표준 main을 가진 기존 코드의 비공개 보조 함수를 진입점으로 고르지 않는다. */
public class 진입호환시험 {
    private static void запустити() { System.out.println("보조 функція_значення 호출"); }
    public static void main(String[] аргументи) {
        запустити();
        System.out.println("표준 запис_бал 유지");
    }
}
