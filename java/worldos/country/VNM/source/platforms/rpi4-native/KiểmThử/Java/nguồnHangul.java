// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class nguồnHangul {
    public static void main(String[] cácĐốiSố) throws tiếngViệt.tựThân.NgoạiLệĐầuRaĐầuVào {
        tiếngViệt.tựThân.ĐầuRa.ghiDòng("tựThân 컴파일러와 tiếngViệt thưViện");
        int sốLượngKýTự = tiếngViệt.tựThân.KýTự.sốLượngĐiểmMã("한글😀");
        tiếngViệt.tựThân.ĐầuRa.ghiSố(sốLượngKýTự);
        tiếngViệt.tựThân.Tệp.ghi("한글자료.txt", "tựThân giáTrịNhân 안에서 저장한 한글😀");
        tiếngViệt.tựThân.ĐầuRa.ghiDòng(tiếngViệt.tựThân.Tệp.đọc("한글자료.txt"));
    }
}
