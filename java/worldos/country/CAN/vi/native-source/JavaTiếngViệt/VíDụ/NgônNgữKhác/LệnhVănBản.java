// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import tiếngViệt.Java.KýTự;

/** Điểm vào Java nhỏ để ngôn ngữ khác nhận kết quả qua đầu ra tiêu chuẩn. */
public final class LệnhVănBản {
    public static void main(String[] cácĐốiSố) {
        if (cácĐốiSố.length != 1) {
            System.err.println("사용법: LệnhVănBản ChuỗiKýTự");
            System.exit(2);
        }
        System.out.println(KýTự.sốLượngĐiểmMã(cácĐốiSố[0]));
    }
}
