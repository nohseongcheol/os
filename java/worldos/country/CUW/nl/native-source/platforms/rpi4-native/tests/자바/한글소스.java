// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 한글소스 {
    public static void main(String[] argumenten) throws Nederlands.Eigen.I_O_uitzondering {
        Nederlands.Eigen.tekstuitvoer.schrijven_lijn("Eigen 컴파일러와 Nederlands bibliotheek");
        int teken_AANTAL = Nederlands.Eigen.문자.codepoint_AANTAL("한글😀");
        Nederlands.Eigen.tekstuitvoer.schrijven_nummer(teken_AANTAL);
        Nederlands.Eigen.bestand.Schrijven("한글자료.txt", "Eigen kernel_WAARDE 안에서 저장한 한글😀");
        Nederlands.Eigen.tekstuitvoer.schrijven_lijn(Nederlands.Eigen.bestand.Lezen("한글자료.txt"));
    }
}
