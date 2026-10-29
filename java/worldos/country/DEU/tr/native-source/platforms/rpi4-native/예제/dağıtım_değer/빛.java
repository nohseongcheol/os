// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 빛 {
    public static void main(String[] bağımsız_değişkenler) throws Exception {
        int SUM_değer = 0;
        int 수 = 1;
        while (수 <= 10) {
            SUM_değer = SUM_değer + 수;
            수 = 수 + 1;
        }
        Türkçe.Öz.metinÇıktısı.수쓰기(SUM_değer);
        Türkçe.Öz.dosya.Yazma("aot.txt", "한글 AOT dosya 😀");
        Türkçe.Öz.metinÇıktısı.yazma_hat(Türkçe.Öz.dosya.Okuma("aot.txt"));
    }
}
