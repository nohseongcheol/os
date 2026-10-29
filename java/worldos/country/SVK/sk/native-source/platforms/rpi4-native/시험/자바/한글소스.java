// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 한글소스 {
    public static void main(String[] Argumenty) throws Slovenský.vlastné.vstup_a_výstup_výnimka {
        Slovenský.vlastné.Výstup.zapísať_linka("vlastné 컴파일러와 Slovenský knižnica");
        int znak_COUNT = Slovenský.vlastné.문자.bod_kódu_COUNT("한글😀");
        Slovenský.vlastné.Výstup.수쓰기(znak_COUNT);
        Slovenský.vlastné.Súbor.Zápis("한글자료.txt", "vlastné jadro_VALUE 안에서 저장한 한글😀");
        Slovenský.vlastné.Výstup.zapísať_linka(Slovenský.vlastné.Súbor.Čítanie("한글자료.txt"));
    }
}
