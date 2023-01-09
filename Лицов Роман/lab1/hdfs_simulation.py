import os
import random
from typing import Optional

BLOCK_NAME = str
FILE_NAME = str


class Host:
    _block_status = {"empty": True, "used": False}

    def __init__(self, title: str, size: int = 1280):
        self.blocks: dict[BLOCK_NAME, bool] = {}
        self.title = title
        self.size = size
        self.is_alive = True

        
        self.host_dir = f"{self.title}/"
        if not os.path.exists(self.host_dir):
            os.mkdir(self.host_dir)

    def get_free_count(self) -> int:
        return len([value for value in self.blocks.values() if value])

    def write_block(self, block_name: BLOCK_NAME, data: str):
        self.blocks[block_name] = self._block_status["used"]
        with open(self.host_dir + block_name, "w", encoding="utf-8") as f:
            f.write(data)

    def del_block(self, block_name: BLOCK_NAME):
        self.blocks[block_name] = self._block_status["empty"]
        os.remove(self.host_dir + block_name)

    def read_block(self, block_name: BLOCK_NAME) -> str:
        with open(self.host_dir + block_name, encoding="utf-8") as f:
            return f.read()

    def __repr__(self) -> str:
        return f'Host(title="{self.title}", is_alive={self.is_alive})'


class Block:
    def __init__(self, number: int, host: Host, file_name: FILE_NAME = ""):
        self.host = host
        self.number = number
        self.title = f"block_{self.number}"
        self.file_name = file_name
        self.replicas: list[Block] = []

    def __repr__(self) -> str:
        return f'Block(title="{self.title}", host={self.host}, file_name="{self.file_name}")'


class NameNode:
    def __init__(self, block_size: int = 128):
        self._hosts: dict[Host, list[Block]] = {}
        self._files: dict[FILE_NAME, list[Block]] = {}
        self._blocks: list[Block] = []
        self._replications = 3
        self.block_size = block_size

    def get_hosts(self) -> list[Host]:
        return [host for host in self._hosts.keys()]

    def get_blocks_used(self) -> list[Block]:
        blocks = []
        for block in self._blocks:
            if block.file_name:
                blocks.append(block)
        return blocks

    def get_blocks_free(self, host: Optional[Host] = None) -> list[Block]:
        blocks = []
        for block in self._blocks:
            if host is not None and block.host != host:
                continue
            if not block.file_name:
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
                if block.file_name:
                    host.del_block(block.title)
                    block.file_name = ""
        self._files = {}

    def get_file_blocks(self, file_name: FILE_NAME) -> dict[Host, list[Block]]:
        current_hosts = {}
        file_blocks = self._files[file_name]
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

    def replicate_block(self, block: Block, file_name: FILE_NAME, data: str):
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
        )[:self._replications]

        for replica_host in replica_hosts:
            replica_host_free_blocks = self.get_blocks_free(host=replica_host)
            if not replica_host_free_blocks:
                continue
            replica_block = replica_host_free_blocks[0]
            replica_block.file_name = f"replica_{file_name}_{random.random()}"
            block.replicas.append(replica_block)
            replica_host.write_block(replica_block.title, data)

    def complete(self, file_name: FILE_NAME):
        self._files[file_name] = []
        for block in self._blocks:
            if block.file_name == file_name:
                self._files[file_name].append(block)

    def split_file(self, file_name: FILE_NAME, file_size: int) -> list[Block]:
        current_blocks = []
        blocks_count = file_size // self.block_size + (file_size % self.block_size != 0)
        for block in self.get_blocks_free()[:blocks_count]:
            block.file_name = file_name
            current_blocks.append(block)
        return current_blocks


class Client:
    def __init__(self, name: str):
        self._name_node: Optional[NameNode] = None
        self._name = name

    def connect(self, name_node: NameNode):
        self._name_node = name_node
        

    def _check_connect(self):
        if self._name_node is None:
            raise ConnectionError("Go and connect first!")

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
        return "[блок утерян]"

    def read_file(self, file_name: FILE_NAME) -> str:
        self._check_connect()
        hosts = self._name_node.get_file_blocks(file_name)
        file_data = ""
        for host, blocks in hosts.items():
            for block in blocks:
                block_data = self.get_block_data(block, host)
                file_data += block_data

        return file_data

    def write_file(self, file_name: FILE_NAME, data: str):
        self._check_connect()
        current_blocks = self._name_node.split_file(file_name, len(data))
        offset = 0

        for block in current_blocks:
            block_data = data[offset : self._name_node.block_size + offset]
            offset += self._name_node.block_size
            block.host.write_block(block.title, block_data)
            self._name_node.replicate_block(block, file_name, block_data)

        self._name_node.complete(file_name)

    def cleanup(self):
        self._name_node.cleanup()