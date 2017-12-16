# realize an example of the pattern "Observer"
# by alarm fire system of some office


class AlarmObservable(object):
    """OfficeAlarmObservable keeps observers and sends a notification to observers on state change."""
    def __init__(self):
        self._observers = []
        self._is_alarm = False

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def detach_all(self):
        self._observers = []

    def display_statuses(self):
        for observer in self._observers:
            print('{}: {}'.format(observer, observer.is_alarm))

    def _notify_alarm(self, is_alarm=False):
        for observer in self._observers:
            observer.set_alarm_status(is_alarm)

    @property
    def is_alarm(self):
        return self._is_alarm

    @is_alarm.setter
    def is_alarm(self, is_alarm):
        if self._is_alarm == is_alarm:
            return

        self._notify_alarm(is_alarm)
        self._is_alarm = is_alarm


class Office(object):
    def __init__(self, name):
        self.name = name
        self.is_alarm = False

    def __str__(self):
        return self.name

    def set_alarm_status(self, is_alarm):
        self.is_alarm = is_alarm


if __name__ == "__main__":
    alarm_observable = AlarmObservable()

    # create offices and attach to alarm observable
    office_names = ['First', 'Second', 'Third']
    for name in office_names:
        alarm_observable.attach(Office(name))

    # turn on alarm and check office statuses
    print('{0} TURN ON ALARM {0}'.format('=' * 10))
    alarm_observable.is_alarm = True
    alarm_observable.display_statuses()

    # turn off alarm and check office statuses
    print('{0} TURN OFF ALARM {0}'.format('=' * 10))
    alarm_observable.is_alarm = False
    alarm_observable.display_statuses()
