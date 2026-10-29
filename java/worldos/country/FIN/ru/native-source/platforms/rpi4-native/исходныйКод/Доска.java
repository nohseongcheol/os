// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 компьютер_5eb260fa граница_ЗНАЧЕН. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class Доска {
    public static native int читатьПиксельЭкрана(int 가로, int Вертикаль_позиция);
    public static native void записатьПиксельЭкрана(int 가로, int Вертикаль_позиция, int 색);
    public static native int удаленное_управление(int Вид_ЗНАЧЕН, int Действие);
    public static native void 원격명령끝(int Состояние_ЗНАЧЕН);
    public static native void удаленный_минутку(int Состояние_ЗНАЧЕН);
    public static native void 직렬쓰기(int ЗНАЧЕН);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int ЦП_привилегия_уровень();
    public static native int Подготовить_экран();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int Вертикаль_позиция, int 색);
    public static native void ДОХОД_ЦП();
    public static native int Create_дело(int ИНДЕКС);
    public static native int дело_Состояние(int ИНДЕКС);
    public static native void Остановить(int Состояние_ЗНАЧЕН);
    public static native int 씨플러스시험();
    public static native int выполнить_пользователь_программа(int ИНДЕКС);
    public static native int чек_пользователь_программа();
    public static native int 인수준비(int товар_СЧЁТ);
    public static native int Выполнить_пользователь_файл();
    public static native int 리눅스파일실행();
    public static native int аргумент_байт(int ИНДЕКС, int позиция, int ЗНАЧЕН);
    public static native int терминал(int Действие);
    public static native int управление_пользователь_программа(int Действие);
    public static native void 입출력전환(int Действие);
    public static native int передача_файла_сервис(int Действие);
    public static native int сеть_статус(int ввод_ЗНАЧЕН, int ИНДЕКС);
    public static native int сеть_Настройки(int Действие, int АДРЕС, int маска_ЗНАЧЕН, int шлюз_ЗНАЧЕН);
    public static native int написать_ответ(int АДРЕС, int заказ_ЗНАЧЕН);
    public static native int чтение_ответ(int ввод_ЗНАЧЕН);
    public static native int запрос_система(int ввод_ЗНАЧЕН, int ИНДЕКС);
    public static native void 전원끄기();
}
