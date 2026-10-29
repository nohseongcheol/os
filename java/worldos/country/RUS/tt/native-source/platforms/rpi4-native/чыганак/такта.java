// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 машина 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class такта {
    public static native int 표시화소읽기(int 가로, int Вертикаль_урнаштыру);
    public static native void язу_дисплей_нокта(int 가로, int Вертикаль_урнаштыру, int 색);
    public static native int читтән_идарә(int 종류, int Гамәл);
    public static native void тәмамлау_читтәге_команда(int халәт_VALUE);
    public static native void 원격대기(int халәт_VALUE);
    public static native void 직렬쓰기(int VALUE);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int процессор_рөхсәтләр_дәрәҗә();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int Вертикаль_урнаштыру, int 색);
    public static native void YIELD_процессор();
    public static native int Төзү_мәсьәлә(int INDEX);
    public static native int мәсьәлә_халәт(int INDEX);
    public static native void туктату(int халәт_VALUE);
    public static native int 씨플러스시험();
    public static native int эшләтү_кулланучы_кушымта(int INDEX);
    public static native int чек_кулланучы_кушымта();
    public static native int 인수준비(int элемент_COUNT);
    public static native int үтәргә_кулланучы_файл();
    public static native int 리눅스파일실행();
    public static native int аргумент_байт(int INDEX, int урнаштыру, int VALUE);
    public static native int Терминал(int Гамәл);
    public static native int идарә_кулланучы_кушымта(int Гамәл);
    public static native void 입출력전환(int Гамәл);
    public static native int файл_күчерү_хезмәт(int Гамәл);
    public static native int Челтәр_халәт(int кертү_VALUE, int INDEX);
    public static native int Челтәр_Параметрлар(int Гамәл, int адрес, int үрнәк_VALUE, int шлюз_VALUE);
    public static native int 응답보내기(int адрес, int тәртипкә_салу_VALUE);
    public static native int 응답읽기(int кертү_VALUE);
    public static native int таләп_система(int кертү_VALUE, int INDEX);
    public static native void 전원끄기();
}
