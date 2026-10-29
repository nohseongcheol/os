// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package EMzantsi_Afrika.JZafOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import EMzantsi_Afrika.JZafOS.기억공간.ikhasi_umphathi;
import EMzantsi_Afrika.JZafOS.uhlobo_loseto_lwefayile.파일서술자표;

/** Inkqubo_ixabiso 식별자와 라운드로빈 lungisa 대기열을 관리한다. */
public final class 배정기 {
    private final ikhasi_umphathi 쪽관리;
    private final Map<Integer, Inkqubo_ixabiso> uluhlu_lweprosesi = new HashMap<Integer, Inkqubo_ixabiso>();
    private final Queue<Inkqubo_ixabiso> 준비대기열 = new ArrayDeque<Inkqubo_ixabiso>();
    private int 다음식별자 = 1;

    public 배정기(ikhasi_umphathi 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public Inkqubo_ixabiso 첫과정(파일서술자표 파일서술자) {
        Inkqubo_ixabiso 새과정 = new Inkqubo_ixabiso(yabela_isalathisi(), 0, 쪽관리.새주소공간(), 파일서술자);
        uluhlu_lweprosesi.put(Integer.valueOf(새과정.isalathisi_ixabiso()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public Inkqubo_ixabiso 복제(Inkqubo_ixabiso 부모) {
        Inkqubo_ixabiso umntwana_ixabiso = new Inkqubo_ixabiso(
                yabela_isalathisi(),
                부모.isalathisi_ixabiso(),
                쪽관리.쓰기시복사복제(부모.idilesi_isithuba()),
                부모.파일서술자().복제());
        umntwana_ixabiso.프로그램끝설정(부모.프로그램끝());
        uluhlu_lweprosesi.put(Integer.valueOf(umntwana_ixabiso.isalathisi_ixabiso()), umntwana_ixabiso);
        준비대기열.offer(umntwana_ixabiso);
        return umntwana_ixabiso;
    }

    public Inkqubo_ixabiso 다음과정() {
        int 검사수 = 준비대기열.size();
        for (int indeksa = 0; indeksa < 검사수; indeksa++) {
            Inkqubo_ixabiso 다음 = 준비대기열.poll();
            if (다음 != null && (다음.imo_ixabiso() == Inkqubo_imo_4346e67f.lungisa || 다음.imo_ixabiso() == Inkqubo_imo_4346e67f.ukwenza_umyalelo)) {
                다음.isethi_imo(Inkqubo_imo_4346e67f.ukwenza_umyalelo);
                준비대기열.offer(다음);
                return 다음;
            }
        }
        return null;
    }

    public int 자식기다리기(Inkqubo_ixabiso 부모, int umntwana_isalathisi, boolean 기다리지않음) {
        for (Inkqubo_ixabiso 후보 : uluhlu_lweprosesi.values()) {
            if (후보.부모식별자() != 부모.isalathisi_ixabiso()) {
                continue;
            }
            if (umntwana_isalathisi > 0 && 후보.isalathisi_ixabiso() != umntwana_isalathisi) {
                continue;
            }
            if (후보.imo_ixabiso() == Inkqubo_imo_4346e67f.phuma_inkqubo) {
                int 결과 = (후보.종료값() & 0xff) << 8;
                uluhlu_lweprosesi.remove(Integer.valueOf(후보.isalathisi_ixabiso()));
                return 결과;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public Inkqubo_ixabiso fumana_Inkqubo(int isalathisi_ixabiso) {
        return uluhlu_lweprosesi.get(Integer.valueOf(isalathisi_ixabiso));
    }

    private int yabela_isalathisi() {
        return 다음식별자++;
    }
}
