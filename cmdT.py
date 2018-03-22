import cmd2

class work(object):
	def __init__(self,name=''):
		self.name=name
		self.now='rest'
		
	def do_start(self,*args):
		"Start working!"
		self.now="work"
		print(self)
		
	def do_stop(self,*args):
		"Have a rest!"
		self.now='rest'
		print(self)
		
	def __str__(self):
		return "Work state: %(now)s" % vars(self)
		
#p=cmd2.Cmd(work())
#p.cmdloop()

class Job(object):
    def __init__(self, name=''):
        self.name = name
        self.state = 'not started'
    def do_run(self, *args):
        'Start the job'
        self.state = 'started'
        print(self)
    def do_stop(self, *args):
        'End the job'
        self.state = 'ended'
        print(self)
    def do_pause(self, *args):
        'Pause the job'
        self.state = 'paused'
        print(self)
    def do_resume(self, *args):
        'Resume the job'
        self.state = 'resumed'
        print(self)
    def do_raise_exc(self, *args):
        'Simulate a method raising an exception'
        raise RuntimeError('some error')
    def __str__(self):
        return 'job %(name)s %(state)s' % vars(self)
		
jobCLI = cmd2.Cmd(Job())
jobCLI.cmdloop()