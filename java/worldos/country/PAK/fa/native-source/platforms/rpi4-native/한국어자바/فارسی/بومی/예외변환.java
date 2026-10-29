// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package فارسی.بومی;

/** 표준 Java 오류를 فارسی API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class 예외변환 {
    private 예외변환() {}
    public static ورودی_خروجی_استثنا ورودی_خروجی(java.io.IOException خطا) {
        if (خطا instanceof ورودی_خروجی_استثنا) return (ورودی_خروجی_استثنا)خطا;
        if (خطا instanceof java.net.SocketTimeoutException) return new منتظر_ماندن_پایان_مهلت_زمانی_استثنا("통신 대기시간을 넘었습니다.");
        if (خطا instanceof java.net.UnknownHostException) return new آدرس_جستجو_استثنا("주소를 확인할 수 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (خطا instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 ستون_مقدار 수 없습니다.");
        if (خطا instanceof java.net.SocketException) return new 통신예외("통신 اتصال 작업 عدم_موفقیت_مقدار: " + خطا.getMessage());
        return new ورودی_خروجی_استثنا("ورودی_خروجی 작업 عدم_موفقیت_مقدار: " + خطا.getMessage());
    }
    public static RuntimeException اجرا_فرمان(RuntimeException خطا) {
        if (خطا instanceof java.lang.NumberFormatException) return new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오.");
        if (خطا instanceof java.lang.IllegalArgumentException) return new بی_اعتبار_آرگومان_استثنا("인수의 값이나 범위를 확인하십시오.");
        if (خطا instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (خطا instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (خطا instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (خطا instanceof java.lang.NullPointerException) return new تهی_مرجع_استثنا("비어 있는 참조입니다.");
        return new 실행예외(خطا.getMessage());
    }
}
