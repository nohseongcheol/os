// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 빛 {
    public static void main(String[] Параметри) throws Exception {
        int 합 = 0;
        int 수 = 1;
        while (수 <= 10) {
            합 = 합 + 수;
            수 = 수 + 1;
        }
        Български.자체.Изход.수쓰기(합);
        Български.자체.Файл.Писане("aot.txt", "한글 AOT Файл 😀");
        Български.자체.Изход.записване_ред(Български.자체.Файл.Четене("aot.txt"));
    }
}
