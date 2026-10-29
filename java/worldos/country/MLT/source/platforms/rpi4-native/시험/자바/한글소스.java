// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 한글소스 {
    public static void main(String[] 인수) throws Malti.자체.입출력예외 {
        Malti.자체.출력.kiteb_linja("자체 컴파일러와 Malti librerija");
        int karattru_COUNT = Malti.자체.문자.kodiċi_tal_karattru_COUNT("한글😀");
        Malti.자체.출력.수쓰기(karattru_COUNT);
        Malti.자체.fajl.kiteb("한글자료.txt", "자체 kernel_VALUE 안에서 저장한 한글😀");
        Malti.자체.출력.kiteb_linja(Malti.자체.fajl.읽기("한글자료.txt"));
    }
}
