// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Espanya.JEspOS.interrupció;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class interrupció_administrador {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean Actiu;

    public void registrar_se_introducció(int INDEX, 개입중단처리기 처리기) {
        번호확인(INDEX);
        처리기들[INDEX] = 처리기;
    }

    public void versió_Emmagatzematge(int INDEX) {
        번호확인(INDEX);
        처리기들[INDEX] = null;
    }

    public int distribuir_VALOR(int INDEX, int 저장된쌓임주소) {
        번호확인(INDEX);
        if (!Actiu) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[INDEX];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.Procés_VALOR_introducció(저장된쌓임주소);
    }

    public void activar() {
        Actiu = true;
    }

    public void desactivar() {
        Actiu = false;
    }

    public boolean tecnologies_de_la_informació_Actiu() {
        return Actiu;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int INDEX) {
        if (INDEX < 0 || INDEX >= 처리기들.length) {
            throw new IllegalArgumentException("interrupció 번호가 올바르지 않습니다.");
        }
    }
}

