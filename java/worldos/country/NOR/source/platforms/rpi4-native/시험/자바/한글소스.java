// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 한글소스 {
    public static void main(String[] Argumenter) throws norsk.eget.I_U_unntak {
        norsk.eget.Utgang.skrive_linje("eget 컴파일러와 norsk bibliotek");
        int tegn_ANTALL = norsk.eget.문자.tegnkode_ANTALL("한글😀");
        norsk.eget.Utgang.skrive_nummer(tegn_ANTALL);
        norsk.eget.Fil.Skriv("한글자료.txt", "eget kjerne_VERDI 안에서 저장한 한글😀");
        norsk.eget.Utgang.skrive_linje(norsk.eget.Fil.Les("한글자료.txt"));
    }
}
