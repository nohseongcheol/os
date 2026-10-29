// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package русский.свой;

/** 표준 Java 오류를 русский API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class ПРЕОБР_исключение {
    private ПРЕОБР_исключение() {}
    public static входные_данные_выход_исключение входные_данные_выход(java.io.IOException ошибка) {
        if (ошибка instanceof входные_данные_выход_исключение) return (входные_данные_выход_исключение)ошибка;
        if (ошибка instanceof java.net.SocketTimeoutException) return new минутку_ТАЙМАУТ_исключение("коммуникация 대기시간을 넘었습니다.");
        if (ошибка instanceof java.net.UnknownHostException) return new АДРЕС_Поиск_исключение("주소를 확인할 수 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (ошибка instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 СТОЛБЕЦ_ЗНАЧЕН 수 없습니다.");
        if (ошибка instanceof java.net.SocketException) return new коммуникация_исключение("коммуникация Подключить 작업 сбой_ЗНАЧЕН: " + ошибка.getMessage());
        return new входные_данные_выход_исключение("входные_данные_выход 작업 сбой_ЗНАЧЕН: " + ошибка.getMessage());
    }
    public static RuntimeException 실행(RuntimeException ошибка) {
        if (ошибка instanceof java.lang.NumberFormatException) return new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오.");
        if (ошибка instanceof java.lang.IllegalArgumentException) return new неверный_аргумент_исключение("인수의 값이나 범위를 확인하십시오.");
        if (ошибка instanceof java.lang.ArrayIndexOutOfBoundsException) return new границы_массива_исключение("배열의 범위를 벗어났습니다.");
        if (ошибка instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (ошибка instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (ошибка instanceof java.lang.NullPointerException) return new пустая_ссылка_исключение("비어 있는 참조입니다.");
        return new выполнение_исключение(ошибка.getMessage());
    }
}
