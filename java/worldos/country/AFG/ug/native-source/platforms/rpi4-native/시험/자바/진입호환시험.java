// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 표준 main을 가진 기존 코드의 비공개 보조 함수를 진입점으로 고르지 않는다. */
public class 진입호환시험 {
    private static void ئىجرا_قىل_2() { System.out.println("보조 فۇنكسىيە_قىممىتى 호출"); }
    public static void main(String[] ئۆزگەرگۈچىلەر) {
        ئىجرا_قىل_2();
        System.out.println("표준 كىرگۈزۈش_نوقتا 유지");
    }
}
