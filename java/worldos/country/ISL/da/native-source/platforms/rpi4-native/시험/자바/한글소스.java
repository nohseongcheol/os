// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 한글소스 {
    public static void main(String[] Argumenter) throws Dansk.eget.I_O_undtagelse {
        Dansk.eget.Udgang.skrive_linje("eget 컴파일러와 Dansk bibliotek");
        int tegn_TÆL = Dansk.eget.문자.tegnkode_TÆL("한글😀");
        Dansk.eget.Udgang.skrive_tal(tegn_TÆL);
        Dansk.eget.Fil.Skrive("한글자료.txt", "eget kerne_VÆRDI 안에서 저장한 한글😀");
        Dansk.eget.Udgang.skrive_linje(Dansk.eget.Fil.Læse("한글자료.txt"));
    }
}
