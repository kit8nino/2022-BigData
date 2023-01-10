from body import Host, NameNode, Client
with open("for_ex_1.txt", encoding="utf-8") as f_:
    test_data = f_.read()
n_node = NameNode()
client = Client("user")
client.connect(n_node)
host1 = Host("host1", 100000)
host2 = Host("host2", 100000)
host3 = Host("host3", 100000)
host4 = Host("host4", 100000)
client.create_hosts(host1, host2, host3, host4)
file_name = "for_ex_1.txt"
client.write_file(file_name, test_data)
res = client.read_file(file_name)
print(res + "\n")
host1.is_alive = False
res = client.read_file(file_name)
host2.is_alive = False
host3.is_alive = False
host4.is_alive = True
res = client.read_file(file_name)
print(res)