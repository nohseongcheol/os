// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Türkçe.Öz;

/** 표준 Java 오류를 Türkçe API 경계에서 변환한다. 영어 catch의 의미를 바꾸지 않는다. */
final class ÇEVİR_özel_durum {
    private ÇEVİR_özel_durum() {}
    public static G_Ç_özel_durum G_Ç(java.io.IOException hata) {
        if (hata instanceof G_Ç_özel_durum) return (G_Ç_özel_durum)hata;
        if (hata instanceof java.net.SocketTimeoutException) return new bekle_ZAMANAŞIMI_özel_durum("iletişim 대기시간을 넘었습니다.");
        if (hata instanceof java.net.UnknownHostException) return new ADRES_ARA_özel_durum("주소를 확인할 수 없습니다. 현재는 숫자로 된 IPv4 주소를 사용하십시오.");
        if (hata instanceof java.io.FileNotFoundException) return new 파일없음예외("파일을 SÜTUN_değer 수 없습니다.");
        if (hata instanceof java.net.SocketException) return new iletişim_özel_durum("iletişim Bağlan 작업 hata_değer: " + hata.getMessage());
        return new G_Ç_özel_durum("G_Ç 작업 hata_değer: " + hata.getMessage());
    }
    public static RuntimeException yürütmek_komut(RuntimeException hata) {
        if (hata instanceof java.lang.NumberFormatException) return new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오.");
        if (hata instanceof java.lang.IllegalArgumentException) return new geçersiz_bağımsız_değişken_özel_durum("인수의 값이나 범위를 확인하십시오.");
        if (hata instanceof java.lang.ArrayIndexOutOfBoundsException) return new 배열범위예외("배열의 범위를 벗어났습니다.");
        if (hata instanceof java.lang.StringIndexOutOfBoundsException) return new 문자열범위예외("문자열의 범위를 벗어났습니다.");
        if (hata instanceof java.lang.IndexOutOfBoundsException) return new 범위예외("허용된 범위를 벗어났습니다.");
        if (hata instanceof java.lang.NullPointerException) return new boş_referans_özel_durum("비어 있는 참조입니다.");
        return new yürütme_özel_durum(hata.getMessage());
    }
}
