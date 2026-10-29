// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 파일예제 {
    public static void 시작() throws 한국어.자체.입출력예외 {
        한국어.자체.파일.쓰기("java.txt", "JAVA 파일: nd 😀\n");
        한국어.자체.출력.쓰기(한국어.자체.파일.읽기("java.txt"));
    }
}
