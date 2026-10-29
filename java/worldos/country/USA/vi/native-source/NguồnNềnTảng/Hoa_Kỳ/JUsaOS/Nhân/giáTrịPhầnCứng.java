// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Hoa_Kỳ.JUsaOS.Nhân;

/** Ranh giới duy nhất giữa nhân do Java quản lý và mã riêng của CPU. */
public interface giáTrịPhầnCứng {
    void đầuRaNốiTiếp(String giáTrịNộiDung);

    int đọcByteCổng(int sốCổngPhầnCứng);

    void ghiByteCổng(int sốCổngPhầnCứng, int giáTrị);

    void cPUDừngHẳn();
}

