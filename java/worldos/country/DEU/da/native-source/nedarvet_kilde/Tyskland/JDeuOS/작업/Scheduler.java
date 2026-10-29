// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Tyskland.JDeuOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Tyskland.JDeuOS.Hukommelse_område.Sidestyring;
import Tyskland.JDeuOS.filsystem.파일서술자표;

/** Proces_VÆRDI 식별자와 라운드로빈 Tilrettelæg 대기열을 관리한다. */
public final class Scheduler {
    private final Sidestyring 쪽관리;
    private final Map<Integer, Proces_VÆRDI> Procesliste = new HashMap<Integer, Proces_VÆRDI>();
    private final Queue<Proces_VÆRDI> 준비대기열 = new ArrayDeque<Proces_VÆRDI>();
    private int Næste_identifikator = 1;

    public Scheduler(Sidestyring 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public Proces_VÆRDI 첫과정(파일서술자표 파일서술자) {
        Proces_VÆRDI 새과정 = new Proces_VÆRDI(tildel_identifikator(), 0, 쪽관리.새주소공간(), 파일서술자);
        Procesliste.put(Integer.valueOf(새과정.identifikator_VÆRDI()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public Proces_VÆRDI klon_VÆRDI(Proces_VÆRDI overordnet_VÆRDI) {
        Proces_VÆRDI barn_VÆRDI = new Proces_VÆRDI(
                tildel_identifikator(),
                overordnet_VÆRDI.identifikator_VÆRDI(),
                쪽관리.쓰기시복사복제(overordnet_VÆRDI.adresseinterval()),
                overordnet_VÆRDI.파일서술자().klon_VÆRDI());
        barn_VÆRDI.sæt_app_pause(overordnet_VÆRDI.app_pause());
        Procesliste.put(Integer.valueOf(barn_VÆRDI.identifikator_VÆRDI()), barn_VÆRDI);
        준비대기열.offer(barn_VÆRDI);
        return barn_VÆRDI;
    }

    public Proces_VÆRDI Næste_Proces() {
        int check_TÆL = 준비대기열.size();
        for (int INDEKS = 0; INDEKS < check_TÆL; INDEKS++) {
            Proces_VÆRDI Næste_vare = 준비대기열.poll();
            if (Næste_vare != null && (Næste_vare.status_VÆRDI() == Proces_status.Tilrettelæg || Næste_vare.status_VÆRDI() == Proces_status.Udfør_kommando)) {
                Næste_vare.sæt_status(Proces_status.Udfør_kommando);
                준비대기열.offer(Næste_vare);
                return Næste_vare;
            }
        }
        return null;
    }

    public int 자식기다리기(Proces_VÆRDI overordnet_VÆRDI, int barn_identifikator, boolean 기다리지않음) {
        for (Proces_VÆRDI 후보 : Procesliste.values()) {
            if (후보.overordnet_identifikator() != overordnet_VÆRDI.identifikator_VÆRDI()) {
                continue;
            }
            if (barn_identifikator > 0 && 후보.identifikator_VÆRDI() != barn_identifikator) {
                continue;
            }
            if (후보.status_VÆRDI() == Proces_status.Afslut_app) {
                int KR = (후보.Afslut_KODE() & 0xff) << 8;
                Procesliste.remove(Integer.valueOf(후보.identifikator_VÆRDI()));
                return KR;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public Proces_VÆRDI Søg_Proces(int identifikator_VÆRDI) {
        return Procesliste.get(Integer.valueOf(identifikator_VÆRDI));
    }

    private int tildel_identifikator() {
        return Næste_identifikator++;
    }
}
