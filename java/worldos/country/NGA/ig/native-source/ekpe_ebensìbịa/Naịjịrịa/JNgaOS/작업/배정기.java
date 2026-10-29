// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Naịjịrịa.JNgaOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Naịjịrịa.JNgaOS.기억공간.ihuakwụkwọ_njikwa;
import Naịjịrịa.JNgaOS.sistèm_ọbọakwụkwo.파일서술자표;

/** ùsòrò_valuu_6712bde7 식별자와 라운드로빈 Kwado 대기열을 관리한다. */
public final class 배정기 {
    private final ihuakwụkwọ_njikwa 쪽관리;
    private final Map<Integer, ùsòrò_valuu_6712bde7> Ndepụta_Usoro = new HashMap<Integer, ùsòrò_valuu_6712bde7>();
    private final Queue<ùsòrò_valuu_6712bde7> 준비대기열 = new ArrayDeque<ùsòrò_valuu_6712bde7>();
    private int 다음식별자 = 1;

    public 배정기(ihuakwụkwọ_njikwa 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public ùsòrò_valuu_6712bde7 첫과정(파일서술자표 파일서술자) {
        ùsòrò_valuu_6712bde7 새과정 = new ùsòrò_valuu_6712bde7(kepụta_ihe_nkọwapụta(), 0, 쪽관리.새주소공간(), 파일서술자);
        Ndepụta_Usoro.put(Integer.valueOf(새과정.ihe_nkọwapụta_valuu()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public ùsòrò_valuu_6712bde7 복제(ùsòrò_valuu_6712bde7 부모) {
        ùsòrò_valuu_6712bde7 njìmebe_nnwā_valuu = new ùsòrò_valuu_6712bde7(
                kepụta_ihe_nkọwapụta(),
                부모.ihe_nkọwapụta_valuu(),
                쪽관리.쓰기시복사복제(부모.àdreèsì_ohere()),
                부모.파일서술자().복제());
        njìmebe_nnwā_valuu.프로그램끝설정(부모.프로그램끝());
        Ndepụta_Usoro.put(Integer.valueOf(njìmebe_nnwā_valuu.ihe_nkọwapụta_valuu()), njìmebe_nnwā_valuu);
        준비대기열.offer(njìmebe_nnwā_valuu);
        return njìmebe_nnwā_valuu;
    }

    public ùsòrò_valuu_6712bde7 다음과정() {
        int 검사수 = 준비대기열.size();
        for (int indèks = 0; indèks < 검사수; indèks++) {
            ùsòrò_valuu_6712bde7 다음 = 준비대기열.poll();
            if (다음 != null && (다음.ọnọdụ_valuu() == ùsòrò_ọnọdụ.Kwado || 다음.ọnọdụ_valuu() == ùsòrò_ọnọdụ.mee_nnyemiwu)) {
                다음.Seti_ọnọdụ(ùsòrò_ọnọdụ.mee_nnyemiwu);
                준비대기열.offer(다음);
                return 다음;
            }
        }
        return null;
    }

    public int 자식기다리기(ùsòrò_valuu_6712bde7 부모, int njìmebe_nnwā_ihe_nkọwapụta, boolean 기다리지않음) {
        for (ùsòrò_valuu_6712bde7 후보 : Ndepụta_Usoro.values()) {
            if (후보.부모식별자() != 부모.ihe_nkọwapụta_valuu()) {
                continue;
            }
            if (njìmebe_nnwā_ihe_nkọwapụta > 0 && 후보.ihe_nkọwapụta_valuu() != njìmebe_nnwā_ihe_nkọwapụta) {
                continue;
            }
            if (후보.ọnọdụ_valuu() == ùsòrò_ọnọdụ.pụọ_app) {
                int 결과 = (후보.종료값() & 0xff) << 8;
                Ndepụta_Usoro.remove(Integer.valueOf(후보.ihe_nkọwapụta_valuu()));
                return 결과;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public ùsòrò_valuu_6712bde7 chọta_ùsòrò(int ihe_nkọwapụta_valuu) {
        return Ndepụta_Usoro.get(Integer.valueOf(ihe_nkọwapụta_valuu));
    }

    private int kepụta_ihe_nkọwapụta() {
        return 다음식별자++;
    }
}
