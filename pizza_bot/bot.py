from .fsm import FSM
import transitions
class DummyStore:
    def __init__(self):
        self._storage = {}

    def get(self, id):
        return self._storage.get(id)

    def set(self, id, state):
        self._storage[id] = state

class Bot:
    def __init__(self, fsm=FSM, storage=DummyStore()):
        self.fsm = fsm
        self.storage = storage

    def handle(self, client_id, message):
        state = self.storage.get(client_id)
        if state is None:
            state = self.fsm()
            self.storage.set(client_id, state)
            return state.get_dialog()
        try:
            state.trigger(message.lower().strip())
            self.storage.set(client_id, state)
        except Exception as e:
            #if '/' in e:
                #pass
            s = state.machine.get_triggers(state.state)
            answer = list(filter(lambda x: not x.startswith('to_'), s))
            return 'Можно ответить: ' + ''.join(word + ' ' for word in answer)
        answer = state.get_dialog()
        return answer
