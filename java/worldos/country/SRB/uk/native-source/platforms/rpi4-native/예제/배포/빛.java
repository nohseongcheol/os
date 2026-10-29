// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 빛 {
    public static void main(String[] аргументи) throws Exception {
        int 합 = 0;
        int 수 = 1;
        while (수 <= 10) {
            합 = 합 + 수;
            수 = 수 + 1;
        }
        українська.своє.Вивід.수쓰기(합);
        українська.своє.файл.Запис("aot.txt", "한글 AOT файл 😀");
        українська.своє.Вивід.записування_рядок(українська.своє.файл.Читання("aot.txt"));
    }
}
