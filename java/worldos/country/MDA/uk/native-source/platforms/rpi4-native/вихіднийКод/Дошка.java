// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 комп_ютер 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class Дошка {
    public static native int 표시화소읽기(int 가로, int Вертикаль_посада);
    public static native void записування_дисплей_елемент_зображення(int 가로, int Вертикаль_посада, int 색);
    public static native int віддалене_керування(int 종류, int Дія);
    public static native void завершити_виклик_віддалений_команда(int Стан_значення);
    public static native void віддалений_хвилиноньку_панове(int Стан_значення);
    public static native void 직렬쓰기(int значення);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int ЦП_право_рівень();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int Вертикаль_посада, int 색);
    public static native void призупиняти_ЦП();
    public static native int Створення_справа(int індекс);
    public static native int справа_Стан(int індекс);
    public static native void Зупинити(int Стан_значення);
    public static native int 씨플러스시험();
    public static native int запускати_користувач_програма(int індекс);
    public static native int перевіряти_користувач_програма();
    public static native int 인수준비(int 개수);
    public static native int Виконати_користувач_Файл();
    public static native int 리눅스파일실행();
    public static native int аргумент_байт(int індекс, int позиція, int значення);
    public static native int термінал(int Дія);
    public static native int керування_користувач_програма(int Дія);
    public static native void 입출력전환(int Дія);
    public static native int передавання_файлу_служба(int Дія);
    public static native int мережа_стан(int запис_значення_962f286b, int індекс);
    public static native int мережа_Настройки(int Дія, int Адреса, int маска_значення, int шлюз_значення);
    public static native int надсилати_відгук(int Адреса, int порядок_значення);
    public static native int 응답읽기(int запис_значення_962f286b);
    public static native int запит_Система(int запис_значення_962f286b, int індекс);
    public static native void 전원끄기();
}
