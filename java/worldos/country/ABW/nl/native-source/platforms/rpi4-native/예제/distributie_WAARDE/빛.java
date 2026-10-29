// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 빛 {
    public static void main(String[] argumenten) throws Exception {
        int SOM_WAARDE = 0;
        int nummer = 1;
        while (nummer <= 10) {
            SOM_WAARDE = SOM_WAARDE + nummer;
            nummer = nummer + 1;
        }
        Nederlands.Eigen.tekstuitvoer.schrijven_nummer(SOM_WAARDE);
        Nederlands.Eigen.bestand.Schrijven("aot.txt", "한글 AOT bestand 😀");
        Nederlands.Eigen.tekstuitvoer.schrijven_lijn(Nederlands.Eigen.bestand.Lezen("aot.txt"));
    }
}
