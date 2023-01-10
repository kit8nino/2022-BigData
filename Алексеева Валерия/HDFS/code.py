import os
import random
from typing import Optional, List

BlockName = str
FileName = str


class Host:
    _block_status = {"empty": True, "used": False}

    def __init__(self, title: str, size: int = 1280):
        self.blocks: dict[BlockName, bool] = {}
        self.title = title
        self.size = size
        self.is_alive = True

        self.host_dir = f"{self.title}/"
        if not os.path.exists(self.host_dir):
            os.mkdir(self.host_dir)

    def get_free_count(self):
        return len([value for value in self.blocks.values() if value])

    def write_block(self, BlockName: BlockName, data: str):
        self.blocks[BlockName] = self._block_status["used"]
        with open(self.host_dir + BlockName, "w", encoding="utf-8") as f:
            f.write(data)

    def del_block(self, BlockName: BlockName):
        self.blocks[BlockName] = self._block_status["empty"]
        os.remove(self.host_dir + BlockName)

    def read_block(self, BlockName: BlockName):
        with open(self.host_dir + BlockName, encoding="utf-8") as f:
            return f.read()

    def __repr__(self):
        return f'Host(title="{self.title}", is_alive={self.is_alive})'


class Block:
    def __init__(self, number: int, host: Host, FileName: str = ""):
        self.host = host
        self.number = number
        self.title = f"block_{self.number}"
        self.FileName = FileName
        self.replicas: list[Block] = []

    def __repr__(self):
        return f'Block(title="{self.title}", host={self.host}, FileName="{self.FileName}")'


class NameNode:
    def __init__(self, block_size: int = 128):
        self._hosts: dict[Host, list[Block]] = {}
        self._files: dict[FileName, list[Block]] = {}
        self._blocks: list[Block] = []
        self._replications = 3
        self.block_size = block_size

    def get_hosts(self):
        return [host for host in self._hosts.keys()]

    def get_blocks_used(self) -> List[Block]:
        blocks = []
        for block in self._blocks:
            if block.FileName:
                blocks.append(block)
        return blocks

    def get_blocks_free(self, host: Optional[Host] = None):
        blocks = []
        for block in self._blocks:
            if host is not None and block.host != host:
                continue
            if not block.FileName:
                blocks.append(block)
        return blocks

    def initial_blocks_mapping(self):
        for host, host_blocks in self._hosts.items():
            host_blocks_count = host.size // self.block_size
            for i in range(host_blocks_count + 1):
                new_block = Block(number=i, host=host)
                host.blocks[new_block.title] = True
                self._hosts[host].append(new_block)
                self._blocks.append(new_block)

    def cleanup(self):
        for host, blocks in self._hosts.items():
            for block in blocks:
                if block.FileName:
                    host.del_block(block.title)
                    block.FileName = ""
        self._files = {}

    def get_file_blocks(self, FileName):
        current_hosts = {}
        file_blocks = self._files[FileName]
        for block in file_blocks:
            if block.host not in current_hosts:
                current_hosts[block.host] = [block]
                continue
            current_hosts[block.host].append(block)

        return current_hosts

    def add_host(self, host: Host):
        if host not in self._hosts.keys():
            self._hosts[host] = []
            return "Ok"
        return "Already in"

    def replicate_block(self, block: Block, FileName: str, data: str):
        possible_replica_hosts = self.get_hosts()
        possible_replica_hosts.remove(block.host)

        replica_hosts: list[Host] = list(
            dict(
                sorted(
                    {
                        host: host.get_free_count() for host in possible_replica_hosts
                    }.items(),
                    key=lambda item: item[1],
                    reverse=True,
                )
            ).keys()
        )[:3]

        for replica_host in replica_hosts:
            replica_block = self.get_blocks_free(host=replica_host)[0]
            replica_block.FileName = f"replica_{FileName}_{random.random()}"
            block.replicas.append(replica_block)
            replica_host.write_block(replica_block.title, data)

    def complete(self, FileName):
        self._files[FileName] = []
        for block in self._blocks:
            if block.FileName == FileName:
                self._files[FileName].append(block)
        return True

    def split_file(self, FileName, fileSize):
        current_blocks = []
        blocks_count = fileSize // self.block_size + (fileSize % self.block_size != 0)
        for block in self.get_blocks_free()[:blocks_count]:
            block.FileName = FileName
            current_blocks.append(block)
        return current_blocks


class Client:
    def __init__(self, name: str):
        self._name_node: Optional[NameNode] = None
        self._name = name

    def connect(self, nameNode: NameNode):
        self._name_node = nameNode
        # connect via socket

    def _check_connect(self):
        if self._name_node is None:
            raise ConnectionError("No connect")

    def create_hosts(self, *hosts: Host):
        self._check_connect()
        for host in hosts:
            self._name_node.add_host(host)
        self._name_node.initial_blocks_mapping()

    @staticmethod
    def get_block_data(block: Block, host: Host):
        if host.is_alive:
            return host.read_block(block.title)

        for block_replica in block.replicas:
            if not block_replica.host.is_alive:
                continue
            return block_replica.host.read_block(block_replica.title)
        return "[block is lost]"

    def read_file(self, FileName: FileName):
        self._check_connect()
        hosts = self._name_node.get_file_blocks(FileName)
        file_data = ""
        for host, blocks in hosts.items():
            for block in blocks:
                block_data = self.get_block_data(block, host)
                file_data += block_data

        return file_data

    def write_file(self, FileName: FileName, data: str):
        self._check_connect()
        current_blocks = self._name_node.split_file(FileName, len(data))
        offset = 0

        for block in current_blocks:
            block_data = data[offset: self._name_node.block_size + offset]
            offset += self._name_node.block_size
            block.host.write_block(block.title, block_data)
            self._name_node.replicate_block(block, FileName, block_data)

        self._name_node.complete(FileName)

    def cleanup(self):
        self._name_node.cleanup()
