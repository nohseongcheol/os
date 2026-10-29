// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 표준 main을 가진 기존 코드의 비공개 보조 함수를 진입점으로 고르지 않는다. */
public class καταχώρηση_συμβατότητα_δοκιμή {
    private static void Εκτέλεση_2() { System.out.println("보조 συνάρτηση_τιμή 호출"); }
    public static void main(String[] Παράμετροι) {
        Εκτέλεση_2();
        System.out.println("표준 σημείο_εισόδου 유지");
    }
}
