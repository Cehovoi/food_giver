import transitions
from transitions import Machine

#Какую вы хотите пиццу? Большую или маленькую?
#Большую
#Как вы будете платить?
# Наличкой
#Вы хотите большую пиццу, оплата - наличкой?
#Да
#Спасибо за заказ

class Consumer(object):
    states = ['Какую вы хотите пиццу? Большую или маленькую?',
              'Как вы будете платить?',
              'Вы хотите большую пиццу, оплата - наличкой?',
              'Спасибо за заказ, ещё?',
              'На старт']
    def __init__(self, id, name):
        self.id=id
        self.name=name
        self.ordered_pizza = 0
        self.switch = 0
        self.machine = Machine(model=self, states=Consumer.states,
                               initial='Какую вы хотите пиццу? Большую или маленькую?')
        self.machine.add_transition(trigger='Большую',
                                    source='Какую вы хотите пиццу? Большую или маленькую?',
                                    dest='Как вы будете платить?')
        self.machine.add_transition(trigger='Наличкой',
                                    source='Как вы будете платить?',
                                    dest='Вы хотите большую пиццу, оплата - наличкой?')
        self.machine.add_transition(trigger='Да',
                                    source='Вы хотите большую пиццу, оплата - наличкой?',
                                    dest='Спасибо за заказ, ещё?',
                                    after='update_journal')
        self.machine.add_transition(trigger='Да',
                                    source='Спасибо за заказ, ещё?',
                                    dest='Какую вы хотите пиццу? Большую или маленькую?')
        self.machine.add_transition(trigger='Нет',
                                    source='Спасибо за заказ, ещё?',
                                    dest='На старт')


    def update_journal(self):
        self.ordered_pizza += 1
        self.switch += 1