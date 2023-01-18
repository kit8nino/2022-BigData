from body import Host, NameNode, Client
with open("for_ex_2(1).txt", encoding="utf-8") as f_:
    test_data = f_.read()
with open("for_ex_2(2).txt", encoding="utf-8") as f_:
    test_data2 = f_.read()
n_node = NameNode()
client = Client("user")
client.connect(n_node)
client.create_hosts(Host("host1", 100000), Host("host2", 100000))
file_name1 = "for_ex_2(1).txt"
client.write_file(file_name1, test_data)
file_name2 = "for_ex_2(2).txt"
client.write_file(file_name2, test_data2)
print(client.read_file(file_name1))
print(client.read_file(file_name2))