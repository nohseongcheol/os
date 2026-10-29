// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ukraina.JUkrOS.wejście_WARTOŚĆ;

import java.util.ArrayDeque;
import java.util.Queue;

/** 인터럽트와 관리 KOD_WARTOŚĆ 사이에서 wejście_WARTOŚĆ 사건을 안전하게 넘긴다. */
public final class wejście_Menedżer {
    private final Queue<wejście_konkurs> Wydarzenia_Lista = new ArrayDeque<wejście_konkurs>();
    private final int 최대사건수;
    private int 버린사건수;

    public wejście_Menedżer(int 최대사건수) {
        if (최대사건수 <= 0) {
            throw new IllegalArgumentException("Wydarzenie 수가 올바르지 않습니다.");
        }
        this.최대사건수 = 최대사건수;
    }

    public synchronized void Klucz_niedziałający(int Klucz_dane) {
        넣기(new wejście_konkurs(wejście_konkurs.Rodzaj_WARTOŚĆ.Klucz_niedziałający, Klucz_dane & 0xff, 0));
    }

    public synchronized void 키놓음(int Klucz_dane) {
        넣기(new wejście_konkurs(wejście_konkurs.Rodzaj_WARTOŚĆ.키놓음, Klucz_dane & 0xff, 0));
    }

    public synchronized void 쥐이동(int 가로, int gałąź_stanowisko) {
        넣기(new wejście_konkurs(wejście_konkurs.Rodzaj_WARTOŚĆ.쥐이동, 가로, gałąź_stanowisko));
    }

    public synchronized wejście_konkurs Dalej_konkurs() {
        return Wydarzenia_Lista.poll();
    }

    public synchronized int 버린사건수() {
        return 버린사건수;
    }

    private void 넣기(wejście_konkurs Wydarzenie) {
        if (Wydarzenia_Lista.size() == 최대사건수) {
            Wydarzenia_Lista.poll();
            버린사건수++;
        }
        Wydarzenia_Lista.offer(Wydarzenie);
    }
}

