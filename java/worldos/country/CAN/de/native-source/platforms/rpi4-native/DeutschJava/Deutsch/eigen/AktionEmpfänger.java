// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;
/** Empfängt und verarbeitet Aktionsmeldungen, etwa von Schaltflächen. */
public interface AktionEmpfänger {
    void aktionEmpfangen(AktionMitteilung mitteilung);
}
