// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package tiếngViệt.tựThân;

/** Kiểm tra các điều kiện mong đợi trong ví dụ và phép thử. */
public final class CácPhépKiểmTra {
    private CácPhépKiểmTra() {}
    public static void đòiHỏi(boolean điềuKiện, String giáTrịNguyênNhân) {
        if (!điềuKiện) throw new NgoạiLệĐốiSốKhôngHợpLệ(giáTrịNguyênNhân);
    }
}
