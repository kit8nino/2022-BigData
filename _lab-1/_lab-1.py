"""
Классы, эмулирующие работу HDFS
"""


class NameNode():
    """
Хранится список живых DataNode
для каждой - список блоков на ней
общий список файлов
для каждого файла - список блоков, в котором он записан
для каждого блока - список хостов, на котором он есть
    """

    msgs = {'ok': 'OK', 'ardy_in': 'Host already in list',
            'nt_in_list': 'Element not in list', 'no_space':
            'Not enought free spce for file'}

    _block_size = 128  # Mb
    _replications = 3

    def __init__(self):
        self._hosts = {}
        self._files = {}
        # block size  = 128 Mb
        self._blocks = {}

    def get_block_size(self):
        return self._block_size

    def add_host(self, h):
        if h not in self._hosts.keys():
            self._hosts[h] = []
            return self.msgs['ok']
        else:
            return self.msgs['ardy_in']

    def del_host(self, h):
        with self._hosts.keys() as hs:
            if h in hs:
                del self._hosts[h]
                return self.msgs['ok']

    def set_hosts(self, hosts):
        for h in hosts:
            if h not in self._hosts.keys():
                self._hosts[h] = []

    def get_hosts(self):
        return self._hosts.keys()

    def get_blocks(self):
        return self._blocks

    def get_free_blocks(self, n, cli_name):
        with self._blocks as bl:
            h = []
            for k, v in bl.items:
                if not v and len(h) < n:
                    bl[k] = [cli_name]
                    h.append[k]
        if len(h) < n:
            return self.msgs['no_space']
        return h

    def get_hosts_to_write(self, b):
        h = []
        for k, v in sorted(self._hosts.items(), key=lambda x: len(x[1])):
            h.append(k)
            if len(h) == len(b):
                return h

    def check_replications(self):
        """
        Проверка, что каждый файл реплицирован N раз
        если нет, команда хостам дозаписать
        """
        pass

    def file_alloc(self, cli_name, file_name, file_size):
        """
        Посчитать блоки, вернуть список блоков,
        вернуть список хостов, на которые эти блоки надо записать
        """

        num_of_blocks_to_reserve = file_size // self._block_size + \
            (file_size % self._block_size != 0)
        b = self.get_free_blocks(num_of_blocks_to_reserve, cli_name)
        h = self.get_hosts_to_write(b)
        self.check_replications()
        return b, h

    def complete(self, cli_name, file_name):
        """
        занесение в список блоков, файлов и хостов
        информации о последней операции
        вызов проверки репликации
        """
        pass

    def build_blocks_hosts(self):
        """
        Первоначальный подсчет объема памяти
        произвoльное разбиение блоков по хостам (с занесением в оба списка)
        пометка 'free' у каждого незанятого блока

        """
    pass


class DataNode():

    def write_blocks(self, blocks):
        self.blocks.append(blocks)
        pass
    pass


class Client():

    def __init__(self, name='Client1', files=[]):
        self.name = name
        self._files = files

    def write_file(self, file, nnode, data_nodes):
        blocks, hosts = nnode.file_alloc(self.name, file['name'], file['size'])
        blocks_to_write = self.write_blocks(blocks, file['data'],
                                            nnode.get_block_size())
        for h, b in zip(hosts, blocks_to_write):
            data_nodes[h].write(b)
        nnode.complete(self.name, file['name'])
        return 'OK'

    def write_blocks(self, blocks, data, size_of_block):
        db = bytes(data)
        blocks_with_data = []
        for i in range(len(blocks)):
            blocks_with_data.append(db[i*size_of_block, (i+1)*size_of_block])
        return blocks_with_data
    pass


class Connector():

    def __init__(self, nnode, clients, hosts):
        self.nnode = nnode
        self.clients = clients
        self.hosts = hosts
