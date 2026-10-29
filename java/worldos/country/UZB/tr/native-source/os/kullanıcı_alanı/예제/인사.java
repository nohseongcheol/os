// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int çalıştır() {
        kullanıcı_alanı.Yazma("Hello from a separate Java ELF!\n");
        kullanıcı_alanı.Yazma(kullanıcı_alanı.yürütme_izin() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int Dizin = 0; Dizin < kullanıcı_alanı.인수개수(); Dizin++) {
            kullanıcı_alanı.Yazma("arg: "); kullanıcı_alanı.Yazma(kullanıcı_alanı.bağımsız_değişkenler(Dizin)); kullanıcı_alanı.Yazma("\n");
        }
        return kullanıcı_alanı.yürütme_izin() == 3 ? 0 : 1;
    }
}
