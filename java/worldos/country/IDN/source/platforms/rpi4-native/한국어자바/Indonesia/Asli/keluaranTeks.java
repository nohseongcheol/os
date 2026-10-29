// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Indonesia.Asli;
/** Asli 커널의 표준 keluaranTeks. UTF-16 서로게이트 쌍은 UART에서 UTF-8로 보낸다. */
public final class keluaranTeks {
    private keluaranTeks() {}
    public static void Tulis(String teks) { System.out.print(teks); }
    public static void tulis_baris(String teks) { System.out.println(teks); }
    public static void 수쓰기(int 수) { System.out.println(수); }
}
