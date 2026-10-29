// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 빛 {
    public static void main(String[] argumen) throws Exception {
        int SUM_VALUE = 0;
        int 수 = 1;
        while (수 <= 10) {
            SUM_VALUE = SUM_VALUE + 수;
            수 = 수 + 1;
        }
        Indonesia.Asli.keluaranTeks.수쓰기(SUM_VALUE);
        Indonesia.Asli.berkas.Tulis("aot.txt", "한글 AOT berkas 😀");
        Indonesia.Asli.keluaranTeks.tulis_baris(Indonesia.Asli.berkas.Baca("aot.txt"));
    }
}
