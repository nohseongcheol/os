// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros пространство_пользователя ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class пространство_пользователя {
    public static native int открыть_файл_дескриптор(int[] файл_ввод_имя, int открыть_Настройки);
    public static native int 파일한바이트읽기(int файл_дескриптор);
    public static native int 파일한바이트쓰기(int файл_дескриптор, int байт_ЗНАЧЕН);
    public static native int Close_файл_дескриптор(int файл_дескриптор);
    public static native int фиксация_Файлы(int файл_дескриптор);
    public static native int чтение_файл(int[] Название, int[] данные);
    public static native int запись_знак_ЗНАЧЕН(int 문자);
    public static native int запись_файл(int[] Название, int[] данные, int длина_ЗНАЧЕН);
    public static native int Запись(String контент_ЗНАЧЕН);
    public static native int 인수개수();
    public static native String аргументы(int ИНДЕКС);
    public static native int выполнение_Полномочие();
    public static native int открыть_сеть(int локальный_порт);
    public static native int написать_данные(int маркер_ЗНАЧЕН, int АДРЕС, int цель_порт, int[] данные, int длина_ЗНАЧЕН);
    public static native int получить_данные(int маркер_ЗНАЧЕН, int[] данные, int 제한밀리초);
    public static native int Close_сеть(int маркер_ЗНАЧЕН);
    public static native int 내주소();
    public static native int 보낸주소(int маркер_ЗНАЧЕН);
    public static native int 보낸창구(int маркер_ЗНАЧЕН);
}
