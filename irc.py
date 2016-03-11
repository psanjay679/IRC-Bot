import socket

class IRC:
    queue = []
    partial = ''
    
    def __init__(self, network, port, name, hostName, serverName, realName):
        self.network = network
        self.port = port
        self.name = name
        self.hostName = hostName
        self.serverName = serverName
        self.realName = realName

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.network, self.port))
        self.nick(name)

        self.send('USER' + self.name + '' + self.serverName + '' +
                  self.hostName + '' + self.realName)

    def quit(self):
        self.send('QUIT')
        self.socket.close()

    def send(self, text):
        self.socket.send(text + 'rn')

    def nick(self, name):
        self.name = name
        self.send('NICK' + self.name)

    def recv(self, size = 2048):
        commands = self.socket.recv(size).split('rn')

        if len(self.partial):
            commands[0] = self.partial + commands[0]

            self.partial = ''
        if len(commands[-1]):
            self.partial = commands[-1]
            self.queue.extend(commands[:-1])
        else:
            self.queue.extend(commands)

    def retrieve(self):
        if len(self.queue):
            commands = self.queue[0]
            self.queue.pop(0)
            return commands
        else:
            return False

    def dismantle(self, command):
        if command:
            source = command.split(':')[1].split('')[0]
            parameters = command.split(':')[1].split('')[1:]

            if not len(parameters[-1]):
                parameters.pop()

            if command.count(':') > 1:
                parameters.append(''.join(command.split(':')[2:]))
            return source, parameters
    def privmsg(self, destination, message):
        self.send('PRIVMSG' + destination + ':' + message)

    def notice(self, destination, message):
        self.send('NOTICE' + destination + ':' + message)

    def join(self, channel):
        self.send('JOIN' + channel)

    def part(self, channel):
        self.send('PART' + channel)

    def topic(self, channel, topic = ''):
        self.send('TOPIC' + channel + '' + topic)

    def names(self, channel):
        self.send('NAMES' + channel)

    def invite(self, nick, channel):
        self.send('INVITE' + nick + '' + channel)

    def mode(self, channel, mode, nick=''):
        self.send('MODE' + channel + '' + mode + '' + nick)

    def kick(self, channel, nick, reason=''):
        self.send('KICK' + channel + '' + nick + '' + reason)

    def who(self, pattern):
        self.send('WHO' + pattern)

    def whois(self, nick):
        self.send('WHOIS' + nick)

    def whowas(self, nick):
        self.send('WHOWAS' + nick)
