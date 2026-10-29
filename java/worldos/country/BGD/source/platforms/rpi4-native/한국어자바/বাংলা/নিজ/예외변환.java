// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package বাংলা.নিজ;

/** 표준 Java 오류를 বাংলা API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class 예외변환 {
    private 예외변환() {}
    public static ইনপুট_আউটপুট_ব্যতিক্রম ইনপুট_আউটপুট(java.io.IOException ত্রুটি) {
        if (ত্রুটি instanceof ইনপুট_আউটপুট_ব্যতিক্রম) return (ইনপুট_আউটপুট_ব্যতিক্রম)ত্রুটি;
        if (ত্রুটি instanceof java.net.SocketTimeoutException) return new অপেক্ষা_টাইমআউট_ব্যতিক্রম("통신 대기시간을 넘었습니다.");
        if (ত্রুটি instanceof java.net.UnknownHostException) return new ইমেইল_লুকআপ_ব্যতিক্রম("주소를 확인할 수 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (ত্রুটি instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 কলাম_মান 수 없습니다.");
        if (ত্রুটি instanceof java.net.SocketException) return new 통신예외("통신 সংযোগ_স্থাপনা 작업 বিফলতা_মান: " + ত্রুটি.getMessage());
        return new ইনপুট_আউটপুট_ব্যতিক্রম("ইনপুট_আউটপুট 작업 বিফলতা_মান: " + ত্রুটি.getMessage());
    }
    public static RuntimeException কার্যকর_করুন_আদেশ(RuntimeException ত্রুটি) {
        if (ত্রুটি instanceof java.lang.NumberFormatException) return new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오.");
        if (ত্রুটি instanceof java.lang.IllegalArgumentException) return new অবৈধ_যুক্তি_ব্যতিক্রম("인수의 값이나 범위를 확인하십시오.");
        if (ত্রুটি instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (ত্রুটি instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (ত্রুটি instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (ত্রুটি instanceof java.lang.NullPointerException) return new নাল_প্রসঙ্গ_ব্যতিক্রম("비어 있는 참조입니다.");
        return new 실행예외(ত্রুটি.getMessage());
    }
}
