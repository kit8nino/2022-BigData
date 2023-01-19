from lb1 import Host, NameNode, Client

with open("1.txt", encoding="utf-8") as f_:
    test_data = f_.read()

with open("2.txt", encoding="utf-8") as f_:
    test_data2 = f_.read()

n_node = NameNode()
client = Client("user")
client.connect(n_node)
client.create_hosts(Host("host1", 10000), Host("host2", 11000), Host("host3", 12000))


file_name1 = "1.txt"
client.write_file(file_name1, test_data)

file_name2 = "2.txt"
client.write_file(file_name2, test_data2)

file_name3 = "3.txt"
client.write_file(file_name3, test_data)

print(client.read_file(file_name1))
print(client.read_file(file_name2))
print(client.read_file(file_name3))
