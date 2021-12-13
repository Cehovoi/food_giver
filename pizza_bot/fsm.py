import transitions

class FSM(object):
    def __init__(self, notify_method=None):
        states = [
            'size', 'pay_method', 'confirm', 'finalize'
        ]
        transition = [
            {
                'trigger': 'большую',
                'source': 'size',
                'dest': 'pay_method',
                'after': 'store_size'
            },
            {
                'trigger': 'маленькую',
                'source': 'size',
                'dest': 'pay_method',
                'after': 'store_size'
            },
            {
                'trigger': 'наличкой',
                'source': 'pay_method',
                'dest': 'confirm',
                'after': 'store_pay_method'
            },
            {
                'trigger': 'пластиком',
                'source': 'pay_method',
                'dest': 'confirm',
                'after': 'store_pay_method'
            },
            {
                'trigger': 'натурой',
                'source': 'pay_method',
                'dest': 'confirm',
                'after': 'store_pay_method'
            },
            {
                'trigger': 'да',
                'source': 'confirm',
                'dest': 'finalize',
                'before': 'notify',
                'after': 'reset',
            },
            {
                'trigger': 'нет',
                'source': 'confirm',
                'dest': 'size', 
                'after': 'reset'
            },
        ]

        self.dialogs = {
            'size': "Какую вы хотите пиццу? Большую или маленькую?",
            'pay_method': 'Как вы будете платить?',
            'confirm': 'Вы хотите {size} пиццу, оплата - {pay_method}?',
            'finalize': "Заказ принят",
        }
        self.machine = transitions.Machine(
            model=self, states=states, initial='size', transitions=transition,
            send_event=True
        )
        self.size = None
        self.pay_method = None
        self.notify_method = notify_method

    def get_dialog(self):
        return self.dialogs[self.state].format(
            size=self.size, pay_method=self.pay_method
        )

    def store_size(self, event_data):
        self.size = event_data.event.name

    def store_pay_method(self, event_data):
        self.pay_method = event_data.event.name

    def notify(self, _):
        if self.notify_method is not None:
            self.notify_method(self.size, self.pay_method)

    def reset(self, _):
        self.state = 'size'
        self.size = None
        self.pay_method = None