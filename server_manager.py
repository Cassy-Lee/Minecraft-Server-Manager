import http.server
import rcon
import mcstatus
import subprocess

SERVER_CMD=r'"C:\\Program Files\\Java\\jre1.8.0_351\\bin\\java.exe" -jar "D:\\Download\\s\\server\\flying-road-3 server\\forge-1.12.2-14.23.5.2860.jar" nogui'
SERVER_CWD=r'D:\Download\s\server\flying-road-3 server'

class MinecraftServerManager:
    'Minecraft server manager.'
    def __init__(self,
        serverCmd:str,
        serverCwd:str='.',
        serverPort:int=None,
        pingTimeout:float=3,
        enableQuery:bool=False,
        queryPort:int=None,
        queryTimeout:float=3,
        enableRcon:bool=False,
        rconPort:int=None,
        rconPassword:str='',
        rconTimeout:int=3
        showConsole:bool=True):
        '''args:
    serverCmd: Command to start server.
    serverCwd: Where server should run.
        Defalt: Current path
    serverPort: The port server run.
        Allows get information by ping.
        (Set in server.properties)
    pingTimeout: Max time in second when waiting ping.
        Defalt: 3
    enableQuery: Allows get information by query.
        If true, queryPort must be set.
        (Set in server.properties)
    queryPort: The port query listener run.
        (Set in server.properties)
    queryTimeout: Max time in second when waiting query.
        Defalt: 3
    enableRcon: Allow remote console to control server.
        Allows the stop method stop server in normal way.
        If true, rconPort and rconPassword must be set.
        (Set in server.properties)
    rconPort: The port rcon run.
        (Set in server.properties)
    rconPassword: The password to login rcon.
        (Set in server.properties)
    rconTimeout: Max time in second when waiting rcon.
        Defalt: 3
    showConsole: Show server console'''
        self.serverCmd=serverCmd
        self.serverCwd=serverCwd
        self.serverPort=serverPort
        #init ping
        self.pingTimeout=pingTimeout
        if self.serverPort is not None:
            self.pingStatus=mcstatus.JavaServer.lookup(f'localhost:{self.serverPort}',timeout=self.pingTimeout)
        #init query
        self.enableQuery=enableQuery
        self.queryPort=queryPort
        self.queryTimeout=queryTimeout
        if self.enableQuery:
            assert self.queryPort is not None,'Query port must be set if enable query.'
            self.queryStatus=mcstatus.JavaServer.lookup(f'localhost:{self.queryPort}',timeout=self.queryTimeout)
        #init rcon
        self.enableRcon=enableRcon
        self.rconPort=rconPort
        self.rconPassword=rconPassword
        self.rconTimeout=rconTimeout
        if self.enableRcon:
            assert self.rconPort is not None,'Rcon port must be set if enable rcon.'
            assert len(self.rconPassword)>0,'Rcon password must be set if enable rcon.'
            self.rconClient=rcon.source.Client('localhost',rconPort)
            self.rconClient.passwd=self.rconPassword
        #other settings
        self.showConsole=showConsole
    def start(self):
        'Start server.'
        assert self.serverProcess is None or self.serverProcess.poll() is not None,'Server already started.'
        self.serverProcess=subprocess.Popen(
            self.serverCmd,
            cwd=self.serverCwd,
            stdin=None if self.showConsole else subprocess.DEVNULL
            stdout=None if self.showConsole else subprocess.DEVNULL
            stderr=None if self.showConsole else subprocess.DEVNULL
            creationflags=subprocess.NORMAL_PRIORITY_CLASS|(subprocess.CREATE_NEW_CONSOLE if self.showConsole else 0)
        )
        return 'Success!'
    def wait(self,forceRcon:bool=False,forceQuery:bool=False,forcePing:bool=False):
        'Wait server loaded'
        if forceRcon:
            assert self.enableRcon,''
                rconClient.timeout=1
                while self.serverProcess.poll() is None:
                    try:
                        rconClient.connect(True)
                    except ConnectionRefusedError:
                        pass
                    else:
                        break
        elif self.enableQuery:
            while self.serverProcess.poll() is None:
                try:
                    self(True)
                except:
                    pass
                else:
                    break
    def stop(self,forceRcon:bool=False):
        'Stop server. Use Rcon if enable and connected.'
        assert self.serverProcess is not None and self.serverProcess.poll() is None,'Server hasn\'t started yet.'
        try:
            assert enableRcon,'Rcon isn\'t enabled.'
                try:
                    rconClient.run('')
                except OSError as e:
                    assert e.errno==10057