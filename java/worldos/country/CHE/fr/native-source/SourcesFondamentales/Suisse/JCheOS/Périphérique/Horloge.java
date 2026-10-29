// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Suisse.JCheOS.Périphérique;

/** Gère les tops du PIT et les instants de préemption. */
public final class Horloge {
    private final int deuxièmeParBattements;
    private long nombreÉlémentsBattement;

    public Horloge(int deuxièmeParBattements) {
        if (deuxièmeParBattements <= 0) {
            throw new IllegalArgumentException("초당 valeurBattement 수가 올바르지 않습니다.");
        }
        this.deuxièmeParBattements = deuxièmeParBattements;
    }

    public long valeurBattement() {
        return ++nombreÉlémentsBattement;
    }

    public long nombreÉlémentsBattement() {
        return nombreÉlémentsBattement;
    }

    public long millisecondesÉcoulé() {
        return nombreÉlémentsBattement * 1000L / deuxièmeParBattements;
    }
}

