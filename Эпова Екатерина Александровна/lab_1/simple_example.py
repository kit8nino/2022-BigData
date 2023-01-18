from hdfs_simulation import Host, NameNode, Client

with open("assets/test_data.txt", encoding="utf-8") as f_:
    test_data = f_.read()

with open("assets/test_data2.txt", encoding="utf-8") as f_:
    test_data2 = f_.read()

n_node = NameNode()
client = Client("user")
client.connect(n_node)
client.create_hosts(Host("host1", 12800), Host("host2", 25600))


file_name1 = "test.txt"
client.write_file(file_name1, test_data)

file_name2 = "test2.txt"
client.write_file(file_name2, test_data2)


print(client.read_file(file_name1))
print(client.read_file(file_name2))
