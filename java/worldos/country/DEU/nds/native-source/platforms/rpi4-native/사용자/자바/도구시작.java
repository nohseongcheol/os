// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 도구시작 {
    public static int Starte() {
        return 사용자.도구번호() == 0 ? 자바컴파일러.Starte() : 자바가상기계.Starte();
    }
}
