// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Afrika_Borwa.JZafOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Afrika_Borwa.JZafOS.기억공간.letlakala_molaodi;
import Afrika_Borwa.JZafOS.tshepedišo_ya_difaele.파일서술자표;

/** tiragalo_boleng 식별자와 라운드로빈 Lokišetša 대기열을 관리한다. */
public final class 배정기 {
    private final letlakala_molaodi 쪽관리;
    private final Map<Integer, tiragalo_boleng> Lenaneo_la_Tshepedišo = new HashMap<Integer, tiragalo_boleng>();
    private final Queue<tiragalo_boleng> 준비대기열 = new ArrayDeque<tiragalo_boleng>();
    private int 다음식별자 = 1;

    public 배정기(letlakala_molaodi 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public tiragalo_boleng 첫과정(파일서술자표 파일서술자) {
        tiragalo_boleng 새과정 = new tiragalo_boleng(aba_sešupi(), 0, 쪽관리.새주소공간(), 파일서술자);
        Lenaneo_la_Tshepedišo.put(Integer.valueOf(새과정.sešupi_boleng()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public tiragalo_boleng 복제(tiragalo_boleng 부모) {
        tiragalo_boleng ngwana_boleng = new tiragalo_boleng(
                aba_sešupi(),
                부모.sešupi_boleng(),
                쪽관리.쓰기시복사복제(부모.atrese_sekgoba()),
                부모.파일서술자().복제());
        ngwana_boleng.프로그램끝설정(부모.프로그램끝());
        Lenaneo_la_Tshepedišo.put(Integer.valueOf(ngwana_boleng.sešupi_boleng()), ngwana_boleng);
        준비대기열.offer(ngwana_boleng);
        return ngwana_boleng;
    }

    public tiragalo_boleng 다음과정() {
        int 검사수 = 준비대기열.size();
        for (int lokela = 0; lokela < 검사수; lokela++) {
            tiragalo_boleng 다음 = 준비대기열.poll();
            if (다음 != null && (다음.boemo_boleng() == tiragalo_boemo.Lokišetša || 다음.boemo_boleng() == tiragalo_boemo.phethagatša_taelo)) {
                다음.sehlopha_boemo(tiragalo_boemo.phethagatša_taelo);
                준비대기열.offer(다음);
                return 다음;
            }
        }
        return null;
    }

    public int 자식기다리기(tiragalo_boleng 부모, int ngwana_sešupi, boolean 기다리지않음) {
        for (tiragalo_boleng 후보 : Lenaneo_la_Tshepedišo.values()) {
            if (후보.부모식별자() != 부모.sešupi_boleng()) {
                continue;
            }
            if (ngwana_sešupi > 0 && 후보.sešupi_boleng() != ngwana_sešupi) {
                continue;
            }
            if (후보.boemo_boleng() == tiragalo_boemo.Etšwa_tirišo) {
                int 결과 = (후보.종료값() & 0xff) << 8;
                Lenaneo_la_Tshepedišo.remove(Integer.valueOf(후보.sešupi_boleng()));
                return 결과;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public tiragalo_boleng hwetša_tiragalo(int sešupi_boleng) {
        return Lenaneo_la_Tshepedišo.get(Integer.valueOf(sešupi_boleng));
    }

    private int aba_sešupi() {
        return 다음식별자++;
    }
}
