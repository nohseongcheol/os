// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;

/** exception : exception pouvant être déclarée, levée et interceptée avec l’API française. */
public class exception extends java.lang.Exception {
    public exception() { super(); }
    public exception(String description) { super(description); }
    public String description() { return getMessage(); }
}
