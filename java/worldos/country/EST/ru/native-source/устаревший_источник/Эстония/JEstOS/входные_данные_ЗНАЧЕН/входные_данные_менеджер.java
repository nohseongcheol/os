// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Эстония.JEstOS.входные_данные_ЗНАЧЕН;

import java.util.ArrayDeque;
import java.util.Queue;

/** 인터럽트와 관리 кодовое_значение 사이에서 входные_данные_ЗНАЧЕН 사건을 안전하게 넘긴다. */
public final class входные_данные_менеджер {
    private final Queue<входные_данные_Событие> События_Список = new ArrayDeque<входные_данные_Событие>();
    private final int 최대사건수;
    private int 버린사건수;

    public входные_данные_менеджер(int 최대사건수) {
        if (최대사건수 <= 0) {
            throw new IllegalArgumentException("Событие 수가 올바르지 않습니다.");
        }
        this.최대사건수 = 최대사건수;
    }

    public synchronized void Ключ_отключен(int Ключ_данные) {
        넣기(new входные_данные_Событие(входные_данные_Событие.Вид_ЗНАЧЕН.Ключ_отключен, Ключ_данные & 0xff, 0));
    }

    public synchronized void 키놓음(int Ключ_данные) {
        넣기(new входные_данные_Событие(входные_данные_Событие.Вид_ЗНАЧЕН.키놓음, Ключ_данные & 0xff, 0));
    }

    public synchronized void 쥐이동(int 가로, int Вертикаль_позиция) {
        넣기(new входные_данные_Событие(входные_данные_Событие.Вид_ЗНАЧЕН.쥐이동, 가로, Вертикаль_позиция));
    }

    public synchronized входные_данные_Событие Далее_Событие() {
        return События_Список.poll();
    }

    public synchronized int 버린사건수() {
        return 버린사건수;
    }

    private void 넣기(входные_данные_Событие Событие) {
        if (События_Список.size() == 최대사건수) {
            События_Список.poll();
            버린사건수++;
        }
        События_Список.offer(Событие);
    }
}

