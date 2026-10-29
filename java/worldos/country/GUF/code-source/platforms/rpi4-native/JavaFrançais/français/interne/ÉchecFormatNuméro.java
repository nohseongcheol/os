// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;

/** ÉchecFormatNuméro : exception pouvant être déclarée, levée et interceptée avec l’API française. */
public class ÉchecFormatNuméro extends ExceptionArgumentInvalide {
    public ÉchecFormatNuméro() { super(); }
    public ÉchecFormatNuméro(String description) { super(description); }
    public String description() { return getMessage(); }
}
