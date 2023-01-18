from code import Host, NameNode, Client

with open("file/d1.txt", encoding="utf-8") as f:
    data1 = f.read()

with open("file/d2.txt", encoding="utf-8") as f:
    data2 = f.read()

with open("file/d3.txt", encoding="utf-8") as f:
    data3 = f.read()

with open("file/d4.txt", encoding="utf-8") as f:
    data4 = f.read()

n_node = NameNode()
client = Client("User")
client.connect(n_node)
client.create_hosts(Host("host1", 11111), Host("host2", 11222), Host("host3", 11333), Host("host4", 11444))


file_name1 = "[1]data.txt"
client.write_file(file_name1, data1)

file_name2 = "[2]data.txt"
client.write_file(file_name2, data2)

file_name3 = "[3]data.txt"
client.write_file(file_name3, data3)

file_name4 = "[4]data.txt"
client.write_file(file_name4, data4)

print(client.read_file(file_name1))
print(client.read_file(file_name2))
print(client.read_file(file_name3))
print(client.read_file(file_name4))
