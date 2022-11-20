import os
import random
from typing import Optional

BLOCKNAME = str
FILENAME = str

class Host:
    _block_status = {"empty": True, "used": False}

    def __init__(self, title: str, size: int = 1280):
        self.blocks: dict[BLOCKNAME, bool] = {}
        self.title = title
        self.size = size
        self.is_alive = True

        # папки это типа хосты
        self.host_dir = f"{self.title}/"
        if not os.path.exists(self.host_dir):
            os.mkdir(self.host_dir)

    def get_free_count(self):
        return len([value for value in self.blocks.values() if value])

    def write_block(self, blockName: BLOCKNAME, data: str):
        self.blocks[blockName] = self._block_status["used"]
        with open(self.host_dir + blockName, "w", encoding="utf-8") as f:
            f.write(data)

    def del_block(self, blockName: BLOCKNAME):
        self.blocks[blockName] = self._block_status["empty"]
        os.remove(self.host_dir + blockName)

    def read_block(self, blockName: BLOCKNAME) -> str:
        with open(self.host_dir + blockName, encoding="utf-8") as f:
            return f.read()

    def __repr__(self):
        return f'Host(title="{self.title}", is_alive={self.is_alive})'


class Block:
    def __init__(self, number: int, host: Host, fileName: str = ""):
        self.host = host
        self.number = number
        self.title = f"block_{self.number}"
        self.fileName = fileName
        self.replicas: list[Block] = []

    def __repr__(self):
        return f'Block(title="{self.title}", host={self.host}, fileName="{self.fileName}")'

class NameNode:
    def __init__(self, block_size: int = 128):
        self._hosts: dict[Host, list[Block]] = {}
        self._files: dict[FILENAME, list[Block]] = {}
        self._blocks: list[Block] = []
        self._replications = 3
        self.block_size = block_size

    def get_hosts(self) -> list[Host]:
        return [host for host in self._hosts.keys()]

    def get_blocks_used(self) -> list[Block]:
        blocks = []
        for block in self._blocks:
            if block.fileName:
                blocks.append(block)
        return blocks

    def get_blocks_free(self, host: Optional[Host] = None) -> list[Block]:
        blocks = []
        for block in self._blocks:
            if host is not None and block.host != host:
                continue
            if not block.fileName:
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
                if block.fileName:
                    host.del_block(block.title)
                    block.fileName = ""
        self._files = {}

    def get_file_blocks(self, fileName) -> dict[Host, list[Block]]:
        current_hosts = {}
        file_blocks = self._files[fileName]
        for block in file_blocks:
            if block.host not in current_hosts:
                current_hosts[block.host] = [block]
                continue
            current_hosts[block.host].append(block)

        return current_hosts

    def add_host(self, host: Host) -> str:
        if host not in self._hosts.keys():
            self._hosts[host] = []
            return "OK"
        return "Already in"

    def replicate_block(self, block: Block, fileName: str, data: str):
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
            replica_block.fileName = f"replica_{fileName}_{random.random()}"
            block.replicas.append(replica_block)
            replica_host.write_block(replica_block.title, data)

    def complete(self, fileName):
        self._files[fileName] = []
        for block in self._blocks:
            if block.fileName == fileName:
                self._files[fileName].append(block)
        return True

    def split_file(self, fileName, fileSize) -> list[Block]:
        current_blocks = []
        blocks_count = fileSize // self.block_size + (fileSize % self.block_size != 0)
        for block in self.get_blocks_free()[:blocks_count]:
            block.fileName = fileName
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
            raise ConnectionError("Not connect!")

    def create_hosts(self, *hosts: Host):
        self._check_connect()
        for host in hosts:
            self._name_node.add_host(host)
        self._name_node.initial_blocks_mapping()

    @staticmethod
    def get_block_data(block: Block, host: Host) -> Optional[str]:
        if host.is_alive:
            return host.read_block(block.title)

        for block_replica in block.replicas:
            if not block_replica.host.is_alive:
                continue
            return block_replica.host.read_block(block_replica.title)
        return "[block is lost]"

    def read_file(self, fileName: FILENAME) -> str:
        self._check_connect()
        hosts = self._name_node.get_file_blocks(fileName)
        file_data = ""
        for host, blocks in hosts.items():
            for block in blocks:
                block_data = self.get_block_data(block, host)
                file_data += block_data

        return file_data

    def write_file(self, fileName: FILENAME, data: str):
        self._check_connect()
        current_blocks = self._name_node.split_file(fileName, len(data))
        offset = 0

        for block in current_blocks:
            block_data = data[offset : self._name_node.block_size + offset]
            offset += self._name_node.block_size
            block.host.write_block(block.title, block_data)
            self._name_node.replicate_block(block, fileName, block_data)

        self._name_node.complete(fileName)

    def cleanup(self):
        self._name_node.cleanup()







