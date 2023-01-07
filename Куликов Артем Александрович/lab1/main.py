import os
import random
from typing import Optional

BlockName = str
FileName = str


class Host():
    _block_status = {'empty': True, 'used': False}

    def __init__(self, title, size: int=1280):
        self._blocks: dict[BlockName, bool] = {}
        self.title = title
        self.size = size
        self.alive = True
        self.host_dir = f"{self.title}/"
        if not os.path.exists(self.host_dir):
            os.mkdir(self.host_dir)

    def write_block(self, block_name, data):
        self._blocks[block_name] = self._block_status['used']
        with open(self.host_dir + block_name, 'w', encoding="utf-8") as way:
            way.write(data)

    def del_block(self, block_name: BlockName):
        self._blocks[block_name] = self._block_status['empty']
        os.remove(self.host_dir + block_name)

    def read_block(self, block_name):
        with open(self.host_dir + block_name, encoding='utf-8') as way:
            return way.read()

    def count_free_blocks(self):
        return len([value for value in self._blocks.values() if value])
    def __str__(self):
        return f'Host: title="{self.title}"; is alive:{self.alive}'

class Block():
    def __init__(self, number: int, host: Host, file_name: str = ''):
        self.host = host
        self.number = number
        self.title = f"block_{self.number}"
        self.file_name = file_name
        self.replicas: list[Block] = []


class NameNode():

    def __init__(self, block_size=128):
        self._hosts: dict[Host, list[Block]] = {}
        self._files: dict[FileName, list[Block]] = {}
        self._blocks: list[Block] = []
        self._replications = 3
        self.block_size = block_size

    def get_host_list(self):
        return list([host for host in self._hosts.keys()])

    def get_blocks_free(self, host: Optional[Host] = None):
        blocks = []
        for block in self._blocks:
            if host is not None and block.host != host:
                continue
            if not block.file_name:
                blocks.append(block)
        return blocks

    def get_blocks_used(self):
        blocks = []
        for k in self._blocks:
            if k.file_name:
                blocks.append(k)
        return blocks

    def initial_blocks_mapping(self):
        for host, host_blocks in self._hosts.items():
            host_blocks_count = host.size // self.block_size
            for i in range(host_blocks_count + 1):
                new_block = Block(number=i, host=host)
                host._blocks[new_block.title] = True
                self._hosts[host].append(new_block)
                self._blocks.append(new_block)

    def cleanup(self):
        for host, blocks in self._hosts.items():
            for block in blocks:
                if block.file_name:
                    host.del_block(block.title)
                    block.file_name = ""
        self._files = {}

    def get_file_blocks(self, file_name) -> dict[Host, list[Block]]:
        hosts = {}
        file_blocks = self._files[file_name]
        for block in file_blocks:
            if block.host not in hosts:
                hosts[block.host] = [block]
            else:
                hosts[block.host].append(block)
        return hosts

    def add_host(self, host):
        if host not in self._hosts.keys():
            self._hosts[host] = []
            return 'OK'
        return 'Already in'

    def replicate_block(self, block,file_name,data):
        potential_replica_hosts = self.get_host_list()
        potential_replica_hosts.remove(block.host)

        replica_hosts: list[Host] = list(
            dict(
                sorted(
                    {
                        host: host.count_free_blocks() for host in potential_replica_hosts
                    }.items(),
                    key=lambda item: item[1],
                    reverse=True,
                )
            ).keys()
        )[:3]

        for r_host in replica_hosts:
            r_block = self.get_blocks_free(host=r_host)[0]
            r_block.file_name = f"replica_{file_name}_{random.random()}"
            block.replicas.append(r_block)
            r_host.write_block(r_block.title, data)

    def complete(self, file_name):
        self._files[file_name] = []
        for block in self._blocks:
            if block.file_name == file_name:
                self._files[file_name].append(block)

    def split_file(self, file_name, file_size):
        current_blocks = []
        count_blocks = file_size // self.block_size + (file_size % self.block_size !=0)
        for block in self.get_blocks_free()[0:count_blocks]:
            block.file_name = file_name
            current_blocks.append(block)
        return current_blocks


class Client():

    def __init__(self, name):
        self._nnode: Optional[NameNode] = None
        self._name = name

    def connect(self, nnode):
        self._nnode = nnode
        # connect via socket

    def _check_connect(self):
        if self._nnode is None:
            raise ConnectionError("Go and connect first!")

    def create_hosts(self, hosts):
        self._check_connect()
        for host in hosts:
            self._nnode.add_host(host)
        self._nnode.initial_blocks_mapping()

    @staticmethod
    def get_data_block(block, host):
        if host.alive:
            return host.read_block(block.title)
        else:
            for block_replica in block.replicas:
                if not block_replica.host.alive:
                    continue
                return block_replica.host.read_block(block_replica.title)
            return "[RIP Block]"

    def read_file(self, file_name):
        self._check_connect()
        hosts = self._nnode.get_file_blocks(file_name)
        data = ''
        for host, blocks in hosts.items():
            for block in blocks:
                data_block = self.get_data_block(block, host)
                data += data_block
        return data

    def write_file(self, file_name, data):
        self._check_connect()
        current_blocks = self._nnode.split_file(file_name, len(data))
        offset = 0

        for block in current_blocks:
            data_block = data[offset: self._nnode.block_size+offset]
            offset +=self._nnode.block_size
            block.host.write_block(block.title, data_block)
            self._nnode.replicate_block(block, file_name, data_block)

        self._nnode.complete(file_name)

    def cleanup(self):
        self._nnode.cleanup()
