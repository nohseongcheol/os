// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Birleşik_Krallık.JGbrOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Birleşik_Krallık.JGbrOS.Bellek_bölge.sayfa_yönetici;
import Birleşik_Krallık.JGbrOS.dosya_sistemi.Dosya_tanımlayıcı_tablo;

/** işlem_değer 식별자와 라운드로빈 Hazırlan 대기열을 관리한다. */
public final class Scheduler {
    private final sayfa_yönetici 쪽관리;
    private final Map<Integer, işlem_değer> İşlem_Listesi = new HashMap<Integer, işlem_değer>();
    private final Queue<işlem_değer> 준비대기열 = new ArrayDeque<işlem_değer>();
    private int Sonraki_tanımlayıcı = 1;

    public Scheduler(sayfa_yönetici 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public işlem_değer 첫과정(Dosya_tanımlayıcı_tablo Dosya_tanımlayıcı) {
        işlem_değer 새과정 = new işlem_değer(ayırmak_tanımlayıcı(), 0, 쪽관리.새주소공간(), Dosya_tanımlayıcı);
        İşlem_Listesi.put(Integer.valueOf(새과정.tanımlayıcı_değer()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public işlem_değer kopya_değer(işlem_değer ana_değer) {
        işlem_değer alt_değer = new işlem_değer(
                ayırmak_tanımlayıcı(),
                ana_değer.tanımlayıcı_değer(),
                쪽관리.쓰기시복사복제(ana_değer.adres_alanı()),
                ana_değer.Dosya_tanımlayıcı().kopya_değer());
        alt_değer.küme_program_mola(ana_değer.program_mola());
        İşlem_Listesi.put(Integer.valueOf(alt_değer.tanımlayıcı_değer()), alt_değer);
        준비대기열.offer(alt_değer);
        return alt_değer;
    }

    public işlem_değer Sonraki_işlem() {
        int çek_BAĞ_DEĞ_SAY = 준비대기열.size();
        for (int Dizin = 0; Dizin < çek_BAĞ_DEĞ_SAY; Dizin++) {
            işlem_değer Sonraki_öğe = 준비대기열.poll();
            if (Sonraki_öğe != null && (Sonraki_öğe.Durum_değer() == işlem_Durum.Hazırlan || Sonraki_öğe.Durum_değer() == işlem_Durum.yürütmek_komut)) {
                Sonraki_öğe.küme_Durum(işlem_Durum.yürütmek_komut);
                준비대기열.offer(Sonraki_öğe);
                return Sonraki_öğe;
            }
        }
        return null;
    }

    public int 자식기다리기(işlem_değer ana_değer, int alt_tanımlayıcı, boolean 기다리지않음) {
        for (işlem_değer aday : İşlem_Listesi.values()) {
            if (aday.ana_tanımlayıcı() != ana_değer.tanımlayıcı_değer()) {
                continue;
            }
            if (alt_tanımlayıcı > 0 && aday.tanımlayıcı_değer() != alt_tanımlayıcı) {
                continue;
            }
            if (aday.Durum_değer() == işlem_Durum.Çıkış_program) {
                int sonuç = (aday.çıkış_kodu() & 0xff) << 8;
                İşlem_Listesi.remove(Integer.valueOf(aday.tanımlayıcı_değer()));
                return sonuç;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public işlem_değer BUL_işlem(int tanımlayıcı_değer) {
        return İşlem_Listesi.get(Integer.valueOf(tanımlayıcı_değer));
    }

    private int ayırmak_tanımlayıcı() {
        return Sonraki_tanımlayıcı++;
    }
}
