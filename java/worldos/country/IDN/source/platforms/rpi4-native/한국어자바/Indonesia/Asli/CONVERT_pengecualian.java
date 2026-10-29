// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Indonesia.Asli;

/** 표준 Java 오류를 Indonesia API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class CONVERT_pengecualian {
    private CONVERT_pengecualian() {}
    public static I_O_pengecualian I_O(java.io.IOException galat) {
        if (galat instanceof I_O_pengecualian) return (I_O_pengecualian)galat;
        if (galat instanceof java.net.SocketTimeoutException) return new tunggu_TIMEOUT_pengecualian("komunikasi 대기시간을 넘었습니다.");
        if (galat instanceof java.net.UnknownHostException) return new surel_LOOKUP_pengecualian("주소를 확인할 수 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (galat instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 kolom_VALUE 수 없습니다.");
        if (galat instanceof java.net.SocketException) return new komunikasi_pengecualian("komunikasi Sambung 작업 kegagalan_VALUE: " + galat.getMessage());
        return new I_O_pengecualian("I_O 작업 kegagalan_VALUE: " + galat.getMessage());
    }
    public static RuntimeException Jalankan_perintah(RuntimeException galat) {
        if (galat instanceof java.lang.NumberFormatException) return new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오.");
        if (galat instanceof java.lang.IllegalArgumentException) return new tidak_sahih_argumen_pengecualian("인수의 값이나 범위를 확인하십시오.");
        if (galat instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (galat instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (galat instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (galat instanceof java.lang.NullPointerException) return new NULL_Referensi_pengecualian("비어 있는 참조입니다.");
        return new 실행예외(galat.getMessage());
    }
}
