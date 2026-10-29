// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ไทย.เอง;

/** 표준 Java 오류를 ไทย API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class แปลง_ข้อยกเว้น {
    private แปลง_ข้อยกเว้น() {}
    public static รับเข้า_ส่งออก_ข้อยกเว้น รับเข้า_ส่งออก(java.io.IOException ข้อผิดพลาด) {
        if (ข้อผิดพลาด instanceof รับเข้า_ส่งออก_ข้อยกเว้น) return (รับเข้า_ส่งออก_ข้อยกเว้น)ข้อผิดพลาด;
        if (ข้อผิดพลาด instanceof java.net.SocketTimeoutException) return new 대기시간초과예외("통신 대기시간을 넘었습니다.");
        if (ข้อผิดพลาด instanceof java.net.UnknownHostException) return new อีเมล_การค้นหา_ข้อยกเว้น("주소를 확인할 หมายเลข 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (ข้อผิดพลาด instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 คอลัมน์_ค่า หมายเลข 없습니다.");
        if (ข้อผิดพลาด instanceof java.net.SocketException) return new 통신예외("통신 เชื่อมต่อ 작업 ความล้มเหลว_ค่า: " + ข้อผิดพลาด.getMessage());
        return new รับเข้า_ส่งออก_ข้อยกเว้น("รับเข้า_ส่งออก 작업 ความล้มเหลว_ค่า: " + ข้อผิดพลาด.getMessage());
    }
    public static RuntimeException ดําเนินการ_คําสั่ง(RuntimeException ข้อผิดพลาด) {
        if (ข้อผิดพลาด instanceof java.lang.NumberFormatException) return new หมายเลข_รูปแบบ_ความล้มเหลว("숫자의 형식이나 범위를 확인하십시오.");
        if (ข้อผิดพลาด instanceof java.lang.IllegalArgumentException) return new ไม่ถูกต้อง_อาร์กิวเมนต์_ข้อยกเว้น("인수의 값이나 범위를 확인하십시오.");
        if (ข้อผิดพลาด instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (ข้อผิดพลาด instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (ข้อผิดพลาด instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (ข้อผิดพลาด instanceof java.lang.NullPointerException) return new การอ้างอิงที่ว่าง_ข้อยกเว้น("비어 있는 참조입니다.");
        return new 실행예외(ข้อผิดพลาด.getMessage());
    }
}
