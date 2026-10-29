// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ελληνικά.ίδιο;

/** 표준 Java 오류를 ελληνικά API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class μετατρέπω_εξαίρεση {
    private μετατρέπω_εξαίρεση() {}
    public static είσοδος_έξοδος_εξαίρεση είσοδος_έξοδος(java.io.IOException ΣΦΑΛΜΑ) {
        if (ΣΦΑΛΜΑ instanceof είσοδος_έξοδος_εξαίρεση) return (είσοδος_έξοδος_εξαίρεση)ΣΦΑΛΜΑ;
        if (ΣΦΑΛΜΑ instanceof java.net.SocketTimeoutException) return new περίμενε_ΤΕΛΟΣ_ΧΡΟΝΟΥ_εξαίρεση("통신 대기시간을 넘었습니다.");
        if (ΣΦΑΛΜΑ instanceof java.net.UnknownHostException) return new διεύθυνση_Αναζήτηση_εξαίρεση("주소를 확인할 수 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (ΣΦΑΛΜΑ instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 στήλη_τιμή 수 없습니다.");
        if (ΣΦΑΛΜΑ instanceof java.net.SocketException) return new 통신예외("통신 Σύνδεση 작업 αποτυχία_τιμή: " + ΣΦΑΛΜΑ.getMessage());
        return new είσοδος_έξοδος_εξαίρεση("είσοδος_έξοδος 작업 αποτυχία_τιμή: " + ΣΦΑΛΜΑ.getMessage());
    }
    public static RuntimeException εκτελώ_εντολή(RuntimeException ΣΦΑΛΜΑ) {
        if (ΣΦΑΛΜΑ instanceof java.lang.NumberFormatException) return new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오.");
        if (ΣΦΑΛΜΑ instanceof java.lang.IllegalArgumentException) return new άκυρος_όρισμα_εξαίρεση("인수의 값이나 범위를 확인하십시오.");
        if (ΣΦΑΛΜΑ instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (ΣΦΑΛΜΑ instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (ΣΦΑΛΜΑ instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (ΣΦΑΛΜΑ instanceof java.lang.NullPointerException) return new αναφορά_null_εξαίρεση("비어 있는 참조입니다.");
        return new εκτέλεση_εξαίρεση(ΣΦΑΛΜΑ.getMessage());
    }
}
