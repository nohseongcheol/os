// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Қазақстан.JKazOS.ядро;

import Қазақстан.JKazOS.Жад_аумақ.Жад_менеджер;
import Қазақстан.JKazOS.Жад_аумақ.бет_менеджер;
import Қазақстан.JKazOS.입력.입력관리자;
import Қазақстан.JKazOS.작업.Процесс_мән;
import Қазақстан.JKazOS.작업.Жоспарлаушы;
import Қазақстан.JKazOS.체계호출.체계호출;
import Қазақстан.JKazOS.файлдық_жүйе.파일서술자표;
import Қазақстан.JKazOS.файлдық_жүйе.файлдық_жүйе;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class ядро {
    private final 하드웨어 құрылғы_мән;
    private final Жад_менеджер Жад_аумақ = new Жад_менеджер(32 * 1024 * 1024);
    private final бет_менеджер 쪽관리 = new бет_менеджер();
    private final файлдық_жүйе файлдық_жүйе = new файлдық_жүйе();
    private final Жоспарлаушы Жоспарлаушы = new Жоспарлаушы(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final Процесс_мән 첫과정;
    private final 체계호출 체계호출;

    public ядро(하드웨어 құрылғы_мән) {
        this.құрылғы_мән = құрылғы_мән;
        첫과정 = Жоспарлаушы.첫과정(new 파일서술자표(файлдық_жүйе));
        체계호출 = new 체계호출(файлдық_жүйе, 쪽관리, Жоспарлаушы, құрылғы_мән, 입력관리);
    }

    public void Орындау_2() {
        құрылғы_мән.직렬출력("=== JKazOS 관리 ядро_мән ===\n");
    }

    public void орындау_қадам() {
        құрылғы_мән.중앙처리장치멈춤();
    }

    public Жад_менеджер Жад_аумақ() {
        return Жад_аумақ;
    }

    public бет_менеджер 쪽관리() {
        return 쪽관리;
    }

    public файлдық_жүйе файлдық_жүйе() {
        return файлдық_жүйе;
    }

    public Жоспарлаушы Жоспарлаушы() {
        return Жоспарлаушы;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public Процесс_мән 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
