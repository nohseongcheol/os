// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Polen.JPolOS.unterbrechen;

@FunctionalInterface
public interface UnterbrechenBehandler {
    int prozessWertEintrag(int gespeichertStapelAdresse);
}

