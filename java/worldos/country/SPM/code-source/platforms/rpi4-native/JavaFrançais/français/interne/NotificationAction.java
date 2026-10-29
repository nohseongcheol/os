// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;
/** Notification d’action créée par le gestionnaire d’événements de la JVM du projet. */
public final class NotificationAction {
    private NotificationAction() {}
    public native String texteCommande();
    public native ÉlémentÉcran sourceÉvènement();
    public native int numéro();
}
