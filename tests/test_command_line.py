import meeting_finder.command_line as cl


class TestParameter(cl.Parameter):
    name = '--hi'
    opts = {
        'help': 'testing TestParameter',
        'default': 1,
        'type': int
    }

    def process(self, argument):
        self.received = argument


def test_parameter():
    t = TestParameter()
    assert t.name == '--hi'
    assert t.opts['default'] == 1
    t.process('bye')
    assert t.received == 'bye'


def test_dispatcher_empty():
    d = cl.Dispatcher()
    d.dispatch([])
    assert d.parameters == []


def test_dispatcher_to_one_with_arg():
    d = cl.Dispatcher()
    t = TestParameter()
    d.add_param(t)
    d.dispatch(['--hi', '2'])
    assert t.received == 2


def test_dispatcher_to_one_with_default():
    d = cl.Dispatcher()
    t = TestParameter()
    d.add_param(t)
    d.dispatch([])
    assert t.received == 1


def test_dispatcher_to_two():
    d = cl.Dispatcher()
    t1 = TestParameter()
    t2 = TestParameter()
    d.add_all_params([t1, t2])
    d.dispatch([])
    assert t1.received == 1
    assert t2.received == 1
