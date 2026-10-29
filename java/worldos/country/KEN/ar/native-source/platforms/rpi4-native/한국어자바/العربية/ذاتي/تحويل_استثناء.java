// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package العربية.ذاتي;

/** 표준 Java 오류를 العربية API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class تحويل_استثناء {
    private تحويل_استثناء() {}
    public static إدخال_إخراج_استثناء إدخال_إخراج(java.io.IOException خطأ) {
        if (خطأ instanceof إدخال_إخراج_استثناء) return (إدخال_إخراج_استثناء)خطأ;
        if (خطأ instanceof java.net.SocketTimeoutException) return new 대기시간초과예외("통신 대기시간을 넘었습니다.");
        if (خطأ instanceof java.net.UnknownHostException) return new عنوان_البحث_استثناء("주소를 확인할 رقم 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (خطأ instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 عمود_قيمة رقم 없습니다.");
        if (خطأ instanceof java.net.SocketException) return new 통신예외("통신 اتصال 작업 فشل_قيمة: " + خطأ.getMessage());
        return new إدخال_إخراج_استثناء("إدخال_إخراج 작업 فشل_قيمة: " + خطأ.getMessage());
    }
    public static RuntimeException ينفذ_أمر(RuntimeException خطأ) {
        if (خطأ instanceof java.lang.NumberFormatException) return new رقم_ينسق_فشل("숫자의 형식이나 범위를 확인하십시오.");
        if (خطأ instanceof java.lang.IllegalArgumentException) return new غير_صالح_وسيطة_استثناء("인수의 값이나 범위를 확인하십시오.");
        if (خطأ instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (خطأ instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (خطأ instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (خطأ instanceof java.lang.NullPointerException) return new مرجع_فارغ_استثناء("비어 있는 참조입니다.");
        return new 실행예외(خطأ.getMessage());
    }
}
