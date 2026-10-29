// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package tiếngViệt.tựThân;

/** Chuyển lỗi Java tiêu chuẩn tại ranh giới API tiếng Việt mà không đổi nghĩa mệnh đề catch tiêu chuẩn. */
final class chuyểnĐổiNgoạiLệ {
    private chuyểnĐổiNgoạiLệ() {}
    public static NgoạiLệĐầuRaĐầuVào đầuRaĐầuVào(java.io.IOException lỗi) {
        if (lỗi instanceof NgoạiLệĐầuRaĐầuVào) return (NgoạiLệĐầuRaĐầuVào)lỗi;
        if (lỗi instanceof java.net.SocketTimeoutException) return new NgoạiLệHếtGiờChờ("Đã hết thời gian chờ liên lạc.");
        if (lỗi instanceof java.net.UnknownHostException) return new NgoạiLệTraCứuĐịaChỉ("Không thể phân giải địa chỉ. Hiện hãy dùng địa chỉ IPv4 dạng số.");
        if (lỗi instanceof java.io.FileNotFoundException) return new NgoạiLệTệpThiếu("Không thể mở tệp.");
        if (lỗi instanceof java.net.SocketException) return new NgoạiLệTruyềnThông("Thao tác kết nối thất bại: " + lỗi.getMessage());
        return new NgoạiLệĐầuRaĐầuVào("Thao tác vào ra thất bại: " + lỗi.getMessage());
    }
    public static RuntimeException thựcThiLệnh(RuntimeException lỗi) {
        if (lỗi instanceof java.lang.NumberFormatException) return new SựThấtBạiĐịnhDạngSố("Hãy kiểm tra định dạng và phạm vi của số.");
        if (lỗi instanceof java.lang.IllegalArgumentException) return new NgoạiLệĐốiSốKhôngHợpLệ("Hãy kiểm tra giá trị và phạm vi của đối số.");
        if (lỗi instanceof java.lang.ArrayIndexOutOfBoundsException) return new NgoạiLệCácCậnMảng("Chỉ số vượt phạm vi mảng.");
        if (lỗi instanceof java.lang.StringIndexOutOfBoundsException) return new NgoạiLệCácCậnChuỗi("Chỉ số vượt phạm vi chuỗi.");
        if (lỗi instanceof java.lang.IndexOutOfBoundsException) return new NgoạiLệCácCận("Đã vượt phạm vi cho phép.");
        if (lỗi instanceof java.lang.NullPointerException) return new NgoạiLệThamChiếuRỗngThamChiếu("Tham chiếu rỗng.");
        return new NgoạiLệViệcThựcThi(lỗi.getMessage());
    }
}
