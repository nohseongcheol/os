// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 инструменты 전용 SVC Подключить. 기존 x86 инструменты 원문을 함께 빌드한다. */
public final class пространство_пользователя {
    public static native int открыть_файл_дескриптор(int[] Название, int Настройки);
    public static native int 파일한바이트읽기(int дескриптор_ввод);
    public static native int 파일한바이트쓰기(int дескриптор_ввод, int ЗНАЧЕН);
    public static native int Close_файл_дескриптор(int дескриптор_ввод);
    public static native int чтение_файл(int[] Название, int[] данные);
    public static native int запись_файл(int[] Название, int[] данные, int длина_ЗНАЧЕН);
    public static native int Запись(String текст);
    public static native int запись_знак_ЗНАЧЕН(int ЗНАЧЕН);
    public static native int 인수개수();
    public static native String аргументы(int ИНДЕКС);
    public static native int 도구번호();
    public static native int экран_контакт(int Действие, int ИНДЕКС, int 가, int СЕКУНДЫ_операнд, int 다, int 라);
    public static native int экран_SMS(int ИНДЕКС, int[] текст, int длина_ЗНАЧЕН);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int поток_управление(int Действие, int дескриптор_ввод, int ЗНАЧЕН);
    public static native int Connect_поток(int дескриптор_ввод, int АДРЕС, int порт_ЗНАЧЕН);
    public static native int открыть_сеть(int порт_ЗНАЧЕН);
    public static native int написать_сеть(int дескриптор_ввод, int АДРЕС, int порт_ЗНАЧЕН, int[] данные, int длина_ЗНАЧЕН);
    public static native int получить_сеть(int дескриптор_ввод, int[] данные, int длина_ЗНАЧЕН);
    public static native int сеть_порт(int дескриптор_ввод);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int прямоугольник(int 가로, int Вертикаль_позиция, int 폭, int 높이, int 색);
}
