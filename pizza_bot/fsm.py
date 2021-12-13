import transitions

class FSM(object):
    def __init__(self):
        states = [
            'size', 'pay_method', 'confirm', 'finalize'
        ]
        transition = [
            {
                'trigger': 'большую',
                'source': 'size',
                'dest': 'pay_method'
            },
            {
                'trigger': 'маленькую',
                'source': 'size',
                'dest': 'pay_method'
            },
            {
                'trigger': 'наличкой',
                'source': 'pay_method',
                'dest': 'confirm'
            },
            {
                'trigger': 'пластиком',
                'source': 'pay_method',
                'dest': 'confirm'
            },
            {
                'trigger': 'натурой',
                'source': 'pay_method',
                'dest': 'confirm'
            },
            {
                'trigger': 'да',
                'source': 'confirm',
                'dest': 'finalize',
            },
            {
                'trigger': 'нет',
                'source': 'confirm',
                'dest': 'size', 
            },
        ]

        self.dialogs = {
            'size': "Какую вы хотите пиццу? Большую или маленькую?",
            'pay_method': 'Как вы будете платить?',
            'confirm': 'Вы хотите {size} пиццу, оплата - {pay_method}?',
            'finalize': "Заказ принят",
        }
        self.machine = transitions.Machine(
            model=self, states=states, initial='size', transitions=transition
        )

    def get_dialog(self):
        answer = self.dialogs[self.state]
        return answer
