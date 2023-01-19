from main import Host, NameNode, Client

with open("tests/1.txt", encoding="utf-8") as file:
    data1 = file.read()

with open("tests/2.txt", encoding="utf-8") as file:
    data2 = file.read()

with open("tests/3.txt", encoding="utf-8") as file:
    data3 = file.read()

with open("tests/4.txt", encoding="utf-8") as file:
    data4 = file.read()

with open("tests/5.txt", encoding="utf-8") as file:
    data5 = file.read()

n_node = NameNode()
client = Client("User")
client.connect(n_node)
client.create_hosts(Host("host1", 10000), Host("host2", 12576), Host("host3", 11352), Host("host4", 13242), Host("host5", 13764))

file_name1 = "[1]data.txt"
client.write_file(file_name1, data1)

file_name2 = "[2]data.txt"
client.write_file(file_name2, data2)

file_name3 = "[3]data.txt"
client.write_file(file_name3, data3)

file_name4 = "[4]data.txt"
client.write_file(file_name4, data4)

file_name5 = "[5]data.txt"
client.write_file(file_name5, data5)

print(client.read_file(file_name1))
print(client.read_file(file_name2))
print(client.read_file(file_name3))
print(client.read_file(file_name4))
print(client.read_file(file_name5))