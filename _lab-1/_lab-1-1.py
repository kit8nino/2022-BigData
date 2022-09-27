class NameNode():

    _hosts = {}
    _files = {}
    _blocks = {}
    _hosts_alive = {'h': True}
    _block_size = 128
    _replications = 3

    def __init__(self, block_size=128):
        self._block_size = block_size

    def get_hosts_names(self):
        return self._hosts.keys()

    def get_blocks_used(self):
        b = []
        for k, v in self._blocks.items():
            if v[1]:
                b.append(k)
        return b

    def get_blocks_free(self):
        b = []
        for k, v in self._blocks.items():
            if not v[1]:
                b.append(k)
        return b

    def initial_blocks_mapping(self):
        pass

    def cleanup(self):
        pass

    def is_alive(self, host):
        if self._hosts_alive:
            return True
        return False
        
    def get_file_blocks(self, file_name):
        b, h = [], {}
        b = self._blocks[file_name]
        for k, v in self._hosts.items():
            if k in b:
                h[b] = v
        return h
        
    def add_host(self, h):
        if h not in self._hosts.keys():
            self._hosts[h] = []
            return 'OK'
        return 'Already in'

    def complete(self, cli, file_name):
        self._files[file_name] = []
        for k, v in self._blocks.items():
            if v[1] == file_name:
                self._files[file].append(k)

    def split_file(self, cli, file_name, file_size):
        n = file_size // self._block_size + (file_size % self._block_size != 0)
        for b in self.get_blocks_free()[0:n]:
            self._blocks[b][1] = file_name


class Host():

    _blocks = {}
    _block_status = {'empty': True, 'used': False}

    def __init__(self, nnode):
        self._name_node = nnode

    def write_block(self, b, data):
        self._blocks[b] = self._block_status['used']
        # open(file_b, 'w').write(data)

    def del_block(self, b):
        self._blocks[b] = self._block_status['empty']

    def read_block(self, b):
        # data = read_file(b)
        # return data
        pass


class Client():

    _name = 'Vova'
    _nnode = ''

    def __init__(self, name='Vova'):
        self._name = name

    def connect(self, nnode):
        self._nnode = nnode
        # connect via socket

    def read_file(self, file_name):
        if not self._nnode:
            return "Go and connect first!"
        h = self._nnode.get_file_blocks(file_name)
        file = []
        for k, v in h.items():
            for h in v:
                if self._nnode.is_alive(h):
                    file.append(h.read_block(k))
                    break
        return file

    def write_file(self, file):
        self

# n = NameNode()
# n.complete('a', 'f')
