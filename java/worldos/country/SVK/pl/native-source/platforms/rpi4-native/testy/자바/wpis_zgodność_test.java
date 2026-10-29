// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 표준 main을 가진 기존 코드의 비공개 보조 함수를 진입점으로 고르지 않는다. */
public class wpis_zgodność_test {
    private static void Uruchom_2() { System.out.println("보조 FUNKCJA_WARTOŚĆ 호출"); }
    public static void main(String[] argumenty) {
        Uruchom_2();
        System.out.println("표준 punkt_wejścia 유지");
    }
}
