// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Svalbard_og_Jan_Mayen.JSjmOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Svalbard_og_Jan_Mayen.JSjmOS.Minne_område.Sidebehandling;
import Svalbard_og_Jan_Mayen.JSjmOS.filsystem.파일서술자표;

/** Prosess_VERDI 식별자와 라운드로빈 Forbered 대기열을 관리한다. */
public final class Scheduler {
    private final Sidebehandling 쪽관리;
    private final Map<Integer, Prosess_VERDI> Prosessliste = new HashMap<Integer, Prosess_VERDI>();
    private final Queue<Prosess_VERDI> 준비대기열 = new ArrayDeque<Prosess_VERDI>();
    private int Neste_identifikator = 1;

    public Scheduler(Sidebehandling 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public Prosess_VERDI 첫과정(파일서술자표 파일서술자) {
        Prosess_VERDI 새과정 = new Prosess_VERDI(tildele_identifikator(), 0, 쪽관리.새주소공간(), 파일서술자);
        Prosessliste.put(Integer.valueOf(새과정.identifikator_VERDI()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public Prosess_VERDI klon_VERDI(Prosess_VERDI overordnet_VERDI_881a8172) {
        Prosess_VERDI barn_VERDI = new Prosess_VERDI(
                tildele_identifikator(),
                overordnet_VERDI_881a8172.identifikator_VERDI(),
                쪽관리.쓰기시복사복제(overordnet_VERDI_881a8172.adresseområde()),
                overordnet_VERDI_881a8172.파일서술자().klon_VERDI());
        barn_VERDI.sett_app_pause(overordnet_VERDI_881a8172.app_pause());
        Prosessliste.put(Integer.valueOf(barn_VERDI.identifikator_VERDI()), barn_VERDI);
        준비대기열.offer(barn_VERDI);
        return barn_VERDI;
    }

    public Prosess_VERDI Neste_Prosess() {
        int sjekk_ANTALL = 준비대기열.size();
        for (int INDEKS = 0; INDEKS < sjekk_ANTALL; INDEKS++) {
            Prosess_VERDI Neste_vare = 준비대기열.poll();
            if (Neste_vare != null && (Neste_vare.status_VERDI() == Prosess_status.Forbered || Neste_vare.status_VERDI() == Prosess_status.Utfør_kommando)) {
                Neste_vare.sett_status(Prosess_status.Utfør_kommando);
                준비대기열.offer(Neste_vare);
                return Neste_vare;
            }
        }
        return null;
    }

    public int 자식기다리기(Prosess_VERDI overordnet_VERDI_881a8172, int barn_identifikator, boolean 기다리지않음) {
        for (Prosess_VERDI 후보 : Prosessliste.values()) {
            if (후보.overordnet_identifikator() != overordnet_VERDI_881a8172.identifikator_VERDI()) {
                continue;
            }
            if (barn_identifikator > 0 && 후보.identifikator_VERDI() != barn_identifikator) {
                continue;
            }
            if (후보.status_VERDI() == Prosess_status.Utgang_app) {
                int KR = (후보.avslutningskode() & 0xff) << 8;
                Prosessliste.remove(Integer.valueOf(후보.identifikator_VERDI()));
                return KR;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public Prosess_VERDI Søk_Prosess(int identifikator_VERDI) {
        return Prosessliste.get(Integer.valueOf(identifikator_VERDI));
    }

    private int tildele_identifikator() {
        return Neste_identifikator++;
    }
}
