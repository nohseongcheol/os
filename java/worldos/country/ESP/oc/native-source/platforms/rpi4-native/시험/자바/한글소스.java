// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 한글소스 {
    public static void main(String[] 인수) throws 한국어.자체.입출력예외 {
        한국어.자체.Sortida.줄쓰기("자체 컴파일러와 한국어 라이브러리");
        int 글자수 = 한국어.자체.문자.코드포인트수("한글😀");
        한국어.자체.Sortida.수쓰기(글자수);
        한국어.자체.Fichièr.Escritura("한글자료.txt", "자체 커널 안에서 저장한 한글😀");
        한국어.자체.Sortida.줄쓰기(한국어.자체.Fichièr.Lectura("한글자료.txt"));
    }
}
