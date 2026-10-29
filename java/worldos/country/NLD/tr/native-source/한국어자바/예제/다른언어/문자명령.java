// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Türkçe.자바.문자;

/** 다른 언어가 표준 출력으로 결과를 받을 수 있는 작은 Java giriş_noktası. */
public final class 문자명령 {
    public static void main(String[] bağımsız_değişkenler) {
        if (bağımsız_değişkenler.length != 1) {
            System.err.println("사용법: 문자명령 dize_değer");
            System.exit(2);
        }
        System.out.println(문자.kod_öğesi_BAĞ_DEĞ_SAY(bağımsız_değişkenler[0]));
    }
}
