// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package suomi.oma;

/** 한국어로 esittely·던지기·잡기를 할 numero 있는 pätemätön_argumentti_poikkeus. */
public class pätemätön_argumentti_poikkeus extends java.lang.IllegalArgumentException {
    public pätemätön_argumentti_poikkeus() { super(); }
    public pätemätön_argumentti_poikkeus(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
