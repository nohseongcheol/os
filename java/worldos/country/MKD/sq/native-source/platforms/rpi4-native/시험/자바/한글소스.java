// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 한글소스 {
    public static void main(String[] Argumente) throws 한국어.자체.I_O_përjashtim {
        한국어.자체.출력.shkruaj_linjë("자체 컴파일러와 한국어 bibliotekë");
        int karakter_COUNT = 한국어.자체.문자.kodi_i_karakterit_COUNT("한글😀");
        한국어.자체.출력.수쓰기(karakter_COUNT);
        한국어.자체.Kartelë.Shkrimi("한글자료.txt", "자체 bërthamë_VALUE 안에서 저장한 한글😀");
        한국어.자체.출력.shkruaj_linjë(한국어.자체.Kartelë.Leximi("한글자료.txt"));
    }
}
