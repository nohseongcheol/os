// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 파일예제 {
    public static void Стартиране() throws Български.자체.В_И_изключение {
        Български.자체.Файл.Писане("java.txt", "JAVA Файл: bg 😀\n");
        Български.자체.Изход.Писане(Български.자체.Файл.Четене("java.txt"));
    }
}
