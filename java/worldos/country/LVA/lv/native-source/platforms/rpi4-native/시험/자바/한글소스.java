// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 한글소스 {
    public static void main(String[] Parametri) throws Latviešu.savs.ievadizvade_izņēmums {
        Latviešu.savs.Izvade.rakstīšana_līnija("savs 컴파일러와 Latviešu bibliotēka");
        int rakstzīme_COUNT = Latviešu.savs.문자.koda_punkts_COUNT("한글😀");
        Latviešu.savs.Izvade.rakstīšana_numurs(rakstzīme_COUNT);
        Latviešu.savs.Fails.Rakstīt("한글자료.txt", "savs kodols_VALUE 안에서 저장한 한글😀");
        Latviešu.savs.Izvade.rakstīšana_līnija(Latviešu.savs.Fails.Lasīt("한글자료.txt"));
    }
}
