// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Hollanda.JNldOS.konak;

import Hollanda.JNldOS.Çekirdek.Çekirdek;

public final class konak_IPL {
    private konak_IPL() {
    }

    public static void main(String[] parametre_bağımsız_değişken) {
        Çekirdek çekirdek_değer = new Çekirdek(new konak_donanım());
        çekirdek_değer.çalıştır();
        çekirdek_değer.yürütmek_adım();
    }
}

